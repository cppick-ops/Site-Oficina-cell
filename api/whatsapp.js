// Endereço que a Meta chama a cada mensagem: https://www.oficinacell.com.br/api/whatsapp

import Anthropic from "@anthropic-ai/sdk";
import { Redis } from "@upstash/redis";
import { waitUntil } from "@vercel/functions";
import { criarMemoria } from "./_lib/memoria.js";
import { criarWhatsApp, assinaturaValida, lerEventos } from "./_lib/whatsapp.js";
import { tratarEventos } from "./_lib/atendente.js";

// A Meta confirma o endereço uma vez, quando você cadastra o webhook
export function GET(request) {
  const params = new URL(request.url).searchParams;
  if (params.get("hub.mode") === "subscribe" && params.get("hub.verify_token") === process.env.WHATSAPP_VERIFY_TOKEN) {
    return new Response(params.get("hub.challenge"));
  }
  return new Response("Proibido", { status: 403 });
}

export async function POST(request) {
  const corpo = await request.text();
  if (!assinaturaValida(corpo, request.headers.get("x-hub-signature-256"), process.env.WHATSAPP_APP_SECRET)) {
    return new Response("Assinatura inválida", { status: 401 });
  }

  // Responde logo para a Meta não reenviar; o atendimento continua em segundo plano
  waitUntil(tratarEventos(lerEventos(JSON.parse(corpo)), dependencias()).catch((erro) => console.error(erro)));
  return new Response("ok");
}

function dependencias() {
  const redis = new Redis({
    url: process.env.KV_REST_API_URL ?? process.env.UPSTASH_REDIS_REST_URL,
    token: process.env.KV_REST_API_TOKEN ?? process.env.UPSTASH_REDIS_REST_TOKEN,
    automaticDeserialization: false,
  });
  return {
    memoria: criarMemoria(redis),
    whatsapp: criarWhatsApp({
      token: process.env.WHATSAPP_TOKEN,
      idNumero: process.env.WHATSAPP_PHONE_NUMBER_ID,
      versao: process.env.WHATSAPP_API_VERSION,
    }),
    claude: new Anthropic(),
    liberados: (process.env.TELEFONES_LIBERADOS ?? "").split(",").filter((numero) => numero.trim()),
    agora: () => new Date(),
  };
}
