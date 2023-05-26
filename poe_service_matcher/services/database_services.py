from ..models import User, ServiceListing
from sqlalchemy.orm import scoped_session
from poe_service_matcher import app

session = scoped_session(app.session_factory)

def get_user(id):
    with app.app_context():
        user = session.query(User).filter_by(username=str(id)).first()

        if not user:
            user = User(username=str(id))
            session.add(user)
            session.commit()

        return user

def list_service(mm, user):
    with app.app_context():
        new_service = ServiceListing(
            user_id=user.username,
            service=mm[0],
            map_provided=(True if mm[1] == 'y' else False),
            slots=int(mm[2]),
            price=int(mm[3])
        )
        session.add(new_service)
        session.commit()

def parse_request(m):

    services = None

    with app.app_context():
        services = session.query(ServiceListing).filter_by(service=m).order_by(ServiceListing.time_listed).all()

    service_lines = []
    for i, service in enumerate(services, start =1):
        username = f'<@{service.user_id}>'
        map_provided = "Yes" if service.map_provided else "No"
        service_lines.append(f"{i}. {username} {service.price} {map_provided}")

    return "Username, price, map provided: \n" + "\n".join(service_lines)

def service_exists(m):
    service = None

    with app.app_context():
        service = ServiceListing.query.filter_by(service=m).first()

    if service is not None:
        return True

    return False

def clear_listings():
     with app.app_context():
        session.query(ServiceListing).delete()
        session.commit()