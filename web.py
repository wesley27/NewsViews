'''
Created on Jan 28, 2017

@author: W. Wesley Weidenhamer II
'''

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/entry', methods = ['POST'])
def entry():
    country1 = request.form['Country 1']
    country2 = request.form['Country 2']
    search = request.form['search']
    print("Country 1 is '" + country1 + "'.")
    print("Country 2 is '" + country2 + "'.")
    print("Search text is '" + search + "'.")
    return redirect('/', code=302, Response=None)

if __name__ == '__main__':
    app.run()