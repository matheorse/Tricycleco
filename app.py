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


# - - - - - - C O L L E C T E  - - - - - -

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
    id_collecte = request.args.get('id')

    if id_collecte:
        try:
            id_collecte = int(id_collecte)
            mycursor = get_db().cursor()
            sql = "SELECT * FROM Collecte WHERE id_collecte=%s;"
            mycursor.execute(sql, (id_collecte,))
            collecte = mycursor.fetchone()

            if not collecte:
                abort(404)

            return render_template('collecte/delete_collecte.html', collecte=collecte)

        except ValueError:
            print("L'ID de la collecte n'est pas un entier valide.")

    return redirect('/collecte/show')


@app.route('/collecte/confirm_delete/<int:id>', methods=['POST'])
def confirm_delete_collecte(id):
    mycursor = get_db().cursor()

    if request.method == 'POST':
        try:
            tuple_param = (id,)
            sql = "DELETE FROM Collecte WHERE id_collecte=%s;"
            mycursor.execute(sql, tuple_param)
            get_db().commit()

            message = f'Suppression de la collecte avec ID {id} réussie.'
            flash(message, 'alert-warning')
        except Exception as e:
            print(f"Erreur lors de la suppression de la collecte : {str(e)}")

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
    type_id = request.form.get('type')
    centre_id = request.form.get('centre')
    tournee_id = request.form.get('tournee')

    mycursor = get_db().cursor()

    centre_name = get_name_by_id(mycursor, 'Centre_collecte', 'lieu_collecte', centre_id)
    type_name = get_name_by_id(mycursor, 'type_dechet', 'libelle_type_dechet', type_id)
    tournee_date = get_name_by_id(mycursor, 'Tournee', 'date_tournee', tournee_id)
    tournee_date_str = str(tournee_date)

    message = u'quantite :' + quantite + ' - type : ' + type_name + ' - centre de collecte : ' + centre_name + ' - tournee : ' + tournee_date_str
    print(message)
    flash(message, 'alert-success')

    tuple_param = (quantite, type_id, centre_id, tournee_id)
    sql = "INSERT INTO Collecte( quantite_dechet_collecte, id_type_dechet, id_centre_collecte, id_tournee) VALUES ( %s, %s, %s, %s);"
    mycursor.execute(sql, tuple_param)
    get_db().commit()

    return redirect('/collecte/show')

def get_name_by_id(mycursor, table, field, id):
    sql = f"SELECT {field} FROM {table} WHERE id_{table}=%s;"
    mycursor.execute(sql, (id,))
    result = mycursor.fetchone()
    return result[field] if result else ''

@app.route('/collecte/edit', methods=['POST'])
def valid_edit_collecte():
    print('''modification de la collecte dans le tableau''')
    id = request.form.get('id')
    quantite = request.form.get('quantite')
    type_id = request.form.get('type')
    centre_id = request.form.get('centre')
    tournee_id = request.form.get('tournee')

    mycursor = get_db().cursor()

    centre_name = get_name_by_id(mycursor, 'Centre_collecte', 'lieu_collecte', centre_id)
    type_name = get_name_by_id(mycursor, 'type_dechet', 'libelle_type_dechet', type_id)
    tournee_date = get_name_by_id(mycursor, 'Tournee', 'date_tournee', tournee_id)
    tournee_date_str = str(tournee_date)

    message = u'quantite :' + quantite + ' - type : ' + type_name + ' - centre de collecte : ' + centre_name + ' - tournee : ' + tournee_date_str + ' - id : ' +str(id)
    print(message)
    flash(message, 'alert-success')

    tuple_param = (quantite, type_id, centre_id, tournee_id, id)
    sql = "UPDATE Collecte SET quantite_dechet_collecte = %s, id_type_dechet= %s, id_centre_collecte= %s, id_tournee= %s WHERE id_collecte=%s;"
    mycursor.execute(sql, tuple_param)
    get_db().commit()

    return redirect('/collecte/show')

