from alchemy import Base
from sqlalchemy import Column, Integer, String, func
from sqlalchemy.orm import Query
class Flight(Base):
    __tablename__ = 'flights'
    id = Column(Integer, primary_key=True)
    f_id = Column(Integer)
    f_country = Column(String(250), nullable=False)
    f_city = Column(String(250), nullable=False)
    f_price = Column(Integer, nullable=False)
    f_from = Column(String, nullable=False)
    f_to = Column(String, nullable=False)

    @staticmethod
    def factory(flight):
        args = {}
        args["f_id"] = int(flight.get("Id"))
        args["f_country"] = flight.get("DealCountryName")
        args["f_city"] = flight.get("DealDestinationName")
        args["f_price"] = flight.get("PriceInShekel")
        args["f_from"] = flight.get("OutboundFlights")[0].get("DepartureATA")
        args["f_to"] = flight.get("InboundFlights")[-1].get("DepartureATA")
        return Flight(**args)


    def already_exists(self, session) -> bool:
        return Query(func.count(Flight.id), session=session).filter(Flight.f_id == self.f_id).filter(Flight.f_price <= self.f_price).first()[0] == 1

    @property
    def href(self):
        return "https://www.hulyo.co.il/flightDetails/{}".format(self.f_id)
    def __str__(self):
        return  """טיסה ל {country} - {dest} ב {price} ש"ח
{f_to} - {f_from}
{href}""".format(country=self.f_country, dest=self.f_city, price=self.f_price, f_from=self.f_from,
                   f_to=self.f_to, href=self.href)






