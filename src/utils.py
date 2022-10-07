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

from colorama import Fore

def calculate_health(health, max_health) -> tuple:
    """
    calculate_health(health, max health) -> (health bar, percent)

    Creates a colored healthbar from the given health and max health

    :param health int: Health of the entity
    :param max_health int: Max health of the entity
    :returns tuple: (Health bar, percent left)
    """

    zero_counter = int(max_health/10) # max 10 0's
    current_zeros = int(health/zero_counter)
    remaining = 10 - current_zeros
    
    if health < 50: color = Fore.YELLOW
    elif health < 25: color = Fore.RED
    else: color = Fore.GREEN
    
    percent = str(int((health/max_health)*100)) + '%'
    
    return f'{color}{"0"*current_zeros}{Fore.LIGHTBLACK_EX}{"0"*remaining}{Fore.RESET}', percent

def clear() -> None:
    """
    clear() -> nothing

    Clears the screen, thats it

    :returns None: Nothing
    """

    try:
        print("\033c", end="")
    except Exception:
        print('\n'*200)