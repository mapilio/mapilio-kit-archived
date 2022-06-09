
echo " __  __    _    ____ ___ _     ___ ___      _  _____ _____"
echo "|  \/  |  / \  |  _ \_ _| |   |_ _/ _ \    | |/ /_ _|_   _|"
echo "| |\/| | / _ \ | |_) | || |    | | | | |   | ' / | |  | |  "
echo "| |  | |/ ___ \|  __/| || |___ | | |_| |   | . \ | |  | |  "
echo "|_|  |_/_/   \_\_|  |___|_____|___\___/    |_|\_\___| |_|  "

python3 -m venv mapilio_venv
source mapilio_venv/bin/activate
set -e

mkdir -p bin
mkdir -p dependencies

#
# install EAC to Equirectangular conversion binary
#
git -C dependencies  clone https://github.com/mcvarer/max2sphere-batch

make -C dependencies/max2sphere-batch -j

cp dependencies/max2sphere-batch/MAX2spherebatch bin/

python setup.py install --force > /dev/null
mapilio_kit --version

echo "Installation has completed"

mapilio_kit authenticate