def get_name_by_id(mycursor, table, field, id):
    sql = f"SELECT {field} FROM {table} WHERE id_{table}=%s;"
    mycursor.execute(sql, (id,))
    result = mycursor.fetchone()
    return result[field] if result else ''

@app.route('/collecte/etat', methods=['GET', 'POST'])
def etat_collecte():
    mycursor = get_db().cursor()

    if request.method == 'POST':
        min_quantite = request.form.get('min_quantite')
        max_quantite = request.form.get('max_quantite')
        min_quantite = min_quantite or 0

        # Requête SQL pour les types de déchets
        sql_types_dechets = f"""SELECT type_dechet.libelle_type_dechet as type,
                                         SUM(Collecte.quantite_dechet_collecte) AS quantite_total_type
                                     FROM Collecte
                                     JOIN type_dechet ON Collecte.id_type_dechet = type_dechet.id_type_dechet
                                     WHERE Collecte.quantite_dechet_collecte BETWEEN %s AND %s
                                     GROUP BY type_dechet.libelle_type_dechet
                                     ORDER BY quantite_total_type DESC;
                                 """

        # Requête SQL pour les centres de collecte
        sql_centres_collecte = f"""SELECT Centre_collecte.lieu_collecte as lieu,
                                           SUM(Collecte.quantite_dechet_collecte) AS quantite_total_centre
                                       FROM Collecte
                                       JOIN Centre_collecte ON Collecte.id_centre_collecte = Centre_collecte.id_centre_collecte
                                       WHERE Collecte.quantite_dechet_collecte BETWEEN %s AND %s
                                       GROUP BY Centre_collecte.lieu_collecte
                                       ORDER BY quantite_total_centre DESC;
                                   """

        tuple_param = (min_quantite, max_quantite)
        mycursor.execute(sql_types_dechets, tuple_param)
        quantite_total_type = mycursor.fetchall()

        tuple_param = (min_quantite, max_quantite)
        mycursor.execute(sql_centres_collecte, tuple_param)
        quantite_total_centre = mycursor.fetchall()
    else:
        # Requête SQL sans filtre
        sql_types_dechets = """SELECT type_dechet.libelle_type_dechet as type,
                                     SUM(Collecte.quantite_dechet_collecte) AS quantite_total_type
                                 FROM Collecte
                                 JOIN type_dechet ON Collecte.id_type_dechet = type_dechet.id_type_dechet
                                 GROUP BY type_dechet.libelle_type_dechet
                                 ORDER BY quantite_total_type DESC;
                             """

        sql_centres_collecte = """SELECT Centre_collecte.lieu_collecte as lieu,
                                       SUM(Collecte.quantite_dechet_collecte) AS quantite_total_centre
                                   FROM Collecte
                                   JOIN Centre_collecte ON Collecte.id_centre_collecte = Centre_collecte.id_centre_collecte
                                   GROUP BY Centre_collecte.lieu_collecte
                                   ORDER BY quantite_total_centre DESC;
                               """

        mycursor.execute(sql_types_dechets)
        quantite_total_type = mycursor.fetchall()

        mycursor.execute(sql_centres_collecte)
        quantite_total_centre = mycursor.fetchall()

    return render_template('/collecte/etat_collecte.html', quantiteTotType=quantite_total_type, quantiteTotCentre=quantite_total_centre)


@app.route('/reset')
def reset():
    cursor = get_db().cursor()
    script = open("tricycleco.sql", "r")
    requete = script.read().split(';')
    script.close()

    for query in requete:
        query = query.strip()  # Supprime les espaces et les sauts de ligne au début et à la fin
        if query:
            cursor.execute(query)
            get_db().commit()

    flash('Le SQL a été bien réinitialisé', 'alert-success')
    return redirect('/')


