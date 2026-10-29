// O atendimento em si: junta as mensagens do cliente, pergunta ao Claude e responde.

import { INSTRUCOES, FERRAMENTAS } from "./conhecimento.js";

const MODELO = "claude-haiku-5-5"; // rápido e barato; para respostas mais caprichadas: "claude-sonnet-5-5"
const ESPERA_MS = 2500; // espera o cliente terminar de digitar antes de responder
const LIMITE_HISTORICO = 80; // conversa muito longa recomeça do zero
const MSG_ERRO = "Oi! Já já um atendente da loja te responde por aqui. 😊";

export async function tratarEventos(eventos, deps) {
  for (const evento of eventos) {
    if (evento.tipo === "loja_respondeu") {
      await deps.memoria.pausar(evento.telefone, "loja_respondeu");
    }
  }

  const clientes = new Set();
  for (const evento of eventos) {
    if (evento.tipo !== "mensagem") continue;
    if (!liberado(evento.telefone, deps.liberados)) continue; // modo de teste: só os números liberados
    if (!(await deps.memoria.primeiraVez(evento.id))) continue;
    if (await deps.memoria.pausado(evento.telefone)) continue; // um humano está atendendo

    // Não marcamos como lida: assim a conversa continua aparecendo para a loja no app
    await deps.memoria.enfileirar(evento.telefone, cabecalho(evento, deps.agora()) + evento.texto);
    clientes.add(evento.telefone);
  }

  await Promise.all([...clientes].map((telefone) => atenderFila(telefone, deps)));
}

// Responde tudo o que estiver na fila do cliente. Se outra execução já está
// respondendo esse cliente, ela mesma pega as mensagens novas.
async function atenderFila(telefone, deps) {
  const { memoria } = deps;
  while (await memoria.travar(telefone)) {
    try {
      await esperar(deps.esperaMs ?? ESPERA_MS);
      let textos;
      while ((textos = await memoria.retirarFila(telefone)).length > 0) {
        if (await memoria.pausado(telefone)) break;
        await responder(telefone, textos.join("\n\n"), deps);
      }
    } finally {
      await memoria.destravar(telefone);
    }
    if (!(await memoria.temFila(telefone)) || (await memoria.pausado(telefone))) return;
  }
}

async function responder(telefone, texto, deps) {
  const { memoria, whatsapp, claude } = deps;

  let mensagens = await memoria.historico(telefone);
  if (mensagens.length > LIMITE_HISTORICO) mensagens = [];
  // O histórico só cresce: o Claude exige que as mensagens antigas não mudem
  mensagens = [...mensagens, { role: "user", content: texto }];

  for (let rodada = 0; rodada < 4; rodada++) {
    let resposta;
    try {
      resposta = await claude.messages.create({
        model: MODELO,
        max_tokens: 16000,
        output_config: { effort: "low" },
        cache_control: { type: "ephemeral" },
        system: INSTRUCOES,
        tools: FERRAMENTAS,
        messages: mensagens,
      });
    } catch (erro) {
      console.error("Erro ao falar com o Claude:", erro);
      await passarParaHumano(telefone, "erro", deps);
      return;
    }

    if (resposta.stop_reason === "refusal") {
      await passarParaHumano(telefone, "recusa", deps);
      return;
    }

    mensagens = [...mensagens, { role: "assistant", content: resposta.content }];

    const fala = resposta.content
      .filter((bloco) => bloco.type === "text")
      .map((bloco) => bloco.text)
      .join("\n\n")
      .trim();
    if (fala) await whatsapp.enviarTexto(telefone, paraWhatsApp(fala));

    const chamadas = resposta.content.filter((bloco) => bloco.type === "tool_use");
    if (resposta.stop_reason !== "tool_use" || chamadas.length === 0) break;

    const resultados = [];
    for (const chamada of chamadas) {
      resultados.push(await executarFerramenta(telefone, chamada, deps));
    }
    mensagens = [...mensagens, { role: "user", content: resultados }];
  }

  await memoria.salvarHistorico(telefone, mensagens);
}

async function executarFerramenta(telefone, chamada, deps) {
  if (chamada.name === "chamar_atendente") {
    const { motivo, resumo } = chamada.input;
    await deps.memoria.pausar(telefone, motivo);
    console.log(`[ATENDENTE] ${telefone} · ${motivo} · ${resumo}`);
    return {
      type: "tool_result",
      tool_use_id: chamada.id,
      content: "Atendente avisado. A partir de agora a conversa fica com ele; despeça-se do cliente em uma frase.",
    };
  }
  return { type: "tool_result", tool_use_id: chamada.id, content: "Ferramenta desconhecida.", is_error: true };
}

async function passarParaHumano(telefone, motivo, deps) {
  await deps.memoria.pausar(telefone, motivo);
  await deps.whatsapp.enviarTexto(telefone, MSG_ERRO).catch((erro) => console.error(erro));
  console.log(`[ATENDENTE] ${telefone} · ${motivo} · a IA não conseguiu responder`);
}

// Modo de teste: com a lista preenchida, a IA só responde a esses números.
// Lista vazia = responde a todos.
function liberado(telefone, liberados = []) {
  return liberados.length === 0 || liberados.some((numero) => mesmoNumero(numero, telefone));
}

// Compara números ignorando sinais e o 9 dos celulares do Brasil, que o WhatsApp às vezes omite
// (ex.: +55 51 98349-6440 chega como 555183496440)
function mesmoNumero(a, b) {
  const normalizar = (numero) => {
    const digitos = String(numero).replace(/\D/g, "");
    return digitos.length === 13 && digitos.startsWith("55") && digitos[4] === "9"
      ? digitos.slice(0, 4) + digitos.slice(5)
      : digitos;
  };
  return normalizar(a) === normalizar(b);
}

// Ex.: "[quinta-feira, 29/10/2026, 14:32 · cliente: Ana]\n"
function cabecalho(evento, agora) {
  const quando = new Intl.DateTimeFormat("pt-BR", {
    timeZone: "America/Sao_Paulo",
    weekday: "long",
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(agora);
  const nome = evento.nome ? ` · cliente: ${evento.nome}` : "";
  return `[${quando}${nome}]\n`;
}

// O WhatsApp usa *um* asterisco para negrito
function paraWhatsApp(texto) {
  return texto.replace(/\*\*(.+?)\*\*/g, "*$1*");
}

function esperar(ms) {
  return new Promise((resolver) => setTimeout(resolver, ms));
}
