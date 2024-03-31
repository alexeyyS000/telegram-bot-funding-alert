from db.dal.user import UserDAL
from db.client import get_session
import contextlib
from .exceptions import *


@contextlib.contextmanager
def get_user_service():
    with get_session() as session:
        user_dal = UserDAL(session)
        yield UserService(user_dal)


class UserService:
    def __init__(self, dal):
        self.dal = dal

    def ban(self, id):
        instance = self.dal.get_one_or_none(id=id)
        if instance is None:
            raise NotExists
        elif not instance.banned:
            self.dal.update_one(
                {"admin": False, "pending": False, "subscriber": False, "banned": True},
                id=id,
            )
        else:
            raise AlreadyBanned("Already added")

    def add(self, id):
        instance = self.dal.get_one_or_none(id=id)
        if instance is None:
            raise NotExists
        elif instance.pending:
            self.dal.update_one({"pending": False}, id=id)
        else:
            raise AlreadyAdded("Already added")

    def make_admin(self, id):
        instance = self.dal.get_one_or_none(id=id)
        if instance is None:
            raise NotExists
        elif not instance.admin:
            self.dal.update_one({"admin": True}, id=id)
        else:
            raise AlreadyAdmin("Already admin")

    def refusal(self, id):
        instance = self.dal.get_one_or_none(id=id)
        if instance is not None:
            self.dal.delete_one(id=id)
        else:
            raise AlreadyRefusaled("Already refusaled")

    def create(self, **kwargs):
        instance = self.dal.get_one_or_none(id=kwargs["id"])
        if instance is not None:
            raise AlreadyExists("Already exist")
        else:
            return self.dal.create_one(**kwargs)

    def subscribe(self, id):
        instance = self.dal.get_one_or_none(id=id)
        if instance is None:
            raise NotExists
        elif not instance.subscriber:
            self.dal.update_one({"subscriber": True}, id=id)
        else:
            raise AlreadySubscribed("Already subscribed")

    def unsubscribe(self, id):
        instance = self.dal.get_one_or_none(id=id)
        if instance is None:
            raise NotExists
        elif instance.subscriber:
            self.dal.update_one({"subscriber": False}, id=id)
        else:
            raise AlreadyUnSubscribed("Already ununsubscribed")

    def get_one_or_none(self, id):
        instance = self.dal.get_one_or_none(id=id)
        return instance

    def get_pagination(self, page=1):
        return self.dal.fetch(3, page)
