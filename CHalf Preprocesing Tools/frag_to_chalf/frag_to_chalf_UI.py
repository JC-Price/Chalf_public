# -*- coding: utf-8 -*-
"""
Created on Sat Aug  9 15:34:43 2025

@author: chadhyer
"""

import sys
import os
import csv
import subprocess
import pandas as pd
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QFileDialog,
    QLineEdit, QLabel, QGroupBox, QCheckBox, QComboBox, QMessageBox, QHeaderView,
    QTextEdit, QProgressBar
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QColor, QPalette, QIcon

def custom_fasta_extract(row,quan=False):
    protID = row['Protein ID']
    if ';' in protID:
        newID, mut, loc = protID.split(';')
        if not quan:
            newStart, newEnd = [int(x) for x in loc.split('-')]
            newEN = row['Entry Name'].split(';')[0]
            row['Start'] = newStart
            row['End'] = newEnd
            row['Entry Name'] = newEN
        row['Protein Description'] = f'{newID}_{mut}'
        row['Mutation'] = mut
        row['Protein ID'] = newID
    else:
        row['Mutation'] = ''
    return row

def DDA_custom_fasta_extract(row,quan=False):
    protID = row['Protein Accession']
    if ';' in protID:
        newID, mut, loc = protID.split(';')
        if not quan:
            newStart, newEnd = [int(x) for x in loc.split('-')]
            row['Start'] = newStart
            row['End'] = newEnd
        row['Mutation'] = mut
        row['Protein Accession'] = newID
    else:
        row['Mutation'] = ''
    return row

def DDA(name,source,outdir,custom_fasta):
    try:
        ptm_dict = {
            '+15.9949' : '+15.99',
            '+31.9898' : '+31.99',
            '+47.9847' : '+47.98',
            '+-17.0265' : '-17.03',
            '+125.8966' : '+125.90',
            '+251.7933' : '+251.79',
            '+57.0215' : '+57.02'
            }
        file = f'{source}/combined_modified_peptide.tsv'
        
        # Check if the file exists before attempting to read it
        if not os.path.exists(file):
            raise FileNotFoundError(f"DDA file not found: {file}")

        df = pd.read_csv(file,delimiter='\t')
        points = [col for col in df.columns if 'Intensity' in col and 'Max' not in col]
        
        pepDF=pd.DataFrame()
        pepDF['Protein Accession'] = df['Protein'].str.replace('sp|','')
        pepDF['Peptide'] = df['Modified Sequence'].str.replace('[','(+').str.replace(']',')')
        for ptm in ptm_dict:
            repl = ptm_dict[ptm]
            pepDF['Peptide'] = pepDF['Peptide'].str.replace(ptm,repl,regex=False)
        pepDF[points] = df[points]
        pepDF[['Start','End']] = df[['Start','End']]
        renamed = [int(col.replace(f'{name}_','').replace(' Intensity','')) for col in points]
        pepDF.rename(columns=dict(zip(points,renamed)),inplace=True)
        protDF = pd.DataFrame()
        protDF['Description'] = df['Protein Description']
        protDF['Accession'] = df['Protein'].str.replace('sp\|','')
        protDF.drop_duplicates(inplace=True)
        if custom_fasta:
            pepDF = pepDF.apply(DDA_custom_fasta_extract,axis=1)
        pepDF.to_csv(f'{outdir}/{name}.csv',index=False)
    except Exception as e:
        print(f"Error in DDA conversion: {e}", file=sys.stderr)
        raise e  # Re-raise the exception after logging

