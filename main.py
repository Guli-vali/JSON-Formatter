import sys
import json

from validator import validate_input, errors_ftm, Errors

if __name__ == '__main__':
    data = json.load(sys.stdin, parse_float=True)
    errors = validate_input(data)
    if not errors:
        print(errors_ftm(data, Errors(errors)))
    else:
        print(data)
