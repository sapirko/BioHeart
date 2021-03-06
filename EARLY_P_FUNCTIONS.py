import os
import numpy as np
import pandas
import HRV_METHODS
import globals
import openpyxl


def flag_match_exec(par, parSIM, lst, col_name):  # flag_match(parECG, parSIM, list_of_bpm_flag, 'BPM')
    """
        Match the scenario flag
        from:simulation data
        to:ecg data
        --> by time

        :param par: DataFrame of par data
        :param parSIM: DataFrame of SIMULATION data
        :param lst: List of List - values for specific flag
        :param col_name: column name
        :type par: DataFrame
        :type parSIM: DataFrame
        :type col_name: str
    """
    i = 0
    j = 1
    initial_rows_at_par = len(par)
    rows_sim = len(parSIM)
    # print("initial_rows_at_par: " + str(initial_rows_at_par))
    # print("initial_rows_at_sim: " + str(rows_sim))
    if col_name == 'BPM':
        l_limit = globals.BPM_lower
        u_limit = globals.BPM_upper
    if col_name == 'RRIntervals':
        l_limit = globals.RR_lower
        u_limit = globals.RR_upper
    # print(l_limit)
    # print(u_limit)
    # print("start while loop")
    exceptions_ok = check_filter_type(col_name)
    while i < initial_rows_at_par:
        curr_value = par.at[i, col_name]
        if exceptions_ok:
            if not (l_limit <= curr_value <= u_limit):  # value not in range
                i += 1
                continue  # move to the next value
        if j < len(parSIM):  # while there are still rows to match in ECG/RR-1
            if parSIM.at[j - 1, 'Time'] <= par.at[i, 'Time'] < parSIM.at[j, 'Time']:
                # if time in ECG/RR between time range in SIM
                if int(parSIM.at[j - 1, 'Scenario']) != 0:  # אם אנחנו לא בתרחיש 0 כלומר תרחיש אמיתי
                    if int(parSIM.at[j, 'Scenario']) == 0 and par.at[i, 'Time'] == parSIM.at[j - 1, 'Time']:
                        scenario = int(parSIM.at[j - 1, 'Scenario'])
                    else:
                        scenario = int(parSIM.at[j, 'Scenario'])
                    par.at[i, 'Scenario'] = scenario  # match the flag
                    lst[scenario].append(par.at[i, col_name])  # מכניס לרשימה של הרשימות- bpm לכל flag
                    if col_name == "BPM":
                        dq_bpm_start_end_min_max_null(i, j, par, parSIM)
                    if col_name == "RRIntervals":
                        dq_rr_min_max_null(i, j, par, parSIM)
                i += 1  # move to the next ECG/RR row to match
            else:
                j += 1
        else:
            break


def check_filter_type(col_name):
    """function that indicates which filter is selected in exceptions window"""
    if globals.filter_type == globals.Filter.NONE:
        return False
    if globals.filter_type == globals.Filter.BPM and col_name != "BPM":
        return False
    if globals.filter_type == globals.Filter.RR and col_name != "RRIntervals":
        return False
    return True


def dq_bpm_start_end_min_max_null(i, j, par, parSIM):
    """
        The function calculates the data quality indicators for calculate BPM (IN ECG FILE):
         - start time
         - end time
         - min value
         - max value
         - null lines
    """
    if int(parSIM.at[j, 'Scenario']) != 0:
        globals.list_end_time[int(parSIM.at[j, 'Scenario']) - 1] = parSIM.at[j, 'Time']  # insert end time - all the time till the end
    if globals.list_start_time[int(parSIM.at[j - 1, 'Scenario']) - 1] == 0:
        globals.list_start_time[int(parSIM.at[j - 1, 'Scenario']) - 1] = parSIM.at[j - 1, 'Time']  # insert start time for the specific scenario
    if par.at[i, 'BPM'] < globals.list_min_bpm[int(parSIM.at[j - 1, 'Scenario']) - 1]:
        globals.list_min_bpm[int(parSIM.at[j - 1, 'Scenario']) - 1] = par.at[i, 'BPM']  # insert min value
    if par.at[i, 'BPM'] > globals.list_max_bpm[int(parSIM.at[j - 1, 'Scenario']) - 1]:
        globals.list_max_bpm[int(parSIM.at[j - 1, 'Scenario']) - 1] = par.at[i, 'BPM']  # insert max value
    if par.at[i, 'BPM'] is None:
        globals.list_null_bpm[int(parSIM.at[j - 1, 'Scenario']) - 1] += 1  # count null lines


