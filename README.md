####Hashtag Raffle

python 3.5 project
falcon 

###To start

You'll need a `config.yml` file with `GOOGLE_SHEETS` and `SPREADSHEET_ID` defined in project root as keys to a yml config dictionary.

Recommended that you make Google Sheet public so you only need an API key:

* Make API key
* Enable Google Sheets API
* Make spreadsheet public via [Share settings](https://groups.google.com/forum/embed/?place=forum%2Fgoogle-spreadsheets-api&showsearch=true&hl=mn#!topic/google-spreadsheets-api/-M51j5VTpmg) "anyone with link can access"
 

```
virtualenv -p python3 env
source env/bin/activate
(env) pip install -r requirements.txt
(env) gunicorn app
```
```
