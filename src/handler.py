'''
This file is part of DungeonCrawler.

DungeonCrawler is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, 
either version 3 of the License, or (at your option) any later version.

DungeonCrawler is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with DungeonCrawler. 
If not, see <https://www.gnu.org/licenses/>. 
'''


keydict = {
    'w': {'move': (0, -1), 'pos': 'up'},
    's': {'move': (0, 1), 'pos': 'down'},
    'a': {'move': (-1, 0), 'pos': 'left'},
    'd': {'move': (1, 0), 'pos': 'right'},
    'g': {'attack': True},
    'key.up': {'pos': 'up'},
    'key.down': {'pos': 'down'},
    'key.left': {'pos': 'left'},
    'key.right': {'pos': 'right'}
}

def handle_key(key) -> dict:
    """
    handle_key(key) -> result

    Handles the given key, and returns movement, attacking, closing the game etc etc

    :param key KeyCode: Key class
    :returns dict: Player entity action
    """

    if not key:
        return {}

    try:
        key = key.char
    except Exception:
        key = str(key).lower()

    if key in keydict.keys():
        return keydict[key]

    return {}