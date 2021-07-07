from .models import db, venue_genres, artist_genres


class Genre(db.Model):
    __tablename__ = 'Genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    venues = db.relationship(
        'Venue', secondary=venue_genres, backref=db.backref('genres', lazy=True))
    artists = db.relationship(
        'Artist', secondary=artist_genres, backref=db.backref('genres', lazy=True))

    def __repr__(self):
        return f'{self.name}'
