import PySimpleGUIQt as sg
from numpy import linspace
import globals

"""
This class contains the implementation of the UI windows (Buttons, Layous, Lables, etc.)
"""


def graphs_window_layout():
    participants_list = globals.list_of_existing_par
    globals.scenarios_list = list(range(1, globals.scenario_num + 1))
    globals.rides_list = list(range(1, globals.par_ride_num + 1))

    layout_graphs_window = \
        [
            [
                sg.Column(layout=[
                    [sg.Text(text="", background_color="transparent", size_px=(0, 90), )],  # first row
                    [  # second row
                        sg.Text(text="", background_color="transparent", size_px=(110, 50), justification="center"),
                        sg.Text(text="Choose Graph", background_color="transparent", text_color='black',
                                size_px=(600, 100), font=("Century Gothic", 42, 'bold')),
                    ],
                    [  # third row
                        sg.Text("", background_color="transparent", size=(0, 20))
                    ],
                    [
                        sg.Radio(group_id="GRAPH", text="   Custom Graph",
                                 background_color="transparent",
                                 key='custom graph', size_px=(300, 35), font=("Century Gothic", 16, 'bold'),
                                 enable_events=True, text_color='red', default=True),
                        sg.Text("", background_color="transparent", size=(1, 0)),
                        sg.Radio(group_id="GRAPH", text="  General Graph", background_color="transparent",
                                 key="general graph", size=(300, 35), font=("Century Gothic", 16, 'bold'),
                                 enable_events=True,
                                 text_color='red'),
                    ],
                    [
                        sg.Text("", background_color="transparent", size=(0, 3)),
                        sg.Text('      Y axis:', size=(20, 1), background_color="transparent",
                                visible=True, key='y axis text', font=("Century Gothic", 16, 'bold'), text_color='red'),
                        sg.Combo(values=globals.methods_list, size=[300, 37], key='y axis', visible=True,
                                 enable_events=True, readonly=True,
                                 font=("Century Gothic", 12)),
                    ],
                    [
                        sg.Text('      X axis:', size=(21, 1), background_color="transparent",
                                visible=True, key='x axis text', font=("Century Gothic", 16, 'bold'), text_color='red'),
                        sg.Radio(group_id="X", text="Rides", background_color="transparent",
                                 key="x axis rides", size=(250, 35), font=("Century Gothic", 14, 'bold'),
                                 enable_events=True, text_color='black', default=True),
                        sg.Radio(group_id="X", text="Scenarios", background_color="transparent",
                                 key="x axis scenarios", size=(250, 35), font=("Century Gothic", 14, 'bold'),
                                 enable_events=True, text_color='black', default=False),
                        sg.Text("", background_color="transparent", size=(3, 0)),

                    ],
                    [
                        sg.Text("", background_color="transparent", size=(21, 2)),
                        sg.Listbox(values=globals.rides_list, size=[150, 100], key='rides listbox', visible=True,
                                   enable_events=True,
                                   font=("Century Gothic", 12),
                                   select_mode=sg.SELECT_MODE_MULTIPLE),
                        sg.Text("", background_color="transparent", size=(12, 0)),
                        sg.Listbox(values=globals.scenarios_list, size=[150, 100], key='scenarios listbox',
                                   visible=True,
                                   enable_events=True, disabled=True,
                                   font=("Century Gothic", 12), select_mode=sg.SELECT_MODE_MULTIPLE),
                    ],

                    [
                        sg.Text("", background_color="transparent", size=(21, 0),
                                font=("Century Gothic", 16)),
                        sg.Button("SELECT ALL", size=(70, 30), font=("Century Gothic", 6), key="SELECT ALL rides",
                                  enable_events=True),
                        sg.Text("", background_color="transparent", size=(1, 0),
                                font=("Century Gothic", 16)),
                        sg.Button("CLEAN ALL", size=(70, 30), font=("Century Gothic", 6), key="CLEAN ALL rides",
                                  enable_events=True),
                        sg.Text("", background_color="transparent", size=(12, 0),
                                font=("Century Gothic", 16)),
                        sg.Button("SELECT ALL", size=(70, 30), font=("Century Gothic", 6), key="SELECT ALL sc",
                                  enable_events=True, disabled=True),
                        sg.Text("", background_color="transparent", size=(1, 0),
                                font=("Century Gothic", 16)),
                        sg.Button("CLEAN ALL", size=(70, 30), font=("Century Gothic", 6), key="CLEAN ALL sc",
                                  enable_events=True, disabled=True)
                    ],
                    [
                        sg.Text("", background_color="transparent", size=(0, 3)),
                        sg.Text('      Choose bar:', size=(30, 2), background_color="transparent",
                                visible=True, font=("Century Gothic", 16, 'bold'), text_color='red'),
                        sg.Radio(group_id="bar", text="Participants\n(up to 5)", background_color="transparent",
                                 key="bar pars", size=(250, 65), font=("Century Gothic", 14, 'bold'),
                                 enable_events=True, text_color='black', default=True),
                        sg.Radio(group_id="bar", text="Groups", background_color="transparent",
                                 key="bar groups", size=(240, 35), font=("Century Gothic", 14, 'bold'),
                                 enable_events=True, text_color='black', default=False),
                    ],
                    [

                        sg.Text("", background_color="transparent", size=(30, 2)),
                        sg.Listbox(values=participants_list, size=[150, 150], key='participant listbox', visible=True,
                                   enable_events=True,
                                   font=("Century Gothic", 12),
                                   select_mode=sg.SELECT_MODE_MULTIPLE),
                    ],
                    [
                        sg.Text("", background_color="transparent", size=(0, 100)),
                    ],
                    [
                        sg.Text("", background_color="transparent", size=(20, 0)),
                        sg.Button("BACK", size=(150, 45), font=("Century Gothic", 18), key="graphs back",
                                  enable_events=True),
                        sg.Text("", background_color="transparent", size=(80, 35),
                                font=("Century Gothic", 16)),
                        sg.Button("CONTINUE", size=(220, 45), font=("Century Gothic", 18), key="CONTINUE_GRAPH",
                                  enable_events=True)
                    ]
                ], background_color="transparent")
            ]

        ]
    return layout_graphs_window


