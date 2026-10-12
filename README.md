# Site Oficina Cell Santa Cruz

Site da Oficina Cell Santa Cruz: assistência técnica de celulares, aparelhos novos e seminovos e acessórios em Santa Cruz do Sul/RS.

Site estático em HTML, CSS e JavaScript, sem dependências. Funciona em qualquer hospedagem simples, inclusive no GitHub Pages.

## Páginas

| Arquivo | Conteúdo |
| --- | --- |
| `index.html` | Página inicial: orçamento pelo WhatsApp, serviços, garantia, aparelhos, avaliações, região e perguntas frequentes |
| `servicos/*.html` | Uma página por serviço: tela, bateria, conector, placa, formatação e vírus |
| `aparelhos.html` | Novos, seminovos, avaliação do usado para troca e acessórios |
| `contato.html` | Endereço, mapa, contatos e "sobre nós" |

## Como editar

Cabeçalho, rodapé, textos e dados da loja ficam em `ferramentas/gerar_site.py`. Depois de editar, gere as páginas de novo:

```bash
python3 ferramentas/gerar_site.py
```

O visual fica em `css/style.css`. O número do WhatsApp usado pelos formulários fica em `js/main.js`.

## Conteúdos pendentes

Aparecem destacados em amarelo ou com borda tracejada no site:

- Fotos: fachada, bancada, equipe, vitrine e aparelhos à venda
- História da loja (anos de mercado)
- Aparelhos disponíveis para venda
