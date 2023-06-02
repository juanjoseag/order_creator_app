from flask import abort


def or_400(object):
    if object is not None:
        return object
    abort(400)


class EmptyObject:
    def __getattr__(self, attr):
        if attr == "id":
            return -1
        return ""

    def __setattr__(self, attr, value):
        pass
