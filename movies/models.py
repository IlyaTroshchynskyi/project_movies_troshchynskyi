from movies import db


films_genres = db.Table('films_genres',
                        db.Column('film_id', db.Integer, db.ForeignKey('films.film_id'),
                                  primary_key=True),
                        db.Column('genre_id', db.Integer, db.ForeignKey('genres.genre_id'),
                                  primary_key=True))

films_directors = db.Table('films_directors',
                           db.Column('film_id', db.Integer, db.ForeignKey('films.film_id'),
                                     primary_key=True),
                           db.Column('director_id', db.Integer,
                                     db.ForeignKey('directors.director_id',
                                                   ondelete="SET DEFAULT"), default='unknown',
                                     primary_key=True))


class Films(db.Model):
    """Table for saving films which have been added by users. Has relationships
        with table users many-to-one
    """

    film_id = db.Column(db.Integer, primary_key=True)
    film_title = db.Column(db.String(100), nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=True)
    rate = db.Column(db.Float)
    poster = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    directors = db.relationship('Directors', secondary=films_directors,
                                backref=db.backref('films', lazy='dynamic'))
    genres = db.relationship('Genres', secondary=films_genres,
                             backref=db.backref('films', lazy='dynamic'))

    def __repr__(self):
        return f'Film: id:{self.film_id}, {self.film_title}, rd:{self.release_date},' \
               f' rate: {self.rate}'


class Users(db.Model):
    """
    Table for saving users who has registered. Has relationships
    with table films one-to-many
    """
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    films = db.relationship('Films', backref='users', lazy=True)

    def __repr__(self):
        return f'User: id: {self.user_id}, first_name:{self.first_name}, is_admin: {self.is_admin}'


class Directors(db.Model):
    """
    Table for saving directors. Has relationships
    with table films many-to-many
    """

    director_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'Directors: id: {self.director_id}, first_name:{self.first_name}'


class Genres(db.Model):
    """
    Table for saving Genres. Has relationships
    with table films many-to-many
    """
    genre_id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'Genres: id: {self.genre_id}, genre_name:{self.genre_name}'
