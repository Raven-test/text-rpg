import json
import sqlite3
import shutil


def get_room(rid, dbfile):
    ret = None

    con = sqlite3.connect(dbfile)

    for row in con.execute("select json from rooms where id=?", (rid,)):
        jsontext = row[0]
        d = json.loads(jsontext)
        d['rid'] = rid
        ret = Room(**d)
        break

    con.close()
    return ret


class Room(object):
    def __init__(self, rid=0, name="aroom", desc="empty room", ground=[], neighbors={}):
        self.rid = rid
        self.name = name
        self. desc = desc
        self.ground = ground
        self.neighbors = neighbors

    def _neighbor(self, direction):
        if direction in self.neighbors:
            return self.neighbors[direction]
        else:
            return None

    def north(self):
        return self._neighbor('n')

    def south(self):
        return self._neighbor('s')

    def east(self):
        return self._neighbor('e')

    def west(self):
        return self._neighbor('w')

    def up(self):
        return self._neighbor('u')

    def down(self):
        return self._neighbor('d')





