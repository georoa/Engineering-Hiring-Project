john = Contact.query.filter_by(name='John Doe')\
.filter(Contact.role == 'Named Insured').first()

db.session.query(Policy).filter_by(policy_number ='Policy One').update({"named_insured": john.id})

db.session.commit()