def data_quality_table_window_layout(dq_table_list):
    layout_data_quality_table_window = \
        [
            [
                sg.Column(layout=[
                    [sg.Text(text="", background_color="transparent", size_px=(0, 80))],
                    [sg.Table(values=dq_table_list, headings=globals.header_data_quality,
                              auto_size_columns=True, bind_return_key=True,
                              num_rows=18, background_color="white", alternating_row_color="lightblue",
                              enable_events=True, key="DataQTable", font=("Century Gothic", 10),
                              text_color="black", justification='center')],
                    [
                        sg.Text(text="", background_color="transparent", size_px=(600, 50)),
                        sg.Button(button_text="BACK", size_px=(150, 60), key="dq back", enable_events=True,
                                  font=("Century Gothic", 16),
                                  tooltip="Back to summary table"),
                        sg.Text(text="", background_color="transparent", size_px=(100, 0)),
                        sg.Button(button_text="Export to EXCEL", size_px=(275, 60), key="dq export",
                                  enable_events=True, font=("Century Gothic", 16),
                                  tooltip="Select a folder to export the table to a XLSX file")

                    ],
                ], background_color="transparent"
                )
            ]
        ]
    return layout_data_quality_table_window


def summary_table_window_layout(summary_table_list):
    layout_summary_table_window = \
        [
            [
                sg.Column(layout=[
                    [sg.Text(text="", background_color="transparent", size_px=(0, 140), )],
                    [
                        sg.Checkbox("Average BPM", background_color='transparent', key='Average BPM', default=True,
                                    enable_events=True, font=("Century Gothic", 13), text_color="black",
                                    tooltip="Average of the number of heart beats per minute (BPM).")
                    ],
                    [
                        sg.Checkbox("RMSSD", background_color='transparent', key='RMSSD', default=True,
                                    enable_events=True, font=("Century Gothic", 13), text_color="black",
                                    tooltip="The root mean square of successive differences between normal heartbeats (RMSSD) is obtained by first calculating each successive time difference between heartbeats in ms. Then, each of the values is squared and the result is averaged before the square root of the total is obtained.")
                    ],
                    [
                        sg.Checkbox("SDSD", background_color='transparent', key='SDSD', default=True,
                                    enable_events=True, font=("Century Gothic", 13), text_color="black",
                                    tooltip="The standard deviation of successive RR interval differences (SDSD).")
                    ],
                    [
                        sg.Checkbox("SDNN", background_color='transparent', key='SDNN', default=True,
                                    enable_events=True, font=("Century Gothic", 13), text_color="black",
                                    tooltip="The standard deviation of the IBI(Inter-Beat Interval) of normal sinus beats (SDNN) is measured in ms.")
                    ],
                    [
                        sg.Checkbox("pNN50", background_color='transparent', key='pNN50', default=True,
                                    enable_events=True, font=("Century Gothic", 13), text_color="black",
                                    tooltip="The percentage of adjacent NN intervals that differ from each other by more than 50 ms (pNN50).")
                    ],
                    [
                        sg.Checkbox("Baseline", background_color='transparent', key='Baseline', default=True,
                                    enable_events=True, font=("Century Gothic", 13), text_color="black",
                                    tooltip="Resting column for each selected HRV method.")
                    ],
                    [sg.Text(text="", background_color="transparent", size_px=(0, 60))],
                    [sg.Button(button_text="Export to EXCEL", size_px=(275, 60), key="Export to CSV",
                               enable_events=True, font=("Century Gothic", 16),
                               tooltip="Select a folder to export the table to a XLSX file")]
                ], background_color="transparent"),
                sg.Column(layout=[
                    [sg.Text(text="", background_color="transparent", size_px=(0, 60))],
                    [sg.Table(values=summary_table_list, headings=globals.header_summary_table,
                              auto_size_columns=True, bind_return_key=True,
                              num_rows=18, background_color="white", alternating_row_color="lightblue",
                              enable_events=True, key="SumTable", font=("Century Gothic", 10),
                              text_color="black", justification='center')],
                    [sg.Text(text="", background_color="transparent", size_px=(100, 100))],
                ], background_color="transparent"
                ),
                sg.Column(layout=[
                    [sg.Text(text="", background_color="transparent", size_px=(200, 250))],
                    [sg.Button(button_text="Data Quality", size_px=(220, 60), key="dq button", enable_events=True,
                               font=("Century Gothic", 16))],
                    [sg.Text(text="", background_color="transparent", size_px=(200, 50))],
                    [sg.Button(button_text="Graphs", size_px=(220, 60), key="Graphs button", enable_events=True,
                               font=("Century Gothic", 16))],
                    [sg.Text(text="", background_color="transparent", size_px=(200, 50))],
                    [sg.Button(button_text="Restart", size_px=(220, 60), key="Restart button", enable_events=True,
                               font=("Century Gothic", 16),
                               tooltip="Reboot the program and insert a new experiment")],
                    [sg.Text(text="", background_color="transparent", size_px=(200, 50))],
                    [sg.Button(button_text="EXIT", size_px=(220, 60), key="summary exit", enable_events=True,
                               font=("Century Gothic", 16))],
                ], background_color="transparent", element_justification="center"
                )
            ]
        ]
    return layout_summary_table_window


