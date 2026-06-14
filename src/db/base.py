# Import the central declarative tracking registry from your session factory
from src.db.session import Base

# Import your database model entities so the Python interpreter registers them onto the Base
from src.models.user import User

# Senior Engineer Note: As ChopNow-API grows, you will import new models here!
# from src.models.vendor import Vendor
# from src.models.order import Order