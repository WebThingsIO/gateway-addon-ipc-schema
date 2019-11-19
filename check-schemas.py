#!/usr/bin/env python3

import glob
import json
import jsonschema
import os
import sys

_BASE = os.path.realpath(os.path.dirname(__file__))


def main():
    files = [os.path.join(_BASE, 'schema.json')]
    files.extend(glob.glob(os.path.join(_BASE, 'messages', '*.json')))
    ids = {}

    for fname in files:
        try:
            with open(fname, 'rt') as f:
                schema = json.load(f)
        except (OSError, IOError, ValueError) as e:
            print('Error parsing file:', fname)
            print(e)
            sys.exit(1)

        try:
            jsonschema.Draft7Validator.check_schema(schema)
        except jsonschema.SchemaError as e:
            print('Error in schema:', fname)
            print(e)
            sys.exit(1)

        if not os.path.basename(fname) == 'schema.json' and \
                not os.path.basename(fname) == 'definitions.json':
            _id = schema['properties']['messageType']['const']

            if _id in ids:
                print('Duplicate id: {}'.format(_id))
                print('  {}'.format(ids[_id]))
                print('  {}'.format(fname))
                sys.exit(1)

            ids[_id] = fname


if __name__ == '__main__':
    main()