def loading_window_layout():
    layout_loading_window = \
        [
            [
                sg.Text(text="", background_color="transparent", size_px=(100, 70))
            ],
            [
                sg.Text(text="              1 of " + str(globals.par_num), background_color="transparent",
                        text_color='black',
                        size_px=(450, 50), font=("Century Gothic", 20), key="num of num", enable_events=True)
            ],
            [
                sg.Text(text="              ", background_color="transparent", size_px=(100, 45)),
                sg.Text(text="", background_color="transparent", text_color='black',
                        size_px=(350, 60),
                        font=("Century Gothic", 20), key="current_ride", enable_events=True),
            ],
            [
                sg.Text(text="               ", background_color="transparent", size_px=(185, 35)),
                sg.Text(text=str(globals.percent * 100) + " %", background_color="transparent", text_color='black',
                        size_px=(200, 60),
                        font=("Century Gothic", 24), key="percent", enable_events=True),
            ],
            [
                sg.Text(text="", background_color="transparent", size_px=(100, 30))
            ],
            [
                sg.Text(text="    Time elapsed:  ", background_color="transparent", text_color='black',
                        size_px=(300, 35), font=("Century Gothic", 16)),
                sg.Text("00:00:00", background_color="transparent", text_color='black', size_px=(150, 35),
                        font=("Century Gothic", 16), key="Time elapsed", enable_events=True)
            ],
            [
                sg.Text(text="", background_color="transparent", size_px=(100, 50))
            ],
            [
                sg.Text(text="  ", background_color="transparent", size_px=(10, 50)),
                sg.ProgressBar(max_value=100, start_value=0, orientation='h', size_px=(450, 50), key="p bar", )
            ],
            [
                sg.Text(text="", background_color="transparent", size_px=(100, 30))
            ],
            [
                sg.Text(text="", background_color="transparent", size_px=(165, 50)),
                sg.Button(button_text="CANCEL", size_px=(150, 60), key="p bar cancel", enable_events=True,
                          font=("Century Gothic", 16),
                          tooltip="Clicking this button will forcibly stop the program from running. Please note that nothing will be saved!")
            ],

        ]
    return layout_loading_window


