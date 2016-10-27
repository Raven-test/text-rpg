#!python3

import cmd
import os
import textwrap

# http://inventwithpython.com/blog/2014/12/11/making-a-text-adventure-game-with-the-cmd-and-textwrap-python-modules/

# DONE:
# TODO: create trade system with value for items

# in progress:
# TODO: create monsters
# set global combat = False (make true when in combat)


# backlog:
# TODO: create fighting system
# TODO: save and load game
# TODO: conversation options for npcs (talk to)
# TODO: create containers that can hold items
# TODO: Create quest system
# TODO: implement doors (closed and open, lockable)

SCREEN_WIDTH = 80

rooms = {'v1': {'name': "Main square",
                      'initial_desc': "initial description of main square",
                      'desc': "look description of main square. This is more or less the center of the village. This is just some text to test the textwrap functionality for the description of locations. The text cannot be on a second line in the dictionary. I wonder if this will all look rather ok in the command line.",
                      'ground': ['stone', 'gold'],
                      'npcs': [],
                      'monsters': ["orc", "troll"],
                      'n': "v2",
                      "e": "v3",
                      "w": "v4"},
         'v2': {'name': "Apothecary",
                      'desc': "Description of the Apothecary",
                      'ground': [],
                      'npcs': ['greg'],
                      'monsters': ["orc", "orc", "troll"],
                      'shop': ['potion'],
                      's': "v1"},
         'v3': {'name': "Sandbox",
                'desc': "Here anything can happen for testing purposes.",
                'ground': [],
                'npcs': ['greg'],
                'monsters': ["orc"],
                'shop': [],
                'w': "v1"},
         'v4': {'name': "Blacksmith",
                'desc': "The place for adventuring equipment",
                'ground': [],
                'npcs': ['greg'],
                'monsters': ["orc"],
                'shop': ["sword"],
                'e': "v1"},
         }

items = {"potion": {'grounddesc': "potion description on the ground",
                         'shortdesc': "potion short description",
                         'longdesc': "potion long description",
                         'takeable': True,
                         'edible': True,
                         'value': 1,
                         'descwords': ['potion']
                         },
              "stone": {'grounddesc': "stone description on the ground",
                         'shortdesc': "stone short description",
                         'longdesc': "stone long description",
                         'takeable': True,
                         'edible': False,
                         'value': 0,
                         'descwords': ['stone', 'rock']
                         },
              "gold": {'grounddesc': "gold description on the ground",
                        'shortdesc': "gold short description",
                        'longdesc': "gold long description",
                        'takeable': True, 
                        'descwords': ['gold', 'coin'],
                        'value': 1,
                        },
			 "shield": {'grounddesc': "shield ground description.", 
			            'shortdesc': "shield short description",
						'longdesc': "shield long description", 
						'descwords': ['shield'],
						'takeable': True,
                        'type': 'armour',
						'slot': ['lhand'],
						'value': 5, 
						'bonus': 2},
			 "sword": {'grounddesc': "sword ground description.", 
			            'shortdesc': "sword short description",
						'longdesc': "sword long description",
                        'descwords': ['sword'],						
						'takeable': True,
						'type': 'weapon',
						'slot': ['rhand'], 
						'value': 3, 
						'bonus': 1},
}

npcs = {'greg': {'name': "Greg",
                      'type': "shopkeeper",
                      'shortdesc': "Greg short description.",
                      'longdesc': "Greg long description"},

}

monsters = {'orc': {'name': "orc", 
                         'desc': "orc description",
                         'stats': {'xp': 1, 'hp': 1, 'str': 2, 'dex': 4, 'con': 5},
						 'attack': 3,
						 'defense': 3,
						 },
			     'troll': {'name': "troll", 
                         'desc': "Troll description",
                         'stats': {'xp': 1, 'hp': 4, 'str': 2, 'dex': 4, 'con': 5},
						 'attack': 5,
						 'defense': 5,
						 },
				} 

player = {'name': "player",
          'location': "v1",
          'inv':  ['stone', 'sword', 'shield', 'gold', 'gold'],
		  'stats': {'str': 1, 'dex': 2, 'con': 4, 'max_hp': 5, 'hp': 5, 'xp': 6},
		  'slots': {'rhand': None,
		            'lhand': None,
					'head': None,
					'body': None,
					'feet': None},
		 'attack': 4,
		 'defense': 6, 
		  
}

