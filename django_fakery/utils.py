def language_to_locale(language):
    """
    Converts django's `LANGUAGE_CODE` settings to a proper locale code.
    """
    tokens = language.split('-')
    if len(tokens) == 1:
        return tokens[0]
    return "%s_%s" % (tokens[0], tokens[1].upper())
