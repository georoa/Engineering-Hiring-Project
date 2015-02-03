
policy = raw_input('Enter the policy name you want to add: ')
year = raw_input('Enter the effective date year: ')
month  = raw_input('Enter the effective date month (Must include leading zeros if any!): ')
day = raw_input('Enter the effective date day (Must include leading zeros if any!): ')
premium = raw_input('Enter the annual premium: ')
billing = raw_input('Enter the billing schedule : ')
agent_input = raw_input('Enter the agents name (Contact must exist!): ')
insured_input = raw_input('Enter the insured name (Contact must exist!): ')

p1 = Policy(policy, date(int(year), int(month), int(day)), int(premium))
p1.billing_schedule = billing

q1 = Contact.query.filter_by(name=agent_input)\
.filter(Contact.role == 'Agent').first()
p1.agent = q1.id

q2 = Contact.query.filter_by(name =insured_input)\
.filter(Contact.role == 'Named Insured').first()
p1.named_insured = q2.id

db.session.add(p1)
db.session.commit()

print("Policy added!")

