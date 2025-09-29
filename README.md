# Simulation of Stockholm's agents using MATSim

## Prerequisites
This project was built and run with the following java version:
```bash
openjdk 21.0.7 2025-04-15 LTS
OpenJDK Runtime Environment Temurin-21.0.7+6 (build 21.0.7+6-LTS)
OpenJDK 64-Bit Server VM Temurin-21.0.7+6 (build 21.0.7+6-LTS, mixed mode, sharing)
```

Install 
```bash
pip install -r path/to/requirements.txt
```

## Other useful things

If you have installed new dependencies in the Python virtual environment (using e.g pip install) Export changes using
```bash
pip freeze > requirements.txt
```



## Old info [remove]
MATSim files are located in the folder named src.
This simulation includes two branches for:
### main 
Includes:
which includes:
- 25% of Stochkolm's synthetic population for 2040,
- Stockholm's road network,
- Toll file that is created for the network, using the information in the [Transportstyrelsen](https://www.transportstyrelsen.se/sv/vagtrafik/Trangselskatt/Trangselskatt-i-stockholm/Betalstationernas-placering1/) website, and
### DRT scenario
that:
- Added new sample drt file,
- Updated config and Run file. 

Things to change when run on a new OS:
1- Directories in:
	MATSim: Run and config files
	Python: Parser functions files

