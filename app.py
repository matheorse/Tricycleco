import pymysql.cursors

import os
from flask import Flask, request, render_template, redirect, url_for, abort, flash
from flask import session, g

app = Flask(__name__)
app.secret_key = 'une cle(token) : grain de sel(any random string)'
def get_db():

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


@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()



@app.route('/')
def show_accueil():
    return render_template('layout.html')


########COLLECTE#########

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
    mycursor = get_db().cursor()
    sql = ''' SELECT lieu_collecte AS lieu , id_centre_collecte as id
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
    return render_template('collecte/add_collecte.html', centreCollect=Centre_collecte, typeDechet=type_dechet, tournee=Tournee)

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
    id = request.args.get('id')
    mycursor = get_db().cursor()
    sql = '''SELECT id_collecte AS id, id_type_dechet AS type, quantite_dechet_collecte AS quantite, id_centre_collecte AS centre, id_tournee AS tournee
             FROM Collecte
             WHERE id_collecte=%s;'''
    tuple_param = (id,)
    mycursor.execute(sql, tuple_param)

    Collecte = mycursor.fetchone()
    print(Collecte)
    sql = '''SELECT id_centre_collecte AS id, lieu_collecte AS lieu
             FROM Centre_collecte'''
    mycursor.execute(sql)
    Centre_collecte = mycursor.fetchall()
    print(Centre_collecte)
    sql = '''SELECT id_type_dechet AS id, libelle_type_dechet AS libelle
             FROM type_dechet'''
    mycursor.execute(sql)
    type_dechet = mycursor.fetchall()
    sql = '''SELECT date_tournee AS date , id_tournee as id
             FROM Tournee'''
    mycursor.execute(sql)
    Tournee = mycursor.fetchall()
    return render_template('collecte/edit_collecte.html', collecte=Collecte, centreCollect=Centre_collecte, typeDechet=type_dechet, tournee=Tournee)


@app.route('/collecte/add', methods=['POST'])
def valid_add_collecte():
    print('''ajout de la collecte dans le tableau''')
    quantite = request.form.get('quantite')
    type = request.form.get('type')
    centre = request.form.get('centre')
    tournee = request.form.get('tournee')
    message = 'quantite :' + quantite + ' - type :' + type + ' - centre de collecte :' + centre + ' - tournee : ' + tournee
    print(message)
    mycursor = get_db().cursor()
    tuple_param=(quantite,type, centre, tournee)
    sql="INSERT INTO Collecte( quantite_dechet_collecte, id_type_dechet, id_centre_collecte, id_tournee) VALUES ( %s, %s, %s, %s);"
    mycursor.execute(sql, tuple_param)
    get_db().commit()
    return redirect('/collecte/show')

@app.route('/collecte/edit', methods=['POST'])
def valid_edit_collecte():
    print('''modification de la collecte dans le tableau''')
    id = request.form.get('id')
    quantite = request.form.get('quantite')
    type = request.form.get('type')
    centre = request.form.get('centre')
    tournee = request.form.get('tournee')
    message = 'quantite :' + quantite + ' - type : ' + type + ' - centre de collecte : ' + centre + ' - tournee : ' + tournee + id
    print(message)
    mycursor = get_db().cursor()
    tuple_param=(quantite,type,centre,tournee,id)
    sql="UPDATE Collecte SET quantite_dechet_collecte = %s, id_type_dechet= %s, id_centre_collecte= %s, id_tournee= %s WHERE id_collecte=%s;"
    mycursor.execute(sql,tuple_param)
    get_db().commit()
    return redirect('/collecte/show')


########TOURNEE########

@app.route('/Tournee/show')
def show_Tournee():
    mycursor = get_db().cursor()
    sql = '''
        SELECT t.id_tournee, t.date_tournee, t.id_centre_recyclage, c.lieu_recyclage, t.id_camion, t.temps, camion.immatriculation_camion
        FROM Tournee t
        INNER JOIN Centre_recyclage c ON t.id_centre_recyclage = c.id_centre_recyclage
        INNER JOIN Camion camion ON t.id_camion = camion.id_camion
        ORDER BY t.id_tournee;
    '''
    mycursor.execute(sql)
    Tournee = mycursor.fetchall()

    return render_template('Tournee/show_Tournee.html', Tournee=Tournee)




@app.route('/Tournee/add', methods=['GET'])
def add_Tournee():
    print('''affichage du formulaire pour saisir une Tournee''')
    mycursor = get_db().cursor()
    sql = '''Select * From Camion;'''
    mycursor.execute(sql)
    camions=mycursor.fetchall()
    sql2 = '''Select * From Centre_recyclage;'''
    mycursor.execute(sql2)
    recyclages = mycursor.fetchall()
    get_db().commit()

    return render_template('Tournee/add_Tournee.html',camions=camions, recyclages=recyclages)


@app.route('/Tournee/delete')
def delete_Tournee():
    print('''Suppression d'une Tournée''')
    id_tournee = request.args.get('id')

    if id_tournee:
        try:
            id_tournee = int(id_tournee)
            mycursor = get_db().cursor()
            tuple_param = (id_tournee,)
            sql = "DELETE FROM Tournee WHERE id_tournee=%s;"
            mycursor.execute(sql, tuple_param)
            get_db().commit()

            message = f'info: suppression d\'une tournee avec - id_tournee =  {id_tournee}'
            flash(message, 'alert-warning')
        except ValueError:
            print("L'ID de la tournée n'est pas un entier valide.")

    return redirect('/Tournee/show')


