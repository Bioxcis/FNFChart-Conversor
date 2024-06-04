## Note Converter

Download the executable and convert notes from FNF Vanilla to Psych Engine!

Instructions:
1. Placing your 'charts' files in 'input_file' is optional but comfortable, search for the file to convert on your system if necessary.
2. Placing your 'metadata' files in 'meta_file' is optional but comfortable, search for the file to convert on your system if necessary.
3. The exported data goes to 'output_file' with the song name + difficulty name.
4. For the song, you will have an option to add events to the chart itself to perform on that specific difficulty of the song.
5. The exported events go to 'events_file' with the name 'event' to be executed globally for all song difficulties.

(Avoid having global and specific events in the music folder at the same time to avoid problems, bugs or unwanted actions).

## Programmer
To turn it into an executable use the following prompt:

1. `pip install pyinstaller`
2. `pyinstaller --windowed chartConverter-Psych.py`
