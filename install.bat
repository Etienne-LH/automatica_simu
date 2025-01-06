py -m venv venv
CALL ./venv/Scripts/activate

python.exe -m pip install --upgrade pip

REM Modifier les chemins absolus dans requirements.txt
pip install -r ./requirements.txt

echo Libraries installed :
pip list
