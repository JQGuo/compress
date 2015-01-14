from flask import Flask, render_template, request, jsonify, redirect, flash, url_for
from database import db_session
from models import URLModel
import string

app = Flask(__name__)
app.config['SERVER_NAME'] = 'localhost:5000'
app.secret_key = 'some_secret'

@app.teardown_appcontext
def shutdown_session(exception=None):
	db_session.remove()

@app.route('/')
def index():
	return render_template('index.html')


def genCode(num):
	arr = []
	while num > 0:
		arr.append(num % 62)
		num //= 62
	
	arr.reverse()
	code = ''
	
	for item in arr:
		if item < 26:
			code += chr(ord('a') + item)
		elif item < 52:
			code += chr(ord('A') + item - 26)
		else:
			code += chr(ord('0') + item - 52)
	return code


@app.route('/generate/')
def generate():
	request_url = request.args.get('url')

	# redirect won't work unless you have the scheme
	if string.find(request_url, 'http') == -1:
		request_url = 'http://' + request_url

	# prevent looping
	if string.find(request_url, app.config['SERVER_NAME']) != -1:
		return jsonify(hasError=True)

	long_url = URLModel.query.filter(URLModel.longURL == request_url).first()
	if long_url:
		return jsonify(shortURL=long_url.shortURL)
	else:
		newURL = URLModel(request_url, '')
		db_session.add(newURL)
		db_session.flush()
		newURL.shortURL = genCode(newURL.id)
		db_session.commit()
		return jsonify(shortURL=newURL.shortURL)


@app.route('/url/<url_id>')
def reroute(url_id):
	request_url = URLModel.query.filter(URLModel.shortURL == url_id).first()
	if not request_url:
		flash('This shortcode (%s) is not in the system!' % (url_id))
		return redirect(url_for('index'))
	else:
		return redirect(request_url.longURL, code=302)


if __name__ == '__main__':
	app.run(debug=True)
