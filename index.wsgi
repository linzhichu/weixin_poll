import os
import sae
import django.core.handlers.wsgi
os.environ['DJANGO_SETTINGS_MODULE']='weixinpoll.settings'
application = sae.create_wsgi_app(django.core.handlers.wsgi.WSGIHandler())
