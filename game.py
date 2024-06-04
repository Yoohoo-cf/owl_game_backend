import string, random
from airport import Airport
from magic_goals import Magic
import config

class Game:

    def __init__(self, id, loc, consumption, player=None):
        self.status = {}
        self.location = []
        self.magics = []

        if id==0:
            # Create new game
            combinations = string.ascii_lowercase + string.ascii_uppercase + string.digits

            self.status = {
                "id": ''.join(random.choice(combinations) for i in range(20)),
                "name": player,
                "energy": {
                    "consumed": config.energy_initial,
                    "budget": config.energy_budget
                },
                "previous_location": ""
            }

            self.location.append(Airport(loc, True))

            sql = f"INSERT INTO game VALUES ('{self.status['id']}', {self.status['energy']['consumed']}, {self.status['energy']['budget']}, '{loc}', '{self.status['name']}')"
            print(sql)
            cur = config.conn.cursor()
            cur.execute(sql)

        else:
            # update energy consumption and budget
            sql2 = f"UPDATE game SET energy_consumed = energy_consumed + {consumption}, energy_budget = energy_budget - {consumption} WHERE id='{id}'"
            print(sql2)
            cur2 = config.conn.cursor()
            cur2.execute(sql2)

            # Find game from database
            sql = "SELECT id, energy_consumed, energy_budget, location, screen_name FROM game WHERE id='" + id + "'"
            print(sql)
            cur = config.conn.cursor()
            cur.execute(sql)
            res = cur.fetchall()
            if len(res) == 1:
                # game found
                self.status = {
                    "id": res[0][0],
                    "name": res[0][4],
                    "energy": {
                        "consumed": res[0][1],
                        "budget": res[0][2]
                    },
                    "previous_location": res[0][3]
                }
                # update to new location
                airport = Airport(loc, True)
                self.location.append(airport)
                self.set_location(airport)

            else:
                print("No game found!")

        self.fetch_magic_info()

    def set_location(self, location):
        sql = f"UPDATE game SET location='{location.ident}' WHERE id='{self.status['id']}'"
        print(sql)
        cur = config.conn.cursor()
        cur.execute(sql)

    def fetch_magic_info(self):
        sql = "SELECT * FROM (SELECT magics.id, magics.name, magics.description, magic_collected.game_id, magics.icon, magics.location, magics.hint "
        sql += "FROM magics INNER JOIN magic_collected ON magics.id = magic_collected.magic_id "
        sql += "WHERE magic_collected.game_id = '" + self.status["id"] + "' "
        sql += "UNION SELECT magics.id, magics.name, magics.description, NULL, magics.icon, magics.location, magics.hint "
        sql += "FROM magics WHERE magics.id NOT IN ("
        sql += "SELECT magics.id FROM magics INNER JOIN magic_collected ON magics.id = magic_collected.magic_id "
        sql += "WHERE magic_collected.game_id = '" + self.status["id"] + "')) AS t ORDER BY t.id;"

        print(sql)
        cur = config.conn.cursor()
        cur.execute(sql)
        res = cur.fetchall()
        for m in res:
            if m[3] == self.status["id"]:
                is_collected = True
            else:
                is_collected = False
            magic = Magic(m[0], m[1], m[2], is_collected, m[4], m[5], m[6])
            self.magics.append(magic)
        return
