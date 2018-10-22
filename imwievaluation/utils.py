from unidecode import unidecode


def clean_string(string):
    # only allow alphanumeric ascii characters
    clean_string = ''.join(ch for ch in string if (ch.isalnum()
                                                   or (ch == ' ')))
    clean_string = unidecode(clean_string)
    return clean_string


def get_or_create(session, model, **kwargs):
    """ Get object from database or create if it does not exist yet.
    See https://stackoverflow.com/questions/2546207/does-sqlalchemy-have-an-equivalent-of-djangos-get-or-create
    """
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def escape_latex_special_characters(string):
    special_characters = ['&', '%', '$', '#', '_', '{', '}', '~', '^']
    # TODO: Maybe \ could be a problem too...
    # escape with '\' to prevent errors in LaTeX for free text answers
    for special_character in special_characters:
        string = string.replace(special_character, '\%s' % special_character)
    return string


def filter_dict(dict, filter=[]):
    """ Only keep entrys with keys given in filter. 
    If filter is an empty list, an empty dict will be returned.
    
    """
    return {key: dict[key] for key in filter}


def sort_dicts(dicts, sort_by):
    """
    
    :param dicts: list of dictionaries
    :param sort_by: key by which the list should be sorted
    :return: sorted list of dicts
    """
    return sorted(dicts, key=lambda k: k[sort_by])


def filter_and_sort_dicts(dicts, sort_by, filter):
    filtered_dicts = []
    for dict in sort_dicts(dicts, sort_by):
        filtered_dicts.append(filter_dict(dict, filter))
    return filtered_dicts
