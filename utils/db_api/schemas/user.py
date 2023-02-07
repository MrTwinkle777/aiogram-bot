from sqlalchemy import Column, BigInteger, sql, String

from utils.db_api.db_gino import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = 'users'
    user_id = Column(BigInteger, primary_key=True)
    notification = Column(String(5))
    query: sql.select
