# *********************************************************************************************
# Copyright (C) 2017 Joel Becker,  Jillian Anderson, Steve McColl and Dr. John McLevey
#
# This file is part of the tidyextractors package developed for Dr John McLevey's Networks Lab
# at the University of Waterloo. For more information, see
# http://tidyextractors.readthedocs.io/en/latest/
#
# tidyextractors is free software: you can redistribute it and/or modify it under the terms of
# the GNU General Public License as published by the Free Software Foundation, either version 3
# of the License, or (at your option) any later version.
#
# tidyextractors is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with tidyextractors.
# If not, see <http://www.gnu.org/licenses/>.
# *********************************************************************************************

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