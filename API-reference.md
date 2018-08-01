# AutoHEC API

Structure of automation code from Optimatics

- [Control](#control)
	- [`runModel.cmd`](#runmodelcmd)
- [API](#api)
	- [`parent_hecConfig_*.py` (class `HecConfig` imported as config)](#parenthecconfigpy-class-hecconfig-imported-as-config)
	- [`hecConfig.py` (class `HecConfig` imported as config)](#hecconfigpy-class-hecconfig-imported-as-config)
	- [`runModel.py`](#runmodelpy)
	- [`hecModel.py` (class Model)](#hecmodelpy-class-model)
	- [`runHms.py` (added by NJS Gaynor)](#runhmspy-added-by-njs-gaynor)
	- [`runRas.py` (added by NJS Gaynor)](#runraspy-added-by-njs-gaynor)
	- [`runHecHmsModel.py`](#runhechmsmodelpy)
	- [`dummyStorageOutflowCurves.py` (added by NJS Gaynor)](#dummystorageoutflowcurvespy-added-by-njs-gaynor)
	- [`copyStorageOutflowCurves.py` (added by NJS Gaynor)](#copystorageoutflowcurvespy-added-by-njs-gaynor)
	- [`createStorageOutflowCurves.py`](#createstorageoutflowcurvespy)

## Control

### `runModel.cmd`
You must choose the input text file that lists the names of the config files. Use two colons to comment out all the options you do *not* wish to use. `runHMS.py` and `runRas.py` must have `subhms = sys.stdin.readlines()` and `subras = sys.stdin.readlines()` uncommented.

>Sets environmental variables and initiates python scripts; command line input should be text file that contains the prefixes for each `hecConfig.py` file. This is how you run the model automation outside of an IDE. Output is stored in `output_hms.txt` and `output_ras.txt`.
>
>- depends on: `runModel.py`

## API

### `parent_hecConfig_*.py` (class `HecConfig` imported as config)
> config file with setup variables for HMS and RAS runs; these files are copied to `hecConfig.py` for use in the program and the original files are retained. There are different `parent_hecConfig` files for each watershed.

- `setme1()`: General settings for HMS and RAS. The only option that changes within
  a watershed is self.modelVersion.
- `setme2hms()`: HMS-specific settings. This is where you specify version
  characteristics like release rate and precipitation.
- `setme2ras()`: RAS-specific settings. These don't change within a watershed.

### `hecConfig.py` (class `HecConfig` imported as config)
> generic file name used to run models. `*_hmsConfig.py` or `*_rasConfig.py` is copied to this file name.

### `runModel.py`
> controls workflow that splits basins and runs HEC-HMS and HEC-RAS; reads lines from input file to find config file for each subsubwatershed, if needed
>
>- depends on: `*hecConfig.py`

### `hecModel.py` (class Model)
> contains all methods to control automation of HEC-HMS and HEC-RAS
>
>- depends on: RunHecHmsModel.py, createStorageOutflowCurves.py,
  ExampleHydraulicComparison.py, win32com module

- `runHms()`: runs HMS model using `HEC-HMS.cmd`
- `newStorageOutflowCurves()`: creates new storage-outflow curves in the DSS file with dummy data for use with the new Reservoirs
- `createStorageOutflowCurves(subbasins)`: modifies the storage-outflow curve data based on Amanda Flegel's algorithm
- `runRas()`: runs HEC-RAS using `HECRASController`
- `getHydraulicResults(ditchNames)` [not currently used]: retrieves and processes RAS results from DSS file using `ExampleHydraulicComparison.py` and `ExampleDssUsage.py`

### `runHms.py` (added by NJS Gaynor)
> runs HMS model for each subwatershed
>
>- depends on: `runModel.py`, `SplitBasins/InitHMS.py`

### `runRas.py` (added by NJS Gaynor)
> runs RAS model for each subwatershed
>
>- depends on: `hecModel.py`, `runModel.py`

### `runHecHmsModel.py`
> runs HEC-HMS instance using hms python module; exactly as in HEC-HMS documentation for command line use of the model
>
> - depends on: `hecConfig.py`, hms module
> - called from: `hecModel.py`

### `dummyStorageOutflowCurves.py` (added by NJS Gaynor)
> creates dummy storage outflow curves using HEC-DSSVue jython script and inserts table into DSS file for use with new Reservoirs added in InitHMS.py
>
>- depends on: hec module, `*hecConfig.py`, `ExampleHydraulicComparison.py` (by way of dtf file)

### `copyStorageOutflowCurves.py` (added by NJS Gaynor)
> copies storage outflow curves from a HEC-HMS DSS file that used 24h precip
  and pastes the curves into the corresponding run that uses 12h precip, using HEC-DSSVue jython script, for use with new Reservoirs added in InitHMS.py
>
>- depends on: hec module, `*hecConfig.py`, `ExampleHydraulicComparison.py` (by way of dtf file)

### `createStorageOutflowCurves.py`
> replaces the dummy storage-outflow curve created in `dummyStorageOutflowCurves.py` because this method assumes the table exists; initial storage is the accumulation of the inflow until the inflow exceeds 3% of the allowable release rate for the subbasin (based on subbasin size and a 0.3 cfs/acre release rate); then outflow hydrograph is a straight line from that point to the point at which inflow drops below the max allowable release rate. For any times where the hydrograph dips below the rating curve, the storage for that time step is set to zero (would otherwise be negative) in order to avoid model errors. Also, some subbasins do not require detention; in that case the rating curve is assigned such that the reservoir is free flowing. The entire rating curve is multiplied by 1.01 to avoid rounding errors, which cause more reservoirs to overflow during the second HEC-HMS run.
>
>- depends on: hec module, `*hecConfig.py`, `ExampleHydraulicComparison.py` (by way of dtf file)

- `indexOfMaxValue(hydrograph)`: finds the index of the maximum value in the inflow hydrograph
- `findFirst(sequence, predicate)`: find the first element in which predicate is true
- `findLast(sequence, predicate)`: find the last element in which predicate is true
- `any(predicate, container)`: returns true if predicate is true in any element of the container
- `flowFileDates()`: finds all dates for FLOW files in the DSS catalog give specified model run; will not be accurate if there is more than one set of data for the specified model run (i.e. more than one distinct time period)
- `buildInflowHydrograph(subbasinName)`: retrieves the FLOW data from the RAS DSS file and concatenates it into a single time series
- `buildStorageOutflowCurve(subbasinName, subBasinArea, allowableReleaseRatePerAcre)`: returns values from `buildStorageOutflowCurveFromHydrograph`
- `findInflowStart(hydrograph, subBasinArea)`: finds the beginning of the outflow hydrograph (i.e. where the inflow hydrograph exceeds 3% of the max allowable release rate for the subbasin based on 0.3 cfs/acre)
- `findMaxReleaseRateIndex(hydrograph, allowableReleaseRate)`: finds the end of the outflow hydrograph (i.e. where the inflow drops below the max allowable release rate for the subbasin based on 0.3 cfs/acre)
- `buildStorageOutflowCurveFromHydrograph(inflowHydrograph, SubBasinArea, allowableReleaseRatePerAcre)`: calculates each time step of the straight-line outflow hydrograph from the index found in `findInflowStart` to the index found in `findMaxReleaseRateIndex` and calculates the accumulated storage over this period; uses a 1.01 multiplier to attempt to account for insufficient max storage problem in HEC-HMS
- `writeTable(tableName, storage, outflowRates)`: writes new storage-outflow table to the RAS DSS file
- `recordTotalStorage(storage, subbasin, totStorage)`: records the max storage from each storage-outflow curve
- `writeTotalStorage(totStorage, fileName, filePath)`: writes total storage for each subbasin to a CSV file named `*_storage.csv` stored in the model version directory


## NOT USED (so should be removed)

### `ExampleDssUsage.py`
> shows how to access (read/write) data to DSS file
>
>- depends on: hec module, `*hecConfig.py`

- `GetMaxValueIndex(hydrograph)`: finds index of the maximum value in hydrograph

### `ExampleHydraulicComparison.py`
> retrieves hydraulic results from DSS file (does nothing with them yet)
>
>- depends on: hec module, `*hecConfig.py`

- `GetMaxValueIndex(hydrograph)`: finds index of the maximum value in hydrograph
