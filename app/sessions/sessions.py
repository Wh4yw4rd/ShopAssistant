import uuid

from app.models.session_models import *


def create_session(user_details):
    id = uuid.uuid4()
    session = {id : Session(**user_details)}
    return id