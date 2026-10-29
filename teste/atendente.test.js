// Simula clientes no WhatsApp, com Redis, WhatsApp e Claude de mentira.
// Rodar: npm test

import { test } from "node:test";
import assert from "node:assert/strict";
import { createHmac } from "node:crypto";
import { criarMemoria } from "../api/_lib/memoria.js";
import { lerEventos, assinaturaValida } from "../api/_lib/whatsapp.js";
import { tratarEventos } from "../api/_lib/atendente.js";

class RedisFalso {
  dados = new Map();
  async set(chave, valor, { nx } = {}) {
    if (nx && this.dados.has(chave)) return null;
    this.dados.set(chave, valor);
    return "OK";
  }
  async get(chave) {
    return this.dados.get(chave) ?? null;
  }
  async del(chave) {
    this.dados.delete(chave);
  }
  async expire() {}
  async rpush(chave, valor) {
    this.dados.set(chave, [...(this.dados.get(chave) ?? []), valor]);
  }
  async lpop(chave, quantidade) {
    const lista = this.dados.get(chave) ?? [];
    this.dados.set(chave, lista.slice(quantidade));
    return lista.length ? lista.slice(0, quantidade) : null;
  }
  async llen(chave) {
    return (this.dados.get(chave) ?? []).length;
  }
}

// Claude falso: devolve as respostas da lista, uma por chamada
function claudeFalso(respostas) {
  const pedidos = [];
  return {
    pedidos,
    messages: {
      async create(pedido) {
        pedidos.push(structuredClone(pedido));
        const resposta = respostas.shift();
        if (resposta instanceof Error) throw resposta;
        return resposta;
      },
    },
  };
}

const texto = (t) => ({ stop_reason: "end_turn", content: [{ type: "text", text: t }] });

function montar(respostas) {
  const enviadas = [];
  const memoria = criarMemoria(new RedisFalso());
  const claude = claudeFalso(respostas);
  const deps = {
    memoria,
    claude,
    whatsapp: { enviarTexto: async (telefone, t) => enviadas.push({ telefone, texto: t }) },
    agora: () => new Date("2026-10-29T17:32:00Z"),
    esperaMs: 0,
  };
  return { deps, enviadas, claude, memoria };
}

function avisoDaMeta(mensagens, nome = "Ana") {
  return {
    entry: [
      {
        changes: [
          {
            field: "messages",
            value: { contacts: [{ wa_id: "5551988887777", profile: { name: nome } }], messages: mensagens },
          },
        ],
      },
    ],
  };
}

const msg = (id, corpo) => ({ id, from: "5551988887777", type: "text", text: { body: corpo } });

test("responde uma dúvida simples com data, hora e nome do cliente", async () => {
  const { deps, enviadas, claude } = montar([texto("Oi, Ana! Abrimos de segunda a sexta, das 9h às 18h.")]);
  await tratarEventos(lerEventos(avisoDaMeta([msg("m1", "que horas vcs abrem?")])), deps);

  assert.deepEqual(enviadas, [{ telefone: "5551988887777", texto: "Oi, Ana! Abrimos de segunda a sexta, das 9h às 18h." }]);
  const pedido = claude.pedidos[0];
  assert.equal(pedido.model, "claude-haiku-5-5");
  assert.match(pedido.messages[0].content, /^\[quinta-feira, 29\/10\/2026, 14:32 · cliente: Ana\]\nque horas vcs abrem\?$/);
});

test("junta mensagens seguidas numa resposta só e lembra da conversa", async () => {
  const { deps, enviadas, claude } = montar([texto("Qual o modelo?"), texto("Certo, iPhone 13.")]);
  await tratarEventos(lerEventos(avisoDaMeta([msg("m1", "oi"), msg("m2", "minha tela quebrou")])), deps);
  await tratarEventos(lerEventos(avisoDaMeta([msg("m3", "iphone 13")])), deps);

  assert.equal(enviadas.length, 2);
  assert.match(claude.pedidos[0].messages[0].content, /oi\n\n\[.*\]\nminha tela quebrou/);
  const segundo = claude.pedidos[1].messages;
  assert.equal(segundo.length, 3);
  assert.equal(segundo[1].role, "assistant");
  assert.match(segundo[2].content, /iphone 13$/);
});