def exceptions_values_layout():
    layout_exceptions_values = \
        [

            [
                sg.Text("", background_color="transparent", size=(0, 100))
            ],
            [  # second row
                sg.Text("", background_color="transparent", size_px=(200, 0)),
                sg.Text(text="Exceptions Filtering", background_color="transparent", text_color='black',
                        size_px=(600, 100), font=("Century Gothic", 32, 'bold'), ),
            ],
            [
                sg.Text("", background_color="transparent", size=(5, 0)),
                sg.Checkbox("No filtering", background_color='transparent', key='no filtering checkbox', default=True,
                            enable_events=True, text_color='red', font=("Century Gothic", 16, 'bold'),
                            size_px=(670, 36)),
            ],
            [
                sg.Text("", background_color="transparent", size=(0, 40)),
            ],
            [
                sg.Text("", background_color="transparent", size=(5, 0)),
                sg.Checkbox("Exceptions values - RR intervals", background_color='transparent',
                            key='checkbox exceptions RR', default=False,
                            enable_events=True, text_color='red', font=("Century Gothic", 16, 'bold'),
                            size_px=(670, 35))
            ],

            [
                sg.Text("", background_color="transparent", size=(15, 0)),
                sg.Text('choose desired range of RR values:', size=(52, 1), background_color="transparent",
                        visible=True,
                        key='choose desired RR range',
                        font=("Century Gothic", 14), text_color='black'),
                sg.Spin([round(i, 1) for i in list(linspace(0, 2, 21))], initial_value=0.6, key='_SPIN_RR_LOWER',
                        size=(7, 1.2),
                        font=("Century Gothic", 14), tooltip="Lower boundary", enable_events=True, disabled=True),
                sg.Text(' - ', size=(2.5, 1), background_color="transparent",
                        visible=True, font=("Century Gothic", 16), text_color='black'),
                sg.Spin([round(i, 1) for i in list(linspace(0, 2, 21))], initial_value=1.2, key='_SPIN_RR_UPPER',
                        size=(7, 1.2),
                        font=("Century Gothic", 14), tooltip="Upper boundary", enable_events=True, disabled=True),
            ],
            [
                sg.Text("", background_color="transparent", size=(0, 40)),
            ],
            [
                sg.Text("", background_color="transparent", size=(5, 0)),
                sg.Checkbox("Exceptions values - ECG BPM", background_color='transparent',
                            key='checkbox exceptions BPM', default=False,
                            enable_events=True, text_color='red', font=("Century Gothic", 16, 'bold'),
                            size_px=(670, 35))

            ],

            [
                sg.Text("", background_color="transparent", size=(15, 0)),
                sg.Text('choose desired range of BPM values:', size=(52, 1), background_color="transparent",
                        visible=True,
                        key='choose desired BPM range',
                        font=("Century Gothic", 14), text_color='black'),
                sg.Spin([str(i) for i in range(0, 201, 1)], change_submits=True, initial_value="40",
                        key='_SPIN_BPM_LOWER', size=(7, 1.2),
                        font=("Century Gothic", 14), tooltip="Lower boundary", enable_events=True, disabled=True),
                sg.Text(' - ', size=(2.5, 1), background_color="transparent",
                        visible=True, font=("Century Gothic", 16), text_color='black'),
                sg.Spin([str(i) for i in range(0, 201, 1)], change_submits=True, initial_value='140',
                        key='_SPIN_BPM_UPPER', size=(7, 1.2), font=("Century Gothic", 14), tooltip="Upper boundary",
                        enable_events=True, disabled=True),
            ],

            [sg.Text(text="", background_color="transparent", size_px=(0, 110), )],
            [
                sg.Text("", background_color="transparent", size_px=(250, 0),
                        font=("Century Gothic", 16)),
                sg.Button("BACK", size=(150, 45), font=("Century Gothic", 18), key="BACK_EXCEPTIONS",
                          enable_events=True),
                sg.Text("", background_color="transparent", size=(80, 35),
                        font=("Century Gothic", 16)),
                sg.Button("CONTINUE", size=(220, 45), font=("Century Gothic", 18), key="CONTINUE_EXCEPTIONS",
                          enable_events=True)
            ]

        ]
    return layout_exceptions_values


