import json
import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox

# Estruturas de dados
songData = {
    'songName': '',
    'stageName': '',
    'needsVoices': True,
    'importEvents': False,
    'gameOverLoop': '',
    'gameOverSound': '',
    'gameOverChar': '',
    'gameOverEnd': '',
}

fileData = {
    'input_file': '',
    'meta_file': '',
    'output_dir': '',
    'diff_name': '',
    'song_strumtime': 0,
    'event_dir': ''
}

window_position = None

## Conversor
def transform_notes():
    global songData, fileData

    d_map = {
        0: 4, 1: 5, 2: 6, 3: 7,
        4: 0, 5: 1, 6: 2, 7: 3
    }

    with open(fileData['input_file'], 'r') as file_i:
        data = json.load(file_i)

    with open(fileData['meta_file'], 'r') as file_m:
        meta = json.load(file_m)

    for key, value in songData.items():
        if isinstance(value, tk.BooleanVar):
            songData[key] = value.get()
    
    notes = data.get('notes', {}).get(fileData['diff_name'], [])
    scrollspeed = data['scrollSpeed'][fileData['diff_name']]
    player1 = meta['playData']['characters']['player']
    player2 = meta['playData']['characters']['opponent']
    player3 = meta['playData']['characters']['girlfriend']
    bpm = meta['timeChanges'][0]['bpm']

    events = []
    sections = []
    current_section = []
    current_limit = fileData['song_strumtime']

    for note in notes:
        t = note['t']
        d = note['d']
        d = d_map.get(note['d'], note['d'])
        l = note.get('l', 0)
        k = note.get('k', '')
        
        if t >= current_limit:
            sections.append({
                "lengthInSteps": 16,
                "sectionNotes": current_section,
                "mustHitSection": False
            })

            current_section = []
            current_limit += fileData['song_strumtime']

        current_section.append([t, d, l, k])

    sections.append({
        "lengthInSteps": 16,
        "sectionNotes": current_section,
        "mustHitSection": False
    })

    if(songData['importEvents']):
        events = get_events(fileData['input_file'])

    output_data = {
        'song': {
            'events': events,
            'notes': sections,
            'player1': player1,
            'player2': player2,
            'player3': None,
            'gfVersion': player3,
            'song': songData['songName'],
            'stage': songData['stageName'],
            'needsVoices': songData['needsVoices'],
            'bpm': bpm,
            'speed': scrollspeed,
            'gameOverSound': songData['gameOverSound'],
            'gameOverChar': songData['gameOverChar'],
            'gameOverLoop': songData['gameOverLoop'],
            'gameOverEnd': songData['gameOverEnd'],
            'arrowSkin': '',
            'splashSkin': 'noteSplashes',
        },
        'generatedBy': 'FNF Chart Conversor - Psych Conversor v0.7.3'
    }

    output_file = os.path.join(fileData['output_dir'], f"{songData['songName']}-{fileData['diff_name']}.json")

    os.makedirs(os.path.dirname(output_file), exist_ok = True)

    with open(output_file, 'w') as file:
        json.dump(output_data, file, indent = 4)

    messagebox.showinfo("Sucesso", f"Dados transformados e salvos em '{output_file}'.")


## Eventos
def get_events(input_file):
    final_events = []

    with open(input_file, 'r') as file_i:
        data = json.load(file_i)

    events = data['events']

    for event in events:
        value1 = ''
        value2 = ''

        time = event['t']
        name = event['e']
        values = event['v']

        if name == 'FocusCamera':
            name = 'Focus Camera'
            tp = type(values)
            if tp == int:
                value1 = values
            elif tp == dict:
                value1 = values.get('char', '0')

        elif name == 'ZoomCamera':
            name = 'Set Camera Zoom'
            value1 = values.get('zoom', '0.7')
            value2 = values.get('duration', '2')

        elif name == 'SetCameraBop':
            name = 'Change Camera Bop'
            value1 = values.get('intensity', '1')

        elif name == 'PlayAnimation':
            name = 'Play Animation'
            value1 = values.get('anim', 'hey')
            value2 = values.get('target', 'bf')

        final_events.append([
            time,
            [
                [
                    name,
                    str(value1),
                    str(value2)
                ]
            ]
        ])

        # if name == 'PlayAnimation':
        #     name = 'Play Animation'
        #     value1 = values.get('anim', 'hey')
        #     value2 = values.get('target', 'bf')

        # if name != 'FocusCamera' and name != 'SetCameraBop' and name != 'ZoomCamera':
        #     final_events.append([
        #         time,
        #         [
        #             [
        #                 name,
        #                 str(value1),
        #                 str(value2)
        #             ]
        #         ]
        #     ])
    return final_events

