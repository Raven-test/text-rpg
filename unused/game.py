#!python3
import cmd
import shutil
import tempfile
import textwrap

from unused.room import get_room


class Game(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.dbfile = tempfile.mktemp()
        shutil.copyfile("game.db", self.dbfile)
        self.loc = get_room(1, self.dbfile)
        self.look()

    prompt = "\ngame>> "

    def move(self, dir):
        new_room = self.loc._neighbor(dir)
        if new_room is None:
            print("you cannot go that way.")
        else:
            self.loc = get_room(new_room, self.dbfile)
            self.look()

    def look(self):
        print(self.loc.name)
        print("")
        for line in textwrap.wrap(self.loc.desc, 80):
            print(line)

    def do_quit(self, arg):
        """quit game"""
        print("thanks for playing")
        return True

    def do_n(self, arg):
        """Go north"""
        self.move("n")

    def do_s(self, arg):
        """Go South"""
        self.move('s')

    def do_e(self, arg):
        """Go East"""
        self.move('e')

    def do_w(self, arg):
        """Go West"""
        self.move('w')

    def do_u(self, arg):
        """Go up"""
        self.move('u')

    def do_d(self, arg):
        """Go down"""
        self.move('d')

    def do_save(self, arg):
        """Saves the game"""
        shutil.copyfile(self.dbfile, arg)
        print("The game was saved to {0}".format(arg))


if __name__ == "__main__":
    g = Game()
    g.cmdloop()
