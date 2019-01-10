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
		raw = nil
	pdrop = @db.execute("SELECT 1 from flights where id = ? AND price - 100 > ?", [flight['Id'], flight['PriceInShekel']]).flatten
	a = flight["FlightsDatesText"].split(' - ')[0]
	b = flight["FlightsDatesText"].split(' - ')[1]
	if pdrop.length > 0
		raw = @db.execute("SELECT raw FROM flights WHERE id = ?", flight['Id']).flatten.first
		raw = JSON.parse(raw)
	end
	@db.execute("UPDATE flights set price = ? where id = ?", [flight['PriceInShekel'], flight['Id']])
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
		raw
	end
	
	
	def sendFlights
		@db.execute("SELECT RAW from flights where sent = 0 order by price")
	end
	
	def commitFlights
		@db.execute("UPDATE flights SET sent = 1")
	end
	
end
