#!python3

import cmd
import os
import textwrap
from npcs import npcs
from rooms import rooms
from items import items
from monsters import monsters
from player import player


# http://inventwithpython.com/blog/2014/12/11/making-a-text-adventure-game-with-the-cmd-and-textwrap-python-modules/

SCREEN_WIDTH = 70


COMBAT = False
showFullExits = True


class Location(object):

    def location_name(self, loc):
        location_name = rooms[loc]['name']
        return location_name

    def location_description(self, loc):
        location_description = rooms[loc]['desc']
        return location_description

    def location_npcs(self, loc):
        if len(rooms[loc]['npcs']) > 0:
            npc_list = rooms[loc]['npcs']
            for i in rooms[loc]['npcs']:
                npc_name = npcs[i]['name']
                npc_type = npcs[i]['type']
                return npc_name, npc_type

    def location_shop(self, loc):
        if 'shop' in rooms[loc]:
            if len(rooms[loc]['shop']) > 0:
                # print("=" * len(rooms[loc]['name']))
                # print("Items for sale:")
                for i in rooms[loc]['shop']:
                    item = i
                    item_value = items[i]['value']
                    # print("{0} ({1} gp)".format(i, items[i]['value']))
                    return item, item_value

    def location_items(self, loc):
        if len(rooms[loc]['ground']) > 0:
            item_list = []
            for i in rooms[loc]['ground']:
                item_list.append(items[i]['grounddesc'])
                item = items[i]['grounddesc']
            return sorted(item_list)

    def location_monsters(self, loc):
        # loc = player['location']
        monster_list = []
        for monster in rooms[loc]['monsters']:
            monster_list.append(monster)
        return monster_list

    def location_events(self, loc):
        if len(rooms[loc]['events']) > 0:
            event_list = []
            for e in rooms[loc]['events']:
                event_list.append(e)
            return event_list


class Monster(object):

    def create_monster(self, monster):
        self.retrieve_monster_type(monster)
        self.construct_monster(monster)

    def retrieve_monster_type(self, monster):
        loc = player['location']

        if monster in rooms[loc]['monsters']:
            print(monster)
            monster_type = monster.split()[1]
            if monster_type in monsters:
                print(monsters[monster_type]['desc'])
            else:
                print("no such monster")
            return monster_type

    def construct_monster(self, monster):
        monster_type = self.retrieve_monster_type(monster)
        print(monster_type)


class Combat(object):

    global COMBAT

    def combat_menu(self):
        os.system('cls')
        print("You are engage in combat")
        print("Opponents:")
        print("+++++++++")
        print(monsters)
        # for k, v in monsters:
        #     pass
        #     # print("{0} hp: {1}".format(combatants[v]['name'], monsters[v]['stats']['hp']))
        # print("{0} hp: {1}\n".format(player['name'], player['stats']['hp']))

    def prepare_fight(self):
        global COMBAT
        COMBAT = True
        loc = player['location']
        Location().location_name(player['location'])
        print("You encountered hostile creatures, you are in combat!")
        monster_list = Location().location_monsters(loc)
        for monster in monster_list:
            print(monster)

    def player_turn(self, monster):
        loc = player['location']
        monster_list = Location().location_monsters(loc)
        print("you Attack: {0}".format(monster))
        rooms[player['location']]['monsters'].remove(monster)

    def monster_turn(self, monster):
        loc = player['location']
        monster_list = Location().location_monsters(loc)
        print(monster_list)
        print("{0} attacks you".format(monster))

    def combat_round(self, monster):
        loc = player['location']
        self.player_turn(monster)
        monster_list = Location().location_monsters(loc)
        if len(monster_list) > 0:
            for monster in monster_list:
                os.system('pause')
                self.monster_turn(monster)
        else:
            Combat().combat_victory()

    def combat_victory(self):
        global COMBAT
        COMBAT = False
        print("All monsters are dead. Combat is over!")

    def player_death(self):
        global COMBAT
        COMBAT = False
        print("You have died!")