@app.route('/Tournee/edit', methods=['GET'])
def edit_Tournee():
    print('''affichage du formulaire pour modifier une Tournee''')
    print(request.args)
    print(request.args.get('id'))
    tournee_id = request.args.get('id')
    mycursor = get_db().cursor()
    sql = '''SELECT id_tournee, date_tournee, id_centre_recyclage, id_camion, temps
             FROM Tournee
             WHERE id_tournee=%s;'''
    tuple_param = (tournee_id,)
    mycursor.execute(sql, tuple_param)
    Tournee = mycursor.fetchone()

    sql_camions = '''Select * From Camion;'''
    mycursor.execute(sql_camions)
    camions = mycursor.fetchall()

    sql_recyclages = '''Select * From Centre_recyclage;'''
    mycursor.execute(sql_recyclages)
    recyclages = mycursor.fetchall()

    get_db().commit()

    return render_template('Tournee/edit_Tournee.html', tournee=Tournee, camions=camions, recyclages=recyclages)


@app.route('/Tournee/add', methods=['POST'])
def valid_add_Tournee():
    print('''Ajout de la tournée dans la table''')
    date_tournee = request.form.get('date_tournee')
    id_centre_recyclage = request.form.get('id_centre_recyclage')
    id_camion = request.form.get('id_camion')
    temps = request.form.get('temps')

    message = (
        f'info: Tournée ajoutée -  date: {date_tournee}, '
        f'id_Centre_recyclage : {id_centre_recyclage}, id_Camion : {id_camion}, '
        f'Temps : {temps}'
    )



    mycursor = get_db().cursor()
    tuple_param = ( date_tournee, id_centre_recyclage, id_camion, temps)
    sql = "INSERT INTO Tournee( date_tournee, id_centre_recyclage, id_camion, temps) VALUES ( %s, %s, %s, %s);"
    mycursor.execute(sql, tuple_param)
    get_db().commit()

    flash(message, 'alert-success')
    return redirect('/Tournee/show')


@app.route('/Tournee/edit', methods=['POST'])
def valid_edit_Tournee():
    print('''Modification de la Tournée dans le tableau''')
    id_tournee = request.form.get('id_tournee')
    date_tournee = request.form.get('date_tournee')
    id_centre_recyclage = request.form.get('id_centre_recyclage')
    id_camion = request.form.get('id_camion')
    temps = request.form.get('temps')

    message = (
        f'info: Tournée modifiée - id_tournee : {id_tournee}, date : {date_tournee}, '
        f'id_Centre_recyclage : {id_centre_recyclage}, id_Camion : {id_camion}, '
        f'Temps : {temps}'
    )
    flash(message, 'alert-success')

    mycursor = get_db().cursor()
    tuple_param = (id_tournee, date_tournee, id_centre_recyclage, id_camion, temps, id_tournee)
    sql_update = '''UPDATE Tournee
                    SET date_tournee = %s, id_centre_recyclage = %s, id_camion = %s, temps = %s
                    WHERE id_tournee = %s;'''
    tuple_params = (date_tournee, id_centre_recyclage, id_camion, temps, id_tournee)

    mycursor.execute(sql_update, tuple_params)
    get_db().commit()

    return redirect('/Tournee/show')

@app.route('/employe/show')
def show_employe():
    mycursor = get_db().cursor()
    sql = '''SELECT id_employe, numero_telephone_employe, nom_employe, prenom_employe, salaire_employe, adresse_employe,id_camion
    FROM Employe'''
    mycursor.execute(sql)
    employe= mycursor.fetchall()
    return render_template('employe/show_employe.html', employe=employe)

@app.route('/employe/add', methods=['GET'])
def add_employe():
    print('''affichage du formulaire pour ajouter un employe''')
    return render_template('employe/add_employe.html')