def export_events():
    global fileData

    events = get_events(fileData['input_file'])

    output_data = {
        "events": events
    }

    output_file = os.path.join(fileData['event_dir'], "events.json")

    os.makedirs(os.path.dirname(output_file), exist_ok = True)

    with open(output_file, 'w') as file:
        json.dump(output_data, file, indent = 4)

    messagebox.showinfo("Sucesso", f"Arquivo de eventos exportado em '{output_file}'.")


## Dados de Entrada
def musicBPM_exists(meta_file):
    with open(meta_file, 'r') as file:
        data = json.load(file)

    if 'timeChanges' in data:
        if isinstance(data['timeChanges'], list) and len(data['timeChanges']) > 0:
            if 'bpm' in data['timeChanges'][0]:
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def difficultyExists(input, diff):
    with open(input, 'r') as file:
        data = json.load(file)

    if 'notes' in data:
        if isinstance(data['notes'], dict):
            if diff in data['notes']:
                if isinstance(data['notes'][diff], list):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False

def get_musicBPM(meta_file):
    with open(meta_file, 'r') as file:
        data = json.load(file)
    bpm = data['timeChanges'][0]['bpm']
    return float(bpm)

def getStrumTime(bpm):
    timePerBeat = (60 * 1000) / bpm
    timePerSection = 4 * timePerBeat
    return timePerSection

def get_song_name():
    with open(fileData['meta_file'], 'r') as file:
        meta = json.load(file)
    return meta['songName']

def get_song_stage():
    with open(fileData['meta_file'], 'r') as file:
        meta = json.load(file)
    return meta['playData']['stage']


## Redefinir variaveis
def resetChartValues():
    songData['songName'] = ''
    songData['stageName'] = ''
    songData['needsVoices'] = True
    songData['importEvents'] = False
    songData['gameOverChar'] = ''
    songData['gameOverEnd'] = ''
    songData['gameOverLoop'] = ''
    songData['gameOverSound'] = ''

    fileData['diff_name'] = ''
    fileData['input_file'] = ''
    fileData['meta_file'] = ''
    fileData['output_dir'] = ''
    fileData['song_strumtime'] = 0
 

## Caminhos
def verifyFilePaths():
    #base_dir = os.path.dirname(__file__)
    base_dir = get_executable_dir()
    input_dir = os.path.join(base_dir, 'charts_input')
    meta_dir = os.path.join(base_dir, 'charts_meta')
    output_dir = os.path.join(base_dir, 'charts_output')
    event_dir = os.path.join(base_dir, 'events_output')

    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if not os.path.exists(meta_dir):
        os.makedirs(meta_dir)
    if not os.path.exists(event_dir):
        os.makedirs(event_dir)

    fileData['output_dir'] = output_dir
    fileData['event_dir'] = event_dir

def get_executable_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))


## Funções do menu principal
def select_input_file():
    base_dir = get_executable_dir()
    input_dir = os.path.join(base_dir, 'charts_input')
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
    file_path = filedialog.askopenfilename(initialdir=input_dir, title="Selecionar arquivo de entrada", filetypes=[("JSON files", "*.json")])
    input_entry.delete(0, tk.END)
    input_entry.insert(0, file_path)

def select_meta_file():
    base_dir = get_executable_dir()
    meta_dir = os.path.join(base_dir, 'charts_meta')
    if not os.path.exists(meta_dir):
        os.makedirs(meta_dir)
    file_path = filedialog.askopenfilename(initialdir=meta_dir, title="Selecionar arquivo de meta", filetypes=[("JSON files", "*.json")])
    meta_entry.delete(0, tk.END)
    meta_entry.insert(0, file_path)

def cancel_menu():
    funkinWindow.destroy()


# Processos
# 1
def first_process():
    global window_position
    input = input_entry.get()
    meta = meta_entry.get()
    diff = diff_entry.get()

    if not input or not meta or not diff:
        messagebox.showerror("Erro", "Há campos não preenchidos!")
        return

    if not os.path.exists(input):
        messagebox.showerror("Erro", f"Arquivo '{input}' não existe!")
        return

    if not os.path.exists(meta):
        messagebox.showerror("Erro", f"Arquivo '{meta}' não existe!")
        return

    if not musicBPM_exists(meta):
        messagebox.showerror("Erro", "Problema ao obter o BPM dos dados!")
        return

    bpm_value = get_musicBPM(meta)
    song_strumtime = getStrumTime(bpm_value)

    if not difficultyExists(input, diff):
        messagebox.showerror("Erro", f"Problema ao obter os dados da dificuldade {diff}!")
        return

    fileData['input_file'] = input
    fileData['meta_file'] = meta
    fileData['diff_name'] = diff
    fileData['song_strumtime'] = song_strumtime

    window_position = (funkinWindow.winfo_x(), funkinWindow.winfo_y())

    open_music_window()

