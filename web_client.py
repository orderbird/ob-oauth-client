import datetime
import logging
from optparse import OptionParser
import os

from flask import Flask, url_for, session, request, redirect, render_template, jsonify
from requests_oauthlib import OAuth2Session

app = Flask(__name__)


def init_client(*args, **kwargs):
    redirect_uri = url_for('authorized', _external=True)
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
        result = oauth.get('http://localhost:8000/api/v3/whoami')
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
        app.config.get('OAUTH_ENDPOINT_AUTHORIZE'),
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
    token = oauth.fetch_token(app.config.get('OAUTH_ENDPOINT_TOKEN'),
                              client_secret=app.config.get('CLIENT_SECRET'),  # TODO really needed here?
                              authorization_response=request.url)

    session['oauth_token'] = token
    session['oauth_token']['expiry_datetime'] = datetime.datetime.fromtimestamp(session['oauth_token']['expires_at'])
    return redirect(url_for('.start'))


@app.route('/refresh')
def refresh():
    oauth = init_client(token=session['oauth_token'])
    session['oauth_token'] = oauth.refresh_token(app.config.get('OAUTH_ENDPOINT_REFRESH'),
                                                 client_id=app.config.get('CLIENT_ID'),
                                                 client_secret=app.config.get('CLIENT_SECRET'))
    session['oauth_token']['expiry_datetime'] = datetime.datetime.fromtimestamp(session['oauth_token']['expires_at'])
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
