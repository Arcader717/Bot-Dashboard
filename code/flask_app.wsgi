from flask import Flask
import sys

path = '/home/yourusername/mysite'
if path not in sys.path:
   sys.path.insert(0, path)

from flask_app import app as application