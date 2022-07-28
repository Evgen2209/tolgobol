# -*- coding: utf-8 -*-
import sys, os
sys.path.append('/home/g/gorbunmu/tolgobol-village.ru/public_html/TolgobolVillage') # указываем директорию с проектом
sys.path.append('/home/g/gorbunmu/.local/lib/python3.6/site-packages') # указываем директорию с библиотеками, куда поставили Flask
os.environ['DJANGO_SETTINGS_MODULE'] = 'TolgobolVillage.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
