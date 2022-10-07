import threading, time, sys, os, json
from random import choice
from colorama import init

init()

from pynput.keyboard import Listener
from src.utils import *
from src.map import *
from src.entity import *
from src.handler import *
from src.sword import *

debug = True

map = Map()
player = Entity(
    2,
    map,
    '@',
    color=(240, 0, 0)
)

enemy = Entity(
    3,
    map, 
    '!',
    12, 
    3,
    color=(0, 0, 255)
)

powerup = Entity(
    6,
    map, 
    '$',
    0, 
    0,
    color=(0, 255, 0),
    damage=(0, 0),
    health=50
)

sword = Sword(map, player)

def main_loop() -> None:
    """
    main_loop() -> nothing

    Main loop, updates the screen and takes care of the HUD (Heads Up Display)

    :returns None: Nothing
    """

    while player.health > 0 and not core.finished:
        clear()

        for entity in core.entities: # display all entites                 
            entity.update()

            if not entity.xpos and not entity.ypos:
                continue
            
            map.update(
                entity.xpos,
                entity.ypos,
                entity
            )

        print(map.make())
        
        health_bar, percent = calculate_health(player.health, player.max_health)
        print(f':Health: [{health_bar}] ({percent})')
        print(f':Current item: {player.current_item}')
        print(f':Notifications: ')

        # print debug info
        if debug:
            print(f':Position: {player.xpos+1}, {player.ypos+1} (x, y)')
            print(f':Viewpos: {player.viewpos}')
            print(f':Entities: {str(core.entities)}')
            print(f':Current tile: {str(core.current_ent)}')
            print(f':Trigger: {core.trigger}')

        time.sleep(0.03)
    
    clear()
    if core.finished:
        print('you win!')
    else:
        print('you died!')

    sys.exit()

def handle(key) -> None:
    """
    handle(KeyCode) -> nothing

    handles the key, and moves or attacks based on the response

    :param key KeyCode: Key
    :returns None: Nothing
    """

    resp = handle_key(key)

    if resp.get('move'):
        xpos, ypos = resp['move']
        player.move(xpos, ypos)
    
    if resp.get('attack'):
        sword.swing(player)

    if resp.get('pos'):
        player.viewpos = resp['pos']

if __name__ == '__main__':
    clear()

    map_data = []
    for root, dirs, files in os.walk(os.path.join('src', 'maps')):
        for file in files:
            with open(os.path.join(root, file)) as fd:
                data = json.loads(fd.read())

                print(f'- Loading map "{data["name"]}", by {data["author"]}')

                map_data.append(map.parse(data))
    
    print('\nPicking and loading random map')
    rand_map = choice(map_data)
    map.map = rand_map

    input('\n\nPress [ENTER] to start your adventure')

    try:
        def key_handler():
            with Listener(on_press=handle) as listener:   
                listener.join() 

        threading.Thread(target=key_handler).start()
        threading.Thread(target=main_loop).start()
    except Exception:
        exit()