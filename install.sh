python3 -m venv mapilio_venv
source mapilio_venv/bin/activate
git pull origin master
python setup.py install --force
mapilio_kit --version

echo "Installation has completed"

mapilio_kit authenticate