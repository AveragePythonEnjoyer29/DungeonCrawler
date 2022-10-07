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

from src.core import core

class Tile():
    """
    Tile(icon, entity id, is walkable, color, damage) -> tile

    Creates a tile from the given arguments

    :param icon str: Tile icon
    :param ent_id int: Tile ID
    :param is_walkable bool: Is the tile walkable?
    :param color tuple: (Red, Green, Blue)
    :param damage tuple: (Damage min, damage max)
    :returns object: The tile
    """

    def __init__(self, icon, ent_id, is_walkable, color=(255, 255, 255), damage=(0, 0)) -> None:
        self.identifier = 0 # all tiles have this as identifier
        self.icon = icon
        self.id = ent_id
        self.is_walkable = is_walkable
        self.color = color
        self.damage = damage

        core.tiles.append(self)

wall = Tile('#', 1, False)
floor = Tile(' ', 0, True)
trigger = Tile(' ', 9, True)
lava = Tile('#', 10, False, (255, 127, 0), (1, 10))
trap = Tile('%', 12, True, (105, 105, 105), (20, 50))
finish = Tile('*', 11, False, (255, 0, 127))