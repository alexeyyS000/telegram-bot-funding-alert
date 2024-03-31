from db.base import Base
from sqlalchemy.orm import mapped_column
from sqlalchemy import Boolean, BigInteger, String, Date


class User(Base):
    __tablename__ = "users"
    id = mapped_column(BigInteger, primary_key=True)
    full_name = mapped_column(String, nullable=False)
    birth_date = mapped_column(Date, nullable=False)
    admin = mapped_column(Boolean, nullable=False, default=False)
    subscriber = mapped_column(Boolean, nullable=False, default=False)
    pending = mapped_column(Boolean, nullable=False, default=False)
    banned = mapped_column(Boolean, nullable=False, default=False)
