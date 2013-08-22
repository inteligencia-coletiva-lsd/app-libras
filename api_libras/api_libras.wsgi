import logging
# Check the official documentation http://flask.pocoo.org/docs/deploying/mod_wsgi/
# Activate the virtual env (we assume that virtualenv is in the env folder)
activate_this = '/home/thyagofas/web_dev/pybossa/env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
# Import sys to add the path of PyBossa
import sys
sys.stdout=sys.stderr
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,'/home/thyagofas/web_dev/pybossa/app-libras/api_libras')
# Run the web-app
from api_libras import app as application
