# 📚 Sistema de Troca de Livros - Sebo Online

Este é um projeto web desenvolvido para facilitar a troca de livros entre usuários, funcionando como um sebo online colaborativo. A plataforma permite que os usuários cadastrem livros, ofereçam para troca e realizem trocas de maneira segura e organizada. O projeto foi desenvolvido como parte de um trabalho acadêmico para o Projeto Integrador da **UNIVESP**, utilizando tecnologias modernas e focando em acessibilidade.

## 🚀 Funcionalidades

- **Cadastro de Usuários e Autenticação:**
  - Os usuários podem criar suas contas, realizar login e gerenciar suas informações de perfil.
  - Sistema de autenticação seguro utilizando as funcionalidades nativas do Django.

- **Cadastro e Gerenciamento de Livros:**
  - Permite adicionar, editar e excluir livros, com detalhes como título, autor, gênero e sinopse.
  - Opção de adicionar imagens dos livros via upload ou link direto.
  - Sistema de validação de campos, com mensagens de erro e preenchimento obrigatório.

- **Troca de Livros:**
  - Funcionalidade central que permite aos usuários listar seus livros disponíveis para troca.
  - Proposta de troca entre usuários, onde cada parte pode aceitar ou recusar a oferta.
  - Sistema de notificações para informar o status das trocas e o histórico de transações.

- **Acessibilidade:**
  - Implementação de uma API de acessibilidade utilizando a **Web Speech API**.
  - Recurso de leitura em voz alta para facilitar a navegação de usuários com deficiência visual.
  - Botões de leitura foram integrados aos templates HTML, permitindo a conversão de texto para áudio diretamente no navegador.

- **Tratamento de Erros e Feedback ao Usuário:**
  - Mensagens claras de sucesso e erro para ações realizadas na plataforma.
  - Validação de campos em tempo real, com feedback visual para preenchimento incorreto ou ausente.

## 🗄️ Estrutura de Banco de Dados

- Utiliza o **SQLite** para armazenamento inicial dos dados, incluindo tabelas para usuários, livros e trocas.
- Relacionamentos implementados entre as tabelas para garantir a integridade dos dados e evitar inconsistências.

## 🛠️ Tecnologias Utilizadas

- **Django**: Framework backend seguindo o padrão MVT (Model-View-Template).
- **HTML, CSS e Bootstrap**: Desenvolvimento do frontend responsivo e amigável.
- **JavaScript**: Funcionalidades dinâmicas e integração com APIs, incluindo validação de formulários e acessibilidade.
- **SQLite**: Banco de dados leve e eficiente para prototipagem.
- **Web Speech API**: API para leitura em voz alta e acessibilidade.
- **Git e GitHub**: Controle de versão e colaboração no desenvolvimento.
- **Heroku**: Plataforma de deploy para hospedagem da aplicação.

## 🌐 API de Acessibilidade

A aplicação inclui uma API de acessibilidade para melhorar a experiência de usuários com deficiência visual. Utilizando a **Web Speech API**, foi implementada a funcionalidade de leitura em voz alta do conteúdo textual das páginas, oferecendo uma navegação mais inclusiva. O recurso pode ser ativado pelos usuários através de botões específicos na interface.

### Como Funciona:

- Ao clicar no botão de leitura, o texto é lido em voz alta utilizando a função `speechSynthesis` do navegador.
- Suporta a leitura em português (`pt-BR`), proporcionando uma experiência personalizada para usuários brasileiros.

## 📈 Estrutura e Organização do Projeto

A estrutura do projeto segue as boas práticas de desenvolvimento web, utilizando o padrão MVT do Django:

