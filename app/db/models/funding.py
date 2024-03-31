from db.base import Base
from sqlalchemy.orm import mapped_column
from sqlalchemy import DateTime, Integer, String, Float


class Funding(Base):
    __tablename__ = "fundings"
    id = mapped_column(Integer, primary_key=True)
    symbol = mapped_column(String, nullable=False)
    rate = mapped_column(Float, nullable=False)
    date_time = mapped_column(DateTime, nullable=False)