def dq_rr_min_max_null(i, j, par, parSIM):
    """
        The function calculates the data quality indicators for calculate HRV METHODS (IN RR FILE):
         - min value
         - max value
         - null lines
    """
    if par.at[i, 'RRIntervals'] < globals.list_min_rr[int(parSIM.at[j - 1, 'Scenario']) - 1]:
        globals.list_min_rr[int(parSIM.at[j - 1, 'Scenario']) - 1] = par.at[i, 'RRIntervals']  # insert min value
    if par.at[i, 'RRIntervals'] > globals.list_max_rr[int(parSIM.at[j - 1, 'Scenario']) - 1]:
        globals.list_max_rr[int(parSIM.at[j - 1, 'Scenario']) - 1] = par.at[i, 'RRIntervals']  # insert max value
    if par.at[i, 'RRIntervals'] is None:
        globals.list_null_rr[int(parSIM.at[j - 1, 'Scenario']) - 1] += 1  # count null lines


def fix_min_bpm():
    """
        The initial minimum value is initialized by a large number (1000)
        and if it remains so, it is updated to be 0, because there is really no minimum value.
    """
    for x in range(globals.scenario_num):
        if globals.list_min_bpm[x] == 1000:
            globals.list_min_bpm[x] = 0


def fix_min_rr():
    """
        The initial minimum value is initialized by a large number (100)
        and if it remains so, it is updated to be 0, because there is really no minimum value.
    """
    for x in range(globals.scenario_num):
        if globals.list_min_rr[x] == 100:
            globals.list_min_rr[x] = 0


def rr_time_match(parRR):
    """
        filling Time coloumn in RR file
        :param parRR: DataFrame of RR data
    """
    i = 1
    while i < len(parRR):
        parRR.at[i, 'Time'] = round(parRR.at[i - 1, 'Time'] + parRR.at[i - 1, 'RRIntervals'], 4)
        i += 1


def initial_list_of_existing_par():
    """function that create a list of existing participants"""
    globals.list_of_existing_par = [*range(1, globals.par_num + 1)]
    copy_of_list_of_existing_par = [*range(1, globals.par_num + 1)]
    # print("begining: list of existing par")
    # print(globals.list_of_existing_par)  # 1,2,3
    for num in copy_of_list_of_existing_par:
        # print("the num in list of copy of existing is " + str(num))
        if num in globals.par_not_existing:
            globals.list_of_existing_par.remove(num)
            # print(globals.list_of_existing_par)
    # print("list of existing par end:\n")
    # print(*globals.list_of_existing_par)


def list_hrv_methods(avg_base, baseRR, list_of_rr_flag):
    """
        Using functions from file "HRV_METHODS" to create lists of HRV methods per scenario
    """
    listRMSSD = HRV_METHODS.RMSSD(list_of_rr_flag)
    listSDSD = HRV_METHODS.SDSD(list_of_rr_flag)
    listSDNN = HRV_METHODS.SDNN(list_of_rr_flag)
    listPNN50 = HRV_METHODS.PNN50(list_of_rr_flag)
    listBaseBPM = [avg_base] * globals.scenario_num
    listBaseRMSSD = [HRV_METHODS.Baseline_RMSSD(baseRR)] * globals.scenario_num
    listBaseSDNN = [HRV_METHODS.Baseline_SDNN(baseRR)] * globals.scenario_num
    listBaseSDSD = [HRV_METHODS.Baseline_SDSD(baseRR)] * globals.scenario_num
    listBasePNN50 = [HRV_METHODS.Baseline_PNN50(baseRR)] * globals.scenario_num
    return listBaseBPM, listBasePNN50, listBaseRMSSD, listBaseSDNN, listBaseSDSD, listPNN50, listRMSSD, listSDNN, listSDSD


