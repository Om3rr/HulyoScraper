from alchemy import Base, engine
from flight import Flight
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)