class Player(object):

    def create_character(self):
        print("Hello what is your name?")
        name = input('>>')
        player['name'] = name

    def player_name(self):
        player_name = player['name']
        return player_name

    def display_inventory(self):
        print("+" * 6)
        print("Inventory:")
        for i in player['inv']:
            print("- " + i)
            return i 

    def display_stats(self):
        print("+" * 6)
        print("Stats:")
        for k, v in player['stats'].items():
            print(k, ": ", v)
        print("-" * 6)
        print("defense: ", player['defense'])
        print("attack: ", player['attack'])

    def display_slots(self):
        print("+" * 6)
        print("Wearing:")
        for k, v in player['slots'].items():
            print(k, ": ", v)

    def character_overview(self):
        title = "Character information"
        print(title)
        print("+" * len(title))
        print("name: " + player['name'])
        self.display_inventory()
        self.display_stats()
        self.display_slots()

    def inventory(self):
        inventory = player['inv']
        if len(inventory) == 0:
            empty_inv = "Inventory:\n (nothing)"
            print(empty_inv)
            return empty_inv

        print("Inventory")
        print(player['inv'])
        item_count = {}
        for i in inventory:
            amount = inventory.count(i)
            if i in item_count.keys():
                item_count[i] = amount
            else:
                item_count[i] = amount

        for i in item_count:
            amount = item_count[i]
            if amount > 1:
                print(" {0} {1}".format(i, amount))
                return item_count
            else:
                print(" " + i)
                return i


class Display(object):

    def display_welcome(self):
        print("Welcome! ")
        print("Type help for commands")
        os.system('pause')

    def start_story(self):
        os.system('cls')
        print("start of the story.")
        os.system('pause')

    def display_location(self, loc):
        os.system('cls')
        location_name = Location().location_name(loc)
        location_description = Location().location_description(loc)
        location_npcs = Location().location_npcs(loc)
        location_shop = Location().location_shop(loc)
        print(location_name)
        print("=" * len(location_name))
        print('\n'.join(textwrap.wrap(location_description, SCREEN_WIDTH)))
        if location_npcs is not None:
            print("=" * len(rooms[loc]['name']))
            print("Persons of interest:")
            npc_name, npc_type = location_npcs
            print(npc_name, ":", npc_type)

        if location_shop is not None:
            item, value = location_shop
            print("=" * len(location_name))
            print("Items for sale:")
            print(item, "(", value, ")")
        self.display_exits(loc)
        # self.display_monsters_at_location(loc)

    def display_exits(self, loc):
        exits = []
        for direction in ('n', 's', 'e', 'w', 'u', 'd'):
            if direction in rooms[loc].keys():
                exits.append(direction.title())

        if showFullExits:
            print("=" * len(rooms[loc]['name']))
            print("Directions:")
            for direction in ('n', 's', 'e', 'w', 'u', 'd'):
                if direction in rooms[loc]:
                    exit_name = rooms[loc][direction]
                    print("%s: %s" % (direction.title(), rooms[exit_name]['name']))
        else:
            print("=" * len(rooms[loc]['name']))
            print("exits: %s" % ' '.join(exits))
            
    def display_combat(self):
        pass

    def display_character(self):
        pass


def get_all_desc_words(item_list):
    desc_words = []
    for i in item_list:
        desc_words.extend(items[i]['descwords'])
    return sorted(list(set(desc_words)))


def get_all_first_desc_words(item_list):
    item_list = sorted(list(set(item_list)))
    desc_words = []
    for i in item_list:
        desc_words.append(items[i]['descwords'][0])
    return sorted(list(set(desc_words)))


def get_first_item_matching_desc(desc, item_list):
    item_list = list(set(item_list))
    for i in item_list:
        if desc in items[i]['descwords']:
            return i
    return None


def get_all_items_matching_desc(desc, item_list):
    item_list = list(set(item_list))
    matching_items = []
    for i in item_list:
        if desc in items[i]['descwords']:
            matching_items.append(i)
    return matching_items


class Shop(object):

    def buy(self, arg):
        loc = player['location']
        if 'shop' not in rooms[loc]:
            text = 'This is not a shop'
            print(text)
            return text

        item_to_buy = arg.lower()
        if item_to_buy == '' or item_to_buy == ' ':
            text = "What would you like to buy?"
            print(text)
            return text

        item = get_first_item_matching_desc(item_to_buy, rooms[loc]['shop'])
        total_wealth = player['inv'].count('gold')
        if item is not None:
            item_value = items[item]['value']
            if item_value <= total_wealth:
                print("You have bought %s" % items[item]['shortdesc'])
                player['inv'].append(item)
                for i in range(item_value):
                    player['inv'].remove('gold')
                return "item bought"
            else:
                text = "You do not have enough gold to buy that."
                print(text)
                return text
        else:
            print("{0} is not sold here.".format(item_to_buy))
            return "item is not sold here"

    def sell(self, arg):
        loc = player['location']
        if 'shop' not in rooms[loc]:
            text = "This is not a shop"
            print(text)
            return text

        item_to_sell = arg.lower()

        if item_to_sell == " " or item_to_sell == '':
            text = "What would you like to sell?"
            print(text)
            return text

        # item = get_first_item_matching_desc(item_to_sell, player['inv'])

        for i in player['inv']:
            if item_to_sell in items[i]['descwords']:
                item_value = items[item_to_sell]['value']
                print("you have sold %s" % items[i]['shortdesc'])
                player['inv'].remove(i)
                for i in range(item_value):
                    player['inv'].append('gold')
                return "item sold"
        print("You do not have %s to sell." % item_to_sell)
        return "no such item to sell"


