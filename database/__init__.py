from sqlalchemy.orm import declarative_base

Base = declarative_base()

from .models import User, Bill, Transaction, Product