# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 12:46:05 2024

@author: chadhyer

LICENSE:

Copyright (c) 2022 Chad D. Hyer, Connor Hadderly, Monica Berg, Hsien-Jung Lavender Lin, John C. Price, and Brigham Young University
All rights reserved.
Redistribution and use in source and binary forms,
with or without modification, are permitted provided
that the following conditions are met:
    * Redistributions of source code must retain the
      above copyright notice, this list of conditions
      and the following disclaimer.
    * Redistributions in binary form must reproduce
      the above copyright notice, this list of conditions
      and the following disclaimer in the documentation
      and/or other materials provided with the distribution.
    * Neither the author nor the names of any contributors
      may be used to endorse or promote products derived
      from this software without specific prior written
      permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


CITATION:
    
Hyer, C. D.; Lin, H.-J. L.; Haderlie, C. T.; Berg, M.; Price, J. C. 
CHalf: Folding Stability Made Simple. 
Journal of Proteome Research 2023, 22 (2), 605-614. 
DOI: 10.1021/acs.jproteome.2c00619.


"""

import matplotlib
matplotlib.use('Agg') # Set the backend to 'Agg' for non-interactive plotting
import matplotlib.backends.backend_svg

import warnings, re, time, argparse, ast, inspect, os, random, subprocess, math, sys, traceback

import matplotlib.pyplot as plt  # must have 'pillow' downloaded for jpg support
import seaborn as sns
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy.stats import t, spearmanr
import scipy.stats as stats
from scipy.signal import savgol_filter
from matplotlib.colors import is_color_like
import matplotlib.ticker as ticker
import altair as alt
from datetime import timedelta

citation = '[NO_TIMESTAMP]Hyer, C. D.; Lin, H.-J. L.; Haderlie, C. T.; Berg, M.; Price, J. C.\n[NO_TIMESTAMP]CHalf: Folding Stability Made Simple.\n[NO_TIMESTAMP]Journal of Proteome Research 2023, 22 (2), 605-614.\n[NO_TIMESTAMP]DOI: 10.1021/acs.jproteome.2c00619.'


def to_dict(x):
        try:
            # Safely evaluate the string as a Python literal
            evaluated_val = ast.literal_eval(x)
            # Check if the evaluated value is indeed a dictionary
            if isinstance(evaluated_val, dict):
                return evaluated_val
            else:
                return None  # Or handle non-dictionary cases as needed
        except (ValueError, SyntaxError):
            return None  # Handle cases where string is not a valid literal

class ParameterDict(dict):
    """
    A dictionary subclass that allows accessing and setting nested dictionary keys
    as attributes using dot notation. When a nested dictionary is accessed,
    it is converted into another ParameterDict instance for seamless hierarchical access.
    """
    def __getattr__(self, name):
        """
        Allows accessing dictionary keys as attributes (e.g., obj.key).
        If the value is a dictionary, it's wrapped in a ParameterDict for nested access.
        """
        try:
            value = self[name]
            if isinstance(value, dict) and not isinstance(value, ParameterDict):
                # If the value is a plain dict, convert it to a ParameterDict
                # and store it back to ensure subsequent accesses are also ParameterDicts.
                self[name] = ParameterDict(value)
                return self[name]
            return value
        except KeyError:
            # If the key does not exist, raise an AttributeError, consistent with attribute access.
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        """
        Allows setting dictionary keys as attributes (e.g., obj.key = value).
        Handles conversion of nested dictionaries to ParameterDicts upon assignment.
        """
        # Check if the attribute name is one of the ParameterDict's own internal attributes
        # (e.g., methods or properties of the class itself).
        if name in self.__dict__:
            super().__setattr__(name, value)
        else:
            # Otherwise, treat it as setting a dictionary item.
            # If the value being assigned is a dictionary, convert it to a ParameterDict.
            if isinstance(value, dict) and not isinstance(value, ParameterDict):
                self[name] = ParameterDict(value)
            else:
                self[name] = value

def read_workflow(file_path: str) -> ParameterDict:
    """
    Reads a parameter file content into a hierarchical ParameterDict structure,
    conditionally including sub-sections based on top-level boolean flags.

    The file is expected to have lines in the format 'key=value'.
    Keys with periods (e.g., 'chalf.search.light') are interpreted as nested parameters.
    Lines starting with '#' or empty lines are ignored.
    Values are automatically converted to boolean (True/False) or float/int if possible;
    otherwise, they remain as strings.

    Sections controlled by a top-level boolean (e.g., 'chalf=False') will have their
    sub-parameters excluded from the final dictionary. The top-level flag itself
    (e.g., 'chalf') will always be included.

    Args:
        file_path: The path to the parameter file.

    Returns:
        A ParameterDict instance representing the hierarchical structure of the parameters.
        You can access parameters using dot notation (e.g., params.chalf.run).
    """
    try:
        with open(file_path, 'r') as f:
            file_content = f.read()

        # Step 1: Parse all lines into a flat dictionary with type conversion
        all_flat_params = {}
        for line in file_content.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, value_str = line.split('=', 1)
                key = key.strip()
                value_str = value_str.strip()

                # Convert value to appropriate type
                if value_str.lower() == 'true':
                    value = True
                elif value_str.lower() == 'false':
                    value = False
                else:
                    try:
                        value = int(value_str) # Try converting to int first
                    except ValueError:
                        try:
                            value = float(value_str)
                        except ValueError:
                            value = value_str
                all_flat_params[key] = value

        # Define the specific top-level keys that control their sub-sections
        controlling_keys = [
            'chalf', 'qc', 'visualization.rm', 'visualization.crm',
            'visualization.dm', 'visualization.cs'
        ]

        # Step 2: Filter the flat_params based on controlling flags
        filtered_flat_params = {}
        keys_to_remove_prefix = set() # Store prefixes whose sub-parameters should be removed

        # First, identify which top-level sections are disabled
        for controlling_key in controlling_keys:
            # A controlling key is considered 'False' if it exists and its value is explicitly False.
            # If it's True or doesn't exist, its section is considered active by default.
            if controlling_key in all_flat_params and all_flat_params[controlling_key] is False:
                keys_to_remove_prefix.add(controlling_key + '.')

        # Now, populate filtered_flat_params
        for full_key, value in all_flat_params.items():
            is_sub_param_of_disabled_section = False
            for prefix_to_remove in keys_to_remove_prefix:
                # Check if the current full_key starts with a prefix that should be removed
                # and is not the controlling key itself (which should always be kept).
                if full_key.startswith(prefix_to_remove) and full_key != prefix_to_remove[:-1]:
                    is_sub_param_of_disabled_section = True
                    break

            # If it's a sub-parameter of a disabled section, skip it.
            # Otherwise, include it.
            if not is_sub_param_of_disabled_section:
                filtered_flat_params[full_key] = value


        # Step 3: Build the nested dictionary structure from the filtered flat_params
        nested_params = {}
        for full_key, value in filtered_flat_params.items():
            parts = full_key.split('.')
            current_level = nested_params
            for i, part in enumerate(parts):
                if i == len(parts) - 1:
                    # If it's the last part of the key, assign the value
                    current_level[part] = value
                else:
                    # If it's an intermediate part, ensure the nested dictionary exists
                    # and move deeper into the structure.
                    if part not in current_level or not isinstance(current_level[part], dict):
                        current_level[part] = {}
                    current_level = current_level[part]

        # Recursively convert the entire nested dictionary structure into ParameterDict instances
        def convert_to_parameter_dict_recursive(obj):
            if isinstance(obj, dict):
                return ParameterDict({k: convert_to_parameter_dict_recursive(v) for k, v in obj.items()})
            return obj
        print("Workflow parameters successfully extracted.")
        return convert_to_parameter_dict_recursive(nested_params)

    except FileNotFoundError:
        raise FileNotFoundError(f"Cancelling run. Required input file not found: {file_path}")

def read_manifest(file):
    try:
        manifestDF = pd.read_csv(file,sep='\t',converters={'conc dict':to_dict},dtype={'File (path)':str,'Condition (unique string)':str,'Concentration columns (preset)':str})
        cols = ['File (path)', 'Condition (unique string)', 'Concentration columns (preset)', 'conc dict']
        for col in cols: 
            if col not in manifestDF.columns: raise ValueError('Manifest does not contain all the necessary columns. Aborting run.')
        return manifestDF
    except FileNotFoundError:
        raise FileNotFoundError('Manifest file not found. Aborting run')

def read_vis(file, working_dir):
    try:
        
        visDF = pd.read_csv(file,sep='\t',dtype={'Condition':str,'Group':str,'Class':str,'Color':str})
        cols = ['Condition', 'Group', 'Class', 'Color']
        for col in cols: 
            if col not in visDF.columns: raise ValueError('Visual config file does not contain all the necessary columns. Aborting run.')
    except FileNotFoundError:
        raise FileNotFoundError('Visual config file not found. Aborting run')
    groups_dict = {}
    for name, group in visDF.groupby(by='Group'):
        conditions_dict = {}
        for index, row in group.iterrows():
            conditions_dict.update({row['Condition']:(f'{working_dir}/{row["Condition"]}/{row["Condition"]} Combined Sites.csv',row["Color"],row["Class"].lower())})
        groups_dict.update({name:conditions_dict})
    return groups_dict

def read_ann_file(file_path: str) -> dict:
    """
    Reads an .ann file and extracts 'subset' (list) and 'custom_annotation' (dictionary).

    The .ann file is expected to contain Python-like assignments for 'subset' and
    'custom_annotation'. Other variables in the file will be ignored. If 'subset'
    or 'custom_annotation' are not present in the file, they will be represented
    as None in the returned dictionary.

    Args:
        file_path: The path to the .ann file.

    Returns:
        A dictionary containing the extracted 'subset' and 'custom_annotation' values.
        If a parameter is not found, its value will be None in the returned dictionary.
    """
    extracted_data = {
        'subset': None,
        'custom_annotation': None
    }
    
    # Use a dictionary to serve as the local namespace for exec.
    # This isolates the execution of the .ann file content.
    local_namespace = {}

    try:
        with open(file_path, 'r') as f:
            file_content = f.read()
        
        # Execute the file content in the local_namespace.
        # This allows the file to define variables as if it were a Python script.
        # The global namespace is kept empty ({}) to prevent unintended side effects.
        exec(file_content, {}, local_namespace)

        # Extract the variables if they exist in the local_namespace.
        # We use .get() for safety, though direct access with an 'in' check is also fine.
        if 'subset' in local_namespace:
            extracted_data['subset'] = local_namespace['subset']
        
        if 'custom_annotation' in local_namespace:
            extracted_data['custom_annotation'] = local_namespace['custom_annotation']

    except FileNotFoundError:
        print(f"Error: .ann file not found at '{file_path}'")
    except Exception as e:
        print(f"Error reading or parsing .ann file '{file_path}': {e}")
        traceback.print_exc()
        # In a production environment, you might want to log this error
        # or raise a more specific exception.

    return extracted_data

def progress_logger(current_iteration, total_iterations, description="", update_every_n_iterations=100, start_time=None):
    """
    Logs the progress of an iterative process, including percentage, iterations per second,
    and estimated time of completion.

    Args:
        current_iteration (int): The current iteration number (0-indexed).
        total_iterations (int): The total number of iterations.
        description (str, optional): A description of the task. Defaults to "".
        update_every_n_iterations (int, optional): How often to print an update. Defaults to 100.
        start_time (float, optional): The time (from time.time()) when the process started.
                                       Required for calculating IPS and estimated time. Defaults to None.
    """
    if current_iteration == 0 or \
       current_iteration == total_iterations - 1 or \
       (current_iteration + 1) % update_every_n_iterations == 0:

        percentage = (current_iteration + 1) / total_iterations * 100
        ips_info = ""
        eta_info = "" # Initialize ETA info

        if start_time is not None:
            elapsed_time = time.time() - start_time
            if elapsed_time > 0:
                ips = (current_iteration + 1) / elapsed_time
                ips_info = f", {ips:.2f} it/s"

                # Calculate Estimated Time of Completion (ETA)
                remaining_iterations = total_iterations - (current_iteration + 1)
                if ips > 0: # Avoid division by zero
                    time_remaining_seconds = remaining_iterations / ips
                    # Format time_remaining_seconds into a more readable format (e.g., HH:MM:SS)
                    eta_delta = timedelta(seconds=int(time_remaining_seconds))
                    eta_info = f", ETA: {str(eta_delta)}"

        progress_msg = (
            f"[NO_TIMESTAMP]{description}: "
            f"{current_iteration + 1}/{total_iterations} "
            f"({percentage:.1f}%)"
            f"{ips_info}"
            f"{eta_info}" # Add ETA info to the message
        )
        print(progress_msg, flush=True)

pd.options.mode.chained_assignment = None  # default='warn'
warnings.filterwarnings("ignore")
    

def fix_PEAKS(row): #fixes old PEAKS formatted protein-peptides files (K.{Sequence}.X)
    peptide = row['Peptide']
    if peptide[1] == '.': peptide = peptide[2:]
    if peptide[-2] == '.': peptide = peptide[:-2]
    row['Peptide'] = peptide
    return row


def sigmoid(x, B, A, Chalf, b):
    """ Fitting Equation
	- Fits data to sigmoid curve.
	- Returns y
	"""
    y = B + ((A - B) / (1 + np.exp((-1 / b) * (Chalf - x))))  ### ORIGINAL CHalf Program
    #y = A + ((B - A) / (1 + np.exp(-Chalf - x / b)))		### Copying paper...
    return y

def get_initial_sigmoid_guesses_robust(x_data, y_data, fraction_for_AB=0.2, min_slope_threshold=0.01):
    """
    Provides initial guesses for sigmoid curve fitting parameters (A, B, Chalf, b)

    Parameters:
    - x_data (array-like): The independent variable data.
    - y_data (array-like): The dependent variable data (0-1 normalized).
    - fraction_for_AB (float): Fraction of data points to use for A and B guesses.
    - min_slope_threshold (float): Minimum absolute difference between A and B to consider it a sigmoid.

    Returns:
    - tuple: (A_guess, B_guess, Chalf_guess, b_guess)
    """

    x_data = np.asarray(x_data)
    y_data = np.asarray(y_data)

    if len(x_data) < 3 or len(y_data) < 3:
        raise ValueError("Not enough data points for meaningful initial guesses (min 3 required).")

    # 1. Guess for A (Pre-transition) and B (Post-transition)
    n_points = len(y_data)
    num_start_points = max(1, int(n_points * fraction_for_AB))
    num_end_points = max(1, int(n_points * fraction_for_AB))

    A_guess = np.mean(y_data[:num_start_points])
    B_guess = np.mean(y_data[-num_end_points:])

    # Check if there's a significant transition (avoid flat data)
    if np.abs(A_guess - B_guess) < min_slope_threshold:
        # Data is likely flat or noisy without a clear sigmoid transition
        # Provide sensible default guesses for a flat line or very shallow sigmoid
        # Set A and B to the average, Chalf to midpoint of x, and b to a large value.
        avg_y = np.mean(y_data)
        A_guess = avg_y
        B_guess = avg_y
        Chalf_guess = np.mean(x_data)
        b_guess = (np.max(x_data) - np.min(x_data)) * 5 # Very large b for flat curve
        if b_guess == 0: b_guess = 1.0 # Ensure b is not zero if x_data is constant
        return A_guess, B_guess, Chalf_guess, b_guess

    # 2. Guess for Chalf (Transition Midpoint)
    # The midpoint y value between A and B
    y_mid = A_guess + (B_guess - A_guess) / 2

    # Find the index of the y value closest to y_mid
    idx_closest = np.argmin(np.abs(y_data - y_mid))
    Chalf_guess = x_data[idx_closest]

    # 3. Robust Guess for b (Steepness)
    # This uses the range of X values that correspond to a significant portion of the Y transition.
    # For a sigmoid, ~80% of the transition (from 0.1 to 0.9 of (B-A)) happens over a certain X-range.
    # We'll use this heuristic.

    # Determine thresholds for 10% and 90% of the Y range (between A and B)
    # Ensure order for consistent calculation, whether A < B or A > B
    y_min_bound = min(A_guess, B_guess)
    y_max_bound = max(A_guess, B_guess)

    y_threshold_10 = y_min_bound + 0.1 * (y_max_bound - y_min_bound)
    y_threshold_90 = y_min_bound + 0.9 * (y_max_bound - y_min_bound)

    # Find x values where y crosses these thresholds
    x_at_10_percent = None
    x_at_90_percent = None

    # Iterate through data to find the first x where y crosses the threshold
    # This assumes x_data is sorted, which is typically true for fitting.
    for i in range(len(y_data)):
        if x_at_10_percent is None and (
            (A_guess < B_guess and y_data[i] >= y_threshold_10) or
            (A_guess > B_guess and y_data[i] <= y_threshold_10)
        ):
            x_at_10_percent = x_data[i]

        if x_at_90_percent is None and (
            (A_guess < B_guess and y_data[i] >= y_threshold_90) or
            (A_guess > B_guess and y_data[i] <= y_threshold_90)
        ):
            x_at_90_percent = x_data[i]
            # Once 90% is found, we can break if we assume a monotonic trend
            # However, for robustness to small fluctuations, we might want to check the rest.
            # For initial guess, first crossings are usually fine.

    # Fallback if thresholds aren't crossed (e.g., incomplete data, very noisy)
    if x_at_10_percent is None:
        x_at_10_percent = x_data[0] # Use start of x range
    if x_at_90_percent is None:
        x_at_90_percent = x_data[-1] # Use end of x range

    # Calculate the effective x-range for the transition
    transition_x_range = np.abs(x_at_90_percent - x_at_10_percent)

    # Heuristic for b: Typically, the transition from 10% to 90% of the full scale
    # takes about 4 times the 'b' value for the exponential part.
    # So, b approx (transition_x_range) / 4.
    if transition_x_range > 0:
        b_guess = transition_x_range / 4.0
    else:
        # If transition_x_range is 0 (e.g., all points at same x, or very few unique x values),
        # or if the data is so flat that 10% and 90% are at the same x.
        # This implies a very steep curve or no transition.
        # Set b to a small positive value for a steep transition.
        b_guess = 0.05 * (np.max(x_data) - np.min(x_data)) # A small fraction of the total x-range
        if b_guess == 0: b_guess = 0.01 # Fallback if x_data is constant

    # Ensure b_guess is positive
    b_guess = abs(b_guess)
    if b_guess == 0: b_guess = 0.01 # Prevent division by zero in fitting

    return A_guess, B_guess, Chalf_guess, b_guess

def fitCHalf(x,y,numPoints,OUTLIER_CUTOFF,MINIMUM_PTS,A_guess=None,B_guess=None,Chalf_guess=None,b_guess=None,INITIAL_GUESS=False): #takes concentration values, abundance values and fits them to a curve. quality metrics of oulier cutoff and minimum number of points for a curve are specified by the user.
    if None in (A_guess, B_guess, Chalf_guess, b_guess): GUESS = False
    else: GUESS = True
    try:
        if GUESS: popt, pcov = curve_fit(sigmoid, x, y, maxfev=100000, p0=[A_guess, B_guess, Chalf_guess, b_guess])
        elif not GUESS: popt, pcov = curve_fit(sigmoid, x, y, maxfev=100000)
        # maxfev is number of fit tries, 1000 being standard; p0=[0, 0.5, 2, 0.2]
        stdError = np.sqrt(np.diag(pcov))  # stdError[ B-error, A-error, CHalf-error, b-error]
        B_stderror, A_stderror, CHalf_stderror, b_stderror = stdError[:]

        fitCurve_B, fitCurve_A, CHalf, fitCurve_b = popt[:]
        if fitCurve_B > fitCurve_A: slope = 'Positive'
        else: slope = 'Negative'
        CHalf_ConfidenceInterval = t.ppf(.975, (numPoints - 1)) * CHalf_stderror / np.sqrt(numPoints)
        CHalf_confidenceInterval_lowBound = CHalf - CHalf_ConfidenceInterval
        CHalf_confidenceInterval_upBound = CHalf + CHalf_ConfidenceInterval

        b_confidenceInterval = t.ppf(.975, (numPoints - 1)) * b_stderror / np.sqrt(numPoints)
        b_confidenceInterval_lowBound = fitCurve_b - b_confidenceInterval
        b_confidenceInterval_upBound = fitCurve_b + b_confidenceInterval

        ''' NOTE: This if/else block of code deals with negative vs. positive slope. A and B change on the
        y-axis, while CHalf changes on the x-axis. So we need to switch the sign on CHalf to get the correct
        confidence interval variables for a confidence interval curve. '''
        if fitCurve_B <= fitCurve_A:
            popt_lowBound = [fitCurve_B - (OUTLIER_CUTOFF * B_stderror),
					 fitCurve_A - (OUTLIER_CUTOFF * A_stderror),
					 CHalf - (OUTLIER_CUTOFF * CHalf_stderror),
					 fitCurve_b]
            popt_upBound = [fitCurve_B + (OUTLIER_CUTOFF * B_stderror),
					fitCurve_A + (OUTLIER_CUTOFF * A_stderror),
					CHalf + (OUTLIER_CUTOFF * CHalf_stderror),
					fitCurve_b]
        else:
            popt_lowBound = [fitCurve_B + (OUTLIER_CUTOFF * B_stderror),
					 fitCurve_A + (OUTLIER_CUTOFF * A_stderror),
					 CHalf - (OUTLIER_CUTOFF * CHalf_stderror),
					 fitCurve_b]
            popt_upBound = [fitCurve_B - (OUTLIER_CUTOFF * B_stderror),
					fitCurve_A - (OUTLIER_CUTOFF * A_stderror),
					CHalf + (OUTLIER_CUTOFF * CHalf_stderror),
					fitCurve_b]

        concRange = max(x) - min(x)
        ratioTOrange = CHalf_ConfidenceInterval / concRange
        
        """ r_squared calculations """
        residuals = y - sigmoid(x, *popt)
        ss_res = np.sum(residuals ** 2)
        ss_tot = np.sum(y - np.mean(y) ** 2)
        r_squared = 1 - (ss_res / ss_tot)
        CHalf_normalized = CHalf / concRange
        
        ''' OUTLIER TRIMMING ''' 
        if fitCurve_B <= fitCurve_A: #removes potential outliers and refits curves to limit effects of artifacts and holes in data
            mask = np.logical_and(np.array(y)>sigmoid(np.array(x),*popt_lowBound),np.array(y)<sigmoid(np.array(x),*popt_upBound))
        else:
            mask = np.logical_and(np.array(y)<sigmoid(np.array(x),*popt_lowBound),np.array(y)>sigmoid(np.array(x),*popt_upBound))
        trim_xValues = list(np.array(x)[mask])
        trim_yValues = list(np.array(y)[mask])
        trim_numPoints = len(trim_yValues)
        if trim_numPoints <= MINIMUM_PTS:
            return [slope,fitCurve_B,fitCurve_A,CHalf,fitCurve_b,B_stderror,A_stderror,CHalf_stderror,b_stderror,CHalf_ConfidenceInterval,ratioTOrange,CHalf_confidenceInterval_lowBound,CHalf_confidenceInterval_upBound,b_confidenceInterval,b_confidenceInterval_lowBound,b_confidenceInterval_upBound,r_squared,CHalf_normalized] + [np.nan]*18
        if INITIAL_GUESS:
            try: #Try to make inital guesses for curve fitting to avoid fitting incorrect local minima
                A_guess, B_guess, Chalf_guess, b_guess = get_initial_sigmoid_guesses_robust(trim_xValues, trim_yValues)
            except ValueError:
                A_guess, B_guess, Chalf_guess, b_guess = [None] * 4
        elif not INITIAL_GUESS: A_guess, B_guess, Chalf_guess, b_guess = [None] * 4
        if None in (A_guess, B_guess, Chalf_guess, b_guess): GUESS = False
        else: GUESS = True
        try:
            if GUESS: trim_popt, trim_pcov = curve_fit(sigmoid, trim_xValues, trim_yValues, maxfev=100000, p0=[A_guess, B_guess, Chalf_guess, b_guess])
            elif not GUESS: trim_popt, trim_pcov = curve_fit(sigmoid, trim_xValues, trim_yValues, maxfev=100000)
        except RuntimeError:
            return [np.nan]*37
        trim_stdError = np.sqrt(np.diag(trim_pcov))  # stdError[ B-error, A-error, CHalf-error, b-error]
        trim_B_stderror, trim_A_stderror, trim_CHalf_stderror, trim_b_stderror = trim_stdError[:]

        trim_B, trim_A, trim_CHalf, trim_b = trim_popt[:]
        if trim_B > trim_A:
            trim_slope = 'Positive'
        else: trim_slope = 'Negative'

        trim_CHalf_ConfidenceInterval = t.ppf(.975, (trim_numPoints - 1)) * trim_CHalf_stderror / np.sqrt(
                trim_numPoints)  ### Figure out where this .975 comes from... and whatever this line means and is doing...
        trim_CHalf_confidenceInterval_lowBound = trim_CHalf - trim_CHalf_ConfidenceInterval
        trim_CHalf_confidenceInterval_upBound = trim_CHalf + trim_CHalf_ConfidenceInterval

        trim_b_confidenceInterval = t.ppf(.975, (trim_numPoints - 1)) * trim_b_stderror / np.sqrt(trim_numPoints)
        trim_b_confidenceInterval_lowBound = trim_b - trim_b_confidenceInterval
        trim_b_confidenceInterval_upBound = trim_b + trim_b_confidenceInterval

        trim_concRange = max(trim_xValues) - min(trim_xValues)
        trim_ratioTOrange = trim_CHalf_ConfidenceInterval / trim_concRange

        """ r_squared calculations """
        trim_residuals = trim_yValues - sigmoid(trim_xValues, *trim_popt)
        trim_ss_res = np.sum(trim_residuals ** 2)
        trim_ss_tot = np.sum(trim_yValues - np.mean(trim_yValues) ** 2)
        trim_r_squared = 1 - (trim_ss_res / trim_ss_tot)
        trim_CHalf_normalized = trim_CHalf / trim_concRange

        return [slope,fitCurve_B,fitCurve_A,CHalf,fitCurve_b,B_stderror,A_stderror,CHalf_stderror,b_stderror,CHalf_ConfidenceInterval,ratioTOrange,CHalf_confidenceInterval_lowBound,CHalf_confidenceInterval_upBound,b_confidenceInterval,b_confidenceInterval_lowBound,b_confidenceInterval_upBound,r_squared,CHalf_normalized,trim_numPoints,trim_slope,trim_B,trim_A,trim_CHalf,trim_b,trim_B_stderror,trim_A_stderror,trim_CHalf_stderror,trim_b_stderror,trim_CHalf_ConfidenceInterval,trim_ratioTOrange,trim_CHalf_confidenceInterval_lowBound,trim_CHalf_confidenceInterval_upBound,trim_b_confidenceInterval,trim_b_confidenceInterval_lowBound,trim_b_confidenceInterval_upBound,trim_r_squared,trim_CHalf_normalized]
    except RuntimeError:
        return [np.nan]*37

def windowed_curves(input_list, window_size): #creates sets of windows for testing for secondary kinetic effects in curve fitting
  overlapping_sublists = []
  for i in range(len(input_list) - window_size + 1):
    overlapping_sublists.append(input_list[i:i + window_size])
  return overlapping_sublists

def qcCHalf(row,range_cutoff,rsq_cutoff):
    return row

def savgol_apply(row,conc_cols,window_length=5,polyorder=2,mode='nearest'):
    row[conc_cols] = savgol_filter(list(row[conc_cols]),window_length=window_length,polyorder=polyorder,mode='nearest')
    return row

def graph_curve(row,to_graph,concentrations,conc_cols,path,file_type='jpg'):
    plt.close()
    suptitle = row['Accession@Peptide']
    title = f'C½: {round(to_graph["CHalf"],4)} | R²: {round(to_graph["r_squared"],4)} | RTR: {round(to_graph["ratioTOrange"],4)}'
    curve_x = np.linspace(min(concentrations),max(concentrations),1000)
    curve_y = sigmoid(x=curve_x,A=to_graph['Baseline'],B=to_graph['Post-Transition'],Chalf=to_graph['CHalf'],b=to_graph['Curve_b'])
    sns.scatterplot(x=concentrations,y=row[conc_cols],label='Curve')
    plt.plot(curve_x,curve_y)
    plt.axvspan(to_graph['CHalf']-to_graph['CHalf_ConfidenceInterval'],to_graph['trim_CHalf']+to_graph['CHalf_ConfidenceInterval'],alpha=0.25,color='gray',label='CI')
    plt.axvline(x=to_graph['CHalf'],label='C½',color='red',linestyle='--')
    plt.legend()
    plt.xlabel('Concentration',fontsize=12,fontweight=600)
    plt.ylabel('Abundance',fontsize=12,fontweight=600)
    plt.suptitle(suptitle,fontsize=14,fontweight=600,y=0.95)
    plt.title(title,fontsize=12)
    name = row['Accession@Peptide'].replace('|','_').replace(':','_')
    plt.xlim(min(concentrations),max(concentrations))
    plt.tight_layout()
    plt.savefig(f'{path}/{name}.{file_type}',bbox_inches='tight')

def make_label_site_function(row,search): #calculates label site
    try:
        peptide = row['Peptide']
        modded = peptide
        if modded[0] == '(': #fix incorrectly notated N terminal modifications
            ind = modded.index(')') + 1
            aa = modded[ind]
            p2 = modded[ind+1:]
            modded = aa + p2
        start = row['Start']
        delimiters = ['(',')']
        for delimiter in delimiters:
            modded = ' '.join(modded.split(delimiter))
        modded = modded.split()
        mods = [modded[i] for i in range(len(modded)) if i % 2 == 1]
        unmodified = ''.join([modded[i][:-1] + modded[i][-1].lower() for i in range(len(modded)-1) if i % 2 == 0])
        sites = [i + start for i, a in enumerate(unmodified) if a.islower()]
        residues = [modded[i][-1] for i in range(len(modded)) if i % 2 == 0][:-1]
        to_remove = [] #removing instances of unsearched labels i.e. YMHC is search but Q(mod) is found
        for i, residue in enumerate(residues):
            if residue not in search: to_remove.append(i)
        if len(to_remove) > 0:
            to_remove.sort(reverse=True)
            for index in to_remove: residues.pop(index); sites.pop(index); mods.pop(index)
        ID = ''.join([f'{residues[i]}({mods[i]})@{sites[i]}_' for i in range(len(residues))])[:-1]
        ID = row['Accession'] + '|' + ID
        if len(sites) == 1 and len(residues) == 1 and len(mods) == 1:
            row['Site Type'] = 'Single Labeled'
            #sites = sites[0]
            residues = residues[0]
            mods = mods[0]
        elif len(sites) > 1 and len(residues)> 1 and len(mods) > 1:
            row['Site Type'] = 'Multi Labeled'
            row['Label Site'] = 'N/A'
            return row
        else:
            occurences = 0
            for res in search:
                occurences += len([m.start() for m in re.finditer(res, peptide)])
                if occurences > 1:
                    row['Site Type'] = 'Multi Unlabeled'
                    row['Label Site'] = 'N/A'
                    return row
            for res in search:
                site = peptide.find(res)
                if site != -1:
                    site += start
                    row['Label Site'] = f'{res}{int(site)}'
                    row['Site Type'] = 'Single Unlabeled'
                    row['Label Type'] = res
                    row['Residue Number'] = site
                    return row
                else:
                    pass
        if len(sites) == 0:
            row['Label Site'] = np.nan
            row['Residue Number'] = np.nan
            row['Label Type'] = np.nan
        else:
            row['Label Site'] = f'{residues}{int(sites[0])}'
            row['Residue Number'] = int(sites[0])
            row['Label Type'] = f'{residues}({mods})'
    except ValueError:
        row['Label Site'] = 'Error'
        row['Site Type'] = 'Error'
    return row

"""DEFAULTS
#conc dict represents the names of the abundance columns in your protein-peptides file and their associated concentrations
conc_dict = conc_dict=dict(zip(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],[0.0, 0.43, 0.87, 1.3, 1.74, 2.17, 2.61, 3.04, 3.48, 3.59]))
OUTLIER_CUTOFF = 2 #how many confidence intervals above the fitted curve before a point is considered an outlier
MINIMUM_PTS = 4 #minimum number of points that must be used before fitting is attempted
LIGHT_SEARCH = True #Only fit curves against peptides that have labelable residues, reduces computation time
search=['Y','M','C','H'] #Residues to fit for if using light search
WINDOW_FIT = False #if curves are to be broken down into component parts and fit in windows
nwindow = 6 #number of points to be considered in each window
SAVGOL_FIT = False #if raw abundances are to smoothed using a savgol filter
SAVGOL_WINDOW = 5
SAVGOL_ORDER = 2
range_cutoff = (0,3.48) #C1/2 value must be within this range to be significant
rsq_cutoff = 0.8 #r squared must be higher than this value to be significant
rtr_cutoff = 0.35 #ratio to range of confidence interval must be lower than this value to be significant, if HANDLE_CI_UNCERTAINY is true, significance will not be based on this value, but CI will be factored in when considering displaying data
highest_criteria = 'rsq' #which method to determine the best fit 'rsq' : maximizes r squared, 'ci' : minimizes confidence interval
HANDLE_CI_UNCERTAINTY = True #treats confidence intervals beyond the desired value as nan values to indicate uncertainty without relying on the confidence interval metric to cut out data as the confidence interval metric is not always useful for indicating whether or not a curve is a good fit and may miss real stability transitions, but CI can be useful for indicating how certain a calculation is; using this paramater allows you to keep real curves that may not have confidence intervals while still indicating that they lack a solid confidence interval when displaying data
CUSTOM_FASTA = False #handles annotating mutations that were inserted into your database during identification; your protein-peptides file should contain a column labeled 'Mutation' that will impact how curves are combined together during Chalf localization; mutated proteins' headers followed the format >PROTEIN_ID;refRNvar;start-end|ENTRY_NAME;refRNvar;start-end DESCRIPTION GN=GENE_NAME;refRNvar;start-end
KEEP_INSIGNIFICANT = True #keeps insignficant curves in final output of combined sites
concentrations = [0.0, 0.43, 0.87, 1.3, 1.74, 2.17, 2.61, 3.04, 3.48, 3.59] #tells combined sites what concentrations to fit for
zero_criteria = 'remove' #replaces zeros in abundances with nan; 'keep' keeps them and factors them in normalization; 'impute' does not factor them in for normalization but fills them back in after normalization
INITIAL_GUESS = True #attempts to do preprocessing to provide an informed initial guess for curve fitting to prevent fitting to local instead of global minima
"""

def CHalf(file,condition,outdir,conc_dict=dict(zip(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],[0.0, 0.43, 0.87, 1.3, 1.74, 2.17, 2.61, 3.04, 3.48, 3.59])),TRIM_OUTLIERS=True,OUTLIER_CUTOFF=2,MINIMUM_PTS=4,LIGHT_SEARCH=True,search=list('YMCH'),WINDOW_FIT=False,nwindow=6,SAVGOL_FIT=False,SAVGOL_WINDOW=5,SAVGOL_ORDER=2,range_cutoff=(0,3.48),rsq_cutoff=0.8,rtr_cutoff=0.35,highest_criteria='rsq',HANDLE_CI_UNCERTAINTY=True,CUSTOM_FASTA=False,zero_criteria='remove',INITIAL_GUESS=True,GRAPH=False,file_type='jpg',graph_min=0,graph_max=3.48,graph_rsq=0.8,graph_ci_filter=False,graph_ci_value=0.35,KEEP_INSIGNIFICANT=None):
    print(f'Reading {file}...')
    try:
        df = pd.read_csv(file)
    except FileNotFoundError:
        raise FileNotFoundError(f'{file} not found for {condition}. Skipping this condition...')
    path = f'{outdir}/{condition}'
    print(f'Creating output directory {path}')
    os.makedirs(path,exist_ok=True)
    if GRAPH:
        graph_path = f'{path}/Graphs'
        os.makedirs(graph_path,exist_ok=True)
    df.rename(columns={'Protein Accession':'Accession'},inplace=True)
    df.insert(0,'Accession@Peptide',df['Accession']+'@'+df['Peptide'])
    tmp_conc_dict = conc_dict
    conc_dict = {}
    for col in tmp_conc_dict: #keep only columns that apply
        if col in df.columns: conc_dict.update({col:tmp_conc_dict[col]})
    concentrations=list(conc_dict.values())
    conc_cols = list(conc_dict)
    
    print(f'Identifying label sites for residues {search}...')
    df = df.apply(make_label_site_function,search=search,axis=1) #Add label site information
    column_order = ['Accession@Peptide', 'Accession', 'Peptide', 'Site Type', 'Residue Number', 'Label Site', 'Label Type'] + conc_cols + ['Start', 'End']
    if CUSTOM_FASTA: column_order = ['Accession@Peptide', 'Accession', 'Peptide', 'Mutation', 'Site Type', 'Residue Number', 'Label Site', 'Label Type'] + conc_cols + ['Start', 'End']
    df = df[column_order] #reorder columns
    
    if LIGHT_SEARCH:
        df = df.dropna(subset=['Site Type']) #limit CHalf calculations to peptides with fittable residues, saves computational time and limits potential artifacts
    raw = df.copy()
    df['#pts'] = df[conc_cols].notna().sum(axis = 1) #count all abundance values that are not nan in concentration columns
    if SAVGOL_FIT:
        print('Applying Savitsky-golay curve smoothing...')
        df = df.apply(savgol_apply, conc_cols=conc_cols, window_length=SAVGOL_WINDOW, polyorder=SAVGOL_ORDER, axis=1)
        raw[conc_cols] = raw[conc_cols].apply(lambda x: (x-np.nanmin(x))/(np.nanmax(x)-np.nanmin(x)), axis=1)
    print('Normalizing intensities and calculating Spearman correlations...')
    df['Mean'] = df[conc_cols].mean(axis=1) #Mean of raw abundances
    df['RSD'] = df[conc_cols].std(axis=1) / df['Mean'] #RSD of raw abundances
    df['Range'] = df[conc_cols].max(axis=1) - df[conc_cols].min(axis=1) #Range of abundances max-min
    df['Relative Range'] = df['Range'] / df['Mean'] #Range of abundances divided by mean abundance
    df['% Change'] = df['Range'] / df[conc_cols].min(axis=1) #% Change from min to max abundance
    df['End-Start'] = df[conc_cols].apply(lambda x: x.dropna()[-1] - x.dropna()[0], axis=1) #last non nan point minus first non nan point 
    df['fit_#non Zero'] = 0
    if zero_criteria == 'remove':
        df[conc_cols] = df[conc_cols].replace(0, np.nan) #replace zero values with nan
        df[conc_cols] = df[conc_cols].apply(lambda x: (x-np.nanmin(x))/(np.nanmax(x)-np.nanmin(x)), axis=1) #min-max normalize abundances of each peptide
        df['fit_#non Zero'] = df[conc_cols].notna().sum(axis = 1)
    elif zero_criteria == 'keep':
        df[conc_cols] = df[conc_cols].apply(lambda x: (x-np.nanmin(x))/(np.nanmax(x)-np.nanmin(x)), axis=1) #min-max normalize abundances of each peptide
        df['fit_#non Zero'] = (df[conc_cols] != 0).sum(axis = 1)
    elif zero_criteria == 'impute':
        df[conc_cols] = df[conc_cols].replace(0, np.nan) #replace zero values with nan
        df[conc_cols] = df[conc_cols].apply(lambda x: (x-np.nanmin(x))/(np.nanmax(x)-np.nanmin(x)), axis=1) #min-max normalize abundances of each peptide
        df[conc_cols] = df[conc_cols].fillna(0) #replace nan values with 0
        df['fit_#non Zero'] = (df[conc_cols] != 0).sum(axis = 1)
    df[['Spearman','P-value']] = df[conc_cols].apply(lambda x: (spearmanr(x,concentrations)[0],spearmanr(x,concentrations)[1]),axis=1).apply(pd.Series)

    #df[conc_cols] = df[conc_cols].fillna(0)
    
    if highest_criteria == 'rsq': None
    elif highest_criteria == 'ci': None
    else: print('Fitting metric not recognized, defaulting to r squared maximization')
    
    data = pd.DataFrame()
    total_rows = df.shape[0]
    process_start_time = time.time()
    print('Fitting curves...')
    count_p = 0
    for index, row in df.iterrows():
        progress_logger(
            count_p,
            total_rows,
            description="CHalf Curve Fitting",
            update_every_n_iterations=total_rows//20, # Adjust for your needs
            start_time=process_start_time
        )
        count_p += 1
        columns = ['fit_#non Zero','fit_slope','fit_Curve_B','fit_Curve_A','fit_CHalf', 'fit_Curve_b', 'fit_B_stderror', 'fit_A_stderror', 'fit_CHalf_stderror','fit_b_stderror', 'fit_CHalf_ConfidenceInterval', 'fit_ratioTOrange','fit_CHalf_confidenceInterval_lowBound', 'fit_CHalf_confidenceInterval_upBound','fit_b_confidenceInterval', 'fit_b_confidenceInterval_lowBound','fit_b_confidenceInterval_upBound', 'fit_r_squared', 'fit_CHalf_normalized','trim_#pts', 'trim_slope', 'trim_B', 'trim_A', 'trim_CHalf', 'trim_b','trim_B_stderror', 'trim_A_stderror', 'trim_CHalf_stderror','trim_b_stderror', 'trim_CHalf_ConfidenceInterval', 'trim_ratioTOrange','trim_CHalf_confidenceInterval_lowBound','trim_CHalf_confidenceInterval_upBound', 'trim_b_confidenceInterval','trim_b_confidenceInterval_lowBound','trim_b_confidenceInterval_upBound', 'trim_r_squared','trim_CHalf_normalized']
        attempts = pd.DataFrame(columns=columns+['Window'])
        y = row[conc_cols].dropna()
        x = [conc_dict[conc] for conc in y.index]
        numPoints = len(y)
        count = row['fit_#non Zero']
        if count <= MINIMUM_PTS or np.isnan(count):
            continue
        window = f'{min(x)}-{max(x)}'
        if INITIAL_GUESS:
            try: #Try to make inital guesses for curve fitting to avoid fitting incorrect local minima
                A_guess, B_guess, Chalf_guess, b_guess = get_initial_sigmoid_guesses_robust(x, y)
            except ValueError:
                A_guess, B_guess, Chalf_guess, b_guess = [None] * 4
        elif not INITIAL_GUESS: A_guess, B_guess, Chalf_guess, b_guess = [None] * 4
        attempt = fitCHalf(x, y, numPoints, OUTLIER_CUTOFF, MINIMUM_PTS, A_guess=A_guess, B_guess=B_guess, Chalf_guess=Chalf_guess, b_guess=b_guess, INITIAL_GUESS=INITIAL_GUESS)
        attempt = dict(zip(columns,[[numPoints]]+[[entry] for entry in attempt]))
        attempt.update({'Window':[window]})
        attempt = pd.DataFrame(attempt)
        to_qc = attempt.loc[0]
        to_qc['Spearman P'] = row['P-value']
        to_qc['Spearman'] = row['Spearman']
        #Pick the better of the fits based on the preferred fitting metric (r squared maximization or confidence interval minimization)
        if TRIM_OUTLIERS:
            if highest_criteria == 'rsq':
                if to_qc['fit_r_squared'] >= to_qc['trim_r_squared'] or np.isnan(to_qc['trim_r_squared']): attempt['CHalf'] = to_qc['fit_CHalf']; attempt['r_squared'] = to_qc['fit_r_squared']; attempt['ratioTOrange'] = to_qc['fit_ratioTOrange']; attempt['CHalf_ConfidenceInterval'] = to_qc['fit_CHalf_ConfidenceInterval']; attempt['Slope'] = to_qc['fit_slope']; to_qc['Slope'] = to_qc['fit_slope']; attempt['Curve_b'] = to_qc['fit_Curve_b']; to_qc['Curve_b'] = to_qc['fit_Curve_b']; attempt['Baseline'] = to_qc['fit_Curve_A']; to_qc['Baseline'] = to_qc['fit_Curve_A']; attempt['Post-Transition'] = to_qc['fit_Curve_B']; to_qc['Post-Transition'] = to_qc['fit_Curve_B']; attempt['Trimmed'] = False
                else: attempt['CHalf'] = to_qc['trim_CHalf']; attempt['r_squared'] = to_qc['trim_r_squared']; attempt['ratioTOrange'] = to_qc['trim_ratioTOrange']; attempt['CHalf_ConfidenceInterval'] = to_qc['trim_CHalf_ConfidenceInterval']; attempt['Slope'] = to_qc['trim_slope']; to_qc['Slope'] = to_qc['trim_slope']; attempt['Curve_b'] = to_qc['trim_b']; to_qc['Curve_b'] = to_qc['trim_b']; attempt['Baseline'] = to_qc['trim_A']; to_qc['Baseline'] = to_qc['trim_A']; attempt['Post-Transition'] = to_qc['trim_B']; to_qc['Post-Transition'] = to_qc['trim_B']; attempt['Trimmed'] = True
            elif highest_criteria == 'ci':
                if to_qc['fit_ratioTOrange'] <= to_qc['trim_ratioTOrange'] or np.isnan(to_qc['trim_ratioTOrange']): attempt['CHalf'] = to_qc['fit_CHalf']; attempt['r_squared'] = to_qc['fit_r_squared']; attempt['ratioTOrange'] = to_qc['fit_ratioTOrange']; attempt['CHalf_ConfidenceInterval'] = to_qc['fit_CHalf_ConfidenceInterval']; attempt['Slope'] = to_qc['fit_slope']; to_qc['Slope'] = to_qc['fit_slope']; attempt['Curve_b'] = to_qc['fit_Curve_b']; to_qc['Curve_b'] = to_qc['fit_Curve_b']; attempt['Baseline'] = to_qc['fit_Curve_A']; to_qc['Baseline'] = to_qc['fit_Curve_A']; attempt['Post-Transition'] = to_qc['fit_Curve_B']; to_qc['Post-Transition'] = to_qc['fit_Curve_B']; attempt['Trimmed'] = False
                else: attempt['CHalf'] = to_qc['trim_CHalf']; attempt['r_squared'] = to_qc['trim_r_squared']; attempt['ratioTOrange'] = to_qc['trim_ratioTOrange']; attempt['CHalf_ConfidenceInterval'] = to_qc['trim_CHalf_ConfidenceInterval']; attempt['Slope'] = to_qc['trim_slope']; to_qc['Slope'] = to_qc['trim_slope']; attempt['Curve_b'] = to_qc['trim_b']; to_qc['Curve_b'] = to_qc['trim_b']; attempt['Baseline'] = to_qc['trim_A']; to_qc['Baseline'] = to_qc['trim_A']; attempt['Post-Transition'] = to_qc['trim_B']; to_qc['Post-Transition'] = to_qc['trim_B']; attempt['Trimmed'] = True
            else: #default to rsq if failed
                if to_qc['fit_r_squared'] >= to_qc['trim_r_squared'] or np.isnan(to_qc['trim_r_squared']): attempt['CHalf'] = to_qc['fit_CHalf']; attempt['r_squared'] = to_qc['fit_r_squared']; attempt['ratioTOrange'] = to_qc['fit_ratioTOrange']; attempt['CHalf_ConfidenceInterval'] = to_qc['fit_CHalf_ConfidenceInterval']; attempt['Slope'] = to_qc['fit_slope']; to_qc['Slope'] = to_qc['fit_slope']; attempt['Curve_b'] = to_qc['fit_Curve_b']; to_qc['Curve_b'] = to_qc['fit_Curve_b']; attempt['Baseline'] = to_qc['fit_Curve_A']; to_qc['Baseline'] = to_qc['fit_Curve_A']; attempt['Post-Transition'] = to_qc['fit_Curve_B']; to_qc['Post-Transition'] = to_qc['fit_Curve_B']; attempt['Trimmed'] = False
                else: attempt['CHalf'] = to_qc['trim_CHalf']; attempt['r_squared'] = to_qc['trim_r_squared']; attempt['ratioTOrange'] = to_qc['trim_ratioTOrange']; attempt['CHalf_ConfidenceInterval'] = to_qc['trim_CHalf_ConfidenceInterval']; attempt['Slope'] = to_qc['trim_slope']; to_qc['Slope'] = to_qc['trim_slope']; attempt['Curve_b'] = to_qc['trim_b']; to_qc['Curve_b'] = to_qc['trim_b']; attempt['Baseline'] = to_qc['trim_A']; to_qc['Baseline'] = to_qc['trim_A']; attempt['Post-Transition'] = to_qc['trim_B']; to_qc['Post-Transition'] = to_qc['trim_B']; attempt['Trimmed'] = True
        else:
            if highest_criteria == 'rsq':
                attempt['CHalf'] = to_qc['fit_CHalf']; attempt['r_squared'] = to_qc['fit_r_squared']; attempt['ratioTOrange'] = to_qc['fit_ratioTOrange']; attempt['CHalf_ConfidenceInterval'] = to_qc['fit_CHalf_ConfidenceInterval']; attempt['Slope'] = to_qc['fit_slope']; to_qc['Slope'] = to_qc['fit_slope']; attempt['Curve_b'] = to_qc['fit_Curve_b']; to_qc['Curve_b'] = to_qc['fit_Curve_b']; attempt['Baseline'] = to_qc['fit_Curve_A']; to_qc['Baseline'] = to_qc['fit_Curve_A']; attempt['Post-Transition'] = to_qc['fit_Curve_B']; to_qc['Post-Transition'] = to_qc['fit_Curve_B']; attempt['Trimmed'] = False
            elif highest_criteria == 'ci':
                attempt['CHalf'] = to_qc['fit_CHalf']; attempt['r_squared'] = to_qc['fit_r_squared']; attempt['ratioTOrange'] = to_qc['fit_ratioTOrange']; attempt['CHalf_ConfidenceInterval'] = to_qc['fit_CHalf_ConfidenceInterval']; attempt['Slope'] = to_qc['fit_slope']; to_qc['Slope'] = to_qc['fit_slope']; attempt['Curve_b'] = to_qc['fit_Curve_b']; to_qc['Curve_b'] = to_qc['fit_Curve_b']; attempt['Baseline'] = to_qc['fit_Curve_A']; to_qc['Baseline'] = to_qc['fit_Curve_A']; attempt['Post-Transition'] = to_qc['fit_Curve_B']; to_qc['Post-Transition'] = to_qc['fit_Curve_B']; attempt['Trimmed'] = False
            else: #default to rsq if failed
                attempt['CHalf'] = to_qc['fit_CHalf']; attempt['r_squared'] = to_qc['fit_r_squared']; attempt['ratioTOrange'] = to_qc['fit_ratioTOrange']; attempt['CHalf_ConfidenceInterval'] = to_qc['fit_CHalf_ConfidenceInterval']; attempt['Slope'] = to_qc['fit_slope']; to_qc['Slope'] = to_qc['fit_slope']; attempt['Curve_b'] = to_qc['fit_Curve_b']; to_qc['Curve_b'] = to_qc['fit_Curve_b']; attempt['Baseline'] = to_qc['fit_Curve_A']; to_qc['Baseline'] = to_qc['fit_Curve_A']; attempt['Post-Transition'] = to_qc['fit_Curve_B']; to_qc['Post-Transition'] = to_qc['fit_Curve_B']; attempt['Trimmed'] = False
        range_qc = range_cutoff[0] <= attempt.loc[0]['CHalf'] <= range_cutoff[1]
        rsq_qc = attempt.loc[0]['r_squared'] >= rsq_cutoff
        if HANDLE_CI_UNCERTAINTY:
            if attempt.loc[0]['ratioTOrange'] > rtr_cutoff:
                #attempt['ratioTOrange'] = np.nan #indicates uncertainty without creating plotting problems; CI often is not a good metric of how well a curve fits real stability transitions but can be useful for indicating how certain a calculation is; using this paramater allows you to keep real curves that may not have confidence intervals while still indicating that they lack a solid confidence interval when displaying data
                #attempt['CHalf_ConfidenceInterval'] = np.nan
                rtr_qc = True
            else: rtr_qc = attempt.loc[0]['ratioTOrange'] <= rtr_cutoff
        else:
            rtr_qc = attempt.loc[0]['ratioTOrange'] <= rtr_cutoff
        spear_qc = to_qc['Spearman P'] <= 0.05 #if there is a significant trend in abundance change, helps catch curves with multiple inflection points due to kinetic or thermodynamic effects
        #and (slope_qc * to_qc['Spearman'] > 0) optional argument for testing curve direction
        if WINDOW_FIT:
            qc_state = range_qc and rsq_qc and spear_qc and rtr_qc
        else:
            qc_state = range_qc and rsq_qc and rtr_qc
        if not qc_state:
            attempt['Significant'] = range_qc and rsq_qc and rtr_qc
            attempts = attempts._append(attempt)
            if WINDOW_FIT and not spear_qc:
                windows = windowed_curves(row[conc_cols], nwindow) #create smaller windowed curves to identify potential real curves lost due to secondary kinetic effects
                windowed_concentrations = windowed_curves(concentrations, nwindow)
                for i in range(len(windows)): #fit each window and take the best fit of them if any of them are significant
                    y = windows[i]
                    x = windowed_concentrations[i]
                    y = y.dropna()
                    x = [conc_dict[conc] for conc in y.index]
                    numPoints = (y != 0).sum()
                    if numPoints <= MINIMUM_PTS: continue
                    window = f'{min(x)}-{max(x)}'
                    #print(index,row[conc_cols],window,y)
                    attempt = fitCHalf(x, y, numPoints, OUTLIER_CUTOFF, MINIMUM_PTS)
                    attempt = dict(zip(columns,[[numPoints]]+[[entry] for entry in attempt]))
                    attempt.update({'Window':[window]})
                    attempt = pd.DataFrame(attempt)
                    to_qc = attempt.loc[0]
                    if to_qc['fit_r_squared'] >= to_qc['trim_r_squared'] or np.isnan(to_qc['trim_r_squared']): attempt['CHalf'] = to_qc['fit_CHalf']; attempt['r_squared'] = to_qc['fit_r_squared']; attempt['ratioTOrange'] = to_qc['fit_ratioTOrange']; attempt['CHalf_ConfidenceInterval'] = to_qc['fit_CHalf_ConfidenceInterval']; attempt['Slope'] = to_qc['fit_slope']; to_qc['Slope'] = to_qc['fit_slope']; attempt['Curve_b'] = to_qc['fit_Curve_b']; to_qc['Curve_b'] = to_qc['fit_Curve_b']; attempt['Baseline'] = to_qc['fit_Curve_A']; to_qc['Baseline'] = to_qc['fit_Curve_A']; attempt['Post-Transition'] = to_qc['fit_Curve_B']; to_qc['Post-Transition'] = to_qc['fit_Curve_B']; attempt['Trimmed'] = False
                    else: attempt['CHalf'] = to_qc['trim_CHalf']; attempt['r_squared'] = to_qc['trim_r_squared']; attempt['ratioTOrange'] = to_qc['trim_ratioTOrange']; attempt['CHalf_ConfidenceInterval'] = to_qc['trim_CHalf_ConfidenceInterval']; attempt['Slope'] = to_qc['trim_slope']; to_qc['Slope'] = to_qc['trim_slope']; attempt['Curve_b'] = to_qc['trim_b']; to_qc['Curve_b'] = to_qc['trim_b']; attempt['Baseline'] = to_qc['trim_A']; to_qc['Baseline'] = to_qc['trim_A']; attempt['Post-Transition'] = to_qc['trim_B']; to_qc['Post-Transition'] = to_qc['trim_B']; attempt['Trimmed'] = True
                    window_range_qc = max([min(x),range_cutoff[0]]) <= attempt.loc[0]['CHalf'] <= min([max(x),range_cutoff[1]])
                    window_rsq_qc = attempt.loc[0]['r_squared'] >= rsq_cutoff
                    
                    if HANDLE_CI_UNCERTAINTY:
                        if attempt.loc[0]['ratioTOrange'] >= rtr_cutoff:
                            window_rtr_qc = True
                        else: window_rtr_qc = attempt.loc[0]['ratioTOrange'] <= rtr_cutoff
                    else:
                        window_rtr_qc = attempt.loc[0]['ratioTOrange'] <= rtr_cutoff
                    window_qc_state = window_range_qc and window_rsq_qc and window_rtr_qc
                    if window_qc_state:
                        attempt['Significant'] = True
                        attempts = attempts._append(attempt,ignore_index=True)
                #print(attempt.columns)
                #print(attempts[list(conc_dict.values())+['fit_#non Zero','Window']])
            if highest_criteria == 'rsq': attempts = attempts.sort_values(by='r_squared',ascending=False).reset_index(drop=True)
            elif highest_criteria == 'ci': attempts = attempts.sort_values(by='CHalf_ConfidenceInterval',ascending=True).reset_index(drop=True)
            else: #default to rsq if failed
                attempts = attempts.sort_values(by='r_squared',ascending=False).reset_index(drop=True)
            to_append = attempts.loc[0]
            if np.isnan(to_append['CHalf']): to_append['Window'] = np.nan #removing fake windows for when curve fitting fails in each window
            if GRAPH:
                try:
                    to_graph = attempt.head(1)
                    to_graph = to_graph.loc[to_graph.index[0]]
                    to_graph['Accession@Peptide'] = row['Accession@Peptide']
                    graph_concentrations = [conc_dict[col] for col in conc_cols]
                    if graph_min < to_graph['CHalf'] < graph_max:
                        if graph_rsq < to_graph['r_squared']:
                            if not(graph_ci_filter) or graph_ci_value >= to_graph['ratioTOrange']:
                                graph_curve(row=row,to_graph=to_graph, concentrations=graph_concentrations, conc_cols=conc_cols, path=graph_path, file_type=file_type)
                except Exception as e:
                        print(f'Skipping graph. Error: {e}')
                        traceback.print_exc()
            data = data._append(to_append.rename(index))
        else:
            attempt['Significant'] = True
            if GRAPH:
                try:
                    to_graph = attempt.head(1)
                    to_graph = to_graph.loc[to_graph.index[0]]
                    to_graph['Accession@Peptide'] = row['Accession@Peptide']
                    graph_concentrations = [conc_dict[col] for col in conc_cols]
                    #print(to_graph, row)
                    if graph_min < to_graph['CHalf'] < graph_max:
                        if graph_rsq < to_graph['r_squared']:
                            if not(graph_ci_filter) or graph_ci_value >= to_graph['ratioTOrange']:
                                graph_curve(row=row,to_graph=to_graph, concentrations=graph_concentrations, conc_cols=conc_cols, path=graph_path, file_type=file_type)
                except Exception as e:
                    print(f'Skipping graph. Error: {row} {to_graph} {e}')
                    traceback.print_exc()
            data = data._append(attempt.loc[0].rename(index))
    
    data.reset_index(inplace=True)
    try:
        data = data.drop(columns=['fit_#non Zero'])
    except:
        None
    df.reset_index(inplace=True)        
    conDF = df.merge(data,how='left',on='index')
    conDF['Significant'] = conDF['Significant'].fillna(False)
    conDF.rename(columns=conc_dict,inplace=True)
    conDF.drop(columns=['index'],inplace=True)
    conDF['Site Type'] = conDF['Site Type'].fillna('Unlabelable')
    if HANDLE_CI_UNCERTAINTY: conDF['CHalf_ConfidenceInterval'] = conDF['CHalf_ConfidenceInterval'].fillna(np.inf).mask(conDF['CHalf_ConfidenceInterval']>rtr_cutoff,np.nan)
    sitesDF = conDF[conDF['Significant']] #only take significant curves
    sitesDF = sitesDF[sitesDF['Site Type'].str.contains('Single')] #only take curves where stability can be localized
    if CUSTOM_FASTA:
        mut_vector = sitesDF['Mutation'].apply(lambda x: f'_{x}' if type(x) == str else '')#('_' + sitesDF['Mutation']).fillna('')
        sitesDF.insert(0,'Label@Accession',sitesDF['Label Type'] + '_' + sitesDF['Label Site'] + '_' + sitesDF['Accession'] + mut_vector)
        sitesDF = sitesDF[['Label@Accession','Accession','Peptide','Mutation','Site Type','Label Site','Label Type','Residue Number','CHalf','r_squared','ratioTOrange','CHalf_ConfidenceInterval','Slope','Curve_b','Baseline','Post-Transition','Significant']+concentrations]
    else: 
        sitesDF.insert(0,'Label@Accession',sitesDF['Label Type'] + '_' + sitesDF['Label Site'] + '_' + sitesDF['Accession'])
        sitesDF = sitesDF[['Label@Accession','Accession','Peptide','Site Type','Label Site','Label Type','Residue Number','CHalf','r_squared','ratioTOrange','CHalf_ConfidenceInterval','Slope','Curve_b','Baseline','Post-Transition','Significant']+concentrations]
    sitesDF = sitesDF.sort_values(by=['Accession','Residue Number'])
    conDF = conDF.sort_values(by=['Accession','Residue Number'])
    conDF = conDF[['Accession@Peptide', 'Accession', 'Peptide', 'Site Type',
           'Residue Number', 'Label Site', 'Label Type','CHalf', 'r_squared', 'ratioTOrange',
           'CHalf_ConfidenceInterval', 'Slope', 'Curve_b', 'Baseline',
           'Post-Transition', 'Trimmed', 'Significant','Window']+list(conc_dict.values())+['Start', 'End',
           '#pts', 'Mean', 'RSD', 'Range', 'Relative Range', '% Change',
           'End-Start', 'fit_#non Zero', 'Spearman', 'P-value', 'fit_slope',
           'fit_Curve_B', 'fit_Curve_A', 'fit_CHalf', 'fit_Curve_b',
           'fit_B_stderror', 'fit_A_stderror', 'fit_CHalf_stderror',
           'fit_b_stderror', 'fit_CHalf_ConfidenceInterval', 'fit_ratioTOrange',
           'fit_CHalf_confidenceInterval_lowBound',
           'fit_CHalf_confidenceInterval_upBound', 'fit_b_confidenceInterval',
           'fit_b_confidenceInterval_lowBound', 'fit_b_confidenceInterval_upBound',
           'fit_r_squared', 'fit_CHalf_normalized', 'trim_#pts', 'trim_slope',
           'trim_B', 'trim_A', 'trim_CHalf', 'trim_b', 'trim_B_stderror',
           'trim_A_stderror', 'trim_CHalf_stderror', 'trim_b_stderror',
           'trim_CHalf_ConfidenceInterval', 'trim_ratioTOrange',
           'trim_CHalf_confidenceInterval_lowBound',
           'trim_CHalf_confidenceInterval_upBound', 'trim_b_confidenceInterval',
           'trim_b_confidenceInterval_lowBound',
           'trim_b_confidenceInterval_upBound', 'trim_r_squared',
           'trim_CHalf_normalized']]
    conDF.to_csv(f'{path}/{condition}_Combined_OUTPUT.csv',index=False)
    sitesDF.to_csv(f'{path}/{condition} Sites.csv',index=False)
    concentrations = conc_dict.values()
    return conDF, sitesDF, concentrations

def CombinedSites(sitesDF, condition, outdir, concentrations=[0.0, 0.43, 0.87, 1.3, 1.74, 2.17, 2.61, 3.04, 3.48, 3.59],TRIM_OUTLIERS=True,OUTLIER_CUTOFF=2,MINIMUM_PTS=4,range_cutoff=(0,3.48),rsq_cutoff=0.8,rtr_cutoff=0.35,highest_criteria='rsq',HANDLE_CI_UNCERTAINTY=True,KEEP_INSIGNIFICANT=True,CUSTOM_FASTA=False,INITIAL_GUESS=True,LIGHT_SEARCH=None,search=None,WINDOW_FIT=None,nwindow=None,SAVGOL_FIT=None,SAVGOL_WINDOW=None,SAVGOL_ORDER=None,GRAPH=None,file_type=None,graph_min=None,graph_max=None,graph_rsq=None,graph_ci_filter=None,graph_ci_value=None,zero_criteria=None):
    csDF = pd.DataFrame()
    print('Localizing stability values...')
    groups = sitesDF.groupby(by='Label@Accession')
    total_rows = len(groups)
    count_p = 0
    process_start_time = time.time()
    for label, group in groups:
        progress_logger(
            count_p,
            total_rows,
            description="Combined Sites Fittting",
            update_every_n_iterations=total_rows//10, # Adjust for your needs
            start_time=process_start_time
        )
        count_p += 1
        if len(group) > 1:
            x = []
            y = []
            peptides = []
            sites = []
            for index, row in group.iterrows():
                row_data = row[concentrations].dropna()
                x += list(row_data.index)#concentrations
                y += list(row_data)#list(row[concentrations])
                peptides.append(row['Peptide'])
                sites.append(row['Site Type'])
            columns = ['fit_#non Zero','fit_slope','fit_Curve_B','fit_Curve_A','fit_CHalf', 'fit_Curve_b', 'fit_B_stderror', 'fit_A_stderror', 'fit_CHalf_stderror','fit_b_stderror', 'fit_CHalf_ConfidenceInterval', 'fit_ratioTOrange','fit_CHalf_confidenceInterval_lowBound', 'fit_CHalf_confidenceInterval_upBound','fit_b_confidenceInterval', 'fit_b_confidenceInterval_lowBound','fit_b_confidenceInterval_upBound', 'fit_r_squared', 'fit_CHalf_normalized','trim_#pts', 'trim_slope', 'trim_B', 'trim_A', 'trim_CHalf', 'trim_b','trim_B_stderror', 'trim_A_stderror', 'trim_CHalf_stderror','trim_b_stderror', 'trim_CHalf_ConfidenceInterval', 'trim_ratioTOrange','trim_CHalf_confidenceInterval_lowBound','trim_CHalf_confidenceInterval_upBound', 'trim_b_confidenceInterval','trim_b_confidenceInterval_lowBound','trim_b_confidenceInterval_upBound', 'trim_r_squared','trim_CHalf_normalized']
            numPoints = len(row_data)
            if numPoints <= MINIMUM_PTS:
                continue
            if INITIAL_GUESS:
                try: #Try to make inital guesses for curve fitting to avoid fitting incorrect local minima
                    A_guess, B_guess, Chalf_guess, b_guess = get_initial_sigmoid_guesses_robust(x, y)
                except ValueError:
                    A_guess, B_guess, Chalf_guess, b_guess = [None] * 4
            elif not INITIAL_GUESS: A_guess, B_guess, Chalf_guess, b_guess = [None] * 4
            attempt = fitCHalf(x, y, numPoints, OUTLIER_CUTOFF, MINIMUM_PTS, A_guess=A_guess, B_guess=B_guess, Chalf_guess=Chalf_guess, b_guess=b_guess, INITIAL_GUESS=INITIAL_GUESS)
            attempt = dict(zip(columns,[[numPoints]]+[[entry] for entry in attempt]))
            attempt = pd.DataFrame(attempt)
            to_qc = attempt.loc[0]
            #Pick the better of the fits based on the preferred fitting metric (r squared maximization or confidence interval minimization)
            if TRIM_OUTLIERS:
                if highest_criteria == 'rsq':
                    if to_qc['fit_r_squared'] >= to_qc['trim_r_squared'] or np.isnan(to_qc['trim_r_squared']): attempt['CHalf'] = to_qc['fit_CHalf']; attempt['r_squared'] = to_qc['fit_r_squared']; attempt['ratioTOrange'] = to_qc['fit_ratioTOrange']; attempt['CHalf_ConfidenceInterval'] = to_qc['fit_CHalf_ConfidenceInterval']; attempt['Slope'] = to_qc['fit_slope']; to_qc['Slope'] = to_qc['fit_slope']; attempt['Curve_b'] = to_qc['fit_Curve_b']; to_qc['Curve_b'] = to_qc['fit_Curve_b']; attempt['Baseline'] = to_qc['fit_Curve_A']; to_qc['Baseline'] = to_qc['fit_Curve_A']; attempt['Post-Transition'] = to_qc['fit_Curve_B']; to_qc['Post-Transition'] = to_qc['fit_Curve_B']; attempt['Trimmed'] = False
                    else: attempt['CHalf'] = to_qc['trim_CHalf']; attempt['r_squared'] = to_qc['trim_r_squared']; attempt['ratioTOrange'] = to_qc['trim_ratioTOrange']; attempt['CHalf_ConfidenceInterval'] = to_qc['trim_CHalf_ConfidenceInterval']; attempt['Slope'] = to_qc['trim_slope']; to_qc['Slope'] = to_qc['trim_slope']; attempt['Curve_b'] = to_qc['trim_b']; to_qc['Curve_b'] = to_qc['trim_b']; attempt['Baseline'] = to_qc['trim_A']; to_qc['Baseline'] = to_qc['trim_A']; attempt['Post-Transition'] = to_qc['trim_B']; to_qc['Post-Transition'] = to_qc['trim_B']; attempt['Trimmed'] = True
                elif highest_criteria == 'ci':
                    if to_qc['fit_ratioTOrange'] <= to_qc['trim_ratioTOrange'] or np.isnan(to_qc['trim_ratioTOrange']): attempt['CHalf'] = to_qc['fit_CHalf']; attempt['r_squared'] = to_qc['fit_r_squared']; attempt['ratioTOrange'] = to_qc['fit_ratioTOrange']; attempt['CHalf_ConfidenceInterval'] = to_qc['fit_CHalf_ConfidenceInterval']; attempt['Slope'] = to_qc['fit_slope']; to_qc['Slope'] = to_qc['fit_slope']; attempt['Curve_b'] = to_qc['fit_Curve_b']; to_qc['Curve_b'] = to_qc['fit_Curve_b']; attempt['Baseline'] = to_qc['fit_Curve_A']; to_qc['Baseline'] = to_qc['fit_Curve_A']; attempt['Post-Transition'] = to_qc['fit_Curve_B']; to_qc['Post-Transition'] = to_qc['fit_Curve_B']; attempt['Trimmed'] = False
                    else: attempt['CHalf'] = to_qc['trim_CHalf']; attempt['r_squared'] = to_qc['trim_r_squared']; attempt['ratioTOrange'] = to_qc['trim_ratioTOrange']; attempt['CHalf_ConfidenceInterval'] = to_qc['trim_CHalf_ConfidenceInterval']; attempt['Slope'] = to_qc['trim_slope']; to_qc['Slope'] = to_qc['trim_slope']; attempt['Curve_b'] = to_qc['trim_b']; to_qc['Curve_b'] = to_qc['trim_b']; attempt['Baseline'] = to_qc['trim_A']; to_qc['Baseline'] = to_qc['trim_A']; attempt['Post-Transition'] = to_qc['trim_B']; to_qc['Post-Transition'] = to_qc['trim_B']; attempt['Trimmed'] = True
                else: #default to rsq if failed
                    if to_qc['fit_r_squared'] >= to_qc['trim_r_squared'] or np.isnan(to_qc['trim_r_squared']): attempt['CHalf'] = to_qc['fit_CHalf']; attempt['r_squared'] = to_qc['fit_r_squared']; attempt['ratioTOrange'] = to_qc['fit_ratioTOrange']; attempt['CHalf_ConfidenceInterval'] = to_qc['fit_CHalf_ConfidenceInterval']; attempt['Slope'] = to_qc['fit_slope']; to_qc['Slope'] = to_qc['fit_slope']; attempt['Curve_b'] = to_qc['fit_Curve_b']; to_qc['Curve_b'] = to_qc['fit_Curve_b']; attempt['Baseline'] = to_qc['fit_Curve_A']; to_qc['Baseline'] = to_qc['fit_Curve_A']; attempt['Post-Transition'] = to_qc['fit_Curve_B']; to_qc['Post-Transition'] = to_qc['fit_Curve_B']; attempt['Trimmed'] = False
                    else: attempt['CHalf'] = to_qc['trim_CHalf']; attempt['r_squared'] = to_qc['trim_r_squared']; attempt['ratioTOrange'] = to_qc['trim_ratioTOrange']; attempt['CHalf_ConfidenceInterval'] = to_qc['trim_CHalf_ConfidenceInterval']; attempt['Slope'] = to_qc['trim_slope']; to_qc['Slope'] = to_qc['trim_slope']; attempt['Curve_b'] = to_qc['trim_b']; to_qc['Curve_b'] = to_qc['trim_b']; attempt['Baseline'] = to_qc['trim_A']; to_qc['Baseline'] = to_qc['trim_A']; attempt['Post-Transition'] = to_qc['trim_B']; to_qc['Post-Transition'] = to_qc['trim_B']; attempt['Trimmed'] = True
            else:
                if highest_criteria == 'rsq':
                    attempt['CHalf'] = to_qc['fit_CHalf']; attempt['r_squared'] = to_qc['fit_r_squared']; attempt['ratioTOrange'] = to_qc['fit_ratioTOrange']; attempt['CHalf_ConfidenceInterval'] = to_qc['fit_CHalf_ConfidenceInterval']; attempt['Slope'] = to_qc['fit_slope']; to_qc['Slope'] = to_qc['fit_slope']; attempt['Curve_b'] = to_qc['fit_Curve_b']; to_qc['Curve_b'] = to_qc['fit_Curve_b']; attempt['Baseline'] = to_qc['fit_Curve_A']; to_qc['Baseline'] = to_qc['fit_Curve_A']; attempt['Post-Transition'] = to_qc['fit_Curve_B']; to_qc['Post-Transition'] = to_qc['fit_Curve_B']; attempt['Trimmed'] = False
                elif highest_criteria == 'ci':
                    attempt['CHalf'] = to_qc['fit_CHalf']; attempt['r_squared'] = to_qc['fit_r_squared']; attempt['ratioTOrange'] = to_qc['fit_ratioTOrange']; attempt['CHalf_ConfidenceInterval'] = to_qc['fit_CHalf_ConfidenceInterval']; attempt['Slope'] = to_qc['fit_slope']; to_qc['Slope'] = to_qc['fit_slope']; attempt['Curve_b'] = to_qc['fit_Curve_b']; to_qc['Curve_b'] = to_qc['fit_Curve_b']; attempt['Baseline'] = to_qc['fit_Curve_A']; to_qc['Baseline'] = to_qc['fit_Curve_A']; attempt['Post-Transition'] = to_qc['fit_Curve_B']; to_qc['Post-Transition'] = to_qc['fit_Curve_B']; attempt['Trimmed'] = False
                else: #default to rsq if failed
                    attempt['CHalf'] = to_qc['fit_CHalf']; attempt['r_squared'] = to_qc['fit_r_squared']; attempt['ratioTOrange'] = to_qc['fit_ratioTOrange']; attempt['CHalf_ConfidenceInterval'] = to_qc['fit_CHalf_ConfidenceInterval']; attempt['Slope'] = to_qc['fit_slope']; to_qc['Slope'] = to_qc['fit_slope']; attempt['Curve_b'] = to_qc['fit_Curve_b']; to_qc['Curve_b'] = to_qc['fit_Curve_b']; attempt['Baseline'] = to_qc['fit_Curve_A']; to_qc['Baseline'] = to_qc['fit_Curve_A']; attempt['Post-Transition'] = to_qc['fit_Curve_B']; to_qc['Post-Transition'] = to_qc['fit_Curve_B']; attempt['Trimmed'] = False
                
            range_qc = range_cutoff[0] <= attempt.loc[0]['CHalf'] <= range_cutoff[1]
            rsq_qc = attempt.loc[0]['r_squared'] >= rsq_cutoff
            if HANDLE_CI_UNCERTAINTY:
                if attempt.loc[0]['ratioTOrange'] > rtr_cutoff: rtr_qc = True
                else: rtr_qc = attempt.loc[0]['ratioTOrange'] <= rtr_cutoff
            else: rtr_qc = attempt.loc[0]['ratioTOrange'] <= rtr_cutoff
            attempt['Peptide'] = [peptides]
            attempt['Label@Accession'] = label
            attempt['Label Type'] = label.split('_')[0]
            if CUSTOM_FASTA: 
                try:
                    attempt['Mutation'] = label.split('_')[4]
                except IndexError:
                    attempt['Mutation'] = 'None'
            attempt['Label Site'] = label.split('_')[1]
            attempt['Accession'] = label.split('_')[2] + '_' + label.split('_')[3] 
            attempt['Site Type'] = sites[0]
            attempt['Residue Number'] = int(label.split('_')[1][1:])
            attempt['Count'] = len(group)
            qc_state = range_qc and rsq_qc and rtr_qc
            if not qc_state:
                attempt['Significant'] = False
            else:
                attempt['Significant'] = True
            if CUSTOM_FASTA: attempt = attempt[['Label@Accession','Accession','Peptide','Mutation','Count','Site Type','Label Site','Label Type','Residue Number','CHalf','r_squared','ratioTOrange','CHalf_ConfidenceInterval','Slope','Curve_b','Baseline','Post-Transition','Significant']]
            else: attempt = attempt[['Label@Accession','Accession','Peptide','Count','Site Type','Label Site','Label Type','Residue Number','CHalf','r_squared','ratioTOrange','CHalf_ConfidenceInterval','Slope','Curve_b','Baseline','Post-Transition','Significant']]
            csDF = csDF._append(attempt,ignore_index=True)
        else:
            group['Count'] = 1
            if CUSTOM_FASTA: group = group[['Label@Accession','Accession','Peptide','Mutation','Count','Site Type','Label Site','Label Type','Residue Number','CHalf','r_squared','ratioTOrange','CHalf_ConfidenceInterval','Slope','Curve_b','Baseline','Post-Transition','Significant']]
            else: group = group[['Label@Accession','Accession','Peptide','Count','Site Type','Label Site','Label Type','Residue Number','CHalf','r_squared','ratioTOrange','CHalf_ConfidenceInterval','Slope','Curve_b','Baseline','Post-Transition','Significant']]
            csDF = csDF._append(group,ignore_index=True)
        if HANDLE_CI_UNCERTAINTY: csDF['CHalf_ConfidenceInterval'] = csDF['CHalf_ConfidenceInterval'].mask(csDF['CHalf_ConfidenceInterval']>rtr_cutoff,np.nan)
        if not KEEP_INSIGNIFICANT: csDF = csDF[csDF['Significant']] #remove insignificant sites from final output
        csDF = csDF.sort_values(by=['Accession','Residue Number'])
        if CUSTOM_FASTA: csDF['Mutation'].fillna('None',inplace=True)
        csDF.to_csv(f'{outdir}/{condition}/{condition} Combined Sites.csv', index=False)
    return csDF

def QualityControl(raw_file,combined_output_file,combined_sites_file,name,outdir,chalf_low=0,chalf_high=3.48,rsq=0.8,confint=0.35,highest_criteria='rsq',residues=['Y','H','M','C'],ci_filter=False): 
    #Get counts prior to filtering
    path = f'{outdir}/{name}'
    print(f'Performing Quality Control for {name}')
    os.makedirs(path,exist_ok=True)
    try:
        rawDF = pd.read_csv(raw_file)
        conDF = pd.read_csv(combined_output_file)
        csDF = pd.read_csv(combined_sites_file)
    except FileNotFoundError as e:
        traceback.print_exc()
        raise FileNotFoundError(f'{name} is missing necessary input files and will be skipped. Error: {e}')
    rawDF = rawDF[['Protein Accession','Peptide']].rename(columns={'Protein Accession':'Accession'})
    raw_pep = len(rawDF)
    raw_prot = len(rawDF['Accession'].unique())
    
    #Keep only peptides that have labelable residues
    labelable = conDF[conDF['Site Type'].str.contains('|'.join(['Single Unlabeled', 'Single Labeled', 'Multi Unlabeled',
           'Multi Labeled']))]
    
    if highest_criteria == 'rsq' and not ci_filter: ci = False
    elif highest_criteria == 'ci' or ci_filter: ci = True
    else: ci = False
    
    '''Fitting QC'''
    #Mark peptides that were fit
    labelable['Can be fit'] = labelable['Slope'].notna()
    #Mark peptides that are in the correct range of CHalf values (and meet the above criteria)
    labelable['C½ in range'] = np.logical_and(labelable['Can be fit'], np.logical_and(labelable['CHalf'] >= chalf_low, labelable['CHalf'] <= chalf_high))
    #Mark peptides that have acceptable rsquared values (and meet the above criteria)
    labelable['R² in range'] = np.logical_and(labelable['C½ in range'], labelable['r_squared'] >= rsq)
    #Mark peptides that have acceptable confidence intervals (and meet the above criteria)
    if ci: labelable['Confidence Interval in range'] = np.logical_and(labelable['R² in range'], labelable['ratioTOrange'] <= confint)
    #Identify which peptides are part of proteins with multiple reporter regions (and meet the above criteria)
    reporter_mask = (labelable.groupby(by=['Accession','Start','End']).count().reset_index().groupby(by='Accession').count()['Start'] > 1).to_frame().reset_index().rename(columns={'Start':'Has >1 reporter'})
    labelable = labelable.merge(reporter_mask, how='left', on='Accession')
    if ci: labelable['Has >1 reporter'] = np.logical_and(labelable['Has >1 reporter'], labelable['Confidence Interval in range'])
    else: labelable['Has >1 reporter'] = np.logical_and(labelable['Has >1 reporter'], labelable['R² in range'])
    
    '''Labeling QC'''
    #Identify what labelable residues are present
    for residue in residues:
        labelable[residue] = labelable['Peptide'].str.contains(residue)
    #Identify which labels are present in each peptide
    raw_labels = [re.escape(label) for label in conDF['Label Type'].dropna().unique() if label not in residues]
    labels = []
    for residue in residues:
        labels += [element for element in raw_labels if residue in element[0]]
    #print(labels)
    for label in labels:
        labelable[label] = labelable['Peptide'].str.contains(label,regex=True)
    
    '''QC Counts'''
    labelable_pep = len(labelable)
    labelable_prot = len(labelable['Accession'].unique())
    can_be_fit_pep = labelable['Can be fit'].sum()
    can_be_fit_prot = len(labelable[labelable['Can be fit']]['Accession'].unique())
    chalf_in_range_pep = labelable['C½ in range'].sum()
    chalf_in_range_prot = len(labelable[labelable['C½ in range']]['Accession'].unique())
    rsq_in_range_pep = labelable['R² in range'].sum()
    rsq_in_range_prot = len(labelable[labelable['R² in range']]['Accession'].unique())
    if ci: ci_in_range_pep = labelable['Confidence Interval in range'].sum(); ci_in_range_prot = len(labelable[labelable['Confidence Interval in range']]['Accession'].unique())
    reporter_pep = labelable['Has >1 reporter'].sum()
    reporter_prot = len(labelable[labelable['Has >1 reporter']]['Accession'].unique())
    
    if ci:
        qcDF = pd.DataFrame({
            'peptide' : [raw_pep,labelable_pep,can_be_fit_pep,chalf_in_range_pep,rsq_in_range_pep,ci_in_range_pep,reporter_pep],
            'protein' : [raw_prot,labelable_prot,can_be_fit_prot,chalf_in_range_prot,rsq_in_range_prot,ci_in_range_prot,reporter_prot],
            'peptide %' : [np.nan,labelable_pep/raw_pep,can_be_fit_pep/labelable_pep,chalf_in_range_pep/labelable_pep,rsq_in_range_pep/labelable_pep,ci_in_range_pep/labelable_pep,reporter_pep/labelable_pep],
            'protein %' : [np.nan,labelable_prot/raw_prot,can_be_fit_prot/labelable_prot,chalf_in_range_prot/labelable_prot,rsq_in_range_prot/labelable_prot,ci_in_range_prot/labelable_prot,reporter_prot/labelable_prot]     
            }, index=['Raw', 'Labelable', 'Can be fit', 'C½ in range', 'R² in range','Confidence Interval in range', 'Has >1 reporter'])
    else:
        qcDF = pd.DataFrame({
            'peptide' : [raw_pep,labelable_pep,can_be_fit_pep,chalf_in_range_pep,rsq_in_range_pep,reporter_pep],
            'protein' : [raw_prot,labelable_prot,can_be_fit_prot,chalf_in_range_prot,rsq_in_range_prot,reporter_prot],
            'peptide %' : [np.nan,labelable_pep/raw_pep,can_be_fit_pep/labelable_pep,chalf_in_range_pep/labelable_pep,rsq_in_range_pep/labelable_pep,reporter_pep/labelable_pep],
            'protein %' : [np.nan,labelable_prot/raw_prot,can_be_fit_prot/labelable_prot,chalf_in_range_prot/labelable_prot,rsq_in_range_prot/labelable_prot,reporter_prot/labelable_prot]     
            }, index=['Raw', 'Labelable', 'Can be fit', 'C½ in range', 'R² in range', 'Has >1 reporter'])
    #Perform counts for residue types
    res_dict = {}
    for residue in residues:
        if ci:
            tmp = {
                'Raw' : [np.nan],
                'Labelable' : [labelable[residue].sum()],
                'Can be fit' : [np.logical_and(labelable['Can be fit'], labelable[residue]).sum()],
                'C½ in range' : [np.logical_and(labelable['C½ in range'], labelable[residue]).sum()],
                'R² in range' : [np.logical_and(labelable['R² in range'], labelable[residue]).sum()],
                'Confidence Interval in range' : [np.logical_and(labelable['Confidence Interval in range'], labelable[residue]).sum()],
                'Has >1 reporter' : [np.logical_and(labelable['Has >1 reporter'], labelable[residue]).sum()]
                }
        else:
            tmp = {
                'Raw' : [np.nan],
                'Labelable' : [labelable[residue].sum()],
                'Can be fit' : [np.logical_and(labelable['Can be fit'], labelable[residue]).sum()],
                'C½ in range' : [np.logical_and(labelable['C½ in range'], labelable[residue]).sum()],
                'R² in range' : [np.logical_and(labelable['R² in range'], labelable[residue]).sum()],
                'Has >1 reporter' : [np.logical_and(labelable['Has >1 reporter'], labelable[residue]).sum()]
                }
        tmpDF = pd.DataFrame(tmp).transpose().rename(columns={0:residue})
        qcDF = qcDF.join(tmpDF)
        res_dict.update({residue:tmpDF})
    
    #Perform counts for label types
    label_dict = {}
    for label in labels:
        #label = label.replace('\\','')
        if ci:
            tmp = {
                'Raw' : [np.nan],
                'Labelable' : [labelable[label].sum()],
                'Can be fit' : [np.logical_and(labelable['Can be fit'], labelable[label]).sum()],
                'C½ in range' : [np.logical_and(labelable['C½ in range'], labelable[label]).sum()],
                'R² in range' : [np.logical_and(labelable['R² in range'], labelable[label]).sum()],
                'Confidence Interval in range' : [np.logical_and(labelable['Confidence Interval in range'], labelable[label]).sum()],
                'Has >1 reporter' : [np.logical_and(labelable['Has >1 reporter'], labelable[label]).sum()]
                }
        else:
            tmp = {
                'Raw' : [np.nan],
                'Labelable' : [labelable[label].sum()],
                'Can be fit' : [np.logical_and(labelable['Can be fit'], labelable[label]).sum()],
                'C½ in range' : [np.logical_and(labelable['C½ in range'], labelable[label]).sum()],
                'R² in range' : [np.logical_and(labelable['R² in range'], labelable[label]).sum()],
                'Has >1 reporter' : [np.logical_and(labelable['Has >1 reporter'], labelable[label]).sum()]
                }
        tmpDF = pd.DataFrame(tmp).transpose().rename(columns={0:label})
        qcDF = qcDF.join(tmpDF)
        label_dict.update({label:tmpDF})
        
    #Perform pairwise label efficiency
    labelable['Unlabeled'] = ~labelable['Peptide'].str.contains('|'.join(labels))
    labelable['Labeled'] = labelable['Peptide'].str.contains('|'.join(labels))
    
    for residue in residues:
        labelable[f'{residue} Labeled'] = labelable['Peptide'].str.contains('|'.join([label for label in labels if residue in label]))
    #print(residues, labels)
    le_cols = residues+[label for label in labels]+['Unlabeled','Labeled']+[f'{residue} Labeled' for residue in residues]
    leDF = labelable.groupby(by=['Accession','Start','End']).sum()[le_cols]
    unique_pep = len(leDF)
    keys = residues+[label for label in labels]
    le_dict = dict(zip(keys,[0]*len(keys)))
    raw_dict = dict(zip(keys,[0]*len(residues)+[np.nan]*len(labels)))
    res_label_dict = dict(zip(residues,[0]*len(residues)))
    for index, row in leDF.iterrows():
        for key in keys:
            if row[key] != 0 and key in residues and row['Unlabeled'] != 0:
                le_dict[key] += 1
            elif row[key] != 0 and key not in residues:
                le_dict[key] += 1
            if row[key] != 0 and key in residues:
                raw_dict[key] += 1
            if f'{key} Labeled' in row.index:
                if row[f'{key} Labeled'] != 0:
                    res_label_dict[key] += 1
                    
    raw_dict.update({'peptide':unique_pep,'protein':np.nan,'peptide %':np.nan,'protein %':np.nan})
    le_dict.update({'peptide':np.nan,'protein':np.nan,'peptide %':np.nan,'protein %':np.nan})
    qcDF = pd.concat([qcDF, pd.Series(raw_dict,name='Unique Sequences').to_frame().transpose()])
    qcDF = pd.concat([qcDF, pd.Series(le_dict,name='Sequence Count').to_frame().transpose()])
    
    unlabeled_dict = {}
    for residue in residues:
        for label in labels:
            #label = label.replace('\\','')
            if residue in label:
                res_label_dict[label] = le_dict[label] / raw_dict[residue]
                unlabeled_dict[label] = np.nan
        unlabeled_dict[residue] = le_dict[residue] / raw_dict[residue]
        res_label_dict[residue] = res_label_dict[residue] / raw_dict[residue]
    raw_label = (leDF['Labeled'] != 0).sum()
    raw_unlabel = (leDF['Unlabeled'] != 0).sum()
    res_label_dict.update({'peptide':raw_label,'protein':np.nan,'peptide %':raw_label/unique_pep,'protein %':np.nan})
    unlabeled_dict.update({'peptide':raw_unlabel,'protein':np.nan,'peptide %':raw_unlabel/unique_pep,'protein %':np.nan})
    qcDF = pd.concat([qcDF, pd.Series(res_label_dict,name='Labeled Penetrance').to_frame().transpose()])
    qcDF = pd.concat([qcDF, pd.Series(unlabeled_dict,name='Unlabeled Penetrance').to_frame().transpose()])
    csDF = csDF[csDF['Significant']]
    cs_dict = {
        'peptide' : len(csDF),
        'protein' : len(csDF['Accession'].unique()),
        'peptide %' : np.nan,
        'protein %' : np.nan
        }
    for residue in residues:
        cs_dict.update({residue:len(csDF[csDF['Label Type']==residue])})
    for label in labels:
        cs_dict.update({label:len(csDF[csDF['Label Type']==label.replace('\\','')])})
    qcDF = pd.concat([qcDF, pd.Series(cs_dict,name='Combined Sites').to_frame().transpose()])
    
    new_columns = [label.replace('\\','') for label in labels]
    qcDF.rename(columns=dict(zip(labels,new_columns)),inplace=True)
    qcDF.to_csv(f'{path}/{name} Quality Control.csv')
    return qcDF

def mutation_extracter(row):
    if row['Mutation'] == 'None': row['marker_shape'] = 'o'
    else: row['marker_shape'] = 'v'; row['Label@Accession'] = '_'.join(row['Label@Accession'].split('_')[:-1])
    return row

def CombinedResidueMapper(conditions_dict,output_dir,file_type='jpg',ylim=(0,3.6),TRENDLINE=True,window_size=3,count_requirement=5,ALLSITES=True,STATS_REFERENCE=True,TRENDLINE_STATS=False,SHARED_ONLY=False,custom_annotation=None,subset=None,CUSTOM_FASTA=False,advanced_options=None):
    #INITIAL TESTS to prevent errors
    print("Checking paramaters and aggregating conditions' data for Combined Residue Mapper...")
    conditions = []
    colors = []
    color_dict = {}
    data_dict = {}
    backup_colors = ['blue', 'lawngreen', 'turquoise', 'magenta', 'darkorchid'] #in case there is an error with colors
    compDF = pd.DataFrame()
    if advanced_options != None:
        extracted_data = read_ann_file(advanced_options)
        if 'subset' in extracted_data: subset = extracted_data['subset']
        if 'custom_annotation' in extracted_data: custom_annotation = extracted_data['custom_annotation']
    if not ((file_type == 'jpg') or (file_type == 'png') or (file_type == 'svg')): #test for correct file type
        print('Unrecognized file type. Selecting .jpg')
        file_type = 'jpg'
    if not os.path.isdir(output_dir): #test if output directory exists
        print(f'Output directory does not exist. Creating {output_dir}')
        os.mkdir(output_dir)
    if not type(window_size) == int: #test if window size is an integer and within correct bounds
        print('Window size is a non-integer value. Defaulting to a window size of 3.')
        window_size = 3
    else:
        if window_size < 2: window_size = 2; print('Window size is below the minimum value of 2. Setting window size to 2.')
    if not type(count_requirement) == int:
        print('Window cutoff is a non-integer value. Defaulting to a window cutoff of 5.')
        count_requirement = 5
    else:
        if count_requirement < window_size:
            count_requirement = window_size
            print(f'Window cutoff must be greater than or equal to window size. Setting window cutoff to {window_size}.') 
    for condition in list(conditions_dict):
        try: #Test if file exists and has the correct formatting
            df = pd.read_csv(conditions_dict[condition][0])
            if CUSTOM_FASTA: df = df[['Label@Accession', 'Accession', 'Peptide', 'Mutation','Count', 'Site Type', 'Label Site', 'Label Type', 'Residue Number', 'CHalf', 'r_squared', 'ratioTOrange', 'CHalf_ConfidenceInterval', 'Slope', 'Significant']]
            else: df = df[['Label@Accession', 'Accession', 'Peptide', 'Count', 'Site Type', 'Label Site', 'Label Type', 'Residue Number', 'CHalf', 'r_squared', 'ratioTOrange', 'CHalf_ConfidenceInterval', 'Slope', 'Significant']]
            conditions.append(condition)
        except KeyError:
            print(f'Input file for {condition} does not have the correct columns. Please check that it is the correct format for a "Combined Sites" file. Skipping to the next conditions.')
            continue
        except FileNotFoundError:
            print(f'Input file for {condition} does not exist. Please check that it has the correct path. Skipping to the next conditions.')
            continue
        df['Condition'] = condition
        data_dict.update({condition:df})
        color = conditions_dict[condition][1]
        if is_color_like(color) and color not in colors: #test if the color is real and unique
            color_dict.update({condition:color})
            colors.append(color)
        else:
            try: #picks an unused color if colors are broken
                backup_color = random.choice(backup_colors)
                backup_colors.remove(backup_color)
                color = backup_color
                print(f'Specified color ({color}) for {condition} is not useable. Selecting a backup color ({backup_color})')
            except (IndexError, ValueError):
                conditions.remove(condition)
                print(f'Cannot resolve color; skipping {condition}')
        df = df[df['Significant']] #only choosing significant sites
        if ALLSITES: df = df[df['Site Type'].str.contains('Single')] #removing non single sites
        else: df = df[df['Site Type']=='Single Labeled'] #keeping only single labeled sites
        compDF = compDF._append(df,ignore_index=True)
    if len(conditions) < 2: print('Not enough conditions to run Combined Residue Mapper. Skipping this step.'); return
    ANNOTATE = False
    compDF['marker_shape'] = 'o'
    if CUSTOM_FASTA:
        compDF['Mutation'] = compDF['Mutation'].fillna('None')
        compDF = compDF.apply(mutation_extracter,axis=1)
    if custom_annotation != None:
        if type(custom_annotation) != dict: print('Custom annotation is in the wrong format. Skipping this step.'); ANNOTATE = False
        else: annotations = list(custom_annotation); ANNOTATE = True
    groups = compDF.groupby(by='Accession')
    total_rows = len(groups)
    count_p = 0
    process_start_time = time.time()
    for accession, group in groups:
        progress_logger(
            count_p,
            total_rows,
            description="Combined Residue Mapper",
            update_every_n_iterations=total_rows//10, # Adjust for your needs
            start_time=process_start_time
        )
        count_p += 1
        with sns.axes_style('whitegrid'):
            plt.close()
            fig, ax = plt.subplots()
            if subset != None and accession not in subset: continue
            count = 0
            group.sort_values(['Condition','Residue Number'],inplace=True)
            if SHARED_ONLY: group = group[group['Label@Accession'].duplicated(keep=False)] #only keeps label@accession values that are shared across conditions
            for condition in conditions:
                if len(group[group['Condition']==condition]) < 1: continue
                else: count += 1
            if count < 2: continue
            if STATS_REFERENCE: outDF = group[['Label@Accession','Residue Number','Label Type']].drop_duplicates().sort_values('Residue Number')
            else: TRENDLINE_STATS = False
            if TRENDLINE_STATS: trendDF = pd.DataFrame()
            for condition in conditions:
                cond_data = group[group['Condition']==condition]
                x = cond_data['Residue Number']
                if len(x) < 1: continue
                else: count += 1
                if STATS_REFERENCE: outDF = outDF.merge(cond_data[['Label@Accession','CHalf','CHalf_ConfidenceInterval']].rename(columns=dict(zip(['CHalf','CHalf_ConfidenceInterval'],[condition,f'{condition}_CI']))),how='left',on='Label@Accession')
                y = cond_data['CHalf']
                ci = cond_data['CHalf_ConfidenceInterval']
                avg = cond_data['CHalf'].rolling(window=window_size).mean()
                #markers = cond_data['marker_shape']
                for marker, cond_data_subset in cond_data.groupby(by='marker_shape'):
                    x_subset = cond_data_subset['Residue Number']
                    y_subset = cond_data_subset['CHalf']
                    if marker == 'o': sns.scatterplot(x=x_subset,y=y_subset,color=color_dict[condition],marker=marker,label=condition,ax=ax)
                    else: sns.scatterplot(x=x_subset,y=y_subset,color=color_dict[condition],marker=marker,s=100,ax=ax)
                #sns.scatterplot(x=x,y=y,color=color_dict[condition],style=markers,markers={'o':'o','s':'s'},label=condition)
                ax.errorbar(x, y, yerr=ci, fmt="none", color=color_dict[condition], capsize=3)
                if TRENDLINE: #Creates trendlines on CRM outputs if there are enough points as specified above
                    if len(x.unique()) >= count_requirement:
                        sns.lineplot(x=x,y=avg,color=color_dict[condition],ax=ax)
                        if TRENDLINE_STATS: trendDF = pd.concat([trendDF,pd.DataFrame({f'{condition}_rn':x,f'{condition}_avg':avg})],axis=1)
            ax.set_xlabel('Residue Number',fontsize=12,weight=600)
            ax.set_ylabel('C½ [GdmCl]',fontsize=12,weight=600)
            ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:.0f}'))
            xticks = list(plt.xticks()[0])
            xlabels = list(plt.xticks()[1])
            ax.tick_params(axis='both', which='major', labelsize=12)
            ax.set_xticks(xticks)
            ax.set_xticklabels(xlabels)#,weight=600)
            #ax.set_yticks(yticks)
            #ax.set_yticklabels(ylabels)#,weight=600)
            ax.set_title(accession,fontsize=14,weight=600)
            ax.legend(fontsize=12,bbox_to_anchor =(0.5,-0.32), loc='lower center', ncol=count)#bbox_to_anchor=(1.05, 1.0), loc='upper left')
            if ANNOTATE:
                if accession in annotations:
                    features = custom_annotation[accession]
                    for feature in features:
                        if type(feature) != dict: print(f'{feature} in custom_annotation not recognized. Skipping this feature.')
                        if feature['type'] == 'title': ax.set_title(feature['value'],fontsize=14,weight=600)
                        elif feature['type'] == 'vline': ax.axvline(feature['value'],linestyle='--',color='black')
                        elif feature['type'] == 'hline': ax.axhline(feature['value'],linestyle='--',color='black')
                        else: print(f'{feature} in custom_annotation not recognized. Skipping this feature.')
            xmin, xmax = ax.get_xlim()
            if xmin < 0: xmin = 0
            ax.set_xlim((xmin,xmax))
            ax.set_ylim(ylim)
            plt.savefig(f'{output_dir}/{accession.replace("|","_")}.{file_type}', bbox_inches='tight')
            if TRENDLINE_STATS: outDF = pd.concat([outDF,trendDF],axis=1)
            if STATS_REFERENCE: outDF.to_csv(f'{output_dir}/{accession.replace("|","_")}_stats.csv',index=False)
        
        
def DeltaMapper(conditions_dict,output_dir,file_type='jpg',significance_cutoff_bool=False,significance_cutoff=None,n_cutoff=3,ylim=(-3.6,3.6),TRENDLINE=True,window_size=3,count_requirement=5,ALLSITES=True,STATS_REFERENCE=True,TRENDLINE_STATS=False,custom_annotation=None,subset=None,CUSTOM_FASTA=False,advanced_options=None):
    #INITIAL TESTS to prevent errors
    print("Checking paramaters and aggregating conditions' data for Delta Mapper...")
    conditions = []
    colors = []
    color_dict = {}
    data_dict = {}
    comp_dict = {'reference':[],'experimental':[]}
    backup_colors = ['blue', 'lawngreen', 'turquoise', 'magenta', 'darkorchid'] #in case there is an error with colors
    compDF = pd.DataFrame()
    if advanced_options != None:
        extracted_data = read_ann_file(advanced_options)
        if 'subset' in extracted_data: subset = extracted_data['subset']
        if 'custom_annotation' in extracted_data: custom_annotation = extracted_data['custom_annotation']
    if significance_cutoff == None or significance_cutoff_bool == False:
        CUT = False
    else:
        CUT = True
        if type(significance_cutoff) != float:
            try:
                significance_cutoff = float(significance_cutoff)
            except ValueError:
                significance_cutoff = 0.05
                print('Significance cutoff must be a float. Defaulting to a p-value of 0.05')
    if not ((file_type == 'jpg') or (file_type == 'png') or (file_type == 'svg')): #test for correct file type
        print('Unrecognized file type. Selecting .jpg')
        file_type = 'jpg'
    if not os.path.isdir(output_dir): #test if output directory exists
        print(f'Output directory does not exist. Creating {output_dir}')
        os.mkdir(output_dir)
    if not type(window_size) == int: #test if window size is an integer and within correct bounds
        print('Window size is a non-integer value. Defaulting to a window size of 3.')
        window_size = 3
    else:
        if window_size < 2: window_size = 2; print('Window size is below the minimum value of 2. Setting window size to 2.')
    if not type(count_requirement) == int:
        print('Window cutoff is a non-integer value. Defaulting to a window cutoff of 5.')
        count_requirement = 5
    else:
        if count_requirement < window_size:
            count_requirement = window_size
            print(f'Window cutoff must be greater than or equal to window size. Setting window cutoff to {window_size}.') 
    for condition in list(conditions_dict):
        try: #Test if file exists and has the correct formatting
            df = pd.read_csv(conditions_dict[condition][0])
            if CUSTOM_FASTA: df = df[['Label@Accession', 'Accession', 'Peptide', 'Mutation','Count', 'Site Type', 'Label Site', 'Label Type', 'Residue Number', 'CHalf', 'r_squared', 'ratioTOrange', 'CHalf_ConfidenceInterval', 'Slope', 'Significant']]
            else: df = df[['Label@Accession', 'Accession', 'Peptide', 'Count', 'Site Type', 'Label Site', 'Label Type', 'Residue Number', 'CHalf', 'r_squared', 'ratioTOrange', 'CHalf_ConfidenceInterval', 'Slope', 'Significant']]
            conditions.append(condition)
        except KeyError:
            print(f'Input file for {condition} does not have the correct columns. Please check that it is the correct format for a "Combined Sites" file. Skipping to the next conditions.')
            continue
        except FileNotFoundError:
            print(f'Input file for {condition} does not exist. Please check that it has the correct path. Skipping to the next conditions.')
            continue
        df['Condition'] = condition
        data_dict.update({condition:df})
        color = conditions_dict[condition][1]
        if is_color_like(color) and color not in colors: #test if the color is real and unique
            color_dict.update({condition:color})
            colors.append(color)
        else:
            try: #picks an unused color if colors are broken
                backup_color = random.choice(backup_colors)
                backup_colors.remove(backup_color)
                color = backup_color
                print(f'Specified color ({color}) for {condition} is not useable. Selecting a backup color ({backup_color})')
            except (IndexError, ValueError):
                conditions.remove(condition)
                print(f'Cannot resolve color; skipping {condition}')
        comp = conditions_dict[condition][2]
        if comp == 'reference' and len(comp_dict['reference']) < 1: #assigning comparison groups, also only taking first case of reference as the reference
            comp_dict['reference'].append(condition)
            df['Type'] = 'reference'
        elif comp == 'experimental':
            comp_dict['experimental'].append(condition)
            df['Type'] = 'experimental'
        else: #preventing more than one reference case
            print(f'{condition} has either an unexpected type or is a second instance of reference. Only one reference may be selected for a group. Setting {condition} to be an experimental condition')
            comp_dict['experimental'].append(condition)
            df['Type'] = 'experimental'
        df = df[df['Significant']] #only choosing significant sites
        if ALLSITES: df = df[df['Site Type'].str.contains('Single')] #removing non single sites
        else: df = df[df['Site Type']=='Single Labeled'] #keeping only single labeled sites
        compDF = compDF._append(df,ignore_index=True)
    if len(conditions) < 2: print('Not enough conditions to run Delta Mapper. Skipping this step.'); return
    ANNOTATE = False
    compDF['marker_shape'] = 'o'
    if CUSTOM_FASTA:
        compDF['Mutation'] = compDF['Mutation'].fillna('None')
        compDF = compDF.apply(mutation_extracter,axis=1)
    if custom_annotation != None:
        if type(custom_annotation) != dict: print('Custom annotation is in the wrong format. Skipping this step.'); ANNOTATE = False
        else: annotations = list(custom_annotation); ANNOTATE = True
    groups = compDF.groupby(by='Accession')
    if len(comp_dict['reference']) < 1 or len(comp_dict['experimental']) < 1: print('Not enough conditions to run Delta Mapper. Skipping this step.'); return
    total_rows = len(groups)
    count_p = 0
    process_start_time = time.time()
    for accession, group in groups:
        progress_logger(
            count_p,
            total_rows,
            description="Delta Mapper",
            update_every_n_iterations=total_rows//10, # Adjust for your needs
            start_time=process_start_time
        )
        count_p += 1
        if subset != None and accession not in subset: continue
        if CUSTOM_FASTA:
            mutation_sites = list(set(group[group['Mutation']!='None']['Residue Number'].to_list()))
        referenceDF = group[group['Type'] == 'reference'].copy()
        referenceDF.rename(columns={'CHalf':'Reference'},inplace=True)
        reference = comp_dict['reference'][0]
        for condition in comp_dict['experimental']: #Make stat plots to compare distributions of conditions
            to_merge = group[group['Condition'] == condition].copy()
            to_merge.rename(columns={'CHalf':condition},inplace=True)
            referenceDF = referenceDF.merge(to_merge[['Label@Accession',condition]],how='left',on='Label@Accession')
            referenceDF[f'Δ{condition}'] = referenceDF[condition] - referenceDF['Reference']
            to_compare = referenceDF.dropna(subset=condition)
            kruskal, p_value = stats.kruskal(to_compare['Reference'],to_compare[condition])
            referenceDF[f'p_{condition}'] = p_value
            if len(to_compare) < n_cutoff: continue
            if CUT: #for removing unsignificant changes
                if p_value > significance_cutoff: continue 
            plt.close()
            with sns.axes_style('whitegrid'):
                fig, (ax1, ax2) = plt.subplots(1,2)
                
                #KDE Plots
                sns.kdeplot(to_compare['Reference'],color=color_dict[reference],ax=ax1,label=reference)
                sns.kdeplot(to_compare[condition],color=color_dict[condition],ax=ax1,label=condition)
                ax1.set_xlabel('C½ [GdmCl]',fontsize=12,weight=600)
                ax1.set_ylabel('Density',fontsize=12,weight=600)
                ax1.tick_params(axis='both', which='major', labelsize=12)
                ax1.legend(fontsize=12)
                ax1.set_title(f'Kruskal: {round(kruskal,4)} n={len(to_compare)}',fontsize=12)
                
                #Boxplots
                data = pd.DataFrame({
                    'CHalf' : to_compare['Reference'].to_list() + to_compare[condition].to_list(),
                    'Group' : [reference]*len(to_compare) + [condition]*len(to_compare)                    
                    })
                sns.boxplot(data=data,x='Group',y='CHalf',ax=ax2,hue='Group',palette=[color_dict[reference],color_dict[condition]])
                ax2.set_ylabel('C½ [GdmCl]',fontsize=12,weight=600)
                ax2.set_xlabel('Condition',fontsize=12,weight=600)
                ax2.tick_params(axis='both', which='major', labelsize=12)
                ax2.set_title(f'P-Value: {round(p_value,4)}',fontsize=12)
                
                plt.suptitle(accession,fontsize=14,weight=600)
                plt.tight_layout()
                plt.savefig(f'{output_dir}/{accession.replace("|","_")} ({reference} vs {condition}) Distribution Comparison.{file_type}')
        if len(referenceDF) == 0: continue
        with sns.axes_style('whitegrid'):
            plt.close()
            fig, ax = plt.subplots()
            referenceDF.sort_values(['Residue Number'],inplace=True)
            if TRENDLINE_STATS: trendDF = pd.DataFrame()
            count = 0
            for condition in comp_dict['experimental']:
                if CUT: #skip insignificant differences
                    p_value = referenceDF[f'p_{condition}'].to_list()[0]
                    if p_value > significance_cutoff or np.isnan(p_value): continue
                if len(referenceDF[f'Δ{condition}'].dropna()) > 0: count += 1
                sns.scatterplot(data=referenceDF, x='Residue Number', y=f'Δ{condition}', ax=ax, color=color_dict[condition], label=condition)
                if TRENDLINE:
                    cond_data = referenceDF.dropna(subset=f'Δ{condition}').copy()
                    x = cond_data['Residue Number']
                    avg = cond_data[f'Δ{condition}'].rolling(window=window_size).mean()
                    if len(x.unique()) >= count_requirement:
                        sns.lineplot(x=x,y=avg,color=color_dict[condition],ax=ax)
                        if TRENDLINE_STATS: trendDF = pd.concat([trendDF,pd.DataFrame({f'{condition}_rn':x,f'{condition}_avg':avg})],axis=1)
            if count == 0: continue
            ax.set_title(accession,fontsize=14,weight=600)
            ax.legend(fontsize=12,bbox_to_anchor =(0.5,-0.32), loc='lower center', ncol=count)#bbox_to_anchor=(1.05, 1.0), loc='upper left')
            ax.set_title(accession,fontsize=14,weight=600)
            
            if CUSTOM_FASTA:
                for site in mutation_sites:
                    ax.plot(site, 0, marker='d', markersize=5, color='black', markeredgecolor='black')
            if ANNOTATE:
                if accession in annotations:
                    features = custom_annotation[accession]
                    for feature in features:
                        if type(feature) != dict: print(f'{feature} in custom_annotation not recognized. Skipping this feature.')
                        if feature['type'] == 'title': ax.set_title(feature['value'],fontsize=14,weight=600)
                        elif feature['type'] == 'vline': ax.axvline(feature['value'],linestyle='--',color='black')
                        elif feature['type'] == 'hline': ax.axhline(feature['value'],linestyle='--',color='black')
                        else: print(f'{feature} in custom_annotation not recognized. Skipping this feature.')
            
            if TRENDLINE_STATS: referenceDF = pd.concat([referenceDF,trendDF],axis=1)
            if STATS_REFERENCE: referenceDF.to_csv(f'{output_dir}/{accession.replace("|","_")}_condition_comparison_stats.csv',index=False)
            
            ax.axhline(0,color='black')
            ax.set_xlabel('Residue Number',fontsize=12,weight=600)
            ax.set_ylabel('ΔC½ [GdmCl]',fontsize=12,weight=600)
            ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:.0f}'))
            ax.set_ylim(ylim)
            ax.tick_params(axis='both', which='major', labelsize=12)

            plt.savefig(f'{output_dir}/{accession.replace("|","_")}_condition_comparison.{file_type}', bbox_inches='tight')

def create_interactive_kde_plot(csv_file, color, condition_name, x_min=0, x_max=3.6, stepsize=500):
    """
    Creates an interactive Altair KDE plot from a CSV file with a 'CHalf' column,
    with tooltips showing density, and customizable color.
    """
    try:
        df = pd.read_csv(csv_file)
        df['Condition'] = condition_name
        df = df[df['Significant']]
    except FileNotFoundError:
        print(f"Error: File '{csv_file}' not found.")
        return
    except KeyError:
        print(f"Error: Column 'CHalf' not found in '{csv_file}'.")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()
        return

    chalf_data = df['CHalf'].dropna()

    if chalf_data.empty:
        print("Error: 'CHalf' column contains no valid numerical data.")
        return

    n = len(chalf_data)
    stdev = chalf_data.std()
    bandwidth = n**(-1/5) * stdev

    chart = alt.Chart(df).transform_density(
        'CHalf',
        as_=['CHalf', 'density'],
        extent=[x_min, x_max],
        groupby=['Condition'],
        counts=False,
        steps=stepsize,
        bandwidth=bandwidth
    ).mark_line(color=color).encode(
        x=alt.X('CHalf:Q', title='C½ [GdmCl]', scale=alt.Scale(domain=(x_min, x_max))),
        y=alt.Y('density:Q', title='Density'),
        color=alt.Color('Condition', legend=alt.Legend(title="Condition")),
        tooltip=[
            alt.Tooltip('CHalf:Q', title='CHalf'),
            alt.Tooltip('density:Q', title='Density'),
            alt.Tooltip('Condition:N', title='Condition')
        ]
    ).properties(
        title='C½ Distribution',
        width=600,
        height=400,
    )

    return chart

def create_combined_boxplot(file_paths, condition_names, colors, y_min=0, y_max=3.6):
    """
    Creates a combined boxplot from multiple CSV files, with customizable colors and condition names.
    """
    dfs = []
    for i, file in enumerate(file_paths):
        try:
            df = pd.read_csv(file)
            df['Condition'] = condition_names[i]
            dfs.append(df)
        except FileNotFoundError:
            print(f"Error: File '{file}' not found for boxplot.")
            return
    if not dfs:
        print("No dataframes to combine for boxplot.")
        return

    conDF = pd.concat(dfs, ignore_index=True)
    conDF = conDF[conDF['Significant']]

    boxplot = alt.Chart(conDF).mark_boxplot(size=40).encode(
        x=alt.X('Condition:N', sort=condition_names, title='Condition'),
        y=alt.Y('CHalf:Q', scale=alt.Scale(domain=(y_min, y_max)), title='C½ [GdmCl]'),
        color=alt.Color('Condition:N', scale=alt.Scale(domain=condition_names, range=colors))
    ).properties(
        title='C½ Boxplot by Condition',
        width=200,
        height=400,
    )
    return boxplot

def create_site_type_bar_chart(df, condition_column, site_type_column, conditions, site_types, colors):
    """
    Creates a bar chart of significant C½ measurements by site type within each condition.
    """
    # Group by condition and site type, then count significant measurements
    grouped_df = df.groupby([condition_column, site_type_column]).size().reset_index(name='count')

    # Calculate total counts per condition
    total_counts_df = df.groupby(condition_column).size().reset_index(name='count')
    total_counts_df[site_type_column] = 'Total'

    # Combine the grouped and total counts
    combined_counts = pd.concat([grouped_df, total_counts_df], ignore_index=True)

    # Define a custom sort order for site types to ensure 'Total' comes first
    site_type_sort_order = ['Total'] + site_types

    # Create the bar chart
    chart = alt.Chart(combined_counts).mark_bar().encode(
        x=alt.X(site_type_column + ':N', title='Site Type', sort=site_type_sort_order), # Added x-axis label and sort
        y=alt.Y('count:Q', title='Significant C½ Measurements'),
        color=alt.Color(condition_column + ':N', title='Condition', scale=alt.Scale(domain=conditions, range=colors)),
        xOffset=alt.XOffset(condition_column + ':N'),
        tooltip=[condition_column + ':N', site_type_column + ':N', 'count:Q']
    ).properties(
        title='Counts of Significant C½ Measurements',
        width=600,
        height=400,
    ).interactive()

    return chart

def generate_qc_report(conditions_dict, output_dir, open_on_completion=False):
    """
    Generates an Altair report with KDE plots, a combined boxplot, and a bar chart
    based on the provided condition data.

    Args:
        conditions_dict (dict): A dictionary where keys are condition names and values are tuples
                                (file_path, color, third_value_not_used).
        output_dir (str): The directory where the HTML report will be saved.
        open_on_completion (bool): If True, the HTML file will be opened after creation.
    """
    condition_names = list(conditions_dict.keys())
    file_paths = [item[0] for item in conditions_dict.values()]
    colors = [item[1] for item in conditions_dict.values()]

    # Create KDE plots
    kde_charts = []
    conDF_for_kde = pd.DataFrame()
    for i, file in enumerate(file_paths):
        chart = create_interactive_kde_plot(file, colors[i], condition_names[i])
        if chart:
            kde_charts.append(chart)
        try:
            df = pd.read_csv(file)
            df['Condition'] = condition_names[i]
            conDF_for_kde = pd.concat([conDF_for_kde, df], ignore_index=True)
        except FileNotFoundError:
            print(f"Error: File '{file}' not found when preparing data for KDE.")
            continue

    if not kde_charts:
        print("No KDE charts were generated. Aborting report generation.")
        return

    # Layer the KDE charts
    out_kde = kde_charts[0]
    for chart in kde_charts[1:]:
        out_kde = alt.layer(out_kde, chart)

    # Create combined boxplot
    boxplot_chart = create_combined_boxplot(file_paths, condition_names, colors)
    if not boxplot_chart:
        print("Boxplot chart could not be generated. Continuing without it.")
        return

    # Filter conDF for significant measurements for the bar chart
    conDF_significant = conDF_for_kde[conDF_for_kde['Significant']]

    # Create bar chart
    site_types = ['Single Labeled', 'Single Unlabeled'] # Assuming these are the fixed site types
    bar_chart = create_site_type_bar_chart(conDF_significant, 'Condition', 'Site Type', condition_names, site_types, colors)
    if not bar_chart:
        print("Bar chart could not be generated. Continuing without it.")
        return

    # Combine all charts
    final_chart = alt.hconcat(out_kde, boxplot_chart, bar_chart).resolve_scale(
        color='independent'
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14,
        titleFontWeight='bold'
    ).configure_title(
        fontSize=20
    )

    # Save the chart to HTML
    output_filepath = os.path.join(output_dir, 'qc_report.html')
    final_chart.save(output_filepath)
    print(f"Report saved to: {output_filepath}")

    # Open on completion if requested
    if open_on_completion:
        try:
            if os.name == 'nt':  # For Windows
                os.startfile(output_filepath)
            elif os.uname().sysname == 'Darwin':  # For macOS
                subprocess.call(['open', output_filepath])
            else:  # For Linux and other POSIX systems
                subprocess.call(['xdg-open', output_filepath])
            print(f"Opened {output_filepath} with default program.")
        except Exception as e:
            print(f"Error opening file: {e}")
            traceback.print_exc()

def ResidueMapper(file,output_dir,file_type='jpg',ylim=(0,3.6),TRENDLINE=True,window_size=3,count_requirement=5,ALLSITES=True,STATS_REFERENCE=True,TRENDLINE_STATS=False,custom_annotation=None,subset=None,CUSTOM_FASTA=False,advanced_options=None):
    #INITIAL TESTS to prevent errors
    print("Performing Residue Mapper...")
    compDF = pd.DataFrame()
    if advanced_options != None:
        extracted_data = read_ann_file(advanced_options)
        if 'subset' in extracted_data: subset = extracted_data['subset']
        if 'custom_annotation' in extracted_data: custom_annotation = extracted_data['custom_annotation']
    if not ((file_type == 'jpg') or (file_type == 'png') or (file_type == 'svg')): #test for correct file type
        print('Unrecognized file type. Selecting .jpg')
        file_type = 'jpg'
    if not os.path.isdir(output_dir): #test if output directory exists
        print(f'Output directory does not exist. Creating {output_dir}')
        os.mkdir(output_dir)
    if not type(window_size) == int: #test if window size is an integer and within correct bounds
        print('Window size is a non-integer value. Defaulting to a window size of 3.')
        window_size = 3
    else:
        if window_size < 2: window_size = 2; print('Window size is below the minimum value of 2. Setting window size to 2.')
    if not type(count_requirement) == int:
        print('Window cutoff is a non-integer value. Defaulting to a window cutoff of 5.')
        count_requirement = 5
    else:
        if count_requirement < window_size:
            count_requirement = window_size
            print(f'Window cutoff must be greater than or equal to window size. Setting window cutoff to {window_size}.') 
    try: #Test if file exists and has the correct formatting
        df = pd.read_csv(file)
        if CUSTOM_FASTA: df = df[['Label@Accession', 'Accession', 'Peptide', 'Mutation','Count', 'Site Type', 'Label Site', 'Label Type', 'Residue Number', 'CHalf', 'r_squared', 'ratioTOrange', 'CHalf_ConfidenceInterval', 'Slope', 'Significant']]
        else: df = df[['Label@Accession', 'Accession', 'Peptide', 'Count', 'Site Type', 'Label Site', 'Label Type', 'Residue Number', 'CHalf', 'r_squared', 'ratioTOrange', 'CHalf_ConfidenceInterval', 'Slope', 'Significant']]
    except KeyError:
        print(f'Input file {file} does not have the correct columns. Please check that it is the correct format for a "Combined Sites" file. Skipping Residue Mapper.')
        return
    except FileNotFoundError:
        print(f'Input file {file} does not exist. Please check that it has the correct path. Skipping Residue Mapper.')
        return
    df = df[df['Significant']] #only choosing significant sites
    if ALLSITES: df = df[df['Site Type'].str.contains('Single')] #removing non single sites
    else: df = df[df['Site Type']=='Single Labeled'] #keeping only single labeled sites
    compDF = compDF._append(df,ignore_index=True)
    ANNOTATE = False
    
    # If CUSTOM_FASTA, marker_shape is determined by mutation_extracter
    # Otherwise, we'll set it to 'o' as a default and let seaborn handle markers by hue.
    if CUSTOM_FASTA:
        compDF['Mutation'] = compDF['Mutation'].fillna('None')
        compDF = compDF.apply(mutation_extracter,axis=1)
    else:
        compDF['marker_shape'] = 'o' # Default marker shape when not dealing with mutations

    if custom_annotation != None:
        if type(custom_annotation) != dict: print('Custom annotation is in the wrong format. Skipping this step.'); ANNOTATE = False
        else: annotations = list(custom_annotation); ANNOTATE = True
            
    # Define a color palette for 'Label Type'
    label_types = compDF['Label Type'].unique()
    colors = sns.color_palette("tab10", len(label_types)) # Using a qualitative palette
    color_map = dict(zip(label_types, colors))

    groups = compDF.groupby(by='Accession')
    total_rows = len(groups)
    count_p = 0
    process_start_time = time.time()
    for accession, group in groups:
        progress_logger(
            count_p,
            total_rows,
            description="Residue Mapper",
            update_every_n_iterations=total_rows//10, # Adjust for your needs
            start_time=process_start_time
        )
        count_p += 1
        with sns.axes_style('whitegrid'):
            plt.close()
            fig, ax = plt.subplots()
            if subset != None and accession not in subset: continue
            
            group.sort_values('Residue Number',inplace=True)
            
            if STATS_REFERENCE: outDF = group[['Label@Accession','Residue Number','Label Type']].drop_duplicates().sort_values('Residue Number')
            if TRENDLINE_STATS: trendDF = pd.DataFrame()
            
            # Plotting based on Label Type and handling mutations
            for label_type, type_group in group.groupby('Label Type'):
                color = color_map[label_type]
                
                # Further group by marker_shape (for mutations if CUSTOM_FASTA is True)
                for marker, marker_group in type_group.groupby('marker_shape'):
                    x_subset = marker_group['Residue Number']
                    y_subset = marker_group['CHalf']
                    ci_subset = marker_group['CHalf_ConfidenceInterval']

                    # Plot scatter points
                    if marker == 'o':
                        sns.scatterplot(x=x_subset, y=y_subset, marker=marker, color=color, label=f'{label_type}', ax=ax)
                    elif marker == 'v': # This is for mutations
                        if CUSTOM_FASTA:
                            sns.scatterplot(x=x_subset, y=y_subset, marker=marker, s=100, color=color, label=f'{label_type} (Mutation)', ax=ax)
                        else: # If not CUSTOM_FASTA, 'v' shouldn't appear, but as a safeguard.
                            sns.scatterplot(x=x_subset, y=y_subset, marker=marker, color=color, label=f'{label_type}', ax=ax)
                            
                    # Plot error bars for each subset
                    ax.errorbar(x_subset, y_subset, yerr=ci_subset, fmt="none", capsize=3, color=color)

            if TRENDLINE: #Creates trendlines on CRM outputs if there are enough points as specified above
                # Calculate trendline for the entire group, regardless of label type, if desired.
                # Or you could calculate per label type if the trend should be type-specific.
                if len(group['Residue Number'].unique()) >= count_requirement:
                    avg = group.groupby('Residue Number')['CHalf'].mean().rolling(window=window_size).mean()
                    sns.lineplot(x=avg.index,y=avg.values,ax=ax, color='grey', linestyle='--', label='Overall Trend') # A neutral color for trend
                    if TRENDLINE_STATS: 
                        trendDF = pd.concat([trendDF,pd.DataFrame({'rn':avg.index,'avg':avg.values})],axis=1)
            
            ax.set_xlabel('Residue Number',fontsize=12,weight=600)
            ax.set_ylabel('C½ [GdmCl]',fontsize=12,weight=600)
            ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:.0f}'))
            xticks = list(plt.xticks()[0])
            xlabels = list(plt.xticks()[1])
            ax.tick_params(axis='both', which='major', labelsize=12)
            ax.set_xticks(xticks)
            ax.set_xticklabels(xlabels)#,weight=600)
            ax.set_title(accession,fontsize=14,weight=600)
            
            # Adjust legend to show both label types and mutation markers
            handles, labels = ax.get_legend_handles_labels()
            # Remove duplicate labels
            unique_labels = {}
            for handle, label in zip(handles, labels):
                if label not in unique_labels:
                    unique_labels[label] = handle
            
            # Sort labels for consistent legend order (optional)
            sorted_labels = sorted(unique_labels.keys())
            sorted_handles = [unique_labels[label] for label in sorted_labels]
            
            # Dynamic ncol calculation
            num_unique_labels = len(sorted_labels)
            max_cols_target = 3 # Aim for a maximum of 3 columns, adjust as needed
            legend_ncol = min(num_unique_labels, max_cols_target)
            
            # Dynamic adjustment for legend y-position to avoid xlabel overlap
            # Estimate number of rows the legend will take
            num_rows = math.ceil(num_unique_labels / legend_ncol)
            
            # Base y-position for a single-row legend, relative to the bottom of the axes (0.0).
            # This value (-0.25) places the *bottom* of the legend at y=-0.25 of the axes.
            # You might need to fine-tune this value based on your specific plot layout and font sizes.
            base_y_pos = -0.25 
            
            # Adjust y-position downwards based on the number of rows.
            # Each additional row pushes the legend further down by a 'row_height_unit'.
            # The '0.05' is an estimated height per row in axes coordinates.
            # This value might also need calibration for your specific output.
            row_height_unit = 0.05 
            dynamic_y_pos = base_y_pos - (num_rows - 1) * row_height_unit
            
            ax.legend(sorted_handles, sorted_labels, fontsize=12, bbox_to_anchor =(0.5,dynamic_y_pos), loc='lower center', ncol=legend_ncol)
            
            if ANNOTATE:
                if accession in annotations:
                    features = custom_annotation[accession]
                    for feature in features:
                        if type(feature) != dict: print(f'{feature} in custom_annotation not recognized. Skipping this feature.')
                        if feature['type'] == 'title': ax.set_title(feature['value'],fontsize=14,weight=600)
                        elif feature['type'] == 'vline': ax.axvline(feature['value'],linestyle='--',color='black')
                        elif feature['type'] == 'hline': ax.axhline(feature['value'],linestyle='--',color='black')
                        else: print(f'{feature} in custom_annotation not recognized. Skipping this feature.')
            xmin, xmax = ax.get_xlim()
            if xmin < 0: xmin = 0
            ax.set_xlim((xmin,xmax))
            ax.set_ylim(ylim)
            plt.savefig(f'{output_dir}/{accession.replace("|","_")}.{file_type}', bbox_inches='tight')
            if TRENDLINE_STATS: outDF = pd.concat([outDF,trendDF],axis=1)
            if STATS_REFERENCE: outDF.to_csv(f'{output_dir}/{accession.replace("|","_")}_stats.csv',index=False)

def get_quality_control_default_args():
    """
    Extracts default arguments from the QualityControl function definition.
    """

    signature = inspect.signature(QualityControl)
    defaults = {
        param.name: param.default
        for param in signature.parameters.values()
        if param.default is not inspect.Parameter.empty
    }
    return defaults

def prepare_quality_control_arguments(params: 'ParameterDict'):
    """
    Extracts QualityControl-specific parameters from a ParameterDict and
    fills in missing values with the default arguments from the QualityControl function.

    Args:
        params: An instance of ParameterDict containing workflow parameters.

    Returns:
        A dictionary of arguments ready to be passed to the QualityControl function
        using the **kwargs syntax.
    """
    qc_args = {}
    default_qc_args = get_quality_control_default_args()

    # Define the mapping from ParameterDict path to QualityControl argument name
    mappings = {
        'qc.filter.min': 'chalf_low',
        'qc.filter.max': 'chalf_high',
        'qc.filter.rsq': 'rsq',
        'qc.filter.ci_value': 'confint',
        'qc.filter.optimize': 'highest_criteria',
        'qc.filter.ci_filter': 'ci_filter'
    }

    for param_path, arg_name in mappings.items():
        try:
            current_value = params
            for part in param_path.split('.'):
                current_value = getattr(current_value, part)
            qc_args[arg_name] = current_value
        except AttributeError:
            print(f"Warning: Parameter '{param_path}' not found. Using default for '{arg_name}' ('{default_qc_args.get(arg_name)}')")
            qc_args[arg_name] = default_qc_args.get(arg_name)

    # Handle 'residues' with conversion from string to list of uppercase characters
    try:
        residues_str = params.qc.search.residues
        if isinstance(residues_str, str):
            qc_args['residues'] = list(residues_str.upper())
        else:
            raise TypeError("qc.search.residues must be a string.")
    except (AttributeError, TypeError):
        print(f"Warning: Parameter 'qc.search.residues' not found or invalid. Using default for 'residues' ('{default_qc_args.get('residues')}')")
        qc_args['residues'] = default_qc_args.get('residues')

    return qc_args

def get_chalf_default_args():
    """
    Extracts default arguments from the CHalf function definition.
    """
    # This is a bit of a hack to get the defaults without importing the actual CHalf function,
    # assuming CHalf is defined elsewhere and we only have its signature.
    # In a real scenario, you would simply import CHalf and use inspect.signature.
    # For now, let's manually define a dummy CHalf function for introspection.

    signature = inspect.signature(CHalf)
    defaults = {
        param.name: param.default
        for param in signature.parameters.values()
        if param.default is not inspect.Parameter.empty
    }
    return defaults

def prepare_chalf_arguments(params: 'ParameterDict'):
    """
    Extracts CHalf-specific parameters from a ParameterDict and
    fills in missing values with the default arguments from the CHalf function.

    Args:
        params: An instance of ParameterDict containing workflow parameters.

    Returns:
        A dictionary of arguments ready to be passed to the CHalf function
        using the **kwargs syntax.
    """
    chalf_args = {}
    default_chalf_args = get_chalf_default_args()

    # Define the mapping from ParameterDict path to CHalf argument name
    # and retrieve values, applying defaults or transformations
    mappings = {
        'chalf.fitting.outlier_trimming': 'TRIM_OUTLIERS',
        'chalf.fitting.outlier_cutoff': 'OUTLIER_CUTOFF',
        'chalf.fitting.min_pts': 'MINIMUM_PTS',
        'chalf.search.light': 'LIGHT_SEARCH',
        'chalf.experimental.wf.window_fit': 'WINDOW_FIT',
        'chalf.experimental.wf.window': 'nwindow',
        'chalf.experimental.sg.smooth': 'SAVGOL_FIT',
        'chalf.experimental.sg.window': 'SAVGOL_WINDOW',
        'chalf.experimental.sg.order': 'SAVGOL_ORDER',
        'chalf.filter.rsq': 'rsq_cutoff',
        'chalf.filter.ci_value': 'rtr_cutoff',
        'chalf.filter.optimize': 'highest_criteria',
        'chalf.filter.ci_filter': 'HANDLE_CI_UNCERTAINTY',
        'chalf.fitting.zero_criteria': 'zero_criteria',
        'chalf.experimental.ms.mutations': 'CUSTOM_FASTA', # Mapped as per clarification
        'chalf.graphing.graph': 'GRAPH',
        'chalf.graphing.file_type': 'file_type',
        'chalf.graphing.min': 'graph_min',
        'chalf.graphing.max': 'graph_max',
        'chalf.graphing.rsq': 'graph_rsq',
        'chalf.graphing.ci_filter': 'graph_ci_filter',
        'chalf.graphing.ci_value': 'graph_ci_value',
        'chalf.filter.sig_only': 'KEEP_INSIGNIFICANT'
    }

    for param_path, arg_name in mappings.items():
        try:
            # Use a recursive approach to get the nested value or raise AttributeError
            current_value = params
            for part in param_path.split('.'):
                current_value = getattr(current_value, part)
            if arg_name == 'HANDLE_CI_UNCERTAINTY' : current_value = not(current_value) #Handle CI argument has the opposite value of ci_filter
            if arg_name == 'KEEP_INSIGNIFICANT' : current_value = not(current_value) #KEEP_INSIGNIFICANT argument has the opposite value of sig_only
            chalf_args[arg_name] = current_value
        except AttributeError:
            print(f"Warning: Parameter '{param_path}' not found. Using default for '{arg_name}' ('{default_chalf_args.get(arg_name)}')")
            chalf_args[arg_name] = default_chalf_args.get(arg_name)

    # Handle 'search' with conversion
    try:
        search_residues_str = params.chalf.search.residues
        if isinstance(search_residues_str, str):
            chalf_args['search'] = list(search_residues_str.upper())
        else:
            raise TypeError("chalf.search.residues must be a string.")
    except (AttributeError, TypeError):
        print(f"Warning: Parameter 'chalf.search.residues' not found or invalid. Using default for 'search' ('{default_chalf_args.get('search')}')")
        chalf_args['search'] = default_chalf_args.get('search')

    # Handle 'range_cutoff'
    min_val = None
    max_val = None
    try:
        min_val = params.chalf.filter.min
    except AttributeError:
        print("Error: Parameter 'chalf.filter.min' not found for 'range_cutoff'. Using default for 'range_cutoff'.")
    try:
        max_val = params.chalf.filter.max
    except AttributeError:
        print("Error: Parameter 'chalf.filter.max' not found for 'range_cutoff'. Using default for 'range_cutoff'.")

    if min_val is not None and max_val is not None:
        chalf_args['range_cutoff'] = (min_val, max_val)
    else:
        # If either is missing, use the default for range_cutoff
        chalf_args['range_cutoff'] = default_chalf_args.get('range_cutoff')


    # Handle 'INITIAL_GUESS' as a special case
    try:
        # Access directly and if it's False, assign False
        if params.chalf.initial_guess is False:
            chalf_args['INITIAL_GUESS'] = False
        else: # If it exists and is True, or some other truthy value
            chalf_args['INITIAL_GUESS'] = True # Default behavior if present and not False
    except AttributeError:
        # If 'chalf.initial_guess' is not found, default to True
        chalf_args['INITIAL_GUESS'] = True

    return chalf_args

def get_crm_default_args():
    """
    Extracts default arguments from the CombinedResidueMapper function definition.
    Updated to reflect 'advanced_options' instead of 'custom_annotation' and 'subset'.
    """

    signature = inspect.signature(CombinedResidueMapper)
    defaults = {
        param.name: param.default
        for param in signature.parameters.values()
        if param.default is not inspect.Parameter.empty
    }
    return defaults

def prepare_combined_residue_mapper_arguments(params: 'ParameterDict'):
    """
    Extracts CombinedResidueMapper-specific parameters from a ParameterDict and
    fills in missing values with the default arguments from the CombinedResidueMapper function.

    Args:
        params: An instance of ParameterDict containing workflow parameters.

    Returns:
        A dictionary of arguments ready to be passed to the CombinedResidueMapper function
        using the **kwargs syntax.
    """
    crm_args = {}
    default_crm_args = get_crm_default_args()

    # Define the mapping from ParameterDict path to CombinedResidueMapper argument name
    mappings = {
        'visualization.crm.file_type': 'file_type',
        'visualization.crm.trendlines.trendline': 'TRENDLINE',
        'visualization.crm.trendlines.window': 'window_size',
        'visualization.crm.trendlines.min': 'count_requirement',
        'visualization.crm.other.all_curves': 'ALLSITES',
        'visualization.crm.other.reference_stats': 'STATS_REFERENCE',
        'visualization.crm.other.crm_trendline_stats': 'TRENDLINE_STATS',
        'visualization.crm.other.mutation_search': 'CUSTOM_FASTA', # Mapping for CUSTOM_FASTA
        'visualization.crm.other.shared_only': 'SHARED_ONLY',
        'visualization.crm.other.advanced': 'advanced_options'
    }

    for param_path, arg_name in mappings.items():
        try:
            current_value = params
            for part in param_path.split('.'):
                current_value = getattr(current_value, part)
            crm_args[arg_name] = current_value
        except AttributeError:
            print(f"Warning: Parameter '{param_path}' not found. Using default for '{arg_name}' ('{default_crm_args.get(arg_name)}')")
            crm_args[arg_name] = default_crm_args.get(arg_name)

    # Handle 'ylim'
    min_val = None
    max_val = None
    try:
        min_val = params.visualization.crm.min
    except AttributeError:
        print("Error: Parameter 'visualization.crm.min' not found for 'ylim'. Using default for 'ylim'.")
    try:
        max_val = params.visualization.crm.max
    except AttributeError:
        print("Error: Parameter 'visualization.crm.max' not found for 'ylim'. Using default for 'ylim'.")

    if min_val is not None and max_val is not None:
        crm_args['ylim'] = (min_val, max_val)
    else:
        # If either is missing, use the default for ylim
        crm_args['ylim'] = default_crm_args.get('ylim')

    # Handle 'SHARED_ONLY'
    try:
        crm_args['SHARED_ONLY'] = params.visualization.crm.other.shared_only
    except AttributeError:
        print(f"Warning: Parameter 'visualization.crm.other.shared_only' not found. Using default for 'SHARED_ONLY' ('{default_crm_args.get('SHARED_ONLY')}')")
        crm_args['SHARED_ONLY'] = default_crm_args.get('SHARED_ONLY')

    # Handle 'advanced_options' (combining custom_annotation and subset)
    try:
        advanced_val = params.visualization.crm.other.advanced
        if advanced_val == '': # Treat empty string as None
            crm_args['advanced_options'] = None
        else:
            crm_args['advanced_options'] = advanced_val
    except AttributeError:
        print(f"Warning: Parameter 'visualization.crm.other.advanced' not found. Using default for 'advanced_options' ('{default_crm_args.get('advanced_options')}')")
        crm_args['advanced_options'] = default_crm_args.get('advanced_options')


    return crm_args

def get_dm_default_args():
    """
    Extracts default arguments from the DeltaMapper function definition.
    """

    signature = inspect.signature(DeltaMapper)
    defaults = {
        param.name: param.default
        for param in signature.parameters.values()
        if param.default is not inspect.Parameter.empty
    }
    return defaults

def prepare_delta_mapper_arguments(params: 'ParameterDict'):
    """
    Extracts DeltaMapper-specific parameters from a ParameterDict and
    fills in missing values with the default arguments from the DeltaMapper function.

    Args:
        params: An instance of ParameterDict containing workflow parameters.

    Returns:
        A dictionary of arguments ready to be passed to the DeltaMapper function
        using the **kwargs syntax.
    """
    dm_args = {}
    default_dm_args = get_dm_default_args()

    # Define the mapping from ParameterDict path to DeltaMapper argument name
    mappings = {
        'visualization.dm.file_type': 'file_type',
        'visualization.dm.sig_value': 'significance_cutoff',
        'visualization.dm.kde.min_pts': 'n_cutoff',
        'visualization.dm.trendlines.trendline': 'TRENDLINE',
        'visualization.dm.trendlines.window': 'window_size',
        'visualization.dm.trendlines.min': 'count_requirement',
        'visualization.dm.other.all_curves': 'ALLSITES',
        'visualization.dm.other.reference_stats': 'STATS_REFERENCE',
        'visualization.dm.other.dm_trendline_stats': 'TRENDLINE_STATS',
        'visualization.dm.sig_filter': 'significance_cutoff_bool'
        # CUSTOM_FASTA and advanced_options handled separately
    }

    for param_path, arg_name in mappings.items():
        try:
            current_value = params
            for part in param_path.split('.'):
                current_value = getattr(current_value, part)
            dm_args[arg_name] = current_value
        except AttributeError:
            print(f"Warning: Parameter '{param_path}' not found. Using default for '{arg_name}' ('{default_dm_args.get(arg_name)}')")
            dm_args[arg_name] = default_dm_args.get(arg_name)

    # Handle 'ylim'
    min_val = None
    max_val = None
    try:
        min_val = params.visualization.dm.min
    except AttributeError:
        print("Error: Parameter 'visualization.dm.min' not found for 'ylim'. Using default for 'ylim'.")
    try:
        max_val = params.visualization.dm.max
    except AttributeError:
        print("Error: Parameter 'visualization.dm.max' not found for 'ylim'. Using default for 'ylim'.")

    if min_val is not None and max_val is not None:
        dm_args['ylim'] = (min_val, max_val)
    else:
        # If either is missing, use the default for ylim
        dm_args['ylim'] = default_dm_args.get('ylim')

    # Handle 'CUSTOM_FASTA' (no direct mapping in params.workflow for DM)
    # Assuming it might be in a general 'visualization.other.mutation_search' if not specific to DM
    try:
        # Check if 'mutation_search' exists under visualization.dm.other
        if hasattr(params.visualization.dm.other, 'mutation_search'):
            dm_args['CUSTOM_FASTA'] = params.visualization.dm.other.mutation_search
        else:
            # Fallback to a more general visualization.other.mutation_search if it exists
            if hasattr(params.visualization.other, 'mutation_search'):
                dm_args['CUSTOM_FASTA'] = params.visualization.other.mutation_search
            else:
                dm_args['CUSTOM_FASTA'] = default_dm_args.get('CUSTOM_FASTA')
                print(f"Warning: Parameter for 'CUSTOM_FASTA' not found in workflow. Using default ('{default_dm_args.get('CUSTOM_FASTA')}')")
    except AttributeError:
        dm_args['CUSTOM_FASTA'] = default_dm_args.get('CUSTOM_FASTA')
        print(f"Warning: Parameter for 'CUSTOM_FASTA' not found in workflow. Using default ('{default_dm_args.get('CUSTOM_FASTA')}')")


    # Handle 'advanced_options'
    try:
        advanced_val = params.visualization.dm.other.advanced
        if advanced_val == '': # Treat empty string as None
            dm_args['advanced_options'] = None
        else:
            dm_args['advanced_options'] = advanced_val
    except AttributeError:
        print(f"Warning: Parameter 'visualization.dm.other.advanced' not found. Using default for 'advanced_options' ('{default_dm_args.get('advanced_options')}')")
        dm_args['advanced_options'] = default_dm_args.get('advanced_options')

    return dm_args

def get_rm_default_args():
    """
    Extracts default arguments from the ResidueMapper function definition.
    """
    # Dummy ResidueMapper function for introspection
    def ResidueMapper_dummy(file,output_dir,file_type='jpg',ylim=(0,3.6),TRENDLINE=True,window_size=3,count_requirement=5,ALLSITES=True,STATS_REFERENCE=True,TRENDLINE_STATS=False,custom_annotation=None,subset=None,CUSTOM_FASTA=False,advanced_options=None):
        pass

    signature = inspect.signature(ResidueMapper_dummy)
    defaults = {
        param.name: param.default
        for param in signature.parameters.values()
        if param.default is not inspect.Parameter.empty
    }
    return defaults

# --- Modified prepare_residue_mapper_args function ---

def prepare_residue_mapper_args(params: ParameterDict) -> dict:
    """
    Prepares arguments for the ResidueMapper function based on a ParameterDict.
    'file' and 'output_dir' are expected to be handled externally.

    Args:
        params: A ParameterDict instance containing the workflow parameters
                (e.g., loaded from a .workflow file).

    Returns:
        A dictionary of keyword arguments ready to be passed to the ResidueMapper function.
        Returns an empty dictionary if 'visualization.rm' is explicitly set to False
        in the parameters, indicating that ResidueMapper should not be run.
    """
    rm_args = {}
    default_rm_args = get_rm_default_args()

    # Check if the ResidueMapper visualization module is enabled in the parameters.
    # If not, return an empty dictionary, indicating no arguments should be prepared
    # and the module likely shouldn't be executed.
    if not params.get('visualization', {}).get('rm', False):
        print("ResidueMapper visualization is disabled in parameters (visualization.rm = False).")
        return rm_args

    try:
        rm_params = params.visualization.rm

        # Define the mapping from ParameterDict path to ResidueMapper argument name
        mappings = {
            'visualization.rm.file_type': 'file_type',
            'visualization.rm.trendlines.trendline': 'TRENDLINE',
            'visualization.rm.trendlines.window': 'window_size',
            'visualization.rm.trendlines.min': 'count_requirement',
            'visualization.rm.other.all_curves': 'ALLSITES',
            'visualization.rm.other.reference_stats': 'STATS_REFERENCE',
            'visualization.rm.other.rm_trendline_stats': 'TRENDLINE_STATS',
            'visualization.rm.other.mutation_search': 'CUSTOM_FASTA',
        }

        for param_path, arg_name in mappings.items():
            try:
                current_value = params
                for part in param_path.split('.'):
                    current_value = getattr(current_value, part)
                rm_args[arg_name] = current_value
            except AttributeError:
                print(f"Warning: Parameter '{param_path}' not found. Using default for '{arg_name}' ('{default_rm_args.get(arg_name)}')")
                rm_args[arg_name] = default_rm_args.get(arg_name)

        # Handle 'ylim'
        min_val = None
        max_val = None
        try:
            min_val = rm_params.min
        except AttributeError:
            print("Error: Parameter 'visualization.rm.min' not found for 'ylim'. Using default for 'ylim'.")
        try:
            max_val = rm_params.max
        except AttributeError:
            print("Error: Parameter 'visualization.rm.max' not found for 'ylim'. Using default for 'ylim'.")

        if min_val is not None and max_val is not None:
            rm_args['ylim'] = (min_val, max_val)
        else:
            rm_args['ylim'] = default_rm_args.get('ylim')

        # Handle 'advanced_options' (which will be the .ann file path or None)
        ann_file_path = None
        try:
            advanced_val = rm_params.other.advanced
            if advanced_val == '': # Treat empty string as None
                ann_file_path = None
            else:
                ann_file_path = advanced_val
        except AttributeError:
            ann_file_path = None # Not found, so no .ann file path

        rm_args['advanced_options'] = ann_file_path # advanced_options will be the path or None

        # custom_annotation and subset will be handled downstream, so set them to None here
        rm_args['custom_annotation'] = None
        rm_args['subset'] = None

    except AttributeError as e:
        print(f"Warning: A required parameter was missing in the 'visualization.rm' section of the workflow file: {e}.")
        print("ResidueMapper arguments might be incomplete. Please check your .workflow file.")
        traceback.print_exc()
        # Depending on your application's robustness needs, you might raise an error here
        # or fill in more specific defaults.

    return rm_args

def get_cs_default_args():
    """
    Extracts default arguments from a dummy CombinedSite function definition.
    This helps in managing default parameters for the `prepare_combined_site_arguments` function.
    """
    # Define a dummy CombinedSite function with only relevant parameters

    signature = inspect.signature(CombinedSite)
    defaults = {
        param.name: param.default
        for param in signature.parameters.values()
        if param.default is not inspect.Parameter.empty
    }
    return defaults

def prepare_combined_site_arguments(params: 'ParameterDict'):
    """
    Extracts CombinedSite-specific parameters from a ParameterDict, specifically focusing on
    'file_type', 'min', and 'max' from 'visualization.cs', and uses default values for others.

    Args:
        params: An instance of ParameterDict containing workflow parameters,
                typically structured like params.visualization.cs.

    Returns:
        A dictionary of arguments ready to be passed to the CombinedSite function
        using the **kwargs syntax.
    """
    cs_args = {}
    default_cs_args = get_cs_default_args()

    # Initialize with all default arguments for CombinedSite
    cs_args.update(default_cs_args)

    # Override defaults with values explicitly read from workflow file
    # 1. file_type
    file_type_val = params.visualization.cs.file_type
    if file_type_val is not None:
        cs_args['file_type'] = file_type_val

    # 2. ylim (min and max)
    min_val = params.visualization.cs.min
    max_val = params.visualization.cs.max

    if min_val is not None and max_val is not None:
        cs_args['ylim'] = (min_val, max_val)

    return cs_args


def CombinedSite(conditions_dict, output_dir, file_type='jpg', ylim=(0,3.6)):
    """
    Generates boxplots for Label@Accession groups across different conditions,
    using seaborn. It expects '{name} Sites.csv' files as input.

    Args:
        conditions_dict (dict): A dictionary where keys are condition names and values are tuples
                                (file_path, color_is_ignored, class_is_ignored).
                                Example: {'Condition1': ('path/to/Condition1 Sites.csv', 'blue', 'control')}
                                The 'color' and 'class' values in the tuple are ignored.
        output_dir (str): The directory where the output plots and summary CSV will be saved.
        file_type (str): The file format for saving plots (e.g., 'jpg', 'png', 'svg').
        ylim (tuple): A tuple (min, max) for the y-axis limits of the plots.
    """
    print("Checking parameters and aggregating conditions' data for Combined Site plots...")
    conditions_order = [] # To maintain the order of conditions as they appear in the config
    compDF = pd.DataFrame() # DataFrame to hold combined data

    # Validate file_type
    if file_type not in ['jpg', 'png', 'svg']:
        print(f'Unrecognized file type "{file_type}". Selecting .jpg')
        file_type = 'jpg'
    # Ensure output directory exists
    if not os.path.isdir(output_dir):
        print(f'Output directory "{output_dir}" does not exist. Creating it.')
        os.makedirs(output_dir, exist_ok=True)

    # Process each condition and aggregate data
    for condition_name, (file_path, _, _) in conditions_dict.items(): # color and class are ignored
        try:
            df = pd.read_csv(file_path)

            # Define required columns for input CSVs
            required_cols = ['Label@Accession', 'Accession', 'Residue Number', 'CHalf', 'Significant', 'Site Type']
            
            # Check for missing required columns
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                raise KeyError(f"Missing required columns in {file_path}: {', '.join(missing_cols)}")

            df['Condition'] = condition_name
            conditions_order.append(condition_name) # Keep track of original order for plotting

            # Filter data based on 'Significant' and 'Site Type'
            df = df[df['Significant']]
            df = df[df['Site Type'].str.contains('Single')]

            compDF = pd.concat([compDF, df], ignore_index=True)

        except KeyError as e:
            print(f'Input file for {condition_name} does not have the correct columns or format. Error: {e}. Skipping to the next condition.')
            traceback.print_exc()
            if condition_name in conditions_order:
                conditions_order.remove(condition_name)
            continue
        except FileNotFoundError as e:
            print(f'Input file for {condition_name} does not exist. Please check that it has the correct path. Skipping to the next condition.')
            traceback.print_exc()
            if condition_name in conditions_order:
                conditions_order.remove(condition_name)
            continue
        except Exception as e:
            print(f'An unexpected error occurred while processing {condition_name}: {e}. Skipping to the next condition.')
            traceback.print_exc()
            if condition_name in conditions_order:
                conditions_order.remove(condition_name)
            continue

    if compDF.empty or len(conditions_order) < 1:
        print('No valid data or conditions found to generate Combined Site plots. Skipping this step.')
        return

    groups = compDF.groupby(by='Label@Accession')
    total_groups = len(groups)
    count_p = 0
    process_start_time = time.time()

    print(f'Generating {total_groups} Combined Site boxplots...')
    summary_data_rows = [] # To collect data for the output CSV

    for label_accession, group_data in groups:
        progress_logger(
            count_p,
            total_groups,
            description="Combined Site Plotting",
            update_every_n_iterations=max(1, total_groups // 20),
            start_time=process_start_time
        )
        count_p += 1

        # Prepare summary row for CSV
        row_summary = {'Label@Accession': label_accession}
        # Extract Label Type, Label Site, Accession, Residue Number
        parts = label_accession.split('_')
        row_summary['Label Type'] = parts[0] if len(parts) > 0 else np.nan
        row_summary['Label Site'] = parts[1] if len(parts) > 1 else np.nan
        row_summary['Accession'] = '_'.join(parts[2:]) if len(parts) > 2 else np.nan
        row_summary['Residue Number'] = group_data['Residue Number'].iloc[0] if not group_data.empty and 'Residue Number' in group_data.columns else np.nan

        # Generate plot for each Label@Accession group
        plt.close('all') # Close all existing figures to prevent memory issues
        fig, ax = plt.subplots(figsize=(8, 6))

        with sns.axes_style('whitegrid'):
            # Create the boxplot - using hue='Condition' for separate boxes and automatic coloring
            sns.boxplot(data=group_data, x='Condition', y='CHalf', ax=ax,
                        order=conditions_order,
                        showfliers=False, # Do not show outliers in boxplot itself
                        linewidth=1.0)

            # Add individual data points (swarmplot)
            sns.swarmplot(data=group_data, x='Condition', y='CHalf', ax=ax,
                          color='black', size=4, dodge=True, zorder=5) # dodge=True for swarmplot on top of boxplot

            ax.set_xlabel('Condition', fontsize=12, weight='bold')
            ax.set_ylabel('C½ [GdmCl]', fontsize=12, weight='bold')
            ax.tick_params(axis='both', which='major', labelsize=10)
            ax.set_title(label_accession, fontsize=14, weight='bold')
            ax.set_ylim(ylim)

            plt.tight_layout()
            # Sanitize filename to remove invalid characters
            safe_label_accession = re.sub(r'[\\/:*?"<>|]', '_', label_accession)
            output_filepath = os.path.join(output_dir, f'{safe_label_accession} Boxplot.{file_type}')
            plt.savefig(output_filepath, bbox_inches='tight', dpi=300) # Save with higher DPI
            plt.close(fig) # Explicitly close the figure to free memory

            # Populate summary row with statistics for each condition
            for condition in conditions_order:
                cond_subset_df = group_data[group_data['Condition'] == condition]['CHalf'].dropna()
                if not cond_subset_df.empty:
                    row_summary[f'{condition}_CHalf_mean'] = cond_subset_df.mean()
                    row_summary[f'{condition}_CHalf_median'] = cond_subset_df.median()
                    row_summary[f'{condition}_CHalf_std'] = cond_subset_df.std()
                    row_summary[f'{condition}_CHalf_count'] = cond_subset_df.count()
                    row_summary[f'{condition}_CHalf_min'] = cond_subset_df.min()
                    row_summary[f'{condition}_CHalf_max'] = cond_subset_df.max()
                    row_summary[f'{condition}_CHalf_Q1'] = cond_subset_df.quantile(0.25)
                    row_summary[f'{condition}_CHalf_Q3'] = cond_subset_df.quantile(0.75)
                else:
                    # Fill with NaN if no data for this condition and site
                    for stat in ['mean', 'median', 'std', 'count', 'min', 'max', 'Q1', 'Q3']:
                        row_summary[f'{condition}_CHalf_{stat}'] = np.nan
        summary_data_rows.append(row_summary)

    # Generate a summary CSV
    if summary_data_rows:
        summary_df = pd.DataFrame(summary_data_rows)
        # Ensure all columns are present and ordered consistently
        all_condition_stat_cols = []
        for cond in conditions_order:
            for stat in ['mean', 'median', 'std', 'count', 'min', 'max', 'Q1', 'Q3']:
                all_condition_stat_cols.append(f'{cond}_CHalf_{stat}')

        # Define fixed identifier columns
        fixed_identifier_cols = ['Label@Accession', 'Label Type', 'Label Site', 'Accession', 'Residue Number']
        
        # Combine fixed and dynamic columns, ensuring unique and order
        final_cols_ordered = fixed_identifier_cols + [col for col in all_condition_stat_cols if col in summary_df.columns and col not in fixed_identifier_cols]
        
        summary_df = summary_df[final_cols_ordered] # Select and order columns
        summary_df.sort_values(by=['Accession','Residue Number'], inplace=True)
        summary_df.reset_index(drop=True, inplace=True)

        summary_filename = os.path.join(output_dir, f'CombinedSites_Summary.csv')
        summary_df.to_csv(summary_filename, index=False)
        print(f"Combined Site summary saved to: {summary_filename}")
    else:
        print("No data processed for summary CSV. It will not be generated.")

    print("Combined Site plotting complete.")

def main(args):
    params_file = args.workflow
    manifest_file = args.manifest
    vis_config_file = args.visual
    working_dir = args.directory
    if not os.path.isdir(working_dir):
        os.makedirs(working_dir,exist_ok=True)
    params = read_workflow(params_file)
    manifest = read_manifest(manifest_file)
    if args.visual: vis_config = read_vis(vis_config_file, working_dir)
    ''' EXTRACT CHALF RUN PARAMATERS '''
    try:
        CHALF = len(params.chalf) > 1
    except (AttributeError, TypeError):
        CHALF = False
        print('Skipping CHalf step.')
    
    try:
        QC =  len(params.qc) > 1
    except (AttributeError, TypeError):
        QC = False
        print('Skipping Quality Control step.')
    
    try:
        RM = len(params.visualization.rm) > 1
    except (AttributeError, TypeError):
        RM = False
    
    if CHALF:
         chalf_kwargs = prepare_chalf_arguments(params)
         print("[NO_TIMESTAMP]Prepared CHalf Arguments:")
         
         for k, v in chalf_kwargs.items():
             print(f"[NO_TIMESTAMP]      {k}: {v}")
    
    if QC:
        qc_kwargs = prepare_quality_control_arguments(params)
        print("[NO_TIMESTAMP]Prepared Quality Control Arguments:")
        for k, v in qc_kwargs.items():
            print(f"[NO_TIMESTAMP]      {k}: {v}")
    
    if RM:
        rm_kwargs = prepare_residue_mapper_args(params)
        print("[NO_TIMESTAMP]Prepared Quality Control Arguments:")
        for k, v in rm_kwargs.items():
            print(f"[NO_TIMESTAMP]      {k}: {v}")
    
    try:
        QC_REPORT = params.visualization.qc.report
        QC_OPEN = params.visualization.qc.open
    except (AttributeError, TypeError):
        QC_REPORT = False
        QC_OPEN = False
    
    try:
        type(vis_config)
        VIS = True
    except NameError:
        VIS = False
    
    if VIS:
        try:
            CRM = len(params.visualization.crm) > 1
        except (AttributeError, TypeError):
            CRM = False
        try:
            CS = len(params.visualization.cs) > 1
        except (AttributeError, TypeError):
            CS = False
        try:
            DM = len(params.visualization.dm) > 1
        except (AttributeError, TypeError):
            DM = False
        try:
            QC_REPORT = params.visualization.qc.report
            QC_REPORT_OPEN = params.visualization.qc.open
        except (AttributeError, TypeError):
            QC_REPORT = False
            QC_REPORT_OPEN = False
    else:
        CRM = False
        CS = False
        DM = False
        QC_REPORT = False
    
    print('Initializing Run...')
    total_runs = manifest.shape[0]
    for index, row in manifest.iterrows():
        file = row['File (path)']
        condition = row['Condition (unique string)']
        conc_dict = row['conc dict']
        print(f'Processing {condition} ({index+1}/{total_runs}):')
        if CHALF:
            try:
                conDF, sitesDF, concentrations = CHalf(file=file, condition=condition, outdir=working_dir, conc_dict=conc_dict, **chalf_kwargs)
                csDF = CombinedSites(sitesDF=sitesDF, condition=condition, outdir=working_dir, concentrations=concentrations, **chalf_kwargs)
            except Exception as e:
                print(f'Skipping CHalf for {condition}. Error: {e}')
                traceback.print_exc()
        if QC:
            try:
                root = f'{working_dir}/{condition}'
                qcDF = QualityControl(raw_file=file, combined_output_file=f'{root}/{condition}_Combined_OUTPUT.csv', combined_sites_file=f'{root}/{condition} Combined Sites.csv', name=condition, outdir=working_dir, **qc_kwargs)
            except Exception as e:
                print(f'Skipping Quality Control for {condition}. Error: {e}')
                traceback.print_exc()
        if RM:
            try:
                root = f'{working_dir}/{condition}'
                ResidueMapper(file=f'{root}/{condition} Combined Sites.csv', output_dir=f'{root}/Residue Mapper', **rm_kwargs)
            except Exception as e:
                print(f'Skipping Residue Mapper for {condition}. Error: {e}')
                traceback.print_exc()
    
    if VIS:
        print('Performing Group Comparisons...')
        for group in vis_config:
            vis_dir = f'{working_dir}/{group} Comparisons'
            os.makedirs(vis_dir,exist_ok=True)
            if QC_REPORT:
                print('Preparing Quality Control Report...')
                try:
                    conditions_dict = vis_config[group]
                    output_dir = f'{working_dir}/{group} Comparisons'
                    generate_qc_report(conditions_dict=conditions_dict, output_dir=output_dir, open_on_completion=QC_REPORT_OPEN)
                except Exception as e:
                    print(f'Skipping Quality Control Report for {group}. Error: {e}')
                    traceback.print_exc()
            if CRM:
                crm_kwargs = prepare_combined_residue_mapper_arguments(params)
                print("[NO_TIMESTAMP]Prepared Combined Residue Mapper Arguments:")          
                for k, v in crm_kwargs.items():
                    print(f"[NO_TIMESTAMP]      {k}: {v}")  
    
                try:
                    conditions_dict = vis_config[group]
                    output_dir = f'{working_dir}/{group} Comparisons/Combined Residue Mapper'
                    os.makedirs(output_dir,exist_ok=True)
                    CombinedResidueMapper(conditions_dict=conditions_dict, output_dir=output_dir, **crm_kwargs)
                except Exception as e:
                    print(f'Skipping runnning {group} in Combined Residue Mapper. Error: {e}')
                    traceback.print_exc()
            if DM:
                dm_kwargs = prepare_delta_mapper_arguments(params)
                print("[NO_TIMESTAMP]Prepared Delta Mapper Arguments:")
                
                for k, v in dm_kwargs.items():
                    print(f"[NO_TIMESTAMP]      {k}: {v}")  
    
                try:
                    conditions_dict = vis_config[group]
                    output_dir = f'{working_dir}/{group} Comparisons/Delta Mapper'
                    os.makedirs(output_dir,exist_ok=True)
                    DeltaMapper(conditions_dict=conditions_dict, output_dir=output_dir, **dm_kwargs)
                except Exception as e:
                    print(f'Skipping runnning {group} in Delta Mapper. Error: {e}')
                    traceback.print_exc()
            if CS:
                cs_kwargs = prepare_combined_site_arguments(params)
                print("[NO_TIMESTAMP]Prepared Combined Site Arguments:")          
                for k, v in cs_kwargs.items():
                    print(f"[NO_TIMESTAMP]      {k}: {v}")
                try:
                    conditions_dict = vis_config[group]
                    for condition in conditions_dict: #modify for combined site
                        values = conditions_dict[condition]
                        sites = values[0].replace('Combined Sites','Sites')
                        conditions_dict[condition] = (sites,values[1],values[2])
                    output_dir = f'{working_dir}/{group} Comparisons/Combined Site'
                    os.makedirs(output_dir,exist_ok=True)
                    CombinedSite(conditions_dict=conditions_dict, output_dir=output_dir, **cs_kwargs)
                except Exception as e:
                    print(f'Skipping runnning {group} in Delta Mapper. Error: {e}')
                    traceback.print_exc()
    print('Workflow complete.')

parser = argparse.ArgumentParser(description="Calculates protein folding stability from mass spec data.")

# Named parameters
parser.add_argument(
    "-w", "--workflow",
    type=str,
    required=True,
    help="A .worfklow file containing all of the parameters to be used by CHalf."
)
parser.add_argument(
    "-m", "--manifest",
    type=str,
    required=True,
    help="A .manifest file containing the information about the input files to be used by CHalf."
)
parser.add_argument(
    "-v", "--visual",
    type=str,
    required=False, # This is the default, but good for clarity
    help="A .vis file used for specifying the parameters of "
)
parser.add_argument(
    "-d", "--directory",
    type=str,
    required=True,
    help="Working directory for the CHalf project."
)
parser.add_argument(
    "-", "--log",
    type=str,
    required=False, # This is the default, but good for clarity
    help="For outputing a log file if using command line. Accepts a string as the name of the log file that will be saved as a .txt file in the output directory."
)

args = parser.parse_args()
working_dir = args.directory
log_param = args.log

if args.log:
    original_stdout = sys.stdout
    if not os.path.isdir(working_dir):
        os.makedirs(working_dir,exist_ok=True)
    with open(f'{working_dir}/{log_param}.txt', 'w') as f:
        sys.stdout = f
        start = time.time()
        main(args)
        end = time.time()
        total_time_seconds = end - start
        total_minutes = total_time_seconds / 60.0
        message_text = f"CHALF PROCESSES COMPLETED IN {total_minutes:.2f} MINUTES"
        
        # Calculate flanking '=' signs for approximate centering
        # Using 78 as an approximate common terminal width for display
        filler_chars_total = 99 - len(message_text)
        left_filler_len = filler_chars_total // 2
        right_filler_len = filler_chars_total - left_filler_len
        
        final_display_message = f"{'=' * left_filler_len} {message_text} {'=' * right_filler_len}"
        print(final_display_message)
        print('[NO_TIMESTAMP]Please cite:')
        print(citation)
    sys.stdout = original_stdout 
else:
    main(args)
    print('[NO_TIMESTAMP]Please cite:')
    print(citation)