class DropTake(object):

    def take(self, arg):
        loc = player['location']
        item_to_take = arg.lower()
        if item_to_take == '' or item_to_take == " ":
            text = "Take which item? (use the look command)"
            print(text)
            return text

        cant_take = False
        takable_items_list = rooms[loc]['ground']
        for i in get_all_items_matching_desc(item_to_take, takable_items_list):
            if items[i].get('takeable', True) is False:
                cant_take = True
                continue
            print("you take %s" % items[i]['shortdesc'])
            rooms[loc]['ground'].remove(i)
            player['inv'].append(i)
            return "item taken"

        if cant_take:
            print("You cannot take %s" % item_to_take)
        else:
            text = "That is not on the ground."
            print(text)
            return text

    def drop(self, arg):
        loc = player['location']
        item_to_drop = arg.lower()

        if item_to_drop == '' or item_to_drop == " ":
            text = "Drop which item?"
            print(text)
            return text

        inv_desc_words = get_all_desc_words(player['inv'])

        if item_to_drop not in inv_desc_words:
            print("you do not have %s " % item_to_drop)
            return "no item in inventory to drop"

        item = get_first_item_matching_desc(item_to_drop, player['inv'])
        if item is not None:
            print("You drop %s" % items[item]['shortdesc'])
            player['inv'].remove(item)
            rooms[loc]['ground'].append(item)
            return "item dropped"


