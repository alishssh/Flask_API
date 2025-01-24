**Documentation**

This Django app aims to load stock data from CSV file intolocal database and api to fetch data for individual stock based on the ticker.

**Tech Stack**

Backend(Django)

Database(PostgreSQL)

API (RESTAPI)

**Project Structure**

flask-stock-api/

├── app/

│   ├── \_\_init\_\_.py

│   ├── models.py

│   ├── routes.py

│   ├── config.py

│   ├── utils.py

│   ├── db\_seed.py

│

├── migrations/

│

├── tests/

│   ├── \_\_init\_\_.py

│   ├── test\_routes.py

│

├── .env

├── .gitignore

├──requirements.txt

├── run.py

├── README.md

**Step-By-Step Implementation**

1.     Load CSV file and store it in thelocal database.

import psycopg2

import pandas as pd

from psycopg2.extras import execute\_values

DB\_NAME = "Intern"

DB\_USER = "postgres"

DB\_PASSWORD = "Alish@123"

DB\_HOST = "localhost"

DB\_PORT = "5432"

csv\_file = "C:\\Users\\SWIFT\\OneDrive\\Documents\\SMTMINTERN\\Task1\\statement\_nav.csv"

try:

    conn = psycopg2.connect(

        dbname=DB\_NAME,

        user=DB\_USER,

        password=DB\_PASSWORD,

        host=DB\_HOST,

        port=DB\_PORT

    )

    cursor = conn.cursor()

    print("Database connectionsuccessful.")

except Exception as e:

    print("Error connecting tothe database:", e)

    exit()

try:

    df = pd.read\_csv(csv\_file)

    print("CSV file loadedsuccessfully.")

except Exception as e:

    print("Error loading CSVfile:", e)

    exit()

columns = \[

    "idstatementnav","Fund\_full\_Name", "Date", "StatementOfNav",

    "Investments","ListedSecurities", "RegisteredEquities","IpoInvestment",

    "GovernmentBonds","CorporateDebentures", "OtherGovernmentSecurities",

    "BankFixedDeposits","OtherInvestments", "CurrentAssets","BankBalance",

    "OtherCurrentAssets","CurrentLiabilities", "NetAssetValueGross",

   "FundManagementAndDepositoryFee1","FundSupervisorFee1", "NetAssetValue",

    "UnitsOutstanding","NavPerUnit", "IncomeStatement", "Income",

    "RealisedIncome","UnrealisedIncome", "Expenses","PreoperatingExpenses",

   "NoticePublicationFee", "AuditFee","FundManagementAndDepositaryFee2",

    "FundSupervisorFee2","OtherExpenses", "NetIncome", "Ticker"

\]

df.columns = \[col.strip() for col in df.columns\] 

if set(columns) != set(df.columns):

    print("Column mismatchbetween CSV and database table.")

    print("CSV Columns:",df.columns)

    print("Database TableColumns:", columns)

    exit()

try:

    data = \[tuple(row) for row indf.itertuples(index=False, name=None)\]

    sql = f"""

        INSERT INTO stocks ({','.join(columns)})

        VALUES %s

    """

    execute\_values(cursor, sql,data)

    conn.commit()

    print(f"Successfullyinserted {len(data)} rows into the database.")

except Exception as e:

    print("Error insertingdata into the database:", e)

    conn.rollback()

finally:

    cursor.close()

    conn.close()

2.     API Implementation

from flask import Flask, jsonify

from flask\_sqlalchemy import SQLAlchemy

from urllib.parse import quote

app = Flask(\_\_name\_\_)

password = quote('Alish@123')

app.config\['SQLALCHEMY\_DATABASE\_URI'\] =f"postgresql://postgres:{password}@localhost:5432/Intern"

app.config\['SQLALCHEMY\_TRACK\_MODIFICATIONS'\] = False

db = SQLAlchemy(app)

