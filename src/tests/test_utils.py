import unittest
from unittest import mock

import utils
from tag import Tag

TAG_YAML_DATA = '''
- syntax: "@param name description"
  collection: params
- syntax: "@author author"
  collection: authors
'''

class TestUtils(unittest.TestCase):
    def tearDown(self):
        Tag._tags = []

    # Helper to load tags
    def load_tags(self, yaml_str):
        with mock.patch("builtins.open", mock.mock_open(read_data=yaml_str)) as open_patch:
            Tag.load_tags('path/to/tags.yaml')
        open_patch.assert_called_with('path/to/tags.yaml', 'r')

    @mock.patch('os.walk')
    def test_get_all_files(self, walk_patch):
        walk_patch.return_value = (
            ('dir1', '', ['file.py', 'file.txt']),
            ('dir2', '', ['FILE.PY', 'file2.py', 'file']),
        )

        files = utils.get_all_files('./', '.py')

        self.assertEqual(files, ['dir1/file.py', 'dir2/FILE.PY', 'dir2/file2.py'])
        walk_patch.assert_called_once_with('./')

    def test_parse_docstring(self):
        lines = ['line 1', 'line 2', '', '@param param1 description for param1', '@param param2 desc2', '@author AUTHOR 1', '@author author 2']
        docstring = '\n'.join(lines)
        expected = {
            'description': 'line 1 line 2   \n',
            'authors': ['AUTHOR 1', 'author 2'],
            'params': [
                {'name': 'param1', 'description': 'description for param1'},
                {'name': 'param2', 'description': 'desc2'},
            ],
        }

        self.load_tags(TAG_YAML_DATA)
        result = utils.parse_docstring(docstring, 'ctx')

        self.assertEqual(result, expected)
