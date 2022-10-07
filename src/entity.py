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


import src.tiles as tiles
from random import randint
from src.core import *
from src.sword import *

class Entity():
    """
    Entity(entity id, dungeon, icon, x position, y position, health, move speed, color, damage) -> nothing

    Class that depicts an Entity

    :param ent_id int: Entity Identifier
    :param dungeon map.Map: Dungeon map
    :param icon str: Player icon
    :param xpos int | None: X position
    :param ypos int | None: Y position
    :param health int: Health of the entity
    :param movespeed int: Movespeed of the entity
    :param color tuple: (red, green blue)
    :param damage tuple or int: Damage
    :returns object: The Entity object
    """

    def __init__(
        self, 
        ent_id: int, 
        dungeon, 
        icon: str, 
        xpos: int = 1, 
        ypos: int = 1, 
        health: int = 100, 
        movespeed:int = 1, 
        color:tuple = (255, 255, 255),
        damage: tuple | int = (25, 35),
        ) -> None:

        self.identifier = 1 # all entities have this as identifier
        self.id = ent_id
        self.map = dungeon
        self.icon = icon
        self.xpos = xpos
        self.ypos = ypos
        self.health = health
        self.max_health = self.health
        self.movespeed = movespeed
        self.color = color
        self.damage = damage

        self.old_xpos = self.old_ypos = 0
        self.viewpos = 'right'
        self.current_item = 'sword'
        self.is_walkable = False # prevent player from waking over other entities

        core.entities.append(self)
    
    def update(self) -> None:
        """
        update() -> nothing

        Gets called by the main loop, checks for health and other stuff

        :returns None: Nothing
        """

        if self.health < 0:
            core.entities.remove(self)
    
    def collision_check(self, xpos, ypos) -> bool:
        """
        collision_check(x position, y position) -> status

        Checks if the current entity is colliding with something or someone

        :param xpos int: X position
        :param ypos int: Y position
        :returns bool: True if we are colliding, False if not
        """

        current_ent = self.map.get_entity(xpos, ypos) # for debugging purposes
        core.current_ent = current_ent # for debugging purposes
        
        # damage the entity if the id is 2 (player), damage it
        if self.id == 2:
            if current_ent.damage != (0, 0):

                damage_min, damage_max = current_ent.damage
                damage_final = randint(damage_min, damage_max)

                self.health -= damage_final # subtract the damage from the players health

        if current_ent.identifier == 0: # if we are walking over a tile
            if current_ent.id == tiles.trigger.id: # trigger the trigger
                core.trigger = True
            
            elif current_ent.id == tiles.finish.id: # if we hit the finish
                core.finished = True

        else:
            # if the entity we are colliding with is not a tile  
            if current_ent.id == 6 and self.id != 6: # powerups
                # TODO: fix quirky behavior
                self.health += current_ent.health
                self.damage += current_ent.damage
                
                # and now, make sure it won't be able to heal or damage us anymore
                current_ent.health = 0
                current_ent.damage = (0, 0)
                current_ent.icon = tiles.floor.icon
                current_ent.color = tiles.floor.color

                self.map.map[current_ent.ypos][current_ent.xpos] = tiles.floor # overwrite it with a floor
                core.entities.remove(current_ent)

                return False

            elif current_ent.id == 4: # sword impact
                if self.id != 2: # make sure the player doesn't get hit by his own sword
                    damage_min, damage_max = current_ent.damage
                    damage_final = randint(damage_min, damage_max)

                    self.health -= damage_final
                
                # block movement
                return True
        
        # check if the current entity is walkable
        # if not, we return a collision
        # if it is walkable, we can walk right through it
        return False if current_ent.is_walkable else True
    
    def move(self, x, y) -> None:
        """
        move(new x position, new y position) -> nothing

        Moves the current entity to the new x an y positions

        :param x int: New X position
        :param y int: New Y position
        :returns None: Nothing
        """

        x, y = x * self.movespeed, y * self.movespeed
        newx, newy = self.xpos + x, self.ypos + y

        if self.collision_check(newx, newy):
            return

        self.old_xpos = self.xpos
        self.old_ypos = self.ypos

        self.xpos += x
        self.ypos += y