# - - - - - - - T O U R N E E - - - - -  -

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
    id_tournee = request.args.get('id')

    if id_tournee:
        return render_template('Tournee/delete_Tournee.html', id_tournee=id_tournee)
    else:
        # Gérer le cas où aucun ID n'est fourni
        flash("Aucun ID de tournée fourni pour la suppression.", 'alert-danger')
        return redirect('/Tournee/show')


@app.route('/Tournee/delete/confirmed', methods=['POST'])
def confirm_delete_Tournee():
    id_tournee = request.form.get('id')

    if id_tournee:
        try:
            id_tournee = int(id_tournee)
            mycursor = get_db().cursor()
            tuple_param = (id_tournee,)
            sql = "DELETE FROM Tournee WHERE id_tournee=%s;"
            mycursor.execute(sql, tuple_param)
            get_db().commit()

            if mycursor.rowcount > 0:
                flash(f'Suppression de la tournée avec l\'ID {id_tournee} confirmée.', 'alert-success')
            else:
                flash(f'Erreur: La tournée avec l\'ID {id_tournee} n\'a pas été trouvée ou ne peut pas être supprimée.',
                      'alert-danger')

        except ValueError:
            flash("L'ID de la tournée n'est pas un entier valide.", 'alert-danger')

        except pymysql.err.IntegrityError as e:
            flash(" Delete Controle : Impossible de supprimer cette tournée car elle est liée à d'autres données.", 'alert-danger')

        except Exception as e:
            flash(f'Une erreur est survenue : {str(e)}', 'alert-danger')

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
@app.route('/Tournee/etat', methods=['GET', 'POST'])
def etat_Tournee():
    selected_locations = []

    if request.method == 'POST':
        selected_locations = request.form.getlist('rue')

        if not selected_locations:
            return "Aucune rue sélectionnée."

    db = get_db()

    # Construction de la requête SQL seulement si selected_locations n'est pas vide
    if selected_locations:
        placeholders = ','.join(['%s'] * len(selected_locations))
        sql = '''
            SELECT t.id_tournee, t.date_tournee, t.id_centre_recyclage, c.lieu_recyclage, 
                   t.id_camion, t.temps, camion.immatriculation_camion
            FROM Tournee t
            INNER JOIN Centre_recyclage c ON t.id_centre_recyclage = c.id_centre_recyclage
            INNER JOIN Camion camion ON t.id_camion = camion.id_camion
            WHERE c.lieu_recyclage IN ({})
        '''.format(placeholders)

        mycursor = db.cursor()
        mycursor.execute(sql, selected_locations)
        filtered_tournees = mycursor.fetchall()

        return render_template('Tournee/Tournee_etat.html', filtered_data=filtered_tournees)

    return render_template('Tournee/Tournee_etat.html')

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


# - - - - - - -E M P L O Y E - - - - - -
@app.route('/employe/show')
def show_employe():
    mycursor = get_db().cursor()
    sql = '''SELECT id_employe  , numero_telephone_employe, nom_employe , prenom_employe, salaire_employe , adresse_employe ,id_camion 
    FROM Employe'''
    mycursor.execute(sql)
    employes= mycursor.fetchall()
    print(employes)
    return render_template('employe/show_employe.html', employes=employes)

@app.route('/employe/add', methods=['GET'])
def add_employe():
    print('''affichage du formulaire pour ajouter un employe''')
    mycursor = get_db().cursor()
    sql = '''Select * From Camion;'''
    mycursor.execute(sql)
    camions = mycursor.fetchall()
    get_db().commit()

    return render_template('employe/add_employe.html',camions=camions)