test("mensagem repetida pela Meta não é respondida duas vezes", async () => {
  const { deps, enviadas } = montar([texto("Oi!")]);
  const aviso = avisoDaMeta([msg("m1", "oi")]);
  await tratarEventos(lerEventos(aviso), deps);
  await tratarEventos(lerEventos(aviso), deps);
  assert.equal(enviadas.length, 1);
});

test("chama o atendente, se despede e para de responder", async () => {
  const { deps, enviadas, claude, memoria } = montar([
    {
      stop_reason: "tool_use",
      content: [
        {
          type: "tool_use",
          id: "t1",
          name: "chamar_atendente",
          input: { motivo: "orcamento_conserto", resumo: "iPhone 13, tela quebrada, toque funcionando" },
        },
      ],
    },
    texto("Pronto! Um atendente já vai te passar o orçamento."),
  ]);
  await tratarEventos(lerEventos(avisoDaMeta([msg("m1", "quanto fica a tela do iphone 13?")])), deps);

  assert.deepEqual(enviadas.map((e) => e.texto), ["Pronto! Um atendente já vai te passar o orçamento."]);
  assert.equal(claude.pedidos[1].messages[2].content[0].type, "tool_result");
  assert.equal(await memoria.pausado("5551988887777"), true);

  await tratarEventos(lerEventos(avisoDaMeta([msg("m2", "e a bateria?")])), deps);
  assert.equal(enviadas.length, 1);
  assert.equal(claude.pedidos.length, 2);
});

test("quando a loja responde pelo app, a IA sai da conversa", async () => {
  const { deps, enviadas } = montar([]);
  await tratarEventos(
    lerEventos({
      entry: [{ changes: [{ field: "smb_message_echoes", value: { message_echoes: [{ from: "5551995255010", to: "5551988887777" }] } }] }],
    }),
    deps,
  );
  await tratarEventos(lerEventos(avisoDaMeta([msg("m1", "obrigado!")])), deps);
  assert.equal(enviadas.length, 0);
});

test("se o Claude falhar, avisa o cliente e passa para a loja", async () => {
  const { deps, enviadas, memoria } = montar([new Error("fora do ar")]);
  await tratarEventos(lerEventos(avisoDaMeta([msg("m1", "oi")])), deps);
  assert.equal(enviadas.length, 1);
  assert.match(enviadas[0].texto, /atendente/);
  assert.equal(await memoria.pausado("5551988887777"), true);
});

test("troca **negrito** do markdown pelo *negrito* do WhatsApp", async () => {
  const { deps, enviadas } = montar([texto("Fazemos a troca no **mesmo dia**.")]);
  await tratarEventos(lerEventos(avisoDaMeta([msg("m1", "demora?")])), deps);
  assert.equal(enviadas[0].texto, "Fazemos a troca no *mesmo dia*.");
});

test("áudio vira um aviso para a IA pedir texto; reação é ignorada", () => {
  const eventos = lerEventos(
    avisoDaMeta([
      { id: "a1", from: "5551988887777", type: "audio", audio: {} },
      { id: "r1", from: "5551988887777", type: "reaction", reaction: { emoji: "👍" } },
    ]),
  );
  assert.equal(eventos.length, 1);
  assert.match(eventos[0].texto, /áudio/);
});

test("confere a assinatura da Meta", () => {
  const corpo = '{"entry":[]}';
  const assinatura = "sha256=" + createHmac("sha256", "segredo").update(corpo).digest("hex");
  assert.equal(assinaturaValida(corpo, assinatura, "segredo"), true);
  assert.equal(assinaturaValida(corpo, assinatura, "outro"), false);
  assert.equal(assinaturaValida(corpo, null, "segredo"), false);
});
