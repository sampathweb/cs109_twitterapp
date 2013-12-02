import sys
import os

sys.path.insert(0, '/home/sampathweb/anaconda/envs/conda27/bin/')

from app import create_app

env = os.environ.get('APPNAME_ENV', 'prod')
app = create_app('app.settings.%sConfig' % env.capitalize(), env)

class WebFactionMiddleware(object):
    def __init__(self, app):
        self.app = app
    def __call__(self, environ, start_response):
        environ['SCRIPT_NAME'] = '/'
        return self.app(environ, start_response)

app.wsgi_app = WebFactionMiddleware(app.wsgi_app)

application = app
