"""Gera as páginas HTML do site da Oficina Cell Santa Cruz.

Cabeçalho, rodapé e dados da loja ficam definidos uma única vez aqui.
Para atualizar o site: edite este arquivo e rode

    python3 ferramentas/gerar_site.py

na raiz do projeto. As páginas .html são sobrescritas.
"""

import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- dados da loja
LOJA = {
    "nome": "Oficina Cell Santa Cruz",
    "dominio": "https://www.oficinacell.com.br",
    "whats": "5551995255010",
    "whats_exibicao": "(51) 99525-5010",
    "rua": "Rua Júlio de Castilhos, 361",
    "complemento": "Centro, ao lado do Cartório Trentin",
    "cidade": "Santa Cruz do Sul",
    "uf": "RS",
    "cep": "96810-046",
    "instagram": "https://www.instagram.com/oficinacell.rs/",
    "instagram_exibicao": "@oficinacell.rs",
    "nota_google": "4,9",
    "avaliacoes_google": "73",
    "link_google": "https://www.google.com/maps/place/Oficina+Cell+Assist%C3%AAncia+T%C3%A9cnica+de+Celulares/@-29.7171585,-52.4283627,17z/data=!4m6!3m5!1s0x951ca3d35591aa63:0x1409d5a23ebd5436!8m2!3d-29.7171585!4d-52.4283627!16s%2Fg%2F11j9kfjv5q",
    "mapa_embed": "https://www.google.com/maps?q=Rua+J%C3%BAlio+de+Castilhos,+361,+Santa+Cruz+do+Sul+-+RS&output=embed",
    "garantia": "mínimo de 90 dias",
    "horario": "Segunda a sexta, das 9h às 18h · Sábado, das 9h às 17h",
    "cnpj": "37.566.888/0001-34",
    "anos": 6,  # anos de mercado: atualizar todo ano
}

# Horário em formato do schema.org (usado pelo Google)
HORARIOS_SCHEMA = [
    {"dias": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "abre": "09:00", "fecha": "18:00"},
    {"dias": ["Saturday"], "abre": "09:00", "fecha": "17:00"},
]

# Avaliações reais do Perfil da Empresa no Google (texto copiado como foi escrito).
AVALIACOES = [
    {"nome": "Katharine D.", "texto": "Ótimo atendimento, produtos e serviços de qualidade. Super recomendo!"},
    {"nome": "Aline B.", "texto": "Ótimo atendimento, serviço de qualidade, rapidez e preço justo!"},
    {"nome": "Veridiana R.", "texto": "Atendimento excelente e super recomendo."},
]

CIDADES = [
    "Santa Cruz do Sul", "Venâncio Aires", "Vera Cruz", "Rio Pardo", "Candelária",
    "Sinimbu", "Passo do Sobrado", "Vale do Sol", "Herveiras", "Gramado Xavier",
]


def pendente(texto):
    return f'<span class="pending">[{texto}]</span>'


def whats_link(msg="Olá, Oficina Cell Santa Cruz! Gostaria de um orçamento."):
    from urllib.parse import quote
    return f"https://wa.me/{LOJA['whats']}?text={quote(msg)}"


# ---------------------------------------------------------------- ícones (SVG)
I = {
    "whats": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.47 14.38c-.3-.15-1.75-.86-2.02-.96-.27-.1-.47-.15-.67.15-.2.3-.77.96-.94 1.16-.17.2-.35.22-.64.07-.3-.15-1.25-.46-2.38-1.47-.88-.79-1.47-1.76-1.65-2.06-.17-.3-.02-.46.13-.6.13-.14.3-.35.45-.52.15-.18.2-.3.3-.5.1-.2.05-.37-.03-.52-.07-.15-.67-1.6-.92-2.2-.24-.58-.49-.5-.67-.5h-.57c-.2 0-.52.07-.8.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.21 3.08c.15.2 2.1 3.2 5.08 4.48.71.31 1.26.49 1.7.63.71.22 1.36.19 1.87.12.57-.09 1.75-.72 2-1.41.25-.7.25-1.29.17-1.41-.07-.13-.27-.2-.57-.35M12.05 21.8h-.01a9.8 9.8 0 0 1-4.99-1.37l-.36-.21-3.71.97.99-3.62-.23-.37a9.8 9.8 0 0 1-1.5-5.23c0-5.42 4.41-9.83 9.84-9.83 2.63 0 5.1 1.03 6.95 2.88a9.77 9.77 0 0 1 2.88 6.95c0 5.43-4.41 9.83-9.86 9.83M20.42 3.48A11.75 11.75 0 0 0 12.05 0C5.5 0 .17 5.33.16 11.88c0 2.1.55 4.14 1.59 5.94L.06 24l6.3-1.65a11.87 11.87 0 0 0 5.68 1.45h.01c6.55 0 11.88-5.33 11.89-11.89a11.82 11.82 0 0 0-3.52-8.43"/></svg>',
    "menu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
    "tela": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="6" y="2" width="12" height="20" rx="2.5"/><path d="m9 6 3 4-2 2 4 5"/></svg>',
    "vidro": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="6" y="2" width="12" height="20" rx="2.5"/><path d="M9 5.5 15 11.5"/><path d="M9 9.5 12.5 13"/><path d="M11 18h2"/></svg>',
    "watch": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="6" y="6" width="12" height="12" rx="3"/><path d="M9 6 9.5 2h5L15 6M9 18l.5 4h5l.5-4"/><path d="M18 10.5h1"/></svg>',
    "estrela": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/></svg>',
    "notebook": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="4" width="16" height="11" rx="1.5"/><path d="M2 19h20l-1.5-4h-17z"/></svg>',
    "bateria": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="7" y="4" width="10" height="18" rx="2"/><path d="M10 2h4"/><path d="m12.5 9-2 4h3l-2 4"/></svg>',
    "conector": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22v-5"/><path d="M9 8V2M15 8V2"/><path d="M18 8v4a6 6 0 0 1-12 0V8z"/></svg>',
    "placa": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="5" y="5" width="14" height="14" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M9 2v3M15 2v3M9 19v3M15 19v3M2 9h3M2 15h3M19 9h3M19 15h3"/></svg>',
    "software": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/><path d="m9 12 2 2 4-4"/></svg>',
    "ferramenta": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>',
    "relogio": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>',
    "escudo": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/></svg>',
    "loja": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>',
    "celular": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="6" y="2" width="12" height="20" rx="2.5"/><path d="M11 18h2"/></svg>',
    "troca": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M17 2l4 4-4 4"/><path d="M3 11v-1a4 4 0 0 1 4-4h14"/><path d="m7 22-4-4 4-4"/><path d="M21 13v1a4 4 0 0 1-4 4H3"/></svg>',
    "fone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 14h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-7a9 9 0 0 1 18 0v7a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3"/></svg>',
    "instagram": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><path d="M17.5 6.5h.01"/></svg>',
    "documento": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/></svg>',
}

