# AutoHEC
Automation scripts related to the Metropolitan Water Reclamation District of Greater Chicago Watershed Release Rate project at the Illinois State Water Survey (2015-2018).

- Developed using Python 2.7.11, HEC-HMS 3.5, HEC-RAS 4.0, and HEC-DSSVue
- Creator(s): Optimatics (optimatics.com); Nicole JS Gaynor, ISWS
- [API-reference](https://github.com/gregbyard/ICE-Coding/blob/master/API-reference.md)

AutoHEC was built to split subbasins in to a developed and an undeveloped portion based on a proposed future redevelopment rate.
Then it applies a release rate to the reservoirs in each subbasin.
The release rate is currently a single value for all subbasins in the
automation, which can be manually edited after running `InitHMS.py` and
before running HEC-HMS the second time in the `*input.json` file
(`inputFileName` defined in the `parent_hecConfig_.py` file for the
project), where `*` is the HMS project name.

## Requirements
- Python 2.7.11 or later
- Python for Windows [Extensions](http://sourceforge.net/projects/pywin32/files/pywin32/Build%20219/pywin32-219.win32-py2.7.exe/download) x86 v219 (required for COM manipulation).
- HEC-DSSVue downloaded to the `src` directory. It does not need to be installed.
- HEC-HMS and HEC-RAS must be installed on the system. The location of HEC-HMS can be set in the `parent_hecConfig_*.py` configuration file using `self.hmsDir`.

## Setup and Configuration

### How to configure your run
`parent_hecConfig_*.py` sets the overall configuration for the watershed. This
includes the location of HEC-HMS, the model version (i.e. directory name),
and model characteristics. `*_hecConfig.py` sets options specific to each
HEC-HMS run listed in the command-line input file in `runModel.cmd`.

`src/Example_files` contains example configuration files based on the
Poplar Creek model set, specifically East Branch. These files show `v005`
settings. The redevelopment rate is 20% for subbasins listed in
`alt_RD_basins.txt`, 0.01% for subbasins listed in `alt_RD_basins.txt`, and
40% for the remaining subbasins. The release rate is 0.1 cfs/acre for
all subbasins listed in `alt_RR_basins.txt` and `alt_RR_basins2.txt`, and
0.15 cfs/acre for all remaining subbasins. The canopy is 0.39 for all
subbasins listed in `alt_can_basins.txt` and 0.52 for all remaining
subbasins. The alternative redevelopment rates, release rates, and
canopy files may be blank, in which case the alt numbers listed in the
parent config file have no effect.

**N.B.:**
- This script depends on the `*.u##` file already being updated to have subbasins and reservoirs point to the new Junction names, which is "JN [subbasin name]".
- Do **_NOT_** edit the HTAB parameter in the HEC-RAS GUI. If you do
and you get a Fortran error, replace the geometry file with the original
version (which was hopefully saved from a prior model setup).

## Running
How to run code that splits basins and runs models:
1. Modify `*_hecConfig.py` files to find the files that need to be
   modified to reflect the characteristics of the future subbasins.
   (See `parent_hecConfig_Example.py`, `Example_hmsConfig.py`, and
   `Example_rasConfig.py`)
2. Modify/create a text file that lists the prefixes for the `*_hecConfig.py`
   files needed for the HEC-HMS runs. Use this file name as the input in
   `runModel.cmd`. (See `Example_hms.txt` and `Example_ras.txt`)
3. Modify/create text files that list the subbasin names where alternative
   release rates, redevelopment rates, and canopy values should be used.
   that list the subbasins that should use the alternative release rates
   These parameters are set using `releaseratealt`, `releaseratealt2`,
   `redevelopmentalt`, `redevelopmentalt2`, and `canopy alt`. The file names are `alt_RR_basins.txt`, `alt_RR_basins2.txt`, `alt_RD_basins.txt`, `alt_RD_basins2.txt`, `alt_can_basins.txt`. These files need to exist and
   should be empty if all the subbasins use the regular release rate.
4. Open Windows Command Prompt.
5. Change to directory containing `runModel.cmd` (`AutoHEC/src`)
   directory (`dir` lists directory contents and `cd` changes directory).
6. Type `runModel.cmd` into the Windows command line and press Enter.
   Output will be saved to `output_hms.txt` and `output_ras.txt`.

<!-- See README in SplitBasins directory for how to run the subbasin splitting code on its own -->

## Error Checking
Be sure to check the output files to make sure that there were no errors.
Common errors may include:
1. Jython/Java error, which would appear below the blocks set off in
   colons (which indicates when the Jython interpreter starts in
   HEC-DSSVue). This may indicate a corrupted file. Try recreating the
   version directory from the source model.
2. HEC-HMS error, which would be indicated after one of the HEC-HMS runs
   on the line that starts with `End HEC-HMS` as `Exit status = -1`. Try
   manually running HEC-HMS. The most likely problem is that a reservoir
   overflowed and the max storage in the rating curve needs to be slightly
   increased.
3. HEC-RAS runs in an absurdly short time (less than 70 seconds or so).
   This will show up on the last line of the output file. Try running the
   model manually in HEC-RAS to make sure it runs to completion. The most
   likely problem is that the model became unstable or there was a HEC-HMS
   error. Try using a different time step or locating where the model
   becomes unstable. Adding or subtracting 0.01 to the HTAB parameter at
   the unstable cross section and 3-5 cross sections on either side of it
   may also help model stability. Do NOT edit the HTAB parameter in the
   HEC-RAS GUI. This will cause a Fortran error in the model code itself.
