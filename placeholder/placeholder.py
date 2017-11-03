
# -*- coding: utf-8 -*-
import hashlib
from django.conf import settings
import sys
import os
from PIL import Image,ImageDraw
from io import  BytesIO
from django.contrib import staticfiles

DEBUG=os.environ.get('DEBUG','ON')=='on'
SECRET_KEY=os.environ.get(' SECRET_KEY','-+tv(2$m-31qz+csa+jf_ci+@$5@a5ijr#m9_%a^_ec45s8fuw')
ALLOWED_HOSTS=os.environ.get('ALLOWED_HOSTS','127.0.0.1').split('.') #返回路径和文件名
BASE_DIR=os.path.dirname(__file__)
settings.configure(
    DEBUG=DEBUG,
    SECRET_KEY=SECRET_KEY,
    ROOT_URLCONF=__name__,
    ALLOWED_HOSTS='*',
    MIDDLEWARE_CLASS = (
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
                       ),
    INSTALLED_APPS=(
        'django.contrib.staticfiles',
    ),
    TEMPLATES=(
        {
            'BACKEND':'django.template.backends.django.DjangoTemplates',
            'DIRS':(os.path.join(BASE_DIR,'templates'),)
        },
    ),
    STATICFILES_DIRS=(
        os.path.join(BASE_DIR,'static'),
    ),
    STATIC_URL='/static/',
    )

from django import forms
from django.conf.urls import url
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.http import etag




class ImageForm(forms.Form):
    height=forms.IntegerField(min_value=1,max_value=2000)
    width=forms.IntegerField(min_value=1,max_value=2000)

    def generate(self,image_format='PNG'):
        height=self.cleaned_data['height']
        width=self.cleaned_data['width']

        key='{}.{}>{}'.format(width,height,image_format)
        content=cache.get(key)
        if content is None:
            image=Image.new('RGB',(width,height))
            draw = ImageDraw.Draw(image)
            text='{}*{}'.format(width,height)
            textwidth,textheight=draw.textsize(text)
            if textwidth <width and textheight < height:
                texttop =(height-textheight) //2
                textleft =(width-textwidth) //2
                draw.text((textleft,texttop),text,fill=(255,255,255))

            content=BytesIO()
            image.save(content,image_format)
            content.seek(0)
            cache.set(key,content,60*60)
        return content

def generrate_etag(request,width,height):
    content ='placeholder:{0}*{1}'.format(width,height)
    return hashlib.sha1(content.encode('utf-8')).hexdigest()



@etag(generrate_etag)
def placeholder(request,width,height):
    form= ImageForm({'height':height,'width':width})
    if form.is_valid():
        image=form.generate()
        return HttpResponse(image,content_type='image/png')
    else:
        return HttpResponse('Invilid Image Request')


def index(request):
    example=reverse('placeholder',kwargs={'width':50,'height':50}) # 翻转 试图来创建一个URL的样例
    context={
        'example':request.build_absolute_uri(example) #返回 example 的绝对URL
    }
    return render(request,'home.html',context) #渲染 home.html模板

urlpatterns=(
    url(r'^$',index,name='homepage'),
    url(r'^image/(?P<width>[0-9]+)*(?P<height>[0-9]+)/$',placeholder,
        name='placeholder',),
)
application=get_wsgi_application()

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)