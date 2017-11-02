from django.conf.urls import  url
from  django.http import HttpResponse
from django.conf    import settings
import sys
import os
from django import forms
from PIL import Image

DEBUG=os.environ.get('DEBUG','ON')=='on'

SECRET_KEY=os.environ.get(' SECRET_KEY','-+tv(2$m-31qz+csa+jf_ci+@$5@a5ijr#m9_%a^_ec45s8fuw')



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



class ImageForm(forms.Form):

    height=forms.IntegerField(min_value=1,max_value=2000)
    width=forms.IntegerField(min_value=1,max_value=2000)
    def generate(self,image_format='PNG'):
        height=self.cleaned_data['height']
        width=self.cleaned_data['width']
        image=Image.new('RGB',(width,height))
        image.save(content,image_format)
        content.seek(0)
        return content
def index(request):
    return HttpResponse('hello')


def placeholder(request,width,height):
    form= ImageForm({'height':height,'width':width})
    if form.is_valid():
        height =form.cleaned_data['height']
        width =form.cleaned_data['width']
        return HttpResponse('OK')
    else:
        return HttpResponse('Invilid Image Request')




urlpatterns=(
    url(r'^$',index),
    url(r'^image/(?p<width>[0-9]+)*(?p<height>[0-9]+)/$',placeholder,
        name='placeholder',
)

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)