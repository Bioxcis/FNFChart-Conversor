import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox

# Estruturas de dados
songData = {
    'songName': '',
    'songInstVolume': 1,
    'needsVoices': True,
    'stageName': '',
    'validScore': True,
}

gameplayData = {
    'bfTrails': False,
    'gfTrails': False,
    'characterTrails': False,
    'cameraMoveOnNotes': False,
    'swapStrumLines': False,
    'healthdrain': 0,
    'healthdrainKill': False,
    'disableDebugButtons': False,
    'disableAntiMash': False,
    'importEvents': False
}

fileData = {
    'input_file': '',
    'meta_file': '',
    'output_dir': '',
    'diff_name': '',
    'song_strumtime': 0,
    'event_dir': ''
}

import_song_events = True
window_position = None

# Funções
def transform_notes():
    global gameplayData, songData, fileData, import_song_events

    d_map = {
        0: 4, 1: 5, 2: 6, 3: 7,
        4: 0, 5: 1, 6: 2, 7: 3
    }

    with open(fileData['input_file'], 'r') as file_i:
        data = json.load(file_i)

    with open(fileData['meta_file'], 'r') as file_m:
        meta = json.load(file_m)

    for key, value in gameplayData.items():
        if isinstance(value, tk.BooleanVar):
            gameplayData[key] = value.get()

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

    if(gameplayData['importEvents']):
        events = get_events(fileData['input_file'])

    output_data = {
        'song': {
            'player1': player1,
            'player2': player2,
            'gfVersion': player3,
            'events': events,
            'notes': sections,
            'bfTrails': gameplayData['bfTrails'],
            'gfTrails': gameplayData['gfTrails'],
            'characterTrails': gameplayData['characterTrails'],
            'swapStrumLines': gameplayData['swapStrumLines'],
            'cameraMoveOnNotes': gameplayData['cameraMoveOnNotes'],
            'healthdrain': gameplayData['healthdrain'],
            'healthdrainKill': gameplayData['healthdrainKill'],
            'arrowSkin': '',
            'splashSkin': 'noteSplashes',
            'disableDebugButtons': gameplayData['disableDebugButtons'],
            'disableAntiMash': gameplayData['disableAntiMash'],
            'song': songData['songName'],
            'speed': scrollspeed,
            'songInstVolume': songData['songInstVolume'],
            'needsVoices': songData['needsVoices'],
            'mania': 3,
            'bpm': bpm,
            'stage': songData['stageName'],
            'validScore': songData['validScore']
        },
        'generatedBy': 'FNF Chart Conversor - Wumpa Conversor v1.5.1'
    }

    output_file = os.path.join(fileData['output_dir'], f"{songData['songName']}-{fileData['diff_name']}.json")

    os.makedirs(os.path.dirname(output_file), exist_ok = True)

    with open(output_file, 'w') as file:
        json.dump(output_data, file, indent = 4)

    messagebox.showinfo("Sucesso", f"Dados transformados e salvos em '{output_file}'.")


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
            value1 = values.get('char', '')
        elif name == 'ZoomCamera':
            name = 'Set Camera Zoom'
            value1 = values.get('zoom', '')
            value2 = values.get('duration', '')
        elif name == 'SetCameraBop':
            name = 'Change Camera Bop'
            value1 = values.get('intensity', '')
        elif name == 'PlayAnimation':
            name = 'Play Animation'
            value1 = values.get('anim', '')
            value2 = values.get('target', '')

        final_events.append([
            time,
            [
                [
                    name,
                    value1,
                    value2
                ]
            ]
        ])
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

# Dados de Entrada
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

def resetChartValues():
    songData['validScore'] = True
    songData['songName'] = ''
    songData['songInstVolume'] = 1
    songData['needsVoices'] = True
    songData['stageName'] = ''
    songData['validScore'] = True
    gameplayData['bfTrails'] = False
    gameplayData['gfTrails'] = False
    gameplayData['characterTrails'] = False
    gameplayData['cameraMoveOnNotes'] = False
    gameplayData['swapStrumLines'] = False
    gameplayData['healthdrain'] = 0
    gameplayData['healthdrainKill'] = False
    gameplayData['disableDebugButtons'] = False
    gameplayData['disableAntiMash'] = False
    fileData['diff_name'] = ''
    fileData['input_file'] = ''
    fileData['meta_file'] = ''
    fileData['output_dir'] = ''
    fileData['song_strumtime'] = 0