@app.route('/employe/add', methods=['POST'])
def valid_add_employe():
    numero_telephone_employe=request.form.get('numero_tel_employe','')
    nom_employe = request.form.get('nom_employe', '')
    prenom_employe = request.form.get('prenom_employe', '')
    salaire_employe= request.form.get('salaire_employe', '')
    adresse_employe = request.form.get('adresse_employe', '')
    id_camion = request.form.get('id_camion', '')
    message = u'employe ajouté , nom: '+nom_employe + ' - prénom : ' + prenom_employe + ' - salaire_employe: ' + salaire_employe + ' - adresse_employe: '+ adresse_employe + ' - id_camion: ' + id_camion + ' - numero telephone: ' + numero_telephone_employe
    mycursor = get_db().cursor()
    tuple_param = (numero_telephone_employe, nom_employe, prenom_employe, salaire_employe, adresse_employe,id_camion)
    print(numero_telephone_employe)
    sql = "INSERT INTO Employe ( numero_telephone_employe, nom_employe, prenom_employe, salaire_employe, adresse_employe,id_camion) VALUES ( %s, %s, %s, %s,%s,%s);"
    mycursor.execute(sql, tuple_param)
    get_db().commit()
    flash(message, 'alert-success')
    return redirect('/employe/show')

@app.route('/employe/delete', methods=['GET'])
def delete_employe():
    print(''' suppression d'un employe''')
    id_employe = request.args.get('id')
    if id_employe:
        try:
            id_employe= int(id_employe)
            mycursor = get_db().cursor()
            tuple_param = (id_employe)
            sql = "DELETE FROM Employe WHERE id_employe=%s;"
            mycursor.execute(sql, tuple_param)
            get_db().commit()

            message  = f'info: suppression d\'un employe avec - id_employe =  {id_employe}'
            flash(message, 'alert-warning')
        except ValueError:
         print("L'ID de l'employe n'est pas un entier valide.")
    return redirect('/employe/show')

@app.route('/employe/edit', methods=['GET'])
def edit_employe():
    print('''affichage du formulaire pour modifier un employe''')
    print(request.args)
    print(request.args.get('id'))
    id_employe= request.args.get('id')
    mycursor = get_db().cursor()
    sql = '''SELECT id_employe , numero_telephone_employe, nom_employe, prenom_employe, salaire_employe, adresse_employe, id_camion
                FROM Employe
                WHERE id_employe=%s;'''
    tuple_param = (id_employe,)
    mycursor.execute(sql, tuple_param)
    employe= mycursor.fetchone()

    sql_camions = '''Select * From Camion;'''
    mycursor.execute(sql_camions)
    camions = mycursor.fetchall()

    get_db().commit()
    return render_template('employe/edit_employe.html', employe=employe,camions=camions)

@app.route('/employe/edit', methods=['POST'])
def valid_edit_employe():
    id_employe = request.form.get('id')
    numero_telephone_employe = request.form.get('numero_telephone_employe', '')
    nom_employe = request.form.get('nom_employe', '')
    prenom_employe = request.form.get('prenom_employe', '')
    salaire_employe = request.form.get('salaire_employe', '')
    adresse_employe = request.form.get('adresse_employe', '')
    id_camion = request.form.get('id_camion', '')

    mycursor = get_db().cursor()
    tuple_param = (  numero_telephone_employe, nom_employe, prenom_employe, salaire_employe, adresse_employe, id_camion,id_employe)

    sql = "UPDATE Employe SET  numero_telephone_employe = %s, nom_employe = %s, prenom_employe = %s, salaire_employe = %s, adresse_employe = %s, id_camion = %s WHERE id_employe = %s;"

    message = u'employe modifie , nom: '+nom_employe + ' - prénom : ' + prenom_employe + ' - salaire_employe: ' + salaire_employe + ' - adresse_employe: '+ adresse_employe + ' - id_camion: ' + id_camion + ' - numero telephone: ' + numero_telephone_employe
    flash(message,'success')
    mycursor.execute(sql, tuple_param)
    get_db().commit()

    return redirect('/employe/show')

