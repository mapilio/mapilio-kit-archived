
echo " __  __    _    ____ ___ _     ___ ___      _  _____ _____"
echo "|  \/  |  / \  |  _ \_ _| |   |_ _/ _ \    | |/ /_ _|_   _|"
echo "| |\/| | / _ \ | |_) | || |    | | | | |   | ' / | |  | |  "
echo "| |  | |/ ___ \|  __/| || |___ | | |_| |   | . \ | |  | |  "
echo "|_|  |_/_/   \_\_|  |___|_____|___\___/    |_|\_\___| |_|  "

python3 -m venv mapilio_venv
source mapilio_venv/bin/activate
python setup.py install --force > /dev/null
mapilio_kit --version

echo "Installation has completed"

mapilio_kit authenticate