def verifyFilePaths():
    base_dir = os.path.dirname(__file__)
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

# Funções do menu principal
def select_input_file():
    base_dir = os.path.dirname(__file__)
    input_dir = os.path.join(base_dir, 'charts_input')
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
    file_path = filedialog.askopenfilename(initialdir=input_dir, title="Selecionar arquivo de entrada", filetypes=[("JSON files", "*.json")])
    input_entry.delete(0, tk.END)
    input_entry.insert(0, file_path)

def select_meta_file():
    base_dir = os.path.dirname(__file__)
    meta_dir = os.path.join(base_dir, 'charts_meta')
    if not os.path.exists(meta_dir):
        os.makedirs(meta_dir)
    file_path = filedialog.askopenfilename(initialdir=meta_dir, title="Selecionar arquivo de meta", filetypes=[("JSON files", "*.json")])
    meta_entry.delete(0, tk.END)
    meta_entry.insert(0, file_path)

def validate_number(new_value):
    try:
        if new_value == "":
            return True
        value = float(new_value)
        return 0 <= value <= 1
    except ValueError:
        return False

def cancel_menu():
    funkinWindow.destroy()


# Processo
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
def second_process(voices, score):
    global window_position
    song_name = name_entry.get()
    stage_name = stage_entry.get()
    inst_vol_text = vol_entry.get()

    if not song_name or not stage_name or not inst_vol_text:
        messagebox.showerror("Erro", "Há campos não preenchidos!")
        return
    
    inst_vol = float(inst_vol_text)

    songData['songName'] = song_name
    songData['needsVoices'] = voices
    songData['stageName'] = stage_name
    songData['validScore'] = score
    songData['songInstVolume'] = inst_vol

    window_position = (musicDataWindow.winfo_x(), musicDataWindow.winfo_y())
    return True

