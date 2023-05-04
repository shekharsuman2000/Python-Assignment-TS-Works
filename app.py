import sqlite3
from flask import Flask, jsonify, render_template

import pandas as pd
import os

app = Flask(__name__,template_folder='templates')
conn = sqlite3.connect('finance.db')

@app.route('/', methods=['GET'])
def index():
    # render the HTML template for the web page
    # return os.getcwd()
    return render_template('finance.html')


@app.route('/', methods=['GET'])
def index():
    # render the HTML template for the web page
    # return os.getcwd()
     templateData = {
         'time': date
         }
    return render_template('returntemplate.html')


# Endpoint to get all companies' stock data for a particular day
# @app.route("/finance/<string:date>", methods=["GET"])
# def get_stock_data_by_date(date):
#     conn = sqlite3.connect("./finance.db")
#     data = pd.read_sql(f"SELECT * FROM stock_prices WHERE Date='{date}'", conn)
#     conn.close()
#     return jsonify(data.to_dict(orient="records"))


# API endpoint to get all companies' stock data for a particular day
@app.route('/stocks/date/<date>', methods=['GET'])
def get_all_stocks_for_date(date):
    return (date)
    # conn = sqlite3.connect('./finance.db')
    # c = conn.cursor()
    # c.execute("SELECT * FROM stock_prices WHERE date = ?", (date,))
    # data = c.fetchall()
    # conn.close()
    # if not data:
    #     return jsonify({'message': 'No data found for the requested date.'})
    # return jsonify(data)



@app.route('/stocks/company/<company>', methods=['GET'])
def get_all_stock_for_company(company):
    conn = sqlite3.connect('./finance.db')
    c = conn.cursor()
    c.execute("SELECT * FROM stock_prices WHERE company = ?", (company,))
    data = c.fetchall()
    conn.close()
    if not data:
        return jsonify({'message': 'No data found for the requested company.'})
    return jsonify(data)
    


# API endpoint to get all stock data for a particular company for a particular day
@app.route('/stocks/<company>/<date>', methods=['GET'])
def get_stock_for_company_for_date(company, date):
    conn = sqlite3.connect('./finance.db')
    c = conn.cursor()
    c.execute("SELECT * FROM stock_prices WHERE company = ? AND date = ?", (company, date))
    data = c.fetchall()
    conn.close()
    return jsonify(data)


# API endpoint to update stock data for a company by date
@app.route('/stocks/<company>/<date>', methods=['POST', 'PATCH'])
def update_stock_for_company_for_date(company, date):
    conn = sqlite3.connect('./finance.db')
    c = conn.cursor()
    open_value = request.json.get('open', None)
    high_value = request.json.get('high', None)
    low_value = request.json.get('low', None)
    close_value = request.json.get('close', None)
    volume_value = request.json.get('volume', None)
    if open_value is not None:
        c.execute("UPDATE stock_prices SET open = ? WHERE company = ? AND date = ?", (open_value, company, date))
    if high_value is not None:
        c.execute("UPDATE stock_prices SET high = ? WHERE company = ? AND date = ?", (high_value, company, date))
    if low_value is not None:
        c.execute("UPDATE stock_prices SET low = ? WHERE company = ? AND date = ?", (low_value, company, date))
    if close_value is not None:
        c.execute("UPDATE stock_prices SET close = ? WHERE company = ? AND date = ?", (close_value, company, date))
    if volume_value is not None:
        c.execute("UPDATE stock_prices SET volume = ? WHERE company = ? AND date = ?", (volume_value, company, date))
    conn.commit()
    conn.close()
    return 'Stock data updated successfully'

if __name__ == '__main__':
    app.run(port=8000, debug=True)
