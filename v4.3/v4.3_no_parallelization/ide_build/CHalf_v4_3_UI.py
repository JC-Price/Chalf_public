# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CHalf_v4.3_gui.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication,
    QMetaObject, QObject, QRect,
    QSize, QUrl, Qt, Signal, QRunnable, QThreadPool, Slot, QTimer)
from PySide6.QtGui import (QBrush, QColor,
    QFont, QIcon, QPalette, QDesktopServices, QTextCursor)
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QCheckBox,
    QComboBox, QDoubleSpinBox, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel,
    QLayout, QLineEdit, QMainWindow, QMenuBar,
    QPushButton, QScrollArea, QSizePolicy, QSpinBox,
    QStatusBar, QTabWidget, QTableWidget, QTableWidgetItem,
    QTextEdit, QVBoxLayout, QWidget, QFileDialog, QMessageBox, QDialog, QDialogButtonBox, QInputDialog, QColorDialog)

from datetime import datetime
import sys, os, json, subprocess, threading, queue, time


_COLOR_PALETTE = [
        "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
        "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
    ]

def extract_workflow(file):
    try:
        with open(f'workflows/{file}','r') as read_file:
            workflow = read_file.readlines()
            parameters = {}
            for line in workflow:
                line = line.strip()
                if line and not line.startswith('#'):  # Skip empty lines and comments
                    key, value = line.split('=', 1)  # Split at the first '='
                    value = value.strip()
                    try:
                        value = int(value)
                    except ValueError:
                        try:
                            value = float(value)
                        except ValueError:
                            try:
                                value = str(value)
                                if value.upper() == 'TRUE':
                                    value = True
                                elif value.upper() == 'FALSE':
                                    value = False
                                elif value == '':
                                    value = None
                            except ValueError:
                                    print(f'Error in {key}')
                    parameters[key.strip()] = value
            return parameters
    except FileNotFoundError: print('Worklist file missing. Cannot load parameters.'); return None
        

def extract_conc_cols(file):
    try:
        with open(f'concentration_columns/{file}','r') as read_file:
            conc_cols = json.loads(read_file.read()) # Modified: Added .read()
            return conc_cols
    except Exception as e: # Modified: Catching specific exception for better debugging
        print(f'conc_cols file missing or formatted incorrectly. Cannot load parameters. Setting to IPSA by default: {e}') # Modified
        return dict(zip(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],[0.0, 0.43, 0.87, 1.3, 1.74, 2.17, 2.61, 3.04, 3.48, 3.59]))

def get_workflows():
    try:
        workflow_files = [file for file in os.listdir('workflows') if '.workflow' in file]
        workflow_names = [name.replace('.workflow','') for name in workflow_files]
        workflows = dict(zip(workflow_names,workflow_files))
    except FileNotFoundError:
        workflows = {'IPSA':None}
        print('workflow folder not found. Applying defaults')
    return workflows

def get_conc_cols():
    try:
        cc_files = [file for file in os.listdir('concentration_columns') if '.cc' in file]
        cc_names = [name.replace('.cc','') for name in cc_files]
        conc_cols = dict(zip(cc_names,cc_files))
    except FileNotFoundError:
        conc_cols = {'IPSA':None}
        print('concentrations_columns folder not found. Applying defaults')
    return conc_cols


workflows = get_workflows()
conc_cols = get_conc_cols()

class StreamEmitter(QObject):
    # Signal to emit when a line is received from the subprocess
    line_received = Signal(str)

# Custom QObject to redirect stream output to a QTextEdit
class TextEditLogger(QObject):
    # Signals for different types of output to the QTextEdit
    append_plain_text_signal = Signal(str, bool) # (text, add_timestamp_flag)
    append_html_text_signal = Signal(str)        # (html_text)

    def __init__(self, text_edit=None):
        super().__init__()
        self._text_edit = None
        self._plain_text_buffer = []  # Buffer for plain text messages
        self._html_text_buffer = []   # Buffer for HTML messages
        self._last_line_was_tqdm = False # To handle in-place updates like progress bars

        if text_edit:
            self.set_text_edit(text_edit)
        
        # Connect internal signals to the actual append slots
        self.append_plain_text_signal.connect(self._actual_append_plain_text)
        self.append_html_text_signal.connect(self._actual_append_html_text)

    def set_text_edit(self, text_edit):
        """Sets the QTextEdit widget and flushes any buffered messages."""
        self._text_edit = text_edit
        # Process buffered plain text messages first
        if self._plain_text_buffer:
            for text, add_timestamp_flag in self._plain_text_buffer:
                self._actual_append_plain_text(text, add_timestamp_flag)
            self._plain_text_buffer.clear()
        # Then process buffered HTML messages
        if self._html_text_buffer:
            for html_text in self._html_text_buffer:
                self._actual_append_html_text(html_text)
            self._html_text_buffer.clear()

    @Slot(str, bool)
    def _actual_append_plain_text(self, text, add_timestamp_flag):
        """Internal slot to append plain text to QTextEdit, handling timestamps and multi-line strings."""
        if not self._text_edit:
            self._plain_text_buffer.append((text, add_timestamp_flag))
            return

        cursor = self._text_edit.textCursor()
        
        # Handle tqdm-like updates (ends with \r)
        is_tqdm_like_update = text.endswith('\r')
        if is_tqdm_like_update:
            text = text.rstrip('\r') # Remove the carriage return for consistent processing

        # Split the incoming text into individual lines to prefix each one.
        lines = text.splitlines(keepends=False) # Split, don't keep original newlines

        # Check if the original incoming text ended with a newline.
        ends_with_newline_in_original = text.endswith(('\n', '\r\n'))

        for i, line in enumerate(lines):
            prefixed_line = line
            if '[NO_TIMESTAMP]' in line: line = line.replace('[NO_TIMESTAMP]',''); add_timestamp_flag = False; prefixed_line = line
            if add_timestamp_flag:
                current_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                prefixed_line = f"[{current_dt}] {line}"
            
            cursor.movePosition(QTextCursor.End)

            if is_tqdm_like_update and self._last_line_was_tqdm and i == 0:
                # If it's a tqdm-like update and the previous was also, overwrite the last line
                cursor.select(QTextCursor.LineUnderCursor)
                cursor.removeSelectedText()
                cursor.insertText(prefixed_line)
            else:
                # For all other cases, simply insert text
                cursor.insertText(prefixed_line)
            
            # Add a newline character, but only if it's not the last line of a multi-line input
            # OR if it's the last line and the original input ended with a newline.
            if i < len(lines) - 1 or ends_with_newline_in_original:
                cursor.insertText("\n")

        self._last_line_was_tqdm = is_tqdm_like_update
        self._text_edit.setTextCursor(cursor)
        self._text_edit.ensureCursorVisible()

    @Slot(str)
    def _actual_append_html_text(self, html_text):
        """Internal slot to append HTML text to QTextEdit."""
        if not self._text_edit:
            self._html_text_buffer.append(html_text)
            return
        
        cursor = self._text_edit.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertHtml(html_text)
        cursor.insertText("\n") # Ensure a newline after HTML block
        
        self._text_edit.setTextCursor(cursor)
        self._text_edit.ensureCursorVisible()
        self._last_line_was_tqdm = False # HTML breaks tqdm-like sequence

    # Public method for general logging (adds timestamp)
    def write(self, text):
        """Writes text to the log with a datetime timestamp."""
        self.append_plain_text_signal.emit(text, True)

    # Public method for raw logging (no timestamp)
    def write_raw(self, text):
        """Writes raw text to the log without a datetime timestamp."""
        self.append_plain_text_signal.emit(text, False)

    # Public method for the "ALL JOBS DONE" message (HTML formatting)
    def write_completion_message(self, total_minutes):
        """Writes a special formatted completion message with total time."""
        message_text = f"CHALF PROCESSES COMPLETED IN {total_minutes:.2f} MINUTES"
        
        # Calculate flanking '=' signs for approximate centering
        # Using 78 as an approximate common terminal width for display
        filler_chars_total = 99 - len(message_text)
        left_filler_len = filler_chars_total // 2
        right_filler_len = filler_chars_total - left_filler_len
        
        final_display_message = f"{'=' * left_filler_len} {message_text} {'=' * right_filler_len}"

        # Create HTML for red color and center alignment
        # Using <p align="center"> provides better centering in QTextEdit than character padding alone.
        html_content = (
            f'<p align="center"><font color="maroon" style="font-family: monospace; white-space: pre;">'
            f'{final_display_message}'
            f'</font></p>'
        )
        self.append_html_text_signal.emit(html_content)

    def flush(self):
        """Required for sys.stdout/stderr redirection, but does nothing in this implementation."""
        pass
