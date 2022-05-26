# ChatBot Support

## How to run
### Setup
1. Clone this repository.
2. Ensure you have django installed. If not: `pip install django`.
3. Head into the *human* folder.
4. Run the server with `py manage.py runserver`
5. Access the website on __http://localhost:8000/__ or __http://127.0.0.1:8000/__ in a browser.
6. Head into the *bot* folder.
7. Run file `py bot.py`
8

*Note:* The application starts with some articles in the database to work with. If you want to start with an empty database do the following:
- remove the *db.sqlite3*
- execute this command: `py manage.py migrate`
- run the server: `py manage.py runserver`
- access the website on __http://localhost:8000/__ or __http://127.0.0.1:8000/__ in a browser.

### What to do with the website
Register new categories and set default message to be send to users

