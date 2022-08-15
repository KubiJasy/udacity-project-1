#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import collections
import datetime

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
collections.Callable = collections.abc.Callable
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migration = Migrate(app, db)

# TODO: connect to a local postgresql database
from models import *

# #----------------------------------------------------------------------------#
#   SETUP GENRES TABLE
#----------------------------------------------------------------------------#

# Run migrations and then run sql script, genres_populate.sql to populate the genres table
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  if isinstance(value, str):
        date = dateutil.parser.parse(value)
  else:
      date = value
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

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
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  #return unique orderedrecords of venues based on city and state
  venues = Venue.query.with_entities(Venue.city, Venue.state).distinct().order_by(Venue.city, Venue.state).all()
  data = []
  for venue in venues:
    venue_dict = {}
    venue_list = []
    venue_dict['city'] = venue.city
    venue_dict['state'] = venue.state
    # query for venues with the same state and city
    venues_filtered = Venue.query.filter(Venue.city == venue.city, Venue.state == venue.state).all()
    for details in venues_filtered:
      venues_filtered_dict = {}
      # loop through and add necessary fields to venues list.
      venues_filtered_dict['id'] = details.venue_id
      venues_filtered_dict['name'] = details.name
      # get upcoming shows
      upcoming_show_count = Show.query.filter(Show.venue_id == details.venue_id, Show.date >= datetime.datetime.now()).count()
      venues_filtered_dict['num_upcoming_shows'] = upcoming_show_count

      venue_list.append(venues_filtered_dict)
    
    # appending venue list to venue data list
    venue_dict['venues'] = venue_list
    data.append(venue_dict)
  return render_template('pages/venues.html', areas=data)

# ******************TO DO *******************************************
@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  search_string = request.form['search_term'].lower()

  results = db.session.query(Venue).filter(Venue.name.ilike(f'%{search_string}%')).all()

  count = db.session.query(Venue).filter(Venue.name.ilike(f'%{search_string}%')).count()
 

  data = [{'id': result.venue_id, 
           'name' : result.name, 
           'num_upcoming_shows': Show.query.filter(Show.venue_id == result.venue_id, Show.date >= datetime.datetime.now()).count()}
           for result in results]

  response = {
    'count': count,
    'data' : data
  }

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
#   shows the venue page with the given venue_id
#   TODO: replace with real venue data from the venues table, using venue_id
  data = {}
  venue_details = Venue.query.get(venue_id)
  data['id'] = venue_id
  data['name'] = venue_details.name
  data['genres'] = [genre.name for genre in venue_details.genres]
  data['address'] = venue_details.address
  data['city'] = venue_details.city
  data['state'] = venue_details.state
  data['phone'] = venue_details.phone
  data['website'] = venue_details.website_link
  data['facebook_link'] = venue_details.facebook_link
  data['seeking_talent'] = venue_details.seeking_talent
  data['seeking_description'] = venue_details.seeking_talent_desc
  data['image_link'] = venue_details.image_link
  artist_shows_past = db.session.query(Show, Artist).join(Artist).filter(Show.venue_id == venue_id, Show.date <= datetime.datetime.now()).all()
  artist_shows_upcoming = db.session.query(Show, Artist).join(Artist).filter(Show.venue_id == venue_id, Show.date >= datetime.datetime.now()).all()
  data['past_shows'] = [{'artist_id' : artist.artist_id,
                            'artist_name' : artist.name,
                            'artist_image_link' : artist.image_link,
                            'start_time' : show.date }
                            for show, artist in artist_shows_past
                            ] 
  
  data['upcoming_shows'] = [{'artist_id' : artist.artist_id,
                            'artist_name' : artist.name,
                            'artist_image_link' : artist.image_link,
                            'start_time' : show.date }
                            for show, artist in artist_shows_upcoming
                            ] 
  
  data['past_shows_count'] = Show.query.filter(Show.venue_id == venue_id, Show.date <= datetime.datetime.now()).count()
  data['upcoming_shows_count'] = Show.query.filter(Show.venue_id == venue_id, Show.date >= datetime.datetime.now()).count()
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  form.genres.choices =  [(genre.genre_id, genre.name) for genre in Genre.query.all()]
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm(request.form)
  form.genres.choices =  [(genre.genre_id, genre.name) for genre in Genre.query.all()]
  # TODO: insert form data as a new Venue record in the db, instead
  if form.validate():
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    address = request.form.get('address', None)
    phone = request.form.get('phone', None)
    genres = request.form.getlist('genres')
    image_link = request.form['image_link']
    facebook_link = request.form.get('facebook_link', None)
    website_link = request.form.get('website_link', None)
    seeking_talent = request.form.get('seeking_talent', None)
    if seeking_talent == 'y':
      seeking_talent = True
    else:
      seeking_talent = False
    seeking_description = request.form.get('seeking_description', None)

    venue_record = Venue(name=name, city=city, state=state, address=address, phone=phone, image_link=image_link, facebook_link=facebook_link, website_link=website_link, seeking_talent=seeking_talent, seeking_talent_desc=seeking_description)

    for genre in genres:
          genre_obj = db.session.query(Genre).filter(Genre.genre_id == genre).first()
          venue_record.genres.append(genre_obj)
    try:
      db.session.add(venue_record)
      db.session.commit()
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
      error = True
      db.session.rollback()
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
      
    finally:
      db.session.close()
    return render_template('pages/home.html')
  
  
  return render_template('forms/new_venue.html', form=form)
    # TODO: modify data to be the data object returned from db insertion

    # on successful db insert, flash success
    
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    
  


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  venue_record = Venue.query.get_or_404(venue_id)
  name = venue_record.name
  db.session.delete(venue_record)
  db.session.commit()
  db.session.close()
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  artists = Artist.query.order_by(Artist.name).all()
  data = [{'id' : artist.artist_id, 'name' : artist.name} for artist in artists]
  return render_template('pages/artists.html', artists=data)

