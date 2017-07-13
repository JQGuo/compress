import os
import math
import random
import redis
from flask import Flask, render_template, request, jsonify, redirect, flash, url_for

# App setup
random.seed()

app = Flask(__name__)
# Used by Flask to flash error message, relies on cookies
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'not really secret')

EXPIRY_SEC = 2592000 # 30 days

MAX_SHORTCODE_DIGITS = 5 # keep RAND_MAX within int range
RAND_MAX = math.pow( 62, MAX_SHORTCODE_DIGITS ) # 62 unique characters [A-Za-z0-9]

REDIS_URL = os.environ.get('REDIS_URL')

r = None

if not REDIS_URL:
    r = redis.Redis(decode_responses=True)
    app.debug = True
else:
    r = redis.from_url(REDIS_URL, decode_responses=True)
    app.debug = False


@app.route('/')
def index():
    return render_template('index.html')


# generate up to a 5 digit shortcode using [A-Za-z0-9]
def gen_shortcode():
    code = ''
    base = random.randint(0, RAND_MAX)

    digits = []
    while base > 0:
        digits.append(base % 62)
        base //= 62

    while digits:
        digit = digits.pop()
        if digit < 26:
            code += chr(ord('A') + digit)
        elif digit < 52:
            code += chr(ord('a') + digit - 26)
        else:
            code += chr(ord('0') + digit - 52)

    return code


# generate and display shortcode for the url requested
@app.route('/generate/')
def generate():
    long_url = request.args.get('url')

    # redirect won't work unless you have the scheme
    if not long_url.startswith('http'):
        long_url = 'http://' + long_url

    short_url = r.get('l__%s' % (long_url) )

    # site has not been mapped
    if not short_url:
        short_url = gen_shortcode()
        while r.get( 's__%s' % (short_url) ):
            short_url = gen_shortcode()

        # create mapping in both directions
        r.set( 's__%s' % (short_url), long_url, ex=2592000 ) 
        r.set( 'l__%s' % (long_url), short_url, ex=2592000 )

    return jsonify(shortURL=short_url)


# use flask redirect if shortcode exists
@app.route('/url/<url_id>')
def reroute(url_id):
    long_url = r.get('s__%s' % url_id)
    if not long_url:
        flash('This shortcode (%s) is not in the system!' % (url_id))
        return redirect(url_for('index'))
    else:
        return redirect(long_url, code=302)


if __name__ == '__main__':
    app.run()

