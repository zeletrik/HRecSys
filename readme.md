# HRecSys

HRecSys is a cloud-ready, Surprise powered recommendation system for hotels.
Based on K-NN Algorithm.

### Tech


* [Python 3.7](https://www.python.org/) - Lets you work quickly and integrate systems more effectively
* [Surprise](http://surpriselib.com/) - Surprise is a Python scikit building and analyzing recommender systems.
* [Joblib](https://joblib.readthedocs.io) - A replacement for pickle to work efficiently on Python objects containing large data
* [flask](http://flask.pocoo.org/) - Go WEB! Create REST endpoints for the application
* [Docker](https://www.docker.com/) - Enterprise Container Platform for High-Velocity Innovation
* Others like Pandas, NumPy, GeoPy, uWSGI, PyMysql

### Database

For obvious reason the database connection is not provided for the application.
There are two necessary table for it:

*user_hotel_rating*

| user_id | hotel_id | rating |
| ------ | ------ | ------ |
| 12345 | 6731381 | 1 |
| 43256 | 4245612 | 3 |

*hotel_data*

| hotel_id | latitude | longitude | guestRating | score |foodAndDrink | thingsToDo | ... |
| ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| 6731381 | 51.507928 | -0.176664 | 5 | 5 | Full breakfast daily  Restaurant | Outdoor seasonal pool  Golf course on site | ... |
| 4245612 | 32.01234 | 1.123443 | 4.6 | 3 |  Restaurant  Bar/lounge  | Fitness facilities  Full-service spa | ... |

And some more field, representing on the `DatabaseHelper.py` file

### Installation

HRecSys easily runs on [Docker](https://www.docker.com/).
```sh
$ cd HRecSys
$ docker build -t h_recsys .
$ docker run -i -t -p 80:80 h_recsys
```

### Endpoints

There are two endpoint

| URL | Method | Request | Response | Description |
| ------ | ------ | ------ | ------ | ------ |
| /retrain | POST | - | 202 - `{"retrain": done}` or 5XX | Starts a retrain on the model|
| /recommend | POST | `{ "userId": 12345, "coordinate": {"latitude": 51.514889,"longitude": -0.176835}}` | 200 - `{"recommendations": 4245612, ...}` or 5XX | Creats a set for the given location and predict recommendations (max 10)|