# ******************TO DO *******************************************
@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_string = request.form['search_term'].lower()

  results = db.session.query(Artist).filter(Artist.name.ilike(f'%{search_string}%')).all()

  count = db.session.query(Artist).filter(Artist.name.ilike(f'%{search_string}%')).count()
 

  data = [{'id': result.artist_id, 
           'name' : result.name, 
           'num_upcoming_shows': Show.query.filter(Show.artist_id == result.artist_id, Show.date >= datetime.datetime.now()).count()}
           for result in results]

  response = {
    'count': count,
    'data' : data
  }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id

  data = {}
  artist_details = Artist.query.get(artist_id)
  data['id'] = artist_id
  data['name'] = artist_details.name
  data['genres'] = [genre.name for genre in artist_details.genres]
  data['city'] = artist_details.city
  data['state'] = artist_details.state
  data['phone'] = artist_details.phone
  data['website'] = artist_details.website_link
  data['facebook_link'] = artist_details.facebook_link
  data['seeking_venue'] = artist_details.seeking_venue
  data['seeking_description'] = artist_details.seeking_venue_desc
  data['image_link'] = artist_details.image_link
  artist_shows_past = db.session.query(Show, Venue).join(Venue).filter(Show.artist_id == artist_id, Show.date <= datetime.datetime.now()).all()
  artist_shows_upcoming = db.session.query(Show, Venue).join(Venue).filter(Show.artist_id == artist_id, Show.date >= datetime.datetime.now()).all()
  data['past_shows'] = [{'venue_id' : venue.venue_id,
                            'venue_name' : venue.name,
                            'venue_image_link' : venue.image_link,
                            'start_time' : show.date }
                            for show, venue in artist_shows_past
                            ] 
  
  data['upcoming_shows'] = [{'venue_id' : venue.venue_id,
                            'venue_name' : venue.name,
                            'venue_image_link' : venue.image_link,
                            'start_time' : show.date }
                            for show, venue in artist_shows_upcoming
                            ] 
  
  data['past_shows_count'] = Show.query.filter(Show.artist_id == artist_id, Show.date <= datetime.datetime.now()).count()
  data['upcoming_shows_count'] = Show.query.filter(Show.artist_id == artist_id, Show.date >= datetime.datetime.now()).count()
  return render_template('pages/show_artist.html', artist=data)



