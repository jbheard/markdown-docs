import sys
import os.path as path
import yaml

class Tag(object):
    """
    Represents a tag (prefixed with '@')
    """
    _tags = []

    def __init__(self, obj):
        """
        @param obj the yaml object to parse the tag from.
               must have syntax and collection fields
        """
        items = obj['syntax'].split()
        self.maxsplit = len(items)-1
        self.tag = items[0]
        self.syntax = items[1:]
        self.collection = obj['collection']

    def parse_string(self, string):
        parts = string.split(maxsplit=self.maxsplit)
        if parts[0] != self.tag:
            return None
        
        if len(parts) <= self.maxsplit:
            raise Exception("Error parsing docstring for {} at {}"
                .format(context, line))

        # Don't need a dict for 1D tags
        if len(parts) == 2:
            return parts[1]

        tag = { self.syntax[i-1] : parts[i] for i in range(1, len(parts)) }
        return tag

    @staticmethod
    def parse(string):
        for tag in Tag._tags:
            result = tag.parse_string(string)
            if result is not None:
                return tag.collection, result
        return None, None

    @staticmethod
    def load_tags(yaml_path, static=False):
        """
        Loads a list of tags from a yaml file into a 
        static list Tag._tags
        @param yaml_path Path to the yaml file to load tags from
        @param static True to load the templates from the application path, False to load normally
        @return a list of tags from the yaml file
        """
        if static:
            root = path.dirname(sys.argv[0])
            yaml_path = path.join(root, yaml_path)
        with open(yaml_path, 'r') as f:
            obj = yaml.safe_load(f.read())
        tags = []
        for tag in obj:
            tags.append( Tag(tag) )
        Tag._tags.extend(tags)
        return tags
