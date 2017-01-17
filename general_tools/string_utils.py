from __future__ import unicode_literals


def try_parse_int(string_to_parse):
    """

    :param str|unicode string_to_parse:
    :return: (bool, int)
    """
    try:
        parsed_int = int(string_to_parse)
        return True, parsed_int

    except ValueError:
        return False, None
