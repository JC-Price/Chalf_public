# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CHalf_v4AOelXm.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import chalf_v4_3_gui.rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(900, 600)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(900, 600))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.logo_chalf = QLabel(self.centralwidget)
        self.logo_chalf.setObjectName(u"logo_chalf")
        self.logo_chalf.setStyleSheet(u"image: url(:/images/CHalf Protein Logo.png);\n"
"border-color: rgb(0, 0, 0);\n"
"background-color: rgb(255,255,255);")

        self.horizontalLayout.addWidget(self.logo_chalf)

        self.logo_text = QLabel(self.centralwidget)
        self.logo_text.setObjectName(u"logo_text")
        font = QFont()
        font.setFamily(u"Bahnschrift")
        font.setPointSize(36)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.logo_text.setFont(font)
        self.logo_text.setStyleSheet(u"font: 36pt \"Bahnschrift\";\n"
"background-color: rgb(255,255,255);")
        self.logo_text.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.logo_text)

        self.logo_byu = QLabel(self.centralwidget)
        self.logo_byu.setObjectName(u"logo_byu")
        self.logo_byu.setStyleSheet(u"image: url(:/images/Brigham_Young_University_medallion.png);\n"
"border-color: rgb(0, 0, 0);\n"
"background-color: rgb(255,255,255);")

        self.horizontalLayout.addWidget(self.logo_byu)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.mainTabWidget = QTabWidget(self.centralwidget)
        self.mainTabWidget.setObjectName(u"mainTabWidget")
        sizePolicy.setHeightForWidth(self.mainTabWidget.sizePolicy().hasHeightForWidth())
        self.mainTabWidget.setSizePolicy(sizePolicy)
        self.mainTabWidget.setMinimumSize(QSize(880, 0))
        self.workflow_tab = QWidget()
        self.workflow_tab.setObjectName(u"workflow_tab")
        self.gridLayout_3 = QGridLayout(self.workflow_tab)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.groupBox = QGroupBox(self.workflow_tab)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy1)
        self.groupBox.setMinimumSize(QSize(0, 80))
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SetMinimumSize)
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy2)

        self.horizontalLayout_2.addWidget(self.label)

        self.workflow_comboBox = QComboBox(self.groupBox)
        self.workflow_comboBox.addItem("")
        self.workflow_comboBox.addItem("")
        self.workflow_comboBox.setObjectName(u"workflow_comboBox")
        sizePolicy3 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.workflow_comboBox.sizePolicy().hasHeightForWidth())
        self.workflow_comboBox.setSizePolicy(sizePolicy3)
        self.workflow_comboBox.setMinimumSize(QSize(300, 0))
        self.workflow_comboBox.setFocusPolicy(Qt.StrongFocus)

        self.horizontalLayout_2.addWidget(self.workflow_comboBox)

        self.load_workflow_pushButton = QPushButton(self.groupBox)
        self.load_workflow_pushButton.setObjectName(u"load_workflow_pushButton")
        sizePolicy3.setHeightForWidth(self.load_workflow_pushButton.sizePolicy().hasHeightForWidth())
        self.load_workflow_pushButton.setSizePolicy(sizePolicy3)

        self.horizontalLayout_2.addWidget(self.load_workflow_pushButton)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        sizePolicy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy4)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.save_workflow_pushButton = QPushButton(self.groupBox)
        self.save_workflow_pushButton.setObjectName(u"save_workflow_pushButton")
        sizePolicy3.setHeightForWidth(self.save_workflow_pushButton.sizePolicy().hasHeightForWidth())
        self.save_workflow_pushButton.setSizePolicy(sizePolicy3)

        self.horizontalLayout_2.addWidget(self.save_workflow_pushButton)

        self.open_workflow_folder_pushButton = QPushButton(self.groupBox)
        self.open_workflow_folder_pushButton.setObjectName(u"open_workflow_folder_pushButton")
        sizePolicy3.setHeightForWidth(self.open_workflow_folder_pushButton.sizePolicy().hasHeightForWidth())
        self.open_workflow_folder_pushButton.setSizePolicy(sizePolicy3)

        self.horizontalLayout_2.addWidget(self.open_workflow_folder_pushButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_2.addWidget(self.label_3)


        self.gridLayout_3.addWidget(self.groupBox, 0, 0, 1, 1)

        self.groupBox_2 = QGroupBox(self.workflow_tab)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setSpacing(10)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_3.addWidget(self.label_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName(u"label_5")
        sizePolicy5 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy5)
        self.label_5.setMinimumSize(QSize(40, 0))
        self.label_5.setMaximumSize(QSize(65, 16777215))

        self.horizontalLayout_3.addWidget(self.label_5)

        self.add_pp_files_pushButton = QPushButton(self.groupBox_2)
        self.add_pp_files_pushButton.setObjectName(u"add_pp_files_pushButton")

        self.horizontalLayout_3.addWidget(self.add_pp_files_pushButton)

        self.remove_selected_pp_files_pushButton = QPushButton(self.groupBox_2)
        self.remove_selected_pp_files_pushButton.setObjectName(u"remove_selected_pp_files_pushButton")

        self.horizontalLayout_3.addWidget(self.remove_selected_pp_files_pushButton)

        self.clear_pp_files_pushButton = QPushButton(self.groupBox_2)
        self.clear_pp_files_pushButton.setObjectName(u"clear_pp_files_pushButton")

        self.horizontalLayout_3.addWidget(self.clear_pp_files_pushButton)

        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_3.addWidget(self.label_6)

        self.save_manifest_pushButton = QPushButton(self.groupBox_2)
        self.save_manifest_pushButton.setObjectName(u"save_manifest_pushButton")

        self.horizontalLayout_3.addWidget(self.save_manifest_pushButton)

        self.load_manifest_pushButton = QPushButton(self.groupBox_2)
        self.load_manifest_pushButton.setObjectName(u"load_manifest_pushButton")

        self.horizontalLayout_3.addWidget(self.load_manifest_pushButton)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.label_8 = QLabel(self.groupBox_2)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.label_8)

        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.horizontalLayout_24.setContentsMargins(-1, 0, -1, -1)
        self.label_27 = QLabel(self.groupBox_2)
        self.label_27.setObjectName(u"label_27")
        sizePolicy4.setHeightForWidth(self.label_27.sizePolicy().hasHeightForWidth())
        self.label_27.setSizePolicy(sizePolicy4)
        self.label_27.setMinimumSize(QSize(130, 0))

        self.horizontalLayout_24.addWidget(self.label_27)

        self.condname_consecutive_pushButton = QPushButton(self.groupBox_2)
        self.condname_consecutive_pushButton.setObjectName(u"condname_consecutive_pushButton")

        self.horizontalLayout_24.addWidget(self.condname_consecutive_pushButton)

        self.condname_filename_pushButton = QPushButton(self.groupBox_2)
        self.condname_filename_pushButton.setObjectName(u"condname_filename_pushButton")

        self.horizontalLayout_24.addWidget(self.condname_filename_pushButton)

        self.condname_dir_pushButton = QPushButton(self.groupBox_2)
        self.condname_dir_pushButton.setObjectName(u"condname_dir_pushButton")

        self.horizontalLayout_24.addWidget(self.condname_dir_pushButton)


        self.verticalLayout_3.addLayout(self.horizontalLayout_24)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMaximumSize(QSize(130, 16777215))

        self.horizontalLayout_4.addWidget(self.label_7)

        self.concentration_columns_comboBox = QComboBox(self.groupBox_2)
        self.concentration_columns_comboBox.addItem("")
        self.concentration_columns_comboBox.setObjectName(u"concentration_columns_comboBox")
        self.concentration_columns_comboBox.setMinimumSize(QSize(300, 0))
        self.concentration_columns_comboBox.setFocusPolicy(Qt.StrongFocus)

        self.horizontalLayout_4.addWidget(self.concentration_columns_comboBox)

        self.assign_concentration_pushButton = QPushButton(self.groupBox_2)
        self.assign_concentration_pushButton.setObjectName(u"assign_concentration_pushButton")

        self.horizontalLayout_4.addWidget(self.assign_concentration_pushButton)

        self.creat_concentration_pushButton = QPushButton(self.groupBox_2)
        self.creat_concentration_pushButton.setObjectName(u"creat_concentration_pushButton")

        self.horizontalLayout_4.addWidget(self.creat_concentration_pushButton)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.files_tableWidget = QTableWidget(self.groupBox_2)
        if (self.files_tableWidget.columnCount() < 3):
            self.files_tableWidget.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.files_tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.files_tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.files_tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        if (self.files_tableWidget.rowCount() < 3):
            self.files_tableWidget.setRowCount(3)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.files_tableWidget.setVerticalHeaderItem(0, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.files_tableWidget.setVerticalHeaderItem(1, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.files_tableWidget.setVerticalHeaderItem(2, __qtablewidgetitem5)
        self.files_tableWidget.setObjectName(u"files_tableWidget")
        sizePolicy6 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.files_tableWidget.sizePolicy().hasHeightForWidth())
        self.files_tableWidget.setSizePolicy(sizePolicy6)
        font1 = QFont()
        font1.setBold(False)
        font1.setItalic(False)
        font1.setWeight(50)
        self.files_tableWidget.setFont(font1)
        self.files_tableWidget.setFocusPolicy(Qt.StrongFocus)
        self.files_tableWidget.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.files_tableWidget.setAutoFillBackground(False)
        self.files_tableWidget.setFrameShape(QFrame.Box)
        self.files_tableWidget.setFrameShadow(QFrame.Plain)
        self.files_tableWidget.setMidLineWidth(0)
        self.files_tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.files_tableWidget.setDragEnabled(False)
        self.files_tableWidget.setDragDropMode(QAbstractItemView.NoDragDrop)
        self.files_tableWidget.setAlternatingRowColors(False)
        self.files_tableWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.files_tableWidget.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.files_tableWidget.setShowGrid(True)
        self.files_tableWidget.setGridStyle(Qt.SolidLine)
        self.files_tableWidget.setSortingEnabled(False)
        self.files_tableWidget.setCornerButtonEnabled(False)
        self.files_tableWidget.horizontalHeader().setVisible(False)
        self.files_tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.files_tableWidget.horizontalHeader().setMinimumSectionSize(50)
        self.files_tableWidget.horizontalHeader().setDefaultSectionSize(250)
        self.files_tableWidget.horizontalHeader().setHighlightSections(True)
        self.files_tableWidget.horizontalHeader().setProperty("showSortIndicator", False)
        self.files_tableWidget.horizontalHeader().setStretchLastSection(True)
        self.files_tableWidget.verticalHeader().setVisible(False)
        self.files_tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.files_tableWidget.verticalHeader().setHighlightSections(True)

        self.verticalLayout_3.addWidget(self.files_tableWidget)


        self.gridLayout_3.addWidget(self.groupBox_2, 1, 0, 1, 1)

        self.mainTabWidget.addTab(self.workflow_tab, "")
        self.chalf_tab = QWidget()
        self.chalf_tab.setObjectName(u"chalf_tab")
        sizePolicy3.setHeightForWidth(self.chalf_tab.sizePolicy().hasHeightForWidth())
        self.chalf_tab.setSizePolicy(sizePolicy3)
        self.chalf_tab.setMinimumSize(QSize(880, 0))
        self.verticalLayout_7 = QVBoxLayout(self.chalf_tab)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.scrollArea = QScrollArea(self.chalf_tab)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy7 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy7)
        self.scrollArea.setMinimumSize(QSize(845, 0))
        self.scrollArea.setFocusPolicy(Qt.StrongFocus)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 843, 1037))
        self.verticalLayout_11 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.run_chalf_checkBox = QCheckBox(self.scrollAreaWidgetContents)
        self.run_chalf_checkBox.setObjectName(u"run_chalf_checkBox")
        self.run_chalf_checkBox.setChecked(True)

        self.verticalLayout_10.addWidget(self.run_chalf_checkBox)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.groupBox_7 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_7.setObjectName(u"groupBox_7")
        sizePolicy4.setHeightForWidth(self.groupBox_7.sizePolicy().hasHeightForWidth())
        self.groupBox_7.setSizePolicy(sizePolicy4)
        self.gridLayout_9 = QGridLayout(self.groupBox_7)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.light_search_checkBox = QCheckBox(self.groupBox_7)
        self.light_search_checkBox.setObjectName(u"light_search_checkBox")
        self.light_search_checkBox.setChecked(True)

        self.gridLayout_9.addWidget(self.light_search_checkBox, 0, 0, 1, 1)

        self.label_11 = QLabel(self.groupBox_7)
        self.label_11.setObjectName(u"label_11")
        sizePolicy1.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy1)
        self.label_11.setWordWrap(True)

        self.gridLayout_9.addWidget(self.label_11, 1, 0, 1, 1)

        self.groupBox_8 = QGroupBox(self.groupBox_7)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_8)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.aa_y_checkBox = QCheckBox(self.groupBox_8)
        self.aa_y_checkBox.setObjectName(u"aa_y_checkBox")
        self.aa_y_checkBox.setChecked(True)

        self.gridLayout_7.addWidget(self.aa_y_checkBox, 0, 0, 1, 1)

        self.aa_q_checkBox = QCheckBox(self.groupBox_8)
        self.aa_q_checkBox.setObjectName(u"aa_q_checkBox")

        self.gridLayout_7.addWidget(self.aa_q_checkBox, 2, 0, 1, 1)

        self.aa_r_checkBox = QCheckBox(self.groupBox_8)
        self.aa_r_checkBox.setObjectName(u"aa_r_checkBox")

        self.gridLayout_7.addWidget(self.aa_r_checkBox, 1, 1, 1, 1)

        self.aa_k_checkBox = QCheckBox(self.groupBox_8)
        self.aa_k_checkBox.setObjectName(u"aa_k_checkBox")

        self.gridLayout_7.addWidget(self.aa_k_checkBox, 1, 0, 1, 1)

        self.aa_d_checkBox = QCheckBox(self.groupBox_8)
        self.aa_d_checkBox.setObjectName(u"aa_d_checkBox")

        self.gridLayout_7.addWidget(self.aa_d_checkBox, 1, 2, 1, 1)

        self.aa_e_checkBox = QCheckBox(self.groupBox_8)
        self.aa_e_checkBox.setObjectName(u"aa_e_checkBox")

        self.gridLayout_7.addWidget(self.aa_e_checkBox, 1, 3, 1, 1)

        self.aa_w_checkBox = QCheckBox(self.groupBox_8)
        self.aa_w_checkBox.setObjectName(u"aa_w_checkBox")

        self.gridLayout_7.addWidget(self.aa_w_checkBox, 0, 4, 1, 1)

        self.aa_n_checkBox = QCheckBox(self.groupBox_8)
        self.aa_n_checkBox.setObjectName(u"aa_n_checkBox")

        self.gridLayout_7.addWidget(self.aa_n_checkBox, 1, 4, 1, 1)

        self.aa_s_checkBox = QCheckBox(self.groupBox_8)
        self.aa_s_checkBox.setObjectName(u"aa_s_checkBox")

        self.gridLayout_7.addWidget(self.aa_s_checkBox, 2, 1, 1, 1)

        self.aa_t_checkBox = QCheckBox(self.groupBox_8)
        self.aa_t_checkBox.setObjectName(u"aa_t_checkBox")

        self.gridLayout_7.addWidget(self.aa_t_checkBox, 2, 2, 1, 1)

        self.aa_p_checkBox = QCheckBox(self.groupBox_8)
        self.aa_p_checkBox.setObjectName(u"aa_p_checkBox")

        self.gridLayout_7.addWidget(self.aa_p_checkBox, 2, 3, 1, 1)

        self.aa_f_checkBox = QCheckBox(self.groupBox_8)
        self.aa_f_checkBox.setObjectName(u"aa_f_checkBox")

        self.gridLayout_7.addWidget(self.aa_f_checkBox, 2, 4, 1, 1)

        self.aa_g_checkBox = QCheckBox(self.groupBox_8)
        self.aa_g_checkBox.setObjectName(u"aa_g_checkBox")

        self.gridLayout_7.addWidget(self.aa_g_checkBox, 3, 0, 1, 1)

        self.aa_a_checkBox = QCheckBox(self.groupBox_8)
        self.aa_a_checkBox.setObjectName(u"aa_a_checkBox")

        self.gridLayout_7.addWidget(self.aa_a_checkBox, 3, 1, 1, 1)

        self.aa_v_checkBox = QCheckBox(self.groupBox_8)
        self.aa_v_checkBox.setObjectName(u"aa_v_checkBox")

        self.gridLayout_7.addWidget(self.aa_v_checkBox, 3, 2, 1, 1)

        self.aa_L_checkBox = QCheckBox(self.groupBox_8)
        self.aa_L_checkBox.setObjectName(u"aa_L_checkBox")

        self.gridLayout_7.addWidget(self.aa_L_checkBox, 3, 3, 1, 1)

        self.aa_i_checkBox = QCheckBox(self.groupBox_8)
        self.aa_i_checkBox.setObjectName(u"aa_i_checkBox")

        self.gridLayout_7.addWidget(self.aa_i_checkBox, 3, 4, 1, 1)

        self.aa_h_checkBox = QCheckBox(self.groupBox_8)
        self.aa_h_checkBox.setObjectName(u"aa_h_checkBox")
        self.aa_h_checkBox.setChecked(True)

        self.gridLayout_7.addWidget(self.aa_h_checkBox, 0, 1, 1, 1)

        self.aa_c_checkBox = QCheckBox(self.groupBox_8)
        self.aa_c_checkBox.setObjectName(u"aa_c_checkBox")
        self.aa_c_checkBox.setChecked(True)

        self.gridLayout_7.addWidget(self.aa_c_checkBox, 0, 3, 1, 1)

        self.aa_m_checkBox = QCheckBox(self.groupBox_8)
        self.aa_m_checkBox.setObjectName(u"aa_m_checkBox")
        self.aa_m_checkBox.setChecked(True)

        self.gridLayout_7.addWidget(self.aa_m_checkBox, 0, 2, 1, 1)


        self.verticalLayout_6.addLayout(self.gridLayout_7)


        self.gridLayout_9.addWidget(self.groupBox_8, 3, 0, 1, 1)


        self.horizontalLayout_15.addWidget(self.groupBox_7)

        self.groupBox_5 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_5.setObjectName(u"groupBox_5")
        sizePolicy1.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy1)
        self.gridLayout_10 = QGridLayout(self.groupBox_5)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_14 = QLabel(self.groupBox_5)
        self.label_14.setObjectName(u"label_14")
        sizePolicy4.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy4)
        self.label_14.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_13.addWidget(self.label_14)

        self.chalf_min_doubleSpinBox = QDoubleSpinBox(self.groupBox_5)
        self.chalf_min_doubleSpinBox.setObjectName(u"chalf_min_doubleSpinBox")
        self.chalf_min_doubleSpinBox.setFocusPolicy(Qt.StrongFocus)
        self.chalf_min_doubleSpinBox.setSingleStep(0.010000000000000)

        self.horizontalLayout_13.addWidget(self.chalf_min_doubleSpinBox)


        self.verticalLayout_5.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_12 = QLabel(self.groupBox_5)
        self.label_12.setObjectName(u"label_12")
        sizePolicy4.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy4)
        self.label_12.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_12.addWidget(self.label_12)

        self.chalf_max_doubleSpinBox = QDoubleSpinBox(self.groupBox_5)
        self.chalf_max_doubleSpinBox.setObjectName(u"chalf_max_doubleSpinBox")
        self.chalf_max_doubleSpinBox.setFocusPolicy(Qt.StrongFocus)
        self.chalf_max_doubleSpinBox.setSingleStep(0.010000000000000)
        self.chalf_max_doubleSpinBox.setValue(3.480000000000000)

        self.horizontalLayout_12.addWidget(self.chalf_max_doubleSpinBox)


        self.verticalLayout_5.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_13 = QLabel(self.groupBox_5)
        self.label_13.setObjectName(u"label_13")
        sizePolicy4.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy4)
        self.label_13.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_11.addWidget(self.label_13)

        self.rsq_doubleSpinBox = QDoubleSpinBox(self.groupBox_5)
        self.rsq_doubleSpinBox.setObjectName(u"rsq_doubleSpinBox")
        self.rsq_doubleSpinBox.setFocusPolicy(Qt.StrongFocus)
        self.rsq_doubleSpinBox.setMaximum(0.990000000000000)
        self.rsq_doubleSpinBox.setSingleStep(0.010000000000000)
        self.rsq_doubleSpinBox.setValue(0.800000000000000)

        self.horizontalLayout_11.addWidget(self.rsq_doubleSpinBox)


        self.verticalLayout_5.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.CI_filter_checkBox = QCheckBox(self.groupBox_5)
        self.CI_filter_checkBox.setObjectName(u"CI_filter_checkBox")
        sizePolicy2.setHeightForWidth(self.CI_filter_checkBox.sizePolicy().hasHeightForWidth())
        self.CI_filter_checkBox.setSizePolicy(sizePolicy2)
        self.CI_filter_checkBox.setMinimumSize(QSize(200, 0))
        self.CI_filter_checkBox.setMaximumSize(QSize(200, 16777215))
        self.CI_filter_checkBox.setBaseSize(QSize(200, 0))

        self.horizontalLayout_10.addWidget(self.CI_filter_checkBox)

        self.CI_doubleSpinBox = QDoubleSpinBox(self.groupBox_5)
        self.CI_doubleSpinBox.setObjectName(u"CI_doubleSpinBox")
        self.CI_doubleSpinBox.setFocusPolicy(Qt.StrongFocus)
        self.CI_doubleSpinBox.setSingleStep(0.010000000000000)
        self.CI_doubleSpinBox.setValue(0.350000000000000)

        self.horizontalLayout_10.addWidget(self.CI_doubleSpinBox)


        self.verticalLayout_5.addLayout(self.horizontalLayout_10)

        self.label_15 = QLabel(self.groupBox_5)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setWordWrap(True)

        self.verticalLayout_5.addWidget(self.label_15)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_16 = QLabel(self.groupBox_5)
        self.label_16.setObjectName(u"label_16")
        sizePolicy4.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy4)
        self.label_16.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_9.addWidget(self.label_16)

        self.fit_opt_comboBox = QComboBox(self.groupBox_5)
        self.fit_opt_comboBox.addItem("")
        self.fit_opt_comboBox.addItem("")
        self.fit_opt_comboBox.setObjectName(u"fit_opt_comboBox")
        self.fit_opt_comboBox.setFocusPolicy(Qt.StrongFocus)

        self.horizontalLayout_9.addWidget(self.fit_opt_comboBox)


        self.verticalLayout_5.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.sig_only_checkBox = QCheckBox(self.groupBox_5)
        self.sig_only_checkBox.setObjectName(u"sig_only_checkBox")

        self.horizontalLayout_8.addWidget(self.sig_only_checkBox)


        self.verticalLayout_5.addLayout(self.horizontalLayout_8)


        self.gridLayout_10.addLayout(self.verticalLayout_5, 1, 0, 1, 1)


        self.horizontalLayout_15.addWidget(self.groupBox_5)


        self.verticalLayout_10.addLayout(self.horizontalLayout_15)


        self.verticalLayout_11.addLayout(self.verticalLayout_10)

        self.groupBox_3 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_3.setObjectName(u"groupBox_3")
        sizePolicy1.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy1)
        self.groupBox_3.setMinimumSize(QSize(200, 75))
        self.groupBox_3.setBaseSize(QSize(100, 200))
        self.verticalLayout_21 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(6)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(4)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setSizeConstraint(QLayout.SetMaximumSize)
        self.label_9 = QLabel(self.groupBox_3)
        self.label_9.setObjectName(u"label_9")
        sizePolicy4.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy4)
        self.label_9.setMinimumSize(QSize(150, 0))
        self.label_9.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_6.addWidget(self.label_9)

        self.min_pts_spinBox = QSpinBox(self.groupBox_3)
        self.min_pts_spinBox.setObjectName(u"min_pts_spinBox")
        sizePolicy3.setHeightForWidth(self.min_pts_spinBox.sizePolicy().hasHeightForWidth())
        self.min_pts_spinBox.setSizePolicy(sizePolicy3)
        self.min_pts_spinBox.setFocusPolicy(Qt.StrongFocus)
        self.min_pts_spinBox.setMinimum(2)
        self.min_pts_spinBox.setMaximum(1000)
        self.min_pts_spinBox.setValue(4)

        self.horizontalLayout_6.addWidget(self.min_pts_spinBox)


        self.horizontalLayout_5.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setSpacing(4)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setSizeConstraint(QLayout.SetMaximumSize)
        self.label_10 = QLabel(self.groupBox_3)
        self.label_10.setObjectName(u"label_10")
        sizePolicy8 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy8)
        self.label_10.setMinimumSize(QSize(130, 0))
        self.label_10.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_7.addWidget(self.label_10)

        self.out_cut_spinBox = QSpinBox(self.groupBox_3)
        self.out_cut_spinBox.setObjectName(u"out_cut_spinBox")
        sizePolicy3.setHeightForWidth(self.out_cut_spinBox.sizePolicy().hasHeightForWidth())
        self.out_cut_spinBox.setSizePolicy(sizePolicy3)
        self.out_cut_spinBox.setFocusPolicy(Qt.StrongFocus)
        self.out_cut_spinBox.setMinimum(0)
        self.out_cut_spinBox.setMaximum(1000)
        self.out_cut_spinBox.setValue(2)

        self.horizontalLayout_7.addWidget(self.out_cut_spinBox)


        self.horizontalLayout_5.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_37 = QHBoxLayout()
        self.horizontalLayout_37.setObjectName(u"horizontalLayout_37")
        self.horizontalLayout_37.setContentsMargins(-1, -1, 0, -1)
        self.label_34 = QLabel(self.groupBox_3)
        self.label_34.setObjectName(u"label_34")
        sizePolicy5.setHeightForWidth(self.label_34.sizePolicy().hasHeightForWidth())
        self.label_34.setSizePolicy(sizePolicy5)
        self.label_34.setMinimumSize(QSize(110, 0))

        self.horizontalLayout_37.addWidget(self.label_34)

        self.chalf_zero_criteria_comboBox = QComboBox(self.groupBox_3)
        self.chalf_zero_criteria_comboBox.addItem("")
        self.chalf_zero_criteria_comboBox.addItem("")
        self.chalf_zero_criteria_comboBox.addItem("")
        self.chalf_zero_criteria_comboBox.setObjectName(u"chalf_zero_criteria_comboBox")
        sizePolicy9 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.chalf_zero_criteria_comboBox.sizePolicy().hasHeightForWidth())
        self.chalf_zero_criteria_comboBox.setSizePolicy(sizePolicy9)

        self.horizontalLayout_37.addWidget(self.chalf_zero_criteria_comboBox)


        self.horizontalLayout_5.addLayout(self.horizontalLayout_37)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.trimming_checkBox = QCheckBox(self.groupBox_3)
        self.trimming_checkBox.setObjectName(u"trimming_checkBox")
        sizePolicy2.setHeightForWidth(self.trimming_checkBox.sizePolicy().hasHeightForWidth())
        self.trimming_checkBox.setSizePolicy(sizePolicy2)
        self.trimming_checkBox.setChecked(True)

        self.horizontalLayout_14.addWidget(self.trimming_checkBox)


        self.horizontalLayout_5.addLayout(self.horizontalLayout_14)


        self.verticalLayout_21.addLayout(self.horizontalLayout_5)

        self.label_35 = QLabel(self.groupBox_3)
        self.label_35.setObjectName(u"label_35")
        self.label_35.setWordWrap(True)

        self.verticalLayout_21.addWidget(self.label_35)


        self.verticalLayout_11.addWidget(self.groupBox_3)

        self.groupBox_4 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_4.setObjectName(u"groupBox_4")
        sizePolicy1.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy1)
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_25 = QHBoxLayout()
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.horizontalLayout_25.setContentsMargins(-1, 0, -1, -1)
        self.graph_cruves_checkBox = QCheckBox(self.groupBox_4)
        self.graph_cruves_checkBox.setObjectName(u"graph_cruves_checkBox")
        sizePolicy2.setHeightForWidth(self.graph_cruves_checkBox.sizePolicy().hasHeightForWidth())
        self.graph_cruves_checkBox.setSizePolicy(sizePolicy2)

        self.horizontalLayout_25.addWidget(self.graph_cruves_checkBox)

        self.label_28 = QLabel(self.groupBox_4)
        self.label_28.setObjectName(u"label_28")
        sizePolicy4.setHeightForWidth(self.label_28.sizePolicy().hasHeightForWidth())
        self.label_28.setSizePolicy(sizePolicy4)

        self.horizontalLayout_25.addWidget(self.label_28, 0, Qt.AlignRight)

        self.graphing_filetype_comboBox = QComboBox(self.groupBox_4)
        self.graphing_filetype_comboBox.addItem("")
        self.graphing_filetype_comboBox.addItem("")
        self.graphing_filetype_comboBox.addItem("")
        self.graphing_filetype_comboBox.setObjectName(u"graphing_filetype_comboBox")
        sizePolicy9.setHeightForWidth(self.graphing_filetype_comboBox.sizePolicy().hasHeightForWidth())
        self.graphing_filetype_comboBox.setSizePolicy(sizePolicy9)

        self.horizontalLayout_25.addWidget(self.graphing_filetype_comboBox)

        self.horizontalLayout_25.setStretch(0, 1)
        self.horizontalLayout_25.setStretch(1, 1)
        self.horizontalLayout_25.setStretch(2, 4)

        self.verticalLayout_4.addLayout(self.horizontalLayout_25)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.label_17 = QLabel(self.groupBox_4)
        self.label_17.setObjectName(u"label_17")
        sizePolicy4.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy4)

        self.horizontalLayout_17.addWidget(self.label_17)

        self.graph_chalf_min_doubleSpinBox = QDoubleSpinBox(self.groupBox_4)
        self.graph_chalf_min_doubleSpinBox.setObjectName(u"graph_chalf_min_doubleSpinBox")
        sizePolicy3.setHeightForWidth(self.graph_chalf_min_doubleSpinBox.sizePolicy().hasHeightForWidth())
        self.graph_chalf_min_doubleSpinBox.setSizePolicy(sizePolicy3)
        self.graph_chalf_min_doubleSpinBox.setMinimumSize(QSize(250, 0))
        self.graph_chalf_min_doubleSpinBox.setFocusPolicy(Qt.StrongFocus)
        self.graph_chalf_min_doubleSpinBox.setSingleStep(0.010000000000000)

        self.horizontalLayout_17.addWidget(self.graph_chalf_min_doubleSpinBox)


        self.gridLayout_4.addLayout(self.horizontalLayout_17, 0, 1, 1, 1)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.label_19 = QLabel(self.groupBox_4)
        self.label_19.setObjectName(u"label_19")
        sizePolicy4.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy4)
        self.label_19.setMinimumSize(QSize(65, 0))

        self.horizontalLayout_19.addWidget(self.label_19)

        self.graph_rsq_doubleSpinBox = QDoubleSpinBox(self.groupBox_4)
        self.graph_rsq_doubleSpinBox.setObjectName(u"graph_rsq_doubleSpinBox")
        sizePolicy3.setHeightForWidth(self.graph_rsq_doubleSpinBox.sizePolicy().hasHeightForWidth())
        self.graph_rsq_doubleSpinBox.setSizePolicy(sizePolicy3)
        self.graph_rsq_doubleSpinBox.setMinimumSize(QSize(250, 0))
        self.graph_rsq_doubleSpinBox.setFocusPolicy(Qt.StrongFocus)
        self.graph_rsq_doubleSpinBox.setMaximum(0.990000000000000)
        self.graph_rsq_doubleSpinBox.setSingleStep(0.010000000000000)
        self.graph_rsq_doubleSpinBox.setValue(0.800000000000000)

        self.horizontalLayout_19.addWidget(self.graph_rsq_doubleSpinBox)


        self.gridLayout_4.addLayout(self.horizontalLayout_19, 1, 1, 1, 1)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.label_18 = QLabel(self.groupBox_4)
        self.label_18.setObjectName(u"label_18")

        self.horizontalLayout_20.addWidget(self.label_18, 0, Qt.AlignRight)

        self.graph_chalf_max_doubleSpinBox = QDoubleSpinBox(self.groupBox_4)
        self.graph_chalf_max_doubleSpinBox.setObjectName(u"graph_chalf_max_doubleSpinBox")
        sizePolicy3.setHeightForWidth(self.graph_chalf_max_doubleSpinBox.sizePolicy().hasHeightForWidth())
        self.graph_chalf_max_doubleSpinBox.setSizePolicy(sizePolicy3)
        self.graph_chalf_max_doubleSpinBox.setMinimumSize(QSize(250, 0))
        self.graph_chalf_max_doubleSpinBox.setFocusPolicy(Qt.StrongFocus)
        self.graph_chalf_max_doubleSpinBox.setSingleStep(0.010000000000000)
        self.graph_chalf_max_doubleSpinBox.setValue(3.480000000000000)

        self.horizontalLayout_20.addWidget(self.graph_chalf_max_doubleSpinBox)


        self.gridLayout_4.addLayout(self.horizontalLayout_20, 0, 4, 1, 1)

        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.graph_ci_checkBox = QCheckBox(self.groupBox_4)
        self.graph_ci_checkBox.setObjectName(u"graph_ci_checkBox")

        self.horizontalLayout_21.addWidget(self.graph_ci_checkBox, 0, Qt.AlignRight)

        self.graph_ci_doubleSpinBox = QDoubleSpinBox(self.groupBox_4)
        self.graph_ci_doubleSpinBox.setObjectName(u"graph_ci_doubleSpinBox")
        sizePolicy3.setHeightForWidth(self.graph_ci_doubleSpinBox.sizePolicy().hasHeightForWidth())
        self.graph_ci_doubleSpinBox.setSizePolicy(sizePolicy3)
        self.graph_ci_doubleSpinBox.setMinimumSize(QSize(250, 0))
        self.graph_ci_doubleSpinBox.setFocusPolicy(Qt.StrongFocus)
        self.graph_ci_doubleSpinBox.setSingleStep(0.010000000000000)
        self.graph_ci_doubleSpinBox.setValue(0.350000000000000)

        self.horizontalLayout_21.addWidget(self.graph_ci_doubleSpinBox)


        self.gridLayout_4.addLayout(self.horizontalLayout_21, 1, 4, 1, 1)


        self.verticalLayout_4.addLayout(self.gridLayout_4)


        self.verticalLayout_11.addWidget(self.groupBox_4)

        self.groupBox_6 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.verticalLayout_8 = QVBoxLayout(self.groupBox_6)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_20 = QLabel(self.groupBox_6)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setWordWrap(True)

        self.verticalLayout_8.addWidget(self.label_20)

        self.groupBox_9 = QGroupBox(self.groupBox_6)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.verticalLayout_9 = QVBoxLayout(self.groupBox_9)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.sg_checkBox = QCheckBox(self.groupBox_9)
        self.sg_checkBox.setObjectName(u"sg_checkBox")

        self.verticalLayout_9.addWidget(self.sg_checkBox)

        self.label_21 = QLabel(self.groupBox_9)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setWordWrap(True)

        self.verticalLayout_9.addWidget(self.label_21)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalLayout_18.setContentsMargins(-1, 0, -1, -1)
        self.label_22 = QLabel(self.groupBox_9)
        self.label_22.setObjectName(u"label_22")
        sizePolicy4.setHeightForWidth(self.label_22.sizePolicy().hasHeightForWidth())
        self.label_22.setSizePolicy(sizePolicy4)
        self.label_22.setMinimumSize(QSize(325, 0))

        self.horizontalLayout_18.addWidget(self.label_22)

        self.sg_window_spinBox = QSpinBox(self.groupBox_9)
        self.sg_window_spinBox.setObjectName(u"sg_window_spinBox")
        self.sg_window_spinBox.setFocusPolicy(Qt.StrongFocus)
        self.sg_window_spinBox.setMinimum(2)
        self.sg_window_spinBox.setValue(5)
        self.sg_window_spinBox.setDisplayIntegerBase(10)

        self.horizontalLayout_18.addWidget(self.sg_window_spinBox)


        self.verticalLayout_9.addLayout(self.horizontalLayout_18)

        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalLayout_22.setContentsMargins(-1, 0, -1, -1)
        self.label_23 = QLabel(self.groupBox_9)
        self.label_23.setObjectName(u"label_23")
        sizePolicy4.setHeightForWidth(self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy4)
        self.label_23.setMinimumSize(QSize(325, 0))

        self.horizontalLayout_22.addWidget(self.label_23)

        self.sg_order_spinBox = QSpinBox(self.groupBox_9)
        self.sg_order_spinBox.setObjectName(u"sg_order_spinBox")
        self.sg_order_spinBox.setFocusPolicy(Qt.StrongFocus)
        self.sg_order_spinBox.setMinimum(1)
        self.sg_order_spinBox.setValue(2)

        self.horizontalLayout_22.addWidget(self.sg_order_spinBox)


        self.verticalLayout_9.addLayout(self.horizontalLayout_22)


        self.verticalLayout_8.addWidget(self.groupBox_9)

        self.groupBox_10 = QGroupBox(self.groupBox_6)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.verticalLayout_12 = QVBoxLayout(self.groupBox_10)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.windowed_fitting_checkBox = QCheckBox(self.groupBox_10)
        self.windowed_fitting_checkBox.setObjectName(u"windowed_fitting_checkBox")

        self.verticalLayout_12.addWidget(self.windowed_fitting_checkBox)

        self.label_24 = QLabel(self.groupBox_10)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setWordWrap(True)

        self.verticalLayout_12.addWidget(self.label_24)

        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.horizontalLayout_23.setContentsMargins(-1, 0, -1, -1)
        self.label_25 = QLabel(self.groupBox_10)
        self.label_25.setObjectName(u"label_25")

        self.horizontalLayout_23.addWidget(self.label_25)

        self.wf_window_spinBox = QSpinBox(self.groupBox_10)
        self.wf_window_spinBox.setObjectName(u"wf_window_spinBox")
        sizePolicy3.setHeightForWidth(self.wf_window_spinBox.sizePolicy().hasHeightForWidth())
        self.wf_window_spinBox.setSizePolicy(sizePolicy3)
        self.wf_window_spinBox.setFocusPolicy(Qt.StrongFocus)
        self.wf_window_spinBox.setMinimum(3)
        self.wf_window_spinBox.setValue(6)

        self.horizontalLayout_23.addWidget(self.wf_window_spinBox)


        self.verticalLayout_12.addLayout(self.horizontalLayout_23)


        self.verticalLayout_8.addWidget(self.groupBox_10)

        self.groupBox_11 = QGroupBox(self.groupBox_6)
        self.groupBox_11.setObjectName(u"groupBox_11")
        self.verticalLayout_13 = QVBoxLayout(self.groupBox_11)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.checkBox_3 = QCheckBox(self.groupBox_11)
        self.checkBox_3.setObjectName(u"checkBox_3")

        self.verticalLayout_13.addWidget(self.checkBox_3)

        self.label_26 = QLabel(self.groupBox_11)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setWordWrap(True)

        self.verticalLayout_13.addWidget(self.label_26)


        self.verticalLayout_8.addWidget(self.groupBox_11)


        self.verticalLayout_11.addWidget(self.groupBox_6)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_7.addWidget(self.scrollArea)

        self.mainTabWidget.addTab(self.chalf_tab, "")
        self.qc_tab = QWidget()
        self.qc_tab.setObjectName(u"qc_tab")
        sizePolicy1.setHeightForWidth(self.qc_tab.sizePolicy().hasHeightForWidth())
        self.qc_tab.setSizePolicy(sizePolicy1)
        self.qc_tab.setMinimumSize(QSize(0, 450))
        self.qc_tab.setMaximumSize(QSize(16777215, 300))
        self.verticalLayout_16 = QVBoxLayout(self.qc_tab)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.qc_checkBox = QCheckBox(self.qc_tab)
        self.qc_checkBox.setObjectName(u"qc_checkBox")
        self.qc_checkBox.setChecked(True)

        self.verticalLayout_16.addWidget(self.qc_checkBox)

        self.groupBox_12 = QGroupBox(self.qc_tab)
        self.groupBox_12.setObjectName(u"groupBox_12")
        sizePolicy1.setHeightForWidth(self.groupBox_12.sizePolicy().hasHeightForWidth())
        self.groupBox_12.setSizePolicy(sizePolicy1)
        self.verticalLayout_14 = QVBoxLayout(self.groupBox_12)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.qc_chalf_filters_pushButton = QPushButton(self.groupBox_12)
        self.qc_chalf_filters_pushButton.setObjectName(u"qc_chalf_filters_pushButton")
        sizePolicy2.setHeightForWidth(self.qc_chalf_filters_pushButton.sizePolicy().hasHeightForWidth())
        self.qc_chalf_filters_pushButton.setSizePolicy(sizePolicy2)
        self.qc_chalf_filters_pushButton.setMinimumSize(QSize(200, 0))

        self.verticalLayout_14.addWidget(self.qc_chalf_filters_pushButton)

        self.horizontalLayout_26 = QHBoxLayout()
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.groupBox_13 = QGroupBox(self.groupBox_12)
        self.groupBox_13.setObjectName(u"groupBox_13")
        sizePolicy4.setHeightForWidth(self.groupBox_13.sizePolicy().hasHeightForWidth())
        self.groupBox_13.setSizePolicy(sizePolicy4)
        self.gridLayout_8 = QGridLayout(self.groupBox_13)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.qc_c_checkBox = QCheckBox(self.groupBox_13)
        self.qc_c_checkBox.setObjectName(u"qc_c_checkBox")

        self.gridLayout_8.addWidget(self.qc_c_checkBox, 0, 3, 1, 1)

        self.qc_t_checkBox = QCheckBox(self.groupBox_13)
        self.qc_t_checkBox.setObjectName(u"qc_t_checkBox")

        self.gridLayout_8.addWidget(self.qc_t_checkBox, 2, 2, 1, 1)

        self.qc_h_checkBox = QCheckBox(self.groupBox_13)
        self.qc_h_checkBox.setObjectName(u"qc_h_checkBox")

        self.gridLayout_8.addWidget(self.qc_h_checkBox, 0, 1, 1, 1)

        self.qc_f_checkBox = QCheckBox(self.groupBox_13)
        self.qc_f_checkBox.setObjectName(u"qc_f_checkBox")

        self.gridLayout_8.addWidget(self.qc_f_checkBox, 2, 4, 1, 1)

        self.qc_q_checkBox = QCheckBox(self.groupBox_13)
        self.qc_q_checkBox.setObjectName(u"qc_q_checkBox")

        self.gridLayout_8.addWidget(self.qc_q_checkBox, 2, 0, 1, 1)

        self.qc_d_checkBox = QCheckBox(self.groupBox_13)
        self.qc_d_checkBox.setObjectName(u"qc_d_checkBox")

        self.gridLayout_8.addWidget(self.qc_d_checkBox, 1, 2, 1, 1)

        self.qc_n_checkBox = QCheckBox(self.groupBox_13)
        self.qc_n_checkBox.setObjectName(u"qc_n_checkBox")

        self.gridLayout_8.addWidget(self.qc_n_checkBox, 1, 4, 1, 1)

        self.qc_k_checkBox = QCheckBox(self.groupBox_13)
        self.qc_k_checkBox.setObjectName(u"qc_k_checkBox")

        self.gridLayout_8.addWidget(self.qc_k_checkBox, 1, 0, 1, 1)

        self.qc_p_checkBox = QCheckBox(self.groupBox_13)
        self.qc_p_checkBox.setObjectName(u"qc_p_checkBox")

        self.gridLayout_8.addWidget(self.qc_p_checkBox, 2, 3, 1, 1)

        self.qc_w_checkBox = QCheckBox(self.groupBox_13)
        self.qc_w_checkBox.setObjectName(u"qc_w_checkBox")

        self.gridLayout_8.addWidget(self.qc_w_checkBox, 0, 4, 1, 1)

        self.qc_e_checkBox = QCheckBox(self.groupBox_13)
        self.qc_e_checkBox.setObjectName(u"qc_e_checkBox")

        self.gridLayout_8.addWidget(self.qc_e_checkBox, 1, 3, 1, 1)

        self.qc_r_checkBox = QCheckBox(self.groupBox_13)
        self.qc_r_checkBox.setObjectName(u"qc_r_checkBox")

        self.gridLayout_8.addWidget(self.qc_r_checkBox, 1, 1, 1, 1)

        self.qc_y_checkBox = QCheckBox(self.groupBox_13)
        self.qc_y_checkBox.setObjectName(u"qc_y_checkBox")

        self.gridLayout_8.addWidget(self.qc_y_checkBox, 0, 0, 1, 1)

        self.qc_m_checkBox = QCheckBox(self.groupBox_13)
        self.qc_m_checkBox.setObjectName(u"qc_m_checkBox")

        self.gridLayout_8.addWidget(self.qc_m_checkBox, 0, 2, 1, 1)

        self.qc_s_checkBox = QCheckBox(self.groupBox_13)
        self.qc_s_checkBox.setObjectName(u"qc_s_checkBox")

        self.gridLayout_8.addWidget(self.qc_s_checkBox, 2, 1, 1, 1)

        self.qc_g_checkBox = QCheckBox(self.groupBox_13)
        self.qc_g_checkBox.setObjectName(u"qc_g_checkBox")

        self.gridLayout_8.addWidget(self.qc_g_checkBox, 3, 0, 1, 1)

        self.qc_a_checkBox = QCheckBox(self.groupBox_13)
        self.qc_a_checkBox.setObjectName(u"qc_a_checkBox")

        self.gridLayout_8.addWidget(self.qc_a_checkBox, 3, 1, 1, 1)

        self.qc_v_checkBox = QCheckBox(self.groupBox_13)
        self.qc_v_checkBox.setObjectName(u"qc_v_checkBox")

        self.gridLayout_8.addWidget(self.qc_v_checkBox, 3, 2, 1, 1)

        self.qc_l_checkBox = QCheckBox(self.groupBox_13)
        self.qc_l_checkBox.setObjectName(u"qc_l_checkBox")

        self.gridLayout_8.addWidget(self.qc_l_checkBox, 3, 3, 1, 1)

        self.qc_i_checkBox = QCheckBox(self.groupBox_13)
        self.qc_i_checkBox.setObjectName(u"qc_i_checkBox")

        self.gridLayout_8.addWidget(self.qc_i_checkBox, 3, 4, 1, 1)


        self.horizontalLayout_26.addWidget(self.groupBox_13)

        self.groupBox_14 = QGroupBox(self.groupBox_12)
        self.groupBox_14.setObjectName(u"groupBox_14")
        self.verticalLayout_15 = QVBoxLayout(self.groupBox_14)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.horizontalLayout_30 = QHBoxLayout()
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.label_29 = QLabel(self.groupBox_14)
        self.label_29.setObjectName(u"label_29")
        sizePolicy4.setHeightForWidth(self.label_29.sizePolicy().hasHeightForWidth())
        self.label_29.setSizePolicy(sizePolicy4)
        self.label_29.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_30.addWidget(self.label_29)

        self.qc_chalf_min_doubleSpinBox = QDoubleSpinBox(self.groupBox_14)
        self.qc_chalf_min_doubleSpinBox.setObjectName(u"qc_chalf_min_doubleSpinBox")
        self.qc_chalf_min_doubleSpinBox.setSingleStep(0.010000000000000)

        self.horizontalLayout_30.addWidget(self.qc_chalf_min_doubleSpinBox)


        self.verticalLayout_15.addLayout(self.horizontalLayout_30)

        self.horizontalLayout_27 = QHBoxLayout()
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.label_30 = QLabel(self.groupBox_14)
        self.label_30.setObjectName(u"label_30")
        sizePolicy4.setHeightForWidth(self.label_30.sizePolicy().hasHeightForWidth())
        self.label_30.setSizePolicy(sizePolicy4)
        self.label_30.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_27.addWidget(self.label_30)

        self.qc_chalf_max_doubleSpinBox = QDoubleSpinBox(self.groupBox_14)
        self.qc_chalf_max_doubleSpinBox.setObjectName(u"qc_chalf_max_doubleSpinBox")
        self.qc_chalf_max_doubleSpinBox.setSingleStep(0.010000000000000)
        self.qc_chalf_max_doubleSpinBox.setValue(3.480000000000000)

        self.horizontalLayout_27.addWidget(self.qc_chalf_max_doubleSpinBox)


        self.verticalLayout_15.addLayout(self.horizontalLayout_27)

        self.horizontalLayout_29 = QHBoxLayout()
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.label_31 = QLabel(self.groupBox_14)
        self.label_31.setObjectName(u"label_31")
        sizePolicy4.setHeightForWidth(self.label_31.sizePolicy().hasHeightForWidth())
        self.label_31.setSizePolicy(sizePolicy4)
        self.label_31.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_29.addWidget(self.label_31)

        self.qc_rsq_doubleSpinBox = QDoubleSpinBox(self.groupBox_14)
        self.qc_rsq_doubleSpinBox.setObjectName(u"qc_rsq_doubleSpinBox")
        self.qc_rsq_doubleSpinBox.setMaximum(0.990000000000000)
        self.qc_rsq_doubleSpinBox.setSingleStep(0.010000000000000)
        self.qc_rsq_doubleSpinBox.setValue(0.800000000000000)

        self.horizontalLayout_29.addWidget(self.qc_rsq_doubleSpinBox)


        self.verticalLayout_15.addLayout(self.horizontalLayout_29)

        self.horizontalLayout_32 = QHBoxLayout()
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.qc_ci_checkBox = QCheckBox(self.groupBox_14)
        self.qc_ci_checkBox.setObjectName(u"qc_ci_checkBox")
        sizePolicy2.setHeightForWidth(self.qc_ci_checkBox.sizePolicy().hasHeightForWidth())
        self.qc_ci_checkBox.setSizePolicy(sizePolicy2)
        self.qc_ci_checkBox.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_32.addWidget(self.qc_ci_checkBox)

        self.qc_ci_doubleSpinBox = QDoubleSpinBox(self.groupBox_14)
        self.qc_ci_doubleSpinBox.setObjectName(u"qc_ci_doubleSpinBox")
        self.qc_ci_doubleSpinBox.setSingleStep(0.010000000000000)
        self.qc_ci_doubleSpinBox.setValue(0.350000000000000)

        self.horizontalLayout_32.addWidget(self.qc_ci_doubleSpinBox)


        self.verticalLayout_15.addLayout(self.horizontalLayout_32)

        self.horizontalLayout_28 = QHBoxLayout()
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.label_32 = QLabel(self.groupBox_14)
        self.label_32.setObjectName(u"label_32")
        sizePolicy4.setHeightForWidth(self.label_32.sizePolicy().hasHeightForWidth())
        self.label_32.setSizePolicy(sizePolicy4)
        self.label_32.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_28.addWidget(self.label_32)

        self.qc_priority_comboBox = QComboBox(self.groupBox_14)
        self.qc_priority_comboBox.addItem("")
        self.qc_priority_comboBox.addItem("")
        self.qc_priority_comboBox.setObjectName(u"qc_priority_comboBox")

        self.horizontalLayout_28.addWidget(self.qc_priority_comboBox)


        self.verticalLayout_15.addLayout(self.horizontalLayout_28)


        self.horizontalLayout_26.addWidget(self.groupBox_14)

        self.horizontalLayout_26.setStretch(0, 1)
        self.horizontalLayout_26.setStretch(1, 3)

        self.verticalLayout_14.addLayout(self.horizontalLayout_26)


        self.verticalLayout_16.addWidget(self.groupBox_12)

        self.label_36 = QLabel(self.qc_tab)
        self.label_36.setObjectName(u"label_36")
        sizePolicy1.setHeightForWidth(self.label_36.sizePolicy().hasHeightForWidth())
        self.label_36.setSizePolicy(sizePolicy1)
        self.label_36.setMinimumSize(QSize(0, 100))
        self.label_36.setMaximumSize(QSize(16777215, 100))
        self.label_36.setFocusPolicy(Qt.StrongFocus)
        self.label_36.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.label_36.setWordWrap(True)

        self.verticalLayout_16.addWidget(self.label_36)

        self.mainTabWidget.addTab(self.qc_tab, "")
        self.visualization_tab = QWidget()
        self.visualization_tab.setObjectName(u"visualization_tab")
        self.horizontalLayout_31 = QHBoxLayout(self.visualization_tab)
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.horizontalLayout_33 = QHBoxLayout()
        self.horizontalLayout_33.setObjectName(u"horizontalLayout_33")
        self.horizontalLayout_33.setContentsMargins(-1, -1, 0, -1)
        self.groupBox_15 = QGroupBox(self.visualization_tab)
        self.groupBox_15.setObjectName(u"groupBox_15")
        self.verticalLayout_18 = QVBoxLayout(self.groupBox_15)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.scrollArea_2 = QScrollArea(self.groupBox_15)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 309, 1549))
        self.verticalLayout_19 = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.groupBox_17 = QGroupBox(self.scrollAreaWidgetContents_2)
        self.groupBox_17.setObjectName(u"groupBox_17")
        sizePolicy1.setHeightForWidth(self.groupBox_17.sizePolicy().hasHeightForWidth())
        self.groupBox_17.setSizePolicy(sizePolicy1)
        self.horizontalLayout_35 = QHBoxLayout(self.groupBox_17)
        self.horizontalLayout_35.setObjectName(u"horizontalLayout_35")
        self.qc_vis_generate_checkBox = QCheckBox(self.groupBox_17)
        self.qc_vis_generate_checkBox.setObjectName(u"qc_vis_generate_checkBox")
        self.qc_vis_generate_checkBox.setChecked(True)

        self.horizontalLayout_35.addWidget(self.qc_vis_generate_checkBox)

        self.qc_vis_open_checkBox = QCheckBox(self.groupBox_17)
        self.qc_vis_open_checkBox.setObjectName(u"qc_vis_open_checkBox")

        self.horizontalLayout_35.addWidget(self.qc_vis_open_checkBox)


        self.verticalLayout_19.addWidget(self.groupBox_17)

        self.groupBox_25 = QGroupBox(self.scrollAreaWidgetContents_2)
        self.groupBox_25.setObjectName(u"groupBox_25")
        sizePolicy1.setHeightForWidth(self.groupBox_25.sizePolicy().hasHeightForWidth())
        self.groupBox_25.setSizePolicy(sizePolicy1)
        self.verticalLayout_25 = QVBoxLayout(self.groupBox_25)
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.rm_checkBox = QCheckBox(self.groupBox_25)
        self.rm_checkBox.setObjectName(u"rm_checkBox")
        self.rm_checkBox.setChecked(True)

        self.verticalLayout_25.addWidget(self.rm_checkBox)

        self.horizontalLayout_46 = QHBoxLayout()
        self.horizontalLayout_46.setObjectName(u"horizontalLayout_46")
        self.label_46 = QLabel(self.groupBox_25)
        self.label_46.setObjectName(u"label_46")
        sizePolicy4.setHeightForWidth(self.label_46.sizePolicy().hasHeightForWidth())
        self.label_46.setSizePolicy(sizePolicy4)
        self.label_46.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_46.addWidget(self.label_46)

        self.rm_filetype_comboBox = QComboBox(self.groupBox_25)
        self.rm_filetype_comboBox.addItem("")
        self.rm_filetype_comboBox.addItem("")
        self.rm_filetype_comboBox.addItem("")
        self.rm_filetype_comboBox.setObjectName(u"rm_filetype_comboBox")

        self.horizontalLayout_46.addWidget(self.rm_filetype_comboBox)


        self.verticalLayout_25.addLayout(self.horizontalLayout_46)

        self.horizontalLayout_47 = QHBoxLayout()
        self.horizontalLayout_47.setObjectName(u"horizontalLayout_47")
        self.label_47 = QLabel(self.groupBox_25)
        self.label_47.setObjectName(u"label_47")
        sizePolicy4.setHeightForWidth(self.label_47.sizePolicy().hasHeightForWidth())
        self.label_47.setSizePolicy(sizePolicy4)
        self.label_47.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_47.addWidget(self.label_47)

        self.rm_chalf_low_doubleSpinBox = QDoubleSpinBox(self.groupBox_25)
        self.rm_chalf_low_doubleSpinBox.setObjectName(u"rm_chalf_low_doubleSpinBox")
        self.rm_chalf_low_doubleSpinBox.setSingleStep(0.010000000000000)

        self.horizontalLayout_47.addWidget(self.rm_chalf_low_doubleSpinBox)


        self.verticalLayout_25.addLayout(self.horizontalLayout_47)

        self.horizontalLayout_48 = QHBoxLayout()
        self.horizontalLayout_48.setObjectName(u"horizontalLayout_48")
        self.label_48 = QLabel(self.groupBox_25)
        self.label_48.setObjectName(u"label_48")
        sizePolicy4.setHeightForWidth(self.label_48.sizePolicy().hasHeightForWidth())
        self.label_48.setSizePolicy(sizePolicy4)
        self.label_48.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_48.addWidget(self.label_48)

        self.rm_chalf_high_doubleSpinBox = QDoubleSpinBox(self.groupBox_25)
        self.rm_chalf_high_doubleSpinBox.setObjectName(u"rm_chalf_high_doubleSpinBox")
        self.rm_chalf_high_doubleSpinBox.setSingleStep(0.010000000000000)
        self.rm_chalf_high_doubleSpinBox.setValue(3.480000000000000)

        self.horizontalLayout_48.addWidget(self.rm_chalf_high_doubleSpinBox)


        self.verticalLayout_25.addLayout(self.horizontalLayout_48)

        self.groupBox_26 = QGroupBox(self.groupBox_25)
        self.groupBox_26.setObjectName(u"groupBox_26")
        sizePolicy1.setHeightForWidth(self.groupBox_26.sizePolicy().hasHeightForWidth())
        self.groupBox_26.setSizePolicy(sizePolicy1)
        self.verticalLayout_26 = QVBoxLayout(self.groupBox_26)
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.rm_trendline_checkBox = QCheckBox(self.groupBox_26)
        self.rm_trendline_checkBox.setObjectName(u"rm_trendline_checkBox")
        self.rm_trendline_checkBox.setChecked(True)

        self.verticalLayout_26.addWidget(self.rm_trendline_checkBox)

        self.horizontalLayout_49 = QHBoxLayout()
        self.horizontalLayout_49.setObjectName(u"horizontalLayout_49")
        self.horizontalLayout_49.setContentsMargins(-1, 0, -1, -1)
        self.label_49 = QLabel(self.groupBox_26)
        self.label_49.setObjectName(u"label_49")
        sizePolicy4.setHeightForWidth(self.label_49.sizePolicy().hasHeightForWidth())
        self.label_49.setSizePolicy(sizePolicy4)
        self.label_49.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_49.addWidget(self.label_49)

        self.rm_trendline_min_spinBox = QSpinBox(self.groupBox_26)
        self.rm_trendline_min_spinBox.setObjectName(u"rm_trendline_min_spinBox")
        self.rm_trendline_min_spinBox.setMinimum(3)
        self.rm_trendline_min_spinBox.setValue(5)

        self.horizontalLayout_49.addWidget(self.rm_trendline_min_spinBox)


        self.verticalLayout_26.addLayout(self.horizontalLayout_49)

        self.horizontalLayout_50 = QHBoxLayout()
        self.horizontalLayout_50.setObjectName(u"horizontalLayout_50")
        self.horizontalLayout_50.setContentsMargins(-1, 0, -1, -1)
        self.label_50 = QLabel(self.groupBox_26)
        self.label_50.setObjectName(u"label_50")
        sizePolicy4.setHeightForWidth(self.label_50.sizePolicy().hasHeightForWidth())
        self.label_50.setSizePolicy(sizePolicy4)
        self.label_50.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_50.addWidget(self.label_50)

        self.rm_trendline_window_spinBox = QSpinBox(self.groupBox_26)
        self.rm_trendline_window_spinBox.setObjectName(u"rm_trendline_window_spinBox")
        self.rm_trendline_window_spinBox.setMinimum(2)
        self.rm_trendline_window_spinBox.setValue(3)

        self.horizontalLayout_50.addWidget(self.rm_trendline_window_spinBox)


        self.verticalLayout_26.addLayout(self.horizontalLayout_50)


        self.verticalLayout_25.addWidget(self.groupBox_26)

        self.groupBox_27 = QGroupBox(self.groupBox_25)
        self.groupBox_27.setObjectName(u"groupBox_27")
        self.gridLayout_5 = QGridLayout(self.groupBox_27)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.rm_custom_fasta_checkBox = QCheckBox(self.groupBox_27)
        self.rm_custom_fasta_checkBox.setObjectName(u"rm_custom_fasta_checkBox")

        self.gridLayout_5.addWidget(self.rm_custom_fasta_checkBox, 3, 0, 1, 1)

        self.horizontalLayout_51 = QHBoxLayout()
        self.horizontalLayout_51.setObjectName(u"horizontalLayout_51")
        self.horizontalLayout_51.setContentsMargins(-1, 0, -1, -1)
        self.label_51 = QLabel(self.groupBox_27)
        self.label_51.setObjectName(u"label_51")

        self.horizontalLayout_51.addWidget(self.label_51)

        self.rm_custom_ann_path_lineEdit = QLineEdit(self.groupBox_27)
        self.rm_custom_ann_path_lineEdit.setObjectName(u"rm_custom_ann_path_lineEdit")

        self.horizontalLayout_51.addWidget(self.rm_custom_ann_path_lineEdit)

        self.rm_custom_ann_select_pushButton = QPushButton(self.groupBox_27)
        self.rm_custom_ann_select_pushButton.setObjectName(u"rm_custom_ann_select_pushButton")

        self.horizontalLayout_51.addWidget(self.rm_custom_ann_select_pushButton)


        self.gridLayout_5.addLayout(self.horizontalLayout_51, 4, 0, 1, 1)

        self.rm_allsites_checkBox = QCheckBox(self.groupBox_27)
        self.rm_allsites_checkBox.setObjectName(u"rm_allsites_checkBox")
        self.rm_allsites_checkBox.setChecked(True)

        self.gridLayout_5.addWidget(self.rm_allsites_checkBox, 0, 0, 1, 1)

        self.rm_stats_reference_checkBox = QCheckBox(self.groupBox_27)
        self.rm_stats_reference_checkBox.setObjectName(u"rm_stats_reference_checkBox")
        self.rm_stats_reference_checkBox.setChecked(True)

        self.gridLayout_5.addWidget(self.rm_stats_reference_checkBox, 1, 0, 1, 1)

        self.rm_trendline_stats_checkBox = QCheckBox(self.groupBox_27)
        self.rm_trendline_stats_checkBox.setObjectName(u"rm_trendline_stats_checkBox")

        self.gridLayout_5.addWidget(self.rm_trendline_stats_checkBox, 2, 0, 1, 1)


        self.verticalLayout_25.addWidget(self.groupBox_27)


        self.verticalLayout_19.addWidget(self.groupBox_25)

        self.groupBox_18 = QGroupBox(self.scrollAreaWidgetContents_2)
        self.groupBox_18.setObjectName(u"groupBox_18")
        sizePolicy1.setHeightForWidth(self.groupBox_18.sizePolicy().hasHeightForWidth())
        self.groupBox_18.setSizePolicy(sizePolicy1)
        self.verticalLayout_23 = QVBoxLayout(self.groupBox_18)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.crm_checkBox = QCheckBox(self.groupBox_18)
        self.crm_checkBox.setObjectName(u"crm_checkBox")
        self.crm_checkBox.setChecked(True)

        self.verticalLayout_23.addWidget(self.crm_checkBox)

        self.horizontalLayout_40 = QHBoxLayout()
        self.horizontalLayout_40.setObjectName(u"horizontalLayout_40")
        self.label_40 = QLabel(self.groupBox_18)
        self.label_40.setObjectName(u"label_40")
        sizePolicy4.setHeightForWidth(self.label_40.sizePolicy().hasHeightForWidth())
        self.label_40.setSizePolicy(sizePolicy4)
        self.label_40.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_40.addWidget(self.label_40)

        self.crm_filetype_comboBox = QComboBox(self.groupBox_18)
        self.crm_filetype_comboBox.addItem("")
        self.crm_filetype_comboBox.addItem("")
        self.crm_filetype_comboBox.addItem("")
        self.crm_filetype_comboBox.setObjectName(u"crm_filetype_comboBox")

        self.horizontalLayout_40.addWidget(self.crm_filetype_comboBox)


        self.verticalLayout_23.addLayout(self.horizontalLayout_40)

        self.horizontalLayout_41 = QHBoxLayout()
        self.horizontalLayout_41.setObjectName(u"horizontalLayout_41")
        self.label_41 = QLabel(self.groupBox_18)
        self.label_41.setObjectName(u"label_41")
        sizePolicy4.setHeightForWidth(self.label_41.sizePolicy().hasHeightForWidth())
        self.label_41.setSizePolicy(sizePolicy4)
        self.label_41.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_41.addWidget(self.label_41)

        self.crm_chalf_low_doubleSpinBox = QDoubleSpinBox(self.groupBox_18)
        self.crm_chalf_low_doubleSpinBox.setObjectName(u"crm_chalf_low_doubleSpinBox")
        self.crm_chalf_low_doubleSpinBox.setSingleStep(0.010000000000000)

        self.horizontalLayout_41.addWidget(self.crm_chalf_low_doubleSpinBox)


        self.verticalLayout_23.addLayout(self.horizontalLayout_41)

        self.horizontalLayout_42 = QHBoxLayout()
        self.horizontalLayout_42.setObjectName(u"horizontalLayout_42")
        self.label_42 = QLabel(self.groupBox_18)
        self.label_42.setObjectName(u"label_42")
        sizePolicy4.setHeightForWidth(self.label_42.sizePolicy().hasHeightForWidth())
        self.label_42.setSizePolicy(sizePolicy4)
        self.label_42.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_42.addWidget(self.label_42)

        self.crm_chalf_high_doubleSpinBox = QDoubleSpinBox(self.groupBox_18)
        self.crm_chalf_high_doubleSpinBox.setObjectName(u"crm_chalf_high_doubleSpinBox")
        self.crm_chalf_high_doubleSpinBox.setSingleStep(0.010000000000000)
        self.crm_chalf_high_doubleSpinBox.setValue(3.480000000000000)

        self.horizontalLayout_42.addWidget(self.crm_chalf_high_doubleSpinBox)


        self.verticalLayout_23.addLayout(self.horizontalLayout_42)

        self.groupBox_23 = QGroupBox(self.groupBox_18)
        self.groupBox_23.setObjectName(u"groupBox_23")
        sizePolicy1.setHeightForWidth(self.groupBox_23.sizePolicy().hasHeightForWidth())
        self.groupBox_23.setSizePolicy(sizePolicy1)
        self.verticalLayout_24 = QVBoxLayout(self.groupBox_23)
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.crm_trendline_checkBox = QCheckBox(self.groupBox_23)
        self.crm_trendline_checkBox.setObjectName(u"crm_trendline_checkBox")
        self.crm_trendline_checkBox.setChecked(True)

        self.verticalLayout_24.addWidget(self.crm_trendline_checkBox)

        self.horizontalLayout_43 = QHBoxLayout()
        self.horizontalLayout_43.setObjectName(u"horizontalLayout_43")
        self.horizontalLayout_43.setContentsMargins(-1, 0, -1, -1)
        self.label_43 = QLabel(self.groupBox_23)
        self.label_43.setObjectName(u"label_43")
        sizePolicy4.setHeightForWidth(self.label_43.sizePolicy().hasHeightForWidth())
        self.label_43.setSizePolicy(sizePolicy4)
        self.label_43.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_43.addWidget(self.label_43)

        self.crm_trendline_min_spinBox = QSpinBox(self.groupBox_23)
        self.crm_trendline_min_spinBox.setObjectName(u"crm_trendline_min_spinBox")
        self.crm_trendline_min_spinBox.setMinimum(3)
        self.crm_trendline_min_spinBox.setValue(5)

        self.horizontalLayout_43.addWidget(self.crm_trendline_min_spinBox)


        self.verticalLayout_24.addLayout(self.horizontalLayout_43)

        self.horizontalLayout_44 = QHBoxLayout()
        self.horizontalLayout_44.setObjectName(u"horizontalLayout_44")
        self.horizontalLayout_44.setContentsMargins(-1, 0, -1, -1)
        self.label_44 = QLabel(self.groupBox_23)
        self.label_44.setObjectName(u"label_44")
        sizePolicy4.setHeightForWidth(self.label_44.sizePolicy().hasHeightForWidth())
        self.label_44.setSizePolicy(sizePolicy4)
        self.label_44.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_44.addWidget(self.label_44)

        self.crm_trendline_window_spinBox = QSpinBox(self.groupBox_23)
        self.crm_trendline_window_spinBox.setObjectName(u"crm_trendline_window_spinBox")
        self.crm_trendline_window_spinBox.setMinimum(2)
        self.crm_trendline_window_spinBox.setValue(3)

        self.horizontalLayout_44.addWidget(self.crm_trendline_window_spinBox)


        self.verticalLayout_24.addLayout(self.horizontalLayout_44)


        self.verticalLayout_23.addWidget(self.groupBox_23)

        self.groupBox_24 = QGroupBox(self.groupBox_18)
        self.groupBox_24.setObjectName(u"groupBox_24")
        self.gridLayout = QGridLayout(self.groupBox_24)
        self.gridLayout.setObjectName(u"gridLayout")
        self.crm_custom_fasta_checkBox = QCheckBox(self.groupBox_24)
        self.crm_custom_fasta_checkBox.setObjectName(u"crm_custom_fasta_checkBox")

        self.gridLayout.addWidget(self.crm_custom_fasta_checkBox, 4, 0, 1, 1)

        self.crm_allsites_checkBox = QCheckBox(self.groupBox_24)
        self.crm_allsites_checkBox.setObjectName(u"crm_allsites_checkBox")
        self.crm_allsites_checkBox.setChecked(True)

        self.gridLayout.addWidget(self.crm_allsites_checkBox, 0, 0, 1, 1)

        self.crm_trendline_stats_checkBox = QCheckBox(self.groupBox_24)
        self.crm_trendline_stats_checkBox.setObjectName(u"crm_trendline_stats_checkBox")

        self.gridLayout.addWidget(self.crm_trendline_stats_checkBox, 3, 0, 1, 1)

        self.crm_shared_only_checkBox = QCheckBox(self.groupBox_24)
        self.crm_shared_only_checkBox.setObjectName(u"crm_shared_only_checkBox")
        self.crm_shared_only_checkBox.setChecked(True)

        self.gridLayout.addWidget(self.crm_shared_only_checkBox, 1, 0, 1, 1)

        self.crm_stats_reference_checkBox = QCheckBox(self.groupBox_24)
        self.crm_stats_reference_checkBox.setObjectName(u"crm_stats_reference_checkBox")
        self.crm_stats_reference_checkBox.setChecked(True)

        self.gridLayout.addWidget(self.crm_stats_reference_checkBox, 2, 0, 1, 1)

        self.horizontalLayout_45 = QHBoxLayout()
        self.horizontalLayout_45.setObjectName(u"horizontalLayout_45")
        self.horizontalLayout_45.setContentsMargins(-1, 0, -1, -1)
        self.label_45 = QLabel(self.groupBox_24)
        self.label_45.setObjectName(u"label_45")

        self.horizontalLayout_45.addWidget(self.label_45)

        self.crm_custom_ann_path_lineEdit = QLineEdit(self.groupBox_24)
        self.crm_custom_ann_path_lineEdit.setObjectName(u"crm_custom_ann_path_lineEdit")

        self.horizontalLayout_45.addWidget(self.crm_custom_ann_path_lineEdit)

        self.crm_custom_ann_select_pushButton = QPushButton(self.groupBox_24)
        self.crm_custom_ann_select_pushButton.setObjectName(u"crm_custom_ann_select_pushButton")

        self.horizontalLayout_45.addWidget(self.crm_custom_ann_select_pushButton)


        self.gridLayout.addLayout(self.horizontalLayout_45, 5, 0, 1, 1)


        self.verticalLayout_23.addWidget(self.groupBox_24)


        self.verticalLayout_19.addWidget(self.groupBox_18)

        self.groupBox_21 = QGroupBox(self.scrollAreaWidgetContents_2)
        self.groupBox_21.setObjectName(u"groupBox_21")
        sizePolicy1.setHeightForWidth(self.groupBox_21.sizePolicy().hasHeightForWidth())
        self.groupBox_21.setSizePolicy(sizePolicy1)
        self.verticalLayout_27 = QVBoxLayout(self.groupBox_21)
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.crm_checkBox_3 = QCheckBox(self.groupBox_21)
        self.crm_checkBox_3.setObjectName(u"crm_checkBox_3")
        self.crm_checkBox_3.setChecked(True)

        self.verticalLayout_27.addWidget(self.crm_checkBox_3)

        self.horizontalLayout_52 = QHBoxLayout()
        self.horizontalLayout_52.setObjectName(u"horizontalLayout_52")
        self.label_52 = QLabel(self.groupBox_21)
        self.label_52.setObjectName(u"label_52")
        sizePolicy4.setHeightForWidth(self.label_52.sizePolicy().hasHeightForWidth())
        self.label_52.setSizePolicy(sizePolicy4)
        self.label_52.setMinimumSize(QSize(90, 0))

        self.horizontalLayout_52.addWidget(self.label_52)

        self.dm_filetype_comboBox = QComboBox(self.groupBox_21)
        self.dm_filetype_comboBox.addItem("")
        self.dm_filetype_comboBox.addItem("")
        self.dm_filetype_comboBox.addItem("")
        self.dm_filetype_comboBox.setObjectName(u"dm_filetype_comboBox")

        self.horizontalLayout_52.addWidget(self.dm_filetype_comboBox)


        self.verticalLayout_27.addLayout(self.horizontalLayout_52)

        self.horizontalLayout_53 = QHBoxLayout()
        self.horizontalLayout_53.setObjectName(u"horizontalLayout_53")
        self.label_53 = QLabel(self.groupBox_21)
        self.label_53.setObjectName(u"label_53")
        sizePolicy4.setHeightForWidth(self.label_53.sizePolicy().hasHeightForWidth())
        self.label_53.setSizePolicy(sizePolicy4)
        self.label_53.setMinimumSize(QSize(90, 0))

        self.horizontalLayout_53.addWidget(self.label_53)

        self.dm_chalf_low_doubleSpinBox = QDoubleSpinBox(self.groupBox_21)
        self.dm_chalf_low_doubleSpinBox.setObjectName(u"dm_chalf_low_doubleSpinBox")
        self.dm_chalf_low_doubleSpinBox.setMinimum(-99.989999999999995)
        self.dm_chalf_low_doubleSpinBox.setMaximum(0.000000000000000)
        self.dm_chalf_low_doubleSpinBox.setSingleStep(0.010000000000000)
        self.dm_chalf_low_doubleSpinBox.setValue(-3.480000000000000)

        self.horizontalLayout_53.addWidget(self.dm_chalf_low_doubleSpinBox)


        self.verticalLayout_27.addLayout(self.horizontalLayout_53)

        self.horizontalLayout_54 = QHBoxLayout()
        self.horizontalLayout_54.setObjectName(u"horizontalLayout_54")
        self.label_54 = QLabel(self.groupBox_21)
        self.label_54.setObjectName(u"label_54")
        sizePolicy4.setHeightForWidth(self.label_54.sizePolicy().hasHeightForWidth())
        self.label_54.setSizePolicy(sizePolicy4)
        self.label_54.setMinimumSize(QSize(90, 0))

        self.horizontalLayout_54.addWidget(self.label_54)

        self.dm_chalf_high_doubleSpinBox = QDoubleSpinBox(self.groupBox_21)
        self.dm_chalf_high_doubleSpinBox.setObjectName(u"dm_chalf_high_doubleSpinBox")
        self.dm_chalf_high_doubleSpinBox.setSingleStep(0.010000000000000)
        self.dm_chalf_high_doubleSpinBox.setValue(3.480000000000000)

        self.horizontalLayout_54.addWidget(self.dm_chalf_high_doubleSpinBox)


        self.verticalLayout_27.addLayout(self.horizontalLayout_54)

        self.groupBox_28 = QGroupBox(self.groupBox_21)
        self.groupBox_28.setObjectName(u"groupBox_28")
        sizePolicy1.setHeightForWidth(self.groupBox_28.sizePolicy().hasHeightForWidth())
        self.groupBox_28.setSizePolicy(sizePolicy1)
        self.verticalLayout_28 = QVBoxLayout(self.groupBox_28)
        self.verticalLayout_28.setObjectName(u"verticalLayout_28")
        self.dm_trendline_checkBox = QCheckBox(self.groupBox_28)
        self.dm_trendline_checkBox.setObjectName(u"dm_trendline_checkBox")
        self.dm_trendline_checkBox.setChecked(True)

        self.verticalLayout_28.addWidget(self.dm_trendline_checkBox)

        self.horizontalLayout_55 = QHBoxLayout()
        self.horizontalLayout_55.setObjectName(u"horizontalLayout_55")
        self.horizontalLayout_55.setContentsMargins(-1, 0, -1, -1)
        self.label_55 = QLabel(self.groupBox_28)
        self.label_55.setObjectName(u"label_55")
        sizePolicy4.setHeightForWidth(self.label_55.sizePolicy().hasHeightForWidth())
        self.label_55.setSizePolicy(sizePolicy4)
        self.label_55.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_55.addWidget(self.label_55)

        self.dm_trendline_min_spinBox = QSpinBox(self.groupBox_28)
        self.dm_trendline_min_spinBox.setObjectName(u"dm_trendline_min_spinBox")
        self.dm_trendline_min_spinBox.setMinimum(3)
        self.dm_trendline_min_spinBox.setValue(5)

        self.horizontalLayout_55.addWidget(self.dm_trendline_min_spinBox)


        self.verticalLayout_28.addLayout(self.horizontalLayout_55)

        self.horizontalLayout_56 = QHBoxLayout()
        self.horizontalLayout_56.setObjectName(u"horizontalLayout_56")
        self.horizontalLayout_56.setContentsMargins(-1, 0, -1, -1)
        self.label_56 = QLabel(self.groupBox_28)
        self.label_56.setObjectName(u"label_56")
        sizePolicy4.setHeightForWidth(self.label_56.sizePolicy().hasHeightForWidth())
        self.label_56.setSizePolicy(sizePolicy4)
        self.label_56.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_56.addWidget(self.label_56)

        self.dm_trendline_window_spinBox = QSpinBox(self.groupBox_28)
        self.dm_trendline_window_spinBox.setObjectName(u"dm_trendline_window_spinBox")
        self.dm_trendline_window_spinBox.setMinimum(2)
        self.dm_trendline_window_spinBox.setValue(3)

        self.horizontalLayout_56.addWidget(self.dm_trendline_window_spinBox)


        self.verticalLayout_28.addLayout(self.horizontalLayout_56)


        self.verticalLayout_27.addWidget(self.groupBox_28)

        self.groupBox_20 = QGroupBox(self.groupBox_21)
        self.groupBox_20.setObjectName(u"groupBox_20")
        self.verticalLayout_22 = QVBoxLayout(self.groupBox_20)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.label_37 = QLabel(self.groupBox_20)
        self.label_37.setObjectName(u"label_37")
        sizePolicy4.setHeightForWidth(self.label_37.sizePolicy().hasHeightForWidth())
        self.label_37.setSizePolicy(sizePolicy4)
        self.label_37.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_16.addWidget(self.label_37)

        self.dm_kde_min_spinBox = QSpinBox(self.groupBox_20)
        self.dm_kde_min_spinBox.setObjectName(u"dm_kde_min_spinBox")
        self.dm_kde_min_spinBox.setMinimum(3)

        self.horizontalLayout_16.addWidget(self.dm_kde_min_spinBox)


        self.verticalLayout_22.addLayout(self.horizontalLayout_16)

        self.horizontalLayout_38 = QHBoxLayout()
        self.horizontalLayout_38.setObjectName(u"horizontalLayout_38")
        self.horizontalLayout_38.setContentsMargins(-1, 6, -1, -1)
        self.dm_kde_sig_cutoff_checkBox = QCheckBox(self.groupBox_20)
        self.dm_kde_sig_cutoff_checkBox.setObjectName(u"dm_kde_sig_cutoff_checkBox")
        sizePolicy2.setHeightForWidth(self.dm_kde_sig_cutoff_checkBox.sizePolicy().hasHeightForWidth())
        self.dm_kde_sig_cutoff_checkBox.setSizePolicy(sizePolicy2)

        self.horizontalLayout_38.addWidget(self.dm_kde_sig_cutoff_checkBox)

        self.dm_kde_sig_cutoff_doubleSpinBox = QDoubleSpinBox(self.groupBox_20)
        self.dm_kde_sig_cutoff_doubleSpinBox.setObjectName(u"dm_kde_sig_cutoff_doubleSpinBox")
        self.dm_kde_sig_cutoff_doubleSpinBox.setDecimals(8)
        self.dm_kde_sig_cutoff_doubleSpinBox.setMaximum(1.000000000000000)
        self.dm_kde_sig_cutoff_doubleSpinBox.setValue(0.050000000000000)

        self.horizontalLayout_38.addWidget(self.dm_kde_sig_cutoff_doubleSpinBox)


        self.verticalLayout_22.addLayout(self.horizontalLayout_38)


        self.verticalLayout_27.addWidget(self.groupBox_20)

        self.groupBox_29 = QGroupBox(self.groupBox_21)
        self.groupBox_29.setObjectName(u"groupBox_29")
        self.gridLayout_6 = QGridLayout(self.groupBox_29)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.dm_trendline_stats_checkBox = QCheckBox(self.groupBox_29)
        self.dm_trendline_stats_checkBox.setObjectName(u"dm_trendline_stats_checkBox")

        self.gridLayout_6.addWidget(self.dm_trendline_stats_checkBox, 2, 0, 1, 1)

        self.horizontalLayout_57 = QHBoxLayout()
        self.horizontalLayout_57.setObjectName(u"horizontalLayout_57")
        self.horizontalLayout_57.setContentsMargins(-1, 0, -1, -1)
        self.label_57 = QLabel(self.groupBox_29)
        self.label_57.setObjectName(u"label_57")

        self.horizontalLayout_57.addWidget(self.label_57)

        self.dm_custom_ann_path_lineEdit = QLineEdit(self.groupBox_29)
        self.dm_custom_ann_path_lineEdit.setObjectName(u"dm_custom_ann_path_lineEdit")

        self.horizontalLayout_57.addWidget(self.dm_custom_ann_path_lineEdit)

        self.dm_custom_ann_select_pushButton = QPushButton(self.groupBox_29)
        self.dm_custom_ann_select_pushButton.setObjectName(u"dm_custom_ann_select_pushButton")

        self.horizontalLayout_57.addWidget(self.dm_custom_ann_select_pushButton)


        self.gridLayout_6.addLayout(self.horizontalLayout_57, 4, 0, 1, 1)

        self.dm_allsites_checkBox = QCheckBox(self.groupBox_29)
        self.dm_allsites_checkBox.setObjectName(u"dm_allsites_checkBox")
        self.dm_allsites_checkBox.setChecked(True)

        self.gridLayout_6.addWidget(self.dm_allsites_checkBox, 0, 0, 1, 1)

        self.dm_stats_reference_checkBox = QCheckBox(self.groupBox_29)
        self.dm_stats_reference_checkBox.setObjectName(u"dm_stats_reference_checkBox")
        self.dm_stats_reference_checkBox.setChecked(True)

        self.gridLayout_6.addWidget(self.dm_stats_reference_checkBox, 1, 0, 1, 1)

        self.dm_custom_fasta_checkBox = QCheckBox(self.groupBox_29)
        self.dm_custom_fasta_checkBox.setObjectName(u"dm_custom_fasta_checkBox")

        self.gridLayout_6.addWidget(self.dm_custom_fasta_checkBox, 3, 0, 1, 1)


        self.verticalLayout_27.addWidget(self.groupBox_29)


        self.verticalLayout_19.addWidget(self.groupBox_21)

        self.groupBox_19 = QGroupBox(self.scrollAreaWidgetContents_2)
        self.groupBox_19.setObjectName(u"groupBox_19")
        self.verticalLayout_29 = QVBoxLayout(self.groupBox_19)
        self.verticalLayout_29.setObjectName(u"verticalLayout_29")
        self.cs_checkBox = QCheckBox(self.groupBox_19)
        self.cs_checkBox.setObjectName(u"cs_checkBox")
        self.cs_checkBox.setChecked(False)

        self.verticalLayout_29.addWidget(self.cs_checkBox)

        self.horizontalLayout_60 = QHBoxLayout()
        self.horizontalLayout_60.setObjectName(u"horizontalLayout_60")
        self.label_60 = QLabel(self.groupBox_19)
        self.label_60.setObjectName(u"label_60")
        sizePolicy4.setHeightForWidth(self.label_60.sizePolicy().hasHeightForWidth())
        self.label_60.setSizePolicy(sizePolicy4)
        self.label_60.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_60.addWidget(self.label_60)

        self.cs_filetype_comboBox = QComboBox(self.groupBox_19)
        self.cs_filetype_comboBox.addItem("")
        self.cs_filetype_comboBox.addItem("")
        self.cs_filetype_comboBox.addItem("")
        self.cs_filetype_comboBox.setObjectName(u"cs_filetype_comboBox")

        self.horizontalLayout_60.addWidget(self.cs_filetype_comboBox)


        self.verticalLayout_29.addLayout(self.horizontalLayout_60)

        self.horizontalLayout_59 = QHBoxLayout()
        self.horizontalLayout_59.setObjectName(u"horizontalLayout_59")
        self.label_59 = QLabel(self.groupBox_19)
        self.label_59.setObjectName(u"label_59")
        sizePolicy4.setHeightForWidth(self.label_59.sizePolicy().hasHeightForWidth())
        self.label_59.setSizePolicy(sizePolicy4)
        self.label_59.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_59.addWidget(self.label_59)

        self.cs_chalf_low_doubleSpinBox = QDoubleSpinBox(self.groupBox_19)
        self.cs_chalf_low_doubleSpinBox.setObjectName(u"cs_chalf_low_doubleSpinBox")
        self.cs_chalf_low_doubleSpinBox.setSingleStep(0.010000000000000)

        self.horizontalLayout_59.addWidget(self.cs_chalf_low_doubleSpinBox)


        self.verticalLayout_29.addLayout(self.horizontalLayout_59)

        self.horizontalLayout_58 = QHBoxLayout()
        self.horizontalLayout_58.setObjectName(u"horizontalLayout_58")
        self.label_58 = QLabel(self.groupBox_19)
        self.label_58.setObjectName(u"label_58")
        sizePolicy4.setHeightForWidth(self.label_58.sizePolicy().hasHeightForWidth())
        self.label_58.setSizePolicy(sizePolicy4)
        self.label_58.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_58.addWidget(self.label_58)

        self.cs_chalf_high_doubleSpinBox = QDoubleSpinBox(self.groupBox_19)
        self.cs_chalf_high_doubleSpinBox.setObjectName(u"cs_chalf_high_doubleSpinBox")
        self.cs_chalf_high_doubleSpinBox.setSingleStep(0.010000000000000)
        self.cs_chalf_high_doubleSpinBox.setValue(3.480000000000000)

        self.horizontalLayout_58.addWidget(self.cs_chalf_high_doubleSpinBox)


        self.verticalLayout_29.addLayout(self.horizontalLayout_58)


        self.verticalLayout_19.addWidget(self.groupBox_19)

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout_18.addWidget(self.scrollArea_2)


        self.horizontalLayout_33.addWidget(self.groupBox_15)

        self.groupBox_16 = QGroupBox(self.visualization_tab)
        self.groupBox_16.setObjectName(u"groupBox_16")
        sizePolicy6.setHeightForWidth(self.groupBox_16.sizePolicy().hasHeightForWidth())
        self.groupBox_16.setSizePolicy(sizePolicy6)
        self.groupBox_16.setMinimumSize(QSize(500, 0))
        self.verticalLayout_17 = QVBoxLayout(self.groupBox_16)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.visaulization_tableWidget = QTableWidget(self.groupBox_16)
        if (self.visaulization_tableWidget.columnCount() < 4):
            self.visaulization_tableWidget.setColumnCount(4)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.visaulization_tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.visaulization_tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.visaulization_tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.visaulization_tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem9)
        self.visaulization_tableWidget.setObjectName(u"visaulization_tableWidget")
        self.visaulization_tableWidget.setEnabled(True)
        sizePolicy.setHeightForWidth(self.visaulization_tableWidget.sizePolicy().hasHeightForWidth())
        self.visaulization_tableWidget.setSizePolicy(sizePolicy)
        self.visaulization_tableWidget.setMinimumSize(QSize(400, 200))
        self.visaulization_tableWidget.setAutoFillBackground(False)
        self.visaulization_tableWidget.horizontalHeader().setDefaultSectionSize(110)
        self.visaulization_tableWidget.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_17.addWidget(self.visaulization_tableWidget)

        self.groupBox_22 = QGroupBox(self.groupBox_16)
        self.groupBox_22.setObjectName(u"groupBox_22")
        sizePolicy1.setHeightForWidth(self.groupBox_22.sizePolicy().hasHeightForWidth())
        self.groupBox_22.setSizePolicy(sizePolicy1)
        self.verticalLayout_20 = QVBoxLayout(self.groupBox_22)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.horizontalLayout_34 = QHBoxLayout()
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.vis_conditions_comboBox = QComboBox(self.groupBox_22)
        self.vis_conditions_comboBox.setObjectName(u"vis_conditions_comboBox")

        self.horizontalLayout_34.addWidget(self.vis_conditions_comboBox)

        self.vis_add_pushButton = QPushButton(self.groupBox_22)
        self.vis_add_pushButton.setObjectName(u"vis_add_pushButton")

        self.horizontalLayout_34.addWidget(self.vis_add_pushButton)

        self.vis_add_all_pushButton = QPushButton(self.groupBox_22)
        self.vis_add_all_pushButton.setObjectName(u"vis_add_all_pushButton")

        self.horizontalLayout_34.addWidget(self.vis_add_all_pushButton)

        self.vis_remove_pushButton = QPushButton(self.groupBox_22)
        self.vis_remove_pushButton.setObjectName(u"vis_remove_pushButton")

        self.horizontalLayout_34.addWidget(self.vis_remove_pushButton)

        self.vis_remove_all_pushButton = QPushButton(self.groupBox_22)
        self.vis_remove_all_pushButton.setObjectName(u"vis_remove_all_pushButton")

        self.horizontalLayout_34.addWidget(self.vis_remove_all_pushButton)

        self.horizontalLayout_34.setStretch(0, 1)

        self.verticalLayout_20.addLayout(self.horizontalLayout_34)

        self.horizontalLayout_36 = QHBoxLayout()
        self.horizontalLayout_36.setObjectName(u"horizontalLayout_36")
        self.vis_set_group_pushButton = QPushButton(self.groupBox_22)
        self.vis_set_group_pushButton.setObjectName(u"vis_set_group_pushButton")

        self.horizontalLayout_36.addWidget(self.vis_set_group_pushButton)

        self.vis_set_ref_pushButton = QPushButton(self.groupBox_22)
        self.vis_set_ref_pushButton.setObjectName(u"vis_set_ref_pushButton")

        self.horizontalLayout_36.addWidget(self.vis_set_ref_pushButton)

        self.vis_set_exp_pushButton = QPushButton(self.groupBox_22)
        self.vis_set_exp_pushButton.setObjectName(u"vis_set_exp_pushButton")

        self.horizontalLayout_36.addWidget(self.vis_set_exp_pushButton)

        self.vis_set_color_pushButton = QPushButton(self.groupBox_22)
        self.vis_set_color_pushButton.setObjectName(u"vis_set_color_pushButton")

        self.horizontalLayout_36.addWidget(self.vis_set_color_pushButton)


        self.verticalLayout_20.addLayout(self.horizontalLayout_36)

        self.label_33 = QLabel(self.groupBox_22)
        self.label_33.setObjectName(u"label_33")
        self.label_33.setWordWrap(True)

        self.verticalLayout_20.addWidget(self.label_33)


        self.verticalLayout_17.addWidget(self.groupBox_22)


        self.horizontalLayout_33.addWidget(self.groupBox_16)

        self.horizontalLayout_33.setStretch(0, 3)
        self.horizontalLayout_33.setStretch(1, 1)

        self.horizontalLayout_31.addLayout(self.horizontalLayout_33)

        self.mainTabWidget.addTab(self.visualization_tab, "")
        self.run_tab = QWidget()
        self.run_tab.setObjectName(u"run_tab")
        self.verticalLayout_30 = QVBoxLayout(self.run_tab)
        self.verticalLayout_30.setObjectName(u"verticalLayout_30")
        self.horizontalLayout_39 = QHBoxLayout()
        self.horizontalLayout_39.setObjectName(u"horizontalLayout_39")
        self.label_38 = QLabel(self.run_tab)
        self.label_38.setObjectName(u"label_38")

        self.horizontalLayout_39.addWidget(self.label_38)

        self.run_outputdir_lineEdit = QLineEdit(self.run_tab)
        self.run_outputdir_lineEdit.setObjectName(u"run_outputdir_lineEdit")

        self.horizontalLayout_39.addWidget(self.run_outputdir_lineEdit)

        self.run_browse_pushButton = QPushButton(self.run_tab)
        self.run_browse_pushButton.setObjectName(u"run_browse_pushButton")

        self.horizontalLayout_39.addWidget(self.run_browse_pushButton)

        self.run_open_pushButton = QPushButton(self.run_tab)
        self.run_open_pushButton.setObjectName(u"run_open_pushButton")

        self.horizontalLayout_39.addWidget(self.run_open_pushButton)


        self.verticalLayout_30.addLayout(self.horizontalLayout_39)

        self.horizontalLayout_61 = QHBoxLayout()
        self.horizontalLayout_61.setObjectName(u"horizontalLayout_61")
        self.run_start_pushButton = QPushButton(self.run_tab)
        self.run_start_pushButton.setObjectName(u"run_start_pushButton")

        self.horizontalLayout_61.addWidget(self.run_start_pushButton)

        self.run_stop_pushButton = QPushButton(self.run_tab)
        self.run_stop_pushButton.setObjectName(u"run_stop_pushButton")

        self.horizontalLayout_61.addWidget(self.run_stop_pushButton)

        self.run_log_export_pushButton = QPushButton(self.run_tab)
        self.run_log_export_pushButton.setObjectName(u"run_log_export_pushButton")

        self.horizontalLayout_61.addWidget(self.run_log_export_pushButton)

        self.run_log_clear_pushButton = QPushButton(self.run_tab)
        self.run_log_clear_pushButton.setObjectName(u"run_log_clear_pushButton")

        self.horizontalLayout_61.addWidget(self.run_log_clear_pushButton)


        self.verticalLayout_30.addLayout(self.horizontalLayout_61)

        self.groupBox_30 = QGroupBox(self.run_tab)
        self.groupBox_30.setObjectName(u"groupBox_30")
        self.verticalLayout_31 = QVBoxLayout(self.groupBox_30)
        self.verticalLayout_31.setObjectName(u"verticalLayout_31")
        self.run_log_textEdit = QTextEdit(self.groupBox_30)
        self.run_log_textEdit.setObjectName(u"run_log_textEdit")

        self.verticalLayout_31.addWidget(self.run_log_textEdit)


        self.verticalLayout_30.addWidget(self.groupBox_30)

        self.mainTabWidget.addTab(self.run_tab, "")

        self.verticalLayout.addWidget(self.mainTabWidget)


        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 900, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.mainTabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.logo_chalf.setText("")
        self.logo_text.setText(QCoreApplication.translate("MainWindow", u"CHalf v4.3 - JC Price Lab", None))
        self.logo_byu.setText("")
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Workflows", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Select a workflow:", None))
        self.workflow_comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Default (IPSA)", None))
        self.workflow_comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"SPROX", None))

        self.load_workflow_pushButton.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Save current settings as workflow:", None))
        self.save_workflow_pushButton.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.open_workflow_folder_pushButton.setText(QCoreApplication.translate("MainWindow", u"Open Folder", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>For information on how workflows work <a href=\"https://github.com/JC-Price/Chalf_public?tab=readme-ov-file#chalf-v422\"><span style=\" text-decoration: underline; color:#0000ff;\">see this tutorial</span></a>.</p></body></html>", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Input Files", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>CHalf takes an input of csv files with quantified and identified peptides. Formatting matters for the analysis. See this <a href=\"https://github.com/JC-Price/Chalf_public/blob/main/Demos/CHalf%20Inputs%20Formatting%20Guide.xlsx\"><span style=\" text-decoration: underline; color:#0000ff;\">formatting guide</span></a> before starting.</p></body></html>", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>File options:</p></body></html>", None))
        self.add_pp_files_pushButton.setText(QCoreApplication.translate("MainWindow", u"Add files", None))
        self.remove_selected_pp_files_pushButton.setText(QCoreApplication.translate("MainWindow", u"Remove selected files", None))
        self.clear_pp_files_pushButton.setText(QCoreApplication.translate("MainWindow", u"Clear files", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"right\">Options for rerunning files:</p></body></html>", None))
        self.save_manifest_pushButton.setText(QCoreApplication.translate("MainWindow", u"Save as manifest", None))
        self.load_manifest_pushButton.setText(QCoreApplication.translate("MainWindow", u"Load manifest", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Named concentration columns are paired to concentration values for use in curve fitting. You can save pairings of column names and concentration values by selecting \"New\" under the dropdown and can assign existing pairings to conditions using \"Assign to condition.\" \"Edit\" allows you to make changes to your existing presets. Presets will be saved in the presets folder in the CHalf base directory.", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"Set condition names:", None))
        self.condname_consecutive_pushButton.setText(QCoreApplication.translate("MainWindow", u"Consecutively", None))
        self.condname_filename_pushButton.setText(QCoreApplication.translate("MainWindow", u"By file name", None))
        self.condname_dir_pushButton.setText(QCoreApplication.translate("MainWindow", u"By parent directory", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Set concentration columns:", None))
        self.concentration_columns_comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Default (IPSA)", None))

        self.assign_concentration_pushButton.setText(QCoreApplication.translate("MainWindow", u"Assign to conditions", None))
        self.creat_concentration_pushButton.setText(QCoreApplication.translate("MainWindow", u"Edit", None))
        ___qtablewidgetitem = self.files_tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"File (path)", None));
        ___qtablewidgetitem1 = self.files_tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Condition (unique string)", None));
        ___qtablewidgetitem2 = self.files_tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Concentration columns (preset)", None));
        ___qtablewidgetitem3 = self.files_tableWidget.verticalHeaderItem(0)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem4 = self.files_tableWidget.verticalHeaderItem(1)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem5 = self.files_tableWidget.verticalHeaderItem(2)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        self.mainTabWidget.setTabText(self.mainTabWidget.indexOf(self.workflow_tab), QCoreApplication.translate("MainWindow", u"Workflow", None))
        self.run_chalf_checkBox.setText(QCoreApplication.translate("MainWindow", u"Run CHalf", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("MainWindow", u"Search Options", None))
        self.light_search_checkBox.setText(QCoreApplication.translate("MainWindow", u"Light Search", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Reduces computation time by only fitting peptides that have labelable residues. \"Residues to Search\" is still mandatory for site localization.", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("MainWindow", u"Residues to Search", None))
        self.aa_y_checkBox.setText(QCoreApplication.translate("MainWindow", u"Y", None))
        self.aa_q_checkBox.setText(QCoreApplication.translate("MainWindow", u"Q", None))
        self.aa_r_checkBox.setText(QCoreApplication.translate("MainWindow", u"R", None))
        self.aa_k_checkBox.setText(QCoreApplication.translate("MainWindow", u"K", None))
        self.aa_d_checkBox.setText(QCoreApplication.translate("MainWindow", u"D", None))
        self.aa_e_checkBox.setText(QCoreApplication.translate("MainWindow", u"E", None))
        self.aa_w_checkBox.setText(QCoreApplication.translate("MainWindow", u"W", None))
        self.aa_n_checkBox.setText(QCoreApplication.translate("MainWindow", u"N", None))
        self.aa_s_checkBox.setText(QCoreApplication.translate("MainWindow", u"S", None))
        self.aa_t_checkBox.setText(QCoreApplication.translate("MainWindow", u"T", None))
        self.aa_p_checkBox.setText(QCoreApplication.translate("MainWindow", u"P", None))
        self.aa_f_checkBox.setText(QCoreApplication.translate("MainWindow", u"F", None))
        self.aa_g_checkBox.setText(QCoreApplication.translate("MainWindow", u"G", None))
        self.aa_a_checkBox.setText(QCoreApplication.translate("MainWindow", u"A", None))
        self.aa_v_checkBox.setText(QCoreApplication.translate("MainWindow", u"V", None))
        self.aa_L_checkBox.setText(QCoreApplication.translate("MainWindow", u"L", None))
        self.aa_i_checkBox.setText(QCoreApplication.translate("MainWindow", u"I", None))
        self.aa_h_checkBox.setText(QCoreApplication.translate("MainWindow", u"H", None))
        self.aa_c_checkBox.setText(QCoreApplication.translate("MainWindow", u"C", None))
        self.aa_m_checkBox.setText(QCoreApplication.translate("MainWindow", u"M", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"Filter Options", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"C\u00bd Minimum:", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"C\u00bd Maximum:", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"R\u00b2 Cutoff:", None))
        self.CI_filter_checkBox.setText(QCoreApplication.translate("MainWindow", u"Confidence Interval / Range Cutoff:", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Confidence Interval is not always a good measure of curve fit. Oftentimes, it will filter out significant transitions with near-perfect fits. R\u00b2 tends to be the best measure of fit, but you may optionally choose to include CI cutoffs.", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Fitting parameter optimization priority:", None))
        self.fit_opt_comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"R\u00b2", None))
        self.fit_opt_comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Confidence Interval", None))

        self.sig_only_checkBox.setText(QCoreApplication.translate("MainWindow", u"Keep only signficant curves in final combined sites output", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Fitting Options", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"right\">Minimum Points for Calculation:</p></body></html>", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"right\">Outlier Cutoff (StdErr x #):</p></body></html>", None))
        self.label_34.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"right\">Zero Abundance Rule:</p></body></html>", None))
        self.chalf_zero_criteria_comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Remove", None))
        self.chalf_zero_criteria_comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Keep", None))
        self.chalf_zero_criteria_comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Impute", None))

        self.trimming_checkBox.setText(QCoreApplication.translate("MainWindow", u"Allow Trimming (Removes outliers)", None))
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>These options set the number of significant points necessary to attempt curve fitting. Paramaters from the resulting curves will be used to remove outliers before attempting a second fitting to get more accurate curves. Zero abundance values in the raw data can be dropped to avoid impacting normalization, kept to serve as the minimum in normalization, or removed prior to normalization and imputed back into the curve prior to fitting. Each method has strengths and weaknesses, but we recommend removing zeros as they often occur more as a result of inconsistencies in precursor selection than due to true zero-abundance species.</p></body></html>", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Graphing Options", None))
        self.graph_cruves_checkBox.setText(QCoreApplication.translate("MainWindow", u"Generate Curve Figures (increases computation time)", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"File Type:", None))
        self.graphing_filetype_comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u".jpg", None))
        self.graphing_filetype_comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u".png", None))
        self.graphing_filetype_comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u".svg", None))

        self.label_17.setText(QCoreApplication.translate("MainWindow", u"C\u00bd Minimum:", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"R\u00b2 Cutoff:", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"C\u00bd Maximum:", None))
        self.graph_ci_checkBox.setText(QCoreApplication.translate("MainWindow", u"Confidence Interval / Range Cutoff:", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"Experimental Options (use at your own risk)", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>This section contains experimental modifcations to CHalf that were tested during development. Each of these tools has a specific use case where they may be beneficial but was ultimately not included in the default CHalf calculation method as they only apply in specific use cases and can lead to incorrect conclusions if used outside of the correct use case. We have included them in this version of CHalf for optional use, but we only recommend using them with caution and where their designed use case applies. These tools are alos less optimized for use in CHalf, meaning that incorrect usage can lead to errors that will not be supported in later development. For more infomration on each of these experimental options, see <a href=\"https://github.com/JC-Price/Chalf_public/blob/main/Demos/Residue%20Mapper%20Explanations.md\"><span style=\" text-decoration: underline; color:#0000ff;\">CHalf Experimental Options</span></a> in the documentation.</p></body></html>", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("MainWindow", u"Savitzky-Golay (SG) Filter", None))
        self.sg_checkBox.setText(QCoreApplication.translate("MainWindow", u"SG Curve Smoothing", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"Performs a Savitzky-Golay (SG) Filter to your raw abundance data prior to normalizing to reduce the impacts of machine noise. Using this option improves the likelihood that peptides will be fit with curves at the risk of introducing incorrect or misleading fits. In general, an SG filter is not recommended before performing curve fitting.", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"Window Size (must be less than the number of points in the curve):", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"Polynomial Order (must be less than the window size):", None))
        self.groupBox_10.setTitle(QCoreApplication.translate("MainWindow", u"Windowed Fitting", None))
        self.windowed_fitting_checkBox.setText(QCoreApplication.translate("MainWindow", u"Windowed Fitting", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Windowed fitting attempt to break the curve into several windows for fitting different features of the curve in order to catch variations in the curve that correspond to structurally significant variations in labeling efficiency. This feature can help identify real C\u00bd values that would often be lost due to noise introduced to the curve through kinetic or thermodynamic effects during labeling. It is also, however, prone to hallucinating insignificant features, so use with extreme caution.</p></body></html>", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"Window Size (must be less than or equal to the number of points in the curve):", None))
        self.groupBox_11.setTitle(QCoreApplication.translate("MainWindow", u"Mutation Search", None))
        self.checkBox_3.setText(QCoreApplication.translate("MainWindow", u"Mutation Search", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Mutation search is used when proteogenomic data is being analyzed and is particularly useful for identifying when mutations contribute to changes in stability. To use this feature, a column labeled &quot;Mutation&quot; must be included in your input files. In this column, peptides with associated mutations must have an entry in the &quot;Mutation&quot; column using the format {reference}{residue-number}{variant} (i.e. G77R). These mutation annotations will be used downstream by visualization tools to highlight mutation-specific trends in the data.</p></body></html>", None))
        self.mainTabWidget.setTabText(self.mainTabWidget.indexOf(self.chalf_tab), QCoreApplication.translate("MainWindow", u"CHalf", None))
        self.qc_checkBox.setText(QCoreApplication.translate("MainWindow", u"Perform Quality Control", None))
        self.groupBox_12.setTitle(QCoreApplication.translate("MainWindow", u"Quality Control Settings", None))
        self.qc_chalf_filters_pushButton.setText(QCoreApplication.translate("MainWindow", u"Import CHalf Filter Options", None))
        self.groupBox_13.setTitle(QCoreApplication.translate("MainWindow", u"Residues to Search", None))
        self.qc_c_checkBox.setText(QCoreApplication.translate("MainWindow", u"C", None))
        self.qc_t_checkBox.setText(QCoreApplication.translate("MainWindow", u"T", None))
        self.qc_h_checkBox.setText(QCoreApplication.translate("MainWindow", u"H", None))
        self.qc_f_checkBox.setText(QCoreApplication.translate("MainWindow", u"F", None))
        self.qc_q_checkBox.setText(QCoreApplication.translate("MainWindow", u"Q", None))
        self.qc_d_checkBox.setText(QCoreApplication.translate("MainWindow", u"D", None))
        self.qc_n_checkBox.setText(QCoreApplication.translate("MainWindow", u"N", None))
        self.qc_k_checkBox.setText(QCoreApplication.translate("MainWindow", u"K", None))
        self.qc_p_checkBox.setText(QCoreApplication.translate("MainWindow", u"P", None))
        self.qc_w_checkBox.setText(QCoreApplication.translate("MainWindow", u"W", None))
        self.qc_e_checkBox.setText(QCoreApplication.translate("MainWindow", u"E", None))
        self.qc_r_checkBox.setText(QCoreApplication.translate("MainWindow", u"R", None))
        self.qc_y_checkBox.setText(QCoreApplication.translate("MainWindow", u"Y", None))
        self.qc_m_checkBox.setText(QCoreApplication.translate("MainWindow", u"M", None))
        self.qc_s_checkBox.setText(QCoreApplication.translate("MainWindow", u"S", None))
        self.qc_g_checkBox.setText(QCoreApplication.translate("MainWindow", u"G", None))
        self.qc_a_checkBox.setText(QCoreApplication.translate("MainWindow", u"A", None))
        self.qc_v_checkBox.setText(QCoreApplication.translate("MainWindow", u"V", None))
        self.qc_l_checkBox.setText(QCoreApplication.translate("MainWindow", u"L", None))
        self.qc_i_checkBox.setText(QCoreApplication.translate("MainWindow", u"I", None))
        self.groupBox_14.setTitle(QCoreApplication.translate("MainWindow", u"Filter Options", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"C\u00bd Minimum:", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"C\u00bd Maximum:", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"R\u00b2 Cutoff:", None))
        self.qc_ci_checkBox.setText(QCoreApplication.translate("MainWindow", u"Confidence Interval / Range Cutoff:", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"Fitting parameter optimization priority:", None))
        self.qc_priority_comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"R\u00b2", None))
        self.qc_priority_comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Confidence Interval", None))

        self.label_36.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Quality Control calculates the fitting and labeling efficiencies of your conditions that can be used to identify the quality of your sample preparation, MS acquistion methods, and analysis workflow. Quality Control can also help you to identify reproducibility between conditions and will generate a report.html file for visualization if selected in the Visualization tab.</p></body></html>", None))
        self.mainTabWidget.setTabText(self.mainTabWidget.indexOf(self.qc_tab), QCoreApplication.translate("MainWindow", u"Quality Control", None))
        self.groupBox_15.setTitle(QCoreApplication.translate("MainWindow", u"Visualization Tools", None))
        self.groupBox_17.setTitle(QCoreApplication.translate("MainWindow", u"Quality Control Report", None))
        self.qc_vis_generate_checkBox.setText(QCoreApplication.translate("MainWindow", u"Generate report.html", None))
        self.qc_vis_open_checkBox.setText(QCoreApplication.translate("MainWindow", u"Open on completion", None))
        self.groupBox_25.setTitle(QCoreApplication.translate("MainWindow", u"Residue Mapper", None))
        self.rm_checkBox.setText(QCoreApplication.translate("MainWindow", u"Residue Mapper", None))
        self.label_46.setText(QCoreApplication.translate("MainWindow", u"File Type:", None))
        self.rm_filetype_comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u".jpg", None))
        self.rm_filetype_comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u".png", None))
        self.rm_filetype_comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u".svg", None))

        self.label_47.setText(QCoreApplication.translate("MainWindow", u"C\u00bd Low Bound:", None))
        self.label_48.setText(QCoreApplication.translate("MainWindow", u"C\u00bd High Bound:", None))
        self.groupBox_26.setTitle(QCoreApplication.translate("MainWindow", u"Trendline Options", None))
        self.rm_trendline_checkBox.setText(QCoreApplication.translate("MainWindow", u"Generate Trendlines", None))
        self.label_49.setText(QCoreApplication.translate("MainWindow", u"Minimum Points:", None))
        self.label_50.setText(QCoreApplication.translate("MainWindow", u"Window Size:", None))
        self.groupBox_27.setTitle(QCoreApplication.translate("MainWindow", u"Other Options", None))
        self.rm_custom_fasta_checkBox.setText(QCoreApplication.translate("MainWindow", u"Mutation search (requires same in CHalf)", None))
        self.label_51.setText(QCoreApplication.translate("MainWindow", u"Advanced Options:", None))
        self.rm_custom_ann_select_pushButton.setText(QCoreApplication.translate("MainWindow", u"Select .ann file", None))
        self.rm_allsites_checkBox.setText(QCoreApplication.translate("MainWindow", u"Labeled and unlabeled curves", None))
        self.rm_stats_reference_checkBox.setText(QCoreApplication.translate("MainWindow", u"Generate reference stats", None))
        self.rm_trendline_stats_checkBox.setText(QCoreApplication.translate("MainWindow", u"Generate trendline stats", None))
        self.groupBox_18.setTitle(QCoreApplication.translate("MainWindow", u"Combined Residue Mapper", None))
        self.crm_checkBox.setText(QCoreApplication.translate("MainWindow", u"Combined Residue Mapper", None))
        self.label_40.setText(QCoreApplication.translate("MainWindow", u"File Type:", None))
        self.crm_filetype_comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u".jpg", None))
        self.crm_filetype_comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u".png", None))
        self.crm_filetype_comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u".svg", None))

        self.label_41.setText(QCoreApplication.translate("MainWindow", u"C\u00bd Low Bound:", None))
        self.label_42.setText(QCoreApplication.translate("MainWindow", u"C\u00bd High Bound:", None))
        self.groupBox_23.setTitle(QCoreApplication.translate("MainWindow", u"Trendline Options", None))
        self.crm_trendline_checkBox.setText(QCoreApplication.translate("MainWindow", u"Generate Trendlines", None))
        self.label_43.setText(QCoreApplication.translate("MainWindow", u"Minimum Points:", None))
        self.label_44.setText(QCoreApplication.translate("MainWindow", u"Window Size:", None))
        self.groupBox_24.setTitle(QCoreApplication.translate("MainWindow", u"Other Options", None))
        self.crm_custom_fasta_checkBox.setText(QCoreApplication.translate("MainWindow", u"Mutation search (requires same in CHalf)", None))
        self.crm_allsites_checkBox.setText(QCoreApplication.translate("MainWindow", u"Labeled and unlabeled curves", None))
        self.crm_trendline_stats_checkBox.setText(QCoreApplication.translate("MainWindow", u"Generate trendline stats", None))
        self.crm_shared_only_checkBox.setText(QCoreApplication.translate("MainWindow", u"Shared curves only", None))
        self.crm_stats_reference_checkBox.setText(QCoreApplication.translate("MainWindow", u"Generate reference stats", None))
        self.label_45.setText(QCoreApplication.translate("MainWindow", u"Advanced Options:", None))
        self.crm_custom_ann_select_pushButton.setText(QCoreApplication.translate("MainWindow", u"Select .ann file", None))
        self.groupBox_21.setTitle(QCoreApplication.translate("MainWindow", u"Delta Mapper", None))
        self.crm_checkBox_3.setText(QCoreApplication.translate("MainWindow", u"Delta Mapper", None))
        self.label_52.setText(QCoreApplication.translate("MainWindow", u"File Type:", None))
        self.dm_filetype_comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u".jpg", None))
        self.dm_filetype_comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u".png", None))
        self.dm_filetype_comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u".svg", None))

        self.label_53.setText(QCoreApplication.translate("MainWindow", u"\u0394C\u00bd Low Bound:", None))
        self.label_54.setText(QCoreApplication.translate("MainWindow", u"\u0394C\u00bd High Bound:", None))
        self.groupBox_28.setTitle(QCoreApplication.translate("MainWindow", u"Trendline Options", None))
        self.dm_trendline_checkBox.setText(QCoreApplication.translate("MainWindow", u"Generate Trendlines", None))
        self.label_55.setText(QCoreApplication.translate("MainWindow", u"Minimum Points:", None))
        self.label_56.setText(QCoreApplication.translate("MainWindow", u"Window Size:", None))
        self.groupBox_20.setTitle(QCoreApplication.translate("MainWindow", u"KDE Options", None))
        self.label_37.setText(QCoreApplication.translate("MainWindow", u"Minimum Points:", None))
        self.dm_kde_sig_cutoff_checkBox.setText(QCoreApplication.translate("MainWindow", u"Signficance cutoff:", None))
        self.groupBox_29.setTitle(QCoreApplication.translate("MainWindow", u"Other Options", None))
        self.dm_trendline_stats_checkBox.setText(QCoreApplication.translate("MainWindow", u"Generate trendline stats", None))
        self.label_57.setText(QCoreApplication.translate("MainWindow", u"Advanced Options:", None))
        self.dm_custom_ann_select_pushButton.setText(QCoreApplication.translate("MainWindow", u"Select .ann file", None))
        self.dm_allsites_checkBox.setText(QCoreApplication.translate("MainWindow", u"Labeled and unlabeled curves", None))
        self.dm_stats_reference_checkBox.setText(QCoreApplication.translate("MainWindow", u"Generate reference stats", None))
        self.dm_custom_fasta_checkBox.setText(QCoreApplication.translate("MainWindow", u"Mutation search (requires same in CHalf)", None))
        self.groupBox_19.setTitle(QCoreApplication.translate("MainWindow", u"Combined Site", None))
        self.cs_checkBox.setText(QCoreApplication.translate("MainWindow", u"Combined Site", None))
        self.label_60.setText(QCoreApplication.translate("MainWindow", u"File Type:", None))
        self.cs_filetype_comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u".jpg", None))
        self.cs_filetype_comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u".png", None))
        self.cs_filetype_comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u".svg", None))

        self.label_59.setText(QCoreApplication.translate("MainWindow", u"C\u00bd Low Bound:", None))
        self.label_58.setText(QCoreApplication.translate("MainWindow", u"C\u00bd High Bound:", None))
        self.groupBox_16.setTitle(QCoreApplication.translate("MainWindow", u"Conditions", None))
        ___qtablewidgetitem6 = self.visaulization_tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Condition", None));
        ___qtablewidgetitem7 = self.visaulization_tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"Group", None));
        ___qtablewidgetitem8 = self.visaulization_tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"Class", None));
        ___qtablewidgetitem9 = self.visaulization_tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"Color", None));
        self.groupBox_22.setTitle(QCoreApplication.translate("MainWindow", u"Condition/Group Properties", None))
        self.vis_add_pushButton.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.vis_add_all_pushButton.setText(QCoreApplication.translate("MainWindow", u"Add All", None))
        self.vis_remove_pushButton.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
        self.vis_remove_all_pushButton.setText(QCoreApplication.translate("MainWindow", u"Remove All", None))
        self.vis_set_group_pushButton.setText(QCoreApplication.translate("MainWindow", u"Set Group", None))
        self.vis_set_ref_pushButton.setText(QCoreApplication.translate("MainWindow", u"Set Reference", None))
        self.vis_set_exp_pushButton.setText(QCoreApplication.translate("MainWindow", u"Set Experimental", None))
        self.vis_set_color_pushButton.setText(QCoreApplication.translate("MainWindow", u"Set Color", None))
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"Visualization tools will be performed group-wise. Comparisons will be made between conditions in the group between the classes \"reference\" and \"experimental.\" Each group must have only one reference condition, and the rest will be experimental. Each condition in a group must also have a unique color assigned. A condition can be part of multiple groups if added multiple times.", None))
        self.mainTabWidget.setTabText(self.mainTabWidget.indexOf(self.visualization_tab), QCoreApplication.translate("MainWindow", u"Visualization", None))
        self.label_38.setText(QCoreApplication.translate("MainWindow", u"Output directory:", None))
        self.run_browse_pushButton.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.run_open_pushButton.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.run_start_pushButton.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.run_stop_pushButton.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.run_log_export_pushButton.setText(QCoreApplication.translate("MainWindow", u"Export Log", None))
        self.run_log_clear_pushButton.setText(QCoreApplication.translate("MainWindow", u"Clear Log", None))
        self.groupBox_30.setTitle(QCoreApplication.translate("MainWindow", u"Log", None))
        self.mainTabWidget.setTabText(self.mainTabWidget.indexOf(self.run_tab), QCoreApplication.translate("MainWindow", u"Run", None))
    # retranslateUi