# ---------------------------------------------------------------- serviços
SERVICOS = [
    {
        "slug": "troca-de-tela",
        "icone": "tela",
        "nome": "Troca de tela",
        "resumo": "Tela trincada, manchada ou sem toque. Troca feita no mesmo dia.",
        "prazo": "No mesmo dia",
        "titulo": "Troca de tela de celular em Santa Cruz do Sul",
        "seo_titulo": "Troca de tela de celular em Santa Cruz do Sul | Oficina Cell Santa Cruz",
        "seo_desc": "Troca de tela de iPhone, Samsung, Motorola e Xiaomi em Santa Cruz do Sul, feita no mesmo dia, com garantia mínima de 90 dias. Orçamento pelo WhatsApp.",
        "lead": "Trincou, ficou com manchas ou parou de responder ao toque? Trocamos a tela do seu celular no mesmo dia, na loja do centro de Santa Cruz do Sul, com garantia mínima de 90 dias.",
        "problema_form": "Tela quebrada ou sem toque",
        "sinais": [
            "Vidro trincado ou estilhaçado",
            "Toque falhando, travando ou clicando sozinho",
            "Manchas, listras ou pontos coloridos na imagem",
            "Tela preta com o aparelho ligado (vibra ou toca)",
        ],
        "faq": [
            ("Quanto tempo leva a troca de tela?", "A troca de tela é feita no mesmo dia. Se precisar encomendar a peça para um modelo específico, avisamos o prazo antes de você aprovar o serviço."),
            ("Dá para trocar só o vidro?", "Sim. Se a imagem e o toque estão funcionando, trocamos apenas o vidro e mantemos a tela original. Somos a única loja de Santa Cruz do Sul com esse serviço. Veja a página de troca de vidro."),
            ("Quanto custa a troca de tela?", "O valor depende do modelo do aparelho e do tipo de tela. Mande o modelo pelo WhatsApp e passamos o orçamento sem compromisso."),
            ("Vou perder minhas fotos e arquivos?", "A troca de tela não mexe na memória do aparelho, então seus dados normalmente ficam onde estão. Mesmo assim, recomendamos manter um backup em dia."),
            ("A troca de tela tem garantia?", "Sim. A garantia é de no mínimo 90 dias, podendo ser maior conforme a peça e o serviço."),
            ("Vocês trocam tela de quais marcas?", "Atendemos iPhone, Samsung, Motorola, Xiaomi e outras marcas, além de Apple Watch. Mande o modelo pelo WhatsApp para confirmarmos."),
        ],
    },
    {
        "slug": "troca-de-vidro",
        "icone": "vidro",
        "atende": "Celular e Apple Watch",
        "nome": "Troca de vidro",
        "resumo": "Só o vidro trincou? Trocamos apenas o vidro e mantemos a tela original. Única loja da cidade com esse serviço.",
        "prazo": None,
        "destaque": "Única na cidade",
        "titulo": "Troca de vidro da tela em Santa Cruz do Sul, mantendo a tela original",
        "seo_titulo": "Troca de vidro da tela de celular e Apple Watch em Santa Cruz do Sul | Oficina Cell Santa Cruz",
        "seo_desc": "Troca só do vidro da tela, mantendo o display original do seu celular ou Apple Watch. Única loja de Santa Cruz do Sul com esse serviço. Garantia mínima de 90 dias.",
        "lead": "Quando só o vidro trincou e a imagem e o toque continuam funcionando, trocamos apenas o vidro e mantemos a tela original do seu aparelho. Somos a única loja de Santa Cruz do Sul que faz esse serviço, inclusive em Apple Watch.",
        "problema_form": "Vidro trincado (imagem e toque funcionando)",
        "sinais": [
            "O vidro trincou, mas a imagem continua perfeita",
            "O toque funciona normalmente",
            "Não há manchas, listras ou pontos na imagem",
            "Apple Watch com o vidro trincado",
        ],
        "faq": [
            ("Qual a diferença entre trocar o vidro e trocar a tela?", "Na troca de tela, o conjunto inteiro (vidro e display) é substituído. Na troca de vidro, retiramos só o vidro quebrado e colocamos um novo sobre o display original do seu aparelho, que é mantido."),
            ("Por que manter a tela original?", "O display original é o que veio de fábrica no seu aparelho, com as cores, o brilho e a qualidade de imagem originais."),
            ("Meu aparelho pode fazer a troca só do vidro?", "Se a imagem e o toque estão funcionando, é bem provável que sim. Confirmamos no diagnóstico e, se o display também estiver danificado, indicamos a troca de tela."),
            ("Vocês trocam o vidro de Apple Watch?", "Sim. Trocamos o vidro de Apple Watch mantendo a tela original do relógio."),
            ("Outras lojas de Santa Cruz do Sul fazem esse serviço?", "Somos a única loja da cidade que faz a troca só do vidro, mantendo a tela original."),
            ("Tem garantia?", "Sim, garantia mínima de 90 dias."),
        ],
    },
    {
        "slug": "troca-de-bateria",
        "icone": "bateria",
        "nome": "Troca de bateria",
        "resumo": "Descarrega rápido, desliga sozinho ou estufou. Troca feita no mesmo dia.",
        "prazo": "No mesmo dia",
        "titulo": "Troca de bateria de celular em Santa Cruz do Sul",
        "seo_titulo": "Troca de bateria de celular em Santa Cruz do Sul | Oficina Cell Santa Cruz",
        "seo_desc": "Bateria descarregando rápido ou estufada? Troca de bateria de iPhone e Android em Santa Cruz do Sul no mesmo dia, com garantia mínima de 90 dias.",
        "lead": "Se o seu celular não aguenta mais o dia, desliga com carga ou a bateria estufou, a troca resolve. Fazemos no mesmo dia, com garantia mínima de 90 dias.",
        "problema_form": "Bateria descarregando rápido ou estufada",
        "sinais": [
            "Descarrega muito rápido, mesmo com pouco uso",
            "Desliga sozinho com 20%, 30% ou mais de carga",
            "Esquenta mais que o normal",
            "A tela ou a tampa está levantando (bateria estufada)",
        ],
        "faq": [
            ("Quanto tempo leva a troca de bateria?", "A troca de bateria é feita no mesmo dia."),
            ("Como sei se preciso trocar a bateria?", "No iPhone, veja em Ajustes > Bateria > Saúde e Carregamento. No Android, os sinais mais comuns são descarregar rápido e desligar com carga. Se tiver dúvida, fazemos o diagnóstico na loja."),
            ("Bateria estufada é perigosa?", "Sim. Bateria estufada pode danificar a tela e aquecer. Pare de carregar o aparelho e traga para a troca o quanto antes."),
            ("Quanto custa a troca de bateria?", "O valor depende do modelo. Mande o modelo pelo WhatsApp e passamos o orçamento sem compromisso."),
            ("A troca de bateria tem garantia?", "Sim, garantia mínima de 90 dias."),
        ],
    },
    {
        "slug": "conector-de-carga",
        "icone": "conector",
        "nome": "Conector de carga",
        "resumo": "Só carrega em uma posição ou não reconhece o cabo. Reparo no mesmo dia.",
        "prazo": "No mesmo dia",
        "titulo": "Troca de conector de carga em Santa Cruz do Sul",
        "seo_titulo": "Conector de carga de celular em Santa Cruz do Sul | Oficina Cell Santa Cruz",
        "seo_desc": "Celular não carrega ou só carrega em uma posição? Reparo e troca de conector de carga em Santa Cruz do Sul no mesmo dia, com garantia mínima de 90 dias.",
        "lead": "Celular que só carrega com o cabo torto, carrega devagar ou não reconhece o carregador quase sempre tem solução rápida. Verificamos o conector e resolvemos no mesmo dia.",
        "problema_form": "Não carrega ou conector com mau contato",
        "sinais": [
            "Só carrega com o cabo em uma posição",
            "Não reconhece o carregador ou o computador",
            "Carrega muito devagar",
            "Cabo frouxo, que sai sozinho do aparelho",
        ],
        "faq": [
            ("Quanto tempo leva o reparo do conector?", "O reparo do conector de carga é feito no mesmo dia."),
            ("Pode ser só sujeira no conector?", "Pode. No diagnóstico verificamos se é sujeira acumulada, mau contato ou defeito na peça, e só então passamos o orçamento."),
            ("E se não for o conector?", "Se o problema estiver na placa ou na bateria, explicamos o que encontramos antes de qualquer serviço."),
            ("Quanto custa?", "Depende do modelo e do que for encontrado no diagnóstico. Mande o modelo pelo WhatsApp para um orçamento sem compromisso."),
            ("Tem garantia?", "Sim, garantia mínima de 90 dias."),
        ],
    },
    {
        "slug": "reparo-em-placa",
        "icone": "placa",
        "nome": "Reparo em placa",
        "resumo": "Não liga, molhou ou reinicia sozinho. Reparos avançados de placa, inclusive Apple.",
        "prazo": "Depende do defeito",
        "titulo": "Reparo em placa de celular em Santa Cruz do Sul",
        "seo_titulo": "Reparo em placa de celular e iPhone em Santa Cruz do Sul | Oficina Cell Santa Cruz",
        "seo_desc": "Celular não liga, molhou ou reinicia sozinho? Reparo avançado em placa de iPhone e Android em Santa Cruz do Sul, com diagnóstico e garantia mínima de 90 dias.",
        "lead": "Somos especializados em reparos avançados de placa, inclusive em aparelhos Apple. Quando outras assistências dizem que não tem conserto, vale trazer para um diagnóstico.",
        "problema_form": "Não liga, molhou ou defeito na placa",
        "sinais": [
            "Não liga, mesmo com bateria e carregador bons",
            "Molhou ou caiu na água",
            "Reinicia sozinho ou fica preso no logo",
            "Sem sinal, sem Wi-Fi ou sem áudio depois de queda",
        ],
        "faq": [
            ("Quanto tempo leva o reparo em placa?", "Não há prazo fixo: depende do defeito encontrado. Depois do diagnóstico, informamos o que precisa ser feito e a previsão antes de você aprovar."),
            ("Meu celular molhou. O que eu faço?", "Desligue o aparelho, não coloque para carregar e traga para a loja o quanto antes. Quanto mais cedo, maiores as chances de recuperar."),
            ("Vocês consertam placa de iPhone?", "Sim. Fazemos reparos avançados em placas da Apple e das outras grandes marcas."),
            ("Consigo recuperar meus dados?", "Depende do defeito. Quando o aparelho volta a funcionar, os dados normalmente são preservados. Avaliamos cada caso no diagnóstico."),
            ("Tem garantia?", "Sim, garantia mínima de 90 dias sobre o serviço realizado."),
        ],
    },
    {
        "slug": "conserto-de-apple-watch",
        "icone": "watch",
        "atende": "Apple Watch",
        "nome": "Apple Watch",
        "resumo": "Conserto de Apple Watch, incluindo troca só do vidro mantendo a tela original.",
        "prazo": None,
        "titulo": "Conserto de Apple Watch em Santa Cruz do Sul",
        "seo_titulo": "Conserto de Apple Watch em Santa Cruz do Sul | Oficina Cell Santa Cruz",
        "seo_desc": "Conserto de Apple Watch em Santa Cruz do Sul, com troca de vidro mantendo a tela original. Especialistas em Apple, garantia mínima de 90 dias.",
        "lead": "Consertamos Apple Watch na loja do centro de Santa Cruz do Sul. Se só o vidro trincou, trocamos apenas o vidro e mantemos a tela original do relógio, um serviço que só nós fazemos na cidade.",
        "problema_form": "Apple Watch com defeito",
        "sinais": [
            "Vidro trincado ou lascado",
            "Tela sem imagem ou sem toque",
            "Bateria que não dura o dia",
            "Relógio que não liga ou não carrega",
        ],
        "faq": [
            ("Vocês trocam só o vidro do Apple Watch?", "Sim. Trocamos apenas o vidro e mantemos a tela original do relógio. Somos a única loja de Santa Cruz do Sul que faz esse serviço."),
            ("Quais modelos de Apple Watch vocês atendem?", "Mande pelo WhatsApp a série e o tamanho do seu relógio (por exemplo, Series 7 de 45 mm) para confirmarmos."),
            ("Quanto custa?", "Depende do modelo e do defeito. Mande o modelo e o problema pelo WhatsApp e passamos o orçamento sem compromisso."),
            ("Tem garantia?", "Sim, garantia mínima de 90 dias."),
        ],
    },
    {
        "slug": "conserto-de-macbook",
        "icone": "notebook",
        "nome": "MacBook",
        "resumo": "Troca de tela, bateria e teclado de MacBook. Carregadores, cabos, adaptadores e hubs.",
        "prazo": None,
        "atende": "MacBook",
        "titulo": "Conserto de MacBook em Santa Cruz do Sul",
        "seo_titulo": "Conserto de MacBook em Santa Cruz do Sul: tela, bateria e teclado | Oficina Cell Santa Cruz",
        "seo_desc": "Troca de tela, bateria e teclado de MacBook em Santa Cruz do Sul, com garantia mínima de 90 dias. Carregadores, cabos, adaptadores e hubs para MacBook.",
        "lead": "Fazemos troca de tela, bateria e teclado de MacBook na loja do centro de Santa Cruz do Sul, com garantia mínima de 90 dias. Também temos carregadores, cabos, adaptadores e hubs para o seu Mac.",
        "problema_form": "MacBook: tela, bateria ou teclado",
        "sinais": [
            "Tela trincada, com manchas, listras ou sem imagem",
            "Bateria que não dura ou aviso de manutenção recomendada",
            "Teclas falhando, repetindo ou sem resposta",
            "MacBook que desliga sozinho com carga",
        ],
        "faq": [
            ("Quais serviços vocês fazem em MacBook?", "Troca de tela, troca de bateria e troca de teclado."),
            ("Quais modelos de MacBook vocês atendem?", "Mande pelo WhatsApp o modelo e o ano do seu MacBook, que aparecem no menu Apple > Sobre Este Mac, para confirmarmos."),
            ("Quanto custa?", "Depende do modelo e do serviço. Mande o modelo e o problema pelo WhatsApp e passamos o orçamento sem compromisso."),
            ("Vocês vendem carregador para MacBook?", "Sim. Temos carregadores, cabos, adaptadores e hubs para MacBook."),
            ("Tem garantia?", "Sim, garantia mínima de 90 dias."),
        ],
    },
    {
        "slug": "formatacao-e-remocao-de-virus",
        "icone": "software",
        "nome": "Formatação e vírus",
        "resumo": "Formatação, hard reset e remoção de vírus para celular lento ou travando. No mesmo dia.",
        "prazo": "No mesmo dia",
        "titulo": "Formatação, hard reset e remoção de vírus em Santa Cruz do Sul",
        "seo_titulo": "Formatação, hard reset e remoção de vírus de celular em Santa Cruz do Sul | Oficina Cell Santa Cruz",
        "seo_desc": "Celular lento, travando ou com anúncios estranhos? Formatação, hard reset e remoção de vírus em Santa Cruz do Sul, com garantia mínima de 90 dias.",
        "lead": "Celular lento, cheio de anúncios ou travando? Fazemos formatação, hard reset e remoção de vírus em Android e iPhone, e orientamos sobre backup antes de começar.",
        "problema_form": "Formatação, hard reset ou vírus",
        "sinais": [
            "Aparelho lento ou travando o tempo todo",
            "Anúncios e janelas aparecendo sozinhos",
            "Aplicativos estranhos que você não instalou",
            "Sistema com erro ou preso em reinicialização",
        ],
        "faq": [
            ("Quanto tempo leva?", "Formatação, hard reset e remoção de vírus são feitos no mesmo dia."),
            ("Vou perder meus dados na formatação?", "Sim. A formatação e o hard reset apagam o conteúdo do aparelho. Faça backup antes ou fale com a gente para orientarmos como salvar fotos e contatos."),
            ("Dá para tirar o vírus sem formatar?", "Em muitos casos, sim. Avaliamos o aparelho e indicamos a solução que preserva seus dados sempre que possível."),
            ("Preciso saber minha conta Google ou Apple ID?", "Sim. Depois de um reset, o aparelho pede a conta que estava cadastrada. É uma proteção contra roubo, por isso só atendemos o dono do aparelho, que precisa ter esses dados."),
            ("Quanto custa?", "Depende do serviço e do aparelho. Mande pelo WhatsApp o que está acontecendo e passamos o orçamento sem compromisso."),
            ("Tem garantia?", "Sim, garantia mínima de 90 dias."),
        ],
    },
]

