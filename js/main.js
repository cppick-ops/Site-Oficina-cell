// Oficina Cell Santa Cruz — comportamento do site

const WHATSAPP_NUMERO = "5551995255010";

function linkWhatsApp(mensagem) {
  return `https://wa.me/${WHATSAPP_NUMERO}?text=${encodeURIComponent(mensagem)}`;
}

// Menu do celular
const toggle = document.querySelector(".menu-toggle");
const nav = document.querySelector(".nav");
if (toggle && nav) {
  toggle.addEventListener("click", () => {
    const aberto = nav.classList.toggle("is-open");
    toggle.setAttribute("aria-expanded", String(aberto));
  });
}

// Formulários de orçamento: montam a mensagem e abrem o WhatsApp
document.querySelectorAll("form[data-orcamento]").forEach((form) => {
  form.addEventListener("submit", (evento) => {
    evento.preventDefault();
    const dados = new FormData(form);
    const aparelho = (dados.get("aparelho") || "").toString().trim();
    const modelo = (dados.get("modelo") || "").toString().trim();
    const problema = (dados.get("problema") || "").toString().trim();
    const detalhes = (dados.get("detalhes") || "").toString().trim();

    const linhas = ["Olá, Oficina Cell Santa Cruz! Gostaria de um orçamento."];
    if (aparelho) linhas.push(`Aparelho: ${aparelho}`);
    if (modelo) linhas.push(`Modelo: ${modelo}`);
    if (problema) linhas.push(`Problema: ${problema}`);
    if (detalhes) linhas.push(`Detalhes: ${detalhes}`);

    window.open(linkWhatsApp(linhas.join("\n")), "_blank", "noopener");
  });
});

// Formulário de avaliação do usado (troca ou venda)
document.querySelectorAll("form[data-avaliacao]").forEach((form) => {
  form.addEventListener("submit", (evento) => {
    evento.preventDefault();
    const dados = new FormData(form);
    const linhas = ["Olá, Oficina Cell Santa Cruz! Quero avaliar meu aparelho usado."];
    [
      ["Modelo", "modelo"],
      ["Armazenamento", "armazenamento"],
      ["Estado", "estado"],
      ["Interesse", "interesse"],
    ].forEach(([rotulo, campo]) => {
      const valor = (dados.get(campo) || "").toString().trim();
      if (valor) linhas.push(`${rotulo}: ${valor}`);
    });
    window.open(linkWhatsApp(linhas.join("\n")), "_blank", "noopener");
  });
});

// Ano atual no rodapé
document.querySelectorAll("[data-ano]").forEach((el) => {
  el.textContent = new Date().getFullYear();
});
