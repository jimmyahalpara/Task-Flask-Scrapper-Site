import sys
import logging
 
sys.path.insert(0, '/var/www/scraper/main')
sys.path.insert(0, '/var/www/scraper/main/lib/python3.8/site-packages/')
 
# Set up logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
 
# Import and run the Flask app
from app import application