# 2
def second_process(voices):
    global window_position
    song_name = name_entry.get()
    stage_name = stage_entry.get()

    if not song_name or not stage_name:
        messagebox.showerror("Erro", "Há campos não preenchidos!")
        return

    songData['songName'] = song_name
    songData['needsVoices'] = voices
    songData['stageName'] = stage_name

    window_position = (musicDataWindow.winfo_x(), musicDataWindow.winfo_y())
    return True

# 3
def finish_process(events):
    global window_position, loop_entry, end_entry, char_entry, sound_entry
    sound = char_entry.get()
    char = char_entry.get()
    loop = char_entry.get()
    end = char_entry.get()

    songData['importEvents'] = events
    songData['gameOverSound'] = sound
    songData['gameOverChar'] = char
    songData['gameOverLoop'] = loop
    songData['gameOverEnd'] = end

    window_position = (musicAssetsWindow.winfo_x(), musicAssetsWindow.winfo_y())

    transform_notes()
    resetChartValues()
    finalize_process()

# 4
def event_process():
    input = input_entry.get()
    if not input:
        messagebox.showerror("Erro", "Há campos não preenchidos!")
        return
    if not os.path.exists(input):
        messagebox.showerror("Erro", f"Arquivo '{input}' não existe!")
        return
    fileData['input_file'] = input
    export_events()

# Interfaces
# 1
def open_main_window():
    global funkinWindow, input_entry, meta_entry, diff_entry

    verifyFilePaths()

    funkinWindow = tk.Tk()
    funkinWindow.title("Friday Night Chart Converter - Psych Engine")
    funkinWindow.resizable(width=False, height=False)
    funkinWindow.geometry("585x170")

    tk.Label(funkinWindow, text="Arquivo de Entrada:").grid(row=0, column=0, padx=10, sticky=tk.W)
    input_entry = tk.Entry(funkinWindow, width=50)
    input_entry.grid(row=0, column=1, padx=5, pady=5)
    tk.Button(funkinWindow, text="Buscar", command=select_input_file).grid(row=0, column=2, padx=5, pady=5)

    tk.Label(funkinWindow, text="Arquivo de Metadados:").grid(row=1, column=0, padx=10, sticky=tk.W)
    meta_entry = tk.Entry(funkinWindow, width=50)
    meta_entry.grid(row=1, column=1, padx=5, pady=5)
    tk.Button(funkinWindow, text="Buscar", command=select_meta_file).grid(row=1, column=2, padx=5, pady=5)

    tk.Label(funkinWindow, text="Dificuldade:").grid(row=2, column=0, padx=10, pady=20, sticky=tk.W)
    diff_entry = tk.Entry(funkinWindow, width=30)
    diff_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
    diff_entry.insert(0, 'normal')

    tk.Button(funkinWindow, text="Exportar Eventos", command=event_process).grid(row=3, column=0, padx=10, sticky=tk.W)
    tk.Button(funkinWindow, text="Converter Chart", command=first_process).grid(row=3, column=1, padx=40, sticky=tk.W)
    tk.Button(funkinWindow, text="Sair", width=6, command=cancel_menu).grid(row=3, column=2, sticky=tk.W)

