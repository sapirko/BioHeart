import time
import threading
import pandas
import numpy as np
import os
import PySimpleGUIQt as sg
import sys
from multiprocessing import Process
import HRV_METHODS
import globals
from EARLY_P_FUNCTIONS import rr_time_match, initial_list_of_existing_par, filling_summary_table, \
    early_process_rr, dq_completeness_bpm, avg_med_bpm, early_process_ecg_sim, early_process_base, \
    initial_data_quality, dq_completeness_rr, med_rr, filling_dq_table, flag_match_exec, fix_min_rr, fix_min_bpm, \
    make_par_group_list, sync_RR
from UI_FUNCTIONS import exportEXCEL_summary, checks_boundaries, initial_tree, \
    exportEXCEL_dq, loading_window_update, all_input_0_9, sync_handle, save_input_open_window, tree_handle, \
    exceptions_checkbox_handle, create_empty_folders, windows_initialization_part_1, \
    windows_initialization_part_2, initial_optional, check_optional_window, \
    plot_with_scenarios, plot_rides, plot_groups_rides, plot_groups_scenarios, general_graph_avg, \
    check_if_can_continue_new_load, check_if_can_continue_exist_load, window_update_custom_graph, \
    window_update_general_graph, window_update_x_axis_rides, window_update_x_axis_scenarios


# --------------------------------------------- early_process ---------------------------------------------
def early_process():
    """
    A function that arranges the raw files
    (adds columns, matches the scenario column by times for all the files)
    and performs the processing of the files. The output is a summary table with the avg heart rate
     and the heart rate variance
    """
    globals.current_par = 1
    globals.current_ride = 1
    globals.percent = 0  # Displays in percentages for how many participants the final table data has been processed

    for par in globals.list_of_existing_par:  # loop for participants that exist
        group_list = make_par_group_list(par)
        # print("par in list_of_existing_par:" + str(par))
        for filename in os.listdir(globals.main_path + "\\" + "ride 1" + "\\" + "ecg"):
            # print("the filename in ecg:" + filename)
            par_num_in_file = ''.join([i for i in filename if i.isdigit()])  # ???????? ???? ???? ???????????? ?????? ??????????
            # print(par_num_in_file)
            if str(par) == par_num_in_file or '0' + str(par) == par_num_in_file:  # ???? ?????????? ???? ???????????? ???????????? ???????????????? ?????????????? ?????????? ?????? ?????????? ???? ???? 0 ????????????
                index_in_folder = os.listdir(globals.main_path + "\\" + "ride 1" + "\\" + "ecg").index(
                    filename)  # ?????????? ???????????? ???????? ???????????? ???? ???????????? ??ecg ?????????? ?????????? filename
                # print(index_in_folder)  # checked
                for ride in range(1, globals.par_ride_num + 1):  # loop for rides
                    globals.current_ride = ride
                    # print("Start early process for ride: " + str(ride) + " for par: " + str(par))
                    # -------------------------------------------- ECG & SIM -----------------------------------------
                    list_of_bpm_flag, parECG, parSIM = early_process_ecg_sim(index_in_folder, ride)
                    initial_data_quality()
                    # filling column 'flag' in parECG, and filling list_of_bpm_flag by scenario.
                    # print("flag_match_exec(parECG, parSIM, list_of_bpm_flag, 'BPM')")
                    flag_match_exec(parECG, parSIM, list_of_bpm_flag, 'BPM')
                    fix_min_bpm()
                    listBPM, listBPM_per_scenario = avg_med_bpm(list_of_bpm_flag)
                    dq_completeness_bpm(listBPM_per_scenario)
                    # ------------------------------------------------ RR --------------------------------------------
                    parRR, list_of_rr_flag = early_process_rr(index_in_folder, ride)
                    rr_time_match(parRR)  # function that fill the time column in parRR
                    if globals.biopac_sync_time > 0:
                        parRR = sync_RR(parRR)
                    # filling column 'flag' in parRR, and filling list_of_rr_flag by scenario.
                    # print("flag_match_exec(parRR, parSIM, list_of_rr_flag, 'RRIntervals')")
                    flag_match_exec(parRR, parSIM, list_of_rr_flag, 'RRIntervals')
                    fix_min_rr()
                    # ------------------------------------------ BASE RR & ECG ---------------------------------------
                    avg_base, baseRR, baseECG = early_process_base(index_in_folder)
                    # ------------------------------------- filling summary table ------------------------------------
                    filling_summary_table(avg_base, baseRR, listBPM, par, list_of_rr_flag, ride, group_list)
                    # ----------------------------------- filling data quality table ---------------------------------
                    med_rr(list_of_rr_flag)
                    dq_completeness_rr()
                    filling_dq_table(listBPM_per_scenario, par, ride, group_list)

                    globals.percent += (1 / len(globals.list_of_existing_par)) / globals.par_ride_num
                if globals.current_par < len(globals.list_of_existing_par):
                    globals.current_par += 1  # ???????????? ???? ?????????? ???????? ???????????? ecg ?????? ????????
        # print(globals.percent * 100)


