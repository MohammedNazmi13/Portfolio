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
        path_info = environ.get('PATH_INFO', '')
        
        # Check if Vercel set matched/forwarded URI in headers or env
        raw_path = (
            environ.get('HTTP_X_MATCHED_PATH') or 
            environ.get('RAW_URI') or 
            environ.get('REQUEST_URI') or 
            environ.get('HTTP_X_FORWARDED_URI') or 
            path_info
        )
        
        # Strip query parameters if present
        if raw_path and '?' in raw_path:
            raw_path = raw_path.split('?')[0]
            
        # Clean up Vercel internal function prefixes if present
        if raw_path:
            if raw_path.startswith('/api/index.py/'):
                raw_path = raw_path[13:]
            elif raw_path == '/api/index.py':
                raw_path = '/'
            elif raw_path.startswith('/api/index/'):
                raw_path = raw_path[10:]
            elif raw_path in ('/api/index', '/api/index/'):
                raw_path = '/'
                
            environ['PATH_INFO'] = raw_path if raw_path.startswith('/') else '/' + raw_path
            
        return self.app(environ, start_response)

app = VercelWSGIMiddleware(flask_app)
