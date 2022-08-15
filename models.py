from app import db

venues_genres = db.Table('venues_genres',
    db.Column('venue_id', db.Integer, db.ForeignKey('venues.venue_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genres.genre_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
)

artists_genres = db.Table('artists_genres',
    db.Column('artist_id', db.Integer, db.ForeignKey('artists.artist_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genres.genre_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
)

class Venue(db.Model):
    __tablename__ = 'venues'

    venue_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.relationship('Genre', secondary=venues_genres, backref='venues', lazy='select')
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_talent_desc = db.Column(db.String(500))


    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artists'

    artist_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.relationship('Genre', secondary=artists_genres, backref='artists', lazy='select')
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_venue_desc = db.Column(db.String(500))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Genre(db.Model):
    __tablename__ = 'genres'
    genre_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)


class Show(db.Model):
    __tablename__ = 'shows'
    show_id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.artist_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.venue_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.