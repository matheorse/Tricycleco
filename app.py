import pymysql.cursors
import dotenv
import os
from flask import Flask, request, render_template, redirect, url_for, abort, flash
from flask import session, g

app = Flask(__name__)
app.secret_key = 'une cle(token) : grain de sel(any random string)'
def get_db():
    dotenv.load_dotenv()
    if 'db' not in g:
        g.db = pymysql.connect(
            host="localhost",
            user='mrose',
            password='mdp',
            database='BDD_mrose',
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db

@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

app = Flask(__name__)

@app.route('/')
def show_accueil():
    return render_template('layout.html')

@app.route('/collecte/show')
def show_collecte():
    mycursor = get_db().cursor()
    sql=''' SELECT id_collecte AS id, id_type_dechet AS type, quantite_dechet_collecte AS quantite, id_centre_collecte AS centre, id_tournee AS tournee
    FROM Collecte'''
    mycursor.execute(sql)
    Collecte = mycursor.fetchall()
    sql=''' SELECT lieu_collecte AS lieu , id_centre_collecte as id
    FROM Centre_collecte'''
    mycursor.execute(sql)
    Centre_collecte = mycursor.fetchall()
    sql = ''' SELECT libelle_type_dechet AS libelle , id_type_dechet as id
        FROM type_dechet'''
    mycursor.execute(sql)
    type_dechet = mycursor.fetchall()
    sql = ''' SELECT date_tournee AS date , id_tournee as id
            FROM Tournee'''
    mycursor.execute(sql)
    Tournee = mycursor.fetchall()
    return render_template('collecte/show_collecte.html', collecte=Collecte , centreCollect=Centre_collecte, typeDechet=type_dechet, tournee= Tournee)


@app.route('/collecte/add', methods=['GET'])
def add_collecte():
    print('''affichage du formulaire pour saisir une collecte''')
    return render_template('collecte/add_collecte.html')

@app.route('/collecte/delete')
def delete_collecte():
    print('''suppression d'une collecte''')
    id=request.args.get('id', None)
    print(id)
    mycursor = get_db().cursor()
    tuple_param=(id)
    sql="DELETE FROM collecte WHERE id_collecte=%s;"
    mycursor.execute(sql,tuple_param)

    get_db().commit()
    print(request.args)
    print(request.args.get('id'))
    id=request.args.get('id',0)
    return redirect('/collecte/show')

@app.route('/collecte/edit', methods=['GET'])
def edit_collecte():
    print('''affichage du formulaire pour modifier une collecte''')
    print(request.args)
    print(request.args.get('id'))
    id=request.args.get('id')
    mycursor = get_db().cursor()
    sql=''' SELECT id_collecte AS id, id_type_dechet AS type, quantite_dechet_collecte AS quantite, id_centre_collecte AS centre, id_tournee
    FROM Collecte
    WHERE id_collecte=%s;'''
    tuple_param=(id)
    mycursor.execute(sql,tuple_param)
    Collecte = mycursor.fetchone()
    return render_template('collecte/edit_collecte.html', collecte=Collecte)


@app.route('/collecte/add', methods=['POST'])
def valid_add_collecte():
    print('''ajout de la collecte dans le tableau''')
    quantite = request.form.get('quantite')
    type = request.form.get('type')
    centre = request.form.get('centre_collecte')
    tournee = request.form.get('tournee')
    message = 'quantite :' + quantite + ' - type :' + type + ' - centre de collecte :' + centre + ' - tournee : ' + tournee
    print(message)
    mycursor = get_db().cursor()
    tuple_param=(quantite,type)
    sql="INSERT INTO Collecte(id_collecte, quantite_dechet_collecte, id_type_dechet, id_centre_collecte, id_tournee) VALUES (NULL, %s, %s);"
    mycursor.execute(sql,tuple_param)
    get_db().commit()
    return redirect('/collecte/show')

@app.route('/collecte/edit', methods=['POST'])
def valid_edit_collecte():
    print('''modification de la collecte dans le tableau''')
    id = request.form.get('id')
    quantite = request.form.get('quantite')
    type = request.form.get('type')
    centre = request.form.get('centre_collecte')
    tournee = request.form.get('tournee')
    message = 'quantite :' + quantite + ' - type :' + type + ' - centre de collecte :' + centre + ' - tournee : ' + tournee + ' pour la collecte d identifiant :' + id
    print(message)
    mycursor = get_db().cursor()
    tuple_param=(quantite,type,id)
    sql="UPDATE Collecte SET quantite_dechet_collecte = %s, id_type_dechet= %s, id_centre_collecte= %s, id_tournee= %s WHERE id_collecte=%s;"
    mycursor.execute(sql,tuple_param)
    get_db().commit()
    return redirect('/collecte/show')


if __name__ == '__main__':
    app.run()