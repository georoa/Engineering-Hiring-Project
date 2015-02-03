policy = raw_input('Enter the policy number you want to update (Policy must exist!): ')
add_name = raw_input('Enter the name of the insured person you want to add (Contact must exist!): ')

q1 = Contact.query.filter_by(name=add_name)\
.filter(Contact.role == 'Named Insured').first()

db.session.query(Policy).filter_by(policy_number =policy).update({"named_insured": q1.id})

db.session.commit()

print("Insured name added!")
