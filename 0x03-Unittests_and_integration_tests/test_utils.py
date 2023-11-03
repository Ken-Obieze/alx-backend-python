#!/usr/bin/env python3
"""Module containing unit tests for utils.access_nested_map function."""
import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from unittest.mock import patch, Mock


class TestAccessNestedMap(unittest.TestCase):
    """TestAccessNestedMap class."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(
            self, nested_map: Dict,
            path: Tuple[str], expected: Union[int, Dict]
            ) -> None:
        """
        Test access to nested map
        Args:
            nested_map (Dict): nested dictionary
            path (Tuple): tuple of possible dictionary keys
            expected (int | Dict): expected result of tested function
        Returns:
            None
        """
        self.assertEqual(
            expected,
            access_nested_map(nested_map, path)
        )

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(
            self, nested_map: Dict, path: Tuple[str]
            ) -> None:
        """
        Test if an exception is correctly raised
        Args:
            same as described above
        Returns:
            None
        """
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)

class TestGetJson(unittest.TestCase):
    """TestGetJson class."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """Test for get_json function."""
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)

        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)

class TestMemoize(unittest.TestCase):
    """TestMemoize class."""

    class TestClass:
        def a_method(self):
            return 42

        @memoize
        def a_property(self):
            return self.a_method()

    @patch('utils.TestMemoize.TestClass.a_method')
    def test_memoize(self, mock_a_method):
        """Test memoize decorator."""
        mock_a_method.return_value = 42

        test_obj = self.TestClass()

        result_1 = test_obj.a_property
        result_2 = test_obj.a_property

        mock_a_method.assert_called_once()
        self.assertEqual(result_1, 42)
        self.assertEqual(result_2, 42)
