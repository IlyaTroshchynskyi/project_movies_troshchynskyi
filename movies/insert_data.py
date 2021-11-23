from datetime import date
from movies import db
from movies.models import Films, Users, Directors, Genres


def populate_db():
    user = Users(first_name="Ilya", last_name="Troshchynskyi", age=27, email="test2@mail.ru",
                 password="Test11111", is_admin=True)

    db.session.add(user)
    db.session.commit()

    genre_1 = Genres(genre_name='Боевик')
    genre_2 = Genres(genre_name='Вестерн')
    genre_3 = Genres(genre_name='Детектив')
    genre_4 = Genres(genre_name='Драма')
    genre_5 = Genres(genre_name='Комедия')
    genre_6 = Genres(genre_name='Мелодрама')
    genre_7 = Genres(genre_name='Сказка')
    genre_8 = Genres(genre_name='Трагедия')
    genre_9 = Genres(genre_name='Триллер')
    genre_10 = Genres(genre_name='Ужасы')

    db.session.add(genre_1)
    db.session.add(genre_2)
    db.session.add(genre_3)
    db.session.add(genre_4)
    db.session.add(genre_5)
    db.session.add(genre_6)
    db.session.add(genre_7)
    db.session.add(genre_8)
    db.session.add(genre_9)
    db.session.add(genre_10)
    db.session.commit()

    directors_1 = Directors(first_name='Джеймс', last_name='Кэмерон', age=40)
    directors_2 = Directors(first_name='Джон', last_name='Ландау', age=40)
    directors_3 = Directors(first_name='Нил', last_name='Х.Мориц', age=40)
    directors_4 = Directors(first_name='Вин', last_name='Дизель', age=40)
    directors_5 = Directors(first_name='Брэдли', last_name='Купер', age=40)
    directors_6 = Directors(first_name='Тодд', last_name='Филлипс', age=40)
    directors_7 = Directors(first_name='Аарон', last_name='Уорнер', age=40)
    directors_8 = Directors(first_name='Саймон', last_name='Кинберг', age=40)
    directors_9 = Directors(first_name='Джеффри', last_name='Сильвер', age=40)
    directors_10 = Directors(first_name='Кевин', last_name='Файги', age=40)
    directors_11 = Directors(first_name='Крис', last_name='Меледандри', age=40)
    directors_12 = Directors(first_name='Джанет', last_name='Хили', age=40)
    directors_13 = Directors(first_name='Дэн', last_name='Лин', age=40)

    db.session.add(directors_1)
    db.session.add(directors_2)
    db.session.add(directors_3)
    db.session.add(directors_4)
    db.session.add(directors_5)
    db.session.add(directors_6)
    db.session.add(directors_7)
    db.session.add(directors_8)
    db.session.add(directors_9)
    db.session.add(directors_10)
    db.session.add(directors_11)
    db.session.add(directors_12)
    db.session.add(directors_13)
    db.session.commit()

    film_1 = Films(film_title='Аватар', user_id=1, release_date=date(2009, 7, 23), rate=9,
                   poster='https://ru.wikipedia.org/wiki/%D0%90%D0%B2%D0%B0%D1%82%D0%B0%D1%80'
                          '_(%D1%84%D0%B8%D0%BB%D1%8C%D0%BC,_2009)#/media/%D0%A4%D0%B0%D0%B9%D0%BB:'
                          'Avatar-2009.jpg')
    film_1.genres = [genre_1]
    film_1.directors = [directors_1, directors_2]

    film_2 = Films(film_title='Титаник', user_id=1, release_date=date(1997, 7, 23), rate=9.7,
                 poster='https://ru.wikipedia.org/wiki/%D0%A2%D0%B8%D1%82%D0%B0%D0%BD%D0%B8%D0%BA_'
                        '(%D1%84%D0%B8%D0%BB%D1%8C%D0%BC,_1997)#/media/%D0%A4%D0%B0%D0%B9%D0%BB:'
                        'Titanic_(Official_Film_Poster).png')
    film_2.genres = [genre_1]
    film_2.directors = [directors_1, directors_2]

    film_3 = Films(film_title='Форсаж 7', user_id=1, release_date=date(2015, 7, 23), rate=9.2,
                 poster='https://ru.wikipedia.org/wiki/%D0%A4%D0%BE%D1%80%D1%81%D0%B0%D0%B6_7#'
                        '/media/%D0%A4%D0%B0%D0%B9%D0%BB:Furious_7.jpg')
    film_3.genres = [genre_1]
    film_3.directors = [directors_3, directors_4]

    film_4 = Films(film_title='Джокер', user_id=1, release_date=date(2019, 7, 23), rate=9.9,
                 poster='https://ru.wikipedia.org/wiki/%D0%94%D0%B6%D0%BE%D0%BA%D0%B5%D1%80_'
                        '(%D1%84%D0%B8%D0%BB%D1%8C%D0%BC,_2019)#/media/%D0%A4%D0%B0%D0%B9%D0%BB:'
                        '%D0%94%D0%B6%D0%BE%D0%BA%D0%B5%D1%80_(%D1%84%D0%B8%D0%BB%D1%8C%D0%BC_'
                        '%D0%A2%D0%BE%D0%B4%D0%B4%D0%B0_%D0%A4%D0%B8%D0%BB%D0%BB%D0%B8%D0%BF%D1%81%D0%B0).jpg')
    film_4.genres = [genre_1]
    film_4.directors = [directors_5, directors_6]

    film_5 = Films(film_title='Шрек 2', user_id=1, release_date=date(2004, 7, 23), rate=9.1,
                   poster='https://ru.wikipedia.org/wiki/%D0%A8%D1%80%D0%B5%D0%BA_2#/media/'
                          '%D0%A4%D0%B0%D0%B9%D0%BB:Shrek_2.jpg')
    film_5.genres = [genre_1]
    film_5.directors = [directors_7]

    film_6 = Films(film_title='Дедпул 2', user_id=1, release_date=date(2018, 7, 23), rate=8.7,
                   poster='https://ru.wikipedia.org/wiki/%D0%94%D1%8D%D0%B4%D0%BF%D1%83%D0%BB_2#/'
                          'media/%D0%A4%D0%B0%D0%B9%D0%BB:Deadpool_2_poster.jpg')

    film_6.genres = [genre_1]
    film_6.directors = [directors_8]

    film_7 = Films(film_title='Король Лев', user_id=1, release_date=date(2019, 7, 23), rate=9,
                   poster='https://ru.wikipedia.org/wiki/%D0%9A%D0%BE%D1%80%D0%BE%D0%BB%D1%8C_'
                          '%D0%9B%D0%B5%D0%B2_(%D0%BC%D1%83%D0%BB%D1%8C%D1%82%D1%84%D0%B8%D0%BB%D1%8C%D0%BC,'
                          '_2019)#/media/%D0%A4%D0%B0%D0%B9%D0%BB:'
                          '%D0%9A%D0%BE%D1%80%D0%BE%D0%BB%D1%8C_%D0%9B%D0%B5%D0%B2.jpg')
    film_7.genres = [genre_1]
    film_7.directors = [directors_9]

    film_8 = Films(film_title='Железный человек 3', user_id=1, release_date=date(2013, 7, 23), rate=9.5,
                   poster='https://ru.wikipedia.org/wiki/%D0%96%D0%B5%D0%BB%D0%B5%D0%B7%D0%BD%D1%8B%D0%B9_'
                          '%D1%87%D0%B5%D0%BB%D0%BE%D0%B2%D0%B5%D0%BA_3#/media/%D0%A4%D0%B0%D0%B9%D0%BB:'
                          'Iron_Man_3.jpg')
    film_8.genres = [genre_2]
    film_8.directors = [directors_10]

    film_9 = Films(film_title='Миньйоны', user_id=1, release_date=date(2015, 7, 23), rate=8.6,
                   poster='https://ru.wikipedia.org/wiki/%D0%9C%D0%B8%D0%BD%D1%8C%D0%BE%D0%BD%D1%8B_'
                          '(%D0%BC%D1%83%D0%BB%D1%8C%D1%82%D1%84%D0%B8%D0%BB%D1%8C%D0%BC)#'
                          '/media/%D0%A4%D0%B0%D0%B9%D0%BB:%D0%9C%D0%B8%D0%BD%D1%8C%D0%BE%D0%BD%D1%8B_'
                          '(%D0%BF%D0%BE%D1%81%D1%82%D0%B5%D1%80).jpg')
    film_9.genres = [genre_2, genre_5]
    film_9.directors = [directors_11, directors_12]

    film_10 = Films(film_title='Аладдин', user_id=1, release_date=date(2019, 7, 23), rate=9,
                    poster='https://ru.wikipedia.org/wiki/%D0%90%D0%BB%D0%B0%D0%B4%D0%B4%D0%B8%D0%BD_'
                           '(%D1%84%D0%B8%D0%BB%D1%8C%D0%BC,_2019)#/media/%D0%A4%D0%B0%D0%B9%D0%BB:'
                           '%D0%9F%D0%BE%D1%81%D1%82%D0%B5%D1%80_%D1%84%D0%B8%D0%BB%D1%8C%D0%BC%D0%B0_'
                           '%C2%AB%D0%90%D0%BB%D0%B0%D0%B4%D0%B4%D0%B8%D0%BD%C2%BB.jpg')
    film_10.genres = [genre_2, genre_4]
    film_10.directors = [directors_1, directors_13]

    film_11 = Films(film_title='Аквамен', user_id=1, release_date=date(2018, 7, 23), rate=8.9,
                    poster='https://ru.wikipedia.org/wiki/%D0%90%D0%BA%D0%B2%D0%B0%D0%BC%D0%B5%D0%BD_'
                           '(%D1%84%D0%B8%D0%BB%D1%8C%D0%BC)#/media/%D0%A4%D0%B0%D0%B9%D0%BB:'
                           '%D0%90%D0%BA%D0%B2%D0%B0%D0%BC%D0%B5%D0%BD.jpg')
    film_11.genres = [genre_2]
    film_11.directors = [directors_11]

    film_12 = Films(film_title='Гарри Поттер и философский камень', user_id=1,
                    release_date=date(2001, 7, 23), rate=9.1,
                    poster="https://ru.wikipedia.org/wiki/%D0%93%D0%B0%D1%80%D1%80%D0%B8_"
                           "%D0%9F%D0%BE%D1%82%D1%82%D0%B5%D1%80_%D0%B8_%D1%84%D0%B8%D0%BB%"
                           "D0%BE%D1%81%D0%BE%D1%84%D1%81%D0%BA%D0%B8%D0%B9_%D0%BA%D0%B0%D0%"
                           "BC%D0%B5%D0%BD%D1%8C_(%D1%84%D0%B8%D0%BB%D1%8C%D0%BC)#/media/%D0%A4%D0%B0%D0%"
                           "B9%D0%BB:Harry_Potter_and_the_Philosopher's_Stone_%E2%80%94_movie.jpg")
    film_12.genres = [genre_2]
    film_12.directors = [directors_7]

    db.session.add(film_1)
    db.session.add(film_2)
    db.session.add(film_3)
    db.session.add(film_4)
    db.session.add(film_5)
    db.session.add(film_6)
    db.session.add(film_7)
    db.session.add(film_8)
    db.session.add(film_9)
    db.session.add(film_10)
    db.session.add(film_11)
    db.session.add(film_12)
    db.session.commit()


if __name__ == '__main__':

    print('Populate db')
    populate_db()
    print('Successfully populated')