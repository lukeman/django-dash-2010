ALLDIRS = ['/home/django/domains/elesma.lethain.com/django-dash-2010/elesma/lib/python2.5/site-packages']
import os
import sys
import site

prev_sys_path = list(sys.path)

for directory in ALLDIRS:
    site.addsitedir(directory)

new_sys_path = []
for item in list(sys.path):
    if item not in prev_sys_path:
       new_sys_path.append(item)
       sys.path.remove(item)
sys.path[:0] = new_sys_path

sys.path.append('/home/django/domains/elesma.lethain.com/django-dash-2010/elesma_project')
sys.path.append('/home/django/domains/elesma.lethain.com/django-dash-2010/elesma_project/apps')

os.environ['PYTHON_EGG_CACHE'] = '/home/django/.python-eggs'
os.environ['DJANGO_SETTINGS_MODULE'] = 'elesma_project.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