def path_load_window_layout():
    layout_path_load_window = \
        [
            [
                sg.Text("", background_color="transparent", size=(0, 15)),
            ],
            [
                sg.Text("", background_color="transparent", size=(1050, 20)),
                sg.Text("Please choose the main folder", background_color="transparent",
                        font=("Century Gothic", 18, 'bold'),
                        text_color='black', size=(650, 30)),
            ],
            [
                sg.Text("", background_color="transparent", size=(1100, 20)),
                sg.Radio(group_id="LOAD", text="New Load", background_color='transparent', key='NEW LOAD', default=True,
                         font=("Century Gothic", 13, 'bold'), text_color='red', size_px=(230, 30)),
                sg.Radio(group_id="LOAD", text="Existing Load", background_color='transparent', key='EXIST LOAD',
                         font=("Century Gothic", 13, 'bold'), text_color='red', size_px=(250, 30)),
            ],
            [
                sg.Text("", background_color="transparent", size=(970, 20)),
                sg.Text("Main Folder", background_color="transparent", text_color='black',
                        font=("Century Gothic", 12, 'bold'), size_px=(150, 30)),
                sg.In(size=(49, 1), enable_events=True, key="-MAIN FOLDER-", font=("Century Gothic", 8), disabled=True),
                sg.FolderBrowse(button_text="...", enable_events=True, key="main path button", size=(40, 35)),
            ],
            [
                sg.Text("", background_color="transparent", size=(1120, 20)),
                sg.Tree(data=sg.TreeData(),
                        headings=[""],
                        auto_size_columns=False,
                        num_rows=29,
                        def_col_width=0,
                        col0_width=0,
                        key='-TREE-',
                        size_px=(490, 1200),
                        text_color='black',
                        background_color='white',
                        show_expanded=False,
                        enable_events=True,
                        tooltip="The contents of the selected \"main folder\""),
            ],
            [
                sg.Text("", background_color="transparent", size=(262, 20)),
                sg.Button("Create empty folders", size=(414, 45), font=("Century Gothic", 18),
                          key="Create empty folders",
                          enable_events=True,
                          tooltip="Clicking this button will create in the selected path: \"main folder\" and all subfolders by the format. If there is a folder named \"main folder\" in the selected path - the contents of the folder will be replaced. Fill in the folders and then go back to the software and choose the main folder on the right side of this window"),
                sg.Text("", background_color="transparent", size=(480, 20)),
                sg.Button("BACK", size=(150, 45), font=("Century Gothic", 18), key="BACK_PATH",
                          tooltip="Return to the experiment data entry screen"),
                sg.Text("", background_color="transparent", size=(50, 35),
                        font=("Century Gothic", 16)),
                sg.Button("CONTINUE", size=(220, 45), font=("Century Gothic", 18), key="CONTINUE_PATH",
                          enable_events=True),
            ],
            [
                sg.Text("", background_color="transparent", size=(0, 20)),
            ]
        ]
    return layout_path_load_window


