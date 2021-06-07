# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

from models import Venue, Artist, Show, Genre, artist_genres, venue_genres, db
from flask_migrate import Migrate
from forms import *
from flask_wtf import Form
from logging import Formatter, FileHandler
import logging
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash,\
    redirect, url_for, abort
# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
# db = SQLAlchemy(app)
# use same instance of the db found in models.py
db.init_app(app)
migrate = Migrate(app, db)
# DONE: connect to a local postgresql database

# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime

# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')

# ----------------------------------------------------------------------------#
#  Venues
# ----------------------------------------------------------------------------#


@app.route('/venues')
def venues():
    # Done: replace with real venues data.
    # num_shows should be aggregated based on number of
    # upcoming shows per venue.

    locations = db.session.query(func.count(Venue.id), Venue.city,
                                 Venue.state).group_by(Venue.city,
                                                       Venue.state).all()

    data = []
    for location in locations:
        city = location.city
        state = location.state
        cityVenues = db.session.query(Venue.id, Venue.name).filter(
            Venue.city == city, Venue.state == state).all()

        venue = []
        for cityVenue in cityVenues:
            ven_name = cityVenue.name
            ven_id = cityVenue.id

            ven_shows = upcoming_shows_by_venue(ven_id)
            venue.append({
                "id": ven_id,
                "name": ven_name,
                "num_upcoming_shows": len(ven_shows)
            })
        data.append({
            "city": city,
            "state": state,
            "venues": venue
        })
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search.
    # Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and
    # "Park Square Live Music & Coffee"
    response = {
        "count": 1,
        "data": [{
            "id": 2,
            "name": "The Dueling Pianos Bar",
            "num_upcoming_shows": 0,
        }]
    }
    return render_template('pages/search_venues.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # DONE: replace with real venue data from the venues table, using venue_id
    venue_details = db.session.query(Venue).filter(Venue.id == venue_id).all()
    upcoming_shows = upcoming_shows_by_venue(venue_id)
    past_shows = past_shows_by_venue(venue_id)
    genres = get_genre_by_venue(venue_id)
    next_shows = []
    prev_shows = []
    genre_list = []
    for show_artist in upcoming_shows:
        next_shows.append({
            "artist_id": show_artist.id,
            "artist_name": show_artist.name,
            "artist_image_link": show_artist.image_link,
            "start_time": show_artist.start_time
        })

    for past_artist in past_shows:
        prev_shows.append({
            "artist_id": past_artist.id,
            "artist_name": past_artist.name,
            "artist_image_link": past_artist.image_link,
            "start_time": past_artist.start_time
        })

    for genre in genres:
        genre_list.append(genre.name)

    for venue_detail in venue_details:
        data = {
            "id": venue_detail.id,
            "name": venue_detail.name,
            "genres": genre_list,
            "address": venue_detail.address,
            "city": venue_detail.city,
            "state": venue_detail.state,
            "phone": venue_detail.phone,
            "website": venue_detail.website,
            "facebook_link": venue_detail.facebook_link,
            "seeking_talent": venue_detail.seeking_talent,
            "seeking_description": venue_detail.seeking_description,
            "image_link": venue_detail.image_link,
            "past_shows": prev_shows,
            "upcoming_shows": next_shows,
            "past_shows_count": len(past_shows),
            "upcoming_shows_count": len(upcoming_shows),
        }
    return render_template('pages/show_venue.html', venue=data)


def upcoming_shows_by_venue(venue_id):
    return db.session.query(Show.start_time, Artist.id, Artist.name,
                            Artist.image_link).\
        join(Artist, Artist.id == Show.artist_id).\
        join(Venue, Venue.id == Show.venue_id).\
        filter((Show.venue_id == venue_id) & (
            Show.start_time >= str(datetime.now()))).all()


def past_shows_by_venue(venue_id):
    return db.session.query(Show.start_time, Artist.id, Artist.name,
                            Artist.image_link).\
        join(Artist, Artist.id == Show.artist_id).\
        join(Venue, Venue.id == Show.venue_id).\
        filter((Show.venue_id == venue_id) & (
            Show.start_time < str(datetime.now()))).all()


def get_genre_by_venue(venue_id):
    return db.session.query(venue_genres, Genre.name).\
        join(Venue, venue_genres.c.venue_id == Venue.id).\
        join(Genre, venue_genres.c.genre_id == Genre.id).\
        filter(venue_genres.c.venue_id == venue_id).all()


def upcoming_shows_by_artist(artist_id):
    return db.session.query(Show.start_time, Venue.id, Venue.name,
                            Venue.image_link).\
        join(Artist, Artist.id == Show.artist_id).\
        join(Venue, Venue.id == Show.venue_id).\
        filter((Show.artist_id == artist_id) & (
            Show.start_time >= str(datetime.now()))).all()


def past_shows_by_artist(artist_id):
    return db.session.query(Show.start_time, Artist.id, Artist.name,
                            Artist.image_link).\
        join(Artist, Artist.id == Show.artist_id).\
        join(Venue, Venue.id == Show.venue_id).\
        filter((Show.artist_id == artist_id) & (
            Show.start_time < str(datetime.now()))).all()


def get_genre_by_artist(artist_id):
    return db.session.query(artist_genres, Genre.name).\
        join(Artist, artist_genres.c.artist_id == Artist.id).\
        join(Genre, artist_genres.c.genre_id == Genre.id).\
        filter(artist_genres.c.artist_id == artist_id).all()

# ----------------------------------------------------------------------------#
#  Create Venue
# ----------------------------------------------------------------------------#


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name +
    # ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('city')
    address = request.form.get('address')
    genres = request.form.getlist('genres')
    fb_link = request.form.get('fb_link')
    phone = request.form.get('phone')

    print(genres)
    genre_ids = []
    for genre in genres:
        gen_id = db.session.query(Genre.id).filter(
            Genre.name == genre).one_or_none()
        genre_ids.append(gen_id[0])
    print(genre_ids)

    try:
        if(request.form):
            venue = Venue(name=name, city=city, state=state,
                          address=address, phone=phone, facebook_link=fb_link)
            db.session.add(venue)
            for gen_id in genre_ids:
                # use Identity map to maintains a unique instance of Genre
                venue.genres.append(db.session.get(Genre, gen_id))

            all_venn = db.session.query(Venue).all()
            print(all_venn)
            all_ven_gen = db.session.query(venue_genres).all()
            print(all_ven_gen)
    except:
        db.session.rollback()
        abort(500)

    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session
    # commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page,
    # have it so that clicking that button delete it from the db then redirect
    # the user to the homepage
    return None

# ----------------------------------------------------------------------------#
#  Artists
# ----------------------------------------------------------------------------#


@app.route('/artists')
def artists():
    # DONE: replace with real data returned from querying the database
    data = db.session.query(Artist).all()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search.
    # Ensure it is case-insensitive. Seach for "A" should return
    # "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    response = {
        "count": 1,
        "data": [{
            "id": 4,
            "name": "Guns N Petals",
            "num_upcoming_shows": 0,
        }]
    }
    return render_template('pages/search_artists.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # DONE: replace with real venue data from the venues table, using venue_id
    artist_details = db.session.query(Artist).\
        filter(Artist.id == artist_id).all()
    upcoming_shows = upcoming_shows_by_artist(artist_id)
    past_shows = past_shows_by_artist(artist_id)
    genres = get_genre_by_artist(artist_id)
    next_shows = []
    prev_shows = []
    genre_list = []

    for show_venue in upcoming_shows:
        next_shows.append({
            "venue_id": show_venue.id,
            "venue_name": show_venue.name,
            "venue_image_link": show_venue.image_link,
            "start_time": show_venue.start_time
        })

    for past_venue in past_shows:
        prev_shows.append({
            "venue_id": past_venue.id,
            "venue_name": past_venue.name,
            "venue_image_link": past_venue.image_link,
            "start_time": past_venue.start_time
        })

    for genre in genres:
        genre_list.append(genre.name)

    for artist in artist_details:
        data = {
            "id": artist.id,
            "name": artist.name,
            "genres": genre_list,
            "city": artist.city,
            "state": artist.state,
            "phone": artist.phone,
            "seeking_venue": artist.seeking_venue,
            "seeking_description": artist.seeking_description,
            "image_link": artist.image_link,
            "past_shows": prev_shows,
            "upcoming_shows": next_shows,
            "past_shows_count": len(past_shows),
            "upcoming_shows_count": len(upcoming_shows),
        }
    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = {
        "id": 4,
        "name": "Guns N Petals",
        "genres": ["Rock n Roll"],
        "city": "San Francisco",
        "state": "CA",
        "phone": "326-123-5000",
        "website": "https://www.gunsnpetalsband.com",
        "facebook_link": "https://www.facebook.com/GunsNPetals",
        "seeking_venue": True,
        "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
        "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
    }
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = {
        "id": 1,
        "name": "The Musical Hop",
        "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
        "address": "1015 Folsom Street",
        "city": "San Francisco",
        "state": "CA",
        "phone": "123-123-1234",
        "website": "https://www.themusicalhop.com",
        "facebook_link": "https://www.facebook.com/TheMusicalHop",
        "seeking_talent": True,
        "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
        "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
    }
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    return redirect(url_for('show_venue', venue_id=venue_id))

# ----------------------------------------------------------------------------#
#  Create Artist
# ----------------------------------------------------------------------------#


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')

# ----------------------------------------------------------------------------#
#  Shows
# ----------------------------------------------------------------------------#


@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # DONE: replace with real venues data.
    show_details = db.session.query(Show.start_time, (Artist.id).label("aid"),
                                    (Artist.name).label(
                                        'aname'), Artist.image_link,
                                    (Venue.id).label("vid"), (Venue.name).
                                    label('vname')).\
        join(Artist, Artist.id == Show.artist_id).\
        join(Venue, Venue.id == Show.venue_id).all()
    data = []

    for show_artVenue in show_details:
        data.append({
            "venue_id": show_artVenue.vid,
            "venue_name": show_artVenue.vname,
            "artist_id": show_artVenue.aid,
            "artist_name": show_artVenue.aname,
            "artist_image_link": show_artVenue.image_link,
            "start_time": show_artVenue.start_time
        })
    # return data
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show
    # listing form
    # TODO: insert form data as a new Show record in the db, instead

    # on successful db insert, flash success
    flash('Show was successfully listed!')
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
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(debug=True)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
