import config
from geopy import distance
from collection import Collection

class Airport:

    def __init__(self, ident, active=False, data=None):
        self.ident = ident
        self.active = active

        if data is None:
            sql = "SELECT ident, name, latitude_deg, longitude_deg FROM airport WHERE ident = '" + ident + "'"
            print(sql)
            cur = config.conn.cursor()
            cur.execute(sql)
            res = cur.fetchall()
            if len(res) == 1:
                self.ident = res[0][0]
                self.name = res[0][1]
                self.latitude = float(res[0][2])
                self.longitude = float(res[0][3])

        else:
            self.name = data['name']
            self.latitude = float(data['latitude'])
            self.longitude = float(data['longitude'])


    # SET Magical Airports DATA
    def set_magic_airports(self):
        magic_airports_list = []

        sql = "SELECT airport.ident, airport.name, airport.latitude_deg, airport.longitude_deg FROM airport "
        sql += " INNER JOIN country ON airport.iso_country = country.iso_country "
        sql += " WHERE country.continent = 'EU' AND airport.type = 'closed' "
        sql += " AND country.name IN ('Slovenia', 'San Marino', 'North Macedonia', 'Moldova', 'Luxembourg', 'Guernsey', 'Andorra', 'Slovakia');"
        print(sql)
        cur = config.conn.cursor()
        cur.execute(sql)
        res = cur.fetchall()

        for r in res:
            if r[0] != self.ident:
                data = {'name': r[1], 'latitude': r[2], 'longitude': r[3]}
                print(data)
                magic_airport = Airport(r[0], False, data)
                magic_airport.distance = self.distanceTo(magic_airport)

                magic_airports_list.append(magic_airport)
                magic_airport.energy_consumption = self.energy_consumption(magic_airport.distance)

        return magic_airports_list

    def fetch_magics(self, game):
        self.magics = Collection(game)

    def distanceTo(self, target):

        address_1 = (self.latitude, self.longitude)
        address_2 = (target.latitude, target.longitude)
        dist = distance.distance(address_1, address_2).km
        return int(dist)

    def energy_consumption(self, km):
        consumption = config.energy_per_flight + km * config.energy_per_km
        return consumption


