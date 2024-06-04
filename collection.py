import config

class Collection:

    def __init__(self, game):
        self.meets_magics = []
        self.check_magic_goals(game)

    def check_magic_goals(self, game):

        for magic in game.magics:
            if magic.loc == game.location[0].ident:
                self.meets_magics.append(magic.magicid)

        for magic in game.magics:
            if magic.collected == False and magic.magicid in self.meets_magics:
                sql = "INSERT INTO magic_collected VALUES ('" + game.status["id"] + "', '" + str(magic.magicid) + "')"
                print(sql)
                cur = config.conn.cursor()
                cur.execute(sql)
                magic.collected = True
        return