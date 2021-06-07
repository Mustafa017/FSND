from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# DONE Implement Show and Artist models, and complete all model relationships
# and properties, as a database migration.

# Table objects (These table only contains columns which reference the two
# sides of the relationship) there are no extra columns e.g Venue_genres and
# Artist_genres
venue_genres = db.Table('Venue_genres',
                        db.Column('venue_id', db.Integer,
                                  db.ForeignKey('Venue.id'), primary_key=True),
                        db.Column('genre_id', db.Integer,
                                  db.ForeignKey('Genre.id'), primary_key=True))

artist_genres = db.Table('Artist_genres',
                         db.Column('genre_id', db.Integer,
                                   db.ForeignKey('Genre.id'), primary_key=True),
                         db.Column('artist_id', db.Integer,
                                   db.ForeignKey('Artist.id'), primary_key=True))

# Association object (This table only contains columns which reference the two
# sides of the relationship plus an additional column) e.g Show Table


class Show(db.Model):
    __tablename__ = 'Show'
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'Artist.id'), primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey(
        'Venue.id'), primary_key=True)
    start_time = db.Column(db.String(250), primary_key=True)

    def __repr__(self):
        return f'<Show: Artist={self.artist_id} venue={self.venue_id} start={self.start_time}>'


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=True)
    seeking_description = db.Column(db.String(120))

    def __repr__(self):
        return f'<Venue {self.id}: {self.name}>'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=False, default=True)
    seeking_description = db.Column(db.String(120))
    venues = db.relationship('Venue', secondary=Show.__table__,
                             backref=db.backref('artists', lazy=True))

    def __repr__(self):
        return f'<Artist {self.id}: {self.name}>'
    # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Genre(db.Model):
    __tablename__ = 'Genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    venues = db.relationship(
        'Venue', secondary=venue_genres, backref=db.backref('genres', lazy=True))
    artists = db.relationship(
        'Artist', secondary=artist_genres, backref=db.backref('genres', lazy=True))

    def __repr__(self):
        return f'<Genre {self.id}: {self.name}>'