#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  # TODO: populate form with fields from artist with ID <artist_id>
  artist_info = db.session.query(Artist).get(artist_id)
  artist = {
    'id' : artist_id,
    'name' : artist_info.name,
    'genres' : [genre.genre_id for genre in artist_info.genres],
    'city' : artist_info.city,
    'state' : artist_info.state,
    'phone' : artist_info.phone,
    'website' : artist_info.website_link,
    'facebook_link' : artist_info.facebook_link,
    'seeking_venue' : artist_info.seeking_venue,
    'seeking_description' : artist_info.seeking_venue_desc,
    'image_link' : artist_info.image_link
  }
  form = ArtistForm()
  form.genres.choices =  [(genre.genre_id, genre.name) for genre in Genre.query.all()]
  form.name.data = artist['name']
  form.city.data = artist['city']
  form.genres.data = artist['genres']
  form.state.data = artist['state']
  form.phone.data = artist['phone']
  form.website_link.data = artist['website']
  form.image_link.data = artist['image_link']
  form.facebook_link.data = artist['facebook_link']
  form.seeking_venue.data = artist['seeking_venue']
  form.seeking_description.data = artist['seeking_description']
  
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  form = ArtistForm(request.form)
  form.genres.choices =  [(genre.genre_id, genre.name) for genre in Genre.query.all()]
  artist_info = db.session.query(Artist).get(artist_id)
  artist = {
    'id' : artist_id,
    'name' : artist_info.name,
    'genres' : [genre.genre_id for genre in artist_info.genres],
    'city' : artist_info.city,
    'state' : artist_info.state,
    'phone' : artist_info.phone,
    'website' : artist_info.website_link,
    'facebook_link' : artist_info.facebook_link,
    'seeking_venue' : artist_info.seeking_venue,
    'seeking_description' : artist_info.seeking_venue_desc,
    'image_link' : artist_info.image_link
  }
  if form.validate():
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    phone = request.form.get('phone', None)
    genres = request.form.getlist('genres')
    image_link = request.form['image_link']
    facebook_link = request.form.get('facebook_link', None)
    website_link = request.form.get('website_link', None)
    seeking_venue = request.form.get('seeking_venue', None)
    if seeking_venue == 'y':
      seeking_venue = True
    else:
      seeking_venue = False
    seeking_description = request.form.get('seeking_description', None)
    
    # artist record with ID <artist_id> using the new attributes

    #getting Artist record with artist_id provided

    artist_record = Artist.query.get(artist_id)

    # updating records
    artist_record.name = name
    artist_record.city = city
    artist_record.state = state
    artist_record.phone = phone
    artist_record.image_link = image_link
    artist_record.facebook_link = facebook_link
    artist_record.website_link = website_link
    artist_record.seeking_venue = seeking_venue
    artist_record.seeking_venue_desc = seeking_description

    # remove existing records of genres list to update with new ones
    artist_record.genres.clear()
    for genre in genres:
      genre_obj = db.session.query(Genre).filter(Genre.genre_id == genre).first()
      artist_record.genres.append(genre_obj)

    try: 
      db.session.add(artist_record)
      db.session.commit()
      flash('Artist ' + request.form['name'] + ' successfully updated.')
    except:
      error = True
      db.session.rollback()
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated.')
    finally:
      db.session.close()
    return redirect(url_for('show_artist', artist_id=artist_id))
  
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  # TODO: populate form with values from venue with ID <venue_id>

  form = VenueForm()
  venue_info = db.session.query(Venue).get(venue_id)
  venue = {
    'id' : venue_id,
    'name' : venue_info.name,
    'genres' : [genre.genre_id for genre in venue_info.genres],
    'address' : venue_info.address,
    'city' : venue_info.city,
    'state' : venue_info.state,
    'phone' : venue_info.phone,
    'website' : venue_info.website_link,
    'facebook_link' : venue_info.facebook_link,
    'seeking_talent' : venue_info.seeking_talent,
    'seeking_description' : venue_info.seeking_talent_desc,
    'image_link' : venue_info.image_link
  }
  form.genres.choices =  [(genre.genre_id, genre.name) for genre in Genre.query.all()]
  form.name.data = venue['name']
  form.city.data = venue['city']
  form.address.data = venue['address']
  form.genres.data = venue['genres']
  form.state.data = venue['state']
  form.phone.data = venue['phone']
  form.website_link.data = venue['website']
  form.image_link.data = venue['image_link']
  form.facebook_link.data = venue['facebook_link']
  form.seeking_talent.data = venue['seeking_talent']
  form.seeking_description.data = venue['seeking_description']
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  form = VenueForm(request.form)
  form.genres.choices =  [(genre.genre_id, genre.name) for genre in Genre.query.all()]
  venue_info = db.session.query(Venue).get(venue_id)
  venue = {
    'id' : venue_id,
    'name' : venue_info.name,
    'genres' : [genre.genre_id for genre in venue_info.genres],
    'address' : venue_info.address,
    'city' : venue_info.city,
    'state' : venue_info.state,
    'phone' : venue_info.phone,
    'website' : venue_info.website_link,
    'facebook_link' : venue_info.facebook_link,
    'seeking_talent' : venue_info.seeking_talent,
    'seeking_description' : venue_info.seeking_talent_desc,
    'image_link' : venue_info.image_link
  }
  if form.validate():
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    address = request.form['address']
    phone = request.form.get('phone', None)
    genres = request.form.getlist('genres')
    image_link = request.form['image_link']
    facebook_link = request.form.get('facebook_link', None)
    website_link = request.form.get('website_link', None)
    seeking_talent = request.form.get('seeking_talent', None)
    if seeking_talent == 'y':
      seeking_talent = True
    else:
      seeking_talent = False
    seeking_description = request.form.get('seeking_description', None)

    # venue record with ID <venue_id> using the new attributes

    #getting venue record with venue_id provided

    venue_record = Venue.query.get(venue_id)

    # updating records
    venue_record.name = name
    venue_record.city = city
    venue_record.state = state
    venue_record.address = address
    venue_record.phone = phone
    venue_record.image_link = image_link
    venue_record.facebook_link = facebook_link
    venue_record.website_link = website_link
    venue_record.seeking_talent = seeking_talent
    venue_record.seeking_talent_desc = seeking_description

    # remove existing records of genres list to update with new ones
    venue_record.genres.clear()
    for genre in genres:
      genre_obj = db.session.query(Genre).filter(Genre.genre_id == genre).first()
      venue_record.genres.append(genre_obj)
    
    try: 
      db.session.add(venue_record)
      db.session.commit()
      flash('Venue ' + request.form['name'] + ' successfully updated.')
    except:
      error = True
      db.session.rollback()
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated.')
    finally:
      db.session.close()
    return redirect(url_for('show_venue', venue_id=venue_id))

  return render_template('forms/edit_venue.html', form=form, venue=venue)
  

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  form.genres.choices =  [(genre.genre_id, genre.name) for genre in Genre.query.all()]
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Artist record in the db, instead
  form = ArtistForm(request.form)
  form.genres.choices =  [(genre.genre_id, genre.name) for genre in Genre.query.all()]
  
  if form.validate():
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    phone = request.form.get('phone', None)
    genres = request.form.getlist('genres')
    image_link = request.form['image_link']
    facebook_link = request.form.get('facebook_link', None)
    website_link = request.form.get('website_link', None)
    seeking_venue = request.form.get('seeking_venue', None)
    if seeking_venue == 'y':
      seeking_venue = True
    else:
      seeking_venue = False
    seeking_description = request.form.get('seeking_description', None)

    artist_record = Artist(name=name, city=city, state=state, phone=phone, image_link=image_link, facebook_link=facebook_link, website_link=website_link, seeking_venue=seeking_venue, seeking_venue_desc=seeking_description)

    for genre in genres:
      genre_obj = db.session.query(Genre).filter(Genre.genre_id == genre).first()
      artist_record.genres.append(genre_obj)
    try:
      db.session.add(artist_record)
      db.session.commit()
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
      error = True
      db.session.rollback()
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
      
    finally:
      db.session.close()
    return render_template('pages/home.html')

  return render_template('forms/new_artist.html', form=form)
  # TODO: modify data to be the data object returned from db insertion
  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.

  shows = db.session.query(Show, Venue, Artist).select_from(Show).join(Venue).join(Artist)
  data = [ {'venue_id' : venue.venue_id,
             'venue_name' : venue.name,
             'artist_id' : artist.artist_id,
             'artist_name': artist.name,
             'artist_image_link' : artist.image_link,
             'start_time' : show.date
            }
            for show, venue, artist in shows
            ]
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
  form = ShowForm(request.form)
  if form.validate():
    artist_id = request.form.get('artist_id')
    venue_id = request.form.get('venue_id')
    start_time = request.form['start_time']

    show_record = Show(artist_id=artist_id, venue_id=venue_id, date=start_time)
    try:
      db.session.add(show_record)
      db.session.commit()
      flash('Show was successfully listed!')
    except:
      error = True
      db.session.rollback()
      flash('Error, please try again.')
    finally:
      db.session.close()
    return render_template('pages/home.html')

  # on successful db insert, flash success
  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('forms/new_show.html', form=form)

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
    app.debug = True
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
