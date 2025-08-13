# Creating a FragToCHalf Executable from Source Files

FragToCHalf is distributed as a compiled executable file to properly manage dependencies, but we recognize that you may want to make edits to it yourself. This can be accomplished by editing ```frag_to_chalf_UI.py```. After editing, however, it is recommended to recompile an executable for ease of distribution. This can be accomplished using an Anaconda environment and PyInstaller. Follow the steps below to accomplish this:

## Compiling frag_to_chalf
1. Create conda environment using the command ```conda create --name frag_to_chalf```.
2. Activate your conda environment using the command ```conda activate frag_to_chalf```.
3. Install the correct dependencies found in ```frag_to_chalf_requirements.txt``` plus any you may have added using the command ```pip install -r frag_to_chalf_requirements.txt```.
4. Install PyInstaller using the command  ```pip install pyinstaller```.
5. Navigate to the directory containing ```frag_to_chalf_UI.py```.
6. Compile the exe using the command ```pyinstaller frag_to_chalf_UI.py --name FragToCHalf --onefile --windowed --icon "frag_to_chalf_logo.ico" --add-data "images;images"```
7. ```FragToCHalf.exe``` should now be in the ```dist``` folder. Include it along with a ```workflows``` folder outside of the ```fragpipe``` directory.

Full list of commands:
```
conda create --name frag_to_chalf
conda activate frag_to_chalf
pip install -r frag_to_chalf_requirements.txt
pip install pyinstaller
pyinstaller frag_to_chalf_UI.py --name FragToCHalf --onefile --windowed --icon "frag_to_chalf_logo.ico" --add-data "images;images"
```