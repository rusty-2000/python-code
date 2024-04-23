import os
import sys

path = '/home/sarthak2000/ecommerce'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'ecommerce.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()