# Running CHalf in an IDE

CHalf is distributed as a compiled executable file to properly manage dependencies, but we recognize that you may want to make edits to CHalf yourself or may need to run CHalf in a different OS. This can be accomplished by editing ```CHalf_v4_3_UI_.py``` for GUI changes or ```CHalf_v4_3.py``` for method changes. This can be accomplished using an Anaconda environment and your IDE of choice. Follow the steps below to accomplish this:

## Creating the CHalf Environment
1. Create conda environment using the command ```conda create --name chalf```.
2. Activate your conda environment using the command ```conda activate chalf```.
3. Install the correct dependencies found in ```chalf_ide_requirements.txt``` plus any you may have added using the command ```pip install -r chalf_ide_requirements.txt```.
4. Navigate to the directory containing ```CHalf_v4_3_UI.py``` and ensure that the ```images```, ```concentration_columns```, and ```workflows``` folders are present in the same directory.
5. Select the `chalf` conda environment in your IDE of choice, and CHalf should be able to run.