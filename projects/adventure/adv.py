from room import Room
from player import Player
from world import World
from util import Stack

import random
from ast import literal_eval

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

graph = {}
stack = Stack()
visited = set()
visited_rooms = set()

for i in range(len(room_graph)):
    graph[i] = {}

while len(visited_rooms) < 500:
    current_room = player.current_room
    current_vertex = graph[current_room.id]
    if current_room.id not in visited_rooms:
        visited_rooms.add(current_room.id)
    exits = [direction for direction in current_room.get_exits()]
    for direction in exits:
        if direction not in current_vertex:
            current_vertex[direction] = '?'
    if '?' not in current_vertex.values():
        direction = stack.pop()
        traversal_path.append(direction)
        player.current_room = current_room.get_room_in_direction(direction)
    else:
        for direction in exits:
            if current_vertex[direction] == '?':
                next_room = current_room.get_room_in_direction(direction)
                opposite_direction = ''
                next_vertex = graph[next_room.id]
                if direction == 'n':
                    opposite_direction = 's'
                elif direction == 's':
                    opposite_direction = 'n'
                elif direction == 'e':
                    opposite_direction = 'w'
                elif direction == 'w':
                    opposite_direction = 'e'
                current_vertex[direction] = next_room.id
                next_vertex[opposite_direction] = current_room.id
                player.current_room = next_room
                traversal_path.append(direction)
                stack.push(opposite_direction)
                break



# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