def filling_summary_table(avg_base, baseRR, listBPM, par, list_of_rr_flag, ride, group_list):
    """
        Using function "list_hrv_methods"
        and filling the summary table with the lists
        using "append" to add all the lines for each participant
    """
    listBaseBPM, listBasePNN50, listBaseRMSSD, listBaseSDNN, listBaseSDSD, listPNN50, listRMSSD, listSDNN, listSDSD = list_hrv_methods(
        avg_base, baseRR, list_of_rr_flag)
    globals.summary_table = globals.summary_table.append(
        pandas.DataFrame({'Participant': [par] * globals.scenario_num,
                          'Ride Number': [ride] * globals.scenario_num,
                          'Scenario': list(range(1, globals.scenario_num + 1)),
                          'Group': group_list,
                          'Average BPM': listBPM, 'RMSSD': listRMSSD, 'SDSD': listSDSD,
                          'SDNN': listSDNN, 'PNN50': listPNN50, 'Baseline BPM': listBaseBPM,
                          'Baseline RMSSD': listBaseRMSSD, 'Baseline SDNN': listBaseSDNN,
                          'Baseline SDSD': listBaseSDSD, 'Baseline PNN50': listBasePNN50,
                          'Subtraction BPM': [round(abs(x - y), 4) for x, y in
                                              zip(listBaseBPM, listBPM)],
                          'Subtraction RMSSD': [round(abs(x - y), 4) for x, y in
                                                zip(listBaseRMSSD, listRMSSD)],
                          'Subtraction SDNN': [round(abs(x - y), 4) for x, y in
                                               zip(listBaseSDNN, listSDNN)],
                          'Subtraction SDSD': [round(abs(x - y), 4) for x, y in
                                               zip(listBaseSDSD, listSDSD)],
                          'Subtraction PNN50': [round(abs(x - y), 4) for x, y in
                                                zip(listBasePNN50, listPNN50)]
                          }))
    globals.summary_table.reset_index(drop=True, inplace=True)  # reset the index after the append


def make_par_group_list(par):
    """
        Create the "Group" column in the Summary_Table
    """
    group_list = []
    if globals.group_num == 0:  # if there is no groups
        group_list = [0] * globals.scenario_num  # the "group" column in the summary table is filled by 0
    else:
        for group in range(globals.group_num):
            if par in globals.lists_of_groups[group]:  # if the participant is in the group
                group_list = [group + 1] * globals.scenario_num  # the group is "+1" becauseine the list : index 0=1, index 1=2...
                break
    return group_list


def calc_rr_num_of_rows_per_flag():
    """
        Calculation the number of rows used to calculate HRV methods, per flag (scenario)
    """
    list_count_rr_flag = []  # rr values count per flag - number of rows in RR file per flag
    for i in range(1, len(globals.list_count_rr_intervals_flag)):
        # add 1 to the interval to get the count of rr values - not rr intervals
        if globals.list_count_rr_intervals_flag[i] != 0:
            list_count_rr_flag.append(globals.list_count_rr_intervals_flag[i] + 1)
        else:
            list_count_rr_flag.append(0)
    return list_count_rr_flag


def filling_dq_table(listBPM_per_scenario, par, ride, group_list):
    """
        Using function "calc_rr_num_of_rows_per_flag"
        and filling the data_quality_table with the lists
        using "append" to add all the lines for each participant
    """
    list_count_rr_flag = calc_rr_num_of_rows_per_flag()

    globals.data_quality_table = \
        globals.data_quality_table.append(pandas.DataFrame({'Participant': [par] * globals.scenario_num,
                                                            'Ride Number': [
                                                                               ride] * globals.scenario_num,
                                                            'Scenario': list(
                                                                range(1, globals.scenario_num + 1)),
                                                            'Group': group_list,
                                                            "Start time (sec)": globals.list_start_time,
                                                            "End time (sec)": globals.list_end_time,
                                                            "Duration (sec)": [round(x - y, 4) for x, y in
                                                                         zip(globals.list_end_time,
                                                                             globals.list_start_time)],
                                                            "BPM(ecg) : Total number of rows": listBPM_per_scenario,
                                                            "BPM(ecg) : Number of empty rows": globals.list_null_bpm,
                                                            "BPM(ecg) : % Completeness": globals.list_completeness_bpm,
                                                            "BPM(ecg) : Minimum value": globals.list_min_bpm,
                                                            "BPM(ecg) : Maximum value": globals.list_max_bpm,
                                                            "BPM(ecg) : Median": globals.list_median_bpm,
                                                            "HRV methods(rr) : Total number of rows": list_count_rr_flag,
                                                            "HRV methods(rr) : Number of empty rows": globals.list_null_rr,
                                                            "HRV methods(rr) : % Completeness": globals.list_completeness_rr,
                                                            "HRV methods(rr) : Minimum value": globals.list_min_rr,
                                                            "HRV methods(rr) : Maximum value": globals.list_max_rr,
                                                            "HRV methods(rr) : Median": globals.list_median_rr
                                                            }))
    globals.data_quality_table.reset_index(drop=True, inplace=True)  # reset the index after the append


