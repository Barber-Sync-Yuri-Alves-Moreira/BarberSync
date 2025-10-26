from pathlib import Path
import os
import dj_database_url # Importa o pacote que instalamos

BASE_DIR = Path(__file__).resolve().parent.parent

# 1. Lê a SECRET_KEY do Vercel. Você DEVE adicionar isso lá.
# Use a sua chave antiga para manter a consistência
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-pg-m0)+*hyd7x*&6o6js68b$0qh7k)m)da_fp81om1!y)r$+y%')

# 2. Lê o DEBUG. No Vercel, será 'False' por padrão.
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# 3. Lê os hosts permitidos. O Vercel adiciona a URL do seu site automaticamente
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '.vercel.app').split(',')
if 'VERCEL_URL' in os.environ and os.environ['VERCEL_URL'] not in ALLOWED_HOSTS:
     ALLOWED_HOSTS.append(os.environ['VERCEL_URL'])

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'agenda',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'barbersync_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'barbersync_project.wsgi.application'

# 4. Configuração do Banco de Dados (Lê a variável do Vercel)
DATABASES = {
    'default': dj_database_url.config(
        # Usa a variável POSTGRES_URL que o Vercel criou
        default=os.environ.get('POSTGRES_URL'), 
        conn_max_age=600,
        ssl_require=True # Neon (o banco do Vercel) exige SSL
    )
}

# Fallback para o banco local se a variável não existir (para rodar no seu PC)
if not DATABASES['default']:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'barbersync',
        'USER': 'postgres',
        'PASSWORD': 'postgre',
        'HOST': 'localhost',
        'PORT': '5432',
    }


AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Bahia' 
USE_I18N = True
USE_TZ = True 

# 5. Configuração de Estáticos para Vercel
STATIC_URL = 'static/'
STATICFILES_DIRS = [ BASE_DIR / "static", ]
STATIC_ROOT = BASE_DIR / "staticfiles_build" 

MEDIA_URL = '/media/'
# ATENÇÃO: Uploads de mídia (fotos) NÃO funcionam de forma persistente no Vercel.
# As fotos que você subir no admin vão sumir depois de um tempo.
# O ideal é usar um serviço como o Amazon S3, mas para testes isso funciona:
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_build') 

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configs do Jazzmin
JAZZMIN_SETTINGS = {
    "site_title": "Cleber Barbearia", "site_header": "BarberSync", "site_brand": "BarberSync",
    "welcome_sign": "Bem-vindo ao BarberSync", "copyright": "BarberSync Ltd",
    "topmenu_links": [
        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},
        {"app": "agenda"},
    ],
    "show_sidebar": True, "navigation_expanded": True,
    "order_with_respect_to": ["agenda", "auth"],
    "icons": {
        "auth": "fas fa-users-cog", "auth.user": "fas fa-user", "auth.Group": "fas fa-users",
        "agenda.barbeiros": "fas fa-cut", "agenda.servicos": "fas fa-stream",
        "agenda.barbeirosservicos": "fas fa-link", "agenda.horariosdisponiveis": "fas fa-calendar-alt",
    },
    "default_icon_parents": "fas fa-chevron-circle-right", "default_icon_children": "fas fa-circle",
    "related_modal_active": False, "custom_css": "css/admin_custom.css", "custom_js": None,
    "show_ui_builder": False, "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
}
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False, "footer_small_text": False, "body_small_text": False,
    "brand_small_text": False, "brand_colour": "navbar-dark", "accent": "accent-primary",
    "navbar": "navbar-dark navbar-expand-sm", "no_navbar_border": False, "navbar_fixed": False,
    "layout_boxed": False, "footer_fixed": False, "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary", "sidebar_nav_small_text": False, "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False, "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False, "sidebar_nav_flat_style": True, "theme": "darkly",
    "dark_mode_theme": "darkly",
    "button_classes": {
        "primary": "btn-primary", "secondary": "btn-secondary", "info": "btn-info",
        "warning": "btn-warning", "danger": "btn-danger", "success": "btn-success"
    }
}