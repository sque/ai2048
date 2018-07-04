from itertools import chain


class GameStatistics():
    pass


class Board(object):
    """
    Board representation of 2048 game
    """

    SIZE = 4

    def __init__(self, starting_tiles=None):

        if starting_tiles is None:
            # Column major 2D array
            self.tiles = [[None] * self.SIZE] * self.SIZE
        else:
            # Check that starting board is valid
            if len(starting_tiles) != self.SIZE:
                raise ValueError("Starting tiles must be {sz}×{sz}".format(sz=self.SIZE ))
            for col in starting_tiles:
                if not isinstance(col, list) or len(col) != 4:
                    raise ValueError("Starting tiles must be {sz}×{sz}".format(sz=self.SIZE ))
            self.tiles = starting_tiles

    @staticmethod
    def _combine_elements_to_beginning(elements):
        """
        Combine a line of elements in the begining of the array
        :param list[T] elements: A list of elements to combine
        :return:
        """

        for current_index in range(0, len(elements) -2):
            previous_index = current_index + 1
            if elements[current_index] is None:
                continue
            if elements[current_index] == elements[previous_index]:
                elements[current_index] *= 2
                elements = elements[:current_index + 1] + elements[previous_index + 1:] + [None]
        return elements

    def move_left(self):
        """
        Get a new board that has been moved leftwards
        :return:
        """

        from copy import deepcopy
        new_tiles = deepcopy(self.tiles)

        for irow in range(0, self.SIZE - 1):
            new_tiles[irow] = deepcopy(self._combine_elements_to_beginning(self.tiles[irow]))

        return Board(starting_tiles=new_tiles)

    def move_right(self):
        """
        Get a new board that has been moved leftwards
        :return:
        """


        for row in range(0, self.SIZE - 1):
            for col in range(self.SIZE - 1, 0, -1):
                prev_col = col - 1
                if self.tiles[col][row] == self.tiles[prev_col][row]:
                    self.tiles[col][row] = None
                    self.tiles[prev_col][row] *= 2

    @property
    def max_tile(self):
        """
        Calculate the maximum tile number in the board
        :rtype: int
        """
        occupated_tiles = [
            t
            for t in self.flat_tiles
            if t is not None
        ]
        if not occupated_tiles:
            return None  # All tiles are none
        return max(occupated_tiles)

    @property
    def flat_tiles(self):
        """
        Get a copy of board tiles in a flat format following x1y1, x1y2, x1y3, x1y4, x2y1...
        :rtype: list

        """
        return list(chain(*self.tiles))

    def __eq__(self, other):
        return self.flat_tiles == other.flat_tiles

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return repr(self.tiles)


class Game(object):

    def __init__(self):
        self.board = Board()
        self.statistics_ = {
            'moves': 0,
            'max_title': 2
        }


    def move_left(self):
        self.board.move_left()
        self.statistics_['moves'] += 1