@app.route('/employe/add', methods=['POST'])
def valid_add_employe():
    numero_telephone_employe=request.form.get('numero_telephone_employe','')
    nom_employe = request.form.get('nom_employe', '')
    prenom_employe = request.form.get('prenom_employe', '')
    salaire_employe= request.form.get('salaire_employe', '')
    adresse_employe = request.form.get('adresse_employe', '')
    id_camion = request.form.get('id_camion', '')
    message = u'employe ajouté , nom: '+nom_employe + ' - prénom : ' + prenom_employe + ' - salaire_employe: ' + salaire_employe + ' - adresse_employe: '+ adresse_employe + ' - id_camion: ' + id_camion
    print(message)
    flash(message, 'alert-success')
    mycursor = get_db().cursor()
    tuple_param = (numero_telephone_employe, 'nom_employe', 'prenom_employe', 'salaire_employe', 'adresse_employe','id_camion')
    sql = "INSERT INTO Employe ( id_employe, `numero_telephone_employe`, 'nom_employe', 'prenom_employe', 'salaire_employe', 'adresse_employe','id_camion') VALUES (%s, %s, %s, %s, %s);"
    mycursor.execute(sql, tuple_param)
    get_db().commit()
    return redirect('/employe/show')


@app.route('/employe/delete', methods=['GET'])
def delete_employe():
    print(''' suppression d'un employe''')
    id_employe = request.args.get('id_employe', None)
    print(id_employe)
    mycursor=get_db().cursor()
    tuple_param = (id_employe,)
    sql="DELETE FROM Employe WHERE id_employe=%s;"
    mycursor.execute(sql,tuple_param)
    get_db().commit()
    message  = f'info: suppression d\'un employe avec - id_employe =  {id_employe}'
    print(message)
    flash(message, 'alert-warning')
    return redirect('/employe/show')


@app.route('/employe/edit', methods=['GET'])
def edit_employe():
    id_employe = request.args.get('id_employe', '')
    id_employe = int(id_employe)
    id_employe = id_employe[id-1]
    print('''affichage du formulaire pour modifier un employe''')
    print(request.args)
    print(request.args.get('id'))
    tournee_id = request.args.get('id')
    mycursor = get_db().cursor()
    sql = '''SELECT id_employe, `numero_telephone_employe`, 'nom_employe', 'prenom_employe', 'salaire_employe', 'adresse_employe','id_camion'
                FROM Employe
                WHERE id_employe=%s;'''
    tuple_param = (tournee_id,)
    mycursor.execute(sql, tuple_param)
    employe= mycursor.fetchone()
    return render_template('employe/edit_employe.html', employe=employe)

@app.route('/employe/edit', methods=['POST'])
def valid_edit_employe():
    id_employe = request.args.get('id_employe', '')
    numero_telephone_employe = request.args.get('numero_telephone_employe', '')
    nom_employe = request.form.get('nom_employe', '')
    prenom_employe = request.form.get('prenom_employe', '')
    salaire_employe= request.form.get('salaire_employe', '')
    adresse_employe = request.form.get('adresse_employe', '')
    id_camion = request.form.get('id_camion', '')
    message = u'employe ajouté , numero_telephone: ' + numero_telephone_employe + 'nom: ' + nom_employe + ' - prénom : ' + prenom_employe + ' - salaire_employe: ' + salaire_employe + ' - salaire_employe: ' + salaire_employe + ' - id_camion: ' + id_camion
    print(message)
    flash(message, 'alert-success')
    mycursor = get_db().cursor()
    tuple_param = (id_employe, numero_telephone_employe, 'nom_employe', 'prenom_employe', 'salaire_employe', 'adresse_employe','id_camion')
    sql = "UPDATE Employe SET id_employe = %s, numero_telephone_employe = %s, nom_employe= %s, prenom_employe = %s, salaire_employe = %s ,adresse_employe=%s,id_camion=%s WHERE id_employe = %s;"
    mycursor.execute(sql, tuple_param)
    get_db().commit()
    return redirect('/employe/show')


# - - - - - - - C O N T E N E U R - - - - - - -
@app.route('/conteneur/show')
def show_conteneur():
    mycursor = get_db().cursor()
    sql = '''
        SELECT
            c.id_conteneur AS id,
            cc.lieu_collecte AS collecte,
            cc.id_centre_collecte AS idc,
            td.libelle_type_dechet AS type,
            td.id_type_dechet AS idtd,
            cr.id_centre_recyclage AS idr,
            cr.lieu_recyclage AS recyclage
        FROM
            Conteneur c
            INNER JOIN Centre_recyclage cr ON c.id_centre_recyclage = cr.id_centre_recyclage
            INNER JOIN type_dechet td ON c.id_type_dechet = td.id_type_dechet
            INNER JOIN Centre_collecte cc ON c.id_centre_collecte = cc.id_centre_collecte
        ORDER BY c.id_conteneur;
    '''
    mycursor.execute(sql)
    conteneur = mycursor.fetchall()

    return render_template('conteneur/show_conteneur.html', conteneur=conteneur)

