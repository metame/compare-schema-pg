# Compare-Schema

Compare the schemas of any two postgres dbs' public schemas.  Does comparison of table, column, and type, printing the results.

# Usage
 1. Run `pip install -r requirements.txt`
 2. Edit `config.py` to enter your Postgres db strings, e.g. `postgres://user:pass@host:port/dbname`
 3. Run `python compare-schema.py`
