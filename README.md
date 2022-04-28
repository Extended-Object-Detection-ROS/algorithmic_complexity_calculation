# algorithmic_complexity_calculation
Experimental calculation of algorithmic complexity

## Install
```bash
git clone --recurse-submodules https://github.com/Extended-Object-Detection-ROS/algorithmic_complexity_calculation
```
## Build
```bash
cd algorithmic_complexity_calculation
mkdir build
cd build
cmake ..
make
cd ..
```
## Launch
### BB_matching
1. Collect data
```
./build/bb_matching 0 900 100 2 ../data/bb_matching_0_900.csv 
```
2. Anylize data
```
python3 src/bb_matching_analyze.py --file data/bb_matching_0_900.csv
```