def optional_window_layout():
    layout_optional_window = \
        [
            [
                sg.Text("", background_color="transparent", size=(250, 440))
            ],
            [
                sg.Text("", background_color="transparent", size=(40, 0)),
                sg.Checkbox("Excluded participants", background_color='transparent', key='Ex par CB', default=False,
                            enable_events=True, font=("Century Gothic", 18), text_color="black", size_px=(480, 50),
                            tooltip="Participants were excluded from the experiment?"),
                sg.Listbox(list(range(1, globals.par_num + 1)), size=(7, 3.5), key='Ex par LB', select_mode='multiple',
                           disabled=True, enable_events=True, font=("Century Gothic", 11)),
                sg.Text("", background_color="transparent", size=(5, 0)),
                sg.Button("Exclude", size=(160, 50), font=("Century Gothic", 16), key="Exclude_OPTIONAL",
                          enable_events=True, visible=False,
                          tooltip="Clicking this button will remove the selected participants from the list of experiment participants."),
            ],
            [
                sg.Text("", background_color="transparent", size=(250, 50))
            ],
            [
                sg.Text("", background_color="transparent", size=(40, 0)),
                sg.Checkbox("Experimental groups", background_color='transparent', key='groups CB', default=False,
                            enable_events=True, font=("Century Gothic", 18), text_color="black", size_px=(490, 50),
                            tooltip="Are the participants in the experiment divided into groups?"),
                sg.Combo(values=[2, 3, 4, 5], size=[50, 40], key='groups num', enable_events=True,
                         font=("Century Gothic", 14), readonly=True, disabled=True),
                sg.Text("", background_color="transparent", size=(6, 0)),
                sg.Button("Choose", size=(160, 50), font=("Century Gothic", 16), key="Choose_OPTIONAL",
                          enable_events=True, visible=False,
                          tooltip="Clicking on this button will create groups and allow you to select participants belonging to each group"),
            ],
            [
                sg.Text("", background_color="transparent", size=(0, 20)),
            ],
            [
                sg.Text("", background_color="transparent", size=(500, 140)),
                sg.Listbox(list(range(1, globals.par_num + 1)), size=(7, 4), key='group1', select_mode='multiple',
                           visible=False, enable_events=True, font=("Century Gothic", 11), tooltip='Group 1'),
                sg.Text("", background_color="transparent", size=(10, 0)),
                sg.Listbox(list(range(1, globals.par_num + 1)), size=(7, 4), key='group2', select_mode='multiple',
                           visible=False, enable_events=True, font=("Century Gothic", 11), tooltip='Group 2'),
                sg.Text("", background_color="transparent", size=(10, 0)),
                sg.Listbox(list(range(1, globals.par_num + 1)), size=(7, 4), key='group3', select_mode='multiple',
                           visible=False, enable_events=True, font=("Century Gothic", 11), tooltip='Group 3'),
                sg.Text("", background_color="transparent", size=(10, 0)),
                sg.Listbox(list(range(1, globals.par_num + 1)), size=(7, 4), key='group4', select_mode='multiple',
                           visible=False, enable_events=True, font=("Century Gothic", 11), tooltip='Group 4'),
                sg.Text("", background_color="transparent", size=(10, 0)),
                sg.Listbox(list(range(1, globals.par_num + 1)), size=(7, 4), key='group5', select_mode='multiple',
                           visible=False, enable_events=True, font=("Century Gothic", 11), tooltip='Group 5'),
            ],
            [
                sg.Text("", background_color="transparent", size=(320, 75)),
            ],
            [
                sg.Text("                                   ", background_color="transparent", size=(670, 35),
                        font=("Century Gothic", 16)),
                sg.Button("BACK", size=(150, 45), font=("Century Gothic", 18), key="BACK_OPTIONAL",
                          enable_events=True, tooltip="Return to the experiment data entry screen"),
                sg.Text("", background_color="transparent", size=(80, 35),
                        font=("Century Gothic", 16)),
                sg.Button("CONTINUE", size=(220, 45), font=("Century Gothic", 18), key="CONTINUE_OPTIONAL",
                          enable_events=True)
            ]
        ]
    return layout_optional_window


