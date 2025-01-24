**Documentation**
This Django app aims to load stock data from CSV file into local database and api to fetch data for individual stock based on the ticker.
Tech Stack
Backend (Django)
Database (PostgreSQL)
API (REST API)

**Project Structure**
flask-stock-api/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── config.py
│   ├── utils.py
│   ├── db_seed.py
│
├── migrations/
│
├── tests/
│   ├── __init__.py
│   ├── test_routes.py
│
├── .env
├── .gitignore
├── requirements.txt
├── run.py
├── README.md
Step-By-Step Implementation
1.	*Load CSV file and store it in the local database.*
import psycopg2
import pandas as pd 
from psycopg2.extras import execute_values


DB_NAME = "Intern"
DB_USER = "postgres"
DB_PASSWORD = "Alish@123"
DB_HOST = "localhost"
DB_PORT = "5432"


csv_file = "C:\Users\SWIFT\OneDrive\Documents\SMTMINTERN\Task 1\statement_nav.csv"


try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()
    print("Database connection successful.")
except Exception as e:
    print("Error connecting to the database:", e)
    exit()


try:
    df = pd.read_csv(csv_file)
    print("CSV file loaded successfully.")
except Exception as e:
    print("Error loading CSV file:", e)
    exit()

columns = [
    "idstatementnav", "Fund_full_Name", "Date", "StatementOfNav",
    "Investments", "ListedSecurities", "RegisteredEquities", "IpoInvestment",
    "GovernmentBonds", "CorporateDebentures", "OtherGovernmentSecurities",
    "BankFixedDeposits", "OtherInvestments", "CurrentAssets", "BankBalance",
    "OtherCurrentAssets", "CurrentLiabilities", "NetAssetValueGross",
    "FundManagementAndDepositoryFee1", "FundSupervisorFee1", "NetAssetValue",
    "UnitsOutstanding", "NavPerUnit", "IncomeStatement", "Income",
    "RealisedIncome", "UnrealisedIncome", "Expenses", "PreoperatingExpenses",
    "NoticePublicationFee", "AuditFee", "FundManagementAndDepositaryFee2",
    "FundSupervisorFee2", "OtherExpenses", "NetIncome", "Ticker"
]

df.columns = [col.strip() for col in df.columns]  


if set(columns) != set(df.columns):
    print("Column mismatch between CSV and database table.")
    print("CSV Columns:", df.columns)
    print("Database Table Columns:", columns)
    exit()

try:
    data = [tuple(row) for row in df.itertuples(index=False, name=None)]

  sql = f
  INSERT INTO stocks ({', '.join(columns)})
 VALUES %s

  execute_values(cursor, sql, data)
   conn.commit()
   print(f"Successfully inserted {len(data)} rows into the database.")
except Exception as e:
    print("Error inserting data into the database:", e)
    conn.rollback()
finally:
    cursor.close()
    conn.close()

*2.	API Implementation*
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote

app = Flask(__name__)

password = quote('Alish@123') 
app.config['SQLALCHEMY_DATABASE_URI'] = f "postgresql://postgres:{password}@localhost:5432/Intern"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Stock(db.Model):
    tablename = 'stocks' 
    idstatementnav = db.Column(db.Integer, primary_key=True)
    Fund_full_Name = db.Column(db.String(255))
    Date = db.Column(db.Date)
    StatementOfNav = db.Column(db.Integer)
    Investments = db.Column(db.Float)
    ListedSecurities = db.Column(db.Float)
    RegisteredEquities = db.Column(db.Float)
    IpoInvestment = db.Column(db.Float)
    GovernmentBonds = db.Column(db.Float)
    CorporateDebentures = db.Column(db.Float)
    OtherGovernmentSecurities = db.Column(db.Float)
    BankFixedDeposits = db.Column(db.Float)
    OtherInvestments = db.Column(db.Integer)
    CurrentAssets = db.Column(db.Float)
    BankBalance = db.Column(db.Float)
    OtherCurrentAssets = db.Column(db.Float)
    CurrentLiabilities = db.Column(db.Float)
    NetAssetValueGross = db.Column(db.Float)
    FundManagementAndDepositoryFee1 = db.Column(db.Float)
    FundSupervisorFee1 = db.Column(db.Float)
    NetAssetValue = db.Column(db.Float)
    UnitsOutstanding = db.Column(db.Float)
    NavPerUnit = db.Column(db.Float)
    IncomeStatement = db.Column(db.Integer)
    Income = db.Column(db.Float)
    RealisedIncome = db.Column(db.Float)
    UnrealisedIncome = db.Column(db.Float)
    Expenses = db.Column(db.Float)
    PreoperatingExpenses = db.Column(db.Float)
    NoticePublicationFee = db.Column(db.Float)
    AuditFee = db.Column(db.Float)
    FundManagementAndDepositaryFee2 = db.Column(db.Float)
    FundSupervisorFee2 = db.Column(db.Float)
    OtherExpenses = db.Column(db.Float)
    NetIncome = db.Column(db.Float)
    Ticker = db.Column(db.String(50))

@app.route('/stocks/<ticker>', methods=['GET', 'POST'])
def get_stock_data(ticker):
    stocks = Stock.query.filter_by(Ticker=ticker).all()
    if not stocks:
        return jsonify({'error': 'Stock not found'}), 404
    result = [{
        'idstatementnav': stock.idstatementnav,
        'Fund_full_Name': stock.Fund_full_Name,
        'Ticker': stock.Ticker
    } for stock in stocks]
    return jsonify(result)

   if request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON'}), 400
        if Stock.query.filter_by(Ticker=ticker).first():
            return jsonify({'error': f"Ticker '{ticker}' already exists"}), 400

try:
            new_stock = Stock(
                idstatementnav=data['idstatementnav'],
                Fund_full_Name=data['Fund_full_Name'],
                Ticker=data['Ticker']
            )
            db.session.add(new_stock)
            db.session.commit()
            return jsonify({'message': 'Stock added successfully!'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
Run the Project
Running the server using python manage.py runserver
The API is then available in https://127.0.0.1:8000/<ticker>

Fetching the data
Sending GET request for http://127.0.0.1:5000/stocks/SEF
 ![]("C:\Users\SWIFT\OneDrive\Documents\SMTMINTERN\Task 1\1.png")


Sending POST request for http://127.0.0.1:5000/stocks/NMB50
"C:\Users\SWIFT\OneDrive\Documents\SMTMINTERN\Task 1\2.png"



Conclusion:
This Django app loads data from CSV file into the local database and provides API to fetch data based in each stock. 



