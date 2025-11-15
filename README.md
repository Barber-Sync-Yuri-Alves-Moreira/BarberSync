# BarberSync


BarberSync é um sistema web completo para gerenciamento de agendamentos
em barbearias. O projeto foi desenvolvido para otimizar o fluxo de
atendimento, eliminando a necessidade de agendamentos manuais (telefone
ou WhatsApp) e fornecendo uma interface digital simples para o Cliente e
um painel de controle robusto para o Administrador.

------------------------------------------------------------------------

##  Funcionalidades Principais

O sistema é dividido em duas partes: **Portal do Cliente (Frontend)** e
**Painel Administrativo (Backend)**.

------------------------------------------------------------------------

##  Frontend (Portal do Cliente)

O fluxo do cliente é **totalmente anônimo**, sem login, composto por **6
etapas intuitivas**:

1.  **Seleção de Barbeiro** -- Exibição dos profissionais disponíveis.\
2.  **Seleção de Serviço** -- Apenas serviços oferecidos pelo barbeiro
    escolhido (preço e duração).\
3.  **Seleção de Data** -- Calendário mostrando apenas os dias com
    horários livres.\
4.  **Seleção de Horário** -- Exibe os horários disponíveis (disponivel
    = True).\
5.  **Dados do Cliente** -- Formulário com Nome, Telefone e CPF (com
    validação).\
6.  **Confirmação via WhatsApp** -- Tela de sucesso com botão que abre o
    WhatsApp com mensagem pronta + redirecionamento para a página
    inicial.

------------------------------------------------------------------------

## Backend (Painel Administrativo)

Localizado em `/admin`, onde toda a lógica do negócio é gerenciada.

### Principais recursos:

-   **Autenticação segura** via tela de login.
-   **Tema moderno** com *django-jazzmin* (dark mode).
-   **Gestão Pai-Filho**:
    -   O Admin gerencia tudo dentro do cadastro do Barbeiro, através de
        inlines.\
    -   Impede erros e agiliza o workflow.
-   **Prevenção de Conflitos**
    -   Uso de `unique_together` para impedir horários duplicados para o
        mesmo barbeiro.
-   **Cancelamento Inteligente**
    -   Ao excluir um agendamento, o horário é automaticamente liberado
        (disponivel = True).
-   **"Arquivamento" Automático**
    -   Exibe apenas agendamentos de hoje e do futuro, evitando poluição
        visual.

------------------------------------------------------------------------

## Tecnologias Utilizadas

### Backend

-   Python 3.10+
-   Django 5+
-   Django Jazzmin
-   Whitenoise

### Frontend

-   HTML5\
-   CSS3 (puro, sem frameworks JS)

### Banco de Dados

-   PostgreSQL

------------------------------------------------------------------------

## Instalação e Execução (Guia para Avaliação)

### 1. Pré-requisitos

-   Python 3.10+\
-   PostgreSQL instalado e rodando

------------------------------------------------------------------------

### 2. Clonar o Repositório

    git clone https://github.com/Barber-Sync-Yuri-Alves-Moreira/BarberSync
    cd BarberSync.v1

------------------------------------------------------------------------

### 3. Criar Ambiente Virtual e Instalar Dependências

    python -m venv venv
    .env\Scriptsctivate   

    pip install django psycopg2-binary django-jazzmin whitenoise
     ou
    pip install -r requirements.txt

------------------------------------------------------------------------

### 4. Configurar o Banco no PostgreSQL

1.  Abra o pgAdmin\
2.  Crie um novo banco:

-   Nome: barbersync\
-   Encoding: UTF8


------------------------------------------------------------------------

### 5. Configurar settings.py

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'barbersync',
            'USER': 'postgres',
            'PASSWORD': 'SUA_SENHA_AQUI',
            'HOST': 'localhost',
            'PORT': '5432',
            'OPTIONS': {
                'options': '-c timezone=utc',
                'client_encoding': 'utf8'
            }
        }
    }

------------------------------------------------------------------------

### 6. Rodar a Aplicação

Criar migrações (se necessário):

    python manage.py makemigrations agenda

Aplicar migrações:

    python manage.py migrate

Criar superusuário:

    python manage.py createsuperuser

Coletar arquivos estáticos:

    python manage.py collectstatic

Iniciar servidor:

    python manage.py runserver

------------------------------------------------------------------------

### 7. Acessar o Sistema

-   Portal do Cliente: http://127.0.0.1:8000/\
-   Painel Admin: http://127.0.0.1:8000/admin/

------------------------------------------------------------------------

##  Autor

**Yuri Alves Moreira**\
📧 moreirayurialves@gmail.com


------------------------------------------------------------------------

© 2025 BarberSync\
Todos os direitos reservados.
