```
# create project directory and enter it
mkdir python-garmin
cd python-garmin

# install python venv and development packages
sudo apt apt install python3-venv python3-dev

# create virtual env and activate it
python3 -m venv .
source bin/activate

# clone radar_pi repo
git clone https://github.com/opencpn-radar-pi/radar_pi

# install dependencies for c++ warper
pip install "pybind11[global]"
pip install cppimport

# initialize submodules
cd radar_pi
git submodule update --init opencpn-libs
rm -rf build; mkdir build; cd build

# install dependencies for radar_pi
sudo apt install devscripts equivs
sudo mk-build-deps -ir build-deps/control
sudo apt-get -q --allow-unauthenticated install -f

# build c++ library (libradar_pi.so)
cmake ..
make tarball
```
