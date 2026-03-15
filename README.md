# CJ's Google Projects

To run: 

```
poetry install
poetry run pyhon main.py
```

This will automatically pull from credentials.json and open up a browser for auth if credentials.json is not there. 

If credebtuaks are expired: 

```
rm res/credentials.json
```

## TODO list 

[] Write setup instructions for categories and credentials 
[] deploy on minikube with cron job
[] auto-expire credentials.json
[] refactor `get_citi_transactions` and `get_transactions`