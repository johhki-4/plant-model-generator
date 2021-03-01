# Plant model generator

## Visual Components & nxtSTUDIO

### Dependencies for the trace generation
To get started, follow all the steps given by the Factory of the Future Repository on github:
https://version.aalto.fi/gitlab/afof/tracing-products/-/tree/master/

There are two minor changes to their guide that is needed to make this project work. The first one is a small addition to the guide when you get to:
- Simulation in Visual Components
  - Requirements
    - Setting up dependencies

Take the file `AFOF_2.py` in **this** repository, and do the exact same steps as with the `AFOF.py` in the guide. For both files, you also need to go into the file and on approximately line 30 specify a desired location to save the generated trace log file.

### Usage of the simulation in Visual Components
The other small change to the guide is when you get to:
- Simulation in Visual Components
  - Usage

Here, you open the `PoductionTracing2020.vcmx` file given in **this** repository instead of the one given in their repository. If all the steps in their guide are done properly, you should now be able to run the plant and record its traces.

## Model Generator
Once the simulations work and you can generate trace files it is time to get the model generator and generate a NuSMV model file from the traces.
The `ModelGenerator` folder contains the following:
- `GeneratedTraces`, where the traces from the Visual Components simulations are saved. The file `2020_11_6_11_58_trace_log.txt` in this folder in an example trace, but as you simulate the plant, more and more trace files are added to this folder.
- `NuSMV_Models`, where the generated models of the plant are saved. The files saved here still required the manual additions to link the subsystems together. Compare the full model in `full_model.smv` with the unmodified generated file `2021_3_1_12_58_log.smv` for the required addition to be made in this approach.
- `PlantUML_Models`, where the automatically generated state machines are stored. Note that this is not a completed feature of the project.

In addition to these folders, there are two files:
- `initial_values.txt`, where all values for the plant are noted and their initial values are stored.
- `model_generator.py`, where the transformation from **trace data** to **NuSMV model file** and **PlantUML state machines** takes place. Note that lines 190-200 in this file specifies folders/locations of files. Make sure that these are setup in a proper way for your system. 

## Evaluating the model in NuSMV
The NuSMV software is used to evaluate the `.svm` model files that are generated from the model generator. Here, you also state the functional properties that the model should adhere to.
- Download: https://nusmv.fbk.eu/
- Guides:
  - User Manual: https://nusmv.fbk.eu/NuSMV/userman/index-v2.html
  - Tutorial: https://nusmv.fbk.eu/NuSMV/tutorial/index.html

## Automaticaly generated state machines 
The state machines are generated in the file `uml_test.txt`. Since this feature is not a completed feature yet, they have been extracted from the generated file and put into their own files in the `manual sm` folder. This enables them to be properly evaluated in PlantUML, and PlantUML can generate the images.
- Download: https://plantuml.com/download
- Learn PlantUML: http://plantuml.com/guide


#
This concludes all the features of the project. 
