p1 = Policy('Policy Four', date(2015, 2, 1), 500)
p1.billing_schedule = 'Two-Pay'

john = Contact.query.filter_by(name='John Doe')\
.filter(Contact.role == 'Agent').first()
p1.agent = john.id

ryan = Contact.query.filter_by(name ='Ryan Bucket')\
.filter(Contact.role == 'Named Insured').first()
p1.named_insured = ryan.id

db.session.add(p1)
db.session.commit()

