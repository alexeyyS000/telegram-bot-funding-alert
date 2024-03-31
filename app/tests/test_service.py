import pytest
import random
import string
from datetime import date, timedelta


@pytest.fixture(scope="function")
def one_user():
    test_data = {
        "id": 1,
        "full_name": random_name_generator(),
        "birth_date": random_date_generator(),
        "pending": True,
    }
    return test_data


def random_name_generator(size=6, chars=string.ascii_letters):
    return "".join(random.choice(chars) for _ in range(size))


def random_date_generator(start=date(2000, 1, 1), end=date(2023, 11, 30)):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)


@pytest.fixture(scope="function")
def create_one_user(user_dal, one_user):
    return user_dal.create_one(**one_user)


@pytest.fixture(scope="function")
def create_one_subscriber_user(user_dal, one_user):
    one_user["subscriber"] = True
    return user_dal.create_one(**one_user)


@pytest.fixture(scope="function")
def create_five_users(user_dal):
    quantaty = 5
    for i in range(1, quantaty):
        test_data = {
            "id": i,
            "full_name": random_name_generator(),
            "birth_date": random_date_generator(),
        }
        user_dal.create_one(**test_data)
    return quantaty


def test_create_one(user_dal, one_user, user_service):
    assert not user_dal.all()
    data = user_service.create(**one_user)
    assert user_dal.get_one_or_none(id=data.id)
    for key, val in one_user.items():
        assert data.__dict__[key] == val


def test_get_one(create_one_user, user_service, one_user, user_dal):
    assert user_dal.all()
    response = user_service.get_one_or_none(create_one_user.id)
    for key, val in one_user.items():
        assert response.__dict__[key] == val


def test_refuse_one(user_dal, user_service, create_one_user):
    assert user_dal.all()
    user_service.refusal(create_one_user.id)
    assert not user_dal.get_one_or_none(id=create_one_user.id)


def test_add_user(user_dal, user_service, create_one_user):
    assert user_dal.all()
    user_service.add(id=create_one_user.id)
    assert not user_dal.get_one_or_none(id=create_one_user.id).pending


def test_make_admin_user(user_dal, user_service, create_one_user):
    assert user_dal.all()
    user_service.make_admin(id=create_one_user.id)
    assert user_dal.get_one_or_none(id=create_one_user.id).admin


def test_ban_user(user_dal, user_service, create_one_user):
    assert user_dal.all()
    user_service.ban(id=create_one_user.id)
    assert user_dal.get_one_or_none(id=create_one_user.id).banned


def test_subscribe_user(user_dal, user_service, create_one_user):
    assert user_dal.all()
    user_service.subscribe(id=create_one_user.id)
    assert user_dal.get_one_or_none(id=create_one_user.id).subscriber


def test_unsubscribe_user(user_dal, user_service, create_one_subscriber_user):
    assert user_dal.all()
    user_service.unsubscribe(id=create_one_subscriber_user.id)
    assert not user_dal.get_one_or_none(id=create_one_subscriber_user.id).subscriber


def test_pagination(create_five_users, user_dal, user_service):
    for page in range(1, create_five_users):
        assert user_dal.all()
        db_response = user_dal.fetch(3, page)
        test_response = user_service.get_pagination(page)
        assert test_response == db_response
