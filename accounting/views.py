# You will probably need more methods from flask but this one is a good start.
from flask import render_template, request

# Import things from Flask that we need.
from accounting import app, db

# Import our models
from models import Contact, Invoice, Policy, Payment
from tools import PolicyAccounting
from datetime import date, datetime

# Routing for the server.
@app.route("/")
@app.route("/get_policy", methods=["POST"])
def get_invoices():
    if request.method == 'POST':
        #pull information from form submission
        policy_number = request.form['policy_number']
        date_cursor = request.form['date']

        #filter to policy number that was submitted
        policy = Policy.query.filter(Policy.policy_number == policy_number).first()
        if policy:
            pa = PolicyAccounting(policy.id)
            #filter invoices to policy that was submitted
            invoices = Invoice.query.filter(Invoice.policy_id == policy.id)\
                                    .filter(Invoice.deleted != 1).all()
            #filter paid invoices
            payments = Payment.query.filter(Payment.policy_id == policy.id).all()
            paid = len(payments)

            account_balance = pa.return_account_balance(date_cursor)

            return render_template('index.html', display=True, balance=account_balance, date=date_cursor, policy=policy_number,invoices=invoices, paid=paid)
        else:
            error = "Sorry the policy you entered may not exist."
            return render_template('index.html', display=False, error=error)

    else:
        error = "Error: Please try again!"
        return render_template('index.html', error=error)
