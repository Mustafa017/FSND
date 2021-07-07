from .models import db

# Association object (This table only contains columns which reference the two
# sides of the relationship plus an additional column) e.g Show Table


class Show(db.Model):
    __tablename__ = 'Show'
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'Artist.id'), primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey(
        'Venue.id'), primary_key=True)
    start_time = db.Column(db.String(250), primary_key=True)
    artist = db.relationship(
        'Artist', backref=db.backref('show', cascade="all, delete-orphan", lazy=True))
    venue = db.relationship(
        'Venue', backref=db.backref('show', cascade="all, delete-orphan", lazy=True))

    def __repr__(self):
        return f'<Show: Artist={self.artist_id} venue={self.venue_id} start={self.start_time}>'
