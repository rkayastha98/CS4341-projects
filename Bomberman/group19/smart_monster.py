import sys
sys.path.insert(0, '../bomberman')
from entity import MonsterEntity

class SmartMonster(MonsterEntity):
    """A random monster that walks away from explosions"""

    def __init__(self, monster, rnge):
        self.dx = monster.dx
        self.dy = monster.dy
        self.x = monster.x
        self.y = monster.y
        self.rnge = rnge

    def look_for_character(self, wrld):
        for dx in range(-self.rnge, self.rnge+1):
            # Avoid out-of-bounds access
            if ((self.x + dx >= 0) and (self.x + dx < wrld.width())):
                for dy in range(-self.rnge, self.rnge+1):
                    # Avoid out-of-bounds access
                    if ((self.y + dy >= 0) and (self.y + dy < wrld.height())):
                        # Is a character at this position?
                        if (wrld.characters_at(self.x + dx, self.y + dy)):
                            return (True, dx, dy)
        # Nothing found
        return (False, 0, 0)

    def must_change_direction(self, wrld):
        # Get next desired position
        (nx, ny) = self.nextpos()
        # If next pos is out of bounds, must change direction
        if ((nx < 0) or (nx >= wrld.width()) or
            (ny < 0) or (ny >= wrld.height())):
            return True
        # If these cells are an explosion, a wall, or a monster, go away
        return (wrld.explosion_at(self.x, self.y) or
                wrld.wall_at(nx, ny) or
                wrld.monsters_at(nx, ny) or
                wrld.exit_at(nx, ny))

    def look_for_empty_cell(self, wrld):
        # List of empty cells
        cells = []
        # Go through neighboring cells
        for dx in [-1, 0, 1]:
            # Avoid out-of-bounds access
            if ((self.x + dx >= 0) and (self.x + dx < wrld.width())):
                for dy in [-1, 0, 1]:
                    # Avoid out-of-bounds access
                    if ((self.y + dy >= 0) and (self.y + dy < wrld.height())):
                        # Is this cell safe?
                        if(wrld.exit_at(self.x + dx, self.y + dy) or
                           wrld.empty_at(self.x + dx, self.y + dy)):
                            # Yes
                            cells.append((dx, dy))
        # All done
        return cells

    def get_actions(self, wrld):
        """Pick an action for the monster"""
        # If a character is in the neighborhood, go to it
        (found, dx, dy) = self.look_for_character(wrld)
        if found and not self.must_change_direction(wrld):
            return [(dx, dy)]
        # If I'm idle or must change direction, change direction
        if ((self.dx == 0 and self.dy == 0) or
            self.must_change_direction(wrld)):
            # Get list of safe moves
            safe = self.look_for_empty_cell(wrld)
            if not safe:
                # Accept death
                return [(0, 0)]
            else:
                # Pick a move at random
                return safe
        else:
            return [(self.dx, self.dy)]