# Worker class to run the external script in a separate thread
class ScriptRunner(QObject, QRunnable):
    finished = Signal()
    error = Signal(str)

    def __init__(self, script_path, args, logger):
        QObject.__init__(self)
        QRunnable.__init__(self)

        self.script_path = script_path
        self.args = args
        self.logger = logger # The TextEditLogger instance
        self._process = None
        self._stop_event = threading.Event() # Event to signal reader threads to stop
        self._stdout_queue = queue.Queue() # Thread-safe queue for stdout
        self._stderr_queue = queue.Queue() # Thread-safe queue for stderr

        # StreamEmitter will live in the main thread to emit signals
        self._stream_emitter = StreamEmitter()
        # Connect stream_emitter's signal to logger's write method
        self._stream_emitter.line_received.connect(self.logger.write)

        # QTimer to periodically check the queues and update GUI
        self._timer = QTimer()
        self._timer.timeout.connect(self._check_queues)
        self._timer.start(50) # Check every 50 ms for new output

    def _read_pipe_in_thread(self, pipe, q):
        """Helper function to read a pipe in a separate thread."""
        while not self._stop_event.is_set():
            line = pipe.readline() # Read line by line
            if not line: # EOF reached
                break
            # Put decoded line into the queue
            q.put(line.decode(sys.getdefaultencoding(), errors='replace'))
        pipe.close()

    @Slot()
    def _check_queues(self):
        """Called by QTimer to process lines from queues and emit signals."""
        # Process stdout queue
        while not self._stdout_queue.empty():
            try:
                line = self._stdout_queue.get_nowait()
                self._stream_emitter.line_received.emit(line)
            except queue.Empty: # Should not happen with get_nowait and empty() check
                break
        # Process stderr queue
        while not self._stderr_queue.empty():
            try:
                line = self._stderr_queue.get_nowait()
                self._stream_emitter.line_received.emit(line)
            except queue.Empty:
                break
        
        # If process has finished and both queues are empty, stop the timer
        if self._process and self._process.poll() is not None and \
           self._stdout_queue.empty() and self._stderr_queue.empty():
            self._timer.stop()


    @Slot()
    def run(self):
        msg = '~'*100
        self.logger.write_raw(f"{msg}\n")
        try:
            # Construct the full command as a list of arguments
            # subprocess.Popen will handle quoting when shell=False
            full_command_list = [sys.executable, self.script_path] + self.args
            # For logging purposes, you can still show how the command would look
            # if executed directly in a shell (though not what Popen uses with shell=False)
            display_command = ' '.join(full_command_list)#[shlex.quote(arg) for arg in full_command_list])
            self.logger.write(f"Executing command: {display_command}\n") # This is just for logging clarity

            # Start the subprocess with shell=False and pass arguments as a list
            self._process = subprocess.Popen(
                full_command_list, # Pass the command as a list of strings
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=False, # <--- IMPORTANT CHANGE: Set shell to False
                text=False, # Still read bytes and decode manually for better control
                bufsize=0,
                env=dict(os.environ, PYTHONUNBUFFERED="1") # Keep for unbuffered Python output
            )

            # Start reader threads for stdout and stderr pipes
            self._stdout_thread = threading.Thread(target=self._read_pipe_in_thread,
                                                   args=(self._process.stdout, self._stdout_queue))
            self._stderr_thread = threading.Thread(target=self._read_pipe_in_thread,
                                                   args=(self._process.stderr, self._stderr_queue))
            
            self._stdout_thread.daemon = True # Allows program to exit even if threads are running
            self._stderr_thread.daemon = True

            self._stdout_thread.start()
            self._stderr_thread.start()

            # Wait for the subprocess to finish. This will block this QRunnable's thread,
            # but pipe reading (and thus GUI updates) happens in separate threads.
            self._process.wait()

            # After subprocess finishes, signal reader threads to stop and wait for them
            self._stop_event.set() # Set the event to tell threads to stop
            self._stdout_thread.join(timeout=1) # Give threads a moment to finish cleanly
            self._stderr_thread.join(timeout=1)
            
            # Process any remaining buffered output immediately after threads join
            self._check_queues()

            # Check subprocess return code for errors
            if self._process.returncode != 0:
                self.error.emit(f"Script '{os.path.basename(self.script_path)}' exited with error code {self._process.returncode}.")

        except FileNotFoundError:
            self.error.emit(f"Script not found: {self.script_path}\n"
                            "Please ensure the script is in the correct directory or its path is specified correctly.")
        except Exception as e:
            self.error.emit(f"An unexpected error occurred during script execution: {e}")
        finally:
            self._timer.stop() # Ensure timer is stopped
            self.finished.emit() # Always emit finished, even if errors occurred

    def stop(self):
        """Method to forcefully stop the running script."""
        if self._process and self._process.poll() is None: # If process is still running
            self._process.terminate() # Terminate the subprocess
            self.logger.write(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Terminating script: {os.path.basename(self.script_path)}\n")
            self.logger.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Script stopped by user.\n")
            
            # Signal reader threads to stop if process terminated and wait for them
            self._stop_event.set()
            if self._stdout_thread.is_alive(): self._stdout_thread.join(timeout=1)
            if self._stderr_thread.is_alive(): self._stderr_thread.join(timeout=1)
            self._timer.stop() # Stop the timer as well

class ColorSelectionDialog(QDialog):
    def __init__(self, parent=None, initial_color_hex="#1f77b4", used_colors=None):
        super().__init__(parent)
        self.setWindowTitle("Select Condition Color")
        self.setModal(True)
        self.selected_color = QColor(initial_color_hex)
        self.used_colors = used_colors if used_colors is not None else set()
        _COLOR_PALETTE = [ # Must be consistent with Ui_MainWindow's palette
            "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
            "#8c564b", "#e377b2", "#7f7f7f", "#bcbd22", "#17becf"
        ] 
        self.setupUi()
        

    def setupUi(self):
        main_layout = QVBoxLayout(self)

        # Color preview
        color_preview_layout = QHBoxLayout()
        self.color_preview_label = QLabel()
        self.color_preview_label.setFixedSize(60, 30)
        self.color_preview_label.setStyleSheet(f"background-color: {self.selected_color.name()}; border: 1px solid black;")
        color_preview_layout.addWidget(QLabel("Current Color:"))
        color_preview_layout.addWidget(self.color_preview_label)
        main_layout.addLayout(color_preview_layout)

        # Hex Input
        hex_layout = QHBoxLayout()
        self.hex_lineEdit = QLineEdit(self.selected_color.name())
        self.hex_lineEdit.textChanged.connect(self._on_hex_changed)
        hex_layout.addWidget(QLabel("Hex:"))
        hex_layout.addWidget(self.hex_lineEdit)
        main_layout.addLayout(hex_layout)

        # RGB SpinBoxes
        rgb_layout = QHBoxLayout()
        self.r_spinbox = QSpinBox()
        self.g_spinbox = QSpinBox()
        self.b_spinbox = QSpinBox()
        for sb in [self.r_spinbox, self.g_spinbox, self.b_spinbox]:
            sb.setRange(0, 255)
            sb.valueChanged.connect(self._on_rgb_changed)
        
        rgb_layout.addWidget(QLabel("R:"))
        rgb_layout.addWidget(self.r_spinbox)
        rgb_layout.addWidget(QLabel("G:"))
        rgb_layout.addWidget(self.g_spinbox)
        rgb_layout.addWidget(QLabel("B:"))
        rgb_layout.addWidget(self.b_spinbox)
        main_layout.addLayout(rgb_layout)
        self._update_rgb_spinboxes_from_color() # Initialize RGB from selected color


        # Preset Colors
        preset_group_box = QGroupBox("Preset Colors")
        preset_layout = QGridLayout()
        for i, color_hex in enumerate(_COLOR_PALETTE):
            btn = QPushButton()
            btn.setFixedSize(30, 30)
            btn.setStyleSheet(f"background-color: {color_hex}; border: 1px solid gray;")
            btn.clicked.connect(lambda checked, c=color_hex: self._set_color(QColor(c)))
            preset_layout.addWidget(btn, i // 5, i % 5) # 5 columns
        preset_group_box.setLayout(preset_layout)
        main_layout.addWidget(preset_group_box)

        # Used Colors Section
        if self.used_colors:
            used_group_box = QGroupBox("Colors Used in Table")
            used_layout = QGridLayout()
            sorted_used_colors = sorted(list(self.used_colors)) # Sort for consistent display
            for i, color_hex in enumerate(sorted_used_colors):
                lbl = QLabel()
                lbl.setFixedSize(30, 30)
                lbl.setStyleSheet(f"background-color: {color_hex}; border: 1px solid gray;")
                lbl.setToolTip(color_hex) # Show hex on hover
                # Make it clickable to select the used color
                lbl.mousePressEvent = lambda event, c=color_hex: self._set_color(QColor(c))
                used_layout.addWidget(lbl, i // 5, i % 5)
            used_group_box.setLayout(used_layout)
            main_layout.addWidget(used_group_box)

        # QColorDialog button for advanced selection (color wheel, saturation/brightness)
        open_color_dialog_btn = QPushButton("More Colors (Color Wheel, etc.)")
        open_color_dialog_btn.clicked.connect(self._open_standard_color_dialog)
        main_layout.addWidget(open_color_dialog_btn)


        # Dialog buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        main_layout.addWidget(button_box)

        # Initial update
        self._set_color(self.selected_color)

    def _set_color(self, color: QColor):
        self.selected_color = color
        self.color_preview_label.setStyleSheet(f"background-color: {self.selected_color.name()}; border: 1px solid black;")
        self.hex_lineEdit.blockSignals(True) # Avoid re-triggering textChanged
        self.hex_lineEdit.setText(self.selected_color.name())
        self.hex_lineEdit.blockSignals(False)
        self._update_rgb_spinboxes_from_color()

    def _on_hex_changed(self, text):
        color = QColor(text)
        if color.isValid():
            self._set_color(color)

    def _on_rgb_changed(self):
        r = self.r_spinbox.value()
        g = self.g_spinbox.value()
        b = self.b_spinbox.value()
        color = QColor(r, g, b)
        self._set_color(color)

    def _update_rgb_spinboxes_from_color(self):
        self.r_spinbox.blockSignals(True)
        self.g_spinbox.blockSignals(True)
        self.b_spinbox.blockSignals(True)
        self.r_spinbox.setValue(self.selected_color.red())
        self.g_spinbox.setValue(self.selected_color.green())
        self.b_spinbox.setValue(self.selected_color.blue())
        self.r_spinbox.blockSignals(False)
        self.g_spinbox.blockSignals(False)
        self.b_spinbox.blockSignals(False)

    def _open_standard_color_dialog(self):
        # Open the standard QColorDialog, initialized with our current color
        color = QColorDialog.getColor(self.selected_color, self, "Select Color", QColorDialog.ShowAlphaChannel)
        if color.isValid():
            self._set_color(color)

    def get_selected_color_hex(self):
        return self.selected_color.name()

class EditConcentrationDialog(QDialog):
    def __init__(self, parent=None, current_conc_data=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Concentration Columns")
        self.setMinimumSize(400, 300)
        self.current_conc_data = current_conc_data if current_conc_data is not None else {}
        self.new_conc_data = {} # To store the data after editing
        self.saved_preset_name = None

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        # Input for new preset name
        name_layout = QHBoxLayout()
        self.name_label = QLabel("Preset Name:")
        self.name_lineEdit = QLineEdit()
        self.name_lineEdit.setPlaceholderText("Enter new preset name or select existing")
        name_layout.addWidget(self.name_label)
        name_layout.addWidget(self.name_lineEdit)
        main_layout.addLayout(name_layout)

        # Dropdown for existing presets
        self.existing_presets_label = QLabel("Existing Presets:")
        self.existing_presets_comboBox = QComboBox()
        self.existing_presets_comboBox.addItem("New Preset") # Default option
        # Populate with existing concentration column presets
        for name in get_conc_cols().keys():
            self.existing_presets_comboBox.addItem(name)
        self.existing_presets_comboBox.currentIndexChanged.connect(self.load_selected_preset)
        main_layout.addWidget(self.existing_presets_label)
        main_layout.addWidget(self.existing_presets_comboBox)

        # Table for concentration values
        self.conc_table = QTableWidget(0, 2) # 0 rows, 2 columns (Column Name, Concentration Value)
        self.conc_table.setHorizontalHeaderLabels(["Column Name", "Associated Concentration"]) # Updated header
        self.conc_table.horizontalHeader().setStretchLastSection(True)
        self.conc_table.setSelectionBehavior(QAbstractItemView.SelectRows) # Select entire rows
        main_layout.addWidget(self.conc_table)

        # Buttons for adding/removing rows
        button_layout = QHBoxLayout()
        self.add_row_button = QPushButton("Add Row")
        self.add_row_button.clicked.connect(self.add_concentration_row)
        self.remove_row_button = QPushButton("Remove Selected Row(s)")
        self.remove_row_button.clicked.connect(self.remove_concentration_row)
        button_layout.addWidget(self.add_row_button)
        button_layout.addWidget(self.remove_row_button)
        main_layout.addLayout(button_layout)

        # Dialog buttons (OK, Cancel)
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept) # Connects OK to accept()
        self.button_box.rejected.connect(self.reject) # Connects Cancel to reject()
        main_layout.addWidget(self.button_box)

        # Load initial data if provided (for editing existing presets)
        if self.current_conc_data:
            self.load_data_into_table(self.current_conc_data)
        else:
            # Add a few empty rows for a new preset by default
            for _ in range(5):
                self.add_concentration_row()

    def load_selected_preset(self):
        selected_name = self.existing_presets_comboBox.currentText()
        if selected_name == "New Preset":
            self.name_lineEdit.clear()
            self.conc_table.setRowCount(0)
            for _ in range(5): # Add some default empty rows for new preset
                self.add_concentration_row()
        else:
            self.name_lineEdit.setText(selected_name)
            # Load data from the selected preset file
            file_name = get_conc_cols().get(selected_name)
            if file_name:
                loaded_data = extract_conc_cols(file_name)
                self.load_data_into_table(loaded_data)
            else:
                QMessageBox.warning(self, "Error", f"Could not find file for preset: {selected_name}")
                self.conc_table.setRowCount(0) # Clear table if file not found

    def load_data_into_table(self, data):
        self.conc_table.setRowCount(0) # Clear existing rows
        row = 0
        # Sort keys to ensure consistent order (optional but good practice for display)
        for col_name in sorted(data.keys(), key=lambda x: int(x) if x.isdigit() else x):
            conc_value = data[col_name]
            self.conc_table.insertRow(row)
            self.conc_table.setItem(row, 0, QTableWidgetItem(str(col_name)))
            self.conc_table.setItem(row, 1, QTableWidgetItem(str(conc_value)))
            row += 1

    def add_concentration_row(self):
        row_count = self.conc_table.rowCount()
        self.conc_table.insertRow(row_count)
        self.conc_table.setItem(row_count, 0, QTableWidgetItem(str(row_count))) # Default column name as index
        self.conc_table.setItem(row_count, 1, QTableWidgetItem("0.0")) # Default concentration value

    def remove_concentration_row(self):
        selected_rows = sorted(list(set(index.row() for index in self.conc_table.selectedIndexes())), reverse=True)
        for row in selected_rows:
            self.conc_table.removeRow(row)

    def get_concentration_data(self):
        data = {}
        has_errors = False
        error_messages = []

        for row in range(self.conc_table.rowCount()):
            column_name_item = self.conc_table.item(row, 0)
            concentration_item = self.conc_table.item(row, 1)

            if column_name_item and concentration_item:
                col_name = column_name_item.text().strip()
                conc_str = concentration_item.text().strip()

                if not col_name:
                    error_messages.append(f"Row {row+1}: 'Column Name' cannot be empty.")
                    has_errors = True
                    # Do not set to default, as the user wants a string name
                    continue # Skip to the next row

                try:
                    conc_value = float(conc_str)
                    data[col_name] = conc_value
                except ValueError:
                    error_messages.append(f"Row {row+1}: Invalid concentration value '{conc_str}'. Setting to 0.0.")
                    has_errors = True
                    # Set the table item's text to "0.0" and store 0.0 in data
                    concentration_item.setText("0.0")
                    data[col_name] = 0.0
            else:
                # This case should ideally not happen if rows are properly managed,
                # but it's a good fallback for incomplete rows.
                error_messages.append(f"Row {row+1}: Both 'Column Name' and 'Associated Concentration' must be filled. This row will be ignored.")
                has_errors = True

        return data, not has_errors, error_messages # Return data, validity status, and error messages

    def save_concentration_data(self):
        preset_name = self.name_lineEdit.text().strip()
        if not preset_name:
            QMessageBox.warning(self, "Save Error", "Please enter a name for the concentration preset.")
            return

        data_to_save = self.new_conc_data
        if not data_to_save:
            QMessageBox.warning(self, "Save Error", "No valid concentration data to save.")
            return

        conc_cols_dir = "concentration_columns"
        if not os.path.exists(conc_cols_dir):
            os.makedirs(conc_cols_dir)

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Concentration Columns Preset",
            os.path.join(conc_cols_dir, f"{preset_name}.cc"),
            "Concentration Column Files (*.cc);;All Files (*)"
        )

        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(data_to_save, f, indent=4)
                QMessageBox.information(self, "Save Successful", f"Preset '{preset_name}' saved to {file_path}")
                # Update the dialog's own combo box
                if preset_name not in [self.existing_presets_comboBox.itemText(i) for i in range(self.existing_presets_comboBox.count())]:
                    self.existing_presets_comboBox.addItem(preset_name)
                self.existing_presets_comboBox.setCurrentText(preset_name)
                self.saved_preset_name = preset_name # Added: Store the name for retrieval by parent
            except Exception as e:
                QMessageBox.critical(self, "Save Error", f"Failed to save preset: {e}")

    def accept(self):
        # Validate data before attempting to save or close
        data_to_save, is_valid, error_messages = self.get_concentration_data()

        if not is_valid:
            QMessageBox.critical(self, "Input Error", "\n".join(error_messages))
            return # Do not close the dialog if there are errors

        # If data is valid, set it and proceed with saving and closing
        self.new_conc_data = data_to_save # Store the valid data
        self.save_concentration_data() # This method will now use self.new_conc_data
        super().accept()

class Ui_MainWindow(QMainWindow):
    global workflows, conc_cols, _COLOR_PALETTE
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1000, 600)
        self.MainWindow = MainWindow
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(1000, 600))
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
        self.logo_chalf.setStyleSheet(u"image: url(images/CHalf Protein Logo.png);\n"
"border-color: rgb(0, 0, 0);\n"
"background-color: rgb(255,255,255);")

        self.horizontalLayout.addWidget(self.logo_chalf)

        self.logo_text = QLabel(self.centralwidget)
        self.logo_text.setObjectName(u"logo_text")
        font = QFont()
        font.setFamilies([u"Bahnschrift"])
        font.setPointSize(36)
        font.setBold(False)
        font.setItalic(False)
        self.logo_text.setFont(font)
        self.logo_text.setStyleSheet(u"font: 36pt \"Bahnschrift\";\n"
"background-color: rgb(255,255,255); color:black")
        self.logo_text.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.logo_text)

        self.logo_byu = QLabel(self.centralwidget)
        self.logo_byu.setObjectName(u"logo_byu")
        self.logo_byu.setStyleSheet(u"image: url(images/Brigham_Young_University_medallion.png);\n"
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
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
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
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy2)

        self.horizontalLayout_2.addWidget(self.label)

        self.workflow_comboBox = QComboBox(self.groupBox)
        
        self.workflow_comboBox.setObjectName(u"workflow_comboBox")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.workflow_comboBox.sizePolicy().hasHeightForWidth())
        self.workflow_comboBox.setSizePolicy(sizePolicy3)
        self.workflow_comboBox.setMinimumSize(QSize(300, 0))
        self.workflow_comboBox.setFocusPolicy(Qt.StrongFocus)
        self.update_workflows()

        self.horizontalLayout_2.addWidget(self.workflow_comboBox)

        self.load_workflow_pushButton = QPushButton(self.groupBox)
        self.load_workflow_pushButton.setObjectName(u"load_workflow_pushButton")
        sizePolicy3.setHeightForWidth(self.load_workflow_pushButton.sizePolicy().hasHeightForWidth())
        self.load_workflow_pushButton.setSizePolicy(sizePolicy3)
        self.load_workflow_pushButton.clicked.connect(self.load_workflow)

        self.horizontalLayout_2.addWidget(self.load_workflow_pushButton)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy4)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.save_workflow_pushButton = QPushButton(self.groupBox)
        self.save_workflow_pushButton.setObjectName(u"save_workflow_pushButton")
        sizePolicy3.setHeightForWidth(self.save_workflow_pushButton.sizePolicy().hasHeightForWidth())
        self.save_workflow_pushButton.setSizePolicy(sizePolicy3)
        self.save_workflow_pushButton.clicked.connect(self.write_parameter_file)

        self.horizontalLayout_2.addWidget(self.save_workflow_pushButton)

        self.open_workflow_folder_pushButton = QPushButton(self.groupBox)
        self.open_workflow_folder_pushButton.setObjectName(u"open_workflow_folder_pushButton")
        sizePolicy3.setHeightForWidth(self.open_workflow_folder_pushButton.sizePolicy().hasHeightForWidth())
        self.open_workflow_folder_pushButton.setSizePolicy(sizePolicy3)
        self.open_workflow_folder_pushButton.clicked.connect(self.open_workflows_folder)

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
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy5)
        self.label_5.setMinimumSize(QSize(40, 0))
        self.label_5.setMaximumSize(QSize(65, 16777215))

        self.horizontalLayout_3.addWidget(self.label_5)

        self.add_pp_files_pushButton = QPushButton(self.groupBox_2)
        self.add_pp_files_pushButton.setObjectName(u"add_pp_files_pushButton")
        self.add_pp_files_pushButton.clicked.connect(self.add_files)

        self.horizontalLayout_3.addWidget(self.add_pp_files_pushButton)

        self.remove_selected_pp_files_pushButton = QPushButton(self.groupBox_2)
        self.remove_selected_pp_files_pushButton.setObjectName(u"remove_selected_pp_files_pushButton")
        self.remove_selected_pp_files_pushButton.clicked.connect(self.remove_selected_rows)

        self.horizontalLayout_3.addWidget(self.remove_selected_pp_files_pushButton)

        self.clear_pp_files_pushButton = QPushButton(self.groupBox_2)
        self.clear_pp_files_pushButton.setObjectName(u"clear_pp_files_pushButton")
        self.clear_pp_files_pushButton.clicked.connect(self.clear_table)

        self.horizontalLayout_3.addWidget(self.clear_pp_files_pushButton)

        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_3.addWidget(self.label_6)

        self.save_manifest_pushButton = QPushButton(self.groupBox_2)
        self.save_manifest_pushButton.setObjectName(u"save_manifest_pushButton")
        self.save_manifest_pushButton.clicked.connect(self.save_manifest_file)

        self.horizontalLayout_3.addWidget(self.save_manifest_pushButton)

        self.load_manifest_pushButton = QPushButton(self.groupBox_2)
        self.load_manifest_pushButton.setObjectName(u"load_manifest_pushButton")
        self.load_manifest_pushButton.clicked.connect(self.load_manifest_file)

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
        self.label_27.setMinimumSize(QSize(145, 0))

        self.horizontalLayout_24.addWidget(self.label_27)

        self.condname_consecutive_pushButton = QPushButton(self.groupBox_2)
        self.condname_consecutive_pushButton.setObjectName(u"condname_consecutive_pushButton")
        self.condname_consecutive_pushButton.clicked.connect(self.set_condition_names_to_row_index)

        self.horizontalLayout_24.addWidget(self.condname_consecutive_pushButton)

        self.condname_filename_pushButton = QPushButton(self.groupBox_2)
        self.condname_filename_pushButton.clicked.connect(self.populate_condition_names)
        self.condname_filename_pushButton.setObjectName(u"condname_filename_pushButton")

        self.horizontalLayout_24.addWidget(self.condname_filename_pushButton)

        self.condname_dir_pushButton = QPushButton(self.groupBox_2)
        self.condname_dir_pushButton.setObjectName(u"condname_dir_pushButton")
        self.condname_dir_pushButton.clicked.connect(self.set_condition_names_to_parent_dir)

        self.horizontalLayout_24.addWidget(self.condname_dir_pushButton)


        self.verticalLayout_3.addLayout(self.horizontalLayout_24)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMaximumSize(QSize(145, 16777215))
        self.label_7.setMinimumSize(QSize(145, 16777215))

        self.horizontalLayout_4.addWidget(self.label_7)

        self.concentration_columns_comboBox = QComboBox(self.groupBox_2)
        self.concentration_columns_comboBox.setObjectName(u"concentration_columns_comboBox")
        self.concentration_columns_comboBox.setMinimumSize(QSize(300, 0))
        self.concentration_columns_comboBox.setFocusPolicy(Qt.StrongFocus)
        self.update_conc_cols()

        self.horizontalLayout_4.addWidget(self.concentration_columns_comboBox)

        self.assign_concentration_pushButton = QPushButton(self.groupBox_2)
        self.assign_concentration_pushButton.clicked.connect(self.fill_concentration_column)
        self.assign_concentration_pushButton.setObjectName(u"assign_concentration_pushButton")

        self.horizontalLayout_4.addWidget(self.assign_concentration_pushButton)

        self.create_concentration_pushButton = QPushButton(self.groupBox_2)
        self.create_concentration_pushButton.setObjectName(u"create_concentration_pushButton")
        self.create_concentration_pushButton.clicked.connect(self.show_edit_concentration_dialog)

        self.horizontalLayout_4.addWidget(self.create_concentration_pushButton)


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
        self.files_tableWidget.cellChanged.connect(self.check_and_fix_condition_names)

        self.files_tableWidget.setObjectName(u"files_tableWidget")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.files_tableWidget.sizePolicy().hasHeightForWidth())
        self.files_tableWidget.setSizePolicy(sizePolicy6)
        font1 = QFont()
        font1.setBold(False)
        font1.setItalic(False)
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
        self.files_tableWidget.horizontalHeader().setVisible(True)
        self.files_tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.files_tableWidget.horizontalHeader().setMinimumSectionSize(50)
        self.files_tableWidget.horizontalHeader().setDefaultSectionSize(250)
        self.files_tableWidget.horizontalHeader().setHighlightSections(True)
        self.files_tableWidget.horizontalHeader().setProperty(u"showSortIndicator", False)
        self.files_tableWidget.horizontalHeader().setStretchLastSection(True)
        self.files_tableWidget.verticalHeader().setVisible(False)
        self.files_tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.files_tableWidget.verticalHeader().setHighlightSections(True)
        
        ## Table update triggers
        self.files_tableWidget.model().dataChanged.connect(
            lambda topLeft, bottomRight, roles: self.update_conditions()
        )
        self.files_tableWidget.model().rowsInserted.connect(
            lambda parent, first, last: self.update_conditions()
        )
        self.files_tableWidget.model().rowsRemoved.connect(
            lambda parent, first, last: self.update_conditions()
        )

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
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding)
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
        self.run_chalf_checkBox.stateChanged.connect(self.update_rule_based_parameters)

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

        self.aa_l_checkBox = QCheckBox(self.groupBox_8)
        self.aa_l_checkBox.setObjectName(u"aa_l_checkBox")

        self.gridLayout_7.addWidget(self.aa_l_checkBox, 3, 3, 1, 1)

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
        self.label_14.setMinimumSize(QSize(210, 0))

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
        self.label_12.setMinimumSize(QSize(210, 0))

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
        self.label_13.setMinimumSize(QSize(210, 0))

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
        self.CI_filter_checkBox.setMinimumSize(QSize(210, 0))
        self.CI_filter_checkBox.setMaximumSize(QSize(210, 16777215))
        self.CI_filter_checkBox.setBaseSize(QSize(210, 0))
        self.CI_filter_checkBox.stateChanged.connect(self.update_rule_based_parameters)

        self.horizontalLayout_10.addWidget(self.CI_filter_checkBox)

        self.CI_doubleSpinBox = QDoubleSpinBox(self.groupBox_5)
        self.CI_doubleSpinBox.setObjectName(u"CI_doubleSpinBox")
        self.CI_doubleSpinBox.setFocusPolicy(Qt.StrongFocus)
        self.CI_doubleSpinBox.setSingleStep(0.010000000000000)
        self.CI_doubleSpinBox.setValue(0.350000000000000)
        self.CI_doubleSpinBox.setEnabled(False)

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
        self.label_16.setMinimumSize(QSize(210, 0))

        self.horizontalLayout_9.addWidget(self.label_16)

        self.fit_opt_comboBox = QComboBox(self.groupBox_5)
        self.fit_opt_comboBox.addItem("")
        self.fit_opt_comboBox.addItem("")
        self.fit_opt_comboBox.setObjectName(u"fit_opt_comboBox")
        self.fit_opt_comboBox.setFocusPolicy(Qt.StrongFocus)
        self.fit_opt_comboBox.currentIndexChanged.connect(self.update_rule_based_parameters)

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
        self.horizontalLayout_5.setSpacing(2)
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
        self.label_9.setMinimumSize(QSize(180, 0))
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
        sizePolicy8 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy8)
        self.label_10.setMinimumSize(QSize(160, 0))
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
        self.label_34.setMinimumSize(QSize(160, 0))

        self.horizontalLayout_37.addWidget(self.label_34)

        self.chalf_zero_criteria_comboBox = QComboBox(self.groupBox_3)
        self.chalf_zero_criteria_comboBox.addItem("")
        self.chalf_zero_criteria_comboBox.addItem("")
        self.chalf_zero_criteria_comboBox.addItem("")
        self.chalf_zero_criteria_comboBox.setObjectName(u"chalf_zero_criteria_comboBox")
        sizePolicy9 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
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
        self.graph_curves_checkBox = QCheckBox(self.groupBox_4)
        self.graph_curves_checkBox.setObjectName(u"graph_curves_checkBox")
        sizePolicy2.setHeightForWidth(self.graph_curves_checkBox.sizePolicy().hasHeightForWidth())
        self.graph_curves_checkBox.setSizePolicy(sizePolicy2)
        self.graph_curves_checkBox.stateChanged.connect(self.update_rule_based_parameters)

        self.horizontalLayout_25.addWidget(self.graph_curves_checkBox)

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
        self.label_17.setMaximumSize(QSize(80,20))
        self.label_17.setMinimumSize(QSize(80,20))

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
        self.label_19.setMinimumSize(QSize(80,20))
        self.label_19.setMaximumSize(QSize(80,20))

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
        self.graph_ci_checkBox.stateChanged.connect(self.update_rule_based_parameters)

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
        self.sg_checkBox.stateChanged.connect(self.update_rule_based_parameters)

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
        self.label_22.setMinimumSize(QSize(355, 0))
        self.label_22.setMaximumSize(QSize(355,20))

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
        self.label_23.setMinimumSize(QSize(355, 0))
        self.label_23.setMaximumSize(QSize(355,20))

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
        self.windowed_fitting_checkBox.stateChanged.connect(self.update_rule_based_parameters)

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
        self.mutation_search_checkBox = QCheckBox(self.groupBox_11)
        self.mutation_search_checkBox.setObjectName(u"mutation_search_checkBox")

        self.verticalLayout_13.addWidget(self.mutation_search_checkBox)

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
        self.qc_checkBox.stateChanged.connect(self.update_rule_based_parameters)

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
        self.qc_chalf_filters_pushButton.clicked.connect(self.copy_chalf_to_qc)

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
        self.qc_c_checkBox.setChecked(True)

        self.gridLayout_8.addWidget(self.qc_c_checkBox, 0, 3, 1, 1)

        self.qc_t_checkBox = QCheckBox(self.groupBox_13)
        self.qc_t_checkBox.setObjectName(u"qc_t_checkBox")

        self.gridLayout_8.addWidget(self.qc_t_checkBox, 2, 2, 1, 1)

        self.qc_h_checkBox = QCheckBox(self.groupBox_13)
        self.qc_h_checkBox.setObjectName(u"qc_h_checkBox")
        self.qc_h_checkBox.setChecked(True)

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
        self.qc_y_checkBox.setChecked(True)

        self.gridLayout_8.addWidget(self.qc_y_checkBox, 0, 0, 1, 1)

        self.qc_m_checkBox = QCheckBox(self.groupBox_13)
        self.qc_m_checkBox.setObjectName(u"qc_m_checkBox")
        self.qc_m_checkBox.setChecked(True)

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
        self.label_29.setMinimumSize(QSize(210, 0))

        self.horizontalLayout_30.addWidget(self.label_29)

        self.qc_chalf_min_doubleSpinBox = QDoubleSpinBox(self.groupBox_14)
        self.qc_chalf_min_doubleSpinBox.setObjectName(u"qc_chalf_min_doubleSpinBox")
        self.qc_chalf_min_doubleSpinBox.setSingleStep(0.010000000000000)
        self.qc_chalf_min_doubleSpinBox.setMinimumSize(QSize(250, 0))

        self.horizontalLayout_30.addWidget(self.qc_chalf_min_doubleSpinBox)


        self.verticalLayout_15.addLayout(self.horizontalLayout_30)

        self.horizontalLayout_27 = QHBoxLayout()
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.label_30 = QLabel(self.groupBox_14)
        self.label_30.setObjectName(u"label_30")
        sizePolicy4.setHeightForWidth(self.label_30.sizePolicy().hasHeightForWidth())
        self.label_30.setSizePolicy(sizePolicy4)
        self.label_30.setMinimumSize(QSize(210, 0))

        self.horizontalLayout_27.addWidget(self.label_30)

        self.qc_chalf_max_doubleSpinBox = QDoubleSpinBox(self.groupBox_14)
        self.qc_chalf_max_doubleSpinBox.setObjectName(u"qc_chalf_max_doubleSpinBox")
        self.qc_chalf_max_doubleSpinBox.setSingleStep(0.010000000000000)
        self.qc_chalf_max_doubleSpinBox.setValue(3.480000000000000)
        self.qc_chalf_max_doubleSpinBox.setMinimumSize(QSize(250, 0))

        self.horizontalLayout_27.addWidget(self.qc_chalf_max_doubleSpinBox)


        self.verticalLayout_15.addLayout(self.horizontalLayout_27)

        self.horizontalLayout_29 = QHBoxLayout()
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.label_31 = QLabel(self.groupBox_14)
        self.label_31.setObjectName(u"label_31")
        sizePolicy4.setHeightForWidth(self.label_31.sizePolicy().hasHeightForWidth())
        self.label_31.setSizePolicy(sizePolicy4)
        self.label_31.setMinimumSize(QSize(210, 0))

        self.horizontalLayout_29.addWidget(self.label_31)

        self.qc_rsq_doubleSpinBox = QDoubleSpinBox(self.groupBox_14)
        self.qc_rsq_doubleSpinBox.setObjectName(u"qc_rsq_doubleSpinBox")
        self.qc_rsq_doubleSpinBox.setMaximum(0.990000000000000)
        self.qc_rsq_doubleSpinBox.setSingleStep(0.010000000000000)
        self.qc_rsq_doubleSpinBox.setValue(0.800000000000000)
        self.qc_rsq_doubleSpinBox.setMinimumSize(QSize(250, 0))

        self.horizontalLayout_29.addWidget(self.qc_rsq_doubleSpinBox)


        self.verticalLayout_15.addLayout(self.horizontalLayout_29)

        self.horizontalLayout_32 = QHBoxLayout()
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.qc_ci_checkBox = QCheckBox(self.groupBox_14)
        self.qc_ci_checkBox.setObjectName(u"qc_ci_checkBox")
        sizePolicy2.setHeightForWidth(self.qc_ci_checkBox.sizePolicy().hasHeightForWidth())
        self.qc_ci_checkBox.setSizePolicy(sizePolicy2)
        self.qc_ci_checkBox.setMinimumSize(QSize(210, 0))
        self.qc_ci_checkBox.setMaximumSize(QSize(210, 17))
        self.qc_ci_checkBox.stateChanged.connect(self.update_rule_based_parameters)

        self.horizontalLayout_32.addWidget(self.qc_ci_checkBox)

        self.qc_ci_doubleSpinBox = QDoubleSpinBox(self.groupBox_14)
        self.qc_ci_doubleSpinBox.setObjectName(u"qc_ci_doubleSpinBox")
        self.qc_ci_doubleSpinBox.setSingleStep(0.010000000000000)
        self.qc_ci_doubleSpinBox.setValue(0.350000000000000)
        self.qc_ci_doubleSpinBox.setMinimumSize(QSize(250, 0))

        self.horizontalLayout_32.addWidget(self.qc_ci_doubleSpinBox)


        self.verticalLayout_15.addLayout(self.horizontalLayout_32)

        self.horizontalLayout_28 = QHBoxLayout()
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.label_32 = QLabel(self.groupBox_14)
        self.label_32.setObjectName(u"label_32")
        sizePolicy4.setHeightForWidth(self.label_32.sizePolicy().hasHeightForWidth())
        self.label_32.setSizePolicy(sizePolicy4)
        self.label_32.setMinimumSize(QSize(210, 0))

        self.horizontalLayout_28.addWidget(self.label_32)

        self.qc_priority_comboBox = QComboBox(self.groupBox_14)
        self.qc_priority_comboBox.addItem("")
        self.qc_priority_comboBox.addItem("")
        self.qc_priority_comboBox.setObjectName(u"qc_priority_comboBox")
        self.qc_priority_comboBox.setMinimumSize(QSize(250, 0))
        self.qc_priority_comboBox.currentIndexChanged.connect(self.update_rule_based_parameters)

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
        self.qc_vis_generate_checkBox.stateChanged.connect(self.update_rule_based_parameters)

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
        self.rm_checkBox.setChecked(False)
        self.rm_checkBox.stateChanged.connect(self.update_rule_based_parameters)

        self.verticalLayout_25.addWidget(self.rm_checkBox)

        self.horizontalLayout_46 = QHBoxLayout()
        self.horizontalLayout_46.setObjectName(u"horizontalLayout_46")
        self.label_46 = QLabel(self.groupBox_25)
        self.label_46.setObjectName(u"label_46")
        sizePolicy4.setHeightForWidth(self.label_46.sizePolicy().hasHeightForWidth())
        self.label_46.setSizePolicy(sizePolicy4)
        self.label_46.setMinimumSize(QSize(90, 0))
        self.label_46.setMaximumSize(QSize(90, 20))

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
        self.label_47.setMinimumSize(QSize(90, 0))
        self.label_47.setMaximumSize(QSize(90, 20))

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
        self.label_48.setMinimumSize(QSize(90, 0))
        self.label_48.setMaximumSize(QSize(90, 20))

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
        self.rm_trendline_checkBox.stateChanged.connect(self.update_rule_based_parameters)

        self.verticalLayout_26.addWidget(self.rm_trendline_checkBox)

        self.horizontalLayout_49 = QHBoxLayout()
        self.horizontalLayout_49.setObjectName(u"horizontalLayout_49")
        self.horizontalLayout_49.setContentsMargins(-1, 0, -1, -1)
        self.label_49 = QLabel(self.groupBox_26)
        self.label_49.setObjectName(u"label_49")
        sizePolicy4.setHeightForWidth(self.label_49.sizePolicy().hasHeightForWidth())
        self.label_49.setSizePolicy(sizePolicy4)
        self.label_49.setMinimumSize(QSize(90, 0))
        self.label_49.setMaximumSize(QSize(90, 20))

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
        self.label_50.setMinimumSize(QSize(90, 0))
        self.label_50.setMaximumSize(QSize(90, 20))

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
        self.rm_custom_ann_select_pushButton.clicked.connect(self.rm_select_ann_file)
        
        self.horizontalLayout_51.addWidget(self.rm_custom_ann_select_pushButton)


        self.gridLayout_5.addLayout(self.horizontalLayout_51, 4, 0, 1, 1)

        self.rm_allsites_checkBox = QCheckBox(self.groupBox_27)
        self.rm_allsites_checkBox.setObjectName(u"rm_allsites_checkBox")
        self.rm_allsites_checkBox.setChecked(True)

        self.gridLayout_5.addWidget(self.rm_allsites_checkBox, 0, 0, 1, 1)

        self.rm_stats_reference_checkBox = QCheckBox(self.groupBox_27)
        self.rm_stats_reference_checkBox.setObjectName(u"rm_stats_reference_checkBox")
        self.rm_stats_reference_checkBox.setChecked(True)
        self.rm_stats_reference_checkBox.stateChanged.connect(self.update_rule_based_parameters)

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
        self.crm_checkBox.stateChanged.connect(self.update_rule_based_parameters)

        self.verticalLayout_23.addWidget(self.crm_checkBox)

        self.horizontalLayout_40 = QHBoxLayout()
        self.horizontalLayout_40.setObjectName(u"horizontalLayout_40")
        self.label_40 = QLabel(self.groupBox_18)
        self.label_40.setObjectName(u"label_40")
        sizePolicy4.setHeightForWidth(self.label_40.sizePolicy().hasHeightForWidth())
        self.label_40.setSizePolicy(sizePolicy4)
        self.label_40.setMinimumSize(QSize(90, 0))
        self.label_40.setMaximumSize(QSize(90, 20))

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
        self.label_41.setMinimumSize(QSize(90, 0))
        self.label_41.setMaximumSize(QSize(90, 20))

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
        self.label_42.setMinimumSize(QSize(90, 0))
        self.label_42.setMaximumSize(QSize(90, 20))

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
        self.crm_trendline_checkBox.stateChanged.connect(self.update_rule_based_parameters)

        self.verticalLayout_24.addWidget(self.crm_trendline_checkBox)

        self.horizontalLayout_43 = QHBoxLayout()
        self.horizontalLayout_43.setObjectName(u"horizontalLayout_43")
        self.horizontalLayout_43.setContentsMargins(-1, 0, -1, -1)
        self.label_43 = QLabel(self.groupBox_23)
        self.label_43.setObjectName(u"label_43")
        sizePolicy4.setHeightForWidth(self.label_43.sizePolicy().hasHeightForWidth())
        self.label_43.setSizePolicy(sizePolicy4)
        self.label_43.setMinimumSize(QSize(90, 0))
        self.label_43.setMaximumSize(QSize(90, 20))

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
        self.label_44.setMinimumSize(QSize(90, 0))
        self.label_44.setMaximumSize(QSize(90, 20))

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
        self.crm_stats_reference_checkBox.stateChanged.connect(self.update_rule_based_parameters)

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
        self.crm_custom_ann_select_pushButton.clicked.connect(self.crm_select_ann_file)

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
        self.dm_checkBox = QCheckBox(self.groupBox_21)
        self.dm_checkBox.setObjectName(u"dm_checkBox")
        self.dm_checkBox.setChecked(True)
        self.dm_checkBox.stateChanged.connect(self.update_rule_based_parameters)

        self.verticalLayout_27.addWidget(self.dm_checkBox)

        self.horizontalLayout_52 = QHBoxLayout()
        self.horizontalLayout_52.setObjectName(u"horizontalLayout_52")
        self.label_52 = QLabel(self.groupBox_21)
        self.label_52.setObjectName(u"label_52")
        sizePolicy4.setHeightForWidth(self.label_52.sizePolicy().hasHeightForWidth())
        self.label_52.setSizePolicy(sizePolicy4)
        self.label_52.setMinimumSize(QSize(100, 0))
        self.label_52.setMaximumSize(QSize(100, 20))

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
        self.label_53.setMinimumSize(QSize(100, 0))
        self.label_53.setMaximumSize(QSize(100, 20))

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
        self.label_54.setMinimumSize(QSize(100, 0))
        self.label_54.setMaximumSize(QSize(100, 20))

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
        self.dm_trendline_checkBox.stateChanged.connect(self.update_rule_based_parameters)

        self.verticalLayout_28.addWidget(self.dm_trendline_checkBox)

        self.horizontalLayout_55 = QHBoxLayout()
        self.horizontalLayout_55.setObjectName(u"horizontalLayout_55")
        self.horizontalLayout_55.setContentsMargins(-1, 0, -1, -1)
        self.label_55 = QLabel(self.groupBox_28)
        self.label_55.setObjectName(u"label_55")
        sizePolicy4.setHeightForWidth(self.label_55.sizePolicy().hasHeightForWidth())
        self.label_55.setSizePolicy(sizePolicy4)
        self.label_55.setMinimumSize(QSize(100, 0))
        self.label_55.setMaximumSize(QSize(100, 20))

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
        self.label_56.setMinimumSize(QSize(100, 0))
        self.label_56.setMaximumSize(QSize(100, 20))

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
        self.label_37.setMinimumSize(QSize(120, 0))
        self.label_37.setMaximumSize(QSize(120, 20))

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
        self.dm_kde_sig_cutoff_checkBox.setMinimumSize(QSize(120, 0))
        self.dm_kde_sig_cutoff_checkBox.setMaximumSize(QSize(120, 20))
        self.dm_kde_sig_cutoff_checkBox.stateChanged.connect(self.update_rule_based_parameters)

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
        self.dm_custom_ann_select_pushButton.clicked.connect(self.dm_select_ann_file)

        self.horizontalLayout_57.addWidget(self.dm_custom_ann_select_pushButton)


        self.gridLayout_6.addLayout(self.horizontalLayout_57, 4, 0, 1, 1)

        self.dm_allsites_checkBox = QCheckBox(self.groupBox_29)
        self.dm_allsites_checkBox.setObjectName(u"dm_allsites_checkBox")
        self.dm_allsites_checkBox.setChecked(True)

        self.gridLayout_6.addWidget(self.dm_allsites_checkBox, 0, 0, 1, 1)

        self.dm_stats_reference_checkBox = QCheckBox(self.groupBox_29)
        self.dm_stats_reference_checkBox.setObjectName(u"dm_stats_reference_checkBox")
        self.dm_stats_reference_checkBox.setChecked(True)
        self.dm_stats_reference_checkBox.stateChanged.connect(self.update_rule_based_parameters)

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
        self.cs_checkBox.stateChanged.connect(self.update_rule_based_parameters)

        self.verticalLayout_29.addWidget(self.cs_checkBox)

        self.horizontalLayout_60 = QHBoxLayout()
        self.horizontalLayout_60.setObjectName(u"horizontalLayout_60")
        self.label_60 = QLabel(self.groupBox_19)
        self.label_60.setObjectName(u"label_60")
        sizePolicy4.setHeightForWidth(self.label_60.sizePolicy().hasHeightForWidth())
        self.label_60.setSizePolicy(sizePolicy4)
        self.label_60.setMinimumSize(QSize(90, 0))
        self.label_60.setMaximumSize(QSize(90, 20))

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
        self.label_59.setMinimumSize(QSize(90, 0))
        self.label_59.setMaximumSize(QSize(90, 20))

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
        self.label_58.setMinimumSize(QSize(90, 0))
        self.label_58.setMaximumSize(QSize(90, 20))

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
        self.visualization_tableWidget = QTableWidget(self.groupBox_16)
        if (self.visualization_tableWidget.columnCount() < 4):
            self.visualization_tableWidget.setColumnCount(4)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.visualization_tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.visualization_tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.visualization_tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.visualization_tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem9)
        self.visualization_tableWidget.setObjectName(u"visaulization_tableWidget")
        self.visualization_tableWidget.setEnabled(True)
        sizePolicy.setHeightForWidth(self.visualization_tableWidget.sizePolicy().hasHeightForWidth())
        self.visualization_tableWidget.setSizePolicy(sizePolicy)
        self.visualization_tableWidget.setMinimumSize(QSize(400, 200))
        self.visualization_tableWidget.setAutoFillBackground(False)
        self.visualization_tableWidget.horizontalHeader().setDefaultSectionSize(110)
        self.visualization_tableWidget.horizontalHeader().setStretchLastSection(True)
        self.visualization_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.verticalLayout_17.addWidget(self.visualization_tableWidget)

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
        self.vis_add_pushButton.clicked.connect(self.add_selected_condition_to_visualization_table)

        self.horizontalLayout_34.addWidget(self.vis_add_pushButton)

        self.vis_add_all_pushButton = QPushButton(self.groupBox_22)
        self.vis_add_all_pushButton.setObjectName(u"vis_add_all_pushButton")
        self.vis_add_all_pushButton.clicked.connect(self.add_all_conditions_to_visualization_table)

        self.horizontalLayout_34.addWidget(self.vis_add_all_pushButton)

        self.vis_remove_pushButton = QPushButton(self.groupBox_22)
        self.vis_remove_pushButton.setObjectName(u"vis_remove_pushButton")
        self.vis_remove_pushButton.clicked.connect(self.remove_highlighted_conditions_from_visualization_table)

        self.horizontalLayout_34.addWidget(self.vis_remove_pushButton)

        self.vis_remove_all_pushButton = QPushButton(self.groupBox_22)
        self.vis_remove_all_pushButton.setObjectName(u"vis_remove_all_pushButton")
        self.vis_remove_all_pushButton.clicked.connect(self.remove_all_conditions_from_visualization_table)

        self.horizontalLayout_34.addWidget(self.vis_remove_all_pushButton)

        self.horizontalLayout_34.setStretch(0, 1)

        self.verticalLayout_20.addLayout(self.horizontalLayout_34)

        self.horizontalLayout_36 = QHBoxLayout()
        self.horizontalLayout_36.setObjectName(u"horizontalLayout_36")
        self.vis_set_group_pushButton = QPushButton(self.groupBox_22)
        self.vis_set_group_pushButton.setObjectName(u"vis_set_group_pushButton")
        self.vis_set_group_pushButton.clicked.connect(self.set_group_for_selected_rows)

        self.horizontalLayout_36.addWidget(self.vis_set_group_pushButton)

        self.vis_set_ref_pushButton = QPushButton(self.groupBox_22)
        self.vis_set_ref_pushButton.setObjectName(u"vis_set_ref_pushButton")
        self.vis_set_ref_pushButton.clicked.connect(self.set_reference_for_selected_rows)

        self.horizontalLayout_36.addWidget(self.vis_set_ref_pushButton)

        self.vis_set_exp_pushButton = QPushButton(self.groupBox_22)
        self.vis_set_exp_pushButton.setObjectName(u"vis_set_exp_pushButton")
        self.vis_set_exp_pushButton.clicked.connect(self.set_experimental_for_selected_rows)

        self.horizontalLayout_36.addWidget(self.vis_set_exp_pushButton)

        self.vis_set_color_pushButton = QPushButton(self.groupBox_22)
        self.vis_set_color_pushButton.setObjectName(u"vis_set_color_pushButton")
        self.vis_set_color_pushButton.clicked.connect(self.set_color_for_selected_conditions)

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
        self.run_browse_pushButton.clicked.connect(self.browse_output_directory)

        self.horizontalLayout_39.addWidget(self.run_browse_pushButton)

        self.run_open_pushButton = QPushButton(self.run_tab)
        self.run_open_pushButton.setObjectName(u"run_open_pushButton")
        self.run_open_pushButton.clicked.connect(self.open_output_directory)

        self.horizontalLayout_39.addWidget(self.run_open_pushButton)


        self.verticalLayout_30.addLayout(self.horizontalLayout_39)

        self.horizontalLayout_61 = QHBoxLayout()
        self.horizontalLayout_61.setObjectName(u"horizontalLayout_61")
        self.run_start_pushButton = QPushButton(self.run_tab)
        self.run_start_pushButton.setObjectName(u"run_start_pushButton")
        self.run_start_pushButton.clicked.connect(self.start_run)

        self.horizontalLayout_61.addWidget(self.run_start_pushButton)

        self.run_stop_pushButton = QPushButton(self.run_tab)
        self.run_stop_pushButton.setObjectName(u"run_stop_pushButton")
        self.run_stop_pushButton.clicked.connect(self.stop_run)
        self.run_stop_pushButton.setEnabled(False)

        self.horizontalLayout_61.addWidget(self.run_stop_pushButton)
        
        self.run_export_headless = QPushButton(self.run_tab)
        self.run_export_headless.setObjectName(u"run_export_headless")
        self.run_export_headless.clicked.connect(self.export_headless)

        self.horizontalLayout_61.addWidget(self.run_export_headless)

        self.run_log_export_pushButton = QPushButton(self.run_tab)
        self.run_log_export_pushButton.setObjectName(u"run_log_export_pushButton")
        self.run_log_export_pushButton.clicked.connect(self.export_log_manual)

        self.horizontalLayout_61.addWidget(self.run_log_export_pushButton)

        self.run_log_clear_pushButton = QPushButton(self.run_tab)
        self.run_log_clear_pushButton.setObjectName(u"run_log_clear_pushButton")
        self.run_log_clear_pushButton.clicked.connect(self.clear_log)

        self.horizontalLayout_61.addWidget(self.run_log_clear_pushButton)


        self.verticalLayout_30.addLayout(self.horizontalLayout_61)

        self.groupBox_30 = QGroupBox(self.run_tab)
        self.groupBox_30.setObjectName(u"groupBox_30")
        self.verticalLayout_31 = QVBoxLayout(self.groupBox_30)
        self.verticalLayout_31.setObjectName(u"verticalLayout_31")
        self.run_log_textEdit = QTextEdit(self.groupBox_30)
        self.run_log_textEdit.setObjectName(u"run_log_textEdit")
        self.run_log_textEdit.setReadOnly(True)
        self.thread_pool = QThreadPool()
        self.thread_pool.setMaxThreadCount(1)
        self.logger = global_logger
        '''self.logger = TextEditLogger(self.run_log_textEdit)
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        sys.stdout = self.logger
        sys.stderr = self.logger'''

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
        self.update_rule_based_parameters()
        self.update_rule_based_parameters()


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"CHalf v4.3", None))
        self.logo_chalf.setText("")
        self.logo_text.setText(QCoreApplication.translate("MainWindow", u"CHalf v4.3 - JC Price Lab", None))
        self.logo_byu.setText("")
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Workflows", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Select a workflow:", None))
        #self.workflow_comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Default (IPSA)", None))
        #self.workflow_comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"SPROX", None))

        self.load_workflow_pushButton.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Save current settings as workflow:", None))
        self.save_workflow_pushButton.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.open_workflow_folder_pushButton.setText(QCoreApplication.translate("MainWindow", u"Open Folder", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>For information on how workflows work <a href=\"https://github.com/JC-Price/Chalf_public/blob/3b80c42da9707da77812db1828d6da7efc31f32c/Demos%20and%20Documentation/workflows_tutorial.md\"><span style=\" text-decoration: underline; color:#0000ff;\">see this tutorial</span></a>.</p></body></html>", None))
        self.label_3.setOpenExternalLinks(True)
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Input Files", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>CHalf takes an input of csv files with quantified and identified peptides. Formatting matters for the analysis. See this <a href=\"https://github.com/JC-Price/Chalf_public/blob/3b80c42da9707da77812db1828d6da7efc31f32c/Demos%20and%20Documentation/formatting_guide.md\"><span style=\" text-decoration: underline; color:#0000ff;\">formatting guide</span></a> before starting.</p></body></html>", None))
        self.label_4.setOpenExternalLinks(True)
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>File options:</p></body></html>", None))
        self.add_pp_files_pushButton.setText(QCoreApplication.translate("MainWindow", u"Add files", None))
        self.remove_selected_pp_files_pushButton.setText(QCoreApplication.translate("MainWindow", u"Remove selected files", None))
        self.clear_pp_files_pushButton.setText(QCoreApplication.translate("MainWindow", u"Clear files", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"right\">Options for rerunning files:</p></body></html>", None))
        self.save_manifest_pushButton.setText(QCoreApplication.translate("MainWindow", u"Save as manifest", None))
        self.load_manifest_pushButton.setText(QCoreApplication.translate("MainWindow", u"Load manifest", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Named concentration columns are paired to concentration values for use in curve fitting. You can save pairings of column names and concentration values by selecting \"New\" under the dropdown and can assign existing pairings to conditions using \"Assign to condition.\" \"Edit\" allows you to make changes to your existing presets. Presets will be saved in the presets folder in the CHalf base directory.", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"Set selected condition names:", None))
        self.condname_consecutive_pushButton.setText(QCoreApplication.translate("MainWindow", u"Consecutively", None))
        self.condname_filename_pushButton.setText(QCoreApplication.translate("MainWindow", u"By file name", None))
        self.condname_dir_pushButton.setText(QCoreApplication.translate("MainWindow", u"By parent directory", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Set concentration columns:", None))
        #self.concentration_columns_comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Default (IPSA)", None))

        self.assign_concentration_pushButton.setText(QCoreApplication.translate("MainWindow", u"Assign to selected conditions", None))
        self.create_concentration_pushButton.setText(QCoreApplication.translate("MainWindow", u"Create/Edit", None))
        ___qtablewidgetitem = self.files_tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"File (path)", None));
        ___qtablewidgetitem1 = self.files_tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Condition (unique string)", None));
        ___qtablewidgetitem2 = self.files_tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Concentration columns (preset)", None));
        
        
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
        self.aa_l_checkBox.setText(QCoreApplication.translate("MainWindow", u"L", None))
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
        self.graph_curves_checkBox.setText(QCoreApplication.translate("MainWindow", u"Generate Curve Figures (increases computation time)", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"File Type:", None))
        self.graphing_filetype_comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u".jpg", None))
        self.graphing_filetype_comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u".png", None))
        self.graphing_filetype_comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u".svg", None))

        self.label_17.setText(QCoreApplication.translate("MainWindow", u"C\u00bd Minimum:", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"R\u00b2 Cutoff:", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"C\u00bd Maximum:", None))
        self.graph_ci_checkBox.setText(QCoreApplication.translate("MainWindow", u"Confidence Interval / Range Cutoff:", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"Experimental Options (use at your own risk)", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>This section contains experimental modifcations to CHalf that were tested during development. Each of these tools has a specific use case where they may be beneficial but was ultimately not included in the default CHalf calculation method as they only apply in specific use cases and can lead to incorrect conclusions if used outside of the correct use case. We have included them in this version of CHalf for optional use, but we only recommend using them with caution and where their designed use case applies. These tools are alos less optimized for use in CHalf, meaning that incorrect usage can lead to errors that will not be supported in later development. For more infomration on each of these experimental options, see <a href=\"https://github.com/JC-Price/Chalf_public/blob/3b80c42da9707da77812db1828d6da7efc31f32c/Demos%20and%20Documentation/experimental_options_guide.md\"><span style=\" text-decoration: underline; color:#0000ff;\">CHalf Experimental Options</span></a> in the documentation.</p></body></html>", None))
        self.label_20.setOpenExternalLinks(True)
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
        self.mutation_search_checkBox.setText(QCoreApplication.translate("MainWindow", u"Mutation Search", None))
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
        self.dm_checkBox.setText(QCoreApplication.translate("MainWindow", u"Delta Mapper", None))
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
        ___qtablewidgetitem6 = self.visualization_tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Condition", None));
        ___qtablewidgetitem7 = self.visualization_tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"Group", None));
        ___qtablewidgetitem8 = self.visualization_tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"Class", None));
        ___qtablewidgetitem9 = self.visualization_tableWidget.horizontalHeaderItem(3)
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
        self.run_export_headless.setText(QCoreApplication.translate("MainWindow", u"Export Headless Run", None))
        self.run_log_export_pushButton.setText(QCoreApplication.translate("MainWindow", u"Export Log", None))
        self.run_log_clear_pushButton.setText(QCoreApplication.translate("MainWindow", u"Clear Log", None))
        self.groupBox_30.setTitle(QCoreApplication.translate("MainWindow", u"Log", None))
        self.mainTabWidget.setTabText(self.mainTabWidget.indexOf(self.run_tab), QCoreApplication.translate("MainWindow", u"Run", None))
    # retranslateUi
    
    def load_parameter(self, key, parameter):
        possible_parameters = ['chalf', 'chalf.search.light', 'chalf.search.residues', 'chalf.filter.min', 'chalf.filter.max', 'chalf.filter.rsq', 'chalf.filter.ci_filter', 'chalf.filter.ci_value', 'chalf.filter.optimize', 'chalf.filter.sig_only', 'chalf.fitting.min_pts', 'chalf.fitting.outlier_trimming', 'chalf.fitting.outlier_cutoff', 'chalf.fitting.zero_criteria', 'chalf.graphing.graph', 'chalf.graphing.file_type', 'chalf.graphing.min', 'chalf.graphing.max', 'chalf.graphing.rsq', 'chalf.graphing.ci_filter', 'chalf.graphing.ci_value', 'chalf.experimental.sg.smooth', 'chalf.experimental.sg.window', 'chalf.experimental.sg.order', 'chalf.experimental.wf.window_fit', 'chalf.experimental.wf.window', 'chalf.experimental.ms.mutations', 'qc', 'qc.search.residues', 'qc.filter.min', 'qc.filter.max', 'qc.filter.rsq', 'qc.filter.ci_filter', 'qc.filter.ci_value', 'qc.filter.optimize', 'visualization.qc.report', 'visualization.qc.open', 'visualization.rm', 'visualization.rm.file_type', 'visualization.rm.min', 'visualization.rm.max', 'visualization.rm.trendlines.trendline', 'visualization.rm.trendlines.min', 'visualization.rm.trendlines.window', 'visualization.rm.other.all_curves', 'visualization.rm.other.reference_stats', 'visualization.rm.other.rm_trendline_stats', 'visualization.rm.other.mutation_search', 'visualization.rm.other.advanced', 'visualization.crm', 'visualization.crm.file_type', 'visualization.crm.min', 'visualization.crm.max', 'visualization.crm.trendlines.trendline', 'visualization.crm.trendlines.min', 'visualization.crm.trendlines.window', 'visualization.crm.other.all_curves', 'visualization.crm.other.reference_stats', 'visualization.crm.other.crm_trendline_stats','visualization.crm.other.shared_only', 'visualization.crm.other.mutation_search', 'visualization.crm.other.advanced', 'visualization.dm', 'visualization.dm.file_type', 'visualization.dm.min', 'visualization.dm.max', 'visualization.dm.trendlines.trendline', 'visualization.dm.trendlines.min', 'visualization.dm.trendlines.window', 'visualization.dm.kde.min_pts', 'visualization.dm.sig_filter', 'visualization.dm.sig_value', 'visualization.dm.other.all_curves', 'visualization.dm.other.reference_stats', 'visualization.dm.other.dm_trendline_stats', 'visualization.dm.other.mutation_search', 'visualization.dm.other.advanced', 'visualization.cs', 'visualization.cs.file_type', 'visualization.cs.min', 'visualization.cs.max']
        if key not in possible_parameters: print(f'Problem at {key}. Ignoring this parameter')
        ### CHALF SETTINGS ###
        if key == 'chalf':
            try:
                self.run_chalf_checkBox.setChecked(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'chalf.search.light':
            try:
                self.light_search_checkBox.setChecked(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'chalf.search.residues':
            try:
                aa_list = 'arndcqeghilkmfpstwyv'
                for aa in parameter:
                    aa = aa.lower()
                    if aa not in aa_list: print(f'{aa} not recognized. Skipping.'); continue
                    aa_list = aa_list.replace(aa,'')
                    checkbox_name = f"aa_{aa}_checkBox"  # Corrected variable name
    
                    # Use getattr to access the attribute and set it.  Handles the case where the attribute *might* not exist.
                    if hasattr(self, checkbox_name):
                         checkbox = getattr(self, checkbox_name)
                         checkbox.setChecked(True)
                    else:
                        print(f"Warning: Checkbox '{checkbox_name}' not found.") #Important:  Handles missing attribute.
                    
                for aa in aa_list:
                    checkbox_name = f"aa_{aa}_checkBox"  # Corrected variable name
                    if hasattr(self, checkbox_name):
                         checkbox = getattr(self, checkbox_name)
                         checkbox.setChecked(False)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        ## CHALF FILTER SETTINGS ##
        elif key == 'chalf.filter.min':
            try:
                self.chalf_min_doubleSpinBox.setValue(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'chalf.filter.max':
            try:
                self.chalf_max_doubleSpinBox.setValue(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'chalf.filter.rsq':
            try:
                self.rsq_doubleSpinBox.setValue(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'chalf.filter.ci_filter':
            try:
                self.CI_filter_checkBox.setChecked(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'chalf.filter.ci_value':
            try:
                self.CI_doubleSpinBox.setValue(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'chalf.filter.optimize':
            try:
                if parameter=='rsq':self.fit_opt_comboBox.setCurrentText("R\u00b2")
                elif parameter=='ci':self.fit_opt_comboBox.setCurrentText('Confidence Interval')
                else:self.fit_opt_comboBox.setCurrentText("R\u00b2")
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'chalf.filter.sig_only':
            try:
                self.sig_only_checkBox.setChecked(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        ## CHALF FITTING OPTIONS ##
        elif key == 'chalf.fitting.min_pts':
            try:
                self.min_pts_spinBox.setValue(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'chalf.fitting.min_pts':
            try:
                self.min_pts_spinBox.setValue(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'chalf.fitting.outlier_trimming':
            try:
                self.trimming_checkBox.setChecked(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'chalf.fitting.outlier_cutoff':
            try:
                self.out_cut_spinBox.setValue(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'chalf.fitting.zero_criteria':
            try:
                if parameter=='remove':self.chalf_zero_criteria_comboBox.setCurrentText("Remove")
                elif parameter=='keep':self.chalf_zero_criteria_comboBox.setCurrentText('Keep')
                elif parameter=='impute':self.chalf_zero_criteria_comboBox.setCurrentText('Impute')
                else:self.chalf_zero_criteria_comboBox.setCurrentText("Remove")
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        ## CHALF GRAPHING OPTIONS ##
        elif key == 'chalf.graphing.graph':
            try:
                self.graph_curves_checkBox.setChecked(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'chalf.graphing.file_type':
            try:
                if parameter=='jpg':self.graphing_filetype_comboBox.setCurrentText('.jpg')
                elif parameter=='png':self.graphing_filetype_comboBox.setCurrentText('.png')
                elif parameter=='svg':self.graphing_filetype_comboBox.setCurrentText('.svg')
                else:self.graphing_filetype_comboBox.setCurrentText('.jpg')
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'chalf.graphing.min':
            try:
                self.graph_chalf_min_doubleSpinBox.setValue(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'chalf.graphing.max':
            try:
                self.graph_chalf_max_doubleSpinBox.setValue(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'chalf.graphing.rsq':
            try:
                self.graph_rsq_doubleSpinBox.setValue(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'chalf.graphing.ci_filter':
            try:
                self.graph_ci_checkBox.setChecked(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'chalf.graphing.ci_value':
            try:
                self.graph_ci_doubleSpinBox.setValue(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        ## CHALF EXPERIMENTAL OPTIONS ##
        elif key == 'chalf.experimental.sg.smooth':
            try:
                self.sg_checkBox.setChecked(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'chalf.experimental.sg.window':
            try:
                self.sg_window_spinBox.setValue(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'chalf.experimental.sg.order':
            try:
                self.sg_order_spinBox.setValue(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'chalf.experimental.wf.window_fit':
            try:
                self.windowed_fitting_checkBox.setChecked(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'chalf.experimental.wf.window':
            try:
                self.wf_window_spinBox.setValue(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'chalf.experimental.ms.mutations':
            try:
                self.mutation_search_checkBox.setChecked(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
                ## QUALITY CONTROL SEARCH SETTINGS ##
        elif key == 'qc':
            try:
                self.qc_checkBox.setChecked(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'qc.search.residues':
            try:
                aa_list = 'arndcqeghilkmfpstwyv'
                for aa in parameter:
                    aa = aa.lower()
                    if aa not in aa_list: print(f'{aa} not recognized in QC residues. Skipping.'); continue
                    aa_list = aa_list.replace(aa,'')
                    checkbox_name = f"qc_{aa}_checkBox"
                    if hasattr(self, checkbox_name):
                        checkbox = getattr(self, checkbox_name)
                        checkbox.setChecked(True)
                    else:
                        print(f"Warning: QC Checkbox '{checkbox_name}' not found.")
                for aa in aa_list:
                    checkbox_name = f"qc_{aa}_checkBox"
                    if hasattr(self, checkbox_name):
                        checkbox = getattr(self, checkbox_name)
                        checkbox.setChecked(False)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        ## QUALITY CONTROL FILTER OPTIONS ##
        elif key == 'qc.filter.min':
            try:
                self.qc_chalf_min_doubleSpinBox.setValue(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'qc.filter.max':
            try:
                self.qc_chalf_max_doubleSpinBox.setValue(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'qc.filter.rsq':
            try:
                self.qc_rsq_doubleSpinBox.setValue(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'qc.filter.ci_filter':
            try:
                self.qc_ci_checkBox.setChecked(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'qc.filter.ci_value':
            try:
                self.qc_ci_doubleSpinBox.setValue(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'qc.filter.optimize':
            try:
                if parameter=='rsq':self.qc_priority_comboBox.setCurrentText("R\u00b2")
                elif parameter=='ci':self.qc_priority_comboBox.setCurrentText('Confidence Interval')
                else:self.qc_priority_comboBox.setCurrentText("R\u00b2")
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        ### VISUALIZATION SETTINGS ###
        ## QUALITY CONTROL REPORT ##
        elif key == 'visualization.qc.report':
            try:
                self.qc_vis_generate_checkBox.setChecked(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'visualization.qc.open':
            try:
                self.qc_vis_open_checkBox.setChecked(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        ## RESIDUE MAPPER ##
        elif key == 'visualization.rm':
            try:
                self.rm_checkBox.setChecked(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'visualization.rm.file_type':
            try:
                if parameter=='jpg':self.rm_filetype_comboBox.setCurrentText('.jpg')
                elif parameter=='png':self.rm_filetype_comboBox.setCurrentText('.png')
                elif parameter=='svg':self.rm_filetype_comboBox.setCurrentText('.svg')
                else:self.rm_filetype_comboBox.setCurrentText('.jpg')
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'visualization.rm.min':
            try:
                self.rm_chalf_low_doubleSpinBox.setValue(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'visualization.rm.max':
            try:
                self.rm_chalf_high_doubleSpinBox.setValue(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        # TRENDLINES #
        elif key == 'visualization.rm.trendlines.trendline':
            try:
                self.rm_trendline_checkBox.setChecked(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'visualization.rm.trendlines.min':
            try:
                self.rm_trendline_min_spinBox.setValue(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'visualization.rm.trendlines.window':
            try:
                self.rm_trendline_window_spinBox.setValue(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        # OTHER OPTIONS #
        elif key == 'visualization.rm.other.all_curves':
            try:
                self.rm_allsites_checkBox.setChecked(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'visualization.rm.other.reference_stats':
            try:
                self.rm_stats_reference_checkBox.setChecked(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'visualization.rm.other.rm_trendline_stats':
            try:
                self.rm_trendline_stats_checkBox.setChecked(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'visualization.rm.other.mutation_search':
            try:
                self.rm_custom_fasta_checkBox.setChecked(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'visualization.rm.other.advanced':
            try:
                self.rm_custom_ann_path_lineEdit.setText(str(parameter))
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        ## COMBINED RESIDUE MAPPER ##
        elif key == 'visualization.crm':
            try:
                self.crm_checkBox.setChecked(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'visualization.crm.file_type':
            try:
                if parameter=='jpg':self.crm_filetype_comboBox.setCurrentText('.jpg')
                elif parameter=='png':self.crm_filetype_comboBox.setCurrentText('.png')
                elif parameter=='svg':self.crm_filetype_comboBox.setCurrentText('.svg')
                else:self.crm_filetype_comboBox.setCurrentText('.jpg')
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'visualization.crm.min':
            try:
                self.crm_chalf_low_doubleSpinBox.setValue(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'visualization.crm.max':
            try:
                self.crm_chalf_high_doubleSpinBox.setValue(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        # TRENDLINES #
        elif key == 'visualization.crm.trendlines.trendline':
            try:
                self.crm_trendline_checkBox.setChecked(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'visualization.crm.trendlines.min':
            try:
                self.crm_trendline_min_spinBox.setValue(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'visualization.crm.trendlines.window':
            try:
                self.crm_trendline_window_spinBox.setValue(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        # OTHER OPTIONS #
        elif key == 'visualization.crm.other.all_curves':
            try:
                self.crm_allsites_checkBox.setChecked(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'visualization.crm.other.reference_stats':
            try:
                self.crm_stats_reference_checkBox.setChecked(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'visualization.crm.other.crm_trendline_stats':
            try:
                self.crm_trendline_stats_checkBox.setChecked(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'visualization.crm.other.shared_only':
            try:
                self.crm_shared_only_checkBox.setChecked(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'visualization.crm.other.mutation_search':
            try:
                self.crm_custom_fasta_checkBox.setChecked(parameter)
                self.crm_shared_only_checkBox.setChecked(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'visualization.crm.other.advanced':
            try:
                self.crm_custom_ann_path_lineEdit.setText(str(parameter))
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        ## DELTA MAPPER OPTIONS ##
        elif key == 'visualization.dm':
            try:
                self.dm_checkBox.setChecked(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'visualization.dm.file_type':
            try:
                if parameter=='jpg':self.dm_filetype_comboBox.setCurrentText('.jpg')
                elif parameter=='png':self.dm_filetype_comboBox.setCurrentText('.png')
                elif parameter=='svg':self.dm_filetype_comboBox.setCurrentText('.svg')
                else:self.dm_filetype_comboBox.setCurrentText('.jpg')
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'visualization.dm.min':
            try:
                self.dm_chalf_low_doubleSpinBox.setValue(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'visualization.dm.max':
            try:
                self.dm_chalf_high_doubleSpinBox.setValue(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        # TRENDLINES #
        elif key == 'visualization.dm.trendlines.trendline':
            try:
                self.dm_trendline_checkBox.setChecked(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'visualization.dm.trendlines.min':
            try:
                self.dm_trendline_min_spinBox.setValue(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'visualization.dm.trendlines.window':
            try:
                self.dm_trendline_window_spinBox.setValue(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        # KDE OPTIONS #
        elif key == 'visualization.dm.kde.min_pts':
            try:
                self.dm_kde_min_spinBox.setValue(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'visualization.dm.sig_filter':
            try:
                self.dm_kde_sig_cutoff_checkBox.setChecked(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'visualization.dm.sig_value':
            try:
                self.dm_kde_sig_cutoff_doubleSpinBox.setValue(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        # OTHER OPTIONS #
        elif key == 'visualization.dm.other.all_curves':
            try:
                self.dm_allsites_checkBox.setChecked(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'visualization.dm.other.reference_stats':
            try:
                self.dm_stats_reference_checkBox.setChecked(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'visualization.dm.other.dm_trendline_stats':
            try:
                self.dm_trendline_stats_checkBox.setChecked(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'visualization.dm.other.mutation_search':
            try:
                self.dm_custom_fasta_checkBox.setChecked(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'visualization.dm.other.advanced':
            try:
                self.dm_custom_ann_path_lineEdit.setText(str(parameter))
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        ## COMBINED SITE ##
        elif key == 'visualization.cs':
            try:
                self.cs_checkBox.setChecked(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'visualization.cs.file_type':
            try:
                if parameter=='jpg':self.cs_filetype_comboBox.setCurrentText('.jpg')
                elif parameter=='png':self.cs_filetype_comboBox.setCurrentText('.png')
                elif parameter=='svg':self.cs_filetype_comboBox.setCurrentText('.svg')
                else:self.cs_filetype_comboBox.setCurrentText('.jpg')
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'visualization.cs.min':
            try:
                self.cs_chalf_low_doubleSpinBox.setValue(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
        elif key == 'visualization.cs.max':
            try:
                self.cs_chalf_high_doubleSpinBox.setValue(parameter)
            except Exception as e:
                print(f'Error with {key}: \n{e}')
    
    def open_workflows_folder(self):
        """
        Opens the 'workflows' subfolder, correctly determining its location
        relative to the executed Python script or bundled executable.
        Displays a warning if the folder is not found.
        """
        # Determine the base path of the application:
        # If running as a frozen executable (e.g., created by PyInstaller)
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        # If running directly from a Python script (.py file)
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        workflows_path = os.path.join(base_path, "workflows")

        if os.path.isdir(workflows_path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(workflows_path))
        else:
            QMessageBox.warning(
                self.MainWindow,
                "Folder Not Found",
                f"The 'workflows' folder was not found at:\n{workflows_path}\n\n"
                "Please ensure it exists in the same directory as the application's executable or script."
            )
    def rm_select_ann_file(self):
        """
        Opens a file dialog to select an .ann file.
        Sets the filename (basename) of the selected file to rm_custom_ann_path_lineEdit.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self.MainWindow, # Parent widget for the dialog
            "Select Annotation File", # Dialog title
            "", # Default directory (empty string for current directory)
            "Annotation Files (*.ann);;All Files (*)" # File filters
        )

        if file_path: # Check if a file was selected (user didn't cancel)
            # Extract only the filename from the full path
            file_name = os.path.abspath(file_path)
            self.rm_custom_ann_path_lineEdit.setText(file_name)
    
    def crm_select_ann_file(self):
        """
        Opens a file dialog to select an .ann file.
        Sets the filename (basename) of the selected file to rm_custom_ann_path_lineEdit.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self.MainWindow, # Parent widget for the dialog
            "Select Annotation File", # Dialog title
            "", # Default directory (empty string for current directory)
            "Annotation Files (*.ann);;All Files (*)" # File filters
        )

        if file_path: # Check if a file was selected (user didn't cancel)
            # Extract only the filename from the full path
            file_name = os.path.abspath(file_path)
            self.crm_custom_ann_path_lineEdit.setText(file_name)
    
    def dm_select_ann_file(self):
        """
        Opens a file dialog to select an .ann file.
        Sets the filename (basename) of the selected file to rm_custom_ann_path_lineEdit.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self.MainWindow, # Parent widget for the dialog
            "Select Annotation File", # Dialog title
            "", # Default directory (empty string for current directory)
            "Annotation Files (*.ann);;All Files (*)" # File filters
        )

        if file_path: # Check if a file was selected (user didn't cancel)
            # Extract only the filename from the full path
            file_name = os.path.abspath(file_path)
            self.dm_custom_ann_path_lineEdit.setText(file_name)
    
    def write_parameter_file(self):
        """
        Extracts information from GUI elements and writes it to a .workflow parameter file.
        """
        # Create the /workflows directory if it doesn't exist
        workflows_dir = "workflows"
        if not os.path.exists(workflows_dir):
            os.makedirs(workflows_dir)
    
        # Prompt the user to choose a filename and location within the /workflows directory
        file_path, _ = QFileDialog.getSaveFileName(
            self,  # Pass self here
            "Save Workflow File",
            os.path.join(workflows_dir, "workflow.workflow"),  # Default filename
            "Workflow Files (*.workflow);;All Files (*)"
        )
    
        if not file_path:
            return  # The user cancelled the dialog
    
        try:
            with open(file_path, 'w') as f:
                # Helper function to write a parameter and its value to the file
                def write_param(param_name, param_value):
                    f.write(f"{param_name}={param_value}\n")
    
                f.write('### CHALF SETTINGS ###\n')
                write_param("chalf", str(self.run_chalf_checkBox.isChecked()))
    
                f.write('\n## CHALF LIGHT SEARCH SETTINGS ##\n')
                write_param("chalf.search.light", str(self.light_search_checkBox.isChecked()))
    
                # Handle the "aa" checkboxes for chalf.search.residues
                aa_residues = ""
                aa_list = ['a', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'y']
                for aa in aa_list:
                    checkbox_name = f"aa_{aa}_checkBox"
                    if hasattr(self, checkbox_name):
                        checkbox = getattr(self, checkbox_name)
                        if checkbox.isChecked():
                            aa_residues += aa
                write_param("chalf.search.residues", aa_residues)
    
                f.write('\n## CHALF FILTER SETTINGS ##\n')
                write_param("chalf.filter.min", str(self.chalf_min_doubleSpinBox.value()))
                write_param("chalf.filter.max", str(self.chalf_max_doubleSpinBox.value()))
                write_param("chalf.filter.rsq", str(self.rsq_doubleSpinBox.value()))
                write_param("chalf.filter.ci_filter", str(self.CI_filter_checkBox.isChecked()))
                write_param("chalf.filter.ci_value", str(self.CI_doubleSpinBox.value()))
                write_param("chalf.filter.optimize", self.fit_opt_comboBox.currentText().replace("R\u00b2", "rsq").replace("Confidence Interval","ci"))
                write_param("chalf.filter.sig_only", str(self.sig_only_checkBox.isChecked()))
    
                f.write('\n## CHALF FITTING OPTIONS ##\n')
                write_param("chalf.fitting.min_pts", str(self.min_pts_spinBox.value()))
                write_param("chalf.fitting.outlier_trimming", str(self.trimming_checkBox.isChecked()))
                write_param("chalf.fitting.outlier_cutoff", str(self.out_cut_spinBox.value()))
                write_param("chalf.fitting.zero_criteria", self.chalf_zero_criteria_comboBox.currentText().lower())
    
                f.write('\n## CHALF GRAPHING OPTIONS ##\n')
                write_param("chalf.graphing.graph", str(self.graph_curves_checkBox.isChecked()))
                write_param("chalf.graphing.file_type", self.graphing_filetype_comboBox.currentText().replace(".","").lower())
                write_param("chalf.graphing.min", str(self.graph_chalf_min_doubleSpinBox.value()))
                write_param("chalf.graphing.max", str(self.graph_chalf_max_doubleSpinBox.value()))
                write_param("chalf.graphing.rsq", str(self.graph_rsq_doubleSpinBox.value()))
                write_param("chalf.graphing.ci_filter", str(self.graph_ci_checkBox.isChecked()))
                write_param("chalf.graphing.ci_value", str(self.graph_ci_doubleSpinBox.value()))
    
                f.write('\n## CHALF EXPERIMENTAL OPTIONS ##\n')
                write_param("chalf.experimental.sg.smooth", str(self.sg_checkBox.isChecked()))
                write_param("chalf.experimental.sg.window", str(self.sg_window_spinBox.value()))
                write_param("chalf.experimental.sg.order", str(self.sg_order_spinBox.value()))
                write_param("chalf.experimental.wf.window_fit", str(self.windowed_fitting_checkBox.isChecked()))
                write_param("chalf.experimental.wf.window", str(self.wf_window_spinBox.value()))
                write_param("chalf.experimental.ms.mutations", str(self.mutation_search_checkBox.isChecked()))
    
                f.write('\n### QUALITY CONTROL SETTINGS ###\n')
                write_param("qc", str(self.qc_checkBox.isChecked()))
    
                f.write('\n## QUALITY CONTROL SEARCH SETTINGS ##\n')
                qc_residues = ""
                qc_aa_list = ['a', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'y']
                for aa in qc_aa_list:
                    checkbox_name = f"qc_{aa}_checkBox"
                    if hasattr(self, checkbox_name):
                        checkbox = getattr(self, checkbox_name)
                        if checkbox.isChecked():
                            qc_residues += aa
                write_param("qc.search.residues", qc_residues)
    
                f.write('\n## QUALITY CONTROL FILTER OPTIONS ##\n')
                write_param("qc.filter.min", str(self.qc_chalf_min_doubleSpinBox.value()))
                write_param("qc.filter.max", str(self.qc_chalf_max_doubleSpinBox.value()))
                write_param("qc.filter.rsq", str(self.qc_rsq_doubleSpinBox.value()))
                write_param("qc.filter.ci_filter", str(self.qc_ci_checkBox.isChecked()))
                write_param("qc.filter.ci_value", str(self.qc_ci_doubleSpinBox.value()))
                write_param("qc.filter.optimize", self.qc_priority_comboBox.currentText().replace("R\u00b2", "rsq").replace("Confidence Interval","ci"))
    
                f.write('\n### VISUALIZATION SETTINGS ###\n')
                f.write('\n## QUALITY CONTROL REPORT ##\n')
                write_param("visualization.qc.report", str(self.qc_vis_generate_checkBox.isChecked()))
                write_param("visualization.qc.open", str(self.qc_vis_open_checkBox.isChecked()))
    
                f.write('\n## RESIDUE MAPPER ##\n')
                write_param("visualization.rm", str(self.rm_checkBox.isChecked()))
                write_param("visualization.rm.file_type", self.rm_filetype_comboBox.currentText().replace(".","").lower())
                write_param("visualization.rm.min", str(self.rm_chalf_low_doubleSpinBox.value()))
                write_param("visualization.rm.max", str(self.rm_chalf_high_doubleSpinBox.value()))
    
                f.write('\n# TRENDLINES #\n')
                write_param("visualization.rm.trendlines.trendline", str(self.rm_trendline_checkBox.isChecked()))
                write_param("visualization.rm.trendlines.min", str(self.rm_trendline_min_spinBox.value()))
                write_param("visualization.rm.trendlines.window", str(self.rm_trendline_window_spinBox.value()))
    
                f.write('\n# OTHER OPTIONS #\n')
                write_param("visualization.rm.other.all_curves", str(self.rm_allsites_checkBox.isChecked()))
                write_param("visualization.rm.other.reference_stats", str(self.rm_stats_reference_checkBox.isChecked()))
                write_param("visualization.rm.other.rm_trendline_stats", str(self.rm_trendline_stats_checkBox.isChecked()))
                write_param("visualization.rm.other.mutation_search", str(self.rm_custom_fasta_checkBox.isChecked()))
                write_param("visualization.rm.other.advanced", self.rm_custom_ann_path_lineEdit.text())
    
                f.write('\n## COMBINED RESIDUE MAPPER ##\n')
                write_param("visualization.crm", str(self.crm_checkBox.isChecked()))
                write_param("visualization.crm.file_type", self.crm_filetype_comboBox.currentText().replace(".","").lower())
                write_param("visualization.crm.min", str(self.crm_chalf_low_doubleSpinBox.value()))
                write_param("visualization.crm.max", str(self.crm_chalf_high_doubleSpinBox.value()))
    
                f.write('\n# TRENDLINES #\n')
                write_param("visualization.crm.trendlines.trendline", str(self.crm_trendline_checkBox.isChecked()))
                write_param("visualization.crm.trendlines.min", str(self.crm_trendline_min_spinBox.value()))
                write_param("visualization.crm.trendlines.window", str(self.crm_trendline_window_spinBox.value()))
    
                f.write('\n# OTHER OPTIONS #\n')
                write_param("visualization.crm.other.all_curves", str(self.crm_allsites_checkBox.isChecked()))
                write_param("visualization.crm.other.reference_stats", str(self.crm_stats_reference_checkBox.isChecked()))
                write_param("visualization.crm.other.crm_trendline_stats", str(self.crm_trendline_stats_checkBox.isChecked()))
                write_param("visualization.crm.other.shared_only", str(self.crm_shared_only_checkBox.isChecked()))
                write_param("visualization.crm.other.mutation_search", str(self.crm_custom_fasta_checkBox.isChecked()))
                write_param("visualization.crm.other.advanced", self.crm_custom_ann_path_lineEdit.text())
    
                f.write('\n## DELTA MAPPER OPTIONS ##\n')
                write_param("visualization.dm", str(self.dm_checkBox.isChecked()))
                write_param("visualization.dm.file_type", self.dm_filetype_comboBox.currentText().replace(".","").lower())
                write_param("visualization.dm.min", str(self.dm_chalf_low_doubleSpinBox.value()))
                write_param("visualization.dm.max", str(self.dm_chalf_high_doubleSpinBox.value()))
    
                f.write('\n# TRENDLINES #\n')
                write_param("visualization.dm.trendlines.trendline", str(self.dm_trendline_checkBox.isChecked()))
                write_param("visualization.dm.trendlines.min", str(self.dm_trendline_min_spinBox.value()))
                write_param("visualization.dm.trendlines.window", str(self.dm_trendline_window_spinBox.value()))
    
                f.write('\n# KDE OPTIONS #\n')
                write_param("visualization.dm.kde.min_pts", str(self.dm_kde_min_spinBox.value()))
                write_param("visualization.dm.sig_filter", str(self.dm_kde_sig_cutoff_checkBox.isChecked()))
                write_param("visualization.dm.sig_value", str(self.dm_kde_sig_cutoff_doubleSpinBox.value()))
    
                f.write('\n# OTHER OPTIONS #\n')
                write_param("visualization.dm.other.all_curves", str(self.dm_allsites_checkBox.isChecked()))
                write_param("visualization.dm.other.reference_stats", str(self.dm_stats_reference_checkBox.isChecked()))
                write_param("visualization.dm.other.dm_trendline_stats", str(self.dm_trendline_stats_checkBox.isChecked()))
                write_param("visualization.dm.other.mutation_search", str(self.dm_custom_fasta_checkBox.isChecked()))
                write_param("visualization.dm.other.advanced", self.dm_custom_ann_path_lineEdit.text())
    
                f.write('\n## COMBINED SITE ##\n')
                write_param("visualization.cs", str(self.cs_checkBox.isChecked()))
                write_param("visualization.cs.file_type", self.cs_filetype_comboBox.currentText().replace(".","").lower())
                write_param("visualization.cs.min", str(self.cs_chalf_low_doubleSpinBox.value()))
                write_param("visualization.cs.max", str(self.cs_chalf_high_doubleSpinBox.value()))
    
            print(f"Parameters written to {file_path}\n")
            self.update_workflows()
            
    
        except Exception as e:
            print(f"Error writing parameter file: {e}")
            
    def start_write_parameter_file(self, output_dir):
        """
        Extracts information from GUI elements and writes it to a .workflow parameter file that will be referenced when runnning everything in CHalf.
        """
        file_path = f'{output_dir}/params.workflow'
    
        try:
            with open(file_path, 'w') as f:
                # Helper function to write a parameter and its value to the file
                def write_param(param_name, param_value):
                    f.write(f"{param_name}={param_value}\n")
    
                f.write('### CHALF SETTINGS ###\n')
                write_param("chalf", str(self.run_chalf_checkBox.isChecked()))
    
                f.write('\n## CHALF LIGHT SEARCH SETTINGS ##\n')
                write_param("chalf.search.light", str(self.light_search_checkBox.isChecked()))
    
                # Handle the "aa" checkboxes for chalf.search.residues
                aa_residues = ""
                aa_list = ['a', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'y']
                for aa in aa_list:
                    checkbox_name = f"aa_{aa}_checkBox"
                    if hasattr(self, checkbox_name):
                        checkbox = getattr(self, checkbox_name)
                        if checkbox.isChecked():
                            aa_residues += aa
                write_param("chalf.search.residues", aa_residues)
    
                f.write('\n## CHALF FILTER SETTINGS ##\n')
                write_param("chalf.filter.min", str(self.chalf_min_doubleSpinBox.value()))
                write_param("chalf.filter.max", str(self.chalf_max_doubleSpinBox.value()))
                write_param("chalf.filter.rsq", str(self.rsq_doubleSpinBox.value()))
                write_param("chalf.filter.ci_filter", str(self.CI_filter_checkBox.isChecked()))
                write_param("chalf.filter.ci_value", str(self.CI_doubleSpinBox.value()))
                write_param("chalf.filter.optimize", self.fit_opt_comboBox.currentText().replace("R\u00b2", "rsq").replace("Confidence Interval","ci"))
                write_param("chalf.filter.sig_only", str(self.sig_only_checkBox.isChecked()))
    
                f.write('\n## CHALF FITTING OPTIONS ##\n')
                write_param("chalf.fitting.min_pts", str(self.min_pts_spinBox.value()))
                write_param("chalf.fitting.outlier_trimming", str(self.trimming_checkBox.isChecked()))
                write_param("chalf.fitting.outlier_cutoff", str(self.out_cut_spinBox.value()))
                write_param("chalf.fitting.zero_criteria", self.chalf_zero_criteria_comboBox.currentText().lower())
    
                f.write('\n## CHALF GRAPHING OPTIONS ##\n')
                write_param("chalf.graphing.graph", str(self.graph_curves_checkBox.isChecked()))
                write_param("chalf.graphing.file_type", self.graphing_filetype_comboBox.currentText().replace(".","").lower())
                write_param("chalf.graphing.min", str(self.graph_chalf_min_doubleSpinBox.value()))
                write_param("chalf.graphing.max", str(self.graph_chalf_max_doubleSpinBox.value()))
                write_param("chalf.graphing.rsq", str(self.graph_rsq_doubleSpinBox.value()))
                write_param("chalf.graphing.ci_filter", str(self.graph_ci_checkBox.isChecked()))
                write_param("chalf.graphing.ci_value", str(self.graph_ci_doubleSpinBox.value()))
    
                f.write('\n## CHALF EXPERIMENTAL OPTIONS ##\n')
                write_param("chalf.experimental.sg.smooth", str(self.sg_checkBox.isChecked()))
                write_param("chalf.experimental.sg.window", str(self.sg_window_spinBox.value()))
                write_param("chalf.experimental.sg.order", str(self.sg_order_spinBox.value()))
                write_param("chalf.experimental.wf.window_fit", str(self.windowed_fitting_checkBox.isChecked()))
                write_param("chalf.experimental.wf.window", str(self.wf_window_spinBox.value()))
                write_param("chalf.experimental.ms.mutations", str(self.mutation_search_checkBox.isChecked()))
    
                f.write('\n### QUALITY CONTROL SETTINGS ###\n')
                write_param("qc", str(self.qc_checkBox.isChecked()))
    
                f.write('\n## QUALITY CONTROL SEARCH SETTINGS ##\n')
                qc_residues = ""
                qc_aa_list = ['a', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'y']
                for aa in qc_aa_list:
                    checkbox_name = f"qc_{aa}_checkBox"
                    if hasattr(self, checkbox_name):
                        checkbox = getattr(self, checkbox_name)
                        if checkbox.isChecked():
                            qc_residues += aa
                write_param("qc.search.residues", qc_residues)
    
                f.write('\n## QUALITY CONTROL FILTER OPTIONS ##\n')
                write_param("qc.filter.min", str(self.qc_chalf_min_doubleSpinBox.value()))
                write_param("qc.filter.max", str(self.qc_chalf_max_doubleSpinBox.value()))
                write_param("qc.filter.rsq", str(self.qc_rsq_doubleSpinBox.value()))
                write_param("qc.filter.ci_filter", str(self.qc_ci_checkBox.isChecked()))
                write_param("qc.filter.ci_value", str(self.qc_ci_doubleSpinBox.value()))
                write_param("qc.filter.optimize", self.qc_priority_comboBox.currentText().replace("R\u00b2", "rsq").replace("Confidence Interval","ci"))
    
                f.write('\n### VISUALIZATION SETTINGS ###\n')
                f.write('\n## QUALITY CONTROL REPORT ##\n')
                write_param("visualization.qc.report", str(self.qc_vis_generate_checkBox.isChecked()))
                write_param("visualization.qc.open", str(self.qc_vis_open_checkBox.isChecked()))
    
                f.write('\n## RESIDUE MAPPER ##\n')
                write_param("visualization.rm", str(self.rm_checkBox.isChecked()))
                write_param("visualization.rm.file_type", self.rm_filetype_comboBox.currentText().replace(".","").lower())
                write_param("visualization.rm.min", str(self.rm_chalf_low_doubleSpinBox.value()))
                write_param("visualization.rm.max", str(self.rm_chalf_high_doubleSpinBox.value()))
    
                f.write('\n# TRENDLINES #\n')
                write_param("visualization.rm.trendlines.trendline", str(self.rm_trendline_checkBox.isChecked()))
                write_param("visualization.rm.trendlines.min", str(self.rm_trendline_min_spinBox.value()))
                write_param("visualization.rm.trendlines.window", str(self.rm_trendline_window_spinBox.value()))
    
                f.write('\n# OTHER OPTIONS #\n')
                write_param("visualization.rm.other.all_curves", str(self.rm_allsites_checkBox.isChecked()))
                write_param("visualization.rm.other.reference_stats", str(self.rm_stats_reference_checkBox.isChecked()))
                write_param("visualization.rm.other.rm_trendline_stats", str(self.rm_trendline_stats_checkBox.isChecked()))
                write_param("visualization.rm.other.mutation_search", str(self.rm_custom_fasta_checkBox.isChecked()))
                write_param("visualization.rm.other.advanced", self.rm_custom_ann_path_lineEdit.text())
    
                f.write('\n## COMBINED RESIDUE MAPPER ##\n')
                write_param("visualization.crm", str(self.crm_checkBox.isChecked()))
                write_param("visualization.crm.file_type", self.crm_filetype_comboBox.currentText().replace(".","").lower())
                write_param("visualization.crm.min", str(self.crm_chalf_low_doubleSpinBox.value()))
                write_param("visualization.crm.max", str(self.crm_chalf_high_doubleSpinBox.value()))
    
                f.write('\n# TRENDLINES #\n')
                write_param("visualization.crm.trendlines.trendline", str(self.crm_trendline_checkBox.isChecked()))
                write_param("visualization.crm.trendlines.min", str(self.crm_trendline_min_spinBox.value()))
                write_param("visualization.crm.trendlines.window", str(self.crm_trendline_window_spinBox.value()))
    
                f.write('\n# OTHER OPTIONS #\n')
                write_param("visualization.crm.other.all_curves", str(self.crm_allsites_checkBox.isChecked()))
                write_param("visualization.crm.other.reference_stats", str(self.crm_stats_reference_checkBox.isChecked()))
                write_param("visualization.crm.other.crm_trendline_stats", str(self.crm_trendline_stats_checkBox.isChecked()))
                write_param("visualization.crm.other.shared_only", str(self.crm_shared_only_checkBox.isChecked()))
                write_param("visualization.crm.other.mutation_search", str(self.crm_custom_fasta_checkBox.isChecked()))
                write_param("visualization.crm.other.advanced", self.crm_custom_ann_path_lineEdit.text())
    
                f.write('\n## DELTA MAPPER OPTIONS ##\n')
                write_param("visualization.dm", str(self.dm_checkBox.isChecked()))
                write_param("visualization.dm.file_type", self.dm_filetype_comboBox.currentText().replace(".","").lower())
                write_param("visualization.dm.min", str(self.dm_chalf_low_doubleSpinBox.value()))
                write_param("visualization.dm.max", str(self.dm_chalf_high_doubleSpinBox.value()))
    
                f.write('\n# TRENDLINES #\n')
                write_param("visualization.dm.trendlines.trendline", str(self.dm_trendline_checkBox.isChecked()))
                write_param("visualization.dm.trendlines.min", str(self.dm_trendline_min_spinBox.value()))
                write_param("visualization.dm.trendlines.window", str(self.dm_trendline_window_spinBox.value()))
    
                f.write('\n# KDE OPTIONS #\n')
                write_param("visualization.dm.kde.min_pts", str(self.dm_kde_min_spinBox.value()))
                write_param("visualization.dm.sig_filter", str(self.dm_kde_sig_cutoff_checkBox.isChecked()))
                write_param("visualization.dm.sig_value", str(self.dm_kde_sig_cutoff_doubleSpinBox.value()))
    
                f.write('\n# OTHER OPTIONS #\n')
                write_param("visualization.dm.other.all_curves", str(self.dm_allsites_checkBox.isChecked()))
                write_param("visualization.dm.other.reference_stats", str(self.dm_stats_reference_checkBox.isChecked()))
                write_param("visualization.dm.other.dm_trendline_stats", str(self.dm_trendline_stats_checkBox.isChecked()))
                write_param("visualization.dm.other.mutation_search", str(self.dm_custom_fasta_checkBox.isChecked()))
                write_param("visualization.dm.other.advanced", self.dm_custom_ann_path_lineEdit.text())
    
                f.write('\n## COMBINED SITE ##\n')
                write_param("visualization.cs", str(self.cs_checkBox.isChecked()))
                write_param("visualization.cs.file_type", self.cs_filetype_comboBox.currentText().replace(".","").lower())
                write_param("visualization.cs.min", str(self.cs_chalf_low_doubleSpinBox.value()))
                write_param("visualization.cs.max", str(self.cs_chalf_high_doubleSpinBox.value()))
    
            print(f"Parameters written to {file_path}")
            self.update_workflows()
            
    
        except Exception as e:
            print(f"Error writing parameter file: {e}")
        
    def load_manifest_file(self):
        """
        Loads data from a tab-delimited .manifest file into the files_tableWidget.
        Validates the file's column headers and excludes the "conc dict" column.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self.MainWindow,
            "Open Manifest File",
            "",
            "Manifest Files (*.manifest);;All Files (*)"
        )
    
        if file_path:
            try:
                # Get the expected headers from the current files_tableWidget configuration
                # This represents the columns we *want* in the table.
                table_expected_headers = []
                for col in range(self.files_tableWidget.columnCount()):
                    header_item = self.files_tableWidget.horizontalHeaderItem(col)
                    if header_item:
                        table_expected_headers.append(header_item.text())
                    else:
                        table_expected_headers.append("")
    
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
    
                    if not lines:
                        QMessageBox.warning(
                            self.MainWindow,
                            "Empty File",
                            "The selected manifest file is empty."
                        )
                        return
    
                    # Process header from the manifest file (first line)
                    file_header_line = lines[0].strip()
                    all_file_headers = file_header_line.split('\t')
    
                    # Create a list of header names to load, excluding "conc dict"
                    # Also, build a mapping from original file header index to desired table header index
                    headers_to_load = []
                    file_to_table_col_map = {}
                    conc_dict_col_in_file = -1 # Keep track of where 'conc dict' is in the file
    
                    for idx, header_name in enumerate(all_file_headers):
                        if header_name == "conc dict":
                            conc_dict_col_in_file = idx
                        else:
                            headers_to_load.append(header_name)
                            # Map the file's original column index to the table's new column index
                            file_to_table_col_map[idx] = len(headers_to_load) - 1 # This will be the index in the new table data
    
                    # Validate if the headers we intend to load match the table's expected headers
                    if headers_to_load != table_expected_headers:
                        QMessageBox.warning(
                            self.MainWindow,
                            "Invalid Manifest Format",
                            "The selected manifest file does not have the expected column headers (excluding 'conc dict').\n\n"
                            f"Expected headers in table: {', '.join(table_expected_headers)}\n"
                            f"Headers found in file (excluding 'conc dict'): {', '.join(headers_to_load)}\n\n"
                            "Please select a file with the correct column scheme or update your table's configuration."
                        )
                        return # Stop loading if headers don't match
    
                    # If headers match, clear existing table content and set up columns
                    self.files_tableWidget.setRowCount(0)
                    # Set column count based on the headers we are *actually loading* into the table
                    self.files_tableWidget.setColumnCount(len(table_expected_headers))
                    self.files_tableWidget.setHorizontalHeaderLabels(table_expected_headers) # Set headers for the table
    
                    # Process data rows (from the second line onwards)
                    for row_idx, line in enumerate(lines[1:]):
                        line = line.strip()
                        if not line: # Skip completely empty lines
                            continue
    
                        full_row_data_from_file = line.split('\t')
    
                        # Validate that each row has the correct number of columns as per the file header
                        if len(full_row_data_from_file) != len(all_file_headers):
                            QMessageBox.warning(
                                self.MainWindow,
                                "Row Data Mismatch",
                                f"Row {row_idx + 2} in the manifest file has an incorrect number of columns "
                                f"({len(full_row_data_from_file)} instead of {len(all_file_headers)}).\n"
                                "This row will be skipped."
                            )
                            continue # Skip this row if column count is wrong
    
                        # Prepare data for the table, skipping the "conc dict" column
                        row_data_for_table = []
                        for file_col_idx, item_text in enumerate(full_row_data_from_file):
                            if file_col_idx != conc_dict_col_in_file:
                                # Append in the order defined by headers_to_load
                                # This implicitly handles the order if 'conc dict' was in the middle
                                row_data_for_table.append(item_text)
    
                        # Insert a new row and populate with filtered data
                        current_table_row = self.files_tableWidget.rowCount()
                        self.files_tableWidget.insertRow(current_table_row)
                        for col_idx, item_text in enumerate(row_data_for_table):
                            # Ensure we only try to set items within the defined column count of the table
                            if col_idx < self.files_tableWidget.columnCount():
                                self.files_tableWidget.setItem(current_table_row, col_idx, QTableWidgetItem(item_text))
    
                QMessageBox.information(
                    self.MainWindow,
                    "Load Successful",
                    f"Manifest file loaded from:\n{file_path}"
                )
    
            except FileNotFoundError:
                QMessageBox.critical(
                    self.MainWindow,
                    "File Not Found",
                    f"The file '{file_path}' was not found."
                )
            except Exception as e:
                QMessageBox.critical(
                    self.MainWindow,
                    "Error Loading File",
                    f"An error occurred while loading the manifest file:\n{e}"
                )
    
    def load_workflow(self):
        workflow = self.workflow_comboBox.currentText()
        parameters = extract_workflow(workflows[workflow])
        for key, parameter in parameters.items():
            self.load_parameter(key,parameter)
    
    def update_workflows(self):
        self.workflow_comboBox.clear()
        workflows = get_workflows()
        for workflow in workflows:
            self.workflow_comboBox.addItem(workflow.replace('.workflow',''))
            
    def update_conc_cols(self):
        self.concentration_columns_comboBox.clear()
        conc_cols = get_conc_cols()
        for conc_col in conc_cols:
            self.concentration_columns_comboBox.addItem(conc_col.replace('.cc',''))
            
    def copy_chalf_to_qc(self):
        """
        Copies selected amino acid boxes and filter options from the CHALF portion of the
        GUI and loads them into the QC portion of the GUI.  Handles the case where
        QC section's widgets might not yet exist.
        """
    
        # Copy the selected amino acids
        chalf_aa_list = ['a', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'y']
        #qc_aa_list = ['a', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'y']
    
        for aa in chalf_aa_list:
            chalf_checkbox_name = f"aa_{aa}_checkBox"
            qc_checkbox_name = f"qc_{aa}_checkBox"
    
            if hasattr(self, chalf_checkbox_name) and hasattr(self, qc_checkbox_name):
                chalf_checkbox = getattr(self, chalf_checkbox_name)
                qc_checkbox = getattr(self, qc_checkbox_name)
                qc_checkbox.setChecked(chalf_checkbox.isChecked())  # Copy checked state
            elif hasattr(self, chalf_checkbox_name): # only copy if chalf exists
                chalf_checkbox = getattr(self, chalf_checkbox_name)
                print(f"Warning: QC Checkbox {qc_checkbox_name} does not exist.  Not copying.")
    
        # Copy the filter options
        filter_options = [
            ("chalf_min_doubleSpinBox", "qc_chalf_min_doubleSpinBox", "value"),
            ("chalf_max_doubleSpinBox", "qc_chalf_max_doubleSpinBox", "value"),
            ("rsq_doubleSpinBox", "qc_rsq_doubleSpinBox", "value"),
            ("CI_filter_checkBox", "qc_ci_checkBox", "isChecked"),
            ("CI_doubleSpinBox", "qc_ci_doubleSpinBox", "value"),
            ("fit_opt_comboBox", "qc_priority_comboBox", "currentIndex"), #copy index
        ]
    
        for chalf_widget_name, qc_widget_name, attribute_name in filter_options:
            if hasattr(self, chalf_widget_name) and hasattr(self, qc_widget_name):
                chalf_widget = getattr(self, chalf_widget_name)
                qc_widget = getattr(self, qc_widget_name)
                if attribute_name == "value":
                    qc_widget.setValue(chalf_widget.value())
                elif attribute_name == "isChecked":
                    qc_widget.setChecked(chalf_widget.isChecked())
                elif attribute_name == "currentIndex":
                     qc_widget.setCurrentIndex(chalf_widget.currentIndex())
            elif hasattr(self, chalf_widget_name):
                print(f"Warning: QC Widget {qc_widget_name} does not exist. Not copying {attribute_name}.")
        self.update_rule_based_parameters()
        self.update_rule_based_parameters()
        
    def update_rule_based_parameters(self): #grays out or ungrays out boxes based on if their dependencies are active
        #CHALF
        chalf = self.run_chalf_checkBox.isChecked()
        chalf_ci = self.CI_filter_checkBox.isChecked()
        chalf_ci_optimize = self.fit_opt_comboBox.currentText() == 'Confidence Interval'
        chalf_trimming = self.trimming_checkBox.isChecked()
        graphing = self.graph_curves_checkBox.isChecked()
        graphing_ci = self.graph_ci_checkBox.isChecked()
        sg = self.sg_checkBox.isChecked()
        wf = self.windowed_fitting_checkBox.isChecked()
        
        #Quality Control
        qc = self.qc_checkBox.isChecked()
        qc_ci = self.qc_ci_checkBox.isChecked()
        qc_ci_optimize = self.qc_priority_comboBox.currentText() == 'Confidence Interval'
        
        #Visualization
        vis_qc = self.qc_vis_generate_checkBox.isChecked()
        vis_rm = self.rm_checkBox.isChecked()
        vis_rm_trend = self.rm_trendline_checkBox.isChecked()
        vis_rm_stats = self.rm_stats_reference_checkBox.isChecked()
        vis_crm = self.crm_checkBox.isChecked()
        vis_crm_trend = self.crm_trendline_checkBox.isChecked()
        vis_crm_stats = self.crm_stats_reference_checkBox.isChecked()
        vis_dm = self.dm_checkBox.isChecked()
        vis_dm_trend = self.dm_trendline_checkBox.isChecked()
        vis_dm_stats = self.dm_stats_reference_checkBox.isChecked()
        vis_dm_sig = self.dm_kde_sig_cutoff_checkBox.isChecked()
        vis_cs = self.cs_checkBox.isChecked()
        
        #CHALF OVERALL
        self.light_search_checkBox.setEnabled(chalf)
        self.aa_a_checkBox.setEnabled(chalf)
        self.aa_c_checkBox.setEnabled(chalf)
        self.aa_d_checkBox.setEnabled(chalf)
        self.aa_e_checkBox.setEnabled(chalf)
        self.aa_f_checkBox.setEnabled(chalf)
        self.aa_g_checkBox.setEnabled(chalf)
        self.aa_h_checkBox.setEnabled(chalf)
        self.aa_i_checkBox.setEnabled(chalf)
        self.aa_k_checkBox.setEnabled(chalf)
        self.aa_l_checkBox.setEnabled(chalf)
        self.aa_m_checkBox.setEnabled(chalf)
        self.aa_n_checkBox.setEnabled(chalf)
        self.aa_p_checkBox.setEnabled(chalf)
        self.aa_q_checkBox.setEnabled(chalf)
        self.aa_r_checkBox.setEnabled(chalf)
        self.aa_s_checkBox.setEnabled(chalf)
        self.aa_t_checkBox.setEnabled(chalf)
        self.aa_v_checkBox.setEnabled(chalf)
        self.aa_w_checkBox.setEnabled(chalf)
        self.aa_y_checkBox.setEnabled(chalf)
        self.chalf_min_doubleSpinBox.setEnabled(chalf)
        self.chalf_max_doubleSpinBox.setEnabled(chalf)
        self.rsq_doubleSpinBox.setEnabled(chalf)
        self.CI_filter_checkBox.setEnabled(chalf)
        self.CI_doubleSpinBox.setEnabled(chalf)
        self.fit_opt_comboBox.setEnabled(chalf)
        self.sig_only_checkBox.setEnabled(chalf)
        self.min_pts_spinBox.setEnabled(chalf)
        self.trimming_checkBox.setEnabled(chalf)
        self.out_cut_spinBox.setEnabled(chalf)
        self.chalf_zero_criteria_comboBox.setEnabled(chalf)
        self.graph_curves_checkBox.setEnabled(chalf)
        self.graphing_filetype_comboBox.setEnabled(chalf)
        self.graph_chalf_min_doubleSpinBox.setEnabled(chalf)
        self.graph_chalf_max_doubleSpinBox.setEnabled(chalf)
        self.graph_rsq_doubleSpinBox.setEnabled(chalf)
        self.graph_ci_checkBox.setEnabled(chalf)
        self.graph_ci_doubleSpinBox.setEnabled(chalf)
        self.sg_checkBox.setEnabled(chalf)
        self.sg_window_spinBox.setEnabled(chalf)
        self.sg_order_spinBox.setEnabled(chalf)
        self.windowed_fitting_checkBox.setEnabled(chalf)
        self.wf_window_spinBox.setEnabled(chalf)
        self.mutation_search_checkBox.setEnabled(chalf)
        
        #CHALF CI
        self.CI_doubleSpinBox.setEnabled(chalf_ci and chalf)
        self.CI_filter_checkBox.setChecked(chalf_ci_optimize or chalf_ci)
        
        #CHALF TRIMMING
        self.out_cut_spinBox.setEnabled(chalf_trimming and chalf)
        
        #CHALF GRAPHING
        self.graphing_filetype_comboBox.setEnabled(chalf and graphing)
        self.graph_chalf_min_doubleSpinBox.setEnabled(chalf and graphing)
        self.graph_chalf_max_doubleSpinBox.setEnabled(chalf and graphing)
        self.graph_rsq_doubleSpinBox.setEnabled(chalf and graphing)
        self.graph_ci_checkBox.setEnabled(chalf and graphing)
        self.graph_ci_doubleSpinBox.setEnabled(chalf and graphing and graphing_ci)
        
        #SG FILTER
        self.sg_window_spinBox.setEnabled(chalf and sg)
        self.sg_order_spinBox.setEnabled(chalf and sg)
        
        #WINDOWED FITTING
        self.wf_window_spinBox.setEnabled(chalf and wf)
        
        #QUALITY CONTROL
        self.qc_a_checkBox.setEnabled(qc)
        self.qc_c_checkBox.setEnabled(qc)
        self.qc_d_checkBox.setEnabled(qc)
        self.qc_e_checkBox.setEnabled(qc)
        self.qc_f_checkBox.setEnabled(qc)
        self.qc_g_checkBox.setEnabled(qc)
        self.qc_h_checkBox.setEnabled(qc)
        self.qc_i_checkBox.setEnabled(qc)
        self.qc_k_checkBox.setEnabled(qc)
        self.qc_l_checkBox.setEnabled(qc)
        self.qc_m_checkBox.setEnabled(qc)
        self.qc_n_checkBox.setEnabled(qc)
        self.qc_p_checkBox.setEnabled(qc)
        self.qc_q_checkBox.setEnabled(qc)
        self.qc_r_checkBox.setEnabled(qc)
        self.qc_s_checkBox.setEnabled(qc)
        self.qc_t_checkBox.setEnabled(qc)
        self.qc_v_checkBox.setEnabled(qc)
        self.qc_w_checkBox.setEnabled(qc)
        self.qc_y_checkBox.setEnabled(qc)
        self.qc_chalf_min_doubleSpinBox.setEnabled(qc)
        self.qc_chalf_max_doubleSpinBox.setEnabled(qc)
        self.qc_rsq_doubleSpinBox.setEnabled(qc)
        self.qc_ci_checkBox.setEnabled(qc)
        self.qc_ci_doubleSpinBox.setEnabled(qc and qc_ci)
        self.qc_priority_comboBox.setEnabled(qc)
        self.qc_ci_checkBox.setChecked(qc_ci_optimize or qc_ci)
        
        #VISUALIZATION
        self.qc_vis_open_checkBox.setEnabled(vis_qc)
        self.rm_filetype_comboBox.setEnabled(vis_rm)
        self.rm_chalf_low_doubleSpinBox.setEnabled(vis_rm)
        self.rm_chalf_high_doubleSpinBox.setEnabled(vis_rm)
        self.rm_trendline_checkBox.setEnabled(vis_rm)
        self.rm_trendline_min_spinBox.setEnabled(vis_rm and vis_rm_trend)
        self.rm_trendline_window_spinBox.setEnabled(vis_rm and vis_rm_trend)
        self.rm_allsites_checkBox.setEnabled(vis_rm)
        self.rm_stats_reference_checkBox.setEnabled(vis_rm)
        self.rm_trendline_stats_checkBox.setEnabled(vis_rm and vis_rm_trend and vis_rm_stats)
        self.rm_custom_fasta_checkBox.setEnabled(vis_rm)
        self.rm_custom_ann_path_lineEdit.setEnabled(vis_rm)
        
        self.crm_filetype_comboBox.setEnabled(vis_crm)
        self.crm_chalf_low_doubleSpinBox.setEnabled(vis_crm)
        self.crm_chalf_high_doubleSpinBox.setEnabled(vis_crm)
        self.crm_trendline_checkBox.setEnabled(vis_crm)
        self.crm_trendline_min_spinBox.setEnabled(vis_crm and vis_crm_trend)
        self.crm_trendline_window_spinBox.setEnabled(vis_crm and vis_crm_trend)
        self.crm_allsites_checkBox.setEnabled(vis_crm)
        self.crm_shared_only_checkBox.setEnabled(vis_crm)
        self.crm_stats_reference_checkBox.setEnabled(vis_crm)
        self.crm_trendline_stats_checkBox.setEnabled(vis_crm and vis_crm_trend and vis_crm_stats)
        self.crm_custom_fasta_checkBox.setEnabled(vis_crm)
        self.crm_custom_ann_path_lineEdit.setEnabled(vis_crm)
        
        self.dm_filetype_comboBox.setEnabled(vis_dm)
        self.dm_chalf_low_doubleSpinBox.setEnabled(vis_dm)
        self.dm_chalf_high_doubleSpinBox.setEnabled(vis_dm)
        self.dm_trendline_checkBox.setEnabled(vis_dm)
        self.dm_trendline_min_spinBox.setEnabled(vis_dm and vis_dm_trend)
        self.dm_trendline_window_spinBox.setEnabled(vis_dm and vis_dm_trend)
        self.dm_kde_min_spinBox.setEnabled(vis_dm)
        self.dm_kde_sig_cutoff_checkBox.setEnabled(vis_dm)
        self.dm_kde_sig_cutoff_doubleSpinBox.setEnabled(vis_dm and vis_dm_sig)
        self.dm_allsites_checkBox.setEnabled(vis_dm)
        self.dm_stats_reference_checkBox.setEnabled(vis_dm)
        self.dm_trendline_stats_checkBox.setEnabled(vis_dm and vis_dm_trend and vis_dm_stats)
        self.dm_custom_fasta_checkBox.setEnabled(vis_dm)
        self.dm_custom_ann_path_lineEdit.setEnabled(vis_dm)
        
        self.cs_filetype_comboBox.setEnabled(vis_cs)
        self.cs_chalf_low_doubleSpinBox.setEnabled(vis_cs)
        self.cs_chalf_high_doubleSpinBox.setEnabled(vis_cs)

    def save_manifest_file(self):
        """
        Saves the data from files_tableWidget to a tab-delimited .manifest file.
        Checks if the table is empty before attempting to save.
        Adds an additional column "conc dict" by pulling data from .cc preset files,
        ensuring the JSON-like object is on a single line.
        """
        if self.files_tableWidget.rowCount() == 0:
            QMessageBox.information(
                self.MainWindow,
                "No Files Loaded",
                "Cannot create a manifest file. Please load files into the table first."
            )
            return
    
        concentration_columns_folder = "concentration_columns"
    
        conc_preset_col_idx = -1
        for col in range(self.files_tableWidget.columnCount()):
            header_item = self.files_tableWidget.horizontalHeaderItem(col)
            if header_item and header_item.text() == "Concentration columns (preset)":
                conc_preset_col_idx = col
                break
    
        if conc_preset_col_idx == -1:
            QMessageBox.critical(
                self.MainWindow,
                "Configuration Error",
                "The 'Concentration columns (preset)' column was not found in the table header. Cannot generate 'conc dict' column."
            )
            return
    
        file_path, _ = QFileDialog.getSaveFileName(
            self.MainWindow,
            "Save Manifest File",
            "",
            "Manifest Files (*.manifest);;All Files (*)"
        )
    
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    header_items = []
                    for col in range(self.files_tableWidget.columnCount()):
                        header_item = self.files_tableWidget.horizontalHeaderItem(col)
                        if header_item:
                            header_items.append(header_item.text())
                        else:
                            header_items.append("")
                    header_items.append("conc dict")
                    f.write("\t".join(header_items) + "\n")
    
                    for row in range(self.files_tableWidget.rowCount()):
                        row_data = []
                        for col in range(self.files_tableWidget.columnCount()):
                            item = self.files_tableWidget.item(row, col)
                            if item:
                                row_data.append(item.text())
                            else:
                                row_data.append("")
    
                        preset_name = self.files_tableWidget.item(row, conc_preset_col_idx).text() if self.files_tableWidget.item(row, conc_preset_col_idx) else ""
                        conc_dict_data_str = "{}" # Will store the stringified, single-line JSON
    
                        if preset_name:
                            cc_file_name = f"{preset_name}.cc"
                            cc_file_path = os.path.join(concentration_columns_folder, cc_file_name)
    
                            if not os.path.exists(concentration_columns_folder):
                                QMessageBox.critical(
                                    self.MainWindow,
                                    "Folder Not Found",
                                    f"The 'concentration_columns' folder was not found at '{os.path.abspath(concentration_columns_folder)}'. Aborting save."
                                )
                                return
    
                            if not os.path.isfile(cc_file_path):
                                QMessageBox.critical(
                                    self.MainWindow,
                                    "File Not Found",
                                    f"The concentration preset file '{cc_file_name}' was not found in '{concentration_columns_folder}'. Aborting save."
                                )
                                return
    
                            try:
                                with open(cc_file_path, 'r', encoding='utf-8') as cc_f:
                                    conc_dict_content = cc_f.read()
                                    try:
                                        # Load the JSON content into a Python dictionary
                                        conc_dict_obj = json.loads(conc_dict_content)
                                        # Convert it back to a compact, single-line JSON string
                                        conc_dict_data_str = json.dumps(conc_dict_obj)
                                    except json.JSONDecodeError:
                                        QMessageBox.critical(
                                            self.MainWindow,
                                            "JSON Error",
                                            f"The content of '{cc_file_name}' is not valid JSON. Aborting save."
                                        )
                                        return
    
                            except Exception as json_e:
                                QMessageBox.critical(
                                    self.MainWindow,
                                    "File Read Error",
                                    f"An error occurred while reading '{cc_file_name}':\n{json_e}. Aborting save."
                                )
                                return
                        
                        row_data.append(conc_dict_data_str) # Append the single-line JSON string
    
                        f.write("\t".join(row_data) + "\n")
    
                QMessageBox.information(
                    self.MainWindow,
                    "Save Successful",
                    f"Manifest file saved to: {file_path}"
                )
            except Exception as e:
                QMessageBox.critical(
                    self.MainWindow,
                    "Error Saving File",
                    f"An error occurred while saving the manifest file:\n{e}"
                )
    
    def start_save_manifest_file(self, output_dir):
        """
        Saves the data from files_tableWidget to a tab-delimited .manifest file at the beginning of a run.
        Checks if the table is empty before attempting to save.
        Adds an additional column "conc dict" by pulling data from .cc preset files,
        ensuring the JSON-like object is on a single line.
        """
        if self.files_tableWidget.rowCount() == 0:
            QMessageBox.information(
                self.MainWindow,
                "No Files Loaded",
                "Cannot create a manifest file. Please load files into the table first."
            )
            return # Exit the function if the table is empty
    
        concentration_columns_folder = "concentration_columns"
    
        conc_preset_col_idx = -1
        for col in range(self.files_tableWidget.columnCount()):
            header_item = self.files_tableWidget.horizontalHeaderItem(col)
            if header_item and header_item.text() == "Concentration columns (preset)":
                conc_preset_col_idx = col
                break
    
        if conc_preset_col_idx == -1:
            QMessageBox.critical(
                self.MainWindow,
                "Configuration Error",
                "The 'Concentration columns (preset)' column was not found in the table header. Cannot generate 'conc dict' column."
            )
            return
    
        file_path = f'{output_dir}/run.manifest'
    
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    header_items = []
                    for col in range(self.files_tableWidget.columnCount()):
                        header_item = self.files_tableWidget.horizontalHeaderItem(col)
                        if header_item:
                            header_items.append(header_item.text())
                        else:
                            header_items.append("")
                    header_items.append("conc dict")
                    f.write("\t".join(header_items) + "\n")
    
                    for row in range(self.files_tableWidget.rowCount()):
                        row_data = []
                        for col in range(self.files_tableWidget.columnCount()):
                            item = self.files_tableWidget.item(row, col)
                            if item:
                                row_data.append(item.text())
                            else:
                                row_data.append("")
    
                        preset_name = self.files_tableWidget.item(row, conc_preset_col_idx).text() if self.files_tableWidget.item(row, conc_preset_col_idx) else ""
                        conc_dict_data_str = "{}" # Will store the stringified, single-line JSON
    
                        if preset_name:
                            cc_file_name = f"{preset_name}.cc"
                            cc_file_path = os.path.join(concentration_columns_folder, cc_file_name)
    
                            if not os.path.exists(concentration_columns_folder):
                                QMessageBox.critical(
                                    self.MainWindow,
                                    "Folder Not Found",
                                    f"The 'concentration_columns' folder was not found at '{os.path.abspath(concentration_columns_folder)}'. Aborting run."
                                )
                                return
    
                            if not os.path.isfile(cc_file_path):
                                QMessageBox.critical(
                                    self.MainWindow,
                                    "File Not Found",
                                    f"The concentration preset file '{cc_file_name}' was not found in '{concentration_columns_folder}'. Aborting run."
                                )
                                return
    
                            try:
                                with open(cc_file_path, 'r', encoding='utf-8') as cc_f:
                                    conc_dict_content = cc_f.read()
                                    try:
                                        # Load the JSON content into a Python dictionary
                                        conc_dict_obj = json.loads(conc_dict_content)
                                        # Convert it back to a compact, single-line JSON string
                                        conc_dict_data_str = json.dumps(conc_dict_obj)
                                    except json.JSONDecodeError:
                                        QMessageBox.critical(
                                            self.MainWindow,
                                            "JSON Error",
                                            f"The content of '{cc_file_name}' is not valid JSON. Aborting run."
                                        )
                                        return
    
                            except Exception as json_e:
                                QMessageBox.critical(
                                    self.MainWindow,
                                    "File Read Error",
                                    f"An error occurred while reading '{cc_file_name}':\n{json_e}. Aborting run."
                                )
                                return
                        
                        row_data.append(conc_dict_data_str) # Append the single-line JSON string
    
                        f.write("\t".join(row_data) + "\n")
    
                print("Save Successful\n")
                print(f"Manifest file saved to: {file_path}\n")
            except Exception as e:
                QMessageBox.critical(
                    self.MainWindow,
                    "Error Saving File",
                    f"An error occurred while saving the manifest file:\n{e}"
                )
                
    def start_save_vis_file(self, output_dir):
        """
        Saves the data from visualization_tableWidget to a tab-delimited .vis file.
        The file will be saved in the current working directory.
        """
        if self.visualization_tableWidget.rowCount() == 0:
            self.logger.write("Visualization table is empty. Skipping .vis file creation.\n")
            return

        # Get the current working directory (set by start_run)
        current_dir = os.getcwd()
        default_file_name = os.path.join(output_dir, "visualization_config.vis")

        # You can choose to prompt the user for a filename, or use a fixed one.
        # For a "start_save" method, a fixed name might be preferred,
        # but a dialog is safer to avoid overwriting.
        # Given the context of "start_run" saving files, we'll assume a fixed name
        # to simplify the automated saving process, but you can add a dialog if needed.
        file_path = default_file_name # Using a fixed name for automated saving

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                # Write the header row
                header_items = []
                for col in range(self.visualization_tableWidget.columnCount()):
                    header_item = self.visualization_tableWidget.horizontalHeaderItem(col)
                    if header_item:
                        header_items.append(header_item.text())
                    else:
                        header_items.append("") # Fallback for missing header
                f.write("\t".join(header_items) + "\n")

                # Write the data rows
                for row in range(self.visualization_tableWidget.rowCount()):
                    row_data = []
                    for col in range(self.visualization_tableWidget.columnCount()):
                        item = self.visualization_tableWidget.item(row, col)
                        if item:
                            row_data.append(item.text())
                        else:
                            row_data.append("") # Handle empty cells
                    f.write("\t".join(row_data) + "\n")

            self.logger.write(f".vis file saved to: {file_path}\n")

        except Exception as e:
            self.logger.write(f"ERROR: Failed to save .vis file to {file_path}: {e}\n")
            QMessageBox.critical(self.MainWindow, "Error Saving .vis File",
                                f"An error occurred while saving the visualization file:\n{e}")

    def add_files(self):
        """
        Opens a file dialog to select multiple CSV files and appends them to the
        files_tableWidget.
        """
        file_dialog = QFileDialog()
        file_paths, _ = file_dialog.getOpenFileNames(
            self,
            "Select CSV Files",
            "",  # Start in the current directory
            "CSV Files (*.csv);;All Files (*)",
            options=QFileDialog.DontUseNativeDialog  # Add this option
        )
        conc_cols = self.concentration_columns_comboBox.currentText()
        if file_paths:  # If the user selected files
            for file_path in file_paths:
                # Get the number of rows in the table
                row_count = self.files_tableWidget.rowCount()
                # Insert a new row at the end
                self.files_tableWidget.insertRow(row_count)
                # Create a new item with the file path
                file_path_item = QTableWidgetItem(file_path)
                # Set the file path item in the first column (index 0)
                self.files_tableWidget.setItem(row_count, 0, file_path_item)
                # Add a filler condition name in the second column (index 1)
                condition_name_item = QTableWidgetItem(f"condition_{row_count}")
                self.files_tableWidget.setItem(row_count, 1, condition_name_item)
                self.files_tableWidget.setItem(row_count, 2, QTableWidgetItem(conc_cols))
        
    def remove_selected_rows(self):
        """
        Removes the selected rows from the files_tableWidget.
        """
        selected_rows = set()  # Use a set to store unique row numbers
        for item in self.files_tableWidget.selectedItems():
            selected_rows.add(item.row())  # Add the row number to the set
    
        # Convert the set to a sorted list (descending order)
        selected_rows_list = sorted(list(selected_rows), reverse=True)
    
        for row in selected_rows_list:
            self.files_tableWidget.removeRow(row)
    
    def clear_table(self):
        """
        Clears all rows from the files_tableWidget.
        """
        self.files_tableWidget.setRowCount(0)
    
    def check_and_fix_condition_names(self):
        """
        Checks if the strings in the second column (index 1) of the files_tableWidget
        are unique.  If any are not unique, it displays an error message and adds a
        suffix "_n" to make them unique, where n is the count of the non-unique
        occurrence.  This version skips processing for blank condition name cells.
        """
        condition_names = {}
        duplicate_found = False
        error_message = "Error: Duplicate condition names found.  Please correct them.\n\n"
    
        # Collect and count condition names
        for row in range(self.files_tableWidget.rowCount()):
            item = self.files_tableWidget.item(row, 1)  # Get item from the second column
            if item is not None and item.text().strip():  # Check for not None and not empty
                condition_name = item.text().strip()
                if condition_name in condition_names:
                    condition_names[condition_name] += 1
                    duplicate_found = True
                else:
                    condition_names[condition_name] = 1
            else:
                error_message += f"Row {row + 1}: Condition name is empty.\n"
                # duplicate_found = True # Removed -  We don't want to rename empty cells
    
        # If duplicates were found, modify the names and show an error
        if duplicate_found:
            # QMessageBox.critical(self, "Duplicate Condition Names", error_message)  # show the error - Moved this
    
            # First, get all the names
            existing_names = []
            for row in range(self.files_tableWidget.rowCount()):
                item = self.files_tableWidget.item(row, 1)
                if item and item.text().strip():
                    existing_names.append(item.text().strip())
                else:
                    existing_names.append("") #add empty string
    
            # Modify condition names in the table
            condition_names = {}  # reset
            for row in range(self.files_tableWidget.rowCount()):
                item = self.files_tableWidget.item(row, 1)
                if item and item.text().strip():  # Only process non-empty cells
                    condition_name = item.text().strip()
                    if condition_name in condition_names:
                        original_name = condition_name
                        suffix = condition_names[condition_name]
                        new_condition_name = f"{condition_name}_{suffix}"
                        while new_condition_name in existing_names:
                            suffix += 1
                            new_condition_name = f"{condition_name}_{suffix}"
                        item.setText(new_condition_name)  # Update the table item
                        condition_names[original_name] = suffix + 1
                    else:
                        condition_names[condition_name] = 2
                elif item and not item.text().strip():
                     item = QTableWidgetItem(f"condition_{row}")
                     self.files_tableWidget.setItem(row, 1, item)
                     condition_names[f"condition_{row}"] = 2
                else:
                    pass #DO NOT edit empty cell
            #QMessageBox.critical(self, "Duplicate Condition Names", error_message)  # Moved this
        
    def populate_condition_names(self):
        """
        Populates the second column (index 1) of the files_tableWidget with condition
        names derived from the filenames in the first column (index 0), only for
        selected rows.
        """
        selected_rows = set()
        for item in self.files_tableWidget.selectedItems():
            selected_rows.add(item.row())
    
        for row in selected_rows:
            file_path_item = self.files_tableWidget.item(row, 0)  # Get the file path item
            if file_path_item is not None:
                file_path = file_path_item.text()
                filename = os.path.basename(file_path)
                condition_name = os.path.splitext(filename)[0]
                condition_name_item = QTableWidgetItem(condition_name)
                self.files_tableWidget.setItem(row, 1, condition_name_item)
            else:
                # Handle the case where the file path is empty or None
                condition_name_item = QTableWidgetItem("")  # Or some default value
                self.files_tableWidget.setItem(row, 1, condition_name_item)
    
    def set_condition_names_to_row_index(self):
        """
        Sets the condition names in the second column (index 1) of the
        files_tableWidget to be "condition_n", where n is the row index.
        """
        selected_rows = set()
        for item in self.files_tableWidget.selectedItems():
            selected_rows.add(item.row())
        for row in selected_rows:
            condition_name_item = QTableWidgetItem(f"condition_{row}")
            self.files_tableWidget.setItem(row, 1, condition_name_item)
            
    def set_condition_names_to_parent_dir(self):
        """
        Sets the condition names in the second column (index 1) of the
        files_tableWidget to be the name of the parent directory of each file,
        only for selected rows.
        """
        selected_rows = set()
        for item in self.files_tableWidget.selectedItems():
            selected_rows.add(item.row())
    
        for row in selected_rows:
            file_path_item = self.files_tableWidget.item(row, 0)  # Get the file path
            if file_path_item is not None:
                file_path = file_path_item.text()
                parent_dir = os.path.dirname(file_path)  # Get the parent directory
                condition_name = os.path.basename(parent_dir)  # Get the directory name
                condition_name_item = QTableWidgetItem(condition_name)
                self.files_tableWidget.setItem(row, 1, condition_name_item)
            else:
                condition_name_item = QTableWidgetItem("")
                self.files_tableWidget.setItem(row, 1, condition_name_item)
    
    def fill_concentration_column(self):
        """
        Gets the current text from the concentration_columns_comboBox and fills the
        third column (index 2) of the files_tableWidget with that text for rows that
        are highlighted.
        """
        # Get the current text from the combo box
        concentration_text = self.concentration_columns_comboBox.currentText()
    
        # Iterate through the selected items to get the selected rows
        selected_rows = set()
        for item in self.files_tableWidget.selectedItems():
            selected_rows.add(item.row())
    
        # Fill the third column for each selected row
        for row in selected_rows:
            # Create a new table item with the combo box text
            concentration_item = QTableWidgetItem(concentration_text)
            # Set the item in the third column (index 2)
            self.files_tableWidget.setItem(row, 2, concentration_item)
    
    def show_edit_concentration_dialog(self):
        """
        Initializes and shows the EditConcentrationDialog.
        It passes the currently selected concentration column data to the dialog.
        After the dialog closes, it updates the main combo box and selects
        the newly saved preset if applicable.
        """
        selected_preset_name = self.concentration_columns_comboBox.currentText()
        current_conc_data = None

        if selected_preset_name != "New Preset" and selected_preset_name in conc_cols: # Ensure "New Preset" doesn't try to load a file
            file_name = conc_cols[selected_preset_name]
            current_conc_data = extract_conc_cols(file_name)
        elif selected_preset_name == "New Preset": # Handle "New Preset" case for initial data
             current_conc_data = {} # Start with empty data for a new preset
        else: # Fallback for "Default (IPSA)" or if conc_cols is empty
            current_conc_data = dict(zip(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],[0.0, 0.43, 0.87, 1.3, 1.74, 2.17, 2.61, 3.04, 3.48, 3.59]))


        dialog = EditConcentrationDialog(self, current_conc_data)
        result = dialog.exec() # This makes the dialog blocking

        if result == QDialog.Accepted: # Check if the dialog was closed with OK
            self.update_conc_cols() # Refresh the main combo box

            if dialog.saved_preset_name: # Check if a new preset was saved
                index = self.concentration_columns_comboBox.findText(dialog.saved_preset_name)
                if index != -1:
                    self.concentration_columns_comboBox.setCurrentIndex(index)
                    
    def update_conditions(self):
        conditions = []
        for row in range(self.files_tableWidget.rowCount()):
            item = self.files_tableWidget.item(row, 1)
            if item is not None:
                conditions.append(item.text())
        self.vis_conditions_comboBox.clear()
        self.vis_conditions_comboBox.addItems(conditions)
    
    def _get_table_state_for_group_logic(self):
        """
        Scans the visualization_tableWidget to gather current state information needed for adding new conditions.
        Returns:
            dict: {
                'max_integer_group_id': int, # The highest integer found in "Group X" names
                'all_existing_conditions': set, # Set of all condition names present anywhere in the table
                'group_ref_status': dict, # {group_name: bool (True if group has Reference, False otherwise)}
                'group_colors_used': dict, # {group_name: set_of_used_colors_hex}
                'group_data_by_group': dict # {group_name: {'conditions_in_group': set}} for checking exact duplicates
                'existing_integer_group_ids': set # NEW: All integer IDs found in "Group X" names
            }
        """
        max_id = 0
        all_conditions = set()
        ref_status = {} # Tracks if a group already has a reference
        colors_used = {} # Tracks colors used per group
        group_data_by_group = {} # Tracks conditions within each group for exact duplicate check
        existing_integer_group_ids = set() # NEW: To track all integer IDs in use

        for row in range(self.visualization_tableWidget.rowCount()):
            try:
                condition_item = self.visualization_tableWidget.item(row, 0) # Condition column (index 0)
                group_item = self.visualization_tableWidget.item(row, 1) # Group column (index 1)
                class_item = self.visualization_tableWidget.item(row, 2) # Class column (index 2)
                color_item = self.visualization_tableWidget.item(row, 3) # Color column (index 3)

                # Skip incomplete rows
                if not (condition_item and group_item and class_item and color_item):
                    continue

                condition_name = condition_item.text()
                group_name = group_item.text()
                class_type = class_item.text()
                color_hex = color_item.text()

                all_conditions.add(condition_name)

                # Update max_integer_group_id and NEW existing_integer_group_ids
                if group_name.startswith("Group "):
                    try:
                        group_id = int(group_name.split(" ")[1])
                        existing_integer_group_ids.add(group_id) # Add to new set
                        if group_id > max_id:
                            max_id = group_id
                    except ValueError:
                        pass # Ignore if it's "Group ABC" or malformed "Group X"

                # Update reference status for the group
                if group_name not in ref_status:
                    ref_status[group_name] = False # Assume no ref until found
                if class_type == "Reference":
                    ref_status[group_name] = True

                # Update colors used for the group
                if group_name not in colors_used:
                    colors_used[group_name] = set()
                colors_used[group_name].add(color_hex)

                # Update conditions in group for exact duplicate check
                if group_name not in group_data_by_group:
                    group_data_by_group[group_name] = {'conditions_in_group': set()}
                group_data_by_group[group_name]['conditions_in_group'].add(condition_name)

            except AttributeError:
                continue # Gracefully handle cases where an item might be None unexpectedly

        return {
            'max_integer_group_id': max_id,
            'all_existing_conditions': all_conditions,
            'group_ref_status': ref_status,
            'group_colors_used': colors_used,
            'group_data_by_group': group_data_by_group,
            'existing_integer_group_ids': existing_integer_group_ids # NEW return value
        }

    def _add_conditions_to_table_core(self, conditions_list_to_add):
        """
        Core logic for adding conditions to the visualization_tableWidget.
        It handles batch processing, duplicate conditions (assigning to new groups,
        prioritizing available integer group IDs), class (Reference/Experimental),
        and color assignment.
        """
        if not conditions_list_to_add:
            QMessageBox.information(self.MainWindow, "No Conditions to Add",
                                    "The provided list of conditions is empty.")
            return

        # Get the current state of the entire table
        table_state = self._get_table_state_for_group_logic()

        # Determine the default group name if no duplicates force a new group
        default_group_for_new_conditions = "Group 1"
        if self.visualization_tableWidget.rowCount() > 0:
            first_row_group_item = self.visualization_tableWidget.item(0, 1) # Group column (index 1)
            if first_row_group_item and first_row_group_item.text():
                default_group_for_new_conditions = first_row_group_item.text()
            else:
                print("Warning: First row in visualization_tableWidget has no group name. Defaulting to 'Group 1'.")

        # --- Check if ANY condition in the input list is a duplicate of ANY existing condition in the table ---
        assign_entire_batch_to_new_group = False
        for cond_name in conditions_list_to_add:
            if cond_name in table_state['all_existing_conditions']:
                assign_entire_batch_to_new_group = True
                break

        # --- Determine the SINGLE target group for the entire batch ---
        target_group_for_this_batch = default_group_for_new_conditions
        if assign_entire_batch_to_new_group:
            # Find the next available integer group ID (smallest positive integer not in use)
            next_available_group_id = 1
            while next_available_group_id in table_state['existing_integer_group_ids']:
                next_available_group_id += 1
            
            target_group_for_this_batch = f"Group {next_available_group_id}"

        # --- Initialize/Update tracking for the target group for this batch within our 'table_state' ---
        # This ensures we are tracking correctly for the specific group we are adding to during this call.
        if target_group_for_this_batch not in table_state['group_ref_status']:
            table_state['group_ref_status'][target_group_for_this_batch] = False
        if target_group_for_this_batch not in table_state['group_colors_used']:
            table_state['group_colors_used'][target_group_for_this_batch] = set()
        if target_group_for_this_batch not in table_state['group_data_by_group']:
            table_state['group_data_by_group'][target_group_for_this_batch] = {'conditions_in_group': set()}

        # Get the specific tracking data for the determined batch group (will be updated dynamically)
        current_group_has_reference_status = table_state['group_ref_status'][target_group_for_this_batch]
        colors_used_in_target_group = table_state['group_colors_used'][target_group_for_this_batch]
        group_conditions_set_for_batch_target = table_state['group_data_by_group'][target_group_for_this_batch]['conditions_in_group']

        # Tracking for this specific batch's additions within the target group
        first_condition_in_batch_eligible_for_reference = not current_group_has_reference_status
        
        # Determine initial color index for this batch within the target group
        next_color_palette_index = 0
        if colors_used_in_target_group:
            # Try to find a good starting point for color cycling (arbitrarily pick after the last used color)
            last_color_used_in_group = next(iter(colors_used_in_target_group), None)
            if last_color_used_in_group and last_color_used_in_group in _COLOR_PALETTE:
                start_index_for_color = (_COLOR_PALETTE.index(last_color_used_in_group) + 1) % len(_COLOR_PALETTE)
                next_color_palette_index = start_index_for_color


        # --- Process each condition to add to the table ---
        for condition_name in conditions_list_to_add:
            # Check if this exact condition already exists within the determined target group (e.g., if adding same batch twice)
            if condition_name in group_conditions_set_for_batch_target:
                print(f"Condition '{condition_name}' already exists in group '{target_group_for_this_batch}'. Skipping this exact duplicate within the same group for this batch.")
                continue

            # Determine Class: 'Reference' or 'Experimental'
            condition_class = "Experimental"
            if first_condition_in_batch_eligible_for_reference:
                condition_class = "Reference"
                first_condition_in_batch_eligible_for_reference = False # Only the first one in this batch gets Reference if eligible
                current_group_has_reference_status = True # Update group status internally for this batch's additions

            # Determine Color: Auto-populate with hex-code, unique per group
            selected_color_hex = None
            for i in range(len(_COLOR_PALETTE)):
                candidate_color = _COLOR_PALETTE[(next_color_palette_index + i) % len(_COLOR_PALETTE)]
                if candidate_color not in colors_used_in_target_group:
                    selected_color_hex = candidate_color
                    next_color_palette_index = (next_color_palette_index + i + 1) % len(_COLOR_PALETTE) # Update for next pick
                    break
            
            # Fallback if all colors in palette are used for this group (highly unlikely with default palette size)
            if selected_color_hex is None:
                selected_color_hex = _COLOR_PALETTE[next_color_palette_index % len(_COLOR_PALETTE)]
                next_color_palette_index = (next_color_palette_index + 1) % len(_COLOR_PALETTE)


            colors_used_in_target_group.add(selected_color_hex) # Mark this color as now used in the group

            # Add new row to the table
            row_pos = self.visualization_tableWidget.rowCount()
            self.visualization_tableWidget.insertRow(row_pos)

            # Create QTableWidgetItem for each column and populate the row
            condition_item = QTableWidgetItem(condition_name)
            group_item = QTableWidgetItem(target_group_for_this_batch)
            class_item = QTableWidgetItem(condition_class)
            color_item = QTableWidgetItem(selected_color_hex)

            # Set the text color of the 'Color' column cell to the hex code specified
            color_brush = QBrush(QColor(selected_color_hex))
            color_item.setForeground(color_brush)

            # Set items in the table
            self.visualization_tableWidget.setItem(row_pos, 0, condition_item)
            self.visualization_tableWidget.setItem(row_pos, 1, group_item)
            self.visualization_tableWidget.setItem(row_pos, 2, class_item)
            self.visualization_tableWidget.setItem(row_pos, 3, color_item)

            # Update the in-memory sets for tracking exact duplicates within the target group for this batch
            group_conditions_set_for_batch_target.add(condition_name)


        # --- Run Validation after the entire batch is processed ---
        self._validate_visualization_table()

    def add_all_conditions_to_visualization_table(self):
        """
        Gathers all conditions from the vis_conditions_comboBox and
        passes them to the core logic to add to the table.
        """
        all_conditions = [self.vis_conditions_comboBox.itemText(i) for i in range(self.vis_conditions_comboBox.count())]
        self._add_conditions_to_table_core(all_conditions)

    def add_selected_condition_to_visualization_table(self):
        """
        Adds only the currently selected condition from vis_conditions_comboBox
        to the table using the core logic.
        """
        selected_condition = self.vis_conditions_comboBox.currentText()
        if not selected_condition:
            QMessageBox.information(self.MainWindow, "No Condition Selected",
                                    "Please select a condition from the dropdown to add.")
            return
        
        self._add_conditions_to_table_core([selected_condition])

    def remove_highlighted_conditions_from_visualization_table(self):
        """
        Removes all highlighted (selected) conditions from the visualization_tableWidget.
        Ensures that each remaining group has exactly one 'Reference' condition.
        If a 'Reference' condition is removed, the first remaining condition in that group
        will be designated as the new 'Reference'.
        """
        selected_rows = set()
        # Get all selected cell items
        for item in self.visualization_tableWidget.selectedItems():
            selected_rows.add(item.row())

        if not selected_rows:
            QMessageBox.information(self.MainWindow, "No Conditions Selected",
                                    "Please select conditions in the table to remove them.")
            return

        # Store affected groups for re-evaluation after deletion
        affected_groups = set()
        
        # Iterate through selected rows in reverse order to avoid index issues during deletion
        sorted_selected_rows = sorted(list(selected_rows), reverse=True)

        for row_index in sorted_selected_rows:
            group_item = self.visualization_tableWidget.item(row_index, 1) # Group column
            if group_item:
                affected_groups.add(group_item.text())
            self.visualization_tableWidget.removeRow(row_index)

        # Re-evaluate affected groups for 'Reference' status
        if affected_groups:
            self._ensure_single_reference_per_group(affected_groups)
        
        # Finally, run a full validation of the table
        self._validate_visualization_table()


    def remove_all_conditions_from_visualization_table(self):
        """
        Removes all conditions from the visualization_tableWidget.
        """
        if self.visualization_tableWidget.rowCount() == 0:
            QMessageBox.information(self.MainWindow, "Table Already Empty",
                                    "The visualization table is already empty.")
            return

        reply = QMessageBox.question(self.MainWindow, 'Clear Table',
                                     "Are you sure you want to remove all conditions from the table?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.visualization_tableWidget.setRowCount(0) # Clear all rows
            QMessageBox.information(self.MainWindow, "Table Cleared",
                                    "All conditions have been removed from the table.")
            # No need to reassign references since all groups are gone
            self._validate_visualization_table() # Validate to ensure an empty table is considered valid

    def _validate_visualization_table(self):
        """
        Validates the entire visualization_tableWidget to ensure:
        1. Exactly one 'Reference' condition per group.
        2. All other conditions in the group are 'Experimental'.
        Displays warnings if inconsistencies are found.
        """
        group_validation_data = {} # {group_name: {'reference_count': int, 'experimental_count': int}}

        for row in range(self.visualization_tableWidget.rowCount()):
            try:
                group_item = self.visualization_tableWidget.item(row, 1)
                class_item = self.visualization_tableWidget.item(row, 2)

                if group_item is None or class_item is None:
                    continue

                group = group_item.text()
                class_type = class_item.text()

                if group not in group_validation_data:
                    group_validation_data[group] = {'reference_count': 0, 'experimental_count': 0}

                if class_type == "Reference":
                    group_validation_data[group]['reference_count'] += 1
                elif class_type == "Experimental":
                    group_validation_data[group]['experimental_count'] += 1
                else:
                    QMessageBox.warning(
                        self.MainWindow,
                        "Invalid Class Type",
                        f"Row {row+1} in Group '{group}' has an unrecognized class type: '{class_type}'. "
                        "Expected 'Reference' or 'Experimental'."
                    )

            except AttributeError:
                continue

        errors = []
        for group_name, counts in group_validation_data.items():
            if counts['reference_count'] == 0:
                errors.append(f"Group '{group_name}' has no 'Reference' condition.")
            elif counts['reference_count'] > 1:
                errors.append(f"Group '{group_name}' has {counts['reference_count']} 'Reference' conditions. Only one is allowed per group.")

        if errors:
            QMessageBox.warning(
                self.MainWindow,
                "Visualization Table Consistency Issues",
                "The 'Visualization Table' has inconsistencies:\n\n" + "\n".join(errors) +
                "\n\nPlease review and correct the entries."
            )

    # Modified Helper method for consistent Reference/Experimental logic application
    def _ensure_single_reference_per_group(self, group_names_to_check, 
                                            user_selected_rows_for_reference=None, 
                                            user_selected_rows_for_experimental=None):
        """
        Ensures that each specified group (or all groups if empty) has exactly one 'Reference' condition.
        Prioritizes user's explicit selections if provided.
        Fixes inconsistencies by promoting/demoting conditions and notifies the user via QMessageBox.
        """
        user_selected_rows_for_reference = user_selected_rows_for_reference if user_selected_rows_for_reference is not None else set()
        user_selected_rows_for_experimental = user_selected_rows_for_experimental if user_selected_rows_for_experimental is not None else set()

        table_state = self._get_table_state_for_group_logic()
        
        # If no specific groups are provided, check all groups currently in the table
        if not group_names_to_check:
            group_names_to_check = set(table_state['group_ref_status'].keys())

        # Track messages for the user
        info_messages = []

        for group_name in group_names_to_check:
            # Skip groups that no longer exist in the table
            if group_name not in table_state['group_ref_status']:
                continue 

            conditions_in_group = [] # List of (row_index, condition_name, current_class) for this group
            for row in range(self.visualization_tableWidget.rowCount()):
                g_item = self.visualization_tableWidget.item(row, 1)
                c_item = self.visualization_tableWidget.item(row, 2)
                cond_item = self.visualization_tableWidget.item(row, 0)
                if g_item and g_item.text() == group_name and c_item and cond_item:
                    conditions_in_group.append((row, cond_item.text(), c_item.text()))
            
            # Sort by row index to ensure consistent "first" condition
            conditions_in_group.sort(key=lambda x: x[0])

            current_references_in_group = [] # List of (row_index, condition_name) for current References
            for row_idx, cond_name, class_type in conditions_in_group:
                if class_type == "Reference":
                    current_references_in_group.append((row_idx, cond_name))

            # --- Apply preference for user-explicitly set 'Reference' ---
            preferred_reference_row = -1
            preferred_reference_cond_name = ""

            # Check if any selected row was explicitly set to Reference
            selected_refs_in_group = sorted([r for r, _, _ in conditions_in_group if r in user_selected_rows_for_reference])
            if selected_refs_in_group:
                preferred_reference_row = selected_refs_in_group[0] # Take the lowest indexed one among user selections
                preferred_reference_cond_name = self.visualization_tableWidget.item(preferred_reference_row, 0).text()
                
                # Make sure this preferred one is indeed Reference and demote others
                for row_idx, cond_name, _ in conditions_in_group:
                    class_item = self.visualization_tableWidget.item(row_idx, 2)
                    if class_item:
                        if row_idx == preferred_reference_row:
                            if class_item.text() != "Reference":
                                class_item.setText("Reference")
                                info_messages.append(f"Group '{group_name}': '{cond_name}' explicitly set as 'Reference'.")
                        else:
                            if class_item.text() == "Reference":
                                class_item.setText("Experimental")
                                info_messages.append(f"Group '{group_name}': '{cond_name}' automatically changed to 'Experimental'.")
                continue # Group fixed, move to next group

            # --- If no user-selected 'Reference' (or set_experimental was called), apply general logic ---
            # Re-gather references after any direct setting in calling methods
            current_references_in_group = []
            for row_idx, cond_name, class_type in conditions_in_group:
                class_item = self.visualization_tableWidget.item(row_idx, 2) # Get fresh state
                if class_item and class_item.text() == "Reference":
                    current_references_in_group.append((row_idx, cond_name))
            current_references_in_group.sort(key=lambda x: x[0]) # Ensure sorted by row index

            # Case 1: Multiple Reference conditions found in the group (after initial explicit setting)
            if len(current_references_in_group) > 1:
                # Keep the first one encountered (lowest row index) as Reference
                # and change others to Experimental
                ref_to_keep_row_idx, ref_to_keep_cond_name = current_references_in_group[0]
                
                for i in range(1, len(current_references_in_group)):
                    other_ref_row_idx, other_ref_cond_name = current_references_in_group[i]
                    class_item = self.visualization_tableWidget.item(other_ref_row_idx, 2)
                    if class_item:
                        class_item.setText("Experimental")
                        info_messages.append(f"Group '{group_name}': '{other_ref_cond_name}' automatically changed to 'Experimental' (only '{ref_to_keep_cond_name}' remains 'Reference').")
            
            # Case 2: No Reference condition found in the group (and group is not empty)
            elif not current_references_in_group and conditions_in_group:
                # Find the best candidate for reference
                candidate_for_reference_row_idx = -1
                candidate_for_reference_cond_name = ""

                # Prefer a non-explicitly-experimental row
                for row_idx, cond_name, class_type in conditions_in_group:
                    if row_idx not in user_selected_rows_for_experimental:
                        candidate_for_reference_row_idx = row_idx
                        candidate_for_reference_cond_name = cond_name
                        break # Found the first suitable candidate

                # If all conditions were explicitly set to Experimental, pick the first one among them
                if candidate_for_reference_row_idx == -1:
                    candidate_for_reference_row_idx, candidate_for_reference_cond_name, _ = conditions_in_group[0]

                class_item = self.visualization_tableWidget.item(candidate_for_reference_row_idx, 2)
                if class_item:
                    class_item.setText("Reference")
                    info_messages.append(f"Group '{group_name}': '{candidate_for_reference_cond_name}' automatically set as 'Reference'.")
        
        if info_messages:
            QMessageBox.information(
                self.MainWindow,
                "Reference/Experimental Logic Applied",
                "Adjustments were made to ensure correct 'Reference' conditions:\n\n" + "\n".join(info_messages)
            )

        # Always re-run the full validation for final consistency check and error reporting
        self._validate_visualization_table()


    def set_group_for_selected_rows(self):
        """
        Sets the group name for all selected rows.
        A QInputDialog prompts for the new group name.
        Prevents moving conditions into a group where that condition name already exists.
        Logic is applied to ensure exactly one reference per group after the change.
        """
        selected_rows = set()
        for item in self.visualization_tableWidget.selectedItems():
            selected_rows.add(item.row())
        
        if not selected_rows:
            QMessageBox.information(self.MainWindow, "No Conditions Selected",
                                    "Please select conditions in the table to set their group.")
            return

        # Get the new group name from the user
        new_group_name, ok = QInputDialog.getText(
            self.MainWindow, "Set Group Name", "Enter the new group name:"
        )

        if not ok or not new_group_name:
            if ok: # User clicked OK but entered empty string
                QMessageBox.warning(self.MainWindow, "Invalid Group Name", "Group name cannot be empty.")
            return # User cancelled or entered empty name

        # --- Check for duplicate conditions within the target group ---
        conditions_to_be_moved = set()
        for row_idx in selected_rows:
            condition_item = self.visualization_tableWidget.item(row_idx, 0)
            if condition_item:
                conditions_to_be_moved.add(condition_item.text())

        current_conditions_in_new_group = set()
        for row_idx in range(self.visualization_tableWidget.rowCount()):
            # Only consider rows NOT being moved (i.e., existing members of the target group)
            if row_idx not in selected_rows:
                group_item = self.visualization_tableWidget.item(row_idx, 1)
                condition_item = self.visualization_tableWidget.item(row_idx, 0)
                if group_item and group_item.text() == new_group_name and condition_item:
                    current_conditions_in_new_group.add(condition_item.text())

        conflicting_conditions = conditions_to_be_moved.intersection(current_conditions_in_new_group)

        if conflicting_conditions:
            conflict_list = "\n- " + "\n- ".join(sorted(list(conflicting_conditions)))
            QMessageBox.warning(
                self.MainWindow,
                "Duplicate Condition Conflict",
                f"The following condition(s) already exist in group '{new_group_name}':{conflict_list}\n\n"
                "A group cannot contain duplicate condition names. Please choose a different group or rename the conflicting conditions."
            )
            return # Stop the operation if conflicts exist

        # --- If no conflicts, proceed with setting the new group ---
        affected_groups = set() # Track groups that might need re-validation of reference status

        # Collect original group names of selected rows before changing them
        for row_idx in selected_rows:
            group_item = self.visualization_tableWidget.item(row_idx, 1)
            if group_item:
                affected_groups.add(group_item.text())

        # Apply the new group name to selected rows
        for row_idx in selected_rows:
            group_item = self.visualization_tableWidget.item(row_idx, 1)
            if group_item:
                group_item.setText(new_group_name)
        
        affected_groups.add(new_group_name) # Add the new group name to affected groups

        # Apply logic to ensure exactly one reference per group
        self._ensure_single_reference_per_group(affected_groups)


    def set_reference_for_selected_rows(self):
        """
        Sets the class of all selected rows to "Reference".
        Logic is applied to ensure exactly one reference per group after the change,
        prioritizing the user's explicit selection.
        """
        selected_rows = set()
        for item in self.visualization_tableWidget.selectedItems():
            selected_rows.add(item.row())
        
        if not selected_rows:
            QMessageBox.information(self.MainWindow, "No Conditions Selected",
                                    "Please select conditions in the table to set them as 'Reference'.")
            return

        affected_groups = set()
        for row_idx in selected_rows:
            class_item = self.visualization_tableWidget.item(row_idx, 2)
            group_item = self.visualization_tableWidget.item(row_idx, 1)
            if class_item and group_item:
                class_item.setText("Reference")
                affected_groups.add(group_item.text())
        
        self._ensure_single_reference_per_group(affected_groups, user_selected_rows_for_reference=selected_rows)

    def set_experimental_for_selected_rows(self):
        """
        Sets the class of all selected rows to "Experimental".
        Logic is applied to ensure exactly one reference per group after the change,
        prioritizing the user's explicit selection.
        """
        selected_rows = set()
        for item in self.visualization_tableWidget.selectedItems():
            selected_rows.add(item.row())
        
        if not selected_rows:
            QMessageBox.information(self.MainWindow, "No Conditions Selected",
                                    "Please select conditions in the table to set them as 'Experimental'.")
            return

        affected_groups = set()
        for row_idx in selected_rows:
            class_item = self.visualization_tableWidget.item(row_idx, 2)
            group_item = self.visualization_tableWidget.item(row_idx, 1)
            if class_item and group_item:
                class_item.setText("Experimental")
                affected_groups.add(group_item.text())

        self._ensure_single_reference_per_group(affected_groups, user_selected_rows_for_experimental=selected_rows)


    def set_color_for_selected_conditions(self):
        """
        Sets the color of selected conditions using a custom color selection dialog.
        The dialog provides preset colors, RGB/Hex input, a color wheel (via QColorDialog),
        and displays colors already in use in the table.
        """
        selected_rows = set()
        for item in self.visualization_tableWidget.selectedItems():
            selected_rows.add(item.row())
        
        if not selected_rows:
            QMessageBox.information(self.MainWindow, "No Conditions Selected",
                                    "Please select conditions in the table to set their color.")
            return

        table_state = self._get_table_state_for_group_logic()
        all_used_colors = set()
        for group_colors in table_state['group_colors_used'].values():
            all_used_colors.update(group_colors)

        # Get initial color from the first selected item, or default
        initial_color_hex = "#1f77b4" # Default if no selection
        if selected_rows:
            first_selected_row = next(iter(selected_rows))
            color_item = self.visualization_tableWidget.item(first_selected_row, 3)
            if color_item:
                initial_color_hex = color_item.text()

        color_dialog = ColorSelectionDialog(self.MainWindow, initial_color_hex, all_used_colors)
        if color_dialog.exec() == QDialog.Accepted:
            selected_color_hex = color_dialog.get_selected_color_hex()
            selected_color_qcolor = QColor(selected_color_hex)
            
            for row_idx in selected_rows:
                color_item = self.visualization_tableWidget.item(row_idx, 3)
                if color_item:
                    color_item.setText(selected_color_hex)
                    color_item.setForeground(QBrush(selected_color_qcolor))
            
            # Re-validate to ensure consistency, especially if color changes affect interpretation (though not standard here)
            self._validate_visualization_table()
    
    def browse_output_directory(self):
        """
        Opens a directory dialog to select the output directory.
        The selected directory's full path is then displayed in the output_directory_lineEdit.
        """
        initial_dir = self.run_outputdir_lineEdit.text()
        if not os.path.isdir(initial_dir):
            initial_dir = os.path.expanduser("~") # Fallback to user home directory if current text is not a valid path

        # Open a directory selection dialog
        directory = QFileDialog.getExistingDirectory(
            self.MainWindow,
            "Select Output Directory",
            initial_dir,
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )

        if directory:
            self.run_outputdir_lineEdit.setText(directory)
    
    def open_output_directory(self):
        """
        Opens the directory specified in the output_directory_lineEdit.
        Displays an error message if the directory is invalid or does not exist.
        """
        directory_path = self.run_outputdir_lineEdit.text()
    
        if not directory_path:
            QMessageBox.warning(self.MainWindow, "Invalid Directory", "The output directory path cannot be empty.")
            return
    
        # Check if the path exists and is a directory
        if os.path.isdir(directory_path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(directory_path))
        else:
            QMessageBox.warning(self.MainWindow, "Directory Not Found",
                                f"The specified output directory does not exist:\n{directory_path}")
                   
    # Store the original working directory to revert to later
    _original_cwd = None
    # Reference to the currently running script worker
    current_script_runner = None
    
    def export_headless(self):
        """
        Creates files for running CHalf headless:
        1. Sets the working directory.
        2. Saves workflow, manifest, and visualization files.
        3. Provides suggested script for running headless CHalf.
        """
        # Ensure the output directory line edit has content
        output_dir = self.run_outputdir_lineEdit.text()
        self._current_output_dir = output_dir

        if not output_dir:
            QMessageBox.warning(self.MainWindow, "Missing Output Directory",
                                "Please select an output directory before exporting.")
            return

        # Initialize the TextEditLogger and redirect stdout/stderr early
        # This ensures all subsequent prints/writes go to the log
        self.text_edit_logger = TextEditLogger(self.run_log_textEdit)
        sys.stdout = self.text_edit_logger
        sys.stderr = self.text_edit_logger

        # Force clear the log for a new run
        self.run_log_textEdit.clear()


        # Create the directory if it doesn't exist
        if not os.path.isdir(output_dir):
            try:
                os.makedirs(output_dir)
                self.logger.write(f"Created output directory: {output_dir}\n")
                QApplication.processEvents() # Force GUI update
            except OSError as e:
                QMessageBox.critical(self.MainWindow, "Error Creating Directory",
                                     f"Could not create output directory '{output_dir}': {e}")
                self._on_script_finished() # Reset UI on error
                return

        # Store the current working directory before changing it
        self._original_cwd = os.getcwd()
        try:
            # Change to the selected output directory (where files will be saved and script will run)
            #os.chdir(output_dir) # If you uncomment this, ensure paths used by subprocess are absolute if needed
            self.logger.write(f"Changed working directory to: {output_dir}\n")
            QApplication.processEvents() # Force GUI update
        except OSError as e:
            QMessageBox.critical(self.MainWindow, "Error Setting Working Directory",
                                 f"Could not change working directory to '{output_dir}': {e}")
            self._on_script_finished() # Reset UI on error
            return # Abort if directory change fails

        self.logger.write("Exporting CHalf parameter files for running headless...\n")
        QApplication.processEvents() # Force GUI update

        # NEW: Add the filler line before the script execution begins
        msg = '~'*100
        self.logger.write_raw(f"{msg}\n")
        QApplication.processEvents() # Force GUI update

        # Store the start time for the "ALL JOBS DONE" message calculation

        try:
            # Call your existing methods to save configuration files
            # These methods are assumed to save files relative to the current working directory
            self.start_write_parameter_file(output_dir)
            self.start_save_manifest_file(output_dir)
            self.start_save_vis_file(output_dir)
            self.logger.write("Workflow, Manifest, and Visualization files saved successfully.\n")
            self.logger.write("Suggested command for running headless:\n")
            self.logger.write_raw(f'CHalf_v4_3_headless.exe --workflow "{output_dir}/params.workflow" --manifest "{output_dir}/run.manifest" --directory "{output_dir}/test"\n')
            self.logger.write_raw('Optionally, you may include the --log flag with a file name to save the headless results to a file.')
            QApplication.processEvents() # Force GUI update
        except Exception as e:
            QMessageBox.critical(self.MainWindow, "File Save Error",
                                 f"An error occurred while saving configuration files: {e}")
            self.logger.write(f"ERROR: File save failed - {e}\n")
            return
    
    def start_run(self):
        """
        Initiates the CHalf run process:
        1. Sets the working directory.
        2. Disables 'Start' and enables 'Stop' buttons.
        3. Saves workflow, manifest, and visualization files.
        4. Starts the bioinformatics script in a separate thread, logging output.
        """
        # Ensure the output directory line edit has content
        output_dir = self.run_outputdir_lineEdit.text()
        self._current_output_dir = output_dir

        if not output_dir:
            QMessageBox.warning(self.MainWindow, "Missing Output Directory",
                                "Please select an output directory before starting the run.")
            return

        # Initialize the TextEditLogger and redirect stdout/stderr early
        # This ensures all subsequent prints/writes go to the log
        self.text_edit_logger = TextEditLogger(self.run_log_textEdit)
        sys.stdout = self.text_edit_logger
        sys.stderr = self.text_edit_logger

        # Force clear the log for a new run
        self.run_log_textEdit.clear()


        # Create the directory if it doesn't exist
        if not os.path.isdir(output_dir):
            try:
                os.makedirs(output_dir)
                self.logger.write(f"Created output directory: {output_dir}\n")
                QApplication.processEvents() # Force GUI update
            except OSError as e:
                QMessageBox.critical(self.MainWindow, "Error Creating Directory",
                                     f"Could not create output directory '{output_dir}': {e}")
                self._on_script_finished() # Reset UI on error
                return

        # Store the current working directory before changing it
        self._original_cwd = os.getcwd()
        try:
            # Change to the selected output directory (where files will be saved and script will run)
            #os.chdir(output_dir) # If you uncomment this, ensure paths used by subprocess are absolute if needed
            self.logger.write(f"Changed working directory to: {output_dir}\n")
            QApplication.processEvents() # Force GUI update
        except OSError as e:
            QMessageBox.critical(self.MainWindow, "Error Setting Working Directory",
                                 f"Could not change working directory to '{output_dir}': {e}")
            self._on_script_finished() # Reset UI on error
            return # Abort if directory change fails

        # Disable Start, Enable Stop, Disable Clear Log during run
        self.run_start_pushButton.setEnabled(False)
        self.run_stop_pushButton.setEnabled(True)
        self.run_log_clear_pushButton.setEnabled(False) # Prevent clearing log while script runs

        self.logger.write("Starting CHalf run...\n")
        QApplication.processEvents() # Force GUI update

        # NEW: Add the filler line before the script execution begins
        msg = '~'*100
        self.logger.write_raw(f"{msg}\n")
        QApplication.processEvents() # Force GUI update

        # Store the start time for the "ALL JOBS DONE" message calculation
        self._job_start_time = time.time() 

        try:
            # Call your existing methods to save configuration files
            # These methods are assumed to save files relative to the current working directory
            self.start_write_parameter_file(output_dir)
            self.start_save_manifest_file(output_dir)
            self.start_save_vis_file(output_dir)
            self.logger.write("Workflow, Manifest, and Visualization files saved successfully.\n")
            QApplication.processEvents() # Force GUI update
        except Exception as e:
            QMessageBox.critical(self.MainWindow, "File Save Error",
                                 f"An error occurred while saving configuration files: {e}")
            self.logger.write(f"ERROR: File save failed - {e}\n")
            self._on_script_finished() # Revert button states, etc.
            return

        # Define the path to your bioinformatics script
        script_to_run = "CHalf_v4_3.py"
        script_args = []
        if os.path.exists(f'{output_dir}/params.workflow'): script_args.extend(['--workflow', f'{output_dir}/params.workflow'])
        if os.path.exists(f'{output_dir}/run.manifest'): script_args.extend(['--manifest', f'{output_dir}/run.manifest'])
        if os.path.exists(f'{output_dir}/visualization_config.vis'): script_args.extend(['--visual', f'{output_dir}/visualization_config.vis'])
        script_args.extend(['--directory', self._current_output_dir])

        # Create an instance of the ScriptRunner
        self.current_script_runner = ScriptRunner(script_to_run, script_args, self.logger)
        
        # Connect signals from the ScriptRunner to slots in the main UI thread
        self.current_script_runner.finished.connect(self._on_script_finished)
        self.current_script_runner.error.connect(self._on_script_error)

        # Start the script runner in the thread pool
        # Ensure self.thread_pool is initialized in your Ui_MainWindow's __init__
        if not hasattr(self, 'thread_pool'):
            self.thread_pool = QThreadPool()
            self.thread_pool.setMaxThreadCount(1) # Or more if you allow multiple concurrent scripts

        self.thread_pool.start(self.current_script_runner)
        self.logger.write(f"Initiated background script: {script_to_run}...\n")
        QApplication.processEvents() # Force GUI update


    def stop_run(self):
        """
        Attempts to stop the currently running bioinformatics script.
        """
        if self.current_script_runner:
            self.current_script_runner.stop() # This will call terminate on the subprocess
            # The _on_script_finished will be triggered by ScriptRunner's 'finished' signal
            # after termination, and will handle UI reset.
        else:
            self.logger.write("No script is currently running to stop.\n")
            QApplication.processEvents()
            # Ensure buttons are in correct state if stop was pressed with no active runner
            self.run_start_pushButton.setEnabled(True)
            self.run_stop_pushButton.setEnabled(False)
            self.run_log_clear_pushButton.setEnabled(True)


    def _on_script_finished(self):
        """
        Slot connected to ScriptRunner.finished signal.
        Handles post-script-execution cleanup and UI state changes.
        """
        # Always revert to the original working directory
        if hasattr(self, '_original_cwd') and self._original_cwd and os.path.isdir(self._original_cwd):
            try:
                os.chdir(self._original_cwd)
                self.logger.write(f"Reverted working directory to: {self._original_cwd}\n")
                QApplication.processEvents()
            except OSError as e:
                self.logger.write(f"Warning: Could not revert working directory to {self._original_cwd}: {e}\n")
                QApplication.processEvents()

        # Re-enable Start, Disable Stop, Enable Clear Log
        self.run_start_pushButton.setEnabled(True)
        self.run_stop_pushButton.setEnabled(False)
        self.run_log_clear_pushButton.setEnabled(True)
        
        self.current_script_runner = None # Clear the reference to the finished runner

        self.logger.write("CHalf run process completed.\n")
        QApplication.processEvents()

        # NEW: Calculate total time and display the completion message
        if hasattr(self, '_job_start_time') and self._job_start_time is not None:
            total_time_seconds = time.time() - self._job_start_time
            total_time_minutes = total_time_seconds / 60.0
            self.logger.write_completion_message(total_time_minutes)
            QApplication.processEvents() # Ensure this last message is also displayed
        
        self.save_log_automatically()


    def _on_script_error(self, message):
        """
        Slot connected to ScriptRunner.error signal.
        Displays critical errors from the script execution.
        """
        QMessageBox.critical(self.MainWindow, "Script Execution Error", message)
        self.logger.write(f"ERROR: {message}\n") # Also log the error in the text edit
        QApplication.processEvents() # Force GUI update for the error message
        self.logger.write(f"ERROR: {message}\n") # Also log the error in the text edit
        self._on_script_finished() # Call the finished handler to reset UI state
        """
        Slot connected to ScriptRunner.error signal.
        Displays critical errors from the script execution.
        """
        QMessageBox.critical(self.MainWindow, "Script Execution Error", message)
        
    # NEW METHOD: Automatic Log Saving
    @Slot()
    def save_log_automatically(self):
        """
        Automatically saves the content of the log (run_log_textEdit)
        to a text file named 'log_{timestamp}.txt' in the current output directory.
        This method is called when the script finishes or encounters an error.
        """
        # Use the stored output directory from start_run
        output_dir = self._current_output_dir

        if not output_dir or not os.path.isdir(output_dir):
            # Log to the GUI if the directory is invalid, but don't show a QMessageBox
            # as this is an automatic background save.
            self.logger.write(f"Warning: Cannot automatically save log. Output directory is not set or invalid: {output_dir}\n")
            QApplication.processEvents()
            return

        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"log_{timestamp_str}.txt"
        log_file_path = os.path.join(output_dir, log_filename)

        try:
            log_content = self.run_log_textEdit.toPlainText()
            with open(log_file_path, 'w', encoding='utf-8') as f:
                f.write(log_content)
            self.logger.write(f"Log automatically saved to: {log_file_path}\n")
            QApplication.processEvents()
        except Exception as e:
            self.logger.write(f"ERROR: Failed to automatically save log to {log_file_path}: {e}\n")
            QApplication.processEvents()
            # Optionally, you could show a QMessageBox here if auto-save failure is critical enough
            # QMessageBox.critical(self.MainWindow, "Auto-Save Log Error",
            #                      f"Failed to automatically save log to '{log_file_path}': {e}")


    # NEW METHOD: Manual Log Export
    @Slot()
    def export_log_manual(self):
        """
        Prompts the user to save the current content of the log (run_log_textEdit)
        to a text file using a QFileDialog.
        """
        # Get the default output directory from the line edit, or fall back to user home
        default_dir = self.run_outputdir_lineEdit.text()
        if not os.path.isdir(default_dir):
            default_dir = os.path.expanduser("~")

        # Suggest a filename with a timestamp
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        suggested_filename = f"chalf_log_export_{timestamp_str}.txt"
        default_path = os.path.join(default_dir, suggested_filename)

        file_path, _ = QFileDialog.getSaveFileName(
            self.MainWindow,
            "Export Log File",
            default_path,
            "Text Files (*.txt);;All Files (*)"
        )

        if file_path:
            try:
                log_content = self.run_log_textEdit.toPlainText()
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(log_content)
                QMessageBox.information(self.MainWindow, "Log Exported",
                                        f"Log successfully exported to:\n{file_path}")
                self.logger.write(f"Log manually exported to: {file_path}\n")
                QApplication.processEvents()
            except Exception as e:
                QMessageBox.critical(self.MainWindow, "Export Error",
                                     f"Failed to export log: {e}")
                self.logger.write(f"ERROR: Failed to manually export log to {file_path}: {e}\n")
                QApplication.processEvents()

    # NEW METHOD: Clear Log
    @Slot()
    def clear_log(self):
        """
        Clears all text from the run_log_textEdit after user confirmation.
        """
        if self.run_log_textEdit.toPlainText(): # Only ask if there's content
            reply = QMessageBox.question(self.MainWindow, 'Clear Log',
                                         "Are you sure you want to clear the log?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.run_log_textEdit.clear()
                self.logger.write_raw(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Log cleared by user.\n")
                QApplication.processEvents()
        else:
            QMessageBox.information(self.MainWindow, "Log Already Empty", "The log is already empty.")
    
if __name__ == "__main__":
    global_logger = TextEditLogger()
    sys.stdout = global_logger
    sys.stderr = global_logger
    # 1. Create the Application instance
    #    (sys.argv allows passing command line arguments to the application)
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    else:
        print('QApplication instance already exists: %s' % str(app))
    
    #app.setStyleSheet(light_stylesheet)
    
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
    # 2. Create the Main Window instance
    #    This is the actual window object.'''
    MainWindow = QMainWindow()
    
    try:
        icon = QIcon('images/CHalf Protein Logo.png')
        MainWindow.setWindowIcon(icon)
    except Exception as e:
        print(e)
        print('CHalf Protein Logo.png missing from /images')

    # 3. Create an instance of your UI definition class
    ui = Ui_MainWindow()

    # 4. Call the setupUi method to build the UI onto the MainWindow
    ui.setupUi(MainWindow)

    # 5. Show the Main Window
    global_logger.set_text_edit(ui.run_log_textEdit)
    MainWindow.show()

    # 6. Start the application's event loop and handle exit
    #    The event loop waits for user interactions (clicks, etc.)
    #    sys.exit() ensures the application closes cleanly.
    sys.exit(app.exec())