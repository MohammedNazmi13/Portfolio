import os
import sys
from urllib.parse import parse_qs

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import create_app

flask_app = create_app()

class VercelWSGIMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        query_string = environ.get('QUERY_STRING', '')
        parsed_query = parse_qs(query_string)
        
        # Check if Vercel passed __path__ parameter in query from vercel.json rewrite
        if '__path__' in parsed_query and parsed_query['__path__']:
            path = parsed_query['__path__'][0]
            if not path.startswith('/'):
                path = '/' + path
            environ['PATH_INFO'] = path
        else:
            path_info = environ.get('PATH_INFO', '')
            raw_path = (
                environ.get('HTTP_X_MATCHED_PATH') or 
                environ.get('RAW_URI') or 
                environ.get('REQUEST_URI') or 
                environ.get('HTTP_X_FORWARDED_URI') or 
                path_info
            )
            if raw_path and '?' in raw_path:
                raw_path = raw_path.split('?')[0]
                
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
