import json
from flask import Flask,render_template,request,redirect,flash,url_for
from datetime import datetime


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        for club in listOfClubs:
            club['total_reserved'] = 0  # Initialiser 'total_reserved' pour chaque club
        return listOfClubs


def loadCompetitions(today=None):
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         if today is not None:
             comp = [competition for competition in listOfCompetitions if datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S") >= today]
             return comp
         return listOfCompetitions



app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()
today = datetime.now()
@app.route('/')
def index():
    comp = [competition for competition in competitions if datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S") >= today]
    return render_template('index.html', clubs=clubs, competitions= comp)


from flask import render_template, flash, redirect, url_for

from flask import flash

@app.route('/showSummary', methods=['POST'])
def showSummary():
    comp = [competition for competition in competitions if datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S") >= today]
    email = request.form.get('email')
    if not email:
        flash('Veuillez entrer votre adresse mail!', 'error')
        return redirect(url_for('index'))
    matching_clubs = [club for club in clubs if club['email'] == email]
    if not matching_clubs:
        flash('Aucun club trouvé avec cette adresse e-mail.', 'error')
        return redirect(url_for('index'))
    club = matching_clubs[0]
    return render_template('welcome.html', club=club, competitions=comp)



@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


from flask import redirect, url_for, flash


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition_name = request.form.get('competition')
    club_name = request.form.get('club')
    places = request.form.get('places')

    # Recherche de la compétition et du club
    competition = next((c for c in competitions if c['name'] == competition_name), None)
    club = next((c for c in clubs if c['name'] == club_name), None)

    # Vérifier si l'utilisateur a fourni toutes les données nécessaires
    if not competition or not club or not places:
        flash('Veuillez fournir toutes les informations nécessaires.')
        return render_template('welcome.html', club=club, competitions=competitions)

    placesRequired = int(places)

    # Vérifier si l'utilisateur essaie de réserver un nombre négatif ou plus de 12 billets
    if placesRequired <= 0:
        flash('Le nombre de billets doit être un nombre positif.')
        return render_template('welcome.html', club=club, competitions=competitions)
    elif placesRequired > 12 or club['total_reserved'] + placesRequired > 12:
        flash('Vous ne pouvez pas réserver plus de 12 billets au total.')
        return render_template('welcome.html', club=club, competitions=competitions)

    # Vérifier si le club a assez de points pour acheter les billets
    if int(club['points']) < placesRequired:
        flash('Vous n\'avez pas assez de points pour acheter ces billets.')
        return render_template('welcome.html', club=club, competitions=competitions)

    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    club['points'] = int(club['points'])-placesRequired  # Diminuer les points du club
    club['total_reserved'] += placesRequired  # Mettre à jour le total des places réservées

    flash('Réservation réussie !')
    return render_template('welcome.html', club=club, competitions=competitions)
 


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))