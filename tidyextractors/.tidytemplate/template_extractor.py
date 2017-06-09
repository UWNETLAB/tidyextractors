import tqdm
import warnings
import pandas as pd
import itertools as it
from tidyextractors import BaseExtractor


class TemplateExtractor(BaseExtractor):

    def __sub_init__(self, source, *args, **kwargs):
        # Populate lookup table:
        # Add lazy short form lookup table:
        pass

    def _extract(self, source, *args, **kwargs):
        # Extract data
        pass

    def data_method(self):
        pass