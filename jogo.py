import sys
import time
import os
import wave
import array
import random
import threading
import subprocess
import json
import winsound
import pygame

# ---------------------------------------------------------------------------
# pygame — só pra inicializar o display, não usado para áudio
# ---------------------------------------------------------------------------
pygame.init()

# ---------------------------------------------------------------------------
# Lista de SFX disponíveis
# ---------------------------------------------------------------------------
SFX_FILES = [
    "audios/whistle.wav",
    "audios/whistle2.wav",
    "audios/whistle3.wav",
    "audios/whistle4.wav",
    "audios/whistle5.wav",
    "audios/whistle6.wav",
    "audios/whistle7.wav",
    "audios/whistle8.wav",
    "audios/whistle9.wav",
    "audios/whistle10.wav",
]

# ---------------------------------------------------------------------------
# TTS via subprocesso isolado (win32com SAPI5)
# ---------------------------------------------------------------------------
def _speak_subprocess(text: str):
    script = (
        "import win32com.client;"
        "s = win32com.client.Dispatch('SAPI.SpVoice');"
        f"s.Speak({json.dumps(str(text))});"
    )
    try:
        subprocess.run(
            [sys.executable, "-c", script],
            timeout=60,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
    except Exception:
        pass

# ---------------------------------------------------------------------------
# Chance de 10% de soltar uma vinheta de um time aleatório a cada saída
# ---------------------------------------------------------------------------
def _play_sfx_worker(sound_path: str):
    candidates = [f for f in SFX_FILES if os.path.exists(f)]
    if not candidates:
        if sound_path and os.path.exists(sound_path):
            candidates = [sound_path]
        else:
            return

    chosen = random.choice(candidates)
    try:
        # SND_FILENAME | SND_ASYNC = toca sem bloquear a thread
        winsound.PlaySound(chosen, winsound.SND_FILENAME | winsound.SND_ASYNC)
    except Exception:
        pass

def play_sfx(sound_path: str = None):
    if random.random() > 0.3:   # 30% de chance
        return
    # Roda em thread separada para não bloquear o fluxo principal
    t = threading.Thread(target=_play_sfx_worker, args=(sound_path,), daemon=False)
    t.start()

# ---------------------------------------------------------------------------
# narrate_fast — versão rápida para contagens (a torcida conta)
# ---------------------------------------------------------------------------
def _speak_fast_subprocess(text: str):
    script = (
        "import win32com.client;"
        "s = win32com.client.Dispatch('SAPI.SpVoice');"
        "s.Rate = 9;"
        f"s.Speak({json.dumps(str(text))});"
    )
    try:
        subprocess.run(
            [sys.executable, "-c", script],
            timeout=60,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
    except Exception:
        pass

def narrate_fast(text: str):
    clean_text = str(text).replace('\n', ' ')

    tts_thread = threading.Thread(
        target=_speak_fast_subprocess,
        args=(clean_text,),
        daemon=False
    )
    tts_thread.start()

    # SFX com 10% de chance, igual ao narrate_and_print
    play_sfx()

    # Typewriter ultrarrápido
    typewriter_print(text, delay=0.005)

    tts_thread.join()


def typewriter_print(text: str, delay: float = 0.04):
    for char in str(text):
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# ---------------------------------------------------------------------------
# narrate_and_print — sfx + typewriter + TTS todos em paralelo
# ---------------------------------------------------------------------------
def narrate_and_print(text: str, sfx_file: str = None):
    clean_text = str(text).replace('\n', ' ')

    # TTS em thread separada
    tts_thread = threading.Thread(
        target=_speak_subprocess,
        args=(clean_text,),
        daemon=False
    )
    tts_thread.start()

    # SFX sorteado a cada saída (10% de chance, arquivo aleatório)
    play_sfx(sfx_file)

    # Typewriter na thread principal
    typewriter_print(text)

    # Espera TTS terminar antes de avançar
    tts_thread.join()

narrate_and_print('apita o árbitro', 'whistle.wav')
tempo = 3
narrate_and_print(f"a torcida canta Preparando para a cobranca de falta...")
while tempo > 0:
    match tempo:
        case 3:
            narrate_and_print(f"a torcida canta Autorizou o juiz!")
        case 2:
            narrate_and_print(f"a torcida canta Ele corre pra bola...")
        case 1:
            narrate_and_print(f"a torcida canta Bateu direto pro gol!")
    tempo -= 1
    break
narrate_and_print(f'o estadio grita {str("GOOOOOOOOOOOL!")}', 'buzina.wav')
narrate_and_print('fim de papo', 'whistle.wav')