@app.route('/employe/etat', methods=['GET'])
def etat_employe():
    mycursor = get_db().cursor()

    sql = '''
        SELECT c.id_camion, COUNT(e.id_employe) AS nombre_employe
        FROM Camion c
        LEFT JOIN Employe e ON c.id_camion = e.id_camion
        GROUP BY c.id_camion;
    '''
    mycursor.execute(sql)
    nombre_employe = mycursor.fetchall()

    sql1="SELECT SUM(salaire_employe) AS montant_total_salaires FROM Employe;"
    mycursor.execute(sql1)
    montant_total_salaires=mycursor.fetchall()

    sql2 = "SELECT MAX(salaire_employe) AS salaire_max FROM Employe ;"
    mycursor.execute(sql2)
    salaire_max=mycursor.fetchall()


    sql_salaire = "SELECT AVG(salaire_employe) AS salaire_moyen FROM Employe"
    mycursor.execute(sql_salaire)
    salaire_moyen = mycursor.fetchall()

    return render_template('employe/etat_employe.html', nombre_employe=nombre_employe, montant_total_salaires=montant_total_salaires ,salaire_max=salaire_max,salaire_moyen=salaire_moyen)


# - - - - - - - C O N T E N E U R - - - - - - -
@app.route('/conteneur/show')
def show_conteneur():
    mycursor = get_db().cursor()
    sql = '''
        SELECT
            c.id_conteneur AS id,
            cc.lieu_collecte AS collecte,
            cc.id_centre_collecte AS idc,
            td.libelle_type_dechet AS type_item,
            td.id_type_dechet AS idtd,
            cr.id_centre_recyclage AS idr,
            cr.lieu_recyclage AS recyclage,
            c.volume_conteneur AS volume,
            c.reference_conteneur AS reference
        FROM
            Conteneur c
            INNER JOIN Centre_recyclage cr ON c.id_centre_recyclage = cr.id_centre_recyclage
            INNER JOIN type_dechet td ON c.id_type_dechet = td.id_type_dechet
            INNER JOIN Centre_collecte cc ON c.id_centre_collecte = cc.id_centre_collecte
        ORDER BY c.id_conteneur, c.volume_conteneur;
    '''
    mycursor.execute(sql)
    conteneur = mycursor.fetchall()

    # Ajoutez la requête pour récupérer les types de déchets
    sql_types_dechet = "SELECT id_type_dechet, libelle_type_dechet FROM type_dechet;"
    mycursor.execute(sql_types_dechet)
    types_dechet = mycursor.fetchall()

    return render_template('conteneur/show_conteneur.html', conteneur=conteneur, types_dechets=types_dechet)

@app.route('/conteneur/delete')
def delete_conteneur():
    print('''Suppression d'un conteneur''')
    id_conteneur = request.args.get('id')

    if id_conteneur is not None:
        try:
            id_conteneur = int(id_conteneur)
            mycursor = get_db().cursor()
            sql = "SELECT * FROM Conteneur WHERE id_conteneur=%s;"
            mycursor.execute(sql, (id_conteneur,))
            conteneur = mycursor.fetchone()

            if not conteneur:
                abort(404)

            return render_template('conteneur/delete_conteneur.html', conteneur=conteneur)

        except ValueError:
            print("L'ID du conteneur n'est pas un entier valide.")

    return redirect('/conteneur/show')

@app.route('/conteneur/confirm_delete/<int:id>', methods=['POST'])
def confirm_delete_conteneur(id):
    mycursor = get_db().cursor()

    if request.method == 'POST':
        try:
            tuple_param = (id,)
            sql = "DELETE FROM Conteneur WHERE id_conteneur=%s;"
            mycursor.execute(sql, tuple_param)
            get_db().commit()

            message = f'Suppression du conteneur avec ID {id} réussie.'
            flash(message, 'alert-warning')
        except Exception as e:
            print(f"Erreur lors de la suppression du conteneur : {str(e)}")

    return redirect('/conteneur/show')

