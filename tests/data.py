# -*- coding: utf-8 -*-
"""
   Test data for tests
"""


genre_1 = {"genre_name": "Боевик"}
genre_2 = {"genre_name": "Комедия"}
genre_fail = {"genre_name": ""}


director_1 = {"first_name": "Джон", "last_name": "Ландау", "age": 30}
director_2 = {"first_name": "Джон_Update", "last_name": "Ландау_Update", "age": 40}
director_fail = {"first_name": "", "last_name": "", "age": 0}

director_errors = ["Length first name should be between 3 and 100 characters",
                   "Length last name should be between 3 and 100 characters",
                   "The age should be more than 17"]


film_1 = {"film_title": "Аватар",
          "release_date": "2009-07-23",
          "description": "Аватар",
          "rate": 9.0,
          "poster": "www.google.com",
          "directors": [director_1],
          "genres": [genre_1]
          }


film_2 = {"film_title": "Аватар1",
          "release_date": "2009-07-24",
          "description": "Аватар1",
          "rate": 10.0,
          "poster": "www.google.com",
          "directors": [director_2],
          "genres": [genre_2]
          }

film_3 = {"film_title": "Железный человек 3",
          "release_date": "2009-07-24",
          "description": "Железный человек 3",
          "rate": 8.0,
          "poster": "www.google.com",
          "directors": [director_2],
          "genres": [genre_2]
          }

film_4 = {"film_title": "Миньйоны",
          "release_date": "2019-07-24",
          "description": "Миньйоны",
          "rate": 8.5,
          "poster": "www.google.com",
          "directors": [director_1],
          "genres": [genre_1]
          }


film_5 = {"film_title": "Аладдин",
          "release_date": "2020-07-24",
          "description": "Аладдин",
          "rate": 9.2,
          "poster": "www.google.com",
          "directors": [director_2],
          "genres": [genre_2]
          }


film_fail = {"film_title": "t",
             "release_date": "1970-01-01",
             "description": "Аватар1",
             "rate": -1.0,
             "poster": "www.google.com",
             "directors": [director_fail],
             "genres": [genre_fail]
             }

film_errors = ["Length film title should be between 3 and 100 characters",
               "Release data should be more than 1971-01-01",
               "Rate should be between 0 and 10",
               "Length should be between 3 and 100 characters",
               "Length first name should be between 3 and 100 characters",
               "Length last name should be between 3 and 100 characters",
               "The age should be more than 17"]

user_1 = {"first_name": "Ilya",
          "last_name": "Troshchynskyi",
          "age": 27,
          "email": "test2@mail.ru",
          "password": "Test11111",
          "is_admin": True
          }

user_2 = {"first_name": "Ilya_Update",
          "last_name": "Troshchynskyi_Update",
          "age": 28,
          "email": "test3@mail.ru",
          "password": "Test11111",
          "is_admin": False
          }


user_fail = {"first_name": "11",
             "last_name": "T",
             "age": 10,
             "email": "test3ail.ru",
             "password": "est",
             "is_admin": "r"
             }


user_errors = ["Length first name should be between 3 and 100 characters",
               "The first name should be string",
               "Length last name should be between 3 and 100 characters",
               "The age should be more than 11", "Invalid email",
               "Make sure your password is at lest 8 letters, has a number in it,"
               " has a capital letter in it"]
