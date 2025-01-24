from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote

app = Flask(__name__)

password = quote('Alish@123') 
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://postgres:{password}@localhost:5432/Intern"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Stock(db.Model):
    __tablename__ = 'stocks' 
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
        
        # Check if the ticker already exists
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