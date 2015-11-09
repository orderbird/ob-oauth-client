from requests_oauthlib import OAuth2Session
import logging
logging.basicConfig(level=logging.DEBUG)

CLIENT_ID = 'wZG5M5xRGZdh1D1cZ7IDNio4a4IqEqiO4H02ImIo'
CLIENT_SECRET = 'kz2ppMsjosVvE0DgmaDPAs4lCRodDbD1p8BvcqIqvS5XaSGxbeOhbFfhaU3Og1rEXbCokQck4sH8QKyvmQ02jmKpx3vbFoNJymGi3lJglV9DjHTDdlVvbLuslzTegzFO'
SERVER_URL = 'http://127.0.0.1:8000'

redirect_uri = 'http://127.0.0.1:5000/authorized'
scope = ['read', 'write']

authorization_base_url = SERVER_URL + '/auth/authorize/'
token_url = SERVER_URL + '/auth/token/'

myob_oauth = OAuth2Session(CLIENT_ID,
                           scope=scope,
                           redirect_uri=redirect_uri)

# Redirect user to my.orderbird to get authorization
authorization_url, state = myob_oauth.authorization_url(
    authorization_base_url,
    access_type='offline',
    approval_prompt='force'
)
print 'Please go here and authorize,', authorization_url

# Get the authorization verifier code from the callback url
redirect_response = raw_input('Paste the full redirect URL here:')

# Fetch the access token
myob_oauth.fetch_token(token_url,
                       client_secret=CLIENT_SECRET,
                       authorization_response=redirect_response)

# Fetch a protected resource, i.e. whoami
r = myob_oauth.get(SERVER_URL + '/api/v3/whoami/')
print r.content
