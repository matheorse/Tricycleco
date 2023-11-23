import pymysql.cursors
#import dotenv
#import os
from flask import Flask, request, render_template, redirect, url_for, abort, flash
from flask import session, g

app = Flask(__name__)
app.secret_key = 'une cle(token) : grain de sel(any random string)'
def get_db():
    #dotenv.load_dotenv()
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
    return render_template('collecte/show_collecte.html', Collecte=Collecte)
@app.route('/ville/add', methods=['GET'])
def add_ville():
    return render_template('ville/add_ville.html')
@app.route('/ville/add', methods=['POST'])
def valid_add_ville():
    nomVille = request.form.get('nomVille', '')
    id = request.form.get('id', '')
    print(u'ville ajoutée , nomVille :', nomVille)
    message = u'La ville '+ nomVille +" avec l'id: "+id+" est ajoutée."
    flash(message, 'alert-success')
    return redirect('/ville/show')
@app.route('/ville/delete', methods=['GET'])
def delete_ville():
    id = request.args.get('id', '')
    nomVille = request.args.get('nomVille', '')
    message = u'La ville '+ nomVille +" avec l'id: "+id+" est supprimée."
    flash(message, 'alert-warning')
    return redirect('/ville/show')
@app.route('/ville/edit', methods=['GET'])
def edit_ville():
    id = request.args.get('id', '')
    nomVille = request.args.get('nomVille', '')
    id=int(id)
    ville = villes[id-1]
    return render_template('ville/edit_ville.html', villes=ville)

@app.route('/ville/edit', methods=['POST'])
def valid_edit_ville():
    nomVille = request.form['nomVille']
    id = request.form.get('id', '')
    print(u'ville modifiée, id: ',id, " nom de la Ville :", nomVille)
    message=u'ville modifiée, id: ' + id + " nom de la Ville : " + nomVille
    flash(message, 'alert-success')
    return redirect('/ville/show')
@app.route('/parking/edit/show')
def edit_show_parking():
    return render_template('parking/edit_show_parking.html', parking=parkings , villes=villes)

@app.route('/parking/edit/add', methods=['GET'])
def edit_add_parking():
    return render_template('parking/edit_add_parking.html', villes=villes)

@app.route('/parking/edit/add', methods=['POST'])
def valid_edit_add_parking():
    nomParking = request.form.get('nomParking', '')
    Ville_id = request.form.get('ville_id', '')
    nbPlaces = request.form.get('nbPlaces', '')
    dateConstruction = request.form.get('dateConstruction', '')
    adresse = request.form.get('adresse', '')
    prixPlaceHeure = request.form.get('prixPlaceHeure', '')
    photo = request.form.get('photo', '')
    print(u'parking ajouté , nomParking: ', nomParking, ' - ville_id :', Ville_id, ' - nbPlaces:', nbPlaces, ' - dateConstruction:', dateConstruction, ' - adresse:', adresse, ' - prixPlaceHeure:', prixPlaceHeure,' - photo:', photo)
    message = u'parking ajouté , nomParking:'+nomParking + '- ville_id :' + Ville_id + ' - nbPlaces:' + nbPlaces + ' - dateConstruction:'+  dateConstruction + ' - adresse:' + adresse + ' - prixPlaceHeure:' + prixPlaceHeure + ' - photo:' + photo
    flash(message, 'alert-success')
    return redirect('/parking/edit/show')

@app.route('/parking/edit/delete', methods=['GET'])
def edit_delete_parking():
    id = request.args.get('id', '')
    message=u'un parking supprimé avec l\'id : ' + id
    flash(message, 'alert-warning')
    return redirect('/parking/edit/show')

@app.route('/parking/edit/edit', methods=['GET'])
def edit_edit_parking():
    id = request.args.get('id', '')
    parking = parkings[int(id)-1]
    return render_template('parking/edit_edit_parking.html', parking=parking, villes=villes)