def open_window_layout():
    layout_open_window = \
        [
            [
                sg.Text("", background_color="transparent", size=(250, 450))
            ],
            [
                sg.Text("                         Number of participants", background_color="transparent",
                        size=(670, 40), font=("Century Gothic", 18), text_color='black'),
                sg.Input(size=[80, 40], justification="center", key="par_num", enable_events=True,
                         font=("Century Gothic", 16), tooltip="Enter only digits 0-9"),
                sg.Text("          Number of participant???s rides", background_color="transparent",
                        size=(630, 40), font=("Century Gothic", 18), text_color='black'),
                sg.Combo(values=[1, 2, 3, 4, 5], size=[50, 40], key='par_ride_num', enable_events=True,
                         font=("Century Gothic", 16), readonly=True)

            ],
            [
                sg.Text("", background_color="transparent", size=(250, 20)),
            ],
            [
                sg.Text("                         Number of scenarios", background_color="transparent",
                        size=(670, 40), font=("Century Gothic", 18), text_color='black'),
                sg.Input(size=[80, 40], justification="center", key='scenario_num', enable_events=True,
                         font=("Century Gothic", 16), tooltip="Enter only digits 0-9"),
                sg.Text("          Scenario???s column number", background_color="transparent",
                        size=(630, 40), font=("Century Gothic", 18), text_color='black'),
                sg.Input(size=[80, 40], justification="center", key='scenario_col_num', enable_events=True,
                         font=("Century Gothic", 16), tooltip="Enter only digits 0-9")
            ],
            [
                sg.Text("", background_color="transparent", size=(250, 70)),
            ],
            [
                sg.Text("", background_color="transparent", size=(30, 0)),
                sg.Checkbox("Synchronized", background_color='transparent', key='Sync', default=True,
                            enable_events=True, font=("Century Gothic", 18), text_color="black", size_px=(400, 40),
                            tooltip="Did you run the simulator and the BIOPAC at the same time?"),
                sg.Text("Simulator", background_color="transparent",
                        size=(190, 35), font=("Century Gothic", 18), text_color='black'),
                sg.Input(size=[100, 40], justification="center", key="sim_sync_time", enable_events=True,
                         font=("Century Gothic", 16), default_text="0", disabled=True,
                         tooltip="Insert SEC to remove from simulator files"),
                sg.Text("  ,    ", background_color="transparent", size=(100, 35), font=("Century Gothic", 18),
                        text_color='black'),
                sg.Text("BIOPAC", background_color="transparent",
                        size=(140, 35), font=("Century Gothic", 16), text_color='black'),
                sg.Input(size=[100, 40], justification="center", key='biopac_sync_time', enable_events=True,
                         font=("Century Gothic", 16), default_text="0", disabled=True,
                         tooltip="Insert SEC to remove from ECG & RR files"),
            ],
            [
                sg.Text("", background_color="transparent", size=(320, 240)),
            ],
            [
                sg.Text("                                   ", background_color="transparent", size=(670, 35),
                        font=("Century Gothic", 16)),
                sg.Button("EXIT", size=(110, 45), font=("Century Gothic", 18), key="EXIT_OPEN",
                          enable_events=True),
                sg.Text("", background_color="transparent", size=(80, 35),
                        font=("Century Gothic", 16)),
                sg.Button("CONTINUE", size=(220, 45), font=("Century Gothic", 18), key="CONTINUE_OPEN",
                          enable_events=True)
            ]
        ]
    return layout_open_window
