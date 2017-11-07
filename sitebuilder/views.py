import os
import json
from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.template import Template, Context
from django.template.loader_tags import BlockNode
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

    meta=None
    for i,node in  enumerate(list(page.nodelist)):

                   #enumerate将其组成一个索引序列，利用它可以同时获得索引和值
        if isinstance(node,BlockNode) and node.name=='context':
            #判断变量node是否是BlockNode类型,遍历节点列表，检查名称为blocknode类，
            # block是用于创建{%block%}元素的类，如果找到定义一个元变量
            meta=page.nodelist.pop(i)
            print(meta)
            break
    page._meta=meta

    return page

def page(request,slug='index'):
    #将要修饰的page和slug的上下文传递给page.html
    file_name='{}.html'.format(slug)
    page=get_page_or_404(file_name)
    context={
        'slug':slug,
        'page':page,
    }
    if page._meta is not None:
        meta=page._meta.render(Context())
        extra_content=json.loads(meta)
        context.update(extra_content)
    return render(request,'page.html',context)