class Rpg(cmd.Cmd):
    pc = Player()
    prompt = '\n>> '

    def default(self, arg):
        # called when no other command works
        print("Unknown command.")

    def move_direction(self, direction):
        current_location = player['location']
        if direction in rooms[current_location]:
            new_location = rooms[current_location][direction]
            player['location'] = new_location
            event_list = Location().location_events(new_location)
            if event_list is not None:
                if 'combat' in event_list:
                    event = 'combat'
                    Combat().prepare_fight()
                    return event
            else:
                Display().display_location(player['location'])
                event = None
                return event
                # return player['location']
        else:
            text = "You cannot go in that direction."
            print(text)
            return text

    def do_quit(self, arg):
        """Quit the game"""
        print("Thanks for playing!")
        return True

    @staticmethod
    def do_combat(self):
        Combat().prepare_fight()

    def do_north(self, arg):
        """type 'north' to go north."""
        self.move_direction('n')

    def do_south(self, arg):
        """"type 'south' to go south."""
        self.move_direction('s')

    def do_east(self, arg):
        """type 'east' to go east."""
        self.move_direction('e')

    def do_west(self, arg):
        """type 'west' to go west"""
        self.move_direction('w')

    def do_up(self, arg):
        """type 'up' to go up."""
        self.move_direction('u')

    def do_down(self, arg):
        """"type 'down' to go down."""
        self.move_direction('d')

    def do_inventory(self, arg):
        """Display list of posessions"""
        Player().inventory()

    do_inv = do_inventory

    def do_take(self, arg):
        """take an item on the ground"""
        DropTake().take(arg)

    def do_drop(self, arg):
        """drop <item> to the ground"""
        DropTake().drop(arg)

    def do_look(self, arg):
        """Look at an item, direction, or the area:
"look" - display the current area's description
"look <direction>" - display the description of the area in that direction
"look exits" - display the description of all adjacent areas
"look <item>" - display the description of an item on the ground or in your inventory"""
        loc = player['location']
        looking_at = arg.lower()
        if looking_at == '':
            # os.system('cls')
            Display().display_location(loc)
            print("=" * len(rooms[loc]['name']))
            print("Items on the ground:")
            location_items = Location().location_items(loc)
            if location_items is not None:
                for i in location_items:
                    print(i)
            return

        if looking_at == 'exits':
            for d in ('n', 's', 'e', 'w', 'u', 'd'):
                if d in rooms['location']:
                    print("%s: %s" % d.title(), rooms[loc][d])
            return

        if looking_at in ('n', 's', 'e', 'w', 'u', 'd', 'north'):
            if looking_at.startswith('n') and 'n' in rooms[loc]:
                name = rooms[loc]['n']
                print(rooms[name]['name'])
            elif looking_at.startswith('s') and 's' in rooms[loc]:
                name = rooms[loc]['s']
                print(rooms[name]['name'])
            elif looking_at.startswith('e') and 'e' in rooms[loc]:
                name = rooms[loc]['e']
                print(rooms[name]['name'])
            elif looking_at.startswith('w') and 'w' in rooms[loc]:
                name = rooms[loc]['w']
                print(rooms[name]['name'])
            elif looking_at.startswith('u') and 'u' in rooms[loc]:
                name = rooms[loc]['u']
                print(rooms[name]['name'])
            elif looking_at.startswith('d') and 'd' in rooms[loc]:
                name = rooms[loc]['d']
                print(rooms[name]['name'])
            else:
                print("There is nothing in that direction.")
            return

        if looking_at in (rooms[loc]['npcs']):
            print(npcs[looking_at]['longdesc'])
            return

        if looking_at in (rooms[loc]['monsters']):
            print(monsters[looking_at]['desc'])
            return		

        item = get_first_item_matching_desc(looking_at, rooms[loc]['ground'])
        if item is not None:
            print("\n". join(textwrap.wrap(items[item]['longdesc'], SCREEN_WIDTH)))
            return

        print("You do not see that nearby.")

    def do_list(self, arg):
        """list items for sale at a shop"""
        loc = player['location']
        if 'shop' not in rooms[loc]:
            print("This is not a shop")
            return

        arg = arg.lower()
        print("For sale:")
        for i in rooms[loc]['shop']:
            print(" - %s" % i)
            if arg == 'full':
                print("\n".join(textwrap.wrap(items[i]['longdesc'], SCREEN_WIDTH)))

    def do_buy(self, arg):
        """ buy items"""
        Shop().buy(arg)

    def do_sell(self, arg):
        """Sell items in a shop"""
        Shop().sell(arg)

    def do_eat(self, arg):
        """eating or drinking an item"""
        item_to_eat = arg.lower()

        if item_to_eat == ' ':
            print("Eat what?")

        cannot_eat = False

        for i in get_all_items_matching_desc(item_to_eat, player['inv']):
            if items[i].get('edible', False) is False:
                cannot_eat = True
                continue
            print("You eat %s" % (items[i]['shortdesc']))
            player['inv'].remove(i)
            return

        if cannot_eat:
            print("You cannot eat that.")
        else:
            print("You do not have %s to eat." % item_to_eat)

    def do_exits(self, arg):
        global showFullExits
        showFullExits = not showFullExits
        if showFullExits:
            print("Showing full exit descriptions")
        else:
            print("Showing brief exit descriptions")

    def do_equip(self, arg):
        """equip <item>"""
        item_to_equip = arg.lower()
        if item_to_equip in player['inv']:
            # print(item_to_equip + " is in inventory!")
            equip_slot = items[item_to_equip]['slot'][0]
            player['slots'][equip_slot] = item_to_equip
            player['inv'].remove(item_to_equip)
            if items[item_to_equip]['type'] == 'armour':
                old_defense = player['defense']
                new_defense = old_defense + items[item_to_equip]['bonus']
                player['defense'] = new_defense
            if items[item_to_equip]['type'] == 'weapon':
                old_attack = player['attack']
                new_attack = old_attack + items[item_to_equip]['bonus']
                player['attack'] = new_attack
        else:
            print("You do not have this item to equip.")

    def do_attack(self, arg):
        """attack <monster>"""
        monster_to_attack = arg.lower()
        loc = player['location']
        if COMBAT:
            monster_list = Location().location_monsters(loc)
            # if monster_to_attack in rooms[loc]['monsters']:
            if len(monster_list) > 0:
                if monster_to_attack in monster_list:
                    Combat().combat_round(monster_to_attack)
                else:
                    print("There is no monster like that in this fight.")
            else:
                Combat().combat_victory()
        else: 
            print("You cannot perform this action when not in combat mode.")		

    def do_char(self, arg):
        """character information"""
        Player().character_overview()

    do_n = do_north
    do_s = do_south
    do_e = do_east
    do_w = do_west
    do_u = do_up
    do_d = do_down
    do_examine = do_look


if __name__ == '__main__':
    location = player['location']
    os.system('cls')
#    text = Display()
    pc = Player()
    # pc.create_character()
    # text.display_welcome()
    # text.start_story()
    Display().display_location(location)
    Rpg().cmdloop()
