# compress

Compress is a simple URL shortener which uses Python Flask and MySQL. Done as an exercise for me to
to make a small web app.

Recommended to set up a virtual env with virtualenvwrapper, and install mysql/connector in regular environment.

Setup:

1. Install Python 2.7.6
2. Install pip
3. Install mysql-connector-python and virtualenvwrapper
4. Install MySQL and MySQL Workbench
5. Create a virtual environment with virtualenvwrapper and enter it using "workon VENV_NAME"
6. pip install -r requirements.txt
7. Go into MySQL and set up a localhost database
8. Change database.py to use your username and password for the database
9. Go into python console:

```python
import init_db from database
init_db()
```
10. python compress.py
11. go to localhost:5000
