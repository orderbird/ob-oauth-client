import datetime
from functools import wraps
import logging
from optparse import OptionParser
import os

from flask import Flask, url_for, session, request, redirect, render_template, jsonify
from requests_oauthlib import OAuth2Session

app = Flask(__name__)


# a simple, in-memory database :)
# TODO: use sqlite??
user_tokens = dict()


def set_token(token):
    username = session.get('username')
    user_tokens[username] = token


def get_token():
    username = session.get('username')
    if username:
        return user_tokens.get(username)


def delete_token():
    username = session.get('username')
    user_tokens.pop(username, None)


def get_from_session(key, default=None):
    username = session.get('username')
    usersessions = session.get('usersessions', {})
    if username and username in usersessions:
        return usersessions.get(username).get(key, None)


def set_in_session(key, value):
    username = session.get('username')
    usersessions = session.get('usersessions', {})
    if username and username in usersessions:
        usersessions.get(username)[key] = None


def init_client(*args, **kwargs):
    redirect_uri = url_for('authorized', _external=True)
    scope = ['read', 'account']
    return OAuth2Session(client_id=app.config.get('CLIENT_ID'),
                         scope=scope,
                         redirect_uri=redirect_uri,
                         **kwargs)


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('username'):
            return redirect(url_for('.login'))

        return f(*args, **kwargs)
    return decorated


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    session['username'] = request.form['username']
    return redirect(url_for('.start'))


@app.route('/logout')
def logout():
    session['username'] = None
    return redirect(url_for('.start'))


@app.route('/')
@requires_auth
def start():
    api_result = None
    token = get_token()
    if token:
        oauth = init_client(token=token)
        result = oauth.get(app.config.get('API_WHOAMI'))
        api_result = jsonify(result.json()) if result else None

    return render_template('start.html',
                           username=session.get('username'),
                           api_result=api_result,
                           session_data=jsonify(token or {}),
                           token=token)


@app.route('/authorize')
@requires_auth
def authorize():
    session['redirect_to'] = request.referrer
    oauth = init_client()
    authorization_url, state = oauth.authorization_url(
        app.config.get('OAUTH_ENDPOINT_AUTHORIZE'),
        access_type='offline',
        approval_prompt='force')
    session['oauth_state'] = state
    return redirect(authorization_url)


@app.route('/reset')
@requires_auth
def reset():
    # TODO: use logout instead
    delete_token()
    return redirect(url_for('.start'))


@app.route('/authorized')
@requires_auth
def authorized():
    """
    Callback uri for delivering the authentication code from oauth2 server.

    """
    oauth = init_client(state=session.get('oauth_state'))
    token = oauth.fetch_token(app.config.get('OAUTH_ENDPOINT_TOKEN'),
                              client_secret=app.config.get('CLIENT_SECRET'),  # TODO really needed here?
                              authorization_response=request.url)
    token['expiry_datetime'] = datetime.datetime.fromtimestamp(token.get('expires_at'))
    set_token(token)
    redirect_to = session.get('redirect_to')
    return redirect(redirect_to)


@app.route('/refresh')
@requires_auth
def refresh():
    oauth = init_client(token=get_token())
    token = oauth.refresh_token(app.config.get('OAUTH_ENDPOINT_REFRESH'),
                                client_id=app.config.get('CLIENT_ID'),
                                client_secret=app.config.get('CLIENT_SECRET'))
    token['expiry_datetime'] = datetime.datetime.fromtimestamp(get_token().get('expires_at'))
    set_token(token)
    return redirect(url_for('.start'))


#  Main application entry point
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("--loglevel", default='INFO', dest="log_level", help="set log level")
    parser.add_option("--insecure", action="store_true", dest="insecure_transport", default=False,
                      help="disables SSL requirement for OAuth")
    parser.add_option("--config", default="config", dest="config_module", help="set python path to config module")

    (options, args) = parser.parse_args()

    # First, set app configuration
    if options.config_module:
        app.config.from_object(options.config_module)

    # Set debug level
    if options.log_level:
        logging.basicConfig(level=options.log_level)
    if options.log_level == 'DEBUG':
        app.debug = True

    # Set SSL
    if options.insecure_transport or app.config.get('OAUTHLIB_INSECURE_TRANSPORT'):
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'

    # Set server host and port
    if len(args) > 0:
        host, port = args[0].split(':')
        port = int(port)
    else:
        host, port = 'localhost', 5000

    app.run(host=host, port=port)