def early_process_rr(index_in_folder, ride):
    """
        Loading the RR files, arranging the columns: TIME, RRIntervals and Scenario
    """
    parRR = pandas.read_excel(os.path.join(globals.main_path + "\\" + "ride " + str(ride) + "\\" + "rr",
                                           os.listdir(
                                               globals.main_path + "\\" + "ride " + str(
                                                   ride) + "\\" + "rr")[
                                               index_in_folder]),
                              names=['RRIntervals'], skiprows=4, skipfooter=8, header=None,
                              engine='openpyxl')
    parRR['RRIntervals'] = [round(x, 3) for x in parRR['RRIntervals']]
    parRR.insert(1, 'Time', [0.00 for x in range(0, (len(parRR)))],
                 True)  # insert Time column with zero
    parRR.insert(2, 'Scenario', [0 for x in range(0, (len(parRR)))],
                 True)  # insert Scenario column with zero
    # Creates a list of lists as the number of scenarios
    list_of_rr_flag = [[] for i in range(globals.scenario_num + 1)]
    return parRR, list_of_rr_flag


def sync_RR(parRR):
    """
        Synchronize RR files. Lower the amount of seconds entered as input from these files
        to reset them in front of the simulator.
    """
    pandas.options.mode.chained_assignment = None  # So as not to give a warning that I am overwriting the original file
    parRR = parRR[parRR['Time'] >= globals.biopac_sync_time]  # leave only the lines that bigger then sync time
    parRR.reset_index(drop=True, inplace=True)
    parRR['Time'] = [round(x - globals.biopac_sync_time, 3) for x in parRR['Time']]  # Subtract the seconds from the remaining rows
    return parRR


def dq_completeness_bpm(listBPM_per_scenario):
    """
        Calculation of the percentage of data integrity in ECG file:
        the total number of rows less the number of empty rows divided by the total number of rows - multiplied by 100.
    """
    for i in range(globals.scenario_num):
        if listBPM_per_scenario[i] == 0:
            globals.list_completeness_bpm[i] = 0
        else:
            globals.list_completeness_bpm[i] = \
                round(((listBPM_per_scenario[i] - globals.list_null_bpm[i]) / listBPM_per_scenario[i]) * 100, 2)


def dq_completeness_rr():
    """
        Calculation of the percentage of data integrity in RR file:
        the total number of rows less the number of empty rows divided by the total number of rows - multiplied by 100.
    """
    for i in range(globals.scenario_num):
        if globals.list_count_rr_intervals_flag[i + 1] == 0:
            globals.list_completeness_rr[i] = 0
        else:
            globals.list_completeness_rr[i] = \
                round(
                    ((globals.list_count_rr_intervals_flag[i + 1] - globals.list_null_bpm[i]) / globals.list_count_rr_intervals_flag[
                        i + 1]) * 100,
                    2)


def avg_med_bpm(list_of_bpm_flag):
    """
        Calculate the mean and median from the ECG files.
    """
    listBPM = []  # list of Average BPM by scenario
    listBPM_per_scenario = []
    for i in range(1, globals.scenario_num + 1):
        if len(list_of_bpm_flag[i]) != 0:
            listBPM.append(sum(list_of_bpm_flag[i]) / len(list_of_bpm_flag[i]))
            globals.list_median_bpm[i - 1] = round(np.median(list_of_bpm_flag[i]), 4)

        else:
            listBPM.append(0)
            globals.list_median_bpm[i - 1] = 0
        listBPM_per_scenario.append(len(list_of_bpm_flag[i]))

    return listBPM, listBPM_per_scenario


def med_rr(list_of_rr_flag):
    """
        Calculate the median from the RR files.
    """
    for i in range(1, globals.scenario_num + 1):
        if len(list_of_rr_flag[i]) != 0:
            globals.list_median_rr[i - 1] = round(np.median(list_of_rr_flag[i]), 4)
        else:
            globals.list_median_rr[i - 1] = 0


