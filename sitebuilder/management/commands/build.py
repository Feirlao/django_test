import os
import shutil
from django.core.management import call_command
from django.core.management.base import BaseCommand,CommandError
from django.urls import reverse
from django.test.client import Client
from django.conf import settings



def get_pages():
    for name in os.listdir(settings.SITE_PAGES_DIRECTORY):#遍历pages 文件夹 收集.html文件
        if name.endswith('.html'): #endswith() 方法用于判断字符串是否以指定后缀结尾
            # 如果以指定后缀结尾返回True，否则返回False
            yield name[:-5]

class Command(BaseCommand):
    help='Build static site output'
    leave_locale_alone = True

    def add_arguments(self, parser): #检查是否有参数传入命令
        parser.add_argument('args',nargs='*')


    def handle(self, *args, **options):
        settings.DEBUG=False
        settings.COMPRESS_ENABLED=True

        if args:
            pages=args
            available=list(get_pages())
            print(available)
            invalid=[]
            for page in pages:
                if page not in available:
                    invalid.append(page)
                if invalid:
                    msg='Invalid pages: {}'.format(','.join(invalid))
                    #如果某个文件不存在,则报错
                    raise CommandError(msg)


        if os.path.exists(settings.SITE_OUTPUT_DIRECTORY):#检查输出目录是否存在
            # ,存在则删除并创建一个新的output目录
            shutil.rmtree(settings.SITE_OUTPUT_DIRECTORY) #递归的去删除文件
        os.mkdir(settings.SITE_OUTPUT_DIRECTORY)
        os.makedirs(settings.STATIC_ROOT,exist_ok=True) #创建递归的目录树

        call_command('collectstatic',interactive=False,clear=True,verbosity=0)
        call_command('compress',force=True)

        client=Client()
        for page in get_pages(): #遍历pages 文件夹 收集.html文件
            url=reverse('page',kwargs={'slug':page})
            response=client.get(url)


            if page == 'index':
                output_dir=settings.SITE_OUTPUT_DIRECTORY
            else:
                output_dir=os.path.join(settings.SITE_OUTPUT_DIRECTORY,page)
                os.makedirs(output_dir)
            with open(os.path.join(output_dir,'index.html'),'wb') as f:
                #将模板修改为静态内容, 模拟朱雀网站页面并将修饰过的内容写入site_output_directory

                f.write(response.content)
