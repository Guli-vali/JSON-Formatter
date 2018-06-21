SCHEMA = {'$schema': 'http://json-schema.org/draft-04/schema#',
    'additionalProperties': False,
    'definitions': {'name': {'additionalProperties': False,
                                'patternProperties': {'^_[a-zA-Z]([^.]+)$': {'$ref': '#/definitions/extension'}},
                                'properties': {
                                               'title': {'description': 'Specifies the type of the attachment, such as "audio/mpeg".',
                                                             'type': 'string'},
                                               },
                                'required': ['title'],
                                'type': 'object'},},
    'weight': {'type': 'number'},
    }

