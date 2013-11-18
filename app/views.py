from flask import render_template, redirect, flash, g, request, url_for
import sqlite3
import config
from app import app
from forms import TournForm, PlayerForm, TourneyEntryForm, MatchForm
from models import Tournament, Player, Match
import tournament_dao, player_dao, tourney

@app.route('/', methods = ['GET','POST'])
def index():
    form = TournForm()
    if form.validate_on_submit():
        tournament = Tournament(0,'',form.description.data,
                                form.tourn_type.data,0)
        tournament_dao.create(tournament)
    tournaments = tournament_dao.find_all()
    return render_template('index.html', 
                           tournaments=tournaments,
                           form=form)

@app.route('/tournament/<id>', methods = ['GET','POST'])
def tournament(id):
    tournament = tournament_dao.find(id)
    form = TourneyEntryForm()
    if not tournament.begun and not form.is_submitted():
        players = player_dao.find_all()
        form.enter.choices = [(player.id, player.fname) for player in players]
        return render_template('edit-tournament.html', 
                               tournament=tournament,
                               players=player,
                               form=form)
    if form.is_submitted():
        tourney.setup_round_robin(form.enter.data, id)
    return redirect('/play-tournament/%s' % id)

@app.route('/play-tournament/<id>', methods = ['GET','POST'])
def play_tournament(id):
    form = MatchForm()
    print form
    if request.method == 'POST': #NEED TO CLEAN UP VALIDATION
        match_dao.update(form.id.data, form.score1.data, form.score2.data)
    tournament = tournament_dao.find(id)
    schedule = tourney.find_matches(id)
    return render_template('play-tournament.html', 
                           tournament=tournament,
                           schedule=schedule,
                           form=form)
    
@app.route('/player', methods = ['GET','POST'])
def player():
    form = PlayerForm()
    if form.validate_on_submit():
        player = Player(form.fname.data)
        player_dao.create(player)
        form.fname.data = ''
    players = player_dao.find_all()
    return render_template('player.html', 
                           players=players,
                           form=form)

@app.before_request
def before_request():
    g.db = connect_db()
    g.db.execute('pragma foreign_keys = ON')
    g.db.commit()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def connect_db():
    return sqlite3.connect(config.DATABASE)

