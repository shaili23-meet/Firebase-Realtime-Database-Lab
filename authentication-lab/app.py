from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  "apiKey": "AIzaSyD7bUc1bC7X_FgliBScqwmQ4BoGkZN4XOk",
  "authDomain": "csyes-b1a2b.firebaseapp.com",
  "projectId": "csyes-b1a2b",
  "storageBucket": "csyes-b1a2b.appspot.com",
  "messagingSenderId": "592989965326",
  "appId": "1:592989965326:web:28d0021babec8ffb1a005f",
  "measurementId": "G-G7Q78BECSQ",
  "databaseURL": "https://csyes-b1a2b-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            user = {"fullname": request.form['fullname'], "username" :request.form['username'], "bio":request.form['bio']}
            db.child("Users").child(login_session['user']['localId']).set(user)
            return redirect(url_for("add_tweet"))
        except:
            error = "Authentication failed"
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == 'POST':
        tweet = {"title":request.form['title'], "textT":request.form['textT']}
        tweet["uid"] = login_session['user']['localId']
        db.child("Tweets").push(tweet)
        return redirect(url_for("all_tweets"))
    return render_template("add_tweet.html")

@app.route('/all_tweets')
def all_tweets():
    return render_template("tweets.html", tweet = db.child("Tweets").get().val())


if __name__ == '__main__':
    app.run(debug=True)