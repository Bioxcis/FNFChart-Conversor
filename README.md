## Note Converter

Download the executable and convert notes from FNF Vanilla to Psych Engine!

Instructions:
1. Placing your 'charts' files in 'input_file' is optional but comfortable, search for the file to convert on your system if necessary.
2. Placing your 'metadata' files in 'meta_file' is optional but comfortable, search for the file to convert on your system if necessary.
3. The exported data goes to 'output_file' with the song name + difficulty name.
4. For the song, you will have an option to add events to the chart itself to perform on that specific difficulty of the song.
5. The exported events go to 'events_file' with the name 'event' to be executed globally for all song difficulties.
* (Avoid having global and specific events in the music folder at the same time to avoid problems, bugs or unwanted actions).

In the future I intend to fix this and other possible problems, in addition to updating if necessary.

If you want to help or have a better solution for this, feel free to contribute.



## Programmers

You must have Python installed on your machine. Check with: `python --version`;

For a virtual environment:
1. Create: `python -m venv venv`;
2. Use: Windows - `.\venv\Scripts\activate` MacOS/Linux - `source venv/bin/activate`;

Dependences:
1. Upgrade pip: `python -m pip install --upgrade pip`;
2. Nuitka: `python -m pip install nuitka`;
3. Compile: `nuitka --standalone --disable-console --enable-plugin=tk-inter --windows-icon-from-ico=chart.ico --include-data-file=chart.ico=chart.ico --include-data-dir=charts_input=charts_input --include-data-dir=charts_meta=charts_meta chartConverter-Psych.py`;
4. To change the external app icon using `.png` use: `python -m pip install imageio`;
5. If you prefer to install the dependencies globally, remove `python -m` from items 1, 2 and 4;

Final result: a folder with the final name `.dist`.

### ------------------------------------------------------------
# Made as a hobby and learning.