# 3
def finish_process(bf, dad, gf, swap, kill, debug, ghost, camera, events):
    global window_position, import_song_events
    drainage = drain_entry.get()

    if not drainage:
        messagebox.showerror("Erro", "Há campos não preenchidos!")
        return
    
    drain = float(drainage)

    gameplayData['bfTrails'] = bf
    gameplayData['characterTrails'] = dad
    gameplayData['gfTrails'] = gf
    gameplayData['swapStrumLines'] = swap
    gameplayData['healthdrain'] = drain

    if drain > 0:
        gameplayData['healthdrainKill'] = kill

    gameplayData['disableDebugButtons'] = debug
    gameplayData['disableAntiMash'] = ghost
    gameplayData['cameraMoveOnNotes'] = camera
    gameplayData['importEvents'] = events

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
    funkinWindow.title("Friday Night Chart Converter - Wumpa Engine")
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
        if second_process(needs_voices, validate_score):
            open_assets_window()

    # 3
    def open_assets_window():
        def return_to_second():
            global window_position
            musicAssetsWindow.destroy()
            musicDataWindow.geometry(f"+{window_position[0]}+{window_position[1]}")
            musicDataWindow.deiconify()

        def to_finish_progress():
            finish_process(bf_trails, dad_trails, gf_trails, swap_lines, drain_kill, buttons_debug, ghost_tapping, camera_moves, import_events)

        def validate_drainage(value):
            try:
                if value == "":
                    return True
                val = float(value)
                return 0 <= val
            except ValueError:
                return False

        def check_drainage(*args):
            drain_value = drain_entry.get()
            if drain_value:
                val = float(drain_value)
                if val <= 0:
                    rb_yes.config(state='disabled')
                    rb_no.config(state='disabled')
                else:
                    rb_yes.config(state='normal')
                    rb_no.config(state='normal')
            else:
                rb_yes.config(state='disabled')
                rb_no.config(state='disabled')

        global musicAssetsWindow, drain_entry, window_position

        musicDataWindow.withdraw()
        musicAssetsWindow = tk.Toplevel()
        musicAssetsWindow.title("Friday Night Funkin Converter - Configurações de Jogo")
        musicAssetsWindow.geometry(f"+{window_position[0]}+{window_position[1]}")
        musicAssetsWindow.resizable(width=False, height=False)
        musicAssetsWindow.geometry("630x340")
        vcme = (musicAssetsWindow.register(validate_drainage), '%P')

        bf_trails = tk.BooleanVar()
        tk.Label(musicAssetsWindow, text="Efeito de Rastro no Boyfriend?").grid(row=0, column=0, padx=10, sticky=tk.W)
        tk.Radiobutton(musicAssetsWindow, text="Sim", variable=bf_trails, value=True).grid(row=0, column=1, padx=10, sticky=tk.W)
        tk.Radiobutton(musicAssetsWindow, text="Não", variable=bf_trails, value=False).grid(row=1, column=1, padx=10, sticky=tk.W)

        dad_trails = tk.BooleanVar()
        tk.Label(musicAssetsWindow, text="Efeito de Rastro no Oponente?").grid(row=2, column=0, padx=10, sticky=tk.W)
        tk.Radiobutton(musicAssetsWindow, text="Sim", variable=dad_trails, value=True).grid(row=2, column=1, padx=10, sticky=tk.W)
        tk.Radiobutton(musicAssetsWindow, text="Não", variable=dad_trails, value=False).grid(row=3, column=1, padx=10, sticky=tk.W)

        gf_trails = tk.BooleanVar()
        tk.Label(musicAssetsWindow, text="Efeito de Rastro na Girfriend?").grid(row=4, column=0, padx=10, sticky=tk.W)
        tk.Radiobutton(musicAssetsWindow, text="Sim", variable=gf_trails, value=True).grid(row=4, column=1, padx=10, sticky=tk.W)
        tk.Radiobutton(musicAssetsWindow, text="Não", variable=gf_trails, value=False).grid(row=5, column=1, padx=10, sticky=tk.W)

        swap_lines = tk.BooleanVar()
        tk.Label(musicAssetsWindow, text="Trocar lado das Notas?").grid(row=6, column=0, padx=10, sticky=tk.W)
        tk.Radiobutton(musicAssetsWindow, text="Sim", variable=swap_lines, value=True).grid(row=6, column=1, padx=10, sticky=tk.W)
        tk.Radiobutton(musicAssetsWindow, text="Não", variable=swap_lines, value=False).grid(row=7, column=1, padx=10, sticky=tk.W)

        tk.Label(musicAssetsWindow, text="Drenagem de Vida:").grid(row=8, column=0, padx=10, sticky=tk.W)
        drain_entry = tk.Entry(musicAssetsWindow, width=10, validate='key', validatecommand=vcme)
        drain_entry.grid(row=8, column=1, padx=5, pady=5, sticky=tk.W)
        drain_entry.insert(0, '0')

        drain_entry.bind("<KeyRelease>", check_drainage)
        drain_entry.bind("<FocusOut>", check_drainage)

        drain_kill = tk.BooleanVar()
        tk.Label(musicAssetsWindow, text="Drenagem Mata").grid(row=0, column=2, padx=10, sticky=tk.W)
        rb_yes = tk.Radiobutton(musicAssetsWindow, text="Sim", variable=drain_kill, value=True)
        rb_yes.grid(row=0, column=3, padx=10, sticky=tk.W)
        rb_no = tk.Radiobutton(musicAssetsWindow, text="Não", variable=drain_kill, value=False)
        rb_no.grid(row=1, column=3, padx=10, sticky=tk.W)

        buttons_debug = tk.BooleanVar()
        tk.Label(musicAssetsWindow, text="Desativar Botões Debug?").grid(row=2, column=2, padx=10, sticky=tk.W)
        tk.Radiobutton(musicAssetsWindow, text="Sim", variable=buttons_debug, value=True).grid(row=2, column=3, padx=10, sticky=tk.W)
        tk.Radiobutton(musicAssetsWindow, text="Não", variable=buttons_debug, value=False).grid(row=3, column=3, padx=10, sticky=tk.W)

        ghost_tapping = tk.BooleanVar()
        tk.Label(musicAssetsWindow, text="Desativar Notas Fantasma?").grid(row=4, column=2, padx=10, sticky=tk.W)
        tk.Radiobutton(musicAssetsWindow, text="Sim", variable=ghost_tapping, value=True).grid(row=4, column=3, padx=10, sticky=tk.W)
        tk.Radiobutton(musicAssetsWindow, text="Não", variable=ghost_tapping, value=False).grid(row=5, column=3, padx=10, sticky=tk.W)

        camera_moves = tk.BooleanVar()
        camera_moves.set(True)
        tk.Label(musicAssetsWindow, text="Movimentação da Camera?").grid(row=6, column=2, padx=10, sticky=tk.W)
        tk.Radiobutton(musicAssetsWindow, text="Sim", variable=camera_moves, value=True).grid(row=6, column=3, padx=10, sticky=tk.W)
        tk.Radiobutton(musicAssetsWindow, text="Não", variable=camera_moves, value=False).grid(row=7, column=3, padx=10, sticky=tk.W)

        import_events = tk.BooleanVar()
        import_events.set(True)
        tk.Label(musicAssetsWindow, text="Importar Eventos?").grid(row=8, column=2, padx=10, sticky=tk.W)
        tk.Radiobutton(musicAssetsWindow, text="Sim", variable=import_events, value=True).grid(row=8, column=3, padx=10, sticky=tk.W)
        tk.Radiobutton(musicAssetsWindow, text="Não", variable=import_events, value=False).grid(row=9, column=3, padx=10, sticky=tk.W)

        tk.Button(musicAssetsWindow, text="Voltar", command=return_to_second).grid(row=10, column=0, padx=20, pady=20, sticky=tk.W)
        tk.Button(musicAssetsWindow, text="Finalizar Conversão", command=to_finish_progress).grid(row=10, column=1, pady=20, sticky=tk.W)

        check_drainage()

        musicAssetsWindow.protocol("WM_DELETE_WINDOW", return_to_second)

    # 2
    global musicDataWindow, name_entry, stage_entry, vol_entry, window_position

    funkinWindow.withdraw()
    musicDataWindow = tk.Toplevel()
    musicDataWindow.title("Friday Night Chart Converter - Dados da Música")
    musicDataWindow.geometry(f"+{window_position[0]}+{window_position[1]}")
    musicDataWindow.resizable(width=False, height=False)
    musicDataWindow.geometry("480x255")
    vcmd = (musicDataWindow.register(validate_number), '%P')

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

    validate_score = tk.BooleanVar()
    validate_score.set(True)
    tk.Label(musicDataWindow, text="Validar Pontuação?").grid(row=4, column=0, padx=10, sticky=tk.W)
    tk.Radiobutton(musicDataWindow, text="Sim", variable=validate_score, value=True).grid(row=4, column=1, padx=10, sticky=tk.W)
    tk.Radiobutton(musicDataWindow, text="Não", variable=validate_score, value=False).grid(row=5, column=1, padx=10, sticky=tk.W)

    tk.Label(musicDataWindow, text="Volume Instrumental:").grid(row=6, column=0, padx=10, sticky=tk.W)
    vol_entry = tk.Entry(musicDataWindow, width=40, validate='key', validatecommand=vcmd)
    vol_entry.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)
    vol_entry.insert(0, '1.0')

    tk.Button(musicDataWindow, text="Voltar", command=return_to_main).grid(row=7, column=0, padx=20, pady=20, sticky=tk.W)
    tk.Button(musicDataWindow, text="Salvar Informações", command=to_third_page).grid(row=7, column=1, padx=30, pady=20, sticky=tk.W)

    musicDataWindow.protocol("WM_DELETE_WINDOW", return_to_main)


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