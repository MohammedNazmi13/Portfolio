import os
import sys

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import create_app
app = create_app()
