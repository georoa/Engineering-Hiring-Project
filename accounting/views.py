# You will probably need more methods from flask but this one is a good start.
from flask import render_template, request

# Import things from Flask that we need.
from accounting import app, db

from datetime import date, datetime

# Import our models
from models import Contact, Invoice, Policy, Payment
#from tools import PolicyAccounting

# Routing for the server.
@app.route("/policy")
def index():
    # You will need to serve something up
    return render_template('index.html')

@app.route("/get_invoices", methods=["POST"])
def get_invoices():
    if request.method == 'POST':

        pa = PolicyAccounting(policy.id)

        #pull information from form submission
        policy_number = request.form['policy_number']
        date_cursor = request.form['date']

        #filter to policy number that was submitted
        policy = Policy.query.all()

        account_balance = pa.return_account_balance(date_cursor)
        return render_template('index.html', balance=account_balance)

    else:
        return render_template('index.html')
