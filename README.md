# demo clients to connect to my.orderbird via oauth2

Two types of demo clients are available:

1. shell based client ```shell_client.py```
2. Flask based web client ```web_client.py```


## Some notes on oauth2 with curl

### Resource owner password-based 

Create a token directly without generating ana authentication code:
``` sh
curl -X POST -d "grant_type=password&username=dennis.hellmich@orderbird.com&password=foobar13" http://<CLIENT_ID>:<CLIENT_SECRET>@localhost:8000/auth/token/
```

Returns a json string in case of success:
``` json
{
    "access_token": "tmLgfB1Y2fWddTQvMoXsm53lQSxCyX",
    "token_type": "Bearer",
    "expires_in": 36000,
    "refresh_token": "LLOrW22MDo2vtspBIsxstatfHPjIs3",
    "scope": "read write"}
```

This token can be refreshed:
``` sh
curl -X POST -d "grant_type=refresh_token&refresh_token=LLOrW22MDo2vtspBIsxstatfHPjIs3" http://<CLIENT_ID>:<CLIENT_SECRET>@localhost:8000/auth/token/
```