def early_process_ecg_sim(index_in_folder, ride):
    """
        File upload: ECG and SIM.
        Arrange the columns in these files.
        If synchronization has taken place -
            ignore the relevant lines (1000 per sec or 60 per sec):
                ECG: skiprows = 11 + int(globals.biopac_sync_time * 1000)
                sim: skiprows = 1 + int(globals.sim_sync_time * 60)
            and subtract the seconds from each remaining line.
    """
    globals.list_count_rr_intervals_flag = [0] * (
            globals.scenario_num + 1)  # Initialize the list to zero for each scenario
    list_of_bpm_flag = [[] for i in
                        range(
                            globals.scenario_num + 1)]  # Creates a list of lists as the number of scenarios
    parECG = pandas.read_csv(os.path.join(globals.main_path + "\\" + "ride " + str(ride) + "\\" + "ecg",
                                          os.listdir(
                                              globals.main_path + "\\" + "ride " + str(
                                                  ride) + "\\" + "ecg")[
                                              index_in_folder]),
                             sep="\t", usecols=[2], names=['BPM'],
                             skiprows=11 + int(globals.biopac_sync_time * 1000), header=None)
    parECG.insert(1, 'Time', [x / 1000 for x in range(0, (len(parECG)))], True)  # filling a time column - 0, 0.001, 0.002...
    parSIM = pandas.read_csv(os.path.join(globals.main_path + "\\" + "ride " + str(ride) + "\\" + "sim",
                                          os.listdir(
                                              globals.main_path + "\\" + "ride " + str(
                                                  ride) + "\\" + "sim")[
                                              index_in_folder]),
                             sep=",", skiprows=1 + int(globals.sim_sync_time * 60),
                             usecols=[0, globals.scenario_col_num - 1],
                             names=['Time', 'Scenario'])
    if globals.sim_sync_time > 0:  # Sync sim time
        parSIM['Time'] = [round(x - globals.sim_sync_time, 4) for x in parSIM['Time']]  # Subtract the seconds from each line to synchronize
    else:
        parSIM['Time'] = [round(x, 4) for x in parSIM['Time']]
    parECG.insert(2, 'Scenario', [0 for x in range(0, (len(parECG)))],
                  True)  # adding scenario column and filling with 0
    return list_of_bpm_flag, parECG, parSIM


def early_process_base(index_in_folder):
    """
        Loading the BASE files with column 'RRIntervals'
        and calculate AVG BPM column.
    """
    baseECG = pandas.read_csv(os.path.join(globals.main_path + "\\" + "base" + "\\" + "base ecg",
                                           os.listdir(
                                               globals.main_path + "\\" + "base" + "\\" + "base ecg")[
                                               index_in_folder]),
                              sep="\t",
                              names=['BPM'], usecols=[2],
                              skiprows=11, header=None)
    avg_base = np.average(baseECG)  # avg for column BPM at baseECG
    baseRR = pandas.read_excel(os.path.join(globals.main_path + "\\" + "base" + "\\" + "base rr",
                                            os.listdir(
                                                globals.main_path + "\\" + "base" + "\\" + "base rr")[
                                                index_in_folder]),
                               names=['RRIntervals'], skiprows=4, skipfooter=8, header=None,
                               engine='openpyxl')
    return avg_base, baseRR, baseECG


def initial_data_quality():
    """
        Initialize values for the lists that calculate the data quality table's columns.
    """
    globals.list_start_time = [0] * globals.scenario_num
    globals.list_end_time = [0] * globals.scenario_num
    globals.list_min_bpm = [1000] * globals.scenario_num
    globals.list_max_bpm = [0] * globals.scenario_num
    globals.list_null_bpm = [0] * globals.scenario_num
    globals.list_completeness_bpm = [0] * globals.scenario_num
    globals.list_median_bpm = [0] * globals.scenario_num
    globals.list_min_rr = [100] * globals.scenario_num
    globals.list_max_rr = [0] * globals.scenario_num
    globals.list_null_rr = [0] * globals.scenario_num
    globals.list_completeness_rr = [0] * globals.scenario_num
    globals.list_median_rr = [0] * globals.scenario_num