@app.route('/conteneur/add', methods=['GET'])
def add_conteneur():
    print('''affichage du formulaire pour ajouter un conteneur''')
    mycursor = get_db().cursor()

    sql1 = '''SELECT * FROM Centre_recyclage;'''
    mycursor.execute(sql1)
    recyclages = mycursor.fetchall()

    sql2 = '''SELECT * FROM type_dechet;'''
    mycursor.execute(sql2)
    types_dechets = mycursor.fetchall()

    sql3 = '''SELECT * FROM Centre_collecte;'''
    mycursor.execute(sql3)
    collectes = mycursor.fetchall()

    sql4 = '''SELECT * FROM Conteneur;'''
    mycursor.execute(sql4)
    conteneurs = mycursor.fetchall()

    get_db().commit()

    return render_template('conteneur/add_conteneur.html', conteneurs=conteneurs, recyclages=recyclages,
                           types_dechets=types_dechets, collectes=collectes)

@app.route('/conteneur/add', methods=['POST'])
def valid_add_conteneur():
        print('''Ajout du conteneur dans la table''')
        id_centre_collecte = request.form.get('id_centre_collecte')
        id_type_dechet = request.form.get('id_type_dechet')
        id_centre_recyclage = request.form.get('id_centre_recyclage')
        volume_conteneur = request.form.get('volume_conteneur')
        reference_conteneur = request.form.get('reference_conteneur')

        message = (
            f'info: Conteneur ajouté - id_centre_collecte : {id_centre_collecte}, '
            f'id_type_dechet : {id_type_dechet}, id_centre_recyclage : {id_centre_recyclage}'
            f' volume_conteneur : {volume_conteneur}, reference_conteneur {reference_conteneur}'
        )

        mycursor = get_db().cursor()
        tuple_param = (id_centre_collecte, id_type_dechet, id_centre_recyclage, volume_conteneur, reference_conteneur)
        sql = "INSERT INTO Conteneur( id_centre_collecte, id_type_dechet, id_centre_recyclage, volume_conteneur, reference_conteneur) VALUES (%s, %s, %s, %s, %s);"
        mycursor.execute(sql, tuple_param)
        get_db().commit()

        flash(message, 'alert-success')
        return redirect('/conteneur/show', )

@app.route('/conteneur/edit', methods=['GET'])
def edit_conteneur():
    if request.method == 'GET':
        id_conteneur = request.args.get('id')
        id_conteneur = int(id_conteneur)  if id_conteneur is not None else None
        mycursor = get_db().cursor()

        sql = '''
            SELECT
                c.id_conteneur AS id_conteneur,
                cc.lieu_collecte AS collecte,
                cc.id_centre_collecte AS id_centre_collecte,
                td.libelle_type_dechet AS type_item,
                td.id_type_dechet AS id_type_dechet,
                cr.id_centre_recyclage AS id_centre_recyclage,
                cr.lieu_recyclage AS recyclage,
                c.volume_conteneur AS volume,
                c.reference_conteneur AS reference
                
            FROM
                Conteneur c
                INNER JOIN Centre_recyclage cr ON c.id_centre_recyclage = cr.id_centre_recyclage
                INNER JOIN type_dechet td ON c.id_type_dechet = td.id_type_dechet
                INNER JOIN Centre_collecte cc ON c.id_centre_collecte = cc.id_centre_collecte
            WHERE c.id_conteneur = %s;
        '''
        tuple_param = (id_conteneur,)
        mycursor.execute(sql, tuple_param)
        conteneur = mycursor.fetchone()

        sql_collecte = '''SELECT * FROM Centre_collecte;'''
        mycursor.execute(sql_collecte)
        collecte = mycursor.fetchall()

        sql_recyclages = '''SELECT * FROM Centre_recyclage;'''
        mycursor.execute(sql_recyclages)
        recyclages = mycursor.fetchall()

        sql_type_dechet = '''SELECT * FROM type_dechet;'''
        mycursor.execute(sql_type_dechet)
        types_dechet = mycursor.fetchall()

        get_db().commit()

        return render_template('conteneur/edit_conteneur.html', conteneur=conteneur, recyclages=recyclages,
                               types_dechets=types_dechet, collectes=collecte)

    elif request.method == 'POST':

        return redirect('/conteneur/show')

