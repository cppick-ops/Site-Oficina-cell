# Atendente virtual no WhatsApp

A IA (Claude) responde os clientes no WhatsApp da loja: tira dúvidas, faz a triagem do conserto, explica o boleto em até 18x e passa a conversa para alguém da loja quando precisa.

## Como funciona

1. O cliente manda uma mensagem. A Meta avisa o endereço `/api/whatsapp` do site, na Vercel.
2. A IA espera uns segundos (o cliente costuma mandar várias mensagens seguidas) e responde tudo de uma vez.
3. Quando a triagem termina, o cliente quer comprar, pede uma pessoa ou a IA não sabe responder, ela se despede e **para de responder aquele cliente por 12 horas**. A conversa fica com você no app WhatsApp Business.
4. Se você responder qualquer cliente pelo app, a IA também sai daquela conversa por 12 horas, para não atropelar você.
5. A IA nunca passa preços. Ela lembra a conversa por 24 horas depois da última mensagem.

O que a IA sabe sobre a loja está em `api/_lib/conhecimento.js`. Mudou horário, serviço ou condição? Atualize lá.

## Arquivos

| Arquivo | O que faz |
| --- | --- |
| `api/whatsapp.js` | Recebe os avisos da Meta |
| `api/_lib/conhecimento.js` | Instruções e informações da loja para a IA |
| `api/_lib/atendente.js` | Junta as mensagens, chama o Claude, responde e passa para a loja |
| `api/_lib/whatsapp.js` | Envia mensagens e lê os avisos da Meta |
| `api/_lib/memoria.js` | Guarda conversas e pausas no Redis |
| `teste/atendente.test.js` | Simula clientes, sem gastar nada (`npm test`) |

## Configuração (uma vez só)

### 1. Banco de dados na Vercel

No painel da Vercel, abra o projeto do site > **Storage** > **Upstash for Redis** (plano gratuito) > conecte ao projeto. As variáveis `KV_REST_API_URL` e `KV_REST_API_TOKEN` são criadas sozinhas.

### 2. Chave do Claude

Em [platform.claude.com](https://platform.claude.com), crie uma chave de API e coloque créditos. Na Vercel, em **Settings > Environment Variables**, crie `ANTHROPIC_API_KEY` com essa chave.

### 3. App na Meta

1. Em [developers.facebook.com](https://developers.facebook.com), crie um app do tipo **Business** e adicione o produto **WhatsApp**, ligado ao portfólio empresarial (Meta Business) da loja.
2. **O número de teste da Meta não serve no Brasil.** Ele é dos EUA, e a Meta bloqueia mensagens de empresas de fora do Brasil para brasileiros (erro 130497). Por isso o teste é feito direto no número da loja, com o modo de teste ligado (veja abaixo).
3. Para usar o número atual **(51) 99525-5010** sem deixar de usar o app WhatsApp Business no celular, a Meta oferece a **coexistência**: o número fica no app e na API ao mesmo tempo, e as conversas aparecem nos dois. O app WhatsApp Business precisa estar atualizado. Na hora de conectar, confira se a opção de conectar um número que já usa o app aparece para a sua conta. Se não aparecer, a alternativa é passar por um parceiro oficial da Meta (BSP) que ofereça coexistência. **Não** cadastre o número da loja do jeito comum, que tira o número do app.

### 4. Variáveis da Meta na Vercel

| Variável | Onde achar |
| --- | --- |
| `WHATSAPP_PHONE_NUMBER_ID` | WhatsApp > Configuração da API > "Identificação do número de telefone" |
| `WHATSAPP_TOKEN` | Configurações do negócio > Usuários do sistema > crie um usuário do sistema, adicione o app e gere um token com a permissão `whatsapp_business_messaging`. O token temporário da tela de teste expira em 24h. |
| `WHATSAPP_APP_SECRET` | Configurações do app > Básico > Chave secreta do app |
| `WHATSAPP_VERIFY_TOKEN` | Invente uma senha qualquer (ex.: uma frase longa). Vai ser usada no passo 5. |
| `TELEFONES_LIBERADOS` | **Modo de teste.** Números separados por vírgula (ex.: `5551983496440`). Com ela preenchida, a IA só responde a esses números e ignora os clientes. Para a IA atender todo mundo, apague a variável e faça um novo deploy. |

Depois de criar as variáveis, faça um novo deploy (as variáveis só valem a partir do próximo deploy).

### 5. Webhook

Em WhatsApp > Configuração, no **Webhook**:

- URL de retorno: `https://www.oficinacell.com.br/api/whatsapp` (ou o endereço `.vercel.app` do projeto, enquanto o domínio não aponta para a Vercel)
- Token de verificação: o mesmo `WHATSAPP_VERIFY_TOKEN`
- Assine os campos **messages** e **smb_message_echoes** (este último é o que faz a IA sair da conversa quando você responde pelo app)

Pronto: mande uma mensagem para o número e veja a resposta. Os registros ficam em Vercel > projeto > **Logs**; as linhas `[ATENDENTE]` mostram cada vez que a IA passou um cliente para a loja, com o resumo do que ele quer.

## Custos

- **Meta:** responder mensagens que o cliente mandou é gratuito. Só mensagens que a loja inicia (promoções, lembretes) são cobradas, e esse sistema não manda nenhuma.
- **Claude:** cobrado por uso. Com o modelo atual (Claude Haiku 5.5), uma conversa custa uma fração de centavo de dólar: 20 a 30 conversas por dia dão uns US$ 2 a 3 por mês. Acompanhe em platform.claude.com > Usage. Se as respostas ficarem fracas, troque `MODELO` em `api/_lib/atendente.js` por `claude-sonnet-5-5` (uns US$ 30 a 47 por mês no mesmo volume).
- **Vercel e Upstash:** o plano gratuito deve bastar para o volume de uma loja.

## Publicar o app na Meta

Para receber mensagens de clientes de verdade, o app precisa estar publicado (modo "Live"). A Meta pede:

- Política de privacidade: `https://www.oficinacell.com.br/privacidade.html`
- Exclusão de dados: o mesmo endereço (a página explica como pedir)
- Ícone: `img/logo-icone.png`
- Categoria: Negócios e páginas (ou Mensagens)

## Limites desta primeira versão

- A IA não vê fotos nem ouve áudios: ela pede para o cliente escrever.
- Ela não sabe o estoque. Quem pergunta por aparelho é passado para a loja.
- Não tem um aviso separado para você quando a IA passa alguém: a conversa aparece no app como sempre, e a última mensagem da IA diz que um atendente vai continuar.
- Para a IA voltar a atender um cliente antes das 12 horas, não há botão: é só esperar.
