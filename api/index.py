import os
import sys

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import create_app

flask_app = create_app()

class VercelWSGIMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')
        # Handle Vercel rewrite paths to prevent 404 errors
        if path in ('/api/index', '/api/index.py', '/api/index/'):
            environ['PATH_INFO'] = '/'
        elif path.startswith('/api/index/'):
            environ['PATH_INFO'] = path[10:]
        elif path.startswith('/api/index.py/'):
            environ['PATH_INFO'] = path[13:]
            
        return self.app(environ, start_response)

app = VercelWSGIMiddleware(flask_app)