def DIA(name,source,outdir,custom_fasta):
    try:
        ptm_dict = {
            'UniMod:35' : '+15.99',
            'UniMod:425' : '+31.99',
            'UniMod:1327' : '+31.99',
            'UniMod:345' : '+47.98',
            'UniMod:28' : '-17.03',
            'UniMod:129' : '+125.90',
            'UniMod:130' : '+251.79',
            }
        
        pep_file = f'{source}/peptide.tsv'
        quant_file = f'{source}/diann-output/report.pr_matrix.tsv'

        # Check if files exist
        if not os.path.exists(pep_file):
            raise FileNotFoundError(f"Peptide file not found: {pep_file}")
        if not os.path.exists(quant_file):
            raise FileNotFoundError(f"Quantification file not found: {quant_file}")
        
        pepDF = pd.read_csv(pep_file,delimiter='\t')
        quanDF = pd.read_csv(quant_file,delimiter='\t')
        
        conc_cols = [col for col in quanDF.columns if '\\' in col]
        conc_list = [int(conc.split('\\')[-1].split('-')[-1][0]) for conc in conc_cols]
        conc_dict = dict(zip(conc_cols,conc_list))
        
        quanDF.rename(columns={'Protein.Ids':'Protein ID','Modified.Sequence':'Modified Peptide','Stripped.Sequence':'Peptide'},inplace=True)
        pepDF.rename(columns={'Protein Start':'Start','Protein End':'End'},inplace=True)
        if custom_fasta:
            pepDF = pepDF.apply(custom_fasta_extract,axis=1)
        pepDF['Protein Accession'] = pepDF['Protein ID'] + '|' + pepDF['Entry Name']
        if custom_fasta: pepDF = pepDF[['Protein ID','Protein Accession','Protein Description','Peptide','Start','End','Mutation']]
        else: pepDF = pepDF[['Protein ID','Protein Accession','Protein Description','Peptide','Start','End']]
        cols = [col for col in quanDF if '\\' in col]
        if custom_fasta: 
            quanDF = quanDF.apply(custom_fasta_extract,quan=True,axis=1)
            quanDF = quanDF[['Protein ID','Peptide','Modified Peptide','Mutation']+cols]
            quanDF = quanDF.merge(pepDF,how='left',on=['Protein ID','Peptide','Mutation'])
            quanDF = quanDF.groupby(by=['Protein ID', 'Peptide', 'Modified Peptide','Protein Accession', 'Protein Description', 'Start', 'End','Mutation']).sum().reset_index()

        else:
            quanDF = quanDF[['Protein ID','Peptide','Modified Peptide']+cols]
            quanDF = quanDF.merge(pepDF,how='left',on=['Protein ID','Peptide'])
            quanDF = quanDF.groupby(by=['Protein ID', 'Peptide', 'Modified Peptide','Protein Accession', 'Protein Description', 'Start', 'End']).sum().reset_index()

        quanDF[cols] = quanDF[cols].fillna(0)
        
        for ptm in ptm_dict:
            quanDF['Modified Peptide'] = quanDF['Modified Peptide'].str.replace(ptm,ptm_dict[ptm])
        quanDF.rename(columns=conc_dict,inplace=True)
        concentrations = list(conc_dict.values())
        concentrations.sort()
        if custom_fasta: prot_pep = quanDF[['Protein Accession','Modified Peptide']+concentrations+['Start','End','Mutation']].rename(columns={'Modified Peptide':'Peptide'})
        else: prot_pep = quanDF[['Protein Accession','Modified Peptide']+concentrations+['Start','End']].rename(columns={'Modified Peptide':'Peptide'})
        prot_pep = prot_pep.rename(columns=conc_dict)
        prot = quanDF[['Protein Description','Protein Accession']].rename(columns={'Protein Description':'Description','Protein Accession':'Accession'})
        prot = prot.drop_duplicates()
        prot_pep['Peptide'] = prot_pep['Peptide'].str.replace(':','|')
        prot_pep.to_csv(f'{outdir}/{name}.csv',index=False)
        return pepDF, quanDF, prot, prot_pep
    except Exception as e:
        print(f"Error in DIA conversion: {e}", file=sys.stderr)
        raise e  # Re-raise the exception after logging

def frag_to_chalf(method,name,source,outdir,custom_fasta):
    if method == 'DDA':
        DDA(name,source,outdir,custom_fasta)
    elif method == 'DIA':
        DIA(name,source,outdir,custom_fasta)
    else:
        print('Non-standard method specified. CHalf Analysis could not be run.')



