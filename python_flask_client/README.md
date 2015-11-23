# Simple Python OAuth2 Web Client

This sample demonstrates a simple implementation of the orderbird connect OAuth2 flow.

## Installation

    $ virtualenv env
    $ source env/bin/activate
    $ pip install -r requriements.txt
    
## API Client Credentials

Set your `CLIENT_ID` and `CLIENT_SECRETE` in config.py file and run by typing
    
    $ python client_client.py
    
## The OAuth2 flow

1. After starting the web client open your browser at http://localhost:5000
2. The venue signs in to orderbird and submits the login form. Note that if the venue is already signed in to 
orderbird, and if the venue has already authorized your application, the OAuth2 flow automatically proceeds to the next 
step without presenting the login form.
3. The current webclient implementation tries to get permisions on 'ACCOUNT READ' scope, so client will redirect you to
authorization view.
4. orderbird sends a request to your applications's redirect URL.
5. The web client extracts the authorizations code provided by orderbird's request and passes it along to the obtain
token endpoint.
6. The obtain token endpoint returns an access token your applications can use in subsequent requests to the connect API.