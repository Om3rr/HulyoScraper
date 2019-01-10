require 'json'
require 'rest-client'
require './initdb'
API_KEY = `echo $TELEGRAM_API`
USERNAME = "Omertesttbot"
CHAT_ID = "@hshshshsjs"


PRICES = {BCN: 120, BGY: 120, PRG: 120, ROM: 120, AMS: 120, HKG: 340, LAS: 400}

all_flights = File.read("flights.json") rescue "[]"
all_flights = JSON.parse(all_flights)
def tn(msg)
	p(msg)
	return if msg.empty?
    RestClient.post "https://api.telegram.org/bot#{API_KEY}/sendMessage", {chat_id: CHAT_ID, text: msg}
end


def get_flights
	resp = RestClient.get "https://s3.eu-central-1.amazonaws.com/catalogs.hulyo.co.il/catalogs/Production/Flights/v1.4/above199FlightsWebOnly.js"
	body = JSON.parse(resp.body)
	body['Flights']
end

def uniq_flight(flight)
	dest = flight['DealDestinationCode']
	price = flight['SalePrice']
	dates = flight['FlightsDatesText']
	return "#{dest} - #{price} - #{dates}"
end

def sendable_flight(flight)
	"#{flight['DealDestinationName']} - #{flight['FlightsDatesText']} - #{flight['PriceTitle']}"
end

def good_flights(flights)
	flights.select do |flight|
		next false if PRICES[flight['DealDestinationCode'].to_sym].nil?
		PRICES[flight['DealDestinationCode'].to_sym] > flight['SalePrice']
	end
end

def save_flights(flights)
	a = File.open('flights.json', 'w')
	a.write JSON.dump(flights.map{|f| f['id']})
end

flights = get_flights
dber = Dber.new
flights.each do |f|
	dber.insertFlight(f)
end
new_flights = dber.sendFlights
new_flights += dber.pdrop
new_flights.each_slice(5).map{|x| tn(x.map{|y| sendable_flight(JSON.parse(y[0]))}.join("\n"))}
dber.commitFlights
