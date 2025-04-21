from app import create_app
from app.models import db,User,Trip,JournalEntry,TrustedContact,Location

app=create_app()

with app.app_context():
    db.create_all()
    db.drop_all()
    
    user=User(username='Felicia',email='feliciakk@gmail.com')
    db.session.add(user)
    db.session.commit()
    
    trip=Trip(title='My Trip', user_id=user.id)
    db.session.add(trip)
    db.session.commit()
    
    journalEntry=JournalEntry(title='My Journal Entry', content='This is my journal entry', user_id=user.id)
    db.session.add(journalEntry)
    db.session.commit()
    
    TrustedContact=TrustedContact(name='Mom', email='janekurui@gmail.com', phone='071234564', user_id=user.id)
    db.session.add(TrustedContact)
    db.session.commit()
    
    location=Location(name='Nairobi', latitude=1.0, longitude=1.0, trip_id=trip.id)
    db.session.add(location)
    db.session.commit()
    
    print("Database seeded")
    
    