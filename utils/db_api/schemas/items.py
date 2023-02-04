from sqlalchemy import Column, BigInteger, String, sql, Float, ForeignKey, Integer

from utils.db_api.db_gino import TimedBaseModel


class Items(TimedBaseModel):
    __tablename__ = 'items'
    item_id = Column(Integer, primary_key=True, autoincrement=True)
    item_name = Column(String(250))
    price = Column(Float(50))
    user_id = Column(BigInteger, ForeignKey('users.user_id'))

    query: sql.select