NAME = 'name'
DESC = 'desc'
NORTH = 'north'
SOUTH = 'south'
EAST = 'east'
WEST = 'west'
UP = 'up'
DOWN = 'down'
GROUND = 'ground'
SHOP = 'shop'
GROUNDDESC = 'grounddesc'
SHORTDESC = 'shortdesc'
LONGDESC = 'longdesc'
TAKEABLE = 'takeable'
EDIBLE = 'edible'
DESCWORDS = 'descwords'

COMBAT = False
location = "v1"
showFullExits = True
combatants = {}


class Combat(object):

    global COMBAT
    global location

    global combatants

    def combat_menu(self):
        global combatants
        os.system('cls')
        print("You are engage in combat")
        print("Opponents:")
        self.create_combatant_list(location)
        monsters = combatants
        print("+++++++++")
        print(monsters)
        # for k, v in monsters:
        #     pass
        #     # print("{0} hp: {1}".format(combatants[v]['name'], monsters[v]['stats']['hp']))
        # print("{0} hp: {1}\n".format(player['name'], player['stats']['hp']))

    def create_combatant_list(self, loc):
        global combatants
        monsters = rooms[loc]['monsters']
        for idx, val in enumerate(monsters):
            base_monster = [monsters[val]]
            x = [idx]
            combatants = dict(zip(x, base_monster))
            # return combatants

    def player_turn(self, monster):
        player_attack = player['attack']
        player_hp = player['stats']['hp']

    def monster_turn(self, monster):
        monster_attack = monsters[monster]['attack']
        player_defense = player['defense']

    def combat_round(self, monster):   
        if len(rooms[location]['monsters']) > 0:
            self.player_turn(monster)
            for monster, v in rooms[location]['monsters'].items():
                os.system('pause')
                self.monster_turn(monster)
        else:
            self.combat_victory()

    def combat_victory(self):
        COMBAT = False
        print("All monsters are dead. Combat is over!")

    def player_death(self):
        COMBAT = False
        print("You have died!")


class PlayerOptions(object):

    def create_character(self):
        print("Hello what is your name?")
        name = input('>>')
        player['name'] = name

    def display_inventory(self):
        print("+" * 6)
        print("Inventory:")
        for i in player['inv']:
            print("- " + i)

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


class PrintText(object):

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
        self.display_location_name(loc)
        self.display_location_description(loc)
        self.display_npc_name(loc)
        self.display_exits(loc)
        # self.display_monsters_at_location(loc)

    def display_location_name(self, loc):
        location_name = rooms[loc]['name']
        try:
            value = location_name
            print(location_name)
            print("=" * len(location_name))
        except KeyError:
            print("Unnamed location")
            print("================")

    def display_exits(self, loc):
        exits = []
        for direction in ('n', 's', 'e', 'w', 'u', 'd'):
            if direction in rooms[loc].keys():
                exits.append(direction.title())

        if showFullExits:
            print("=" * len(rooms[loc]['name']))
            print("Dirctions:")
            for direction in ('n', 's', 'e', 'w', 'u', 'd'):
                if direction in rooms[loc]:
                    exit_name = rooms[loc][direction]
                    print("%s: %s" % (direction.title(), rooms[exit_name]['name']))
        else:
            print("=" * len(rooms[loc]['name']))
            print("exits: %s" % ' '.join(exits))

    def display_location_description(self, loc):

        print('\n'.join(textwrap.wrap(rooms[loc]['desc'], SCREEN_WIDTH)))

    def display_items_at_location(self, loc):
        if len(rooms[loc]['ground']) > 0:
            print("=" * len(rooms[loc]['name']))
            print("Items on the ground:")
            for i in rooms[loc]['ground']:
                print(items[i]['grounddesc'])

    def display_npc_name(self, loc):
        if len(rooms[loc]['npcs']) > 0:
            print("=" * len(rooms[loc]['name']))
            print("Persons of interest:")
            npc_list = rooms[loc]['npcs']
            for i in rooms[loc]['npcs']:
                name = npcs[i]['name']
                type = npcs[i]['type']
                print(name + ": " + type)

    def display_monsters_at_location(self, loc):
        location_monsters = rooms[loc]['monsters']
        if len(location_monsters) > 0:
            print("Monsters:")
            for m in location_monsters:
                print(m)
        else:
            pass


