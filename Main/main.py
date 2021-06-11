from django.http import HttpResponseRedirect
from FakeCSV.settings import DEFAULT_LOGIN_PAGE


def check_authorize(fun):
    def decorator(*args):
        if len(args) == 0:
            raise Exception('no request in func arguments')
        request = args[0]
        if not request.user.is_authenticated:
            return HttpResponseRedirect(DEFAULT_LOGIN_PAGE)
        return fun(*args)
    return decorator
