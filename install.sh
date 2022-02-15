cd ~
python3 -m venv mapilio_venv
source mapilio_venv/bin/activate
python setup.py install --force
mapilio_kit --version

echo "Installation has completed"

mapilio_kit authenticate