def get_name_by_id(mycursor, table, field, id):
    sql = f"SELECT {field} FROM {table} WHERE id_{table}=%s;"
    mycursor.execute(sql, (id,))
    result = mycursor.fetchone()
    return result[field] if result else ''

@app.route('/conteneur/edit', methods=['POST'])
def valid_edit_conteneur():
    print('''Modification du conteneur dans le tableau''')
    id_conteneur = int(request.form.get('id_conteneur'))
    id_type_dechet = int(request.form.get('id_type_dechet'))
    id_centre_recyclage = int(request.form.get('id_centre_recyclage'))
    id_centre_collecte = int(request.form.get('id_centre_collecte'))
    volume_conteneur = int(request.form.get('volume_conteneur'))
    reference_conteneur = request.form.get('reference_conteneur')



    message = f'Id conteneur : {id_conteneur} - centre de collecte :{id_centre_collecte } - Type de dechet : {id_type_dechet} - centre de recyclage : { id_centre_recyclage} - volume : {volume_conteneur} - reference : {reference_conteneur}'
    print(message)
    flash(message, 'alert-success')
    mycursor = get_db().cursor()

    tuple_params = ( id_type_dechet, id_centre_recyclage, id_centre_collecte, volume_conteneur, reference_conteneur, id_conteneur)
    sql_update = '''
            UPDATE Conteneur
            SET id_type_dechet = %s, id_centre_recyclage = %s, id_centre_collecte = %s, volume_conteneur = %s, reference_conteneur = %s
            WHERE id_conteneur = %s;
        '''
    mycursor.execute(sql_update, tuple_params)
    get_db().commit()

    return redirect('/conteneur/show')

@app.route('/conteneur/etat', methods=['GET', 'POST'])
def etat_conteneur():
    mycursor = get_db().cursor()

    if request.method == 'POST':
        min_volume_total = request.form.get('min_volume_total') or 0
        max_volume_total = request.form.get('max_volume_total') or float('inf')

        # Requête SQL pour les centres de collecte après le filtre
        sql_centres = """SELECT Centre_collecte.lieu_collecte AS lieu,
                                  SUM(Conteneur.volume_conteneur) AS volume_total
                           FROM Centre_collecte
                           LEFT JOIN Conteneur ON Centre_collecte.id_centre_collecte = Conteneur.id_centre_collecte
                           GROUP BY Centre_collecte.lieu_collecte
                           HAVING volume_total BETWEEN %s AND %s
                           ORDER BY lieu;
                       """

        tuple_param = (min_volume_total, max_volume_total)
        mycursor.execute(sql_centres, tuple_param)
        centres = mycursor.fetchall()

        # Message flash avec les informations de filtre
        flash(f"Paramétrage avec un volume total minimum : {min_volume_total} et un volume total maximum : {max_volume_total}", 'success')

        return render_template('/conteneur/etat_conteneur.html', centres=centres)

    # Requête SQL pour les centres de collecte avant le filtre
    sql_centres = """SELECT Centre_collecte.lieu_collecte AS lieu,
                            SUM(Conteneur.volume_conteneur) AS volume_total
                     FROM Centre_collecte
                     LEFT JOIN Conteneur ON Centre_collecte.id_centre_collecte = Conteneur.id_centre_collecte
                     GROUP BY Centre_collecte.lieu_collecte
                     ORDER BY lieu;
                 """

    mycursor.execute(sql_centres)
    centres = mycursor.fetchall()

    return render_template('/conteneur/etat_conteneur.html', centres=centres)


if __name__ == '__main__':
    app.run()