class FragPipeWorker(QThread):
    """
    A worker thread to run the fragpipe command in the background.
    """
    # Custom signals for real-time output and completion notification
    output_signal = Signal(str)
    finished_signal = Signal(int)

    def __init__(self, command, log_file_path):
        super().__init__()
        self.command = command
        self.log_file_path = log_file_path

    def run(self):
        """
        Executes the fragpipe command and redirects output to a log file and a signal.
        """
        self.output_signal.emit(f'Command to run: {self.command}')
        try:
            # Open log file for writing
            with open(self.log_file_path, 'w') as log_file:
                # Use subprocess.Popen to run the command asynchronously
                process = subprocess.Popen(
                    self.command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,  # Redirect stderr to stdout
                    text=True,
                    universal_newlines=True,
                    bufsize=1
                )

                # Read output line by line, write to log file, and emit signal
                for line in iter(process.stdout.readline, ''):
                    log_file.write(line)
                    self.output_signal.emit(line.strip())
                
                # Wait for the process to finish
                process.stdout.close()
                return_code = process.wait()

                # Emit finished signal with the return code
                self.finished_signal.emit(return_code)

        except FileNotFoundError:
            self.output_signal.emit(f"Error: Command not found. Check if fragpipe.exe is in the correct directory.")
            self.finished_signal.emit(1)
        except Exception as e:
            self.output_signal.emit(f"An error occurred: {e}")
            self.finished_signal.emit(1)


