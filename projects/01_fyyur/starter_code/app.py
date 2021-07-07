# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

from re import search

from flask.json import jsonify
from models import Venue, Artist, Show, Genre, artist_genres, venue_genres, db
from flask_migrate import Migrate
from forms import *
from flask_wtf import Form
from logging import Formatter, FileHandler, error
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
            ven_id = cityVenue.id
            venue_obj = db.session.get(Venue, ven_id)
            ven_shows = venue_obj.short_format
            venue.append(ven_shows)
        data.append({
            "city": city,
            "state": state,
            "venues": venue
        })
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # Done: implement search on artists with partial string search.
    # Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and
    # "Park Square Live Music & Coffee"

    response = _search(Venue)

    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # DONE: replace with real venue data from the venues table, using venue_id
    venue_details = db.session.get(Venue, venue_id)

    data = venue_details.long_format
    artists = db.session.query(Show).filter(Show.venue_id == venue_id).all()
    for artist in artists:
        artist_id = artist.artist_id
        artist = db.session.get(Artist, artist_id)
        upcoming_shows = artist.upcoming_shows
        past_shows = artist.past_shows
        data['upcoming_shows'] = upcoming_shows
        data['past_shows'] = past_shows
        data['upcoming_shows_count'] = len(upcoming_shows)
        data['past_shows_count'] = len(past_shows)

    return render_template('pages/show_venue.html', venue=data)


def get_genre_by_artist(artist_id):
    return db.session.query(artist_genres, Genre.name).\
        join(Artist, artist_genres.c.artist_id == Artist.id).\
        join(Genre, artist_genres.c.genre_id == Genre.id).\
        filter(artist_genres.c.artist_id == artist_id).all()


def _search(entity):
    search = request.form.get('search_term', None)

    if(search is None):
        selections = db.session.query(entity).all()
    else:
        selections = db.session.query(entity).filter(
            entity.name.ilike('%{}%'.format(search))).all()

    data = []
    for selection in selections:
        select_id = selection.id
        select_obj = db.session.get(entity, select_id)
        venue_shows = select_obj.short_format
        data.append(venue_shows)

    response = {
        "count": len(selections),
        "data": data
    }
    return response

# ----------------------------------------------------------------------------#
#  Create Venue
# ----------------------------------------------------------------------------#


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # DONE: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

    name = request.form.get('name', None)
    city = request.form.get('city', None)
    state = request.form.get('state', None)
    address = request.form.get('address', None)
    genres = request.form.getlist('genres', None)
    fb_link = request.form.get('fb_link', None)
    phone = request.form.get('phone', None)

    try:
        if(request.form):
            venue = Venue(name=name, city=city, state=state,
                          address=address, phone=phone, facebook_link=fb_link)
            db.session.add(venue)

            for genre in genres:
                genre_id = db.session.query(Genre.id).filter(
                    Genre.name == genre).one_or_none()
                # use Identity map to maintains a unique instance of Genre
                genre_obj = db.session.get(Genre, genre_id)
                venue.genres.append(genre_obj)
            db.session.commit()

            # on successful db insert, flash success
            flash('Venue ' + request.form['name'] +
                  ' was successfully listed!')
        else:
            abort(500)
    except Exception as e:
        print(e)
        db.session.rollback()
        # DONE: on unsuccessful db insert, flash an error instead.
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be listed.')

    return render_template('pages/home.html')


