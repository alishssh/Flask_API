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

    sql = f"""
        INSERT INTO stocks ({', '.join(columns)})
        VALUES %s
    """

    execute_values(cursor, sql, data)
    conn.commit()
    print(f"Successfully inserted {len(data)} rows into the database.")
except Exception as e:
    print("Error inserting data into the database:", e)
    conn.rollback()
finally:
    cursor.close()
    conn.close()
