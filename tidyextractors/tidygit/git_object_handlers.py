import git


# All handlers have the following pattern:
#   handler(name,object) => dictionary of attributes
#   attributes in the dict will become values in rows
#   of the output dataframe.


def handle_stats(name, obj):
    """
    Stats object handler.
    :param name: Unused String
    :param obj: GitPython Stats
    :return: Dictionary of attributes.
    """
    return {'total_deletions': obj.total['deletions'],
            'total_insertions': obj.total['insertions'],
            'total_lines': obj.total['lines'],
            'total_files': obj.total['files'],
            'changes': obj.files}


def handle_actor(name, obj):
    """
    Actor object handler.
    :param name: Unused String
    :param obj: GitPython Actor
    :return: Dictionary of attributes.
    """
    return {'author_name': obj.name,
            'author_email': obj.email}


# Handler functions to turn objects into usable attributes.
#   Functions return a dictionary of attributes, which
#   will appear in a row of the pandas dataframe.

git_object_handlers_lookup = {git.Stats: handle_stats,
                              git.Actor: handle_actor}