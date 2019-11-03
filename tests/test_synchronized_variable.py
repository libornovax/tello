#!/usr/bin/env python

import unittest

from tello.synchronized_variable import SynchronizedVariable


class TestSynchronizedVariable(unittest.TestCase):

    def setUp(self):
        self.synchronized_variable = SynchronizedVariable({"a": 10})

    def test_initial_value_is_correctly_set(self):
        self.assertEqual(self.synchronized_variable.value, {"a": 10})

    def test_setter_correctly_sets_value(self):
        self.synchronized_variable.value = "unicorn"
        self.assertEqual(self.synchronized_variable.value, "unicorn")

    def test_returned_value_is_not_changed_by_setter(self):
        value = self.synchronized_variable.value
        self.assertEqual(value, {"a": 10})

        # Set the synchronized variable value to a new value
        self.synchronized_variable.value = {"a": 20}

        self.assertEqual(value, {"a": 10})
        self.assertEqual(self.synchronized_variable.value, {"a": 20})


if __name__ == "__main__":
    unittest.main()
