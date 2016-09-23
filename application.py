#!/usr/bin/env python

from flask import Flask, render_template, request, redirect
from flask import jsonify, url_for, flash, make_response
from flask import session as login_session

from jinja2 import Environment

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, PlaceType, Place

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

import random
import string
import httplib2
import json
import requests

# Add in loopcontrols Jinja extension (to add break functionality)
jinja_env = Environment(extensions=['jinja2.ext.loopcontrols'])

app = Flask(__name__)

# Add the loop controls extension to app
app.jinja_env.add_extension('jinja2.ext.loopcontrols')


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = 'Nuevo Mexico'


# Connect to the database and create a database session
engine = create_engine('sqlite:///nuevomexico.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def showLogin():
    """Create an anti-forgery state token"""
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """Create a route to login with Google"""
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data

    try:
        # Change the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json',
                                             scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Make sure the access token is valid
    access_token = credentials.access_token
    # Make a JSON get request
    url = (
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' %
        access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # Abort if there was an error in the access token info
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is for the intended user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this application
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check to see if the user is already logged in
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps
                                 ('Cuurent user is already connected'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use
    login_session['provider'] = 'google'
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # See if the user exists, if the user does not exist, create a new user
    # Store the user's user_id in the login_session under user_id
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '</h1>'
    output += '<img_src"'
    output += login_session['picture']
    output += '"style = width: 200px; height: 200px; border-radius: 150px; -webkit-border-radius: 150px; -moz-border-radius: 150px;">'  # noqa
    flash('You are now logged in as %s' % login_session['username'])
    return output


@app.route('/gdisconnect')
def gdisconnect():
    """
    Create a Google disconnect route
    (revoke a current user's token and reset their login session)
    """
    access_token = login_session['access_token']
    if access_token is None:
        print 'Access token is None'
        response = make_response(json.dumps
                                 ('Current user not connected'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Execute HTTP GET request to revoke current token
    access_token = login_session.get('credentials')
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session[  # noqa
        'access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] != '200':
        # The given token was invalid
        response = make_response(
            json.dumps('Failed to revoke token for given user'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    """Create a Facebook login route"""
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data

    # Exchange client token for a long-lived server-side token
    app_id = json.loads(
        open(
            'fb_client_secrets.json',
            'r').read())['web']['app_id']
    app_secret = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (  # noqa
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = 'https://graph.facebook.com/v2.4/me'
    # Strip expire tag from access token
    token = result.split('&')[0]

    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data['name']
    login_session['email'] = data['email']
    login_session['facebook_id'] = data['id']

    # Token must be stored in the login_session in order to properly logout
    stored_token = token.split('=')[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token  # noqa
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['picture'] = data['data']['url']

    # Check to see if the user already exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '</h1>'
    output += '<img_src"'
    output += login_session['picture']
    output += '"style = width: 200px; height: 200px; border-radius: 150px; -webkit-border-radius: 150px; -moz-border-radius: 150px;">'  # noqa
    flash('You are now logged in as %s' % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    """Create a Facebook disconnect route"""
    facebook_id = login_session['facebook_id']
    # The access token must be included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s?permissions?access_token=%s' % (
        facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return 'You have been logged out'


@app.route('/disconnect')
def disconnect():
    """Create a disconnect route"""
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']

        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash('You have successfully been logged out.')
        return redirect(url_for('showPlaceTypes'))
    else:
        flash('You are not logged in.')
        redirect(url_for('showPlaceTypes'))


@app.route('/')
def showHome():
    """Create a route to the welcome or home page"""
    return render_template('index.html')


@app.route('/about/')
def showAbout():
    """Create a route to the about page"""
    return render_template('about.html')


@app.route('/placetype/')
def showPlaceTypes():
    """Create a route to show all types of places to visit"""
    placeTypes = session.query(PlaceType).order_by(asc(PlaceType.name))
    if 'username' not in login_session:
        return render_template('publicPlaceTypes.html',
                               placeTypes=placeTypes)
    else:
        return render_template('placeTypes.html',
                               placeTypes=placeTypes)


@app.route('/placetype/new/', methods=['GET', 'POST'])
def newPlaceType():
    """Create a route for creating a new place type"""
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newType = PlaceType(name=request.form['name'],
                            user_id=login_session['user_id'])
        session.add(newType)
        session.commit()
        flash('New place type %s created' % newType.name)
        return redirect(url_for('showPlaceTypes'))
    else:
        return render_template('newPlaceType.html')


@app.route('/placetype/<int:placeType_id>/edit/', methods=['GET', 'POST'])
def editPlaceType(placeType_id):
    """Create a route for editing a place type"""
    editType = session.query(PlaceType).filter_by(id=placeType_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editType.user_id != login_session['user_id']:
        return "<script>function myfunction() {alert('You are not authorized to edit this place type. Only the creator can edit it.');}</script><body onload='myfunction()'>"  # noqa
    if request.method == 'POST':
        if request.form['name']:
            editType.name = request.form['name']
            session.add(editType)
            session.commit()
            flash('Place type successfully edited')
            return redirect(url_for('showPlaceTypes'))
    else:
        return render_template('editPlaceType.html',
                               placeType_id=placeType_id, placeType=editType)


@app.route('/placetype/<int:placeType_id>/delete/',
           methods=['GET', 'POST'])
def delPlaceType(placeType_id):
    """Create a route for deleting a place type"""
    delType = session.query(PlaceType).filter_by(id=placeType_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if delType.user_id != login_session['user_id']:
        return "<script>function myfunction() {alert('You are not authorized to delete this place type. Only the creator can delete it.');}</script><body onload='myfunction()'>"  # noqa
    if request.method == 'POST':
        session.delete(delType)
        session.commit()
        flash('Place type successfully deleted')
        return redirect(url_for('showPlaceTypes'))
    else:
        return render_template('deletePlaceType.html',
                               placeType_id=placeType_id, placeType=delType)


@app.route('/placetype/<int:placeType_id>/')
@app.route('/placetype/<int:placeType_id>/place/')
def showPlaces(placeType_id):
    """Create a route for displaying a list of places within one category"""
    placeType = session.query(PlaceType).filter_by(id=placeType_id).one()
    creator = getUserInfo(placeType.user_id)
    places = session.query(Place).filter_by(placeType_id=placeType_id).\
        order_by(Place.name).all()
    if 'username' not in login_session or creator.id != login_session[
            'user_id']:
        return render_template(
            'publicPlaces.html',
            placeType=placeType,
            places=places,
            creator=creator)
    else:
        return render_template('places.html', placeType=placeType,
                               places=places, creator=creator)


@app.route('/placetype/<int:placeType_id>/place/new/',
           methods=['GET', 'POST'])
def newPlace(placeType_id):
    """Create a route for creating a new place"""
    placeType = session.query(PlaceType).filter_by(id=placeType_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if placeType.user_id != login_session['user_id']:
        return "<script>function myfunction() {alert('You are not authorized to create a new place for this category. Only the place type creator can do this.');}</script><body onload='myfunction()'>"  # noqa
    if request.method == 'POST':
        rawLink = request.form['link']
        if 'http://' not in rawLink:
            rawLink = 'http://' + rawLink
        newPlaceItem = Place(name=request.form['name'],
                             description=request.form['description'],
                             location=request.form['location'],
                             price=request.form['price'],
                             link=rawLink,
                             placeType_id=placeType_id)
        session.add(newPlaceItem)
        session.commit()
        flash('New place successfully created')
        return redirect(url_for('showPlaces', placeType_id=placeType_id))
    else:
        return render_template('newPlace.html', placeType=placeType)


@app.route('/placetype/<int:placeType_id>/place/<int:place_id>/edit/',
           methods=['GET', 'POST'])
def editPlace(placeType_id, place_id):
    """Create a route for editing a place"""
    placeType = session.query(PlaceType).filter_by(id=placeType_id).one()
    editPlaceItem = session.query(Place).filter_by(id=place_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if placeType.user_id != login_session['user_id']:
        return "<script>function myfunction() {alert('You are not authorized to edit this place. Only the place type creator can edit it.');}</script><body onload='myfunction()'>"  # noqa
    if request.method == 'POST':
        if request.form['name']:
            editPlaceItem.name = request.form['name']
            editPlaceItem.description = request.form['description']
            editPlaceItem.location = request.form['location']
            editPlaceItem.price = request.form['price']
            link = request.form['link']
            if 'http://' not in link:
                link = 'http://' + link
            editPlaceItem.link = link
            session.add(editPlaceItem)
            session.commit()
            flash('Place successfully edited')
            return redirect(url_for('showPlaces',
                                    placeType_id=placeType_id))
    else:
        return render_template('editPlace.html', placeType=placeType,
                               place=editPlaceItem)


@app.route('/placetype/<int:placeType_id>/place/<int:place_id>/delete/',
           methods=['GET', 'POST'])
def delPlace(placeType_id, place_id):
    """Create a route for deleting a place"""
    placeType = session.query(PlaceType).filter_by(id=placeType_id).one()
    delPlaceItem = session.query(Place).filter_by(id=place_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if placeType.user_id != login_session['user_id']:
        return "<script>function myfunction() {alert('You are not authorized to delete this place. Only the place type creator can delete it.');}</script><body onload='myfunction()'>"  # noqa
    if request.method == 'POST':
        session.delete(delPlaceItem)
        session.commit()
        flash('Place successfully deleted')
        return redirect(url_for('showPlaces', placeType_id=placeType_id))
    else:
        return render_template('deletePlace.html', placeType=placeType,
                               place=delPlaceItem)


# Create routes for JSON API endpoints
@app.route('/placetype/JSON/')
def showPlaceTypesJSON():
    """Create an API endpoint for a list of types of places to visit"""
    placeTypes = session.query(PlaceType).order_by(PlaceType.id).all()
    return jsonify(placeTypeList=[p.serialize for p in placeTypes])


@app.route('/placetype/<int:placeType_id>/place/JSON/')
def showPlacesJSON(placeType_id):
    """
    Create an API endpoint for a list of places wihtin one place type
    """
    placeType = session.query(PlaceType).filter_by(id=placeType_id).one()
    places = session.query(Place).filter_by(placeType_id=placeType_id).\
        order_by(Place.name).all()
    return jsonify(placesList=[p.serialize for p in places])


@app.route('/placetype/<int:placeType_id>/place/<int:place_id>/JSON/')
def showPlaceDetailsJSON(placeType_id, place_id):
    """Create an API endpoint for an individual place item"""
    place = session.query(Place).filter_by(id=place_id).one()
    return jsonify(placeDetails=place.serialize)


# Create helper functions
def createUser(login_session):
    """Create createUser function"""
    # Create a new instance of the User class
    newUser = User(
        name=login_session['username'],
        email=login_session['email'],
        picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    """Create getUserInfo function"""
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    """Create getUserID function"""
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


if __name__ == '__main__':
    app.secret_key = '12345'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)


# SOURCES

# This should probably go without saying, but I relied very (very!) heavily
# on the related Udacity videos and examples for the code in this script
# as well as the html files in the templates directory, the database_setup.py
# file and the populator.py file.