@app.route('/conteneur/delete')
def delete_conteneur():
    print('''Suppression d'un conteneur''')
    id_tournee = request.args.get('id')

    if id_tournee:
        try:
            id_tournee = int(id_tournee)
            mycursor = get_db().cursor()
            tuple_param = (id_tournee,)
            sql = "DELETE FROM Tournee WHERE id_tournee=%s;"
            mycursor.execute(sql, tuple_param)
            get_db().commit()

            message = f'info: suppression d\'un conteneur avec - id_conteneur =  {id_conteneur}'
            flash(message, 'alert-warning')
        except ValueError:
            print("L'ID du conteneur n'est pas un entier valide.")

    return redirect('/conteneur/show')

@app.route('/conteneur/add', methods=['GET'])
def add_conteneur():
    print('''affichage du formulaire pour saisir un conteneur''')
    mycursor = get_db().cursor()
    sql = '''SELECT * FROM Centre_recyclage;'''
    mycursor.execute(sql)
    recyclages = mycursor.fetchall()
    sql2 = '''SELECT * FROM type_dechet;'''
    mycursor.execute(sql2)
    types_dechet = mycursor.fetchall()
    sql3 = '''SELECT * FROM Centre_collecte;'''
    mycursor.execute(sql3)
    centres_collecte = mycursor.fetchall()
    get_db().commit()

    return render_template('conteneur/add_conteneur.html', recyclages=recyclages, types_dechet=types_dechet, centres_collecte=centres_collecte)

@app.route('/conteneur/add', methods=['POST'])
def valid_add_conteneur():
    print('''Ajout du conteneur dans la table''')
    id_centre_collecte = request.form.get('id_centre_collecte')
    id_type_dechet = request.form.get('id_type_dechet')
    id_centre_recyclage = request.form.get('id_centre_recyclage')

    message = (
        f'info: Conteneur ajouté - id_centre_collecte : {id_centre_collecte}, '
        f'id_type_dechet : {id_type_dechet}, id_centre_recyclage : {id_centre_recyclage}'
    )

    mycursor = get_db().cursor()
    tuple_param = (id_centre_collecte, id_type_dechet, id_centre_recyclage)
    sql = "INSERT INTO Conteneur(id_centre_collecte, id_type_dechet, id_centre_recyclage) VALUES (%s, %s, %s);"
    mycursor.execute(sql, tuple_param)
    get_db().commit()

    flash(message, 'alert-success')
    return redirect('/conteneur/show')


@app.route('/conteneur/edit', methods=['GET'])
def edit_conteneur():
    print('''affichage du formulaire pour modifier un conteneur''')
    print(request.args)
    print(request.args.get('id'))
    tournee_id = request.args.get('id')
    mycursor = get_db().cursor()
    sql = '''SELECT id_tournee, date_tournee, id_centre_recyclage, id_camion, temps
             FROM Tournee
             WHERE id_tournee=%s;'''
    tuple_param = (tournee_id,)
    mycursor.execute(sql, tuple_param)
    conteneur = mycursor.fetchone()

    sql_camions = '''Select * From Camion;'''
    mycursor.execute(sql_camions)
    camions = mycursor.fetchall()

    sql_recyclages = '''Select * From Centre_recyclage;'''
    mycursor.execute(sql_recyclages)
    recyclages = mycursor.fetchall()

    get_db().commit()

    return render_template('conteneur/edit_conteneur.html', conteneur=conteneur, camions=camions, recyclages=recyclages)

@app.route('/conteneur/edit', methods=['POST'])
def valid_edit_conteneur():
    print('''Modification du conteneur dans le tableau''')
    id_tournee = request.form.get('id_tournee')
    date_tournee = request.form.get('date_tournee')
    id_centre_recyclage = request.form.get('id_centre_recyclage')
    id_camion = request.form.get('id_camion')
    temps = request.form.get('temps')

    message = (
        f'info: Conteneur modifié - id_tournee : {id_tournee}, date : {date_tournee}, '
        f'id_Centre_recyclage : {id_centre_recyclage}, id_Camion : {id_camion}, '
        f'Temps : {temps}'
    )
    flash(message, 'alert-success')

    mycursor = get_db().cursor()
    tuple_param = (id_tournee, date_tournee, id_centre_recyclage, id_camion, temps, id_tournee)
    sql_update = '''UPDATE Tournee
                    SET date_tournee = %s, id_centre_recyclage = %s, id_camion = %s, temps = %s
                    WHERE id_tournee = %s;'''
    tuple_params = (date_tournee, id_centre_recyclage, id_camion, temps, id_tournee)

    mycursor.execute(sql_update, tuple_params)
    get_db().commit()

    return redirect('/conteneur/show')


if __name__ == '__main__':
    app.run()