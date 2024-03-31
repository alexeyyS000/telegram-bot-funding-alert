from utils.sql.dal import SqlAlchemyRepository
from db.models import User


class UserDAL(SqlAlchemyRepository):
    class Config:
        model = User
