import yaml

class Tag(object):
    """
    Represents a tag (prefixed with '@')
    """
    _tags = []
    YAML_REQUIRED = ('syntax', 'collection')

    def __init__(self, obj):
        """
        @param obj the yaml object to parse the tag from.
               must have syntax and collection fields
        """
        if any(required not in obj for required in Tag.YAML_REQUIRED):
            raise ValueError(f'Invalid yaml, the following are required: {Tag.YAML_REQUIRED}')

        items = obj['syntax'].split()
        self.maxsplit = len(items)-1
        self.tag = items[0]
        self.syntax = items[1:]
        self.collection = obj['collection']

    def parse_string(self, string: str, context: str) -> None|str|dict[str, list[str]]:
        parts = string.split(maxsplit=self.maxsplit)
        if parts[0] != self.tag:
            return None

        if len(parts) <= self.maxsplit:
            raise ValueError(f'Error parsing {self.tag} for {context}')

        # Don't need a dict for 1D tags
        if len(parts) == 2:
            return parts[1]

        tag = { self.syntax[i-1] : parts[i] for i in range(1, len(parts)) }
        return tag

    @staticmethod
    def parse(string: str, context: str):
        for tag in Tag._tags:
            result = tag.parse_string(string, context)
            if result is not None:
                return tag.collection, result
        return None, None

    @staticmethod
    def load_tags(yaml_path: str):
        """
        Loads a list of tags from a yaml file into the static list Tag._tags
        @param yaml_path Path to the yaml file to load tags from
        @return a list of tags from the yaml file
        """
        with open(yaml_path, 'r') as f:
            obj = yaml.safe_load(f.read())

        if obj is None:
            raise ValueError(f'Failed to load tags from "{yaml_path}"')

        tags = []
        for tag in obj:
            tags.append(Tag(tag))
        Tag._tags.extend(tags)
        return tags
