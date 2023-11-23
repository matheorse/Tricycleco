import pymysql.cursors
from flask import Flask, request, render_template, redirect, url_for, abort, flash
from flask import session, g

app = Flask(__name__)
app.secret_key = 'une cle(token) : grain de sel(any random string)'
def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host="localhost",
            user="",
            password="",
            database="",
            charset="",
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db

@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_accueil():
    return render_template('layout.html')

if __name__ == '__main__':
    app.run()