from .models import db
from datetime import datetime


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

    def __init__(self, name, city, state, phone, facebook_link) -> None:
        self.name = name
        self.city = city
        self.state = state
        self.phone = phone
        self.facebook_link = facebook_link

    @property
    def upcoming_shows(self):
        next_shows = []
        for show in self.show:
            if(show.start_time >= str(datetime.now())):
                next_shows.append({
                    "artist_id": self.id,
                    "artist_name": self.name,
                    "artist_image_link": self.image_link,
                    "start_time": show.start_time
                })
        return next_shows

    @property
    def past_shows(self):
        previous_shows = []
        for show in self.show:
            if(show.start_time < str(datetime.now())):
                previous_shows.append({
                    "artist_id": self.id,
                    "artist_name": self.name,
                    "artist_image_link": self.image_link,
                    "start_time": show.start_time
                })
        return previous_shows

    @property
    def short_format(self):
        count = 0
        for show in self.show:
            if(show.start_time >= str(datetime.now())):
                count += 1
        return{
            'id': self.id,
            'name': self.name,
            'num_upcoming_shows': count
        }

    @property
    def long_format(self):
        return{
            'id': self.id,
            'name': self.name,
            'genres': self.genres,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'website': self.website,
            'seeking_description': self.seeking_description
        }

    def __repr__(self):
        return f'<Artist {self.id}: {self.name}>'
