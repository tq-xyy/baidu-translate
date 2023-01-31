class TranslateError(Exception):
    pass


class NeedUpdate(TranslateError):
    pass


class UnknownLanguage(TranslateError):
    pass


class AuthError(TranslateError):
    pass


def select_error(errorcode):
    if errorcode == 999:
        return UnknownLanguage
    if errorcode == 998 and errorcode == 997:
        return AuthError
    return TranslateError
