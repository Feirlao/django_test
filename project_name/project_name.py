from django.conf.urls import  url
from  django.http import HttpResponse
from django.conf    import settings
import sys
import os

DEBUG=os.environ.get('DEBUG','ON')=='on'

SECRET_KEY=os.environ.get(' SECRET_KEY','{{secret_key}}')



settings.configure(

    DEBUG=DEBUG,
    SECRET_KEY=SECRET_KEY,
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASS = (
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
                       ),
    )


def index(request):
    return HttpResponse('hello')

urlpatterns=(
    url(r'^$',index),
)

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)