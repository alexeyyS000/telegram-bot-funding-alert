from utils.sql.dal import SqlAlchemyRepository
from db.models import Funding


class FundingDAL(SqlAlchemyRepository):
    class Config:
        model = Funding