@app.route('/venues/<int:venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session
    # commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page,
    # have it so that clicking that button delete it from the db then redirect
    # the user to the homepage
    error = False

    try:
        selection = db.session.get(Venue, venue_id)
        db.session.delete(selection)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        error = True

    if error:
        abort(500)
    else:
        return jsonify({'success': True})

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
    # Done: implement search on artists with partial string search.
    # Ensure it is case-insensitive. Seach for "A" should return
    # "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".

    response = _search(Artist)
    return render_template('pages/search_artists.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # DONE: replace with real venue data from the venues table, using venue_id
    artist_details = db.session.get(Artist, artist_id)
    data = artist_details.long_format

    for artist in artist_details.show:
        venue_id = artist.venue_id
        venue_obj = db.session.get(Venue, venue_id)
        upcoming_shows = venue_obj.upcoming_shows
        past_shows = venue_obj.past_shows
        data['upcoming_shows'] = upcoming_shows
        data['past_shows'] = past_shows
        data['upcoming_shows_count'] = len(upcoming_shows)
        data['past_shows_count'] = len(past_shows)

    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist = db.session.get(Artist, artist_id)
    genres = [(name, name) for name in artist.genres]

    # DONE: populate form with fields from artist with ID <artist_id>
    form = ArtistForm(obj=artist, data=genres)
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # DONE: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    name = request.form.get('name', None)
    city = request.form.get('city', None)
    state = request.form.get('state', None)
    genres = request.form.getlist('genres', None)
    fb_link = request.form.get('fb_link', None)
    phone = request.form.get('phone', None)

    artist = db.session.get(Artist, artist_id)
    artist.name = name
    artist.city = city
    artist.state = state
    artist.fb_link = fb_link
    artist.phone = phone

    for genre in genres:
        genre_id = db.session.query(Genre.id).filter(
            Genre.name == genre).one_or_none()
        # use Identity map to maintains a unique instance of Genre
        genre_obj = db.session.get(Genre, genre_id)
        artist.genres.append(genre_obj)

    db.session.add(artist)
    db.session.commit()

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue = db.session.get(Venue, venue_id)
    genres = [(name, name) for name in venue.genres]

    # DONE: populate form with values from venue with ID <venue_id>
    form = VenueForm(obj=venue, data=genres)
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # DONE: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    name = request.form.get('name', None)
    city = request.form.get('city', None)
    state = request.form.get('state', None)
    address = request.form.get('address', None)
    genres = request.form.getlist('genres', None)
    fb_link = request.form.get('fb_link', None)
    phone = request.form.get('phone', None)

    venue = db.session.get(Venue, venue_id)
    venue.name = name
    venue.city = city
    venue.state = state
    venue.address = address
    venue.fb_link = fb_link
    venue.phone = phone

    for genre in genres:
        genre_id = db.session.query(Genre.id).filter(
            Genre.name == genre).one_or_none()
        # use Identity map to maintains a unique instance of Genre
        genre_obj = db.session.get(Genre, genre_id)
        venue.genres.append(genre_obj)
    db.session.add(venue)
    db.session.commit()

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
    # DONE: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    name = request.form.get('name', None)
    city = request.form.get('city', None)
    state = request.form.get('state', None)
    genres = request.form.getlist('genres', None)
    fb_link = request.form.get('fb_link', None)
    phone = request.form.get('phone', None)

    try:
        artist = Artist(name, city, state, phone, fb_link)
        db.session.add(artist)

        for genre in genres:
            genre_id = db.session.query(Genre.id).filter(
                Genre.name == genre).one_or_none()
            # use Identity map to maintains a unique instance of Genre
            genre_obj = db.session.get(Genre, genre_id)
            artist.genres.append(genre_obj)

        db.session.commit()
        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except Exception as e:
        print(e)
        # DONE: on unsuccessful db insert, flash an error instead.
        flash('An error occurred. Artist ' +
              request.form['name'] + ' could not be listed.')

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
    # DONE: insert form data as a new Show record in the db, instead

    artist_id = request.form.get('artist_id', None)
    venue_id = request.form.get('venue_id', None)
    start_time = request.form.get('start_time', None)

    try:
        artist = db.session.get(Artist, artist_id)
        venue = db.session.get(Venue, venue_id)
        show = Show(start_time=start_time)
        show.artist = artist
        show.venue = venue
        db.session.add(show)
        db.session.commit()

        # on successful db insert, flash success
        flash('Show was successfully listed!')
    except Exception as e:
        print(e)
        # DONE: on unsuccessful db insert, flash an error instead.
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        flash('An error occurred. Show could not be listed.')

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