class FragPipeManifestCreator(QMainWindow):
    """
    A PySide6 GUI application for creating a FragPipe .fp-manifest file.
    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle("FragToCHalf")
        self.setGeometry(100, 100, 1000, 600)

        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # --- Table Section ---
        self.table_group = QGroupBox("Input Files")
        self.table_layout = QVBoxLayout()
        self.table_group.setLayout(self.table_layout)

        self.file_table = QTableWidget()
        self.file_table.setColumnCount(3)
        self.file_table.setHorizontalHeaderLabels(["File", "Point", "Acquisition Method"])
        self.file_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.file_table.setSelectionMode(QTableWidget.SelectionMode.ExtendedSelection)
        
        # Adjusting column sizes
        header = self.file_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # "File" column stretches
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents) # "Point" resizes to content
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents) # "Acquisition Method" resizes to content
        
        self.table_layout.addWidget(self.file_table)

        self.file_buttons_layout = QHBoxLayout()
        self.select_files_btn = QPushButton("Select Raw Files")
        self.select_files_btn.clicked.connect(self.select_raw_files)
        
        self.remove_files_btn = QPushButton("Remove Selected")
        self.remove_files_btn.clicked.connect(self.remove_selected_rows)

        self.set_dia_btn = QPushButton("Set to DIA")
        self.set_dia_btn.clicked.connect(lambda: self.set_acquisition_method("DIA"))
        
        self.set_dda_btn = QPushButton("Set to DDA")
        self.set_dda_btn.clicked.connect(lambda: self.set_acquisition_method("DDA"))

        self.file_buttons_layout.addWidget(self.select_files_btn)
        self.file_buttons_layout.addWidget(self.remove_files_btn)
        self.file_buttons_layout.addStretch() # Adds a spacer
        self.file_buttons_layout.addWidget(self.set_dia_btn)
        self.file_buttons_layout.addWidget(self.set_dda_btn)

        self.table_layout.addLayout(self.file_buttons_layout)

        self.main_layout.addWidget(self.table_group)

        # --- Analysis Settings Section ---
        self.settings_group = QGroupBox("Analysis Settings")
        self.settings_layout = QVBoxLayout()
        self.settings_group.setLayout(self.settings_layout)

        # Condition Name
        self.condition_layout = QHBoxLayout()
        self.condition_label = QLabel("Condition Name:")
        self.condition_edit = QLineEdit()
        self.condition_edit.setPlaceholderText("e.g., C1")
        self.condition_layout.addWidget(self.condition_label)
        self.condition_layout.addWidget(self.condition_edit)
        self.settings_layout.addLayout(self.condition_layout)
        
        # Output Directory
        self.output_layout = QHBoxLayout()
        self.output_label = QLabel("Output Directory:")
        self.output_edit = QLineEdit()
        self.output_edit.setReadOnly(True)
        self.select_output_btn = QPushButton("Select")
        self.select_output_btn.clicked.connect(self.select_output_directory)
        self.output_layout.addWidget(self.output_label)
        self.output_layout.addWidget(self.output_edit)
        self.output_layout.addWidget(self.select_output_btn)
        self.settings_layout.addLayout(self.output_layout)

        # Method Dropdown (Dropdown menu will draw from the workflows folder)
        self.method_layout = QHBoxLayout()
        self.method_label = QLabel("Method:")
        self.method_combo = QComboBox()
        self.load_workflows()
        self.method_layout.addWidget(self.method_label)
        self.method_layout.addWidget(self.method_combo)
        self.settings_layout.addLayout(self.method_layout)
        
        # Custom FASTA Checkbox and Line Edit
        self.fasta_layout = QHBoxLayout()
        self.fasta_checkbox = QCheckBox("Custom FASTA")
        self.fasta_edit = QLineEdit()
        self.fasta_edit.setReadOnly(True)
        self.fasta_edit.setEnabled(False) # Initially disabled
        self.fasta_browse_btn = QPushButton("Browse")
        self.fasta_browse_btn.setEnabled(False) # Initially disabled
        
        self.fasta_checkbox.toggled.connect(self.fasta_edit.setEnabled)
        self.fasta_checkbox.toggled.connect(self.fasta_browse_btn.setEnabled)
        self.fasta_browse_btn.clicked.connect(self.select_fasta_file)
        
        self.fasta_layout.addWidget(self.fasta_checkbox)
        self.fasta_layout.addWidget(self.fasta_edit)
        self.fasta_layout.addWidget(self.fasta_browse_btn)
        self.settings_layout.addLayout(self.fasta_layout)

        self.main_layout.addWidget(self.settings_group)
        
        # --- Terminal Output Section ---
        self.terminal_group = QGroupBox("FragPipe Output")
        self.terminal_layout = QVBoxLayout()
        self.terminal_group.setLayout(self.terminal_layout)
        self.output_terminal = QTextEdit()
        self.output_terminal.setReadOnly(True)
        self.terminal_layout.addWidget(self.output_terminal)
        self.main_layout.addWidget(self.terminal_group)

        # --- Run and Open Buttons ---
        self.button_layout = QHBoxLayout()
        self.run_btn = QPushButton("Run")
        self.run_btn.clicked.connect(self.run_analysis)
        self.open_output_btn = QPushButton("Open Output Directory")
        self.open_output_btn.clicked.connect(self.open_output_directory)
        self.run_existing_project_btn = QPushButton("Run on Existing Project")
        self.run_existing_project_btn.clicked.connect(self.run_on_existing_project)
        self.button_layout.addWidget(self.run_btn)
        self.button_layout.addWidget(self.open_output_btn)
        self.button_layout.addWidget(self.run_existing_project_btn)
        self.main_layout.addLayout(self.button_layout)
        
        # Initialize worker thread variable
        self.fragpipe_worker = None
        
    def run_on_existing_project(self):
        """
        Runs frag_to_chalf on an existing FragPipe project directory.
        """
        # Get project directory from a file dialog
        project_dir = QFileDialog.getExistingDirectory(self, "Select Existing FragPipe Project Directory")
        if not project_dir:
            return
    
        # Check for the manifest file to determine project name and method
        manifest_files = [f for f in os.listdir(project_dir) if f.endswith('.fp-manifest')]
        if not manifest_files:
            QMessageBox.critical(self, "Error", "No .fp-manifest file found in the selected directory.")
            return
    
        manifest_path = os.path.join(project_dir, manifest_files[0])
        read_manifest = pd.read_csv(manifest_path,header=None,sep='\t')
        condition_name = read_manifest.loc[0][1]
    
        # Read the manifest to get the acquisition method
        try:
            with open(manifest_path, 'r') as f:
                reader = csv.reader(f, delimiter='\t')
                # Skip header
                next(reader) 
                first_row = next(reader)
                method = first_row[3]
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to read manifest file: {e}")
            return
        
        # Get other settings from the UI
        custom_fasta = self.fasta_checkbox.isChecked()
        
        self.output_terminal.append(f"Found project '{condition_name}' with method '{method}'.")
        self.output_terminal.append(f"Running frag_to_chalf on existing project at: {project_dir}")
        outdir = self.output_edit.text().strip()
        if not outdir:
            self.log_message("Please select an Output Directory first.", is_error=True)
            return
        try:
            # The output directory for the CSVs will be the project directory itself
            print(method, condition_name, project_dir, outdir, custom_fasta)
            frag_to_chalf(method, condition_name, project_dir, outdir, custom_fasta) #method,name,source,outdir,custom_fasta
            self.output_terminal.append("frag_to_chalf completed successfully.")
            QMessageBox.information(self, "Success", "frag_to_chalf finished.")
        except Exception as e:
            self.output_terminal.append(f"Error during frag_to_chalf run: {e}")
            QMessageBox.critical(self, "Error", f"frag_to_chalf failed with error: {e}")
    
    def log_message(self, message, is_error=False):
        """Helper function to log messages to the terminal."""
        if is_error:
            self.output_terminal.append(f"<span style='color:red;'>ERROR: {message}</span>")
        else:
            self.output_terminal.append(f"INFO: {message}")

    def load_workflows(self):
        """
        Populates the 'Method' dropdown with .workflow files from a 'workflows' folder.
        If the folder doesn't exist, it creates it and a dummy file for demonstration.
        """
        try:
            # Get the path of the current script's directory
            script_dir = os.getcwd()#os.path.dirname(os.path.abspath(__file__))
            workflows_dir = os.path.join(script_dir, "workflows")
            
            # Create workflows directory if it doesn't exist, and add a dummy file
            if not os.path.exists(workflows_dir):
                os.makedirs(workflows_dir)
                with open(os.path.join(workflows_dir, "default.workflow"), "w") as f:
                    f.write("# Dummy workflow file for demonstration")
            
            # Load workflow files from the directory
            if os.path.isdir(workflows_dir):
                for filename in os.listdir(workflows_dir):
                    if filename.endswith(".workflow"):
                        # Add filename without extension to the dropdown
                        self.method_combo.addItem(os.path.splitext(filename)[0])
        except Exception as e:
            self.log_message(f"Could not load workflows: {e}", is_error=True)

    def select_raw_files(self):
        """Opens a file dialog to select raw files and populates the table."""
        try:
            file_paths, _ = QFileDialog.getOpenFileNames(self, "Select Raw Files", "", "Raw Files (*.raw *.mzML);;All Files (*)")
            if file_paths:
                current_row_count = self.file_table.rowCount()
                self.file_table.setRowCount(current_row_count + len(file_paths))
                
                for i, file_path in enumerate(file_paths):
                    row = current_row_count + i
                    # Populate the "File" column with the full path, ensuring correct path separator
                    item = QTableWidgetItem(file_path)
                    item.setFlags(item.flags() ^ Qt.ItemIsEditable) # Make "File" column non-editable
                    self.file_table.setItem(row, 0, item)
                    
                    # Automatically assign the point number
                    self.file_table.setItem(row, 1, QTableWidgetItem(str(row)))

                    # Leave "Acquisition Method" empty for manual input
                    self.file_table.setItem(row, 2, QTableWidgetItem(""))
        except Exception as e:
            self.log_message(f"Error selecting files: {e}", is_error=True)

    def remove_selected_rows(self):
        """Removes the selected rows from the table."""
        try:
            # Get selected rows and sort them in descending order to avoid index issues
            selected_rows = sorted(list(set(index.row() for index in self.file_table.selectedIndexes())), reverse=True)
            for row in selected_rows:
                self.file_table.removeRow(row)
        except Exception as e:
            self.log_message(f"Error removing rows: {e}", is_error=True)

    def set_acquisition_method(self, method):
        """
        Sets the 'Acquisition Method' for all selected rows.
        If no rows are selected, it sets the method for all rows in the table.
        """
        try:
            selected_rows = list(set(index.row() for index in self.file_table.selectedIndexes()))
            
            if not selected_rows:
                for row in range(self.file_table.rowCount()):
                    self.file_table.setItem(row, 2, QTableWidgetItem(method))
            else:
                for row in selected_rows:
                    self.file_table.setItem(row, 2, QTableWidgetItem(method))
        except Exception as e:
            self.log_message(f"Error setting acquisition method: {e}", is_error=True)

    def select_output_directory(self):
        """Opens a directory dialog and updates the output directory line edit."""
        try:
            output_dir = QFileDialog.getExistingDirectory(self, "Select Output Directory")
            if output_dir:
                self.output_edit.setText(output_dir)
        except Exception as e:
            self.log_message(f"Error selecting output directory: {e}", is_error=True)

    def select_fasta_file(self):
        """Opens a file dialog to select a FASTA file and updates the line edit."""
        try:
            fasta_file, _ = QFileDialog.getOpenFileName(self, "Select FASTA File", "", "FASTA Files (*.fasta *.fa *.fas);;All Files (*)")
            if fasta_file:
                self.fasta_edit.setText(fasta_file)
        except Exception as e:
            self.log_message(f"Error selecting FASTA file: {e}", is_error=True)

    def update_workflow_with_fasta(self, workflow_path, fasta_path, output_path):
        """
        Reads a workflow file, updates the database.db-path with a custom FASTA path,
        and saves the modified workflow to a new file.
        """
        try:
            with open(workflow_path, 'r') as f_in:
                lines = f_in.readlines()
            
            with open(output_path, 'w') as f_out:
                for line in lines:
                    # Check for the database.db-path line and replace it
                    if line.strip().startswith('database.db-path='):
                        # Ensure the path uses correct double backslashes
                        f_out.write(f"database.db-path={fasta_path.replace('/', '\\\\')}\n")
                    else:
                        f_out.write(line)
            return True
        except Exception as e:
            self.log_message(f"An error occurred while updating the workflow file: {e}", is_error=True)
            return False

    def copy_workflow_file(self, source_path, destination_path):
        """
        Copies a workflow file from source to destination.
        """
        try:
            with open(source_path, 'r') as f_in:
                lines = f_in.readlines()
            
            with open(destination_path, 'w') as f_out:
                f_out.writelines(lines)
            return True
        except Exception as e:
            self.log_message(f"An error occurred while copying the workflow file: {e}", is_error=True)
            return False
            
    def open_output_directory(self):
        """Opens the selected output directory in the system's file explorer."""
        try:
            output_dir = self.output_edit.text().strip()
            if not output_dir:
                self.log_message("Please select an Output Directory first.", is_error=True)
                return

            if not os.path.isdir(output_dir):
                self.log_message("The selected directory does not exist.", is_error=True)
                return

            if sys.platform == "win32":
                os.startfile(output_dir)
            elif sys.platform == "darwin":  # macOS
                subprocess.Popen(["open", output_dir])
            else:  # linux
                subprocess.Popen(["xdg-open", output_dir])
        except Exception as e:
            self.log_message(f"Could not open directory: {e}", is_error=True)

    def run_analysis(self):
        """
        Gathers data from the GUI, performs validation, and generates the .fp-manifest file
        and the updated .workflow file. It then starts a new thread to run fragpipe.
        """
        self.output_terminal.clear()
        
        # Get user inputs
        condition_name = self.condition_edit.text().strip()
        output_dir = self.output_edit.text().strip()
        
        # Basic validation
        if not condition_name:
            self.log_message("Please enter a Condition Name.", is_error=True)
            QMessageBox.critical(self, "Input Error", "Please enter a Condition Name.")
            return
        if not output_dir:
            self.log_message("Please select an Output Directory.", is_error=True)
            QMessageBox.critical(self, "Input Error", "Please select an Output Directory.")
            return
        if self.file_table.rowCount() == 0:
            self.log_message("Please select at least one raw file.", is_error=True)
            QMessageBox.critical(self, "Input Error", "Please select at least one raw file.")
            return

        # Perform table data validation
        for row in range(self.file_table.rowCount()):
            file_item = self.file_table.item(row, 0)
            point_item = self.file_table.item(row, 1)
            method_item = self.file_table.item(row, 2)
            
            # Validate file paths for spaces
            file_path = file_item.text() if file_item else ""
            if " " in file_path:
                self.log_message(f"File path in row {row + 1} contains spaces. Please correct the file path: {file_path}", is_error=True)
                QMessageBox.critical(self, "Input Error", f"File path in row {row + 1} contains spaces. Please correct the file path.")
                return

            # Validate 'Point' column
            if point_item:
                point_text = point_item.text().strip()
                try:
                    int(point_text)
                except ValueError:
                    self.log_message(f"Point value '{point_text}' in row {row + 1} is not a valid integer.", is_error=True)
                    QMessageBox.critical(self, "Input Error", f"Point value in row {row + 1} is not a valid integer.")
                    return
            else:
                self.log_message(f"Point value in row {row + 1} is missing.", is_error=True)
                QMessageBox.critical(self, "Input Error", f"Point value in row {row + 1} is missing.")
                return

            # Validate 'Acquisition Method' column
            if method_item:
                method_text = method_item.text().strip().upper()
                if method_text and method_text not in ["DIA", "DDA"]:
                    self.log_message(f"Acquisition Method '{method_text}' in row {row + 1} must be either 'DIA' or 'DDA' (or blank).", is_error=True)
                    QMessageBox.critical(self, "Input Error", f"Acquisition Method in row {row + 1} is invalid.")
                    return
            
        # --- Handle workflow and manifest file creation ---
        selected_workflow_name = self.method_combo.currentText()
        script_dir = os.getcwd()#os.path.dirname(os.path.abspath(__file__))
        original_workflow_path = os.path.join(script_dir, "workflows", f"{selected_workflow_name}.workflow")
        final_workflow_path = os.path.join(output_dir, f"{condition_name}.workflow")
        
        custom_fasta_used = self.fasta_checkbox.isChecked()
        if custom_fasta_used:
            fasta_file = self.fasta_edit.text().strip()
            if not fasta_file:
                self.log_message("Please select a custom FASTA file.", is_error=True)
                QMessageBox.critical(self, "Input Error", "Please select a custom FASTA file.")
                return
            # Validate custom FASTA path for spaces
            if " " in fasta_file:
                self.log_message(f"The custom FASTA file path contains spaces. Please correct the file path: {fasta_file}", is_error=True)
                QMessageBox.critical(self, "Input Error", "The custom FASTA file path contains spaces.")
                return
            if not self.update_workflow_with_fasta(original_workflow_path, fasta_file, final_workflow_path):
                return
        else:
            if not self.copy_workflow_file(original_workflow_path, final_workflow_path):
                return
        
        # Prepare the manifest output file path
        output_filepath = os.path.join(output_dir, f"{condition_name}.fp-manifest")

        # Get data from the table
        manifest_data = []
        for row in range(self.file_table.rowCount()):
            file_item = self.file_table.item(row, 0)
            point_item = self.file_table.item(row, 1)
            method_item = self.file_table.item(row, 2)
            
            # Use empty strings if items are not set to avoid errors
            file_path = file_item.text() if file_item else ""
            point = point_item.text() if point_item else ""
            acq_method = method_item.text() if method_item else ""

            # The output format is: File, Condition, Point, Acquisition Method
            # Ensure file paths use backslashes
            formatted_file_path = file_path.replace("/", "\\\\")
            manifest_data.append([formatted_file_path, condition_name, point, acq_method])

        # Write the data to the .fp-manifest file
        try:
            with open(output_filepath, 'w', newline='') as f:
                writer = csv.writer(f, delimiter='\t')
                writer.writerows(manifest_data)
        except Exception as e:
            self.log_message(f"An error occurred while saving the manifest file: {e}", is_error=True)
            QMessageBox.critical(self, "Error", f"Could not save manifest file:\n{e}")
            return
            
        # --- Run FragPipe in a separate thread ---
        # Get relative path to fragpipe/bin
        script_dir = os.getcwd()#os.path.dirname(os.path.abspath(__file__))
        fragpipe_dir = os.path.join(script_dir, "fragpipe", "bin")
        fragpipe_bat_path = os.path.join(fragpipe_dir, "fragpipe.exe")

        # Create the working directory for fragpipe
        fragpipe_workdir = os.path.join(output_dir, f"{condition_name}_FP")
        os.makedirs(fragpipe_workdir, exist_ok=True)
        
        # Build the command
        command_list = [
            fragpipe_bat_path,
            "--headless",
            "--workflow", final_workflow_path.replace("/", "\\\\"),
            "--manifest", output_filepath.replace("/", "\\\\"),
            "--workdir", fragpipe_workdir.replace("/", "\\\\"),
            "--config-tools-folder", os.path.join(script_dir, "fragpipe", "tools").replace("/", "\\\\")
        ]
        
        self.log_message("Validation successful. Starting FragPipe analysis...")
        
        # Prepare log file path
        log_file_path = os.path.join(output_dir, f"{condition_name}.log")

        # Store parameters for post-analysis
        self.fragpipe_params = {
            'condition_name': condition_name,
            'output_dir': output_dir,
            'fragpipe_workdir': fragpipe_workdir,
            'custom_fasta_used': custom_fasta_used
        }

        # Create and start the worker thread
        self.fragpipe_worker = FragPipeWorker(command_list, log_file_path)
        self.fragpipe_worker.output_signal.connect(self.handle_fragpipe_output)
        self.fragpipe_worker.finished_signal.connect(self.handle_fragpipe_finished)
        self.fragpipe_worker.start()

    def handle_fragpipe_output(self, line):
        """Slot to receive and display real-time output from the worker thread."""
        self.output_terminal.append(line)

    def handle_fragpipe_finished(self, return_code):
        """
        Slot to handle the completion of the worker thread.
        It checks for output files and runs frag_to_chalf.
        """
        if return_code != 0:
            self.log_message(f"FragPipe analysis failed with return code: {return_code}. Check the log file for details.", is_error=True)
            QMessageBox.critical(self, "FragPipe Error", f"FragPipe analysis failed. See the log output for details.")
            return

        # FragPipe finished successfully, now attempt the conversion
        self.log_message("FragPipe analysis has finished successfully. Starting file conversion...")

        try:
            condition_name = self.fragpipe_params['condition_name']
            output_dir = self.fragpipe_params['output_dir']
            fragpipe_workdir = self.fragpipe_params['fragpipe_workdir']
            custom_fasta_used = self.fragpipe_params['custom_fasta_used']

            dda_file = os.path.join(fragpipe_workdir, "combined_modified_peptide.tsv")
            dia_file = os.path.join(fragpipe_workdir, "diann-output", "report.pr_matrix.tsv")
            
            if os.path.exists(dda_file):
                self.log_message("DDA output found. Running frag_to_chalf.")
                frag_to_chalf('DDA', condition_name, fragpipe_workdir, output_dir, custom_fasta_used)
            elif os.path.exists(dia_file):
                self.log_message("DIA output found. Running frag_to_chalf.")
                frag_to_chalf('DIA', condition_name, fragpipe_workdir, output_dir, custom_fasta_used)
            else:
                raise FileNotFoundError("Neither 'combined_modified_peptide.tsv' nor 'report.pr_matrix.tsv' was found. Conversion cannot be made.")

            self.log_message("All tasks completed successfully!", is_error=False)
            QMessageBox.information(self, "Success", "All analysis and file conversions are complete.")

        except Exception as e:
            self.log_message(f"An error occurred during file conversion: {e}", is_error=True)
            QMessageBox.critical(self, "Conversion Error", f"An error occurred during the final file conversion step:\n{e}")

