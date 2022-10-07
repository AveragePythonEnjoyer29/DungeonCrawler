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

import time
from random import randint

class Sword():
    """
    Sword(map, owner entity) -> sword

    Creates a sword entity for the master entity

    :param map Map: Map to play on
    :param owner_ent Entity: Owner entity
    :returns object: the sword!
    """

    def __init__(self, dungeon, owner_ent):
        self.map = dungeon
        self.damage = owner_ent.damage

        self.id = 4
        self.icon = '-'
        self.color = (255, 255, 255)
        self.xpos = self.ypos = 0
        self.old_xpos = self.old_ypos = 0
    
    def swing(self, entity) -> None:
        """
        swing(master entity) -> nothing

        Swings the sword, and calculates the view position by using the master entity's x and y pos

        :param entity object: Master entity
        :returns None: Nothing
        """

        # calculate view position
        xpos = entity.xpos
        ypos = entity.ypos

        if entity.viewpos == 'up': ypos = entity.ypos - 1
        elif entity.viewpos == 'down': ypos = entity.ypos + 1
        elif entity.viewpos == 'left': xpos = entity.xpos - 1
        elif entity.viewpos == 'right': xpos = entity.xpos + 1
        
        # get the tile we will overwrite with the sword
        old_ent = self.map.map[ypos][xpos]
        if old_ent.id == 1: # don't overwrite walls
            return 

        # calculate damage, ignores damage if the current tile is empty
        damage_min, damage_max = self.damage
        damage_final = randint(damage_min, damage_max)

        if old_ent.id != 0:
            old_ent.health -= damage_final

        # display the sword
        self.map.update(
            xpos,
            ypos,
            self
        )

        # then remove it 10 ms afterwards
        time.sleep(0.10)
        self.map.update(
            xpos,
            ypos,
            old_ent
        )