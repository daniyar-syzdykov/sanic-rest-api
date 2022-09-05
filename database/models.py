import uuid
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update, delete
from sqlalchemy import Column, String, Integer, Text, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy_utils import PasswordType
from sqlalchemy.dialects.postgresql import UUID
from . import Base
from .utils import async_db_session as session
from sanic.exceptions import *


class DBMixin:
    @classmethod
    async def create(cls, **kwargs):
        new_data = cls(**kwargs)
        created = session.add(new_data)
        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()
            raise BadRequest(
                f'{cls.__name__} with this credentials already exists')
        finally:
            await session.close()
        return new_data.__dict__

    @classmethod
    async def get_all(cls):
        query = select(cls)
        result = await session.execute(query)
        result = [i[0] for i in result.all()]
        await session.close()
        return result

    @classmethod
    async def update(cls, id, **kwargs):
        query = (
            update(cls).where(cls.id == id).values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        result = await session.execute(query)
        result = [i[0] for i in result.all()]
        await session.commit()
        await session.close()

    @classmethod
    async def get_by_id(cls, id):
        query = select(cls).where(cls.id == id)
        result = await session.execute(query)
        if result is None:
            return None
        result = result.one_or_none()
        await session.close()
        return result[0] if result else None

    @classmethod
    async def delete(cls, id):
        """no idea what to do with this method"""
        query = delete(cls).where(cls.id == id)
        result = await session.execute(query)
        await session.close()
        return {'success': True}

    __mapper_args__ = {"eager_defaults": True}


class User(Base, DBMixin):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4)
    username = Column(String(255), unique=True)
    password = Column(PasswordType(max_length=32,
                                   schemes=[
                                       'pbkdf2_sha512',
                                       'md5_crypt',
                                   ],
                                   deprecated=['md5_crypt']
                                   ))
    is_active = Column(Boolean(), default=False)
    is_admin = Column(Boolean(), default=False)
    access_token = Column(Text())
    refresh_token = Column(Text())
    bills = relationship('Bill', backref='users', cascade='all, delete')

    @classmethod
    async def get_user_by_id(cls, id):
        query = select(User).where(
            User.id == id).options(joinedload(User.bills).joinedload(Bill.transactions))
        result = await session.execute(query)
        result = result.unique()
        result = result.one_or_none()
        await session.close()
        if result is None:
            return None
        return result[0]

    @classmethod
    async def get_by_username(cls, username):
        query = select(User).where(
            User.username == username).options(joinedload(User.bills).joinedload(Bill.transactions))
        result = await session.execute(query)
        result = result.unique()
        result = result.one_or_none()
        await session.close()
        if result is None:
            return None
        return result[0]

    @classmethod
    async def get_all_users(cls):
        _query = (select(User).options(joinedload(
            User.bills).joinedload(Bill.transactions)))
        result = await session.execute(_query)
        result = result.unique()
        result = [i[0] for i in result.all()]
        await session.close()
        return result

    @classmethod
    async def activate_user(cls, uuid):
        query = (
            update(User).where(User.uuid == uuid).values(is_active=True)
            .execution_options(synchronize_session="fetch")
        )
        result = await session.execute(query)
        result = [i[0] for i in result.all()]
        await session.commit()
        await session.close()

    @classmethod
    async def get_refresh_tokens(cls, user_id):
        query = select(User.refresh_token).where(User.id == user_id)
        result = await session.execute(query)
        result = result.unique()
        result = result.one_or_none()
        await session.close()
        return result[0] if result else None

    @classmethod
    async def get_access_token(cls, user_id):
        query = select(User.access_token).where(User.id == user_id)
        result = await session.execute(query)
        result = result.unique()
        result = result.one_or_none()
        await session.close()
        return result[0] if result else None


class Bill(Base, DBMixin):
    __tablename__ = 'bills'

    id = Column(Integer(), primary_key=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4)
    balance = Column(Float(), default=0)
    user_id = Column(Integer(), ForeignKey('users.id', ondelete='CASCADE'))
    transactions = relationship(
        'Transaction', backref='bills', cascade='all, delete')

    @classmethod
    async def get_all_bills(cls):
        query = (select(Bill).options(joinedload(Bill.transactions)))
        result = await session.execute(query)
        result = result.unique()
        result = [i[0] for i in result.all()]
        return result

    @classmethod
    async def get_bill_by_id(cls, id):
        query = select(Bill).where(
            Bill.id == id).options(joinedload(Bill.transactions))
        result = await session.execute(query)
        result = result.unique()
        result = result.one_or_none()
        await session.close()
        return result[0] if result else None


class Transaction(Base, DBMixin):
    __tablename__ = 'transactions'

    id = Column(Integer(), primary_key=True)
    transfered = Column(Integer(), default=0)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4)
    bill_id = Column(Integer(), ForeignKey('bills.id', ondelete='CASCADE'))


class Product(Base, DBMixin):
    __tablename__ = 'products'

    id = Column(Integer(), primary_key=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4())
    name = Column(String(255))
    description = Column(Text())
    price = Column(Float(precision=2))


# class Token(Base, DBMixin):
#     __tablename__ = 'tokens'

#     id = Column(Integer(), primary_key=True)
#     uuid = Column(UUID(as_uuid=True), default=uuid.uuid4())
#     user_id = Column(Integer(), ForeignKey('users.id', ondelete='CASCADE'))
#     refresh_token = Column(String(255))