def move_direction(direction):
    global location
    menu = PrintText()

    if direction in rooms[location]:
        location = rooms[location][direction]
        os.system('cls')
        menu.display_location(location)
        player['location'] = location
    else:
        print("You cannot go in that direction")


def get_all_desc_words(item_list):
    desc_words = []
    for i in item_list:
        desc_words.extend(items[i]['descwords'])
    return list(set(desc_words))


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


class Rpg(cmd.Cmd):

    pc = PlayerOptions()
    text = PrintText()
    prompt = '\n>> '

    def default(self, arg):
        # called when no other command works
        print("Unknown command.")

    def do_quit(self, arg):
        """Quit the game"""
        print("Thanks for playing!")
        return True

    @staticmethod
    def do_combat(self):
        global COMBAT
        combat = Combat()
        COMBAT = True
        combat.combat_menu()

    def do_north(self, arg):
        """type 'north' to go north."""
        move_direction('n')

    def do_south(self, arg):
        """"type 'south' to go south."""
        move_direction('s')

    def do_east(self, arg):
        """type 'east' to go east."""
        move_direction('e')

    def do_west(self, arg):
        """type 'west' to go west"""
        move_direction('w')

    def do_up(self, arg):
        """type 'up' to go up."""
        move_direction('u')

    def do_down(self, arg):
        """"type 'down' to go down."""
        move_direction('d')

    def do_inventory(self, arg):
        """Display list of posessions"""
        if len(player['inv']) == 0:
            print("Inventory:\n (nothing)")
            return

        item_count = {}
        for i in player['inv']:
            if i in item_count.keys():
                item_count[i] += 1
            else:
                item_count[i] = 1

        print("Inventory")
        for i in set(player['inv']):
            if item_count[i] > 1:
                print(" %s (%s)" % (i, item_count[i]))
            else:
                print(" " + i)

    do_inv = do_inventory

    def do_take(self, arg):
        """take an item on the ground"""
        item_to_take = arg.lower()
        if item_to_take == '':
            print("Which item? (type look)")
            return

        cant_take = False
        for i in get_all_items_matching_desc(item_to_take, rooms[location]['ground']):
            if items[i].get('takeable', True) == False:
                cant_take = True
                continue
            print("you take %s" % items[i]['shortdesc'])
            rooms[location]['ground'].remove(i)
            player['inv'].append(i)
            return

        if cant_take:
            print("You cannot take %s" % item_to_take)
        else:
            print("That is not on the ground.")

    def do_drop(self, arg):
        """drop <item> to the ground"""
        item_to_drop = arg.lower()

        inv_desc_words = get_all_desc_words(player['inv'])

        if item_to_drop not in inv_desc_words:
            print("you do not have %s " % item_to_drop)
            return

        item = get_first_item_matching_desc(item_to_drop, player['inv'])
        if item is not None:
            print("You drop %s" % items[item]['shortdesc'])
            player['inv'].remove(item)
            rooms[location]['ground'].append(item)

    def do_look(self, arg):
        """Look at an item, direction, or the area:
"look" - display the current area's description
"look <direction>" - display the description of the area in that direction
"look exits" - display the description of all adjacent areas
"look <item>" - display the description of an item on the ground or in your inventory"""

        looking_at = arg.lower()
        if looking_at == '':
            # os.system('cls')
            text.display_location(location)
            text.display_items_at_location(location)
            return

        if looking_at == 'exits':
            for d in ('n', 's', 'e', 'w', 'u', 'd'):
                if d in rooms['location']:
                    print("%s: %s" % d.title(), rooms[location][d])
            return

        if looking_at in ('n', 's', 'e', 'w', 'u', 'd', 'north'):
            if looking_at.startswith('n') and 'n' in rooms[location]:
                name = rooms[location]['n']
                print(rooms[name]['name'])
            elif looking_at.startswith('s') and 's' in rooms[location]:
                name = rooms[location]['s']
                print(rooms[name]['name'])
            elif looking_at.startswith('e') and 'e' in rooms[location]:
                name = rooms[location]['e']
                print(rooms[name]['name'])
            elif looking_at.startswith('w') and 'w' in rooms[location]:
                name = rooms[location]['w']
                print(rooms[name]['name'])
            elif looking_at.startswith('u') and 'u' in rooms[location]:
                name = rooms[location]['u']
                print(rooms[name]['name'])
            elif looking_at.startswith('d') and 'd' in rooms[location]:
                name = rooms[location]['d']
                print(rooms[name]['name'])
            else:
                print("There is nothing in that direction.")
            return

        if looking_at in (rooms[location]['npcs']):
            print(npcs[looking_at]['longdesc'])
            return

        if looking_at in (rooms[location]['monsters']):
            print(monsters[looking_at]['desc'])
            return		

        item = get_first_item_matching_desc(looking_at, rooms[location]['ground'])
        if item is not None:
            print("\n". join(textwrap.wrap(items[item]['longdesc'], SCREEN_WIDTH)))
            return

        print("You do not see that nearby.")

    def do_list(self, arg):
        """list items for sale at a shop"""
        if 'shop' not in rooms[location]:
            print("This is not a shop")
            return

        arg = arg.lower()
        print("For sale:")
        for i in rooms[location]['shop']:
            print(" - %s" % i)
            if arg == 'full':
                print("\n".join(textwrap.wrap(items[i]['longdesc'], SCREEN_WIDTH)))

    def do_buy(self, arg):
        """ buy items"""

        if 'shop' not in rooms[location]:
            print("This is not a shop")
            return
        item_to_buy = arg.lower()
        if item_to_buy == ' ':
            print("What would you like to buy?")
            return

        item = get_first_item_matching_desc(item_to_buy, rooms[location]['shop'])
        item_value = items[item]['value']
        total_wealth = player['inv'].count('gold')
        if item is not None:
            if item_value <= total_wealth:
                print("You have bought %s" % items[item]['shortdesc'])
                player['inv'].append(item)
                for i in range(item_value):
                    player['inv'].remove('gold')	
                return
            else:
                print("You do not have enough gold to buy that.")
                return

        print("%s is not sold here." % item_to_buy)

    def do_sell(self, arg):
        """Sell items in a shop"""
        if 'shop' not in rooms[location]:
            print("This is not a shop")
            return

        item_to_sell = arg.lower()

        if item_to_sell == " ":
            print("What would you like to sell?")
            return

        # item = get_first_item_matching_desc(item_to_sell, player['inv'])
        item_value = items[item_to_sell]['value']
          
        for i in player['inv']:
            if item_to_sell in items[i]['descwords']:
                print("you have sold %s" % items[i]['shortdesc'])
                player['inv'].remove(i)
                for i in range(item_value):
                    player['inv'].append('gold')
                return
        print("You do not have %s to sell." % item_to_sell)

    def do_eat(self, arg):
        """eating or drinking an item"""
        item_to_eat = arg.lower()

        if item_to_eat == ' ':
            print("Eat what?")

        cannot_eat = False

        for i in get_all_items_matching_desc(item_to_eat, player['inv']):
            if items[i].get('edible', False) == False:
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
        combat = Combat()
        monster_to_attack = arg.lower()
        if COMBAT: 
#            combat.player_turn(monster_to_attack)
#            os.system('pause')
#            combat.monster_turn(monster_to_attack)
            combat.combat_round(monster_to_attack)
        else: 
            print("You cannot perform this action when not in combat mode.")		


    def do_char(self, arg):
        """character information"""
        pc = PlayerOptions()
        title = "Character information"
        print(title)
        print("+" * len(title))
        print("name: " + player['name'])
        pc.display_inventory()
        pc.display_stats()
        pc.display_slots()

    do_n = do_north
    do_s = do_south
    do_e = do_east
    do_w = do_west
    do_u = do_up
    do_d = do_down
    do_examine = do_look


if __name__ == '__main__':
    os.system('cls')
    text = PrintText()
    pc = PlayerOptions()
    # pc.create_character()
    # text.display_welcome()
    # text.start_story()
    text.display_location(location)
    Rpg().cmdloop()