@app.route('/parking/edit/edit', methods=['POST'])
def valid_edit_edit_parking():
    nomParking = request.form['nomParking']
    id = request.form.get('id', '')
    Ville_id = request.form.get('Ville_id', '')
    nbPlaces = request.form.get('nbPlaces', '')
    dateConstruction = request.form.get('dateConstruction', '')
    adresse = request.form.get('adresse', '')
    prixPlaceHeure = request.form.get('prixPlaceHeure', '')
    photo = request.form.get('photo', '')

    if photo!='':
        message = u'parking modifié, id:'+ id + ' - nomParking: '+nomParking + ' - ville id: ' + Ville_id + ' - nbPlaces: ' + nbPlaces + ' - dateConstruction: '+  dateConstruction + ' - adresse: ' + adresse + ' - prixPlaceHeure:'+ prixPlaceHeure + ' - photo:'+photo
    else:
        message = u'parking modifié, id:'+ id + ' - nomParking: '+nomParking + ' - ville id: ' + Ville_id + ' - nbPlaces: ' + nbPlaces + ' - dateConstruction: '+  dateConstruction + ' - adresse: ' + adresse + ' - prixPlaceHeure:'+ prixPlaceHeure
    flash(message, 'alert-success')
    return redirect('/parking/edit/show')


@app.route('/parking/show', methods=['GET'])
def show_parking():
    filter_word = request.args.get('filter_word',None)
    filter_value_min = request.args.get('filter_value_min', None)
    filter_value_max = request.args.get('filter_value_max', None)
    filter_value_date_min = request.args.get('filter_value_date_min', None)
    filter_value_date_max = request.args.get('filter_value_date_max', None)
    print(type(filter_value_date_min))
    filter_items = request.args.getlist('filter_items', None)
    if filter_word and filter_word != "":
        message = u'filtre sur le mot : '+filter_word
        flash(message,'alert-success')
    if filter_value_date_min or filter_value_date_max:
        if filter_value_date_max!='' and filter_value_date_min=='':
            message = u"Date de construction: Toute jusqu'à "+ filter_value_date_max[8:10]+"/"+filter_value_date_max[5:7]+"/"+filter_value_date_max[:4]
            flash(message, 'alert-success')
        elif filter_value_date_max=='' and filter_value_date_min!='':
            message = u"Date de construction: Du "+ filter_value_date_min[8:10]+"/"+filter_value_date_min[5:7]+"/"+filter_value_date_min[:4] +u" jusqu'à la fin"
            flash(message, 'alert-success')
        elif int(filter_value_date_max[:4]) >= int(filter_value_date_min[:4]) and int(filter_value_date_max[5:7]) >= int(filter_value_date_min[5:7]) and int(filter_value_date_max[8:10]) >= int(filter_value_date_min[8:10]):
            message = u"Date de construction: Du " + filter_value_date_min[8:10] + "/" + filter_value_date_min[5:7] + "/" + filter_value_date_min[:4] + u" jusqu'à "+ filter_value_date_max[8:10]+"/"+filter_value_date_max[5:7]+"/"+filter_value_date_max[:4]
            flash(message, 'alert-success')
        else:
            message=u"Date de construction: (Date_début < Date_fin)"
            flash(message, 'alert-warning')
    if filter_value_min or filter_value_max:
        if filter_value_min.isdecimal() and filter_value_max.isdecimal():
            if int(filter_value_min) < int(filter_value_max):
                message = u'Prix de la place par heure entre ' + filter_value_min + '€ et ' + filter_value_max +u'€'
                flash(message , 'alert-success')
            else:
                message=u'min <max'
                flash(message,'alert-warning')
        elif filter_value_min.isdecimal() and filter_value_max=='':
            message = u'Prix de la place par heure entre ' + filter_value_min + '€ et plus'
            flash(message, 'alert-success')
        elif filter_value_min =='' and filter_value_max.isdecimal():
            message = u'Prix de la place par heure entre ' + filter_value_max + '€ et moins'
            flash(message, 'alert-success')
        else:
            message=u'Le prix ne peut pas être <0'
            flash(message, 'alert-warning')
    if filter_items and filter_items != []:
        message=u'ville sélectionnée '
        for case in filter_items:
            message+='id: '+case+ ', '
        flash(message[:-2], 'alert-success')
    return render_template('parking/show_parking.html', villes=villes,parking=parkings)

if __name__ == '__main__':
    app.run()