#!/user/bin/env python2.7

import unittest
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from accounting import db
from models import Contact, Invoice, Payment, Policy
from tools import PolicyAccounting

"""
#######################################################
Test Suite for PolicyAccounting
#######################################################
"""

#Test Problem 9.
class TestCancelPolicy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.policy = Policy('Test Policy', date(2015, 1, 1), 1200)
        db.session.add(cls.policy)
        db.session.commit()

    @classmethod
    def tearDownClass(cls):
        db.session.delete(cls.policy)
        db.session.commit()

    def setUp(self):
        pass

    def tearDown(self):
        for invoice in self.policy.invoices:
            db.session.delete(invoice)
        db.session.commit()

    def test_cancel_policy(self):
        """
            Test to see if descriptive_cancel_policy successfully cancels policy in database.
        """
        pa = PolicyAccounting(self.policy.id)
        pa.descriptive_cancel_policy("This policy is canceled.")
        self.assertEquals(self.policy.description, "This policy is canceled.")
        self.assertEquals(self.policy.cancel_date, datetime.now().date())
        self.assertEquals(self.policy.status, "Canceled")

class TestBillingSchedules(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_agent = Contact('Test Agent', 'Agent')
        cls.test_insured = Contact('Test Insured', 'Named Insured')
        db.session.add(cls.test_agent)
        db.session.add(cls.test_insured)
        db.session.commit()

        cls.policy = Policy('Test Policy', date(2015, 1, 1), 1200)
        db.session.add(cls.policy)
        cls.policy.named_insured = cls.test_insured.id
        cls.policy.agent = cls.test_agent.id
        db.session.commit()

    @classmethod
    def tearDownClass(cls):
        db.session.delete(cls.test_insured)
        db.session.delete(cls.test_agent)
        db.session.delete(cls.policy)
        db.session.commit()

    def setUp(self):
        pass

    def tearDown(self):
        for invoice in self.policy.invoices:
            db.session.delete(invoice)
        db.session.commit()

    def test_annual_billing_schedule(self):
        self.policy.billing_schedule = "Annual"
        #No invoices currently exist
        self.assertFalse(self.policy.invoices)
        #Invoices should be made when the class is initiated
        pa = PolicyAccounting(self.policy.id)
        self.assertEquals(len(self.policy.invoices), 1)
        self.assertEquals(self.policy.invoices[0].amount_due, self.policy.annual_premium)

    #Problem 2
    def test_monthly_billing_schedule(self):
        self.policy.billing_schedule = "Monthly"
        self.assertFalse(self.policy.invoices)
        pa = PolicyAccounting(self.policy.id)
        self.assertEquals(len(self.policy.invoices), 12)#assertEquals is the test
        self.assertEquals(self.policy.invoices[0].amount_due, self.policy.annual_premium/12)

    #Test Problem 8.
    def test_change_billing_schedule(self):
        p1 = Policy('Test Policy', date(2015, 01, 01), 500)
        p1.billing_schedule = 'Quarterly'
        db.session.add(p1)
        db.session.commit()
        pa = PolicyAccounting(p1.id)
        self.assertEquals(len(pa.policy.invoices), 4)
        self.assertEquals(pa.policy.invoices[0].amount_due, pa.policy.annual_premium/4)
        pa.change_billing_schedule('Monthly')
        #filters out deleted invoices
        active_invoices = Invoice.query.filter_by(policy_id = pa.policy.id)\
                            .filter(Invoice.deleted != 1)\
                            .all()
        self.assertEquals(len(active_invoices), 12)
        self.assertEquals(active_invoices[0].amount_due, pa.policy.annual_premium/12)

class TestReturnAccountBalance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_agent = Contact('Test Agent', 'Agent')
        cls.test_insured = Contact('Test Insured', 'Named Insured')
        db.session.add(cls.test_agent)
        db.session.add(cls.test_insured)
        db.session.commit()

        cls.policy = Policy('Test Policy', date(2015, 1, 1), 1200)
        cls.policy.named_insured = cls.test_insured.id
        cls.policy.agent = cls.test_agent.id
        db.session.add(cls.policy)
        db.session.commit()

    @classmethod
    def tearDownClass(cls):
        db.session.delete(cls.test_insured)
        db.session.delete(cls.test_agent)
        db.session.delete(cls.policy)
        db.session.commit()

    def setUp(self):
        self.payments = []

    def tearDown(self):
        for invoice in self.policy.invoices:
            db.session.delete(invoice)
        for payment in self.payments:
            db.session.delete(payment)
        db.session.commit()

    def test_annual_on_eff_date(self):
        self.policy.billing_schedule = "Annual"
        pa = PolicyAccounting(self.policy.id)
        self.assertEquals(pa.return_account_balance(date_cursor=self.policy.effective_date), 1200)

    def test_quarterly_on_eff_date(self):
        self.policy.billing_schedule = "Quarterly"
        pa = PolicyAccounting(self.policy.id)
        self.assertEquals(pa.return_account_balance(date_cursor=self.policy.effective_date), 300)

    def test_quarterly_on_last_installment_bill_date(self):
        self.policy.billing_schedule = "Quarterly"
        pa = PolicyAccounting(self.policy.id)
        invoices = Invoice.query.filter_by(policy_id=self.policy.id)\
                                .order_by(Invoice.bill_date).all()
        self.assertEquals(pa.return_account_balance(date_cursor=invoices[3].bill_date), 1200)

    def test_quarterly_on_second_installment_bill_date_with_full_payment(self):
        self.policy.billing_schedule = "Quarterly"
        pa = PolicyAccounting(self.policy.id)
        invoices = Invoice.query.filter_by(policy_id=self.policy.id)\
                                .order_by(Invoice.bill_date).all()
        self.payments.append(pa.make_payment(contact_id=self.policy.named_insured,
                                             date_cursor=invoices[1].bill_date, amount=600))
        self.assertEquals(pa.return_account_balance(date_cursor=invoices[1].bill_date), 0)
