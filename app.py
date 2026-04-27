import identity.web
import requests
import os
from flask import Flask, redirect, render_template, request, session, url_for
from flask_session import Session

# The following variables are required for the app to run.

# TODO: Use the Azure portal to register your application and generate client id and secret credentials.
CLIENT_ID = "6b7ce157-c212-4487-b4fd-434b3b07cf05"
CLIENT_SECRET = "fc35d008-d6fc-44ea-9afc-f3655bc528eb"
TENANT_ID = "0cff9966-b3c0-4a41-9874-3c22e287ab4c"

# TODO: Figure out your authentication authority id.
AUTHORITY = "https://login.microsoftonline.com/0cff9966-b3c0-4a41-9874-3c22e287ab4c"

# TODO: generate a secret. Used by flask session for protecting cookies.
SESSION_SECRET = "762ddfd787b297d5ce1106dc3de6417ef20049d72fb3734b667b62d09c3691ae"

# TODO: Figure out what scopes you need to use
SCOPES = ["User.Read"]

# TODO: Figure out the URO where Azure will redirect to after authentication. After deployment, this should
#  be on your server. The URI must match one you have configured in your application registration.
REDIRECT_URI = "http://localhost:5000/getAToken"

REDIRECT_PATH = "/getAToken"

app = Flask(__name__)

app.config['SECRET_KEY'] = SESSION_SECRET
app.config['SESSION_TYPE'] = 'filesystem'
app.config['TESTING'] = True
app.config['DEBUG'] = True
Session(app)

# The auth object provide methods for interacting with the Microsoft OpenID service.
auth = identity.web.Auth(session=session,
                         authority=AUTHORITY,
                         client_id=CLIENT_ID,
                         client_credential=CLIENT_SECRET)

@app.route("/login")
def login():
    # TODO: Use the auth object to log in.
    response = auth.log_in(
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    return render_template("login.html", **response)


@app.route(REDIRECT_PATH)
def auth_response():
    result = auth.complete_log_in(request.args)
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    # TODO: Use the auth object to log out and redirect to the home page
    return redirect(auth.log_out(redirect_uri=url_for("index", _external=True)))


@app.route("/")
def index():
    # TODO: use the auth object to get the profile of the logged in user.
    if not auth.get_user():
        return redirect(url_for("login"))
    return render_template('index.html', user=None)


@app.route("/profile", methods=["GET"])
def get_profile():

    # TODO: Check that the user is loggen in and add credentials to the http request.
    if not auth.get_user():
        return redirect(url_for("login"))

    token = auth.get_token_for_user(SCOPES)
    headers = {'Authorization': 'Bearer ' + token['access_token']}

    result = requests.get(
        'https://graph.microsoft.com/v1.0/me', headers=headers
    )

    return render_template('profile.html', user=result.json(), result=None)

@app.route("/profile", methods=["POST"])
def post_profile():

    # TODO: check that the user is logged in and add credentials to the http request.
    if not auth.get_user():
        return redirect(url_for("login"))

    token = auth.get_token_for_user(SCOPES)
    headers = {'Authorization': 'Bearer ' + token['access_token']}
    result = requests.patch(
        'https://graph.microsoft.com/v1.0/users/' + request.form.get("id"),
        json=request.form.to_dict(), headers=headers
    )

    # TODO: add credentials to the http request.
    profile = requests.get(
        'https://graph.microsoft.com/v1.0/me',  headers=headers

    )
    return render_template('profile.html',
                           user=profile.json(),
                           result=result)


@app.route("/users")
def get_users():

    # TODO: Check that user is logged in and add credentials to the request.
    if not auth.get_user():
        return redirect(url_for("login"))
    token = auth.get_token_for_user(SCOPES)
    headers = {'Authorization': 'Bearer ' + token['access_token']}
    result = requests.get(
        'https://graph.microsoft.com/v1.0/users', headers=headers
    )
    return render_template('users.html', result=result.json())


if __name__ == "__main__":
    app.run()