OUTROS_REPAROS = "Câmera, alto-falante, microfone, botões, tampa traseira e outros reparos."


# ---------------------------------------------------------------- blocos comuns
def head(titulo, descricao, caminho, prefixo, extra_jsonld=None):
    url = f"{LOJA['dominio']}/{caminho}".rstrip("/") + ("/" if caminho == "" else "")
    jsonld = [jsonld_loja()]
    if extra_jsonld:
        jsonld.extend(extra_jsonld)
    scripts = "\n".join(
        f'  <script type="application/ld+json">{json.dumps(item, ensure_ascii=False)}</script>' for item in jsonld
    )
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{titulo}</title>
  <meta name="description" content="{descricao}">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="pt_BR">
  <meta property="og:site_name" content="{LOJA['nome']}">
  <meta property="og:title" content="{titulo}">
  <meta property="og:description" content="{descricao}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{LOJA['dominio']}/img/og-image.jpg">
  <meta name="theme-color" content="#0e0f09">
  <link rel="icon" href="{prefixo}img/favicon.png" type="image/png">
  <link rel="apple-touch-icon" href="{prefixo}img/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Saira:wght@600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{prefixo}css/style.css">
{scripts}
</head>
<body>
"""


def jsonld_loja():
    dados = {
        "@context": "https://schema.org",
        "@type": "MobilePhoneStore",
        "name": LOJA["nome"],
        "url": LOJA["dominio"] + "/",
        "logo": LOJA["dominio"] + "/img/logo.png",
        "image": LOJA["dominio"] + "/img/og-image.jpg",
        "telephone": "+55 " + LOJA["whats_exibicao"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": LOJA["rua"],
            "addressLocality": LOJA["cidade"],
            "addressRegion": LOJA["uf"],
            "postalCode": LOJA["cep"],
            "addressCountry": "BR",
        },
        "areaServed": [{"@type": "City", "name": c} for c in CIDADES],
        "sameAs": [LOJA["instagram"]],
        "taxID": LOJA["cnpj"],
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": h["dias"], "opens": h["abre"], "closes": h["fecha"]}
            for h in HORARIOS_SCHEMA
        ],
    }
    return dados


def header(prefixo, ativo):
    def link(href, texto, chave):
        atual = ' aria-current="page"' if chave == ativo else ""
        return f'<a href="{href}"{atual}>{texto}</a>'

    return f"""  <div class="topbar">
    <div class="container">
      <span class="topbar__endereco">{LOJA['rua']} · {LOJA['complemento']} · {LOJA['cidade']}/{LOJA['uf']}</span>
      <a href="{whats_link()}" target="_blank" rel="noopener">WhatsApp {LOJA['whats_exibicao']}</a>
    </div>
  </div>
  <header class="header">
    <div class="container">
      <a class="logo" href="{prefixo}index.html" aria-label="{LOJA['nome']}, página inicial">
        <img src="{prefixo}img/logo-icone.png" alt="" width="46" height="44">
        <span>Oficina Cell<small>Santa Cruz</small></span>
      </a>
      <button class="menu-toggle" aria-expanded="false" aria-controls="menu" aria-label="Abrir menu">{I['menu']}</button>
      <nav class="nav" id="menu" aria-label="Principal">
        {link(prefixo + 'index.html#servicos', 'Serviços', 'servicos')}
        {link(prefixo + 'aparelhos.html', 'Aparelhos e acessórios', 'aparelhos')}
        {link(prefixo + 'contato.html', 'A loja e contato', 'contato')}
        <a class="btn btn--whats" href="{whats_link()}" target="_blank" rel="noopener">{I['whats']} Orçamento</a>
      </nav>
    </div>
  </header>
