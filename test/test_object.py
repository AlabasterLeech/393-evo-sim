import unittest
from src.Object import Object


class ObjectTest(unittest.TestCase):
    def setUp(self):
        x = 0
        y = 0
        obj_type = 'food'
        density = 0.75
        self.obj = Object(x, y, obj_type, density)

    def test_get_state(self):
        state = {'x': 0,
                 'y': 0,
                 'object_type': 'food',
                 'density': 0.75}
        msg = 'Not the same state!'
        self.assertEqual(state, self.obj.get_state(), msg)

    def test_set_state(self):
        state = {'x': 2,
                 'y': 3,
                 'object_type': 'obstacle',
                 'density': 1}
        msg = 'State was not updated!'
        self.obj.set_state(state)
        self.assertEqual(state['x'], self.obj.get_state()['x'], msg)


if __name__ == '__main__':
    unittest.main()
