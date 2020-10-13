#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from flask_migrate import Migrate
from forms import *
import datetime
import random
import sys



#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:mypassword@localhost:5432/Fyyur'



#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))

    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    website = db.Column(db.String(120))

    Show = db.relationship('Show',backref='Venue')

    def toDic (self):

        dic = {
        'id': self.id,
        'name': self.name,
        'city': self.city,
        'state': self.state,
        'address': self.address,
        'phone': self.phone,
        'image_link': self.image_link,
        'facebook_link': self.facebook_link,
        'genres':self.genres,
        'seeking_description': self.seeking_description,
        'website': self.website

        }
        return dic

    def __repr__ (self):
        return f'<Venue {self.id} {self.name}>'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))

    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    website = db.Column(db.String(120))

    Show = db.relationship('Show',backref='Artist')

    def toDic (self):

        dic = {
        'id': self.id,
        'name': self.name,
        'city': self.city,
        'state': self.state,
        'phone': self.phone,
        'image_link': self.image_link,
        'facebook_link': self.facebook_link,
        'genres': self.genres,
        'seeking_description': self.seeking_description,
        'website': self.website

        }
        return dic


    def __repr__ (self):
        return f'<Aritst {self.id} {self.name}>'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO: Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
    __tablename__ = 'Shows'
    startTime = db.Column(db.DateTime,nullable=False,primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=True)

    venue = db.relationship('Venue')
    artist = db.relationship('Artist')

    def artistDic(self):
        dic = {
        "artist_id": self.artist_id,
        "artist_name": self.artist.name,
        "artist_image": self.artist.image_link,


        }

    def venueDic(self):
        dic = {
        "venue_id": self.venue_id,
        "venue_name": self.venue.name,
        "venue_image": self.venue.image_link,

        }

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
# we want to have a states that has whatever venues inside it (distinct)

      data = []
      dict = {}
      venues = []
      uniqueGeo = db.session.query(Venue.city, Venue.state).group_by(Venue.city, Venue.state).all()



    #we want to filter city and states so we can insert the venues underneath

      for v in uniqueGeo:
                city = v[0]
                state = v[1]

                locVenues = Venue.query.filter(Venue.city == city, Venue.state == state)

                dict = {
                    'city': city,
                    'state': state,
                    'venues': []
                }
                venueLocation = locVenues.all()
                # assiging each venue in state and city to the proper state and city
                for venue in venueLocation:
                    dict['venues'].append({
                    'id': venue.id
                    ,'name': venue.name
                    ,'num_upcoming_shows': len(list(filter(lambda var: var.startTime > datetime.datetime.today(), venue.Show))) #returns the length of the list of the shows that satisfies the condition on lambda
                    })
                print(dict['city'])
                data.append(dict)



    # venue_data = {
    #     'id': venue.id,
    #     'name': venue.name,
    #     'num_upcoming_shows': len(list(filter(lambda var: var.start_time > datetime.today(), venue.Show))) #returns the length of the list of the shows that satisfies the condition on lambda
    #         }

      return render_template('pages/venues.html',areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  term = request.form['search_term']

  search = "%{}%".format(term)
  result = Venue.query.filter(Venue.name.ilike(search)).all()
  data = []

  for r in result:
      temp = {}
      temp['id'] = r.id
      temp['name'] = r.name
      temp['num_upcoming_shows'] = len(list(filter(lambda var: var.startTime > datetime.datetime.today(), r.Show)))
      data.append(temp)

  response = {}
  response['count'] = len(data)
  response['data'] = data
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venues = {}
  # v = Venue.query.get(venue_id)
  #
  # seekingValue = False
  # if len(v.seeking_description) > 1:
  #     seekingValue = True
  #
  # p = list(filter(lambda var: var.startTime > datetime.datetime.today(), v.Show))
  # u = list(filter(lambda var: var.startTime <= datetime.datetime.today(), v.Show))
  # p = list(map(lambda var: var.artistDic(), p))
  # u = list(map(lambda var: var.artistDic(), u))
  #
  # venue = v.toDic()
  #
  # venue['past_shows'] = p
  # venue['upcoming_shows'] = u
  # venue['past_shows_count'] = len(p)
  # venue['upcoming_shows_count'] = len(u)
  # venue['seeking_talent'] = seekingValue
  # did not work, some how
  v = Venue.query.get(venue_id)
  num_shows = Show.query.filter_by(venue_id=v.id).all()
  seekingValue = False
  #check wether there is a discpretion
  if len(v.seeking_description) > 1:
      seekingValue = True
  past = []
  up = []

  for s in num_shows:
      artist = Artist.query.get(s.artist_id)
      # artist_dic = artist.artistDic()
      # date = [ ('start_time', str(s.startTime))]
      # artist_dic.update(date)
      artist_dic = {
      'artist_id': s.artist_id,
      'artist_name': artist.name,
      'artist_image_link': artist.image_link,
      'start_time': str(s.startTime)
      }

      if s.startTime > datetime.datetime.now():
          up.append(artist_dic)
      else:
          past.append(artist_dic)


  venues = v.toDic()
  venues['past_shows'] = past
  venues['upcoming_shows'] = up
  venues['past_shows_count'] = len(past)
  venues['upcoming_shows_count'] = len(up)
  venues['seeking_talent'] = seekingValue
  venues['genres'] = v.genres

  return render_template('pages/show_venue.html', venue= venues)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
    form = VenueForm()
    flag = False


    try:
          venue = Venue()

          venue.name = request.form['name']
          venue.city = request.form['city']
          venue.state = request.form['state']
          venue.address = request.form['address']
          venue.phone = request.form['phone']
          venue.genres = request.form.getlist('genres')

          venue.website = request.form['website']

          venue.seeking_description = request.form['seeking_description']

          venue.image_link = request.form['image_link']

          venue.facebook_link = request.form['facebook_link']


          db.session.add(venue)
          db.session.commit()

    except:
          db.session.rollback()
          flag = True
    finally:
          db.session.close()
      # on successful db insert, flash success
    if not flag:
          flash('Venue ' + request.form['name'] + ' was successfully listed!')
    else:
          flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
      # TODO: on unsuccessful db insert, flash an error instead.
      # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
      # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  delVenue = Venue.query.filter_by(id=venue_id)

  try:
      db.session.delete(delVenue)
      db.session.commit()
  except:
      db.session.rollback()
  finally:
      db.session.close()

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database

  return render_template('pages/artists.html', artists=Artist.query.all())

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  term = request.form['search_term']

  search = "%{}%".format(term)
  result = Artist.query.filter(Artist.name.ilike(search)).all()
  data = []


  for r in result:
        temp = {}
        temp['id'] = r.id
        temp['name'] = r.name
        temp['num_upcoming_shows'] = len(list(filter(lambda var: var.startTime > datetime.datetime.today(), r.Show)))
        data.append(temp)

  response = {}
  response['count'] = len(data)
  response['data'] = data

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  a = Artist.query.get(artist_id)
  num_shows = Show.query.filter_by(artist_id=a.id).all()
  seekingValue = False
  #check wether there is a discpretion
  if len(a.seeking_description) > 1:
      seekingValue = True
  print(seekingValue)

  past = []
  up = []

  for s in num_shows:
      venue = Venue.query.get(s.venue_id)
      # artist_dic = artist.artistDic()
      # date = [ ('start_time', str(s.startTime))]
      # artist_dic.update(date)
      venue_dic = {
      'venue_id': venue.id,
      'venue_name': venue.name,
      'venue_image_link': venue.image_link,
      'start_time': str(s.startTime)
      }

      if s.startTime > datetime.datetime.now():
          up.append(venue_dic)
      else:
          past.append(venue_dic)
  newGenres= []
  newGenre = []
  strng = ""
  index = 0
  comas = []
  for g in a.genres:
    if g == ",":
        comas.append(index)
    if g == "}":
        comas.append(index)
    index = index + 1

  x = 0
  y = 0
  z = 0
  while x < len(comas):
      while y < comas[x]:
          strng += a.genres[y]
          y = y+1
      newGenres.append(strng)
      strng = ""
      x = x+1

  for g in newGenres:
      if g.find('{') != -1:
          newGenre.append(g.replace('{',''))
      if g.find(',') != -1:
          newGenre.append(g.replace(',',''))

  print(len(a.genres))
  print(len(comas))
  if len(comas) == 0:
        while z < len(a.genres):
            strng += a.genres[y]
            z = z+1

        newGenre.strng
        strng = ""


  # i dont know whats worng, but the genres was splited with comas (although i have deleted the split method)
  # but the above code, is just to return the genres to its normal form, a list of genres
  artist = a.toDic()
  artist['past_shows'] = past
  artist['upcoming_shows'] = up
  artist['past_shows_count'] = len(past)
  artist['upcoming_shows_count'] = len(up)
  artist['seeking_venue'] = seekingValue
  artist['genres'] = newGenre
  print(a.genres)
  return render_template('pages/show_artist.html', artist=artist)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  a = Artist.query.get(artist_id)
  # artist = a.toDic
  #
  # form.name.data = a.name
  # form.phone.data = a.phone
  # form.image_link.data = a.image_link
  # form.city.data = a.city
  # form.state.data = a.state
  # form.facebook_link.data = a.facebook_link
  # form.genres.data = a.genres
  # form.website.data = a.website
  # form.seeking_description.data = a.seeking_description

  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=a)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
      form = ArtistForm()

      print('no')
      a = Artist.query.get(artist_id)
      print('no')
      a.name = request.form['name']
      a.genres = request.form['genres']
      a.city = request.form['city']
      print('no')
      a.state = request.form['state']
      a.facebook_link = request.form['facebook_link']
      a.image_link = request.form['image_link']
      print('no')
      a.phone = request.form['phone']
      a.seeking_description = request.form['seeking_description']
      print('no')
      a.website = request.form['website']
      print('no')
      db.session.add(a)
      db.session.commit()
      #
      # db.session.rollback()
      # print('yes, its an error')
      #
      # db.session.close()
      return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)

  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
    form = VenueForm()

    print('no')
    a = Venue.query.get(venue_id)
    print('no')
    a.name = request.form['name']
    a.genres = request.form['genres']
    a.city = request.form['city']
    print('no')
    a.state = request.form['state']
    a.facebook_link = request.form['facebook_link']
    a.image_link = request.form['image_link']
    print('no')
    a.phone = request.form['phone']
    a.seeking_description = request.form['seeking_description']
    print('no')
    a.website = request.form['website']
    print('no')
    db.session.add(a)
    db.session.commit()

    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html',form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():

  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
    flag = False


    try:
      artist = Artist()

      artist.name = request.form['name']
      artist.city = request.form['city']
      artist.state = request.form['state']
      artist.phone = request.form['phone']
      artist.genres = request.form.getlist('genres')
      artist.seeking_description = request.form['seeking_description']
      artist.website = request.form['website']
      artist.image_link = request.form['image_link']
      artist.facebook_link = request.form['facebook_link']

      db.session.add(artist)
      db.session.commit()

    except:
      flag = True
      db.session.rollback()
      print(sys.exc_info())
    finally:
      db.session.close()

    if not flag:
        flash('Artist ' + request.form['name'] + ' Was successfully added!')
    else:
        flash('an error occurred. Artist '+request.form['name'] + ' could not be listed')

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.


  all_shows = Show.query.all()
  print(all_shows[0].artist_id)
  data= []

  for show in all_shows:
      venue = show.venue
      artist = show.artist
      data.append({
      'venue_id': show.venue_id,
      'venue_name': venue.name,
      'aritst_id': show.artist_id,
      'artist_name': artist.name,
      'artist_image_link': artist.image_link,
      'start_time': str(show.startTime)
      })
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  flag = False
  try:
      show = Show()
      show.startTime = request.form['start_time']
      show.artist_id = request.form['artist_id']
      show.venue_id = request.form['venue_id']

      db.session.add(show)
      db.session.commit()
  except:
      db.session.rollback
      flag = true
  finally:
      db.session.close()


  # on successful db insert, flash success
  if not flag:
        flash('Show was successfully listed!')
  else:
        flash('problem occured when listing Show!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
