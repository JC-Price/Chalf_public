# -*- coding: utf-8 -*-
"""
Created on Tue Aug 12 14:52:40 2025

@author: chadhyer
"""

import sys
import os
import argparse
import json
import pandas as pd
from Bio.PDB import PDBParser, MMCIFParser, PDBIO, MMCIFIO
from Bio.PDB.SASA import ShrakeRupley
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QFileDialog, QLineEdit,
    QTextEdit, QLabel, QMessageBox, QGroupBox, QFormLayout,
    QDialog, QDialogButtonBox, QRadioButton, QInputDialog, QScrollArea
)
from PySide6.QtGui import QFont, QPalette, QColor, QIcon
from PySide6.QtCore import Qt
from collections import defaultdict

class SequenceDialog(QDialog):
    """A dialog to display the amino acid sequences of all chains."""
    def __init__(self, sequences, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Chain Sequences")
        self.setGeometry(200, 200, 600, 400)
        
        layout = QVBoxLayout()
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setFont(QFont("Courier", 10))
        
        # Fixed: Format the sequence with numbers above them and ensure alignment.
        full_text = ""
        for chain_id, seq in sequences.items():
            full_text += f"Chain: {chain_id}\n"
            
            # Iterate over the sequence in chunks of 50 for wrapping and alignment
            for i in range(0, len(seq), 50):
                line_chunk = seq[i:i + 50]
                
                # Create the number line for this chunk
                number_line = ""
                for j in range(0, len(line_chunk), 10):
                    current_num = i + j + 1
                    # Pad the number to 11 characters to align with 10 letters + 1 space
                    number_line += f"{current_num:<11}"
                
                full_text += number_line.rstrip() + "\n"
                
                # Create the sequence line for this chunk
                sequence_line = ""
                for j in range(0, len(line_chunk), 10):
                    sequence_block = line_chunk[j:j+10]
                    sequence_line += sequence_block + " "
                
                full_text += sequence_line.rstrip() + "\n\n"
        
        text_edit.setText(full_text)
        layout.addWidget(text_edit)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)
        
        self.setLayout(layout)

