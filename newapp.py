import sqlite3
from flask import Flask, g, jsonify, render_template, request

app = Flask(__name__, template_folder='templates')
DATABASE = 'finance.db'

def get_db():
    """
    Open a new database connection if there is none yet for the current application context.
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_db(error):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    conn = sqlite3.connect("finance.db")
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT company FROM stock_prices")
    companies = cur.fetchall()
    cur.execute("SELECT DISTINCT date FROM stock_prices")
    dates = cur.fetchall()
    conn.close()
    return render_template('homepage.html', companies=companies, dates=dates)

@app.route('/stocks/date', methods=['GET'])
def get_all_stocks_for_date():
    date = request.args.get('date')
    if date:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM stock_prices WHERE Date=?", (date,))
        rows = cursor.fetchall()
        return render_template('stock.html', rows=rows)
    else:
        return "No date specified."
        
#get all stock data for a particular company
@app.route('/stocks/company/', methods=['GET'])
def get_all_stock_for_company():
    company = request.args.get('company')
    if company:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM stock_prices WHERE company = ?", (company,))
        rows = cursor.fetchall()
        return render_template('stock.html', rows=rows)
    if not company:
        return jsonify({'message': 'No data found for the requested company.'})
    return jsonify(data)


#get all stock data for a particular company for a particular day
@app.route('/stocks/', methods=['GET'])
def get_stock_for_company_for_date():
    company = request.args.get('company')
    date = request.args.get('date')
    if company and date:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM stock_prices WHERE company = ? AND date = ?", (company, date))
        rows = cursor.fetchall()
        return render_template('stock.html', rows=rows)

# Update stock data for a company by date
@app.route('/update_stock_data_for_company_by_date', methods=['POST', 'PATCH'])
def update_stock_data_for_company_by_date():
    company = request.form.get("company")
    date = request.form.get("date")
    open_price = request.form.get("open")
    high_price = request.form.get("high")
    low_price = request.form.get("low")
    close_price = request.form.get('close')
    volume = request.form.get("volume")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE stock_prices SET open='{open_price}', high='{high_price}', low='{low_price}', close='{close_price}', volume='{volume}' WHERE company='{company}' AND date='{date}'")
    conn.commit()
    return "Data updated successfully!!!!"

if __name__ == '__main__':
    app.run(port=8000, debug=True)
