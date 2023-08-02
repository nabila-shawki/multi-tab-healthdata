# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 14:42:17 2023

@author: nabil
"""

# AndroidDat.py

# AndroidDat.py

import os
import pandas as pd
import plotly.graph_objs as go


class AndroidDat:
    def __init__(self, fname):
        self.fname = fname
        self.df = None
        self.filtered_df = None
       
       
    def read_dat(self):
        self.df = pd.read_csv(self.fname)
        self.filtered_df = self.df
        
        if 'Date' in self.df.columns:
            self.filtered_df['Date'] = pd.to_datetime(self.df['Date'])
    
    def filter_dates(self, start_date, end_date):
        self.filtered_df = self.filtered_df[self.df['Date'].between(start_date, end_date)]
        self.days = len(self.filtered_df)
    
    def drop_nan_columns(self, threshold=0.5):
        threshold = len(self.filtered_df) * threshold
        self.filtered_df = self.filtered_df.dropna(axis=1, thresh=threshold)
    
    def si_to_imperial(self, column_regex, si_unit, imp_unit, multiplier):
        columns_si = self.filtered_df.filter(regex=column_regex, axis=1)
        columns_si = columns_si.columns.tolist()
        
        for col in columns_si:
            col_imp = col.replace(si_unit, imp_unit)
            self.filtered_df[col_imp] = self.filtered_df[col] * multiplier
            self.filtered_df = self.filtered_df.drop(col, axis=1)
            
    def convert_units(self):
        self.si_to_imperial('.*\(m\).*', "(m)", "(mile)", 0.000621371)
        self.si_to_imperial('.*\(m/s\).*', "(m/s)", "(mph)", 2.23694)
        self.si_to_imperial('.*\(kg\).*', "(kg)", "(lb)", 2.20462)
        
    def get_week_number(self, date):
        year, week_num, _ = date.isocalendar()
        return week_num
    
    def assign_week_num(self):
        self.filtered_df["Week #"] = self.filtered_df['Date'].apply(self.get_week_number)

    def modify_week_num(self):
        first_week = self.filtered_df["Week #"].min()
        self.filtered_df["Week #"] = self.filtered_df["Week #"] - first_week + 1
        
    def remove_zero_columns(self):
        self.filtered_df = self.filtered_df.loc[:, (self.filtered_df != 0).any(axis=0)]   
    
    def find_target_met(self, target_count):
        self.filtered_df['Target Met'] = (self.filtered_df['Step count'] >= target_count).astype(int)
        self.filtered_df['Target Met perc'] = (self.filtered_df['Step count'] / target_count) * 100
    


class WeeklyMetricsAnalyzer:
    def __init__(self, df):
        self.df = df

    def extract_metrics(self, week_start, week_end, target_step_count=2000):

        # Filter the data for the specified week
        week_data = self.df[(self.df['Date'] >= week_start) & (self.df['Date'] <= week_end)]
        self.week_data = week_data

        # Calculate the percentage of days the target was met
        total_days = week_data.shape[0]
        days_met_target = week_data[week_data['Step count'] >= target_step_count].shape[0]
        percentage_days_met_target = (days_met_target / total_days) * 100

        # Calculate the average step count
        average_step_count = week_data['Step count'].mean(skipna=True)

        # Get the original step counts as a list for the bar graph
        original_step_counts = week_data['Step count'].tolist()

        # Calculate the average distance, speed, activity time, heart rate, blood pressure, and weight
        average_distance = week_data['Distance (mile)'].mean(skipna=True)
        average_speed = week_data['Average speed (mph)'].mean(skipna=True)
        average_activity_time = week_data['Move Minutes count'].mean(skipna=True)

        # Create and return the dictionary with the values
        self.activity_metric = {
            'Total days': total_days,
            'Days met target': days_met_target,
            "Percentage of days met target": percentage_days_met_target,
            "Average step count": average_step_count,
            "Original step counts": original_step_counts,
            "Average distance": average_distance,
            "Average speed": average_speed,
            "Average activity time": average_activity_time
        }

        self.health_dat = {
            "Average heart rate": week_data['Average heart rate (bpm)'].mean(skipna=True),
            "Max heart rate": week_data['Max heart rate (bpm)'].max(skipna=True),
            "Min heart rate": week_data['Min heart rate (bpm)'].min(skipna=True),
            "Average BP diastolic": week_data['Average diastolic blood pressure (mmHg)'].mean(skipna=True),
            "Average BP systolic": week_data['Average systolic blood pressure (mmHg)'].mean(skipna=True),
            "Average weight": week_data['Average weight (lb)'].mean(skipna=True),
            "Average calories": week_data['Calories (kcal)'].mean(skipna=True),
        }

        #print (self.activity_metric["Average step count"])




# # Assuming you have already stored the data in the 'df' DataFrame as shown in the previous code

# # Create an instance of WeeklyMetricsAnalyzer
# analyzer = WeeklyMetricsAnalyzer(df)

# # Define the start and end dates for Week 1 and Week 2
# week1_start = pd.to_datetime('2023-06-05')
# week1_end = pd.to_datetime('2023-06-11')

# week2_start = pd.to_datetime('2023-06-12')
# week2_end = pd.to_datetime('2023-06-18')

# # Analyze the weekly metrics for Week 1
# week1_metrics = analyzer.analyze_weekly_metrics(week1_start, week1_end)

# # Analyze the weekly metrics for Week 2
# week2_metrics = analyzer.analyze_weekly_metrics(week2_start, week2_end)

# # Print the results
# print("Week 1: 2023-06-05 - 2023-06-11")
# print(week1_metrics)

# print("\nWeek 2: 2023-06-12 - 2023-06-18")
# print(week2_metrics)
