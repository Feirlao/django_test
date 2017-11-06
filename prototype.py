
# -*- coding: utf-8 -*-

from django.conf import settings
import sys
import os


BASE_DIR = os.path.dirname(__file__)
settings.configure(
    DEBUG=True,
    SECRET_KEY='-+tv(2$m-31qz+csa+jf_ci+@$5@a5ijr#m9_%a^_ec45s8fuw',
    ROOT_URLCONF='sitebuilder.urls',
    MIDDLEWARE_CLASS=(),
    INSTALLED_APPS=(
        'django.contrib.staticfiles',
        'sitebuilder',

    ),
    TEMPLATES=(
        {
            'BACKEND':'django.template.backends.django.DjangoTemplates',
            'DIRS':[],
            'APP_DIRS':True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },

        },
    ),
    STATIC_URL='/static/',
    SITE_PAGES_DIRECTORY=os.path.join(BASE_DIR,'pages'),
    STATICFILES_DIRS = [os.path.join(BASE_DIR, "/sitebuilder/static"), ]
     #country是生成的APP#

    )

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)