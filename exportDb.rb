require 'json'
require 'sqlite3'
require 'time'

db = SQLite3::Database.new "test.db"

#will create an object of "dest": [[date, price].....]


rows = db.execute("SELECT distinct dest, hdest, price, from_date from flights")
dests = db.execute("SELECT distinct(dest) from flights")
o = {}
k = {}
dests.each{|d| o[d[0]] = []}
rows.each do |row|
	dest, hdest, price, f_date = row
	t = Time.strptime(f_date, "%d/%m")
	o[dest] << [t.to_i * 1000, price]
	k[dest] = hdest
end

File.open("data.json", "w+"){|f| f.write JSON.dump({o: o, k: k})}