# Compress

## Summary

Compress is a simple URL shortener which uses Python Flask and Redis. It is a small web app that is easy to understand. The Python, Javascript, HTML, and CSS are each under 100 lines of code.

You can see a live demo on https://cmprs.herokuapp.com/.

Originally, the code was only meant to be run locally, but was modified so as to be a hosted service on Heroku. Parts of the code which deal with seemingly random environment variable names are used to differentiate between "production" and "local" execution.

## Local Setup

1. Install Python 3
2. Install pip
3. Run `pip install virtualenvwrapper`
4. Install redis-server
5. Create a virtual environment with virtualenvwrapper and enter it using `workon VENV_NAME`
6. Run `pip install -r requirements.txt` to install required python packages
7. Run `python3 compress.py`
8. Go to localhost:5000

## Design

This is a very basic design which will attempt to generate uniformly random keys to map short codes to user supplied URLs. It has to check all keys for possible collisions, because unlike UUIDs, the goal is for the keys to be shorter (making the probability of collisions higher). The app naively generates keys until one is free, which assumes that usage will be balanced out by the expiry time. If usage is oversaturated, this will cause the backend to freeze up. It doesn't really matter because this is a toy webapp.

It's also not possible to prevent a third-party from finding your codes because they are meant to be public to be easily sharable. One idea would be to allow the user to provide an optional password along with the URL when making a shortened URL, and having consumers save this password in cookies or local storage when accessing them. But this makes it cumbersome to use.

Lastly, since analytics comes in every piece of software these days, URL shorteners tend to offer time-series data on when links were clicked, what websites users came from, and what country they are from etc. At the moment, this webapp just shortens URLs for you.