class ProteinAnalyzerGUI(QMainWindow):
    """Main GUI application window."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDB Tools")
        self.setGeometry(100, 100, 800, 600)

        self.current_file_path = None
        self.current_structure = None
        self.chain_inputs = {}
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # File selection section
        file_group = QGroupBox("File Selection")
        file_layout = QHBoxLayout()
        self.file_path_label = QLabel("No file selected.")
        browse_button = QPushButton("Browse...")
        browse_button.clicked.connect(self.open_file_dialog)
        file_layout.addWidget(self.file_path_label)
        file_layout.addWidget(browse_button)
        file_group.setLayout(file_layout)
        main_layout.addWidget(file_group)

        # Chain renumbering and naming section - now with a scroll area
        self.chains_group = QGroupBox("Chain Renumbering and Naming")
        self.chains_layout = QFormLayout()
        self.chains_group.setLayout(self.chains_layout)
        self.chains_group.setEnabled(False)  # Initially disabled
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.chains_group)
        main_layout.addWidget(self.scroll_area)
        
        # Sequence and output options
        options_group = QGroupBox("Options")
        options_layout = QHBoxLayout()
        self.show_seq_button = QPushButton("Show Sequences")
        self.show_seq_button.setEnabled(False)
        self.show_seq_button.clicked.connect(self.show_sequences)
        
        self.pdb_radio = QRadioButton("Save as PDB")
        self.pdb_radio.setChecked(False)
        self.cif_radio = QRadioButton("Save as CIF")
        self.cif_radio.setChecked(True)
        
        options_layout.addWidget(self.show_seq_button)
        options_layout.addStretch()
        options_layout.addWidget(QLabel("Output File Type:"))
        options_layout.addWidget(self.pdb_radio)
        options_layout.addWidget(self.cif_radio)
        options_group.setLayout(options_layout)
        main_layout.addWidget(options_group)

        # Output and processing section
        process_group = QGroupBox("Process & Save")
        process_layout = QVBoxLayout()
        
        self.process_button = QPushButton("Process and Save")
        self.process_button.setEnabled(False)
        self.process_button.clicked.connect(self.run_analysis)
        process_layout.addWidget(self.process_button)
        
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setText("Waiting for a file to be loaded...")
        process_layout.addWidget(self.log_output)
        
        process_group.setLayout(process_layout)
        main_layout.addWidget(process_group)

    def log(self, message):
        self.log_output.append(message)
        
    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open PDB/mmCIF File", "", "Protein Files (*.pdb *.cif)"
        )
        if file_path:
            self.current_file_path = file_path
            self.file_path_label.setText(os.path.basename(file_path))
            self.log(f"File selected: {self.current_file_path}")
            self.load_structure()

    def load_structure(self):
        self.log("Loading structure...")
        
        # Clear previous chain inputs
        while self.chains_layout.count():
            item = self.chains_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.chain_inputs.clear()
        
        file_extension = os.path.splitext(self.current_file_path)[1].lower()
        if file_extension == '.pdb':
            parser = PDBParser(QUIET=True)
            self.current_structure = parser.get_structure('protein', self.current_file_path)
        elif file_extension == '.cif':
            parser = MMCIFParser(QUIET=True)
            self.current_structure = parser.get_structure('protein', self.current_file_path)
        else:
            QMessageBox.warning(self, "Unsupported File Type", "Please select a .pdb or .cif file.")
            self.log("Error: Unsupported file type.")
            self.chains_group.setEnabled(False)
            self.show_seq_button.setEnabled(False)
            self.process_button.setEnabled(False)
            return

        self.log("Structure loaded successfully. Initializing chains...")
        
        # Populate chain renumbering and naming section
        for model in self.current_structure:
            for chain in model:
                res_list = list(chain.get_residues())
                if res_list:
                    start_res = res_list[0].id[1]
                    end_res = res_list[-1].id[1]
                    
                    # Modified: Display the residue range in the GUI
                    label = QLabel(f"Chain {chain.id} (Residues: {start_res}-{end_res})")
                    new_start_edit = QLineEdit(str(start_res))
                    new_name_edit = QLineEdit(chain.id)
                    
                    self.chains_layout.addRow(label)
                    self.chains_layout.addRow("New Start:", new_start_edit)
                    self.chains_layout.addRow("New Name:", new_name_edit)
                    self.chains_layout.addRow(QLabel("---")) # Add a separator
                    self.chain_inputs[chain.id] = (new_start_edit, new_name_edit)
        
        self.chains_group.setEnabled(True)
        self.show_seq_button.setEnabled(True)
        self.process_button.setEnabled(True)
        self.log("Ready to process. Enter new starting residue numbers and names for each chain.")

    def show_sequences(self):
        """Extract and display sequences for all chains."""
        if not self.current_structure:
            QMessageBox.warning(self, "No Structure", "Please load a protein structure file first.")
            return

        sequences = defaultdict(str)
        for model in self.current_structure:
            for chain in model:
                for residue in chain:
                    if residue.has_id('CA'): # Check for alpha-carbon to filter out heteroatoms
                        res_name = residue.get_resname()
                        # Simple mapping for common amino acids
                        one_letter_code = {
                            "ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C", "GLN": "Q", "GLU": "E", "GLY": "G",
                            "HIS": "H", "ILE": "I", "LEU": "L", "LYS": "K", "MET": "M", "PHE": "F", "PRO": "P", "SER": "S",
                            "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V"
                        }.get(res_name, '?')
                        sequences[chain.id] += one_letter_code
        
        if sequences:
            dialog = SequenceDialog(sequences, self)
            dialog.exec()
        else:
            QMessageBox.information(self, "No Chains Found", "No protein chains with valid residues were found.")
            
    def run_analysis(self):
        """Main function to trigger renumbering, data extraction, and saving."""
        if not self.current_structure:
            QMessageBox.warning(self, "No Structure", "Please load a protein structure file first.")
            return
        
        output_dir = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if not output_dir:
            self.log("Output directory selection canceled.")
            return
            
        output_name, ok = QInputDialog.getText(self, "Output Directory Name", "Enter a name for the output directory:")
        if not ok or not output_name:
            self.log("Output directory name not provided.")
            return

        full_output_path = os.path.join(output_dir, output_name)
        
        config = self.get_gui_config()
        if not config:
            return # get_gui_config handles its own errors
        
        output_type = 'pdb' if self.pdb_radio.isChecked() else 'cif'

        try:
            self.process_structure(self.current_structure, config, full_output_path, output_name, output_type, self.log)
            QMessageBox.information(self, "Success", "Analysis complete and files saved.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred during processing: {e}")

    def get_gui_config(self):
        """Gathers configuration from GUI input fields."""
        config = {}
        new_chain_names = set()
        for chain_id, (start_edit, name_edit) in self.chain_inputs.items():
            new_start_str = start_edit.text()
            new_name = name_edit.text().strip()
            
            if not new_name:
                QMessageBox.warning(self, "Invalid Chain Name", "Chain names cannot be empty.")
                return None
            
            if new_name in new_chain_names:
                QMessageBox.warning(self, "Duplicate Chain Name", f"The new name '{new_name}' is already used. Please choose a unique name.")
                return None
            new_chain_names.add(new_name)
            
            try:
                new_start_resnum = int(new_start_str)
                config[chain_id] = {"new_start": new_start_resnum, "new_name": new_name}
            except ValueError:
                QMessageBox.warning(self, "Invalid Input", f"Invalid starting number for chain {chain_id}. Please enter an integer.")
                return None
        return config

    @staticmethod
    def process_structure(structure, config, output_path, output_name, output_type, logger=print):
        """
        Core logic for renumbering, calculating SASA, and saving.
        This is used by both the GUI and CLI.
        """
        logger("Starting analysis...")
        
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            logger(f"Created output directory: {output_path}")

        # Renumber and rename chains
        logger("Renumbering and renaming chains in two passes to avoid conflicts...")
        new_structure = structure.copy()
        
        # Pass 1: Renumber all residues to negative numbers to clear conflicts
        temp_resnum = -1
        for model in new_structure:
            for chain in model:
                if chain.id in config:
                    for residue in chain:
                        residue.id = (" ", temp_resnum, " ")
                        temp_resnum -= 1
        
        # Pass 2: Renumber to the user's desired starting numbers and rename chains
        for model in new_structure:
            for chain in model:
                if chain.id in config:
                    new_start_resnum = config[chain.id]["new_start"]
                    new_name = config[chain.id]["new_name"]
                    
                    chain.id = new_name  # Update chain ID
                    
                    resnum = new_start_resnum
                    for residue in chain:
                        residue.id = (" ", resnum, " ")
                        resnum += 1

        # Calculate SASA
        logger("Calculating SASA...")
        sr = ShrakeRupley()
        sr.compute(new_structure, level="R")

        # Assign SASA values to the occupancy for visualization
        logger("Assigning SASA values to atom occupancy...")
        for model in new_structure:
            for chain in model:
                for residue in chain:
                    if residue.sasa is not None:
                        for atom in residue:
                            # Round the SASA value to 2 decimal places as occupancy is a float
                            atom.set_occupancy(round(residue.sasa, 2))

        # Extract all data into a pandas DataFrame
        logger("Extracting data...")
        data = []
        for model in new_structure:
            for chain in new_structure.get_chains():
                for residue in chain.get_residues():
                    res_name = residue.get_resname()
                    res_num = residue.get_id()[1]
                    chain_id = chain.id
                    sasa_value = residue.sasa
                    
                    # Original pLDDT data is still in the b-factor field.
                    plddt_value = None
                    try:
                        # This gets the pLDDT from the original file
                        plddt_value = next(residue.get_atoms()).get_bfactor()
                    except StopIteration:
                        plddt_value = None # No atoms in residue
                    
                    data.append({
                        'residue_number': res_num,
                        'residue_name': res_name,
                        'chain_id': chain_id,
                        'pLDDT': plddt_value,
                        'sasa': sasa_value
                    })
        
        output_df = pd.DataFrame(data)

        # Save files
        logger(f"Saving output files to {output_path}...")
        # Modified: Use the provided output_name for file names
        csv_file = os.path.join(output_path, f"{output_name}.csv")
        output_df.to_csv(csv_file, index=False)
        logger(f"CSV file saved: {csv_file}")
        
        structure_file = os.path.join(output_path, f"{output_name}.{output_type}")
        if output_type == 'pdb':
            io = PDBIO()
            io.set_structure(new_structure)
            io.save(structure_file)
        else: # cif
            io = MMCIFIO()
            io.set_structure(new_structure)
            io.save(structure_file)
        logger(f"Structure file saved: {structure_file}")
        logger("Processing complete.")

def run_headless(args):
    """Executes the analysis from the command line."""
    print("Running in headless mode...")
    
    # Check for required files
    if not os.path.exists(args.file):
        print(f"Error: Input file not found at '{args.file}'")
        sys.exit(1)
        
    if not os.path.exists(args.config):
        print(f"Error: Config file not found at '{args.config}'")
        sys.exit(1)

    # Load config file
    try:
        with open(args.config, 'r') as f:
            config = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Could not parse JSON config file '{args.config}'. Please check the format.")
        sys.exit(1)

    # Validate config file structure and names
    new_chain_names = set()
    for chain_id, data in config.items():
        if "new_start" not in data or "new_name" not in data:
            print(f"Error: Invalid config for chain '{chain_id}'. Must contain 'new_start' and 'new_name'.")
            sys.exit(1)
        if data["new_name"] in new_chain_names:
            print(f"Error: Duplicate new chain name '{data['new_name']}' found in config file.")
            sys.exit(1)
        new_chain_names.add(data["new_name"])
    
    # Load structure
    file_extension = os.path.splitext(args.file)[1].lower()
    if file_extension == '.pdb':
        parser = PDBParser(QUIET=True)
    elif file_extension == '.cif':
        parser = MMCIFParser(QUIET=True)
    else:
        print(f"Error: Unsupported file type '{file_extension}'. Please use .pdb or .cif.")
        sys.exit(1)
        
    try:
        structure = parser.get_structure('protein', args.file)
    except Exception as e:
        print(f"Error: Failed to parse structure file '{args.file}'. {e}")
        sys.exit(1)
        
    # Run the core processing logic
    output_path = os.path.join(args.output_dir,args.name)
    os.makedirs(output_path,exist_ok=True)
    #output_path = os.path.join(os.getcwd(), args.output_dir)
    try:
        # Modified: Pass the output directory name to the processing function
        ProteinAnalyzerGUI.process_structure(structure, config, output_path, args.name, args.output_type, print)
        print("Headless processing completed successfully.")
    except Exception as e:
        print(f"An error occurred during headless processing: {e}")
        sys.exit(1)
def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(description="Protein structure analyzer with GUI and CLI options.")
    parser.add_argument("--headless", action="store_true", help="Run in command-line mode without GUI.")
    parser.add_argument("--file", type=str, help="Path to the input PDB or CIF file (for headless mode).")
    parser.add_argument("--config", type=str, help="Path to a JSON file with renumbering and naming configuration (for headless mode).")
    parser.add_argument("--output_dir", type=str, help="Name of the output directory (for headless mode).")
    parser.add_argument("--output_type", choices=['pdb', 'cif'], default='pdb', help="Output file type (for headless mode).")
    
    args = parser.parse_args()

    if args.headless:
        # Check if all required arguments for headless mode are provided
        if not all([args.file, args.config, args.output_dir]):
            parser.error("--file, --config, and --output_dir are required in headless mode.")
        run_headless(args)
    else:
        app = QApplication(sys.argv)
        window = ProteinAnalyzerGUI()
        window.show()
        sys.exit(app.exec())

def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(description="Protein structure analyzer with GUI and CLI options.")
    parser.add_argument("--headless", action="store_true", help="Run in command-line mode without GUI.")
    parser.add_argument("--file", type=str, help="Path to the input PDB or CIF file (for headless mode).")
    parser.add_argument("--config", type=str, help="Path to a JSON file with renumbering and naming configuration (for headless mode).")
    parser.add_argument("--output_dir", type=str, help="Name of the output directory (for headless mode).")
    parser.add_argument("--name", type=str, help="Name of the output file (for headless mode).")
    parser.add_argument("--output_type", choices=['pdb', 'cif'], default='cif', help="Output file type (for headless mode).")
    
    args = parser.parse_args()

    if args.headless:
        # Check if all required arguments for headless mode are provided
        if not all([args.file, args.config, args.output_dir, args.name]):
            parser.error("--file, --config, --name, and --output_dir are required in headless mode.")
        run_headless(args)
    else:
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

        window = ProteinAnalyzerGUI()
        try:
            # Determine if running as a PyInstaller bundled executable
            if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
                # If bundled, the 'images' folder is relative to sys._MEIPASS
                icon_path = os.path.join(sys._MEIPASS, 'images', 'pdb_tools_logo.png')
            else:
                # If running from source, assume 'images' is relative to the script's directory
                script_dir = os.getcwd()#os.path.dirname(os.path.abspath(__file__))
                icon_path = os.path.join(script_dir, 'images', 'pdb_tools_logo.png')
            
            icon = QIcon(icon_path)
            window.setWindowIcon(icon)
        except Exception as e:
            print(f"Error loading icon: {e}")
            print('frag_to_chalf_logo.png might be missing or path is incorrect.')
        window.show()
        sys.exit(app.exec())

if __name__ == "__main__":
    main()
