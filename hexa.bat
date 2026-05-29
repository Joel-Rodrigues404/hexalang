@echo off
setlocal

if "%~1" == "" (
    echo [Erro] Forneca um arquivo .hexa para executar.
    echo Exemplo: hexa.bat .\hexa_scripts\jogo.hexa
    exit /b
)

set "ARQUIVO_HEXA=%~1"
set "NOME_SCRIPT=%~n1"
set "ARQUIVO_PY=.\hexa_to_python\%NOME_SCRIPT%.py"

if not exist ".\hexa_to_python\" mkdir ".\hexa_to_python"

if exist "%ARQUIVO_PY%" del "%ARQUIVO_PY%"

echo [HexaLang] Transpilando %ARQUIVO_HEXA%...
python .\hexalang.py "%ARQUIVO_HEXA%"

if not exist "%ARQUIVO_PY%" (
    echo [Erro] O arquivo transpilado "%ARQUIVO_PY%" nao foi encontrado.
    exit /b
)

echo [HexaLang] Executando...
echo ---------------------------------------------------
python "%ARQUIVO_PY%"
echo ---------------------------------------------------

if exist ".\hexa_to_python\" del /q ".\hexa_to_python\*.*"

endlocal