"""


def footer(prefixo):
    servicos = "\n".join(
        f'          <li><a href="{prefixo}servicos/{s["slug"]}.html">{s["nome"]}</a></li>' for s in SERVICOS
    )
    horario = LOJA["horario"] or pendente("Horário de funcionamento")
    cnpj = LOJA["cnpj"] or pendente("CNPJ")
    return f"""  <section class="cta">
    <div class="container">
      <h2>Seu celular precisa de conserto?</h2>
      <p>Mande o modelo e o problema pelo WhatsApp. Respondemos com o orçamento, sem compromisso.</p>
      <a class="btn btn--light" href="{whats_link()}" target="_blank" rel="noopener">{I['whats']} Chamar no WhatsApp</a>
    </div>
  </section>
  <footer class="footer">
    <div class="container">
      <div>
        <img class="footer__logo" src="{prefixo}img/logo.png" alt="{LOJA['nome']}" width="592" height="240" loading="lazy">
        <p>Assistência técnica de celulares, tablets, Apple Watch e MacBook, aparelhos novos e seminovos e acessórios. Atendemos Santa Cruz do Sul e região.</p>
        <p>{LOJA['rua']} · {LOJA['complemento']}<br>{LOJA['cidade']}/{LOJA['uf']} · CEP {LOJA['cep']}</p>
        <p>Horário: {horario}<br>CNPJ: {cnpj}</p>
      </div>
      <div>
        <h3>Serviços</h3>
        <ul>
{servicos}
        </ul>
      </div>
      <div>
        <h3>Contato</h3>
        <ul>
          <li><a href="{whats_link()}" target="_blank" rel="noopener">WhatsApp {LOJA['whats_exibicao']}</a></li>
          <li><a href="{LOJA['instagram']}" target="_blank" rel="noopener">Instagram {LOJA['instagram_exibicao']}</a></li>
          <li><a href="{LOJA['link_google']}" target="_blank" rel="noopener">Avaliações no Google</a></li>
          <li><a href="{prefixo}aparelhos.html">Aparelhos e acessórios</a></li>
          <li><a href="{prefixo}contato.html">Como chegar</a></li>
        </ul>
      </div>
      <div class="footer__bottom">© <span data-ano></span> {LOJA['nome']}. Todos os direitos reservados.</div>
    </div>
  </footer>
  <a class="float-whats" href="{whats_link()}" target="_blank" rel="noopener" aria-label="Falar no WhatsApp">{I['whats']}</a>
  <script src="{prefixo}js/main.js"></script>
