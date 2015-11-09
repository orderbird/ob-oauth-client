import datetime
import logging

from flask import Flask, url_for, session, request, redirect, render_template, jsonify
from requests_oauthlib import OAuth2Session

app = Flask(__name__)
app.debug = True
app.config.from_object('config')

logging.basicConfig(level=logging.DEBUG)


def init_client(*args, **kwargs):
    redirect_uri = 'http://127.0.0.1:5000/authorized'
    scope = ['read', 'account']
    return OAuth2Session(client_id=app.config.get('CLIENT_ID'),
                         scope=scope,
                         redirect_uri=redirect_uri,
                         **kwargs)


@app.route('/')
def start():
    api_result = None
    if 'oauth_token' in session:
        oauth = init_client(token=session['oauth_token'])
        result = oauth.get(app.config.get('SERVER')+'/api/v3/whoami')
        api_result = jsonify(result.json()) if result else None

    return render_template('start.html',
                           user=None,
                           api_result=api_result,
                           session=jsonify(session.get('oauth_token', {})),
                           token=session.get('oauth_token', None))


@app.route('/authorize')
def authorize():
    oauth = init_client()
    authorization_url, state = oauth.authorization_url(
        app.config.get('SERVER')+'/auth/authorize/',
        access_type='offline',
        approval_prompt='force')
    session['oauth_state'] = state
    return redirect(authorization_url)


@app.route('/reset')
def reset():
    if 'oauth_token' in session:
        del session['oauth_token']
    return redirect(url_for('.start'))


@app.route('/authorized')
def authorized():
    """
    Callback uri for delivering the authentication code from oauth2 server.

    """
    oauth = init_client(state=session['oauth_state'])
    token = oauth.fetch_token(app.config.get('SERVER')+'/auth/token/',
                              client_secret=app.config.get('CLIENT_SECRET'),  # TODO really needed here?
                              authorization_response=request.url)

    session['oauth_token'] = token
    session['oauth_token']['expiry_datetime'] = datetime.datetime.fromtimestamp(session['oauth_token']['expires_at'])
    return redirect(url_for('.start'))


@app.route('/refresh')
def refresh():
    oauth = init_client(token=session['oauth_token'])
    session['oauth_token'] = oauth.refresh_token(app.config.get('SERVER')+'/auth/token/',
                                                 client_id=app.config.get('CLIENT_ID'),
                                                 client_secret=app.config.get('CLIENT_SECRET'))
    session['oauth_token']['expiry_datetime'] = datetime.datetime.fromtimestamp(session['oauth_token']['expires_at'])
    return redirect(url_for('.start'))


if __name__ == '__main__':
    import os
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'
    app.run(host='localhost', port=5000)
