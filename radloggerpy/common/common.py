from collections.abc import Sequence


def seq_but_not_str(obj):
    """Determines if object is a collection but not a string or byte array"""
    return isinstance(obj, Sequence) and not isinstance(obj, (str, bytes, bytearray))