def pickle_early_process():
    """
    A function that loads the files: summary table (pickle) and data quality (pickle)
    """
    # Initialize the load screen variables to 100%
    globals.current_ride = globals.par_ride_num
    globals.current_par = globals.par_num
    globals.percent = 100  # Displays in percentages for how many participants the final table data has been processed


# --------------------------------------------- UI ---------------------------------------------
def ui():
    # -------------------------------------------- Windows Layout --------------------------------------------
    correct_open_window, correct_optional_window, correct_path_window, exceptions_values_window, exclude_correct, finish_while_loop, group_correct, layout_loading_window, is_newload, open_window, optional_window, path_load_window = windows_initialization_part_1()
    # -------------------------------------------- Open Windows --------------------------------------------
    while True:  # Create an event loop
        event, values = open_window.read()
        open_window.bring_to_front()
        if event == "EXIT_OPEN" or event == sg.WIN_CLOSED:
            # End program if user closes window or presses the EXIT button
            return False  # can stop the loop and the window will close
        # Limit the fields to accept only digits between 0 and 9 without any other characters
        all_input_0_9(event, open_window, values)
        if event == 'Sync':
            sync_handle(open_window, values)
        if event == "CONTINUE_OPEN":
            # ----------------------------------------- SAVE INPUT -----------------------------------------
            if (not values['par_num']) or (not values['scenario_num']) or (
                    not values['scenario_col_num']) or (
                    not values['Sync'] and (not values['sim_sync_time']) or (not values['biopac_sync_time'])):
                # Check if at least one of the 3 fields is incomplete
                sg.popup_quick_message('Please fill in all the fields', font=("Century Gothic", 14),
                                       background_color='red', location=(970, 880))
            else:  # all fields are complete
                if not values['Sync'] and ((values['sim_sync_time'] != "0") and (values['biopac_sync_time'] != "0")):
                    sg.popup_quick_message('At least one of the simulator/ECG fields must start from 0',
                                           font=("Century Gothic", 14), background_color='red', location=(970, 880),
                                           auto_close_duration=5)
                else:
                    # Keeping the inputs in variables
                    save_input_open_window(values)
                    initial_list_of_existing_par()
                    correct_open_window = True  # ???? ???????????? ???????? ????????????, ???????? ???????????? ???????? ??????

        if correct_open_window:  # ???? ???? ???? ???????????? ?????? ???????????? ???????????? ???????? ??????????
            # ?????????? - ???? ?????????? ?????????? ???????? ???????? ?????? ????????, ???????? ???????????? ?????????? ??????
            optional_window.un_hide()
            open_window.hide()
            # ------------------------------------------- OPTIONAL Window ---------------------------------
            initial_optional(optional_window)
            while True:
                event9, values9 = optional_window.read()
                if event9 == sg.WIN_CLOSED:
                    return False
                if event9 == 'Ex par CB':
                    if values9['Ex par CB']:
                        optional_window.element('Ex par LB').update(disabled=False)
                        optional_window.element('Exclude_OPTIONAL').update(visible=True)
                    else:
                        optional_window.element('Ex par LB').update(disabled=True)
                        optional_window.element('Exclude_OPTIONAL').update(visible=False)
                        globals.par_not_existing = []
                        initial_optional(optional_window)
                if event9 == 'groups CB':
                    if values9['groups CB']:
                        optional_window.element('groups num').update(disabled=False)
                        optional_window.element('Choose_OPTIONAL').update(visible=True)
                    else:
                        optional_window.element('groups num').update(disabled=True)
                        optional_window.element('Choose_OPTIONAL').update(visible=False)
                        globals.group_num = 0
                        for i in list(range(1, 6)):
                            optional_window.element('group' + str(i)).update(visible=False)

                if event9 == 'Exclude_OPTIONAL':
                    globals.par_not_existing = values9['Ex par LB']
                    initial_list_of_existing_par()
                    optional_window.element('Ex par LB').update(globals.list_of_existing_par)
                    for i in list(range(1, 6)):
                        optional_window.element('group' + str(i)).update(visible=False)
                        optional_window.element('group' + str(i)).update(globals.list_of_existing_par)

                if event9 == 'Choose_OPTIONAL':
                    globals.group_num = int(values9['groups num'])
                    list_groups = list(range(1, globals.group_num + 1))
                    for i in list(range(1, 6)):
                        optional_window.element('group' + str(i)).update(visible=False)
                    if len(globals.list_of_existing_par) >= globals.group_num:
                        for i in list_groups:
                            optional_window.element('group' + str(i)).update(visible=True)
                    else:
                        sg.popup_quick_message("Select a number of groups that is less than or equal to the number of participants",
                                               font=("Century Gothic", 14),
                                               background_color='red', location=(970, 800), auto_close_duration=5)

                if event9 == 'CONTINUE_OPTIONAL':
                    correct_optional_window = check_optional_window(correct_optional_window, exclude_correct,
                                                                    group_correct, values9)
                if event9 == "BACK_OPTIONAL":
                    optional_window.hide()
                    open_window.un_hide()
                    correct_open_window = False  # ?????????? ???????????? ?????? ?????????? ???? ?????????????? ???? ???????????? ??????

                    break
                if correct_optional_window:
                    # ------------------------------------- Path Load Windows ----------------------------------
                    path_load_window.un_hide()
                    optional_window.hide()
                    initial_tree(path_load_window['-TREE-'], "")
                    while True:
                        event2, values2 = path_load_window.read()
                        if event2 == sg.WIN_CLOSED:
                            return False
                        if event2 == "Create empty folders":
                            create_empty_folders()
                        if event2 == "-MAIN FOLDER-":
                            tree_handle(path_load_window, values2)
                        if event2 == "CONTINUE_PATH":
                            if values2['NEW LOAD']:
                                correct_path_window, is_newload = check_if_can_continue_new_load(correct_path_window, is_newload,
                                                                                        values2)
                                """
                                print("correct_path_window")
                                print(correct_path_window)
                                print("is_newload?")
                                print(is_newload)
                                """

                            if values2['EXIST LOAD']:
                                correct_path_window, is_newload = check_if_can_continue_exist_load(correct_path_window, is_newload,
                                                                                        values2)
                                """
                                print("correct_path_window")
                                print(correct_path_window)
                                print("is_newload?")
                                print(is_newload)
                                """

                        if event2 == "BACK_PATH":
                            optional_window.un_hide()
                            path_load_window.hide()
                            correct_optional_window = False
                            correct_path_window = False
                            break
                        if correct_path_window:
                            path_load_window.hide()
                            if is_newload:
                                exceptions_values_window.un_hide()
                                # ???? ?????????? ???????? ???????? ?????? ????????, ???????? ???????????? ?????????? ??????
                                # ------------------------------ EXCEPTIONS VALUES Window -------------------------
                                while True:
                                    event8, values8 = exceptions_values_window.read()
                                    if event8 == sg.WIN_CLOSED:
                                        return False

                                    exceptions_checkbox_handle(event8, exceptions_values_window, values8)

                                    if event8 == "CONTINUE_EXCEPTIONS":
                                        if values8["no filtering checkbox"]:
                                            # ?????????? ?????????????????? ??????????????
                                            globals.filter_type = globals.Filter.NONE
                                            finish_while_loop = True
                                            exceptions_values_window.close()
                                            break
                                        else:
                                            if values8["checkbox exceptions RR"] and not values8["checkbox exceptions BPM"]:
                                                globals.RR_lower = float(values8['_SPIN_RR_LOWER'])
                                                globals.RR_upper = float(values8['_SPIN_RR_UPPER'])
                                                if checks_boundaries(globals.RR_lower, globals.RR_upper):
                                                    globals.filter_type = globals.Filter.RR
                                                    finish_while_loop = True
                                                    break
                                                else:
                                                    sg.popup_quick_message(
                                                        'Error! Notice that the lower RR limit must be smaller than the upper RR limit',
                                                        font=("Century Gothic", 10),
                                                        background_color='white', text_color='red', location=(670, 655))

                                            if values8["checkbox exceptions BPM"] and not values8["checkbox exceptions RR"]:
                                                globals.BPM_lower = int(values8['_SPIN_BPM_LOWER'])
                                                globals.BPM_upper = int(values8['_SPIN_BPM_UPPER'])
                                                if checks_boundaries(globals.BPM_lower, globals.BPM_upper):
                                                    globals.filter_type = globals.Filter.BPM
                                                    finish_while_loop = True
                                                    break
                                                else:
                                                    sg.popup_quick_message(
                                                        'Error! Notice that the lower BPM limit must be smaller than the upper BPM limit',
                                                        font=("Century Gothic", 10),
                                                        background_color='white', text_color='red', location=(670, 655))

                                            if values8["checkbox exceptions BPM"] and values8["checkbox exceptions RR"]:
                                                globals.RR_lower = float(values8['_SPIN_RR_LOWER'])
                                                globals.RR_upper = float(values8['_SPIN_RR_UPPER'])
                                                globals.BPM_lower = int(values8['_SPIN_BPM_LOWER'])
                                                globals.BPM_upper = int(values8['_SPIN_BPM_UPPER'])
                                                if checks_boundaries(globals.BPM_lower,
                                                                     globals.BPM_upper) and checks_boundaries(
                                                    globals.RR_lower, globals.RR_upper):
                                                    globals.filter_type = globals.Filter.BOTH
                                                    finish_while_loop = True
                                                    break
                                                else:
                                                    sg.popup_quick_message(
                                                        'Error! Notice that the lower limits must be smaller than the upper limits',
                                                        font=("Century Gothic", 10),
                                                        background_color='white', text_color='red', location=(670, 655))
                                    if event8 == "BACK_EXCEPTIONS":
                                        exceptions_values_window.hide()
                                        path_load_window.un_hide()
                                        correct_path_window = False  # ?????????? ???????????? ?????? ?????????? ???? ?????????????? ???? ???????????? ??????
                                        finish_while_loop = False
                                        break

                                if finish_while_loop:
                                    exceptions_values_window.close()
                                    path_load_window.close()
                                    break
                            else:
                                finish_while_loop = True
                                globals.percent = 1
                                break

                    if finish_while_loop:
                        break
        if finish_while_loop and is_newload:
            # ------------------------------------------- CHECK_IF_NEWLOAD_OR_EXIST --------------------------------
            # ------------------------------------------- LOADING Window -------------------------------------------
            loading_window = sg.Window(title="loading", layout=layout_loading_window, size=(500, 500),
                                       disable_minimize=True,
                                       location=(700, 250), background_image="./load.png", element_padding=(0, 0),
                                       finalize=True)
            start_time = time.time()  # ?????????? ?????? ?????????? ???????? ??????????
            # ???????? ?????? ???????????? ???? ???????????????? ?????????????? ???????? ???????? ???? ????????
            t = threading.Thread(target=early_process if is_newload else pickle_early_process)
            t.setDaemon(True)  # ???????? ???????? "????????" ???????????? ???????? ?????????? ????????
            t.start()  # ?????????? ???????? ????????
            while True:
                event3, values3 = loading_window.read(timeout=1)
                # ---------------------------------- update window elements ----------------------------------
                loading_window_update(loading_window, start_time)
                if globals.percent * 100 >= 99.9:
                    loading_window_update(loading_window, start_time)
                    time.sleep(3)
                    break
                if event3 == "p bar cancel" or event3 == sg.WIN_CLOSED:
                    sys.exit()  # ?????????? ?????????? ???? ????????????, ???????? "????"
            loading_window.close()

        if globals.percent * 100 >= 99.99:  # ???? ?????????? ?????????? ???????? ?????????????? ???????? ????????????, ???????? ?????????? ???? ?????????? ??????
            data_quality_table_window, dq_table_list, graph_window, summary_table_list, summary_table_window = windows_initialization_part_2(is_newload)
            do_restart = False
            while True:
                summary_table_window.element("SumTable").update(
                    values=summary_table_list)  # ???????? ?????????????? ?????????? ?????????? ??????????
                event4, values4 = summary_table_window.read()
                if event4 == "summary exit" or event4 == sg.WIN_CLOSED:
                    break
                if event4 == "Restart button":
                    do_restart = True
                    break
                if event4 == 'Export to CSV':
                    exportEXCEL_summary(values4)
                if event4 == "Graphs button":
                    summary_table_window.hide()
                    graph_window.un_hide()
                    while True:
                        y_axis_choose = True
                        x_axis_choose = True
                        rides_choose = True
                        scenarios_choose = True
                        participants_choose = True
                        event5, values5 = graph_window.read()
                        graph_window.bring_to_front()

                        if event5 == "custom graph":
                            window_update_custom_graph(graph_window)

                        if event5 == "general graph":
                            window_update_general_graph(graph_window)

                        if event5 == "x axis rides":
                            window_update_x_axis_rides(graph_window)

                        if event5 == "x axis scenarios":
                            window_update_x_axis_scenarios(graph_window)

                        if event5 == "bar groups":
                            graph_window['participant listbox'].update("")
                            graph_window['participant listbox'].update(globals.list_of_existing_par)
                            graph_window['participant listbox'].update(disabled=True)

                        if event5 == "bar pars":
                            graph_window['participant listbox'].update(disabled=False)

                        if event5 == "SELECT ALL rides":
                            graph_window['rides listbox'].SetValue(globals.rides_list)

                        if event5 == "CLEAN ALL rides":
                            graph_window['rides listbox'].update("")
                            graph_window['rides listbox'].update(globals.rides_list)

                        if event5 == "SELECT ALL sc":
                            graph_window['scenarios listbox'].SetValue(globals.scenarios_list)
                        if event5 == "CLEAN ALL sc":
                            graph_window['scenarios listbox'].update("")
                            graph_window['scenarios listbox'].update(globals.scenarios_list)

                        if event5 == "graphs back":
                            graph_window.hide()
                            summary_table_window.un_hide()
                            break

                        if event5 == "CONTINUE_GRAPH":
                            if values5["custom graph"]:
                                if not values5['y axis']:  # ???? ???? ???????? ?????? ?????????????? ??????????
                                    sg.popup_quick_message('You have to choose Y axis!',
                                                           font=("Century Gothic", 14), background_color='red',
                                                           location=(970, 880))
                                    y_axis_choose = False

                                if values5["x axis rides"]:  # ????????????
                                    if not values5['rides listbox']:  # ?????? ???? ?????????? ?????????????????? ????????????
                                        sg.popup_quick_message('You have to choose specific rides!',
                                                               font=("Century Gothic", 14), background_color='red',
                                                               location=(970, 880))
                                        rides_choose = False
                                    else:  # ?????????? ???????????? ?????????????? ??????????????????
                                        if y_axis_choose and rides_choose:
                                            axis_y_input = values5['y axis']
                                            # axis_x_scenarios_input = values5['scenarios listbox']
                                            rides_input = values5['rides listbox']

                                            if values5["bar pars"]:
                                                if not values5['participant listbox']:  # ???? ?????????? ??????????????
                                                    sg.popup_quick_message('You have to choose specific participants!',
                                                                           font=("Century Gothic", 14),
                                                                           background_color='red',
                                                                           location=(970, 880))
                                                    participants_choose = False
                                                else:  # ?????????? ??????????????
                                                    if len(values5['participant listbox']) > 5:
                                                        sg.popup_quick_message(
                                                            'You have to choose up to 5 participants!',
                                                            font=("Century Gothic", 14),
                                                            background_color='red',
                                                            location=(970, 880))
                                                    else:  # ?????????? ???? 5 ??????????????
                                                        bar_participants_input = values5['participant listbox']
                                                        # print("?????????? ???? ?????? p4 ???? ???????????? ???????? ???????? ???????????????? ??????????????")
                                                        axis_y_input = values5['y axis']
                                                        p4 = Process(target=plot_rides, args=(
                                                            bar_participants_input, rides_input, axis_y_input,
                                                            globals.summary_table))
                                                        p4.start()

                                            else:  # ?????????? ????????????
                                                """
                                                print("y axis:" +
                                                      axis_y_input + " ,axis x of rides: " + str(
                                                      rides_input) + " with groups" + str(globals.group_num))
                                                print(
                                                    "?????????? ???? ?????? p6 ???? ???????????? ???????? ???????? ???????????????? ???????????? ")
                                                """
                                                axis_y_input = values5['y axis']
                                                p6 = Process(target=plot_groups_rides, args=(
                                                    globals.group_num, rides_input, axis_y_input,
                                                    globals.summary_table))
                                                p6.start()
                                if values5["x axis scenarios"]:  # ???? ?????????? ?????????????? ???????? ????????
                                    if not values5["scenarios listbox"]:  # ???? ?????????? ??????????????
                                        sg.popup_quick_message('You have to choose specific scenarios!',
                                                               font=("Century Gothic", 14), background_color='red',
                                                               location=(970, 880))
                                        scenarios_choose = False
                                    if y_axis_choose and scenarios_choose:
                                        axis_y_input = values5['y axis']
                                        axis_x_scenarios_input = values5['scenarios listbox']
                                        if values5["bar pars"]:
                                            if not values5['participant listbox']:  # ???? ?????????? ??????????????
                                                sg.popup_quick_message('You have to choose specific participants!',
                                                                       font=("Century Gothic", 14),
                                                                       background_color='red',
                                                                       location=(970, 880))
                                                participants_choose = False
                                            else:  # ?????????? ??????????????
                                                if len(values5['participant listbox']) > 5:
                                                    sg.popup_quick_message(
                                                        'You have to choose up to 5 participants!',
                                                        font=("Century Gothic", 14),
                                                        background_color='red',
                                                        location=(970, 880))
                                                else:  # ?????????? ???? 5 ??????????????
                                                    bar_participants_input = values5['participant listbox']
                                                    """
                                                    print("y axis:" + str(
                                                        axis_y_input) + " ,axis x scenarios: " + str(
                                                        axis_x_scenarios_input) + " participants: " + str(bar_participants_input))
                                                    print(
                                                        "?????????? ???? ?????? p3 ???? ?????????????? ???????? ???????? ???????????????? ?????????????? ")
                                                    """
                                                    axis_y_input = values5['y axis']
                                                    p3 = Process(target=plot_with_scenarios, args=(
                                                        axis_x_scenarios_input, bar_participants_input,
                                                        axis_y_input, globals.summary_table))
                                                    p3.start()

                                        else:  # ?????????? ???????????? ????????????????
                                            """
                                            print("y axis:" + str(
                                                axis_y_input) + " ,axis x of scenarios: " + str(
                                                axis_x_scenarios_input) + "with groups " + str(globals.group_num))
                                            print(
                                                "?????????? ???? ?????? p5 ???? ?????????????? ???????? ???????? ???????????????? ???????????? ")
                                            """
                                            axis_y_input = values5['y axis']
                                            p5 = Process(target=plot_groups_scenarios,
                                                         args=(axis_x_scenarios_input,
                                                               globals.group_num, axis_y_input,
                                                               globals.summary_table))
                                            p5.start()

                            else:  # choose general graphs
                                if not values5['y axis']:  # ???? ???? ???????? ?????? ?????????????? ??????????
                                    sg.popup_quick_message('You have to choose Y axis!',
                                                           font=("Century Gothic", 14), background_color='red',
                                                           location=(970, 880))
                                else:  # ???????? ??????
                                    axis_y_input = values5['y axis']
                                    p7 = Process(target=general_graph_avg,
                                                 args=(globals.scenarios_list,
                                                       globals.rides_list,
                                                       axis_y_input,
                                                       globals.summary_table))
                                    p7.start()

                if event4 == "dq button":
                    summary_table_window.hide()
                    data_quality_table_window.un_hide()
                    data_quality_table_window.element("dq export").update(visible=True)
                    while True:
                        data_quality_table_window.element("DataQTable").update(
                            values=dq_table_list)  # ???????? ?????????????? ?????????? ?????????? ??????????
                        event6, values6 = data_quality_table_window.read()
                        data_quality_table_window.bring_to_front()
                        if event6 == "dq back":
                            data_quality_table_window.hide()
                            summary_table_window.un_hide()
                            break
                        if event6 == "dq export":
                            exportEXCEL_dq()
                if event4 == "SumTable":
                    if values4["SumTable"]:
                        line = [dq_table_list[values4["SumTable"][0]]]
                        summary_table_window.hide()
                        data_quality_table_window.un_hide()
                        data_quality_table_window.element("dq export").update(visible=False)
                        while True:
                            data_quality_table_window.element("DataQTable").update(
                                values=line)  # ???????? ?????????????? ?????????? ?????????? ??????????
                            event7, values7 = data_quality_table_window.read()
                            if event7 == "dq back":
                                data_quality_table_window.hide()
                                summary_table_window.un_hide()
                                break
            open_window.close()
            data_quality_table_window.close()
            graph_window.close()
            summary_table_window.close()
            return do_restart


if __name__ == '__main__':
    restart = ui()
    if restart:
        os.system('main.py')
        exit()
    else:
        sys.exit(0)
