
from PoE_service_matcher import db, app
from PoE_service_matcher.models import User, ServiceListing

with app.app_context():
    db.create_all()

    # Add users
    user1 = User(username='user1')
    user2 = User(username='user2')
    user3 = User(username='user3')

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)

    db.session.commit()

    # Add service listings
    service1 = ServiceListing(service='service1', slots=5, user_id=user1.id)
    service2 = ServiceListing(service='service2', slots=2, user_id=user1.id)
    service3 = ServiceListing(service='service3', slots=4, user_id=user2.id)
    service4 = ServiceListing(service='service4', slots=3, user_id=user2.id)
    service5 = ServiceListing(service='service5', slots=2, user_id=user3.id)

    db.session.add(service1)
    db.session.add(service2)
    db.session.add(service3)
    db.session.add(service4)
    db.session.add(service5)

    # Commit the changes
    db.session.commit()