class Stock(db.Model):

    \_\_tablename\_\_ = 'stocks'

    idstatementnav =db.Column(db.Integer, primary\_key=True)

    Fund\_full\_Name =db.Column(db.String(255))

    Date = db.Column(db.Date)

    StatementOfNav =db.Column(db.Integer)

    Investments =db.Column(db.Float)

    ListedSecurities =db.Column(db.Float)

    RegisteredEquities =db.Column(db.Float)

    IpoInvestment =db.Column(db.Float)

    GovernmentBonds =db.Column(db.Float)

    CorporateDebentures =db.Column(db.Float)

    OtherGovernmentSecurities =db.Column(db.Float)

    BankFixedDeposits =db.Column(db.Float)

    OtherInvestments =db.Column(db.Integer)

    CurrentAssets =db.Column(db.Float)

    BankBalance = db.Column(db.Float)

    OtherCurrentAssets =db.Column(db.Float)

    CurrentLiabilities =db.Column(db.Float)

    NetAssetValueGross =db.Column(db.Float)

    FundManagementAndDepositoryFee1= db.Column(db.Float)

    FundSupervisorFee1 =db.Column(db.Float)

    NetAssetValue =db.Column(db.Float)

    UnitsOutstanding =db.Column(db.Float)

    NavPerUnit =db.Column(db.Float)

    IncomeStatement =db.Column(db.Integer)

    Income = db.Column(db.Float)

    RealisedIncome =db.Column(db.Float)

    UnrealisedIncome =db.Column(db.Float)

    Expenses = db.Column(db.Float)

    PreoperatingExpenses =db.Column(db.Float)

    NoticePublicationFee =db.Column(db.Float)

    AuditFee = db.Column(db.Float)

    FundManagementAndDepositaryFee2= db.Column(db.Float)

    FundSupervisorFee2 =db.Column(db.Float)

    OtherExpenses =db.Column(db.Float)

    NetIncome = db.Column(db.Float)

    Ticker =db.Column(db.String(50))

@app.route('/stocks/', methods=\['GET', 'POST'\])

def get\_stock\_data(ticker):

    stocks = Stock.query.filter\_by(Ticker=ticker).all()

    if not stocks:

        return jsonify({'error':'Stock not found'}), 404

    result = \[{

        'idstatementnav':stock.idstatementnav,

        'Fund\_full\_Name':stock.Fund\_full\_Name,

        'Ticker': stock.Ticker

    } for stock in stocks\]

    return jsonify(result)

    if request.method == 'POST':

        data = request.get\_json()

        if not data:

            returnjsonify({'error': 'Invalid JSON'}), 400

        # Check if the tickeralready exists

        ifStock.query.filter\_by(Ticker=ticker).first():

            returnjsonify({'error': f"Ticker '{ticker}' already exists"}), 400

        try:

            new\_stock = Stock(

               idstatementnav=data\['idstatementnav'\],

                Fund\_full\_Name=data\['Fund\_full\_Name'\],

               Ticker=data\['Ticker'\]

            )

           db.session.add(new\_stock)

            db.session.commit()

            returnjsonify({'message': 'Stock added successfully!'}), 201

        except Exception as e:

            db.session.rollback()

            returnjsonify({'error': str(e)}), 500

if \_\_name\_\_ == '\_\_main\_\_':

    app.run(debug=True)

**Run the Project**

Running theserver using python manage.py runserver

The API isthen available in [https://127.0.0.1:8000/\>](https://127.0.0.1:8000/<ticker)

 [](https://127.0.0.1:8000/<ticker)

[**Fetching the data**](https://127.0.0.1:8000/<ticker)

[Sending GET request for](https://127.0.0.1:8000/<ticker) [http://127.0.0.1:5000/stocks/SEF](http://127.0.0.1:5000/stocks/SEF)

Sending POST request for [http://127.0.0.1:5000/stocks/NMB50](http://127.0.0.1:5000/stocks/NMB50)

**Conclusion:**

This Django app loads data from CSV file into the localdatabase and provides API to fetch data based in each stock.