# 2
def open_music_window():
    def return_to_main():
        global window_position
        musicDataWindow.destroy()
        funkinWindow.geometry(f"+{window_position[0]}+{window_position[1]}")
        funkinWindow.deiconify()

    def to_third_page():
        if second_process(needs_voices):
            open_assets_window()

    # 3
    def open_assets_window():
        def return_to_second():
            global window_position
            musicAssetsWindow.destroy()
            musicDataWindow.geometry(f"+{window_position[0]}+{window_position[1]}")
            musicDataWindow.deiconify()

        def to_finish_progress():
            finish_process(import_events)

        global musicAssetsWindow, window_position, loop_entry, end_entry, char_entry, sound_entry

        musicDataWindow.withdraw()
        musicAssetsWindow = tk.Toplevel()
        musicAssetsWindow.title("Friday Night Funkin Converter - Configurações")
        musicAssetsWindow.geometry(f"+{window_position[0]}+{window_position[1]}")
        musicAssetsWindow.resizable(width=False, height=False)
        musicAssetsWindow.geometry("460x255")

        tk.Label(musicAssetsWindow, text="Dados Game Over:").grid(row=0, column=0, padx=10, sticky=tk.W)
        tk.Label(musicAssetsWindow, text="(Permite campos vazios)").grid(row=0, column=1, sticky=tk.W)

        tk.Label(musicAssetsWindow, text="Música em Loop:").grid(row=1, column=0, padx=10, sticky=tk.W)
        loop_entry = tk.Entry(musicAssetsWindow, width=40)
        loop_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(musicAssetsWindow, text="Música Final:").grid(row=2, column=0, padx=10, sticky=tk.W)
        end_entry = tk.Entry(musicAssetsWindow, width=40)
        end_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(musicAssetsWindow, text="Personagem:").grid(row=3, column=0, padx=10, sticky=tk.W)
        char_entry = tk.Entry(musicAssetsWindow, width=40)
        char_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(musicAssetsWindow, text="Som de Morte:").grid(row=4, column=0, padx=10, sticky=tk.W)
        sound_entry = tk.Entry(musicAssetsWindow, width=40)
        sound_entry.grid(row=4, column=1, padx=5, pady=5)

        separator_frame = tk.Frame(musicAssetsWindow)
        separator_frame.grid(row=5, column=0, columnspan=4, pady=(20, 0))
        
        import_events = tk.BooleanVar()
        import_events.set(True)
        tk.Label(musicAssetsWindow, text="Importar Eventos?").grid(row=6, column=0, padx=10, sticky=tk.W)
        tk.Radiobutton(musicAssetsWindow, text="Sim", variable=import_events, value=True).grid(row=6, column=1, padx=10, sticky=tk.W)
        tk.Radiobutton(musicAssetsWindow, text="Não", variable=import_events, value=False).grid(row=7, column=1, padx=10, sticky=tk.W)

        tk.Button(musicAssetsWindow, text="Voltar", command=return_to_second).grid(row=8, column=0, padx=20, pady=15, sticky=tk.W)
        tk.Button(musicAssetsWindow, text="Finalizar Conversão", command=to_finish_progress).grid(row=8, column=1, pady=15, sticky=tk.W)

        musicAssetsWindow.protocol("WM_DELETE_WINDOW", return_to_second)

    # 2
    global musicDataWindow, name_entry, stage_entry, window_position

    funkinWindow.withdraw()
    musicDataWindow = tk.Toplevel()
    musicDataWindow.title("Friday Night Chart Converter - Dados da Música")
    musicDataWindow.geometry(f"+{window_position[0]}+{window_position[1]}")
    musicDataWindow.resizable(width=False, height=False)
    musicDataWindow.geometry("470x170")

    tk.Label(musicDataWindow, text="Nome da Música:").grid(row=0, column=0, padx=10, sticky=tk.W)
    name_entry = tk.Entry(musicDataWindow, width=40)
    name_entry.grid(row=0, column=1, padx=5, pady=5)
    name = get_song_name()
    name_entry.insert(0, name)

    tk.Label(musicDataWindow, text="Nome do Estágio:").grid(row=1, column=0, padx=10, sticky=tk.W)
    stage_entry = tk.Entry(musicDataWindow, width=40)
    stage_entry.grid(row=1, column=1, padx=5, pady=5)
    stage = get_song_stage()
    stage_entry.insert(0, stage)

    needs_voices = tk.BooleanVar()
    needs_voices.set(True)
    tk.Label(musicDataWindow, text="Precisa de Vozes?").grid(row=2, column=0, padx=10, sticky=tk.W)
    tk.Radiobutton(musicDataWindow, text="Sim", variable=needs_voices, value=True).grid(row=2, column=1, padx=10, sticky=tk.W)
    tk.Radiobutton(musicDataWindow, text="Não", variable=needs_voices, value=False).grid(row=3, column=1, padx=10, sticky=tk.W)

    tk.Button(musicDataWindow, text="Voltar", command=return_to_main).grid(row=7, column=0, padx=20, pady=20, sticky=tk.W)
    tk.Button(musicDataWindow, text="Salvar Informações", command=to_third_page).grid(row=7, column=1, padx=30, pady=20, sticky=tk.W)

    musicDataWindow.protocol("WM_DELETE_WINDOW", return_to_main)


## Processos finais
def finalize_process():
    musicAssetsWindow.destroy()
    musicDataWindow.destroy()
    reset_fields()
    funkinWindow.geometry(f"+{window_position[0]}+{window_position[1]}")
    funkinWindow.deiconify()

def reset_fields():
    input_entry.delete(0, tk.END)
    meta_entry.delete(0, tk.END)

##################### ###################### #####################
##################### FRIDAY NIGHT CONVERTER #####################
##################### ###################### #####################

def main():
    open_main_window()
    funkinWindow.mainloop()

if __name__ == "__main__":
    main()