if __name__ == "__main__":
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    else:
        print('QApplication instance already exists: %s' % str(app))
    app.setStyle("fusion")
    
    # Create a palette and set the desired colors for light mode
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(240, 240, 240))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 220))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.ColorRole.Link, QColor(0, 0, 255))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 120, 215))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    # Disabled color group (for deactivated objects)
    disabled_color = QColor(180, 180, 180) # A light gray color for disabled elements
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, QColor(220, 220, 220))
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, disabled_color)
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, QColor(235, 235, 235))
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.AlternateBase, QColor(220, 220, 220))
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ToolTipBase, QColor(255, 255, 220))
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ToolTipText, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, disabled_color)
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, QColor(220, 220, 220))
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, disabled_color)
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.BrightText, QColor(255, 150, 150))
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Link, QColor(150, 150, 255))
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Highlight, QColor(180, 200, 220))
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.HighlightedText, QColor(240, 240, 240))
    app.setPalette(palette)
    app.styleHints().setColorScheme(Qt.ColorScheme.Light)
    window = FragPipeManifestCreator()
    try:
        # Determine if running as a PyInstaller bundled executable
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # If bundled, the 'images' folder is relative to sys._MEIPASS
            icon_path = os.path.join(sys._MEIPASS, 'images', 'frag_to_chalf_logo.png')
        else:
            # If running from source, assume 'images' is relative to the script's directory
            script_dir = os.getcwd()#os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(script_dir, 'images', 'frag_to_chalf_logo.png')
        
        icon = QIcon(icon_path)
        window.setWindowIcon(icon)
    except Exception as e:
        print(f"Error loading icon: {e}")
        print('frag_to_chalf_logo.png might be missing or path is incorrect.')
    window.show()
    sys.exit(app.exec())