</body>
</html>
"""


def form_orcamento(problema_padrao=None, titulo="Peça seu orçamento", id_sufixo=""):
    opcoes = [s["problema_form"] for s in SERVICOS] + ["Outro problema"]
    opts = "\n".join(
        f'            <option{" selected" if o == problema_padrao else ""}>{o}</option>' for o in opcoes
    )
    return f"""      <form class="quote" data-orcamento aria-labelledby="orc-titulo{id_sufixo}">
        <h2 id="orc-titulo{id_sufixo}">{titulo}</h2>
        <p>Preencha e envie pelo WhatsApp. Respondemos com o orçamento, sem compromisso.</p>
        <div class="form-row">
          <div class="field">
            <label for="aparelho{id_sufixo}">Aparelho</label>
            <select id="aparelho{id_sufixo}" name="aparelho">
              <option>Celular</option>
              <option>Tablet</option>
              <option>Apple Watch</option>
              <option>MacBook</option>
            </select>
          </div>
          <div class="field">
            <label for="modelo{id_sufixo}">Marca e modelo</label>
            <input id="modelo{id_sufixo}" name="modelo" placeholder="Ex.: iPhone 13, Galaxy A54" required>
          </div>
        </div>
        <div class="field">
          <label for="problema{id_sufixo}">Qual o problema?</label>
          <select id="problema{id_sufixo}" name="problema">
{opts}
          </select>
        </div>
        <div class="field">
          <label for="detalhes{id_sufixo}">Detalhes (opcional)</label>
          <textarea id="detalhes{id_sufixo}" name="detalhes" placeholder="Conte o que aconteceu"></textarea>
        </div>
        <button class="btn btn--whats btn--block" type="submit">{I['whats']} Enviar pelo WhatsApp</button>
        <p class="quote__note">Garantia mínima de 90 dias em todos os serviços.</p>
      </form>
