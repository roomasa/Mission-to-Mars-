from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraping

# Let's break down what this code is doing.
#The first line says that we'll use Flask to render a template.
#The second line says we'll use PyMongo to interact with our Mongo database.
#Finally, the last line says that to use the scraping code, we will convert from Jupyter notebook to Python.
#Under these lines, let's add the following to set up Flask:
app = Flask(__name__)