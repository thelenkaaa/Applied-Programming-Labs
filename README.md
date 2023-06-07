## Prerequisites
1. Update `alembic.ini` file line 58, database/config.py
```
sqlalchemy.url = mysql+mysqlconnector://root:pass@127.0.0.1:3306/mysqldb
```
2. Run alembic upgrade command.
```
alembic upgrade heads
```
3. Install requirements.
```
pip3 install -r requirements.txt
```
4. Populate database tables.
```
python3 database/initial_database_data.py
```

## Start Flask Application
The application will run at `127.0.0.1:5044`.

## Run pytest Tests
1. Run tests.
```
python3 -m coverage run -m pytest
```
2. Run coverage report.
```
coverage report 
```