"""


def faq_html(perguntas):
    itens = "\n".join(
        f"""        <details>
          <summary>{p}</summary>
          <div><p>{r}</p></div>
        </details>"""
        for p, r in perguntas
    )
    return f'      <div class="faq">\n{itens}\n      </div>'


def faq_jsonld(perguntas):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": p, "acceptedAnswer": {"@type": "Answer", "text": r}}
            for p, r in perguntas
        ],
    }


def prazo_texto(s):
    return s["prazo"] or pendente("Prazo a confirmar")


# ---------------------------------------------------------------- página inicial
FAQ_HOME = [
    ("Quanto tempo leva o conserto?", "Troca de tela, bateria, conector, formatação, remoção de vírus e outros reparos comuns são feitos no mesmo dia. Reparos em placa não têm prazo fixo: dependem do defeito encontrado no diagnóstico."),
    ("Qual a garantia dos serviços?", "A garantia é de no mínimo 90 dias, podendo ser maior conforme o produto e o serviço."),
    ("Por que vocês não mostram preços no site?", "O valor muda conforme o modelo e o defeito. Mande o modelo e o problema pelo WhatsApp e respondemos com o orçamento, sem compromisso."),
    ("Preciso agendar?", "Não. Você pode vir direto à loja no centro de Santa Cruz do Sul. Se mandar o modelo antes pelo WhatsApp, já deixamos tudo encaminhado."),
    ("Vocês atendem clientes de outras cidades?", "Sim. Atendemos clientes de Santa Cruz do Sul e de toda a região, como Venâncio Aires, Vera Cruz, Rio Pardo, Candelária e Sinimbu."),
    ("Vocês consertam iPhone e Apple Watch?", "Sim. Somos especializados em Apple e nas grandes marcas, incluindo reparos avançados de placa e conserto de Apple Watch."),
    ("Vocês consertam MacBook?", "Sim. Fazemos troca de tela, bateria e teclado de MacBook, e temos carregadores, cabos, adaptadores e hubs."),
    ("Vocês trocam só o vidro da tela?", "Sim. Somos a única loja de Santa Cruz do Sul que troca apenas o vidro, mantendo a tela original do celular ou do Apple Watch. Funciona quando a imagem e o toque continuam bons."),
]


def pagina_inicial():
    cards = "\n".join(
        f"""        <a class="card" href="servicos/{s['slug']}.html">
          <span class="card__icon">{I[s['icone']]}</span>
          <h3>{s['nome']}</h3>
          <p>{s['resumo']}</p>
          <span class="tag{' tag--destaque' if s.get('destaque') else ('' if s['prazo'] == 'No mesmo dia' else ' tag--neutral')}">{s.get('destaque') or s['prazo'] or 'Consulte o prazo'}</span>
          <span class="card__link">Saiba mais →</span>
        </a>"""
        for s in SERVICOS
    )
    cards += f"""
        <a class="card card--wide" href="{whats_link('Olá, Oficina Cell Santa Cruz! Preciso de um reparo que não está na lista do site.')}" target="_blank" rel="noopener">
          <span class="card__icon">{I['ferramenta']}</span>
          <div class="card__body">
            <h3>Outros reparos</h3>
            <p>{OUTROS_REPAROS}</p>
          </div>
          <span class="tag">No mesmo dia</span>
          <span class="card__link">Pedir orçamento →</span>
        </a>"""

    chips = "\n".join(f'        <span class="chip">{c}</span>' for c in CIDADES)
    depoimentos = "\n".join(
        f'        <figure class="review"><blockquote><p>“{a["texto"]}”</p></blockquote>'
        f'<figcaption><strong>{a["nome"]}</strong><br><small>Avaliação no Google</small></figcaption></figure>'
        for a in AVALIACOES
    )

    corpo = f"""  <main>
  <section class="hero">
    <div class="container">
      <div>
        <a class="rating" href="{LOJA['link_google']}" target="_blank" rel="noopener">
          <span class="rating__stars" aria-hidden="true">★★★★★</span>
          <span>{LOJA['nota_google']} no Google</span>
          <span>· {LOJA['avaliacoes_google']} avaliações</span>
        </a>
        <h1>Assistência técnica de celular em <span>Santa Cruz do Sul</span></h1>
        <p class="hero__lead">Troca de tela, bateria e conector no mesmo dia. Reparos avançados de placa e conserto de Apple Watch e MacBook. Somos a única loja da cidade que troca apenas o vidro da tela, mantendo o display original. Garantia mínima de 90 dias.</p>
        <div class="hero__actions">
          <a class="btn btn--whats" href="{whats_link()}" target="_blank" rel="noopener">{I['whats']} Orçamento pelo WhatsApp</a>
          <a class="btn btn--ghost" href="#servicos">Ver serviços</a>
        </div>
        <div class="trust">
          <div class="trust__item">{I['relogio']} Reparos comuns no mesmo dia</div>
          <div class="trust__item">{I['escudo']} Garantia mínima de 90 dias</div>
          <div class="trust__item">{I['loja']} {LOJA['anos']} anos no centro da cidade</div>
        </div>
      </div>
{form_orcamento()}
    </div>
  </section>

  <section class="section" id="servicos">
    <div class="container">
      <div class="section__head">
        <span class="eyebrow">Serviços</span>
        <h2>O que consertamos</h2>
        <p>Atendemos iPhone, Samsung, Motorola, Xiaomi e outras marcas, além de tablets, Apple Watch e MacBook.</p>
      </div>
      <div class="grid grid--4">
{cards}
      </div>
    </div>
  </section>

  <section class="section section--tight">
    <div class="container">
      <div class="exclusivo">
        <div class="exclusivo__selo">{I['estrela']} Única em Santa Cruz do Sul</div>
        <div>
          <h2>Trincou só o vidro? Mantenha a tela original.</h2>
          <p>Trocamos apenas o vidro da tela do seu celular ou Apple Watch e mantemos o display original, com as cores e o brilho de fábrica. Somos a única loja da cidade que faz esse serviço.</p>
        </div>
        <a class="btn btn--whats" href="servicos/troca-de-vidro.html">Saiba mais</a>
      </div>
    </div>
  </section>

  <section class="section section--soft">
    <div class="container">
      <div class="section__head">
        <span class="eyebrow">Como funciona</span>
        <h2>Do orçamento ao aparelho pronto</h2>
      </div>
      <div class="grid grid--3 steps">
        <div class="step">
          <h3>Mande o modelo e o problema</h3>
          <p>Pelo WhatsApp ou direto na loja. Respondemos com o orçamento, sem compromisso.</p>
        </div>
        <div class="step">
          <h3>Diagnóstico e aprovação</h3>
          <p>Avaliamos o aparelho e só começamos depois que você aprova o serviço.</p>
        </div>
        <div class="step">
          <h3>Retire com garantia</h3>
          <p>Reparos comuns ficam prontos no mesmo dia, com garantia mínima de 90 dias.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="band">
        <div>
          <span class="eyebrow">Garantia</span>
          <h2>Garantia mínima de 90 dias em todos os serviços</h2>
          <p>Dependendo do produto e do serviço, a garantia pode ser maior.</p>
        </div>
        <ul>
          <li>{I['check']} Troca de tela, bateria e conector no mesmo dia</li>
          <li>{I['check']} Há {LOJA['anos']} anos em Santa Cruz do Sul</li>
          <li>{I['check']} Reparo de placa com diagnóstico antes de aprovar</li>
          <li>{I['check']} Única loja da cidade que troca só o vidro</li>
          <li>{I['check']} Especialistas em Apple, inclusive Apple Watch</li>
        </ul>
      </div>
    </div>
  </section>

  <section class="section section--soft">
    <div class="container">
      <div class="section__head">
        <span class="eyebrow">Aparelhos e acessórios</span>
        <h2>Celulares novos, seminovos e acessórios</h2>
        <p>Encontre seu próximo celular ou traga o usado para avaliarmos na troca.</p>
      </div>
      <div class="grid grid--3">
        <a class="card" href="aparelhos.html#seminovos">
          <span class="card__icon">{I['celular']}</span>
          <h3>Novos e seminovos</h3>
          <p>iPhone e Android com garantia. Veja os aparelhos disponíveis.</p>
          <span class="card__link">Ver aparelhos →</span>
        </a>
        <a class="card" href="aparelhos.html#troca">
          <span class="card__icon">{I['troca']}</span>
          <h3>Troque seu usado</h3>
          <p>Avaliamos seu aparelho usado como parte do pagamento.</p>
          <span class="card__link">Avaliar meu aparelho →</span>
        </a>
        <a class="card" href="aparelhos.html#acessorios">
          <span class="card__icon">{I['fone']}</span>
          <h3>Acessórios</h3>
          <p>Películas, capas, carregadores, cabos e fones. Para MacBook: carregadores, cabos, adaptadores e hubs.</p>
          <span class="card__link">Ver acessórios →</span>
        </a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="section__head">
        <span class="eyebrow">Avaliações</span>
        <h2>{LOJA['nota_google']} estrelas no Google, com {LOJA['avaliacoes_google']} avaliações</h2>
        <p><a href="{LOJA['link_google']}" target="_blank" rel="noopener">Ver todas as avaliações no Google →</a></p>
      </div>
      <div class="grid grid--3">
{depoimentos}
      </div>
    </div>
  </section>

  <section class="section section--soft">
    <div class="container grid grid--2" style="align-items:center">
      <div>
        <span class="eyebrow">A loja</span>
        <h2>No centro de Santa Cruz do Sul</h2>
        <p>Estamos na {LOJA['rua']}, no centro, {LOJA['complemento'].split(', ', 1)[1]}. Venha conhecer a loja ou mande seu aparelho para diagnóstico.</p>
        <p>Atendemos clientes de toda a região:</p>
        <div class="chips">
{chips}
        </div>
        <p style="margin-top:24px"><a class="btn btn--primary" href="contato.html">Como chegar</a></p>
      </div>
      <img class="midia midia--retrato" src="img/fachada-dia.jpg" alt="Fachada da {LOJA['nome']}, na Rua Júlio de Castilhos, 361" width="900" height="1600" loading="lazy">
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="section__head">
        <span class="eyebrow">Dúvidas frequentes</span>
        <h2>Perguntas frequentes</h2>
      </div>
{faq_html(FAQ_HOME)}
    </div>
  </section>
  </main>
