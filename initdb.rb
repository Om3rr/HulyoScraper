require 'sqlite3'
require 'json'




class Dber
	def initialize
		@db = SQLite3::Database.new "test.db"
		@drops = []
	end

	def pdrop
		return @drops
	end
	

	def insertFlight(flight)
	p @db.execute("SELECT *
 from flights where id = ? AND price - 100 > ?", [flight['Id'], flight['PriceInShekel']])
	p flight
p " -----------------------------------"
p " -----------------------------------"
p " -----------------------------------"
p " -----------------------------------"
p " -----------------------------------"
p " -----------------------------------"
p " -----------------------------------"
p " -----------------------------------"

	a = flight["FlightsDatesText"].split(' - ')[0]
	b = flight["FlightsDatesText"].split(' - ')[1]
	@db.execute("UPDATE flights set price = ? where id = ?", [flight['Id'], flight['PriceInShekel']])
	@db.execute("INSERT OR IGNORE INTO flights (id, price, dest, hdest, raw, from_date, to_date) 
            VALUES (?, ?, ?, ?, ?, ?, ?)", 
			[
				flight['Id'],
				flight['PriceInShekel'], 
				flight['DealDestinationCode'],
				flight['DealDestinationName'],
				JSON.dump(flight),
				a,
				b
			]
			) 
	end
	
	
	def sendFlights
		@db.execute("SELECT RAW from flights where sent = 0 order by price")
	end
	
	def commitFlights
		@db.execute("UPDATE flights SET sent = 1")
	end
	
end
