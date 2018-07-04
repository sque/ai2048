import unittest
import os
import json

from ai2048.engine import Board


class BoardTestCase(unittest.TestCase):

    def setUp(self):
        boards_json = os.path.join(
            os.path.dirname(__file__),
            'fixtures',
            'boards.json'
        )
        with open(boards_json) as fp:
            self.test_boards = json.load(fp)

        # Replace -1 on boards to None
        for name, board in self.test_boards.items():
            self.test_boards[name] = list(map(
                lambda row: list(map(
                    lambda cell: None if cell == -1 else cell,
                    row)),
                board
            ))

    def test_construction(self):

        # Construct an empty board
        brd = Board()
        self.assertIsNone(brd.max_tile)
        self.assertEqual(brd.flat_tiles,
                         [None] * 16)

        # Construct with a false map
        with self.assertRaises(ValueError):
            brd = Board([1,2,3,4])

        # Construct with a custom map
        brd = Board([
            [None, None, 2, None],
            [None, None, 2, None],
            [None, None, None, None],
            [None, 1024, None, None],
        ])
        self.assertEqual(brd.max_tile, 1024)
        self.assertEqual(brd.flat_tiles, [
            None, None, 2, None,
            None, None, 2, None,
            None, None, None, None,
            None, 1024, None, None,
        ])

    def test_comparison(self):

        # Compare empty boards
        b1 = Board()
        b2 = Board()
        self.assertIsNot(b1, b2)
        self.assertEqual(b1, b2)
        self.assertTrue(b1 == b2)
        self.assertFalse(b1 != b2)

        # Compare two different boards
        b1 = Board()
        b2 = Board([
            [None, None, 2, None],
            [None, None, 2, None],
            [None, None, None, None],
            [None, 1024, None, None],
        ])
        self.assertNotEqual(b1, b2)
        self.assertIsNot(b1, b2)
        self.assertFalse(b1 == b2)
        self.assertTrue(b1 != b2)

    def test_combine_elemenets_to_beginning(self):

        a = [2, 2, 2, None]
        self.assertListEqual(
            Board._combine_elements_to_beginning(a),
            [4, 2, None, None]
        )

        a = [None, None, None, None]
        self.assertListEqual(
            Board._combine_elements_to_beginning(a),
            [None, None, None, None]
        )

        a = [16, 8, 8, 8]
        self.assertListEqual(
            Board._combine_elements_to_beginning(a),
            [16, 16, 8, None]
        )

    def test_movements(self):

        board_names = ['crowded_1', 'crowded_2']
        for board_name in board_names:

            b1 = Board(starting_tiles=self.test_boards[board_name])
            print(b1.move_left())

            self.assertEqual(
                b1.move_left(),
                Board(starting_tiles=self.test_boards["{}_left".format(board_name)])
            )

if __name__ == '__main__':
    unittest.main()
