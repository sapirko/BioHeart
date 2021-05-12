from enum import Enum

import pandas
import PySimpleGUIQt as sg

class Filter(Enum):
    NONE=1
    BPM=2
    RR=3
    BOTH=4

scenario_num = 0
scenario_col_num = 0
par_num = 0
par_ride_num = 0
sim_start = 0.0
ecg_start = 0.0
par_not_existing = [1,2]
current_par = 0
current_ride = 0
percent = 0
list_of_existing_par = []
list_count_rmssd = []
list_start_time = []
list_end_time = []
list_min_bpm = []
list_max_bpm = []
list_null_bpm = []
list_completeness_bpm = []
list_median_bpm = []
list_min_rr = []
list_max_rr = []
list_null_rr = []
list_completeness_rr = []
list_median_rr = []
filter_type = Filter.NONE
RR_lower = 0
RR_upper = 0
BPM_lower = 0
BPM_upper = 0
# path_noam = r"C:\Users\user\PycharmProjects\ProjectGmar\main folder"
# path_sapir = r"C:\Users\sapir\Desktop\project_gmar_path"
main_path = ""
treedata = sg.TreeData()
header_summary_table = ["Participant", "Ride Number", "Scenario", "Average BPM", "RMSSD", "SDSD", "SDNN", "PNN50",
                        "Baseline BPM",
                        "Subtraction BPM", "Baseline RMSSD", "Subtraction RMSSD", "Baseline SDNN",
                        "Subtraction SDNN",
                        "Baseline SDSD", "Subtraction SDSD", "Baseline PNN50",
                        "Subtraction PNN50"]
summary_table = pandas.DataFrame(columns=header_summary_table)  # create empty table,only with columns names
header_data_quality = ["Participant", "Ride Number", "Scenario", "Start time", "End time", "Duration",
                       "BPM(ecg) : Total number of rows", "BPM(ecg) : Number of empty rows",
                       "BPM(ecg) : % Completeness", "BPM(ecg) : Minimum value",
                       "BPM(ecg) : Maximum value", "BPM(ecg) : Median",
                       "HRV methods(rr) : Total number of rows",
                       "HRV methods(rr) : Number of empty rows",
                       "HRV methods(rr) : % Completeness",
                       "HRV methods(rr) : Minimum value",
                       "HRV methods(rr) : Maximum value", "HRV methods(rr) : Median"]
data_quality_table = pandas.DataFrame(columns=header_data_quality)

"""
def initialize():
    global scenario_num
    global scenario_col_num
    global par_num
    global par_ride_num
    global current_par
    global main_path
    global percent
    global list_count_rmssd  # list which contains the number of N (RR intervals) in all scenarios.
    global summary_table
    global data_quality_table
    global header_summary_table
    global header_data_quality
    global treedata
    global fig  # ???????????????
    # global participant_num_input
"""
