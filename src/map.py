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
from src.core import core

class Map():
    """
    Map() -> the map class

    Creates a map

    :returns object: The map class
    """

    def __init__(self):
        # hardcoded map
        self.map = [
            [tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall],
            [tiles.wall, tiles.floor, tiles.floor, tiles.floor, tiles.floor, tiles.floor, tiles.floor, tiles.floor, tiles.floor, tiles.wall, tiles.floor, tiles.floor, tiles.floor, tiles.floor, tiles.floor, tiles.floor, tiles.floor, tiles.wall],
            [tiles.wall, tiles.floor, tiles.floor, tiles.floor, tiles.floor, tiles.floor, tiles.floor, tiles.floor, tiles.floor, tiles.wall, tiles.floor, tiles.floor, tiles.floor, tiles.floor, tiles.floor, tiles.floor, tiles.floor, tiles.wall],
            [tiles.wall, tiles.floor, tiles.floor, tiles.floor, tiles.floor, tiles.floor, tiles.floor, tiles.floor, tiles.floor, tiles.wall, tiles.floor, tiles.floor, tiles.floor, tiles.floor, tiles.floor, tiles.floor, tiles.floor, tiles.wall],
            [tiles.wall, tiles.floor, tiles.floor, tiles.floor, tiles.floor, tiles.floor, tiles.floor, tiles.floor, tiles.floor, tiles.floor, tiles.floor, tiles.floor, tiles.floor, tiles.floor, tiles.floor, tiles.floor, tiles.floor, tiles.wall],
            [tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.lava, tiles.trigger, tiles.lava, tiles.wall],
            [tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.lava, tiles.floor, tiles.lava, tiles.wall],
            [tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.lava, tiles.floor, tiles.lava, tiles.wall],
            [tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.lava, tiles.floor, tiles.lava, tiles.wall],
            [tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall, tiles.wall],
        ]
    
    def parse(
        self,
        json_map: dict
        ) -> list:
        """
        parse(map json data) -> parsed map

        Parses the map data from a dictionary

        :param json_map dict: Dictionary holding map data
        :returns list: Parsed map array
        """

        data = json_map['map']
        result = []
        for row in data:
            tmp_rows = [] # temp list holding the tiles

            for tile in row:
                for created_tile in core.tiles:

                    # if the tile id matches the id stored in the json array
                    # we append the actual tile object
                    if created_tile.id == tile: 
                        tmp_rows.append(created_tile)
                
                for created_ent in core.entities:

                    # same as above, but with entities
                    if created_ent.id == tile:
                        tmp_rows.append(created_ent)
            
            result.append(tmp_rows)
            
        return result
    
    def get_entity(
        self, 
        xpos: int,
        ypos: int
        ) -> object:
        """
        get_entity(x position, y position) -> object

        Gets the entity from the given x and y position

        :param xpos int: X position
        :param ypos int: Y position
        :returns object: The tile or entity
        """

        return self.map[ypos][xpos]
    
    def update(
        self,
        xpos: int,
        ypos: int,
        entity
        ) -> None:
        """
        update(x position, y position, entity object) -> nothing

        Updates the given x and y position to the entity

        :param xpos int: X position
        :param ypos int: Y position
        :param entity object: Entity class
        :returns None: Nothing
        """
        
        try:
            self.map[entity.old_ypos][entity.old_xpos] = tiles.floor
        except Exception:
            pass

        self.map[ypos][xpos] = entity
    
    def make_colored(
        self,
        icon: str,
        rgb: tuple
        ) -> str:
        """
        make_colored(icon, rgb color code) -> colored ansi string

        Creates an ANSI code from the given R, G and B codes

        :param icon str: Entity icon
        :param rgb tuple: (Red, Green and Blue)
        :returns str: The ANSI colored string
        """

        r, g, b = rgb

        return f'\033[38;2;{r};{g};{b}m{icon}\033[0m'

    def make(self) -> str:
        """
        make() -> map

        Creates a map, with all the icons and tiles

        :returns str: The map
        """

        formatted_map = []
        for row in self.map:
            tmp_rows = []

            for tile in row:

                # hard fix for immortal entities
                if tile.id == 3:
                    if tile.health > 0:
                        tmp_rows.append(self.make_colored(
                            tile.icon, 
                            tile.color
                        ))

                    else:
                        tmp_rows.append(self.make_colored(
                            tiles.floor.icon, 
                            tiles.floor.color
                        ))

                        self.get_entity(
                            tile.xpos, 
                            tile.ypos
                        ).damage = (0, 0) # set the damage to 0

                        self.map[tile.ypos][tile.xpos] = tiles.floor # overwrite the dead entity with a floor

                else:      
                    tmp_rows.append(self.make_colored(tile.icon, tile.color))

            formatted_map.append(tmp_rows)
            
        return "\n".join(["".join(row) for row in formatted_map])