import re
import json

from collections import defaultdict

from jsonschema import Draft4Validator
from jsonschema.exceptions import relevance
from schema import SCHEMA

json_validator = Draft4Validator(SCHEMA)


class Errors(object):
    """
    Checking which validators failed.
    """

    def __init__(self, errors=()):
        self.errors = defaultdict(list)
        self._contents = defaultdict(self.__class__)

        for error in errors:
            container = self
            for element in error.path:
                container = container[element]
            container.errors[error.validator] += [error]

            container._instance = error.instance

    def __contains__(self, index):
        """
        Check ``instance[index]`` has errors.
        """

        return index in self._contents

    def __getitem__(self, index):

        if index not in self:
            self._instance[index]

        return self._contents[index]

    def __setitem__(self, index, value):
        self._contents[index] = value

    def __iter__(self):

        return iter(self._contents)

    def __repr__(self):
        return "<%s (%s total errors)>" % (self.__class__.__name__, len(self))


def validate_input(feed):
    errors = json_validator.iter_errors(feed)
    errors = sorted(errors, key=relevance, reverse=True)
    errors = (error for error in errors if not error.context)

    return list(errors)


def validate_str(json_str):
    data = json.loads(json_str)
    validate_input(data)


def shape(path, value):

    container = {
        path.pop(): value
    }

    for part in reversed(path):
        _container = {
            part: container
        }
        container = _container

    return container


PARSER = re.compile(r"u'(.*)' is a required property")


def format_message(error):
    if error.validator == 'required':
        key = PARSER.match(error.message).items[0]
        return "A schema must %s is a required property" % key


def errors_ftm(instance, error_tree):
    context = {}

    if isinstance(instance, dict):
        for key, val in instance.items():
            try:
                context[key] = errors_ftm(val, error_tree[key])
            except Exception as err:
                print("Error {}".format(err))

    else:
        for i, val in enumerate(instance):
            try:
                context[i] = errors_ftm(val, error_tree[i])
            except Exception as err:
                print("Error {}".format(err))

    if error_tree.errors:
        context["errors"] = {
            key: [e.message for e in val] for key, val in error_tree.errors.items()
        }

    return context
