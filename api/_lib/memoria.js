// Memória das conversas no Redis (Upstash, pelo Marketplace da Vercel).
// As funções da Vercel não guardam nada entre uma mensagem e outra, por isso
// histórico, fila e pausas ficam aqui.

const UM_DIA = 24 * 60 * 60;
const PAUSA = 12 * 60 * 60; // tempo que a IA fica quieta depois que um humano assume

export function criarMemoria(redis) {
  return {
    // true só na primeira vez que vemos esta mensagem (a Meta às vezes reenvia)
    async primeiraVez(idMensagem) {
      return (await redis.set(`wa:msg:${idMensagem}`, "1", { nx: true, ex: UM_DIA })) === "OK";
    },

    async pausado(telefone) {
      return (await redis.get(`wa:pausa:${telefone}`)) !== null;
    },

    async pausar(telefone, motivo) {
      await redis.set(`wa:pausa:${telefone}`, motivo, { ex: PAUSA });
    },

    async enfileirar(telefone, texto) {
      await redis.rpush(`wa:fila:${telefone}`, texto);
      await redis.expire(`wa:fila:${telefone}`, UM_DIA);
    },

    async retirarFila(telefone) {
      return (await redis.lpop(`wa:fila:${telefone}`, 50)) ?? [];
    },

    async temFila(telefone) {
      return (await redis.llen(`wa:fila:${telefone}`)) > 0;
    },

    // Só uma resposta por cliente de cada vez, para não embaralhar o histórico
    async travar(telefone) {
      return (await redis.set(`wa:trava:${telefone}`, "1", { nx: true, ex: 120 })) === "OK";
    },

    async destravar(telefone) {
      await redis.del(`wa:trava:${telefone}`);
    },

    // O histórico vale por 24h depois da última mensagem; depois disso a conversa recomeça
    async historico(telefone) {
      const salvo = await redis.get(`wa:conversa:${telefone}`);
      return salvo ? JSON.parse(salvo) : [];
    },

    async salvarHistorico(telefone, mensagens) {
      await redis.set(`wa:conversa:${telefone}`, JSON.stringify(mensagens), { ex: UM_DIA });
    },
  };
}
