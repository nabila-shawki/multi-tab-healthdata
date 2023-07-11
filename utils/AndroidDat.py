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
        self.df['Date'] = pd.to_datetime(self.df['Date'])
    
    def filter_dates(self, start_date, end_date):
        self.filtered_df = self.df[self.df['Date'].between(start_date, end_date)]
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
    
    # def get_day_count(self):        
    #     return 

    # def plot_step_target(self):
    #     # plot and save images
    #     # start with the target days
    #     #
    #     total_days = self.days
    #     target_met = (self.filtered_df['Target Met'] == 1).sum()

    #     # Calculate the percentage of target met
    #     percentage_met = (target_met / total_days) * 100
    #     percentage_not_met = 100 - percentage_met

    #     # Create the donut chart
    #     data = [
    #         go.Pie(
    #             labels=['Target Met', 'Target Not Met'],
    #             values=[target_met, total_days - target_met],
    #             hole=0.8,  # Adjust the hole size for thickness of the donut
    #             marker=dict(colors=['#2E86C1', '#cccccc']),  # Customize the colors of the segments
    #             textinfo='none',  # Remove the percentages on the chart

    #         )
    #     ]
    #     # Set the layout of the chart
    #     # Set the layout of the chart
    #     layout = go.Layout(
    #         title=dict(
    #     text=f"<span style='font-size: 20px; color: #5DADE2; font-weight: bold; font-family: Arial;'>Step Target Met</span><br><br>"
    #                  f"<span style='font-size: 30px; color: #5DADE2; font-weight: bold; font-family: Arial;'>{target_met}/{total_days}</span><br>"
    #                  f"<span style='font-size: 20px; color: #5DADE2; font-weight: bold; font-family: Arial;'>Days</span>",
             
    #             x=0.5,  # Set the title position in the middle
    #             y=0.5,
    #             xanchor='center',
    #             yanchor='middle',
    #         ),
    #         showlegend=False,
    #     )

    #     # Create the figure
    #     figure = go.Figure(data=data, layout=layout)
    #     figure.update_layout(paper_bgcolor = "rgba(0,0,0,0)",
    #               plot_bgcolor = "rgba(0,0,0,0)")
        
    #     return figure
