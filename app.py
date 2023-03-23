import os

from flask import Flask, render_template, request, flash, redirect, session, g,abort,jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from riotwatcher import LolWatcher,ApiError
from SECRETAPI import LOLAPI

from forms import SearchMatch, Register, Login
from models import db, connect_db,Puuid,User

lol_watcher = LolWatcher(LOLAPI)
region = 'na1'

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL','postgresql:///lolmatch'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = "it's a secret"
toolbar = DebugToolbarExtension(app)

connect_db(app)

me = lol_watcher.summoner.by_name('na1','finkle11')
@app.route('/')
def home():
    # search = SearchMatch()
    championlist = lol_watcher.data_dragon.champions('13.5.1')
    return render_template('index.html',champions=championlist)

@app.route('/search',methods=['GET','POST'])
def search():
    form = SearchMatch()
    if form.validate_on_submit():
        value = form.search.data
        name = Puuid.query.filter_by(username=value).first()
        if name is None:
            summoner = lol_watcher.summoner.by_name('na1',value)

            addpuuid = Puuid(puuid= (summoner['puuid']),username=value) 
            db.session.add(addpuuid)
            db.session.commit()
        return redirect(f'/search/{value}')
    return render_template('search.html',form=form)

@app.route('/search/<username>',methods=['GET'])
def showmatches(username):
    user = Puuid.query.filter_by(username=username).first()
    
    matches = lol_watcher.match.matchlist_by_puuid('na1',user.puuid,0,2)
    games = []
    for match in matches:
        games.append(lol_watcher.match.by_id('na1',match))
    
    counter = 0;
    # enemies = []
    # for puuid in games[0]['info']['participants']:
    #    if puuid['puuid'] == user.puuid:
    #         player = puuid
    #    else: enemies.append(puuid)
    # return render_template('match.html',player=player, enemies=enemies,games=games,user=user)
    return render_template('match.html',games=games,user=user,counter=counter)

# User Signup/login/logout

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user unique id to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/register',methods=['GET','POST'])
def register():
    """Handle user Signup. Add user to db, redirect to home page."""
    form = Register()
    if form.validate_on_submit():
        try:
            user = User.register(username=form.username.data,
                                 password=form.password.data,
                                 email=form.email.data,
                                 image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()

        except IntegrityError:
            flash('Username already taken','danger')
            return render_template('register.html',form=form)
        
        do_login(user)
        return redirect('/')

    else:
        return render_template('register.html',form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        user = User.authenticate(username=form.username.data,
                                 password=form.password.data)
        if user:
            do_login(user)
            flash(f"Hello, {user.username}!","success")
            return redirect('/')
        
        flash("Invalid credentials.","danger")

    return render_template('login.html',form=form)

@app.route('/logout')
def logout():
    session.pop(CURR_USER_KEY)
    flash('Goodbye!','info')
    return redirect('/')

#Profile login/edit settings

@app.route('/users/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Not a current User','danger')
        return redirect('/')
    
    return render_template('profile.html',user=user)
    


# @app.route('/matches')
# def history():
#     matches = lol_watcher.match.matchlist_by_puuid('na1',me['puuid'],0,2)
#     return render_template('match.html',me=me,matches=matches)