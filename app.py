from flask import Flask, render_template, request, flash, redirect, session, g,abort,jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from riotwatcher import LolWatcher,ApiError
from SECRETAPI import LOLAPI

lol_watcher = LolWatcher(LOLAPI)
region = 'na1'



from forms import SearchMatch
from models import db, connect_db,Puuid

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///lolmatch'

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
    # enemies = []
    # for puuid in games[0]['info']['participants']:
    #    if puuid['puuid'] == user.puuid:
    #         player = puuid
    #    else: enemies.append(puuid)
    # return render_template('match.html',player=player, enemies=enemies,games=games,user=user)
    return render_template('match.html',games=games,user=user)
    # return render_template('match.html',matches=matches,match=match)


# @app.route('/matches')
# def history():
#     matches = lol_watcher.match.matchlist_by_puuid('na1',me['puuid'],0,2)
#     return render_template('match.html',me=me,matches=matches)