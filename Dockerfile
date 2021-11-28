FROM python:3.8

# set work directory
WORKDIR /app


# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv
RUN pipenv install --system --ignore-pipfile

EXPOSE 8000

# copy project
COPY . .

CMD ["gunicorn", "-b 0.0.0.0:8000", "-w 4", "app:app"]