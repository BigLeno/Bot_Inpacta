# Documentação do Projeto Bot_Inpacta

## Descrição

O Bot_Inpacta é um bot do Telegram desenvolvido para a Incubadora Inpacta. Ele foi projetado para automatizar tarefas e fornecer informações úteis aos membros da incubadora. Com este bot, os usuários podem obter informações sobre os projetos atuais, receber atualizações sobre eventos futuros e interagir com outros membros da incubadora de maneira mais eficiente.

O bot é construído em Python e usa a API do Telegram para interagir com os usuários. Ele também se integra a outras ferramentas e serviços, como Google Sheets, para gerenciar e fornecer informações.

Este projeto está em constante desenvolvimento, com novos recursos e melhorias sendo adicionados regularmente. Confira a seção "Notas de Atualização" para ver o que há de novo na versão mais recente.

## Configuração

Para configurar o Bot_Inpacta, siga os passos abaixo:

1. **Clone o repositório**: Primeiro, clone o repositório do projeto para a sua máquina local usando o comando `git clone`.

2. **Instale as dependências**: O projeto requer algumas bibliotecas Python para funcionar corretamente. Você pode instalar todas as dependências necessárias usando o comando `pip install -r requirements.txt`.

3. **Configure as variáveis de ambiente**: O bot usa algumas variáveis de ambiente para funcionar corretamente. Crie um arquivo `.env` na raiz do projeto e adicione as seguintes variáveis:
    - `TELEGRAM_TOKEN`: O token do bot do Telegram.
    - `GOOGLE_SHEETS_API_KEY`: A chave da API do Google Sheets.

4. **Inicie o bot**: Finalmente, você pode iniciar o bot usando o comando `python ./app/app.py`.

## Uso

O Bot_Inpacta é fácil de usar. Após iniciar uma conversa com o bot no Telegram, você pode usar os seguintes comandos:

- `/start`: Inicia a interação com o bot.
- `/gestores`: Lista os gestores atuais.
- `/bolsistas`: Lista os bolsistas atuais.
- `/horarios`: Consulta os horários dos gestores.
- `/agendar`: Agenda reuniões com os gestores.

Cada comando deve ser enviado como uma mensagem no chat do bot. O bot responderá com a informação solicitada ou uma confirmação de que a ação foi realizada com sucesso.

Lembre-se de que o bot é uma ferramenta de automação e não substitui a interação humana. Se você tiver problemas ou perguntas que o bot não pode resolver, entre em contato com um membro da equipe.

## Notas de Atualização

### Versão 1.0.0 (07/12/2023)

- Lançamento inicial do Bot_Inpacta.
- Implementação da integração com o Google Sheets para gerenciar e fornecer informações.
- Adicionado comando `/start` para iniciar a interação com o bot.

### Versão 1.1.0 (09/12/2023)

- Adicionado comando `/gestores` para listar os gestores atuais.
- Melhorada a performance da integração com o Google Sheets.
- Corrigido bug que causava falha ao tentar acessar a planilha quando a conexão com a internet estava instável.

### Versão 1.2.0 (10/12/2023)

- Adicionado comando `/bolsistas` para listar os bolsistas atuais.
- Melhorada a formatação das mensagens enviadas pelo bot.
- Corrigido bug que causava falha ao tentar listar os bolsistas quando a planilha estava vazia.

### Versão 1.3.0 (11/12/2023)

- Adicionado comando `/horarios` para consultar os horários dos gestores.
- Melhorada a afetividade do bot em suas respostas.
- Corrigido bug que causava falha ao tentar listar os gestores quando a planilha estava vazia.

### Versão 1.4.0 (11/12/2023)

- Adicionado comando `/agendar` para agendar reuniões com os gestores.
- Melhorada a gestão de exceções para evitar falhas inesperadas.

### Versão 1.5.0 (12/12/2023)

- Melhorada a afetividade do bot em suas respostas.
- Corrigido bug que causava falha ao tentar agendar uma reunião para um horário inválido.
- Corrigido bug que causava falha ao tentar consultar os horários dos gestores quando a planilha estava vazia.

## Contribuição

Sua contribuição é muito bem-vinda! Se você tem ideias para novas funcionalidades ou melhorias e gostaria de contribuir para o projeto, aqui estão algumas maneiras de fazer isso:

- **Ideias para novas funcionalidades**: Se você tem uma ideia para uma nova funcionalidade que gostaria de ver no Bot_Inpacta, por favor, abra uma issue no GitHub descrevendo sua ideia.

- **Melhorias**: Se você encontrou um bug ou acha que alguma parte do bot poderia ser melhorada, sinta-se à vontade para abrir uma issue no GitHub. Por favor, inclua o máximo de detalhes possível para que possamos entender o problema e trabalhar em uma solução.

Lembre-se de que este é um projeto de código aberto e nós encorajamos contribuições de todos. Obrigado por ajudar a tornar o Bot_Inpacta ainda melhor!

## Licença

Este projeto está licenciado sob a licença MIT. Isso significa que você pode copiar, modificar, mesclar, publicar, distribuir, sublicenciar e/ou vender cópias do software, desde que inclua o seguinte aviso de direitos autorais em todas as cópias ou partes substanciais do software:


Para mais detalhes, por favor, veja o arquivo [LICENSE](LICENSE) no repositório do projeto.

Copyright (2023) (Rutileno Gabriel)
