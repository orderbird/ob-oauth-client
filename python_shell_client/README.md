# Simple Python OAuth2 Shell Client

This sample demonstrates a simple implementation of the orderbird connect OAuth2 flow:

## Installation

    $ virtualenv env
    $ source env/bin/activate
    $ pip install -r requriements.txt
    
## API Client Credentials

Set your `CLIENT_ID` and `CLIENT_SECRETE` in shell_client.py and run by typing
    
    $ python shell_client.py
    
In case you are running a insecure local server you need to disable secure transport
```
$ OAUTHLIB_INSECURE_TRANSPORT=true python shell_client.py
```

## Then follow the instructions on prompt.

1. After starting the shell client open your browser and copy URL given on the terminal.
2. The venue signs in to orderbird and submit the login form. Note that if the venue is already signed in to 
orderbird, and if the venue has already authorized your application, the OAuth2 flow automatically proceeds to the next 
step without presenting the login form.
3. The current webclient implementation tries to get permisions on 'ACCOUNT READ' scope, so client will redirect you to
authorization view.
4. orderbird tries to redirect the browser, this fails. Copy the URL you was redirected to an paste into your terminal.
5. The shell client extracts the authorizations code provided by orderbird's redirect URL and passes it along to the obtain
token endpoint.
6. The obtain token endpoint returns an access token your applications can use in subsequent requests to the connect API.
