from pathlib import Path
import os
import environ

# getting environment variables
env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-cr^=pqr7@bie(u*=hx-n4c#$z3!fb*7p=r!=l^_p1ol9m401(y'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.vercel.app']


# Application definition

INSTALLED_APPS = [
    # admin page customizer
    'jazzmin',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # my apps
    'customer',
    'product',
    'vendors',

    # API handling
    'rest_framework',

    # API Token Authentication
    'knox',

    # React Data Handling
    'corsheaders'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # corsheaders middleware
    'corsheaders.middleware.CorsMiddleware'
]

# Whitelisting the React-Django sync port
CORS_ORIGIN_WHITELIST = [
    'http://localhost:5173'
]

# Rest Framework allowed permissions
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'knox.auth.TokenAuthentication'
    ]
}

# Backend POST server authentication
AUTHENTICATION_BACKENDS = [
    'customer.auth.CustomAuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend'
]


ROOT_URLCONF = 'boltshift.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # os.path.join(BASE_DIR, 'templates')
        ],
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

WSGI_APPLICATION = 'boltshift.wsgi.app'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Media folder
MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Registering the custom user
AUTH_USER_MODEL = 'customer.CustomUser'


# Customizing the admin panel
JAZZMIN_SETTINGS = {
    "site_title": "Boltshift Admin",
    "site_header": "Boltshift",
    "site_logo": "logo/neutral1.png",
    'site_brand': 'Boltshift Admin',
    "welcome_sign": "Welcome to Boltshift Admin Panel",
    'copyright': 'Boltshift Marketplace',
    "show_ui_builder": True,
    "custom_css": "css/admin.css",

    # user avatar/profile image
    "user_avatar": "",
    
    # adding icons to the dashboard
    "icons": {
        "auth": "fas fa-users-cog", # default auth token icon
        "knox.authtoken": "fa fa-lock", # knox auth icon
        "auth.user": "fas fa-user", # user icon
        "auth.Group": "fas fa-users", # group icon

        # customer icons
        "customer.CustomUser": "fa fa-user-plus",
        "customer.CartItem": "fa fa-cart-plus",
        "customer.UserAddress": "fa fa-address-book",
        "customer.UserPayment": "fa fa-wallet",
        "customer.ProductReview": "fa fa-comments",
        "customer.ShoppingSession": "fa fa-shopping-bag",
        "customer.ProductOrders": "fa fa-retweet",

        # vendor icons
        "vendors.Vendor": "fa fa-industry",

        # product icons
        "product.ShoppingSession": "fa fa-shopping-basket",
        "product.Inventory": "fa fa-plus-circle",
        "product.Product": "fa fa-th-list",
        "product.ProductImage": "fa fa-camera",
        "product.Category": "fa fa-list-alt",
        "product.Discount": "fa fa-percent"
    },
}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "dark_mode_theme": "solar",
    "brand_colour": "navbar-dark",
    "no_navbar_border": False,
    "body_small_text": True,
    "navbar_fixed": True,
    "sidebar_fixed": True,
    "footer_fixed": True,
    "accent": "accent-navy",
    "sidebar": "sidebar-dark-primary",
}