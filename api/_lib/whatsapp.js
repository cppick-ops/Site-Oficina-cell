// Conversa com a WhatsApp Cloud API (Meta).

import { createHmac, timingSafeEqual } from "node:crypto";

export function criarWhatsApp({ token, idNumero, versao = "v25.0", fetch = globalThis.fetch }) {
  async function enviar(corpo) {
    const resposta = await fetch(`https://graph.facebook.com/${versao}/${idNumero}/messages`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
      body: JSON.stringify({ messaging_product: "whatsapp", ...corpo }),
    });
    if (!resposta.ok) {
      throw new Error(`WhatsApp respondeu ${resposta.status}: ${await resposta.text()}`);
    }
  }

  return {
    async enviarTexto(telefone, texto) {
      await enviar({ to: telefone, type: "text", text: { body: texto } });
    },
  };
}

// Confere se o aviso veio mesmo da Meta (cabeçalho X-Hub-Signature-256)
export function assinaturaValida(corpo, assinatura, segredo) {
  if (!assinatura || !segredo) return false;
  const esperada = "sha256=" + createHmac("sha256", segredo).update(corpo).digest("hex");
  return esperada.length === assinatura.length && timingSafeEqual(Buffer.from(esperada), Buffer.from(assinatura));
}

// Transforma o aviso da Meta numa lista simples de eventos
export function lerEventos(dados) {
  const eventos = [];
  for (const entrada of dados.entry ?? []) {
    for (const mudanca of entrada.changes ?? []) {
      const valor = mudanca.value ?? {};

      if (mudanca.field === "messages") {
        const nomes = Object.fromEntries((valor.contacts ?? []).map((c) => [c.wa_id, c.profile?.name]));
        for (const msg of valor.messages ?? []) {
          const texto = textoDaMensagem(msg);
          if (texto) {
            eventos.push({ tipo: "mensagem", id: msg.id, telefone: msg.from, nome: nomes[msg.from], texto });
          }
        }
      }

      // Com o número no app WhatsApp Business (coexistência), a Meta avisa quando
      // alguém da loja responde pelo celular: aí a IA sai da conversa.
      if (mudanca.field === "smb_message_echoes") {
        for (const eco of valor.message_echoes ?? []) {
          if (eco.to) eventos.push({ tipo: "loja_respondeu", telefone: eco.to });
        }
      }
    }
  }
  return eventos;
}

function textoDaMensagem(msg) {
  switch (msg.type) {
    case "text":
      return msg.text?.body;
    case "button":
      return msg.button?.text;
    case "interactive":
      return msg.interactive?.button_reply?.title ?? msg.interactive?.list_reply?.title;
    case "image":
      return comLegenda("[O cliente enviou uma foto, que você não consegue ver.]", msg.image?.caption);
    case "video":
      return comLegenda("[O cliente enviou um vídeo, que você não consegue ver.]", msg.video?.caption);
    case "document":
      return comLegenda("[O cliente enviou um arquivo, que você não consegue abrir.]", msg.document?.caption);
    case "audio":
      return "[O cliente enviou um áudio, que você não consegue ouvir. Peça com gentileza para ele escrever.]";
    case "location":
      return "[O cliente enviou a localização dele.]";
    case "reaction":
    case "unsupported":
      return null; // reações e figurinhas não precisam de resposta
    case "sticker":
      return null;
    default:
      return `[O cliente enviou uma mensagem do tipo "${msg.type}".]`;
  }
}

function comLegenda(aviso, legenda) {
  return legenda ? `${aviso}\n${legenda}` : aviso;
}
