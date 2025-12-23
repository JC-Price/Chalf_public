# Creating a CHalf Executable from Source Files

CHalf is distributed as a compiled executable file to properly manage dependencies, but we recognize that you may want to make edits to CHalf yourself. This can be accomplished by editing ```CHalf_v4_3_UI_production.py``` for GUI changes or ```CHalf_v4_3.py``` for method changes. After editing, however, it is recommended to recompile an executable for ease of distribution. This can be accomplished using an Anaconda environment and PyInstaller. Follow the steps below to accomplish this:

## Compiling CHalf GUI
1. Create conda environment using the command ```conda create --name chalf_gui```.
2. Activate your conda environment using the command ```conda activate chalf_gui```.
3. Install the correct dependencies found in ```gui_requirements.txt``` plus any you may have added using the command ```pip install -r gui_requirements.txt```.
4. Install PyInstaller using the command  ```pip install pyinstaller```.
5. Navigate to the directory containing ```CHalf_v4_3_UI_production.py``` and ensure that the ```images``` folder and ```CHalf Protein Logo.ico``` are present in the same directory.
6. Compile the exe using the command ```pyinstaller CHalf_v4_3_UI_production.py --name CHalf_v4_3 --onefile --windowed --icon "CHalf Protein Logo.ico" --add-data "images;images"```
7. ```CHalf_v4_3.exe``` should now be in the ```dist``` folder. Include it along with the ```images``` folder, a ```core``` folder containing ```CHalf_v4_3_core.py```, a ```workflows``` folder, and a ```concentrations_columns``` folder all in the same directory, and it should be safe to execute.

Full list of commands:
```
conda create --name chalf_gui
conda activate chalf_gui
pip install -r gui_requirements.txt
pip install pyinstaller
python -m PyInstaller chalf_ui.spec
```

## Compiling CHalf Core
1. Create conda environment using the command ```conda create --name chalf_core```.
2. Activate your conda environment using the command ```conda activate chalf_core```.
3. Install the correct dependencies found in ```chalf_requirements.txt``` plus any you may have added using the command ```pip install -r chalf_requirements.txt```.
4. Install PyInstaller using the command  ```pip install pyinstaller```.
5. Navigate to the directory containing ```CHalf_v4_3.py``` and ensure that ```CHalf Protein Logo.ico``` is present in the same directory.
6. Compile the exe using the command ```pyinstaller CHalf_v4_3.py --name CHalf_v4_3_core --onefile --icon "CHalf Protein Logo.ico"```
7. ```CHalf_v4_3_core.exe``` should now be in the ```dist``` folder. Include it inside of a ```core``` folder along with the ```images``` folder, a ```workflows``` folder, a ```concentrations_columns``` folder, and ```CHalf_v4_3.exe``` all in the same directory.

Full list of commands:
```
conda create --name chalf_core
conda activate chalf_core
pip install -r chalf_requirements.txt
pip install pyinstaller
python -m PyInstaller chalf_core.spec
```

For compiling a strictly headless version, you may use the same environment but use this command instead:
```
python -m PyInstaller chalf_headless.spec
```