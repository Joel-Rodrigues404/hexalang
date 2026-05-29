# HEXALANG ⚽🔥

> "Aqui o código joga bonito."

O **HexaLang** é uma linguagem inspirada no futebol que transpila arquivos `.hexa` para Python.

Ela transforma código em uma experiência divertida com:

* 🎙️ Narração em voz
* 📢 Sons de torcida
* ⌨️ Efeito máquina de escrever
* 🇧🇷 Sintaxe em português

---

# 📁 Estrutura do Projeto

```txt
HEXALANG/
│
├── audios/                 # Sons usados pelo sistema
│
├── hexa_scripts/           # Scripts .hexa
│   ├── hello.hexa
│   ├── jogo.hexa
│   ├── cervejas.hexa
│   └── ...
│
├── hexa_to_python/         # Python gerado automaticamente
│
├── utils/
│
├── hexalang.py             # Transpilador
├── hexa.bat                # Executor automático
│
└── README.md
```

---

# ⚙️ Requisitos

## Python

O projeto funciona com:

```txt
3.10.x < Python < 3.14.x
```

Baixe em:

https://www.python.org/downloads/

---

# 📦 Instalação das Dependências

O HexaLang usa:

* `pywin32`
* `winsound` (já vem no Windows)

Instale o `pywin32`:

```bash
pip install pywin32
```

---

# 🔊 Instalando Voz em Português

Caso o Windows não tenha voz PT-BR instalada, siga os passos abaixo.

## ✅ Pré-requisitos

* Windows 10 ou 11
* PowerShell como Administrador
* Internet

---

## 🚀 Instalar Voz PT-BR

Abra o **PowerShell como Administrador** e execute:

```powershell
Add-WindowsCapability -Online -Name Language.TextToSpeech~~~pt-BR~0.0.1.0
```

---

## 🔧 Habilitar a voz no SAPI5

Execute os comandos abaixo linha por linha:

```powershell
$source = "HKLM:\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens\MSTTS_V110_ptBR_MariaM"

$dest = "HKLM:\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_ptBR_MariaM"

Copy-Item -Path $source -Destination $dest -Recurse -Force
```

---

## 🧪 Verificar instalação

Na pasta do projeto execute:

```bash
python .\utils\view_windows_language.py
```

Resultado esperado:

```txt
Microsoft Maria - Portuguese (Brazil)
```

---

# ▶️ Como Executar

## 1. Crie um arquivo `.hexa`

Exemplo:

```txt
apita o árbitro

camisa 0 gols

a torcida canta "O jogo começou!"

enquanto gols é menor que 5
    a torcida conta gols
    gols vai mais 1
...

fim de papo
```

Salve como:

```txt
meu_jogo.hexa
```

---

## 2. Execute usando o `hexa.bat`

Dentro da pasta do projeto:

```bash
hexa.bat .\hexa_scripts\meu_jogo.hexa
```

O sistema irá:

1. Transpilar `.hexa` → `.py`
2. Executar o Python automaticamente
3. Narrar o código com voz e sons

---

# ⚠️ Importante

O `hexa.bat` funciona apenas dentro da pasta do projeto.

Se quiser executar manualmente fora dela:

## 1. Transpile

```bash
python hexalang.py arquivo.hexa
```

## 2. Execute o Python gerado

```bash
python arquivo.py
```

---

# 📌 Exemplo Completo

```txt
apita o árbitro

camisa 0 gols

a torcida canta "O jogo começou!"

enquanto gols é menor que 5
    a torcida conta gols
    gols vai mais 1
...

chama o var pra ver se gols é igual a 5
    torcida grita "GOOOOOOOL"

fim de papo
```

---

# 📚 Sintaxe Básica

## 📢 Narrar texto

```txt
a torcida canta "Olá mundo!"
```

---

## 🔢 Criar variável

```txt
camisa 10 gols
```

Resultado:

```python
gols = 10
```

---

## ➕ Somar

```txt
gols vai mais 1
```

---

## ➖ Subtrair

```txt
gols vai menos 1
```

---

## 🔁 Loop

```txt
enquanto gols é menor que 5
```

---

## ❓ Condição

```txt
chama o var pra ver se gols é igual a 5
```

---

## ⌨️ Entrada de usuário

```txt
nome responde a pergunta "Qual seu nome?"
```

---

# 🔊 Sistema de Áudio

A cada saída do código existe uma chance de tocar uma vinheta aleatória.

Os sons ficam em:

```txt
audios/
```

Você pode adicionar novos arquivos `.wav`.

Exemplo:

```txt
audios/meu_audio.wav
```

---

# 🛠️ Como Funciona

```txt
Arquivo .hexa
      ↓
Transpilador Python
      ↓
Arquivo .py gerado
      ↓
Execução
      ↓
Narração + Sons + Texto
```

---

# 📚 Exemplos

## Hello World

```txt
a torcida canta "Olá mundo!"
```

---

## Contador

```txt
camisa 0 contador

enquanto contador é menor que 10
    a torcida conta contador
    contador vai mais 1
...
```

---

## Pergunta para o usuário

```txt
nome responde a pergunta "Qual o seu nome?"

a torcida canta "Olá {nome}"
```

---

