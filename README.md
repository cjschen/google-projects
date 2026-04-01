# CJ's Google Projects

To run: 

```
poetry install
poetry run pyhon main.py
```

This will automatically pull from credentials.json and open up a browser for auth if credentials.json is not there. 

If credentials are expired: 

```
rm secrets/credentials.json
```

## TODO list 

- [ ] Write setup instructions for categories and credentials 
- [x] deploy on minikube with cron job
- [ ] auto-expire credentials.json
- [x] refactor `get_citi_transactions` and `get_transactions`
    - [ ] refactor to return transaction list 
    - [ ] order transactions list by date
- [x] add tests with google api mocks
- [ ] investigate Plaid (like Yodelee) for hobby purposes
- Build MCP server (scary) https://www.youtube.com/watch?v=5PBaiMEPBsE
  - integrate w/ Google Home/Gemini
  