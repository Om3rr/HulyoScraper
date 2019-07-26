from alchemy import Base
import datetime
from sqlalchemy import Column, Integer, String, func, DateTime
from sqlalchemy.orm import Query
class Flight(Base):
    __tablename__ = 'flights'
    id = Column(Integer, primary_key=True)
    f_id = Column(Integer)
    f_country = Column(String(250), nullable=False)
    f_city = Column(String(250), nullable=False)
    f_price = Column(Integer, nullable=False)
    f_from = Column(DateTime, nullable=False)
    f_to = Column(DateTime, nullable=False)

    @staticmethod
    def factory(flight):
        args = {}
        args["f_id"] = int(flight.get("Id"))
        args["f_country"] = flight.get("DealCountryName")
        args["f_city"] = flight.get("DealDestinationName")
        args["f_price"] = flight.get("PriceInShekel")
        args["f_from"] = Flight.format_time(flight.get("OutboundFlights")[0].get("DepartureATA"))
        args["f_to"] = Flight.format_time(flight.get("InboundFlights")[-1].get("DepartureATA"))
        return Flight(**args)

    @staticmethod
    def format_time(str_time):
        return datetime.datetime.strptime(str_time, '%d/%m/%Y %H:%M')


    def already_exists(self, session) -> bool:
        return Query(func.count(Flight.id), session=session).filter(Flight.f_id == self.f_id).filter(Flight.f_price <= self.f_price).first()[0] == 1

    @staticmethod
    def find_by_country(session, country):
        return Flight.basic_query(session, lambda x: x.filter(Flight.f_country == country))

    @staticmethod
    def find_by_city(session, city):
        return Flight.basic_query(session, lambda x: x.filter(Flight.f_city == city))

    @staticmethod
    def basic_query(session, block):
        query = Query([Flight], session)
        query = block(query)
        return query.filter(Flight.f_from > datetime.datetime.now() + datetime.timedelta(days=1)) \
            .order_by(Flight.f_price) \
            .all()

    @property
    def href(self):
        return "https://www.hulyo.co.il/flightDetails/{}".format(self.f_id)
    def __str__(self):
        return  """טיסה ל {country} - {dest} ב {price} ש"ח
{f_to} - {f_from}
{href}""".format(country=self.f_country, dest=self.f_city, price=self.f_price, f_from=self.f_from,
                   f_to=self.f_to, href=self.href)






