from pathlib import Path
import os
import environ
from datetime import timedelta

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
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',
    'django_filters',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'knox',
    'axes',
    'apps.customer',
    'apps.product',
    'apps.vendors',
    'apps.provision',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # corsheaders middleware
    'corsheaders.middleware.CorsMiddleware',
    
    # handling suspicious logins
    'axes.middleware.AxesMiddleware',
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
    # authentication classes
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

# REST Framework JWT Authentication
SIMPLE_JWT = {
        'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),
        'REFRESH_TOKEN_LIFETIME': timedelta(days=20),
        'ROTATE_REFRESH_TOKENS': True,
        'BLACKLIST_AFTER_ROTATION': True,
        'UPDATE_LAST_LOGIN': False,

        # encryption algorithm
        'ALGORITHM': 'HS256',

        'VERYFYING_KEY': None,
        'AUDIENCE': None,
        'ISSUER': None,
        'JWK_URL': None,
        'LEEWAY': 0,

        'JTI_CLAIM': 'jti',

        'AUTH_HEADER_TYPES': ('Bearer', ),
        'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
        'USER_ID_FIELD': 'id',
        'USER_ID_CLAIM': 'user_id',
        "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

        'AUTH_TOKEN_CLASSES': [
            'rest_framework_simplejwt.tokens.AccessToken'
        ],
        'TOKEN_TYPE_CLAIM': 'token_type',
        'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

        'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
        'SLIDING_TOKEN_LIFETIME': timedelta(minutes=10),
        'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),

        "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
        "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
        "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
        "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
        "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
        "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}

# Backend POST server authentication
# Default authentication for API routes (registration, login, ...)
AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend'
]

# enabling axes plugin functionality
AXES_ENABLED = False

# setting up number of allowed login attempts
AXES_FAILURE_LIMIT = 3

# setting up axes cooloff timer to next login
AXES_COOLOFF_TIME = 1 # for one hour

# ckeditor upload url
CKEDITOR_UPLOAD_PATH = 'uploads/'

# ckeditor configs set-up
CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        'codeSnippet_theme': 'monokai',
        'toolbar': 'all',
        'extraPlugins': ','.join(
            [
                'widget',
                'dialog'
            ]
        ),
    }
}

ROOT_URLCONF = 'project.urls'

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

WSGI_APPLICATION = 'project.wsgi.app'


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

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "var/www/boltshift/static_files")

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
AUTH_USER_MODEL = 'customer.Customer'


# Customizing the admin panel
JAZZMIN_SETTINGS = {
    "site_title": "Boltshift Admin",
    "site_header": "Boltshift",
    "site_logo": "logo/neutral1.png",
    'site_brand': 'Boltshift Admin | Dashboard',
    "welcome_sign": "Welcome to Boltshift Admin Panel",
    'copyright': 'Boltshift Marketplace',
    "show_ui_builder": True,
    "custom_css": "css/admin.css",

    # user avatar/profile image
    "user_avatar": "image",
    
    # adding icons to the dashboard
    "icons": {
        "auth": "fas fa-users-cog", # default auth token icon
        'token_blacklist.blacklistedtoken': "fa fa-lock", # rest_framework auth token icon
        'token_blacklist.outstandingtoken': "fa fa-lock",
        "auth.user": "fas fa-user", # user icon
        "axes.accesslog": "fa fa-book",
        "axes.accessfailurelog": "fa fa-ban",
        "axes.accessattempt": "fa fa-key",
        "knox.authtoken": "fa fa-lock",
        "auth.Group": "fas fa-users", # group icon

        # customer icons
        "customer.Customer": "fa fa-user-plus",
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
        "product.Discount": "fa fa-percent",
        "product.ProductReview": "fa fa-star",
        "product.ProductOrders": "fa fa-shopping-cart",
        
        # provision icons
        "provision.CartItem": "fa fa-cart-plus",
        "provision.ShoppingSession": "fa fa-shopping-bag"
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