"""
    return (
        head(
            "Assistência técnica de celular em Santa Cruz do Sul | Oficina Cell Santa Cruz",
            "Conserto de celular em Santa Cruz do Sul: troca de tela, bateria e conector no mesmo dia, reparo em placa e iPhone. Garantia mínima de 90 dias. Orçamento pelo WhatsApp.",
            "",
            "",
            [faq_jsonld(FAQ_HOME)],
        )
        + header("", "inicio")
        + corpo
        + footer("")
    )


# ---------------------------------------------------------------- páginas de serviço
def pagina_servico(s):
    p = "../"
    sinais = "\n".join(f"          <li>{x}</li>" for x in s["sinais"])
    outros = "\n".join(
        f"""        <a class="card" href="{o['slug']}.html">
          <span class="card__icon">{I[o['icone']]}</span>
          <h3>{o['nome']}</h3>
          <p>{o['resumo']}</p>
          <span class="card__link">Saiba mais →</span>
        </a>"""
        for o in SERVICOS
        if o["slug"] != s["slug"]
    )
    servico_jsonld = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": s["titulo"],
        "serviceType": s["nome"],
        "description": s["seo_desc"],
        "provider": {"@type": "MobilePhoneStore", "name": LOJA["nome"], "url": LOJA["dominio"] + "/"},
        "areaServed": [{"@type": "City", "name": c} for c in CIDADES],
    }
    corpo = f"""  <main>
  <section class="page-hero">
    <div class="container">
      <div>
        <nav class="breadcrumb" aria-label="Você está em"><a href="{p}index.html">Início</a> › <a href="{p}index.html#servicos">Serviços</a> › {s['nome']}</nav>
        {f'<p class="selo">{I["estrela"]} {s["destaque"]}</p>' if s.get('destaque') else ''}
        <h1>{s['titulo']}</h1>
        <p class="hero__lead">{s['lead']}</p>
        <div class="facts">
          <div class="fact"><small>Prazo</small><strong>{prazo_texto(s)}</strong></div>
          <div class="fact"><small>Garantia</small><strong>Mínimo 90 dias</strong></div>
          <div class="fact"><small>Atendemos</small><strong>{s.get('atende', 'Apple e Android')}</strong></div>
        </div>
        <a class="btn btn--whats" href="{whats_link('Olá, Oficina Cell Santa Cruz! Gostaria de um orçamento de ' + s['nome'].lower() + '.')}" target="_blank" rel="noopener">{I['whats']} Orçamento pelo WhatsApp</a>
      </div>
{form_orcamento(s['problema_form'], 'Orçamento sem compromisso')}
    </div>
  </section>

  <section class="section">
    <div class="container grid grid--2">
      <div>
        <h2>Sinais de que você precisa deste serviço</h2>
        <ul class="checklist">
{sinais}
        </ul>
      </div>
      <div class="placeholder">[Foto: {s['nome'].lower()} sendo feita na bancada]</div>
    </div>
  </section>

  <section class="section section--soft">
    <div class="container">
      <div class="section__head"><h2>Como funciona</h2></div>
      <div class="grid grid--3 steps">
        <div class="step"><h3>Diagnóstico</h3><p>Avaliamos o aparelho e confirmamos qual é o defeito.</p></div>
        <div class="step"><h3>Orçamento e aprovação</h3><p>Você recebe o valor e o prazo e decide se quer seguir.</p></div>
        <div class="step"><h3>Reparo e garantia</h3><p>Você retira o aparelho com garantia mínima de 90 dias.</p></div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="section__head"><h2>Perguntas frequentes sobre {s['nome'].lower()}</h2></div>
{faq_html(s['faq'])}
    </div>
  </section>

  <section class="section section--soft">
    <div class="container">
      <div class="section__head"><h2>Outros serviços</h2></div>
      <div class="grid grid--4 grid--compacto">
{outros}
      </div>
    </div>
  </section>
  </main>
"""
    return (
        head(s["seo_titulo"], s["seo_desc"], f"servicos/{s['slug']}.html", p, [servico_jsonld, faq_jsonld(s["faq"])])
        + header(p, "servicos")
        + corpo
        + footer(p)
    )


# ---------------------------------------------------------------- aparelhos e acessórios
FAQ_APARELHOS = [
    ("Os seminovos têm garantia?", "Sim. Todos os aparelhos vendidos têm garantia mínima de 90 dias, que pode ser maior conforme o produto."),
    ("Vocês aceitam meu usado na troca?", "Sim. Preencha a avaliação com o modelo e o estado do aparelho e respondemos pelo WhatsApp com uma proposta."),
    ("Como sei quais aparelhos estão disponíveis?", "Os aparelhos em estoque aparecem nesta página e no nosso Instagram. Para confirmar disponibilidade, chame no WhatsApp."),
]


def pagina_aparelhos():
    produto = f"""        <div class="card">
          <div class="placeholder placeholder--sm">[Foto do aparelho]</div>
          <h3 style="margin-top:16px">{pendente('Modelo')}</h3>
          <p>{pendente('Armazenamento')} · {pendente('Estado de conservação')} · {pendente('Saúde da bateria')}</p>
          <span class="tag">Garantia mínima de 90 dias</span>
          <a class="card__link" href="{whats_link('Olá, Oficina Cell Santa Cruz! Tenho interesse em um aparelho do site.')}" target="_blank" rel="noopener">Tenho interesse →</a>
        </div>"""
    produtos = "\n".join([produto] * 3)
    acessorios = [
        ("Películas", "Para proteger a tela do seu modelo."),
        ("Capas", "Proteção contra quedas e riscos."),
        ("Carregadores e cabos", "Para iPhone e Android."),
        ("Fones e áudio", "Com fio e Bluetooth."),
        ("Para MacBook", "Carregadores, cabos, adaptadores e hubs."),
    ]
    acess_html = "\n".join(
        f"""        <div class="card">
          <h3>{n}</h3>
          <p>{d}</p>
        </div>"""
        for n, d in acessorios
    )
    corpo = f"""  <main>
  <section class="page-hero">
    <div class="container">
      <div>
        <nav class="breadcrumb" aria-label="Você está em"><a href="index.html">Início</a> › Aparelhos e acessórios</nav>
        <h1>Celulares novos, seminovos e acessórios em Santa Cruz do Sul</h1>
        <p class="hero__lead">iPhone e Android novos e seminovos, com garantia mínima de 90 dias. Traga seu usado para avaliarmos na troca.</p>
        <div class="hero__actions">
          <a class="btn btn--whats" href="{whats_link('Olá, Oficina Cell Santa Cruz! Quero saber quais aparelhos estão disponíveis.')}" target="_blank" rel="noopener">{I['whats']} Ver disponíveis no WhatsApp</a>
          <a class="btn btn--ghost" href="{LOJA['instagram']}" target="_blank" rel="noopener">{I['instagram']} Instagram</a>
        </div>
      </div>
      <div class="placeholder">[Foto: vitrine de aparelhos da loja]</div>
    </div>
  </section>

  <section class="section" id="seminovos">
    <div class="container">
      <div class="section__head">
        <span class="eyebrow">Novos e seminovos</span>
        <h2>Aparelhos disponíveis</h2>
        <p>Cada aparelho é anunciado com estado de conservação, saúde da bateria e garantia.</p>
      </div>
      <div class="grid grid--3">
{produtos}
      </div>
    </div>
  </section>

  <section class="section section--soft" id="troca">
    <div class="container grid grid--2" style="align-items:start">
      <div>
        <span class="eyebrow">Troca ou venda</span>
        <h2>Avalie seu aparelho usado</h2>
        <p>Informe o modelo e o estado do aparelho. Respondemos pelo WhatsApp com uma proposta para usar na troca ou vender.</p>
        <ul class="checklist">
          <li>Avaliação sem compromisso</li>
          <li>Seu usado pode entrar como parte do pagamento</li>
          <li>Atendimento na loja do centro</li>
        </ul>
      </div>
      <form class="quote" data-avaliacao aria-labelledby="aval-titulo">
        <h2 id="aval-titulo">Avaliar meu aparelho</h2>
        <div class="form-row">
          <div class="field">
            <label for="av-modelo">Modelo</label>
            <input id="av-modelo" name="modelo" placeholder="Ex.: iPhone 12" required>
          </div>
          <div class="field">
            <label for="av-arm">Armazenamento</label>
            <select id="av-arm" name="armazenamento">
              <option>64 GB</option><option>128 GB</option><option>256 GB</option><option>512 GB ou mais</option><option>Não sei</option>
            </select>
          </div>
        </div>
        <div class="field">
          <label for="av-estado">Estado</label>
          <select id="av-estado" name="estado">
            <option>Como novo, sem marcas</option>
            <option>Bom, com marcas leves de uso</option>
            <option>Com riscos ou amassados</option>
            <option>Com defeito ou tela quebrada</option>
          </select>
        </div>
        <div class="field">
          <label for="av-interesse">Interesse</label>
          <select id="av-interesse" name="interesse">
            <option>Trocar por outro aparelho</option>
            <option>Vender</option>
          </select>
        </div>
        <button class="btn btn--whats btn--block" type="submit">{I['whats']} Enviar pelo WhatsApp</button>
      </form>
    </div>
  </section>

  <section class="section" id="acessorios">
    <div class="container">
      <div class="section__head">
        <span class="eyebrow">Acessórios</span>
        <h2>Acessórios para celular e MacBook</h2>
        <p>Consulte os modelos disponíveis na loja ou pelo WhatsApp.</p>
      </div>
      <div class="grid grid--3">
{acess_html}
      </div>
    </div>
  </section>

  <section class="section section--soft">
    <div class="container">
      <div class="section__head"><h2>Perguntas frequentes</h2></div>
{faq_html(FAQ_APARELHOS)}
    </div>
  </section>
  </main>
