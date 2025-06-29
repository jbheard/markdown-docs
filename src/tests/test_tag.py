import unittest
from unittest import mock

from tag import Tag

YAML_DATA = '''
- syntax: "@param name description"
  collection: params
- syntax: "@author author"
  collection: authors
'''

YAML_DATA_BAD_FORMAT = '''
- syntax: "@param name description"
- syntax: "@author author"
'''

class TestTag(unittest.TestCase):
    def tearDown(self):
        Tag._tags = []

    # Helper to load tags
    def load_tags(self, yaml_str):
        with mock.patch("builtins.open", mock.mock_open(read_data=yaml_str)) as open_patch:
            Tag.load_tags('path/to/tags.yaml')
        open_patch.assert_called_with('path/to/tags.yaml', 'r')

    def test_load_tags(self):
        self.load_tags(YAML_DATA)

        self.assertEqual(len(Tag._tags), 2)

        self.assertEqual(Tag._tags[0].tag, '@param')
        self.assertEqual(Tag._tags[0].syntax, ['name', 'description'])
        self.assertEqual(Tag._tags[0].collection, 'params')

        self.assertEqual(Tag._tags[1].tag, '@author')
        self.assertEqual(Tag._tags[1].syntax, ['author'])
        self.assertEqual(Tag._tags[1].collection, 'authors')

    def test_load_tags_empty_file(self):
        with self.assertRaises(ValueError):
            self.load_tags('')
        self.assertEqual(len(Tag._tags), 0)

    def test_load_tags_bad_format(self):
        with self.assertRaises(ValueError):
            self.load_tags(YAML_DATA_BAD_FORMAT)
        self.assertEqual(len(Tag._tags), 0)

    def test_parse_dict_tag(self):
        self.load_tags(YAML_DATA)
        collection, result = Tag.parse('@param NAME DESC', '')

        self.assertEqual(collection, 'params')
        self.assertEqual(result, {'name': 'NAME', 'description': 'DESC'})

    def test_parse_str_tag(self):
        self.load_tags(YAML_DATA)
        collection, result = Tag.parse('@author NAME', '')

        self.assertEqual(collection, 'authors')
        self.assertEqual(result, 'NAME')

    def test_parse_tag_missing(self):
        self.load_tags(YAML_DATA)
        collection, result = Tag.parse('@not-a-tag param1 param2', '')

        self.assertEqual(collection, None)
        self.assertEqual(result, None)

    def test_parse_tag_bad_format(self):
        self.load_tags(YAML_DATA)

        with self.assertRaises(ValueError) as cm:
            Tag.parse('@param NAME', 'class.function')
        self.assertEqual(cm.exception.args, ('Error parsing @param for class.function',))
