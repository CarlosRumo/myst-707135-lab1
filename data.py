
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: First Laboratory                                                        -- #
# -- script: data.py : python script for data collection                                                 -- #
# -- author: CarlosRumo                                                                     -- #
# -- license: GNU General Public License v3.0                                               -- #
# -- repository: https://github.com/CarlosRumo/myst-707135-lab1                                                                        -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
import json
import pandas as pd
from pathlib import Path

def read_file(file):
    """
    Read data from a local file
    
    Parameters
    ----------
    
    fie_name: str, (default = None)
        name of the file to be read
    
    folder_route: str, (default = None)
        Relative or full path to the file
    
    Returns
    -------
    
    A json object with the contents of the file
    
    """
    f = open(file)

    orderbooks_data = json.load(f)
    
    return orderbooks_data



def read_data(file_path):

    df = pd.read_parquet(file_path)
    return df