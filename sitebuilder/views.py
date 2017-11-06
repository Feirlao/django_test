import os
from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.template import  Template
from  django.utils._os import safe_join

def get_page_or_404(name):
    #返回一个页面404错误
    try:
        file_path=safe_join(settings.SITE_PAGES_DIRECTORY,name)#
    except ValueError:
        raise Http404('page not found')
    else:
        if not os.path.exists(file_path): #打开每个文件并使用文件内容创建新的模板
            raise Http404('Page Not Found')

    with open(file_path,'r') as f:
        page=Template(f.read())

    return page

def page(request,slug='index'):
    #将要修饰的page和slug的上下文传递给page.html
    file_name='{}.html'.format(slug)
    page=get_page_or_404(file_name)
    context={
        'slug':slug,
        'page':page,
    }
    return render(request,'page.html',context)
