# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 11:43:14 2023

@author: nabil
"""

from utils.AndroidDat import AndroidDat
import pandas as pd
import re

# read and filter the data for further processing
#
def read_dat(fname, start_date, end_date, target_count):
    
    android_dat = AndroidDat(fname)
    android_dat.read_dat()
    android_dat.filter_dates(start_date, end_date)
    android_dat.drop_nan_columns()
    android_dat.remove_zero_columns()
    android_dat.convert_units()
    android_dat.assign_week_num()
    android_dat.modify_week_num()
    android_dat.find_target_met(target_count)
    
    return android_dat   
#
# end of method

# read and filter the data for further processing
#
def read_daily_dat(fname):
    
    android_dat = AndroidDat(fname)
    android_dat.read_dat()
    android_dat.convert_units()
    
    return android_dat   
#
# end of method

def extract_dates(string):
  """Extracts the two dates from the given string.

  Args:
    string: The string containing the two dates.

  Returns:
    A tuple of the two dates.
  """

  pattern = r"(\d{4})-(\w+)-(\d+) - (\d{4})-(\w+)-(\d+)"
  match = re.search(pattern, string)
  if match:
    dates = (match.group(1), match.group(2), match.group(3), match.group(4),
            match.group(5), match.group(6))
    
    date = dates[:3]
    date = '-'.join(date)
    start_date = pd.to_datetime(date)
    
    date = dates[3:]
    date = '-'.join(date)
    end_date = pd.to_datetime(date)

    return start_date, end_date
    
  else:
    return None
