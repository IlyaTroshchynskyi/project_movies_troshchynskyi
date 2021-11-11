def parse_films_json_data(data):
    film_title = data.get('film_title')
    release_date = data.get('release_date')
    description = data.get('description')
    rate = data.get('rate')
    poster = data.get('poster')
    input_ = {"film_title": film_title, 'release_date': release_date, "description": description,
              "rate": rate, "poster": poster}
    return input_