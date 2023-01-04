import sys
import os
import sys

WEB_DIR = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir), "web")
sys.path.append(WEB_DIR)
sys.path.insert(0, "/var/www/html/app/web")
from web.app import app as application
