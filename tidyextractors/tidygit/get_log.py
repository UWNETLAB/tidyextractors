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
import tqdm
import pandas as pd
from tidyextractors.tidygit.git_object_handlers import git_object_handlers_lookup

# TODO: Increase get_log efficiency i.e. using gitnet implementation

# A default list of attributes to be extracted.
simple_attributes = ['author',
                     'author_tz_offset',
                     'authored_date',
                     'authored_datetime',
                     'encoding',
                     'hexsha',
                     'stats',
                     'summary',
                     'type'
                     ]

def handle_object(name, obj):
    """
    This helper function handles incoming test_data for make_object_dict.
    If thereis a special handler in git_object_handlers_lookup, this
    is used. Otherwise, the given name:obj pair is returned
    as-is.
    :param name: String
    :param obj: The object to be processed.
    :return: A dictionary of attributes.
    """
    if type(obj) in git_object_handlers_lookup:
        return git_object_handlers_lookup[type(obj)](name, obj)
    else:
        return {name:obj}


def make_object_dict(obj, keep=[]):
    """
    Processes an object, exporting its data as a nested dictionary.
    Individual objects are handled using handle_object.
    :param obj: The object to be processed.
    :param keep: Object attributes to be kept. Defaults to all attributes.
    :return: A dictionary of attributes.
    """
    data = {}
    if keep == []:
        get_attrs = dir(obj)
    else:
        get_attrs = keep

    for attr in get_attrs:
        datum = getattr(obj,attr)
        data.update(handle_object(attr,datum))
    return data


def extract_log(rpath,extract=simple_attributes):
    """
    Extracts Git commit test_data from a local repository.
    :param rpath: The path to a local Git repo.
    :param extract: A list of attribute name strings.
    :return: A Pandas dataframe containing Git commit test_data.
    """
    # Get repo
    m_repo = git.Repo(rpath)

    # Count commits
    count = 0
    m_commits = m_repo.iter_commits()
    for commit in m_commits:
        count += 1

    # Initialize progress bar and index

    with tqdm.tqdm(total=count) as pbar:

        # Get commits again
        m_commits = m_repo.iter_commits()

        # Setup test_data extraction
        update_interval = max(min(count//100,100),5)
        index = 0
        buffer = []

        # Extract commit test_data
        while True:

            # Add the next commit to the buffer
            try:
                next_commit = next(m_commits)
                buffer.append(make_object_dict(next_commit,extract))
                index += 1
                if index%update_interval == 0:
                    pbar.update(update_interval)

            # If no more commits, clear the buffer
            except StopIteration:
                break

    # final_df = pd.concat(sub_df_list)
    return pd.DataFrame(buffer)

