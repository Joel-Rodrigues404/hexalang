import sys
import os

BOILERPLATE = r"""import sys
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
"""

# ===========================================================================
# TRANSPILADOR
# ===========================================================================
def transpile(input_file):
    if not input_file.endswith(".hexa"):
        print("Erro: O arquivo precisa ter a extensao .hexa")
        sys.exit(1)

    output_file = input_file.replace(".hexa", ".py")

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    python_code = [BOILERPLATE]
    loop_depth = 0

    for line in lines:
        stripped = line.strip()
        indent = line[:len(line) - len(line.lstrip())]

        if not stripped:
            continue

        is_break = False
        is_continue = False
        if stripped.endswith("..."):
            is_continue = True
            stripped = stripped[:-3].strip()
        elif stripped.endswith("."):
            is_break = True
            stripped = stripped[:-1].strip()

        if stripped == "apita o árbitro":
            python_code.append(indent + "narrate_and_print('apita o árbitro', 'whistle.wav')")

        elif stripped == "fim de papo":
            python_code.append(indent + "narrate_and_print('fim de papo', 'whistle.wav')")

        elif stripped.startswith("a torcida canta "):
            msg = stripped[len("a torcida canta "):].strip()
            # Se for string literal com aspas, gera f-string para interpolar {vars}
            if (msg.startswith('"') and msg.endswith('"')) or (msg.startswith("'") and msg.endswith("'")):
                inner = msg[1:-1]  # remove as aspas externas
                python_code.append(indent + f'narrate_and_print(f"a torcida canta {inner}")')
            else:
                python_code.append(indent + f"narrate_and_print(f'a torcida canta {{str({msg})}}')")

        elif stripped.startswith("a torcida conta "):
            msg = stripped[len("a torcida conta "):].strip()
            python_code.append(indent + f"narrate_fast(f'{{str({msg})}}')")

        elif stripped.startswith("torcida grita "):
            msg = stripped[len("torcida grita "):].strip()
            python_code.append(indent + f"narrate_and_print(f'torcida grita {{str({msg})}}')")

        elif stripped.startswith("o estadio grita "):
            msg = stripped[len("o estadio grita "):].strip()
            python_code.append(indent + f"narrate_and_print(f'o estadio grita {{str({msg})}}', 'buzina.wav')")

        elif stripped.startswith("camisa ") or stripped.startswith("odd "):
            parts = stripped.split()
            if len(parts) >= 3:
                name = parts[2]
                val  = parts[1]
                python_code.append(indent + f"{name} = {val}")

        elif " é " in stripped and ('"' in stripped or "'" in stripped):
            parts = stripped.split(" é ", 1)
            python_code.append(indent + f"{parts[0].strip()} = {parts[1].strip()}")

        elif stripped.startswith("vamos as opcoes do banco "):
            var_name = stripped[len("vamos as opcoes do banco "):].strip()
            python_code.append(indent + f"match {var_name}:")

        elif stripped.startswith("se entrar o "):
            val = stripped[len("se entrar o "):].rstrip(":").strip()
            python_code.append(indent + f"case {val}:")

        elif stripped.startswith("chama o var pra ver se "):
            cond = stripped[len("chama o var pra ver se "):].strip()
            cond = cond.replace(" é igual a ", " == ")
            python_code.append(indent + f"if {cond}:")

        elif stripped.startswith("enquanto "):
            loop_depth += 1
            cond = stripped[len("enquanto "):].strip()
            cond = (cond
                    .replace(" é igual a ", " == ")
                    .replace(" é maior que ", " > ")
                    .replace(" é menor que ", " < "))
            python_code.append(indent + f"while {cond}:")

        elif " vai mais " in stripped:
            parts = stripped.split(" vai mais ", 1)
            python_code.append(indent + f"{parts[0].strip()} += {parts[1].strip()}")

        elif " vai menos " in stripped:
            parts = stripped.split(" vai menos ", 1)
            python_code.append(indent + f"{parts[0].strip()} -= {parts[1].strip()}")

        if is_break:
            if loop_depth > 0:
                python_code.append(indent + "break")
            loop_depth = max(0, loop_depth - 1)

        if is_continue:
            python_code.append(indent + "continue")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(python_code))

    print(f"VAR confirmou a traducao! Arquivo gerado: {output_file}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python hexalang.py <arquivo.hexa>")
        sys.exit(1)
    transpile(sys.argv[1])