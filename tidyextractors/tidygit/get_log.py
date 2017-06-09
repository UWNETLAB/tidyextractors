import git
import tqdm
import pandas as pd
from tidyextractors.tidygit.object_handlers import object_handlers_lookup

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

def handle_object(name,object):
    '''
    This helper function handles incoming test_data for make_object_dict.
    If thereis a special handler in object_handlers_lookup, this
    is used. Otherwise, the given name:object pair is returned
    as-is.
    Args:
        name: 
        object: 

    Returns:
        A dict of attributes.
    '''
    if type(object) in object_handlers_lookup:
        return object_handlers_lookup[type(object)](name,object)
    else:
        return {name:object}


def make_object_dict(obj,keep=[]):
    '''
    Processes an object, exporting its test_data as a nested dictionary.
    Individual objects are handled using handle_object.
    Args:
        obj: 
        keep: 

    Returns:

    '''
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
    '''
    Extracts Git commit test_data from a local repository.
    
    Args:
        rpath: The path to a local Git repo.

    Returns:
        A Pandas dataframe containing Git commit test_data.
    '''

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
