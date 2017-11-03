
# -*- coding: utf-8 -*-

from django.conf import settings
import sys



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
        },
    ),
    STATIC_URL='/static/',
    )

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)