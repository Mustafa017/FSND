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