"""
    return (
        head(
            "Celulares novos e seminovos em Santa Cruz do Sul | Oficina Cell Santa Cruz",
            "iPhone e Android novos e seminovos com garantia mínima de 90 dias em Santa Cruz do Sul. Avalie seu usado para troca. Acessórios para celular e MacBook.",
            "aparelhos.html",
            "",
            [faq_jsonld(FAQ_APARELHOS)],
        )
        + header("", "aparelhos")
        + corpo
        + footer("")
    )


# ---------------------------------------------------------------- a loja e contato
def pagina_contato():
    horario = LOJA["horario"] or pendente("Horário de funcionamento")
    cnpj = LOJA["cnpj"] or pendente("CNPJ")
    corpo = f"""  <main>
  <section class="page-hero">
    <div class="container">
      <div>
        <nav class="breadcrumb" aria-label="Você está em"><a href="index.html">Início</a> › A loja e contato</nav>
        <h1>A loja e contato</h1>
        <p class="hero__lead">Estamos no centro de Santa Cruz do Sul, {LOJA['complemento'].split(', ', 1)[1]}. Venha até a loja ou fale com a gente pelo WhatsApp.</p>
        <ul class="contact-list">
          <li>{I['loja']}<div><strong>Endereço</strong><br>{LOJA['rua']}, {LOJA['complemento']}<br>{LOJA['cidade']}/{LOJA['uf']} · CEP {LOJA['cep']}</div></li>
          <li>{I['whats']}<div><strong>WhatsApp</strong><br><a href="{whats_link()}" target="_blank" rel="noopener">{LOJA['whats_exibicao']}</a></div></li>
          <li>{I['instagram']}<div><strong>Instagram</strong><br><a href="{LOJA['instagram']}" target="_blank" rel="noopener">{LOJA['instagram_exibicao']}</a></div></li>
          <li>{I['relogio']}<div><strong>Horário</strong><br>{horario}</div></li>
          <li>{I['documento']}<div><strong>CNPJ</strong><br>{cnpj}</div></li>
        </ul>
      </div>
      <iframe class="map" title="Mapa da {LOJA['nome']}" src="{LOJA['mapa_embed']}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="section__head">
        <span class="eyebrow">Sobre nós</span>
        <h2>Especialistas em conserto de celulares e tablets</h2>
        <p>A {LOJA['nome']} é especializada em reparos avançados de placa da Apple e das grandes marcas. Também fazemos troca de tela, bateria e conector no mesmo dia, consertamos Apple Watch e MacBook, fazemos formatação e remoção de vírus, e vendemos aparelhos novos, seminovos e acessórios. Somos a única loja de Santa Cruz do Sul que troca só o vidro da tela, mantendo a tela original do celular ou do Apple Watch.</p>
        <p>Há {LOJA['anos']} anos atendemos Santa Cruz do Sul e região.</p>
      </div>
      <div class="grid grid--3">
        <img class="midia midia--card" src="img/fachada-noite.jpg" alt="Fachada da {LOJA['nome']} à noite, com o letreiro iluminado" width="900" height="1200" loading="lazy">
        <div class="placeholder">[Foto: bancada de reparo]</div>
        <div class="placeholder">[Foto: equipe]</div>
      </div>
    </div>
  </section>
  </main>
"""
    return (
        head(
            "Endereço e contato | Oficina Cell Santa Cruz, centro de Santa Cruz do Sul",
            f"Oficina Cell Santa Cruz: {LOJA['rua']}, centro de Santa Cruz do Sul/RS. WhatsApp {LOJA['whats_exibicao']}. Assistência técnica de celulares, aparelhos e acessórios.",
            "contato.html",
            "",
        )
        + header("", "contato")
        + corpo
        + footer("")
    )


# ---------------------------------------------------------------- arquivos auxiliares
def sitemap():
    urls = ["", "aparelhos.html", "contato.html"] + [f"servicos/{s['slug']}.html" for s in SERVICOS]
    itens = "\n".join(f"  <url><loc>{LOJA['dominio']}/{u}</loc></url>" for u in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{itens}\n</urlset>\n'


def robots():
    return f"User-agent: *\nAllow: /\n\nSitemap: {LOJA['dominio']}/sitemap.xml\n"


def escrever(caminho, conteudo):
    destino = RAIZ / caminho
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(conteudo, encoding="utf-8")
    print("gerado:", caminho)


def main():
    escrever("index.html", pagina_inicial())
    escrever("aparelhos.html", pagina_aparelhos())
    escrever("contato.html", pagina_contato())
    for s in SERVICOS:
        escrever(f"servicos/{s['slug']}.html", pagina_servico(s))
    escrever("sitemap.xml", sitemap())
    escrever("robots.txt", robots())


if __name__ == "__main__":
    main()
