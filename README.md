# Plant model generator

## Dependencies for the trace generation
Follow all the steps given by the Factory of the Future Repository on github:
https://version.aalto.fi/gitlab/afof/tracing-products/-/tree/master/

When you get to:
- Simulation in Visual Components
  - Requirements
    - Setting up dependencies,

do the same steps for the `AFOF_2.py` file given in this repository.

You also need to go into the file and on line 30 specify the desired location.

## Usage of the simulation in Visual Components
When you get to:
- Simulation in Visual Components
  - Usage,

open the `PoductionTracing2020.vcmx` file given in **this** repository instead.

## Model Generator
Once the simulations work and you can generate trace files it is time to get the model generator and generate a NuSMV model file from the traces.
In the folder `ModelGenerator`, there are some additional folders:
- `GeneratedTraces`, where the traces from the Visual Components simulations are saved. The file `2020_11_6_11_58_trace_log.txt` in this folder in an example trace, but as you simulate the plant, more and more trace files are added to this folder.
- `NuSMV_Models`, where the generated models of the plant are saved. The files saved here still required the manual additions to link the subsystems together. Compare the full model in `full_model.smv` with the unmodified generated file `2021_3_1_12_58_log.smv` for the changes made in this scenario.
- `PlantUML_Models`, where the automatically generated state machines are stored. Note that this is not a completed feature of the project. Nonetheless, the state machines are generated in the same file `uml_test.txt` and to visualize how they look, they have been extracted and put into their own files in the `manual sm` folder. The `.txt` files are evaluated in PlantUML(https://plantuml.com/state-diagram), and PlantUML generates the images.

In addition to these folders, there are two files:
- `initial_values.txt`, where all values for the plant are noted and their initial values are stored.
- `model_generator.py`, where the transformation from **trace data** to **NuSMV model file** and **PlantUML state machines** takes place. Note that lines 190-200 in this file specifies folders/locations of files. Make sure that these are setup in a proper way for your system. 

## Evaluating the model in NuSMV
The NuSMV software (https://nusmv.fbk.eu/) is used to evaluate the `.svm` that are genereted from out model generator. Go to the website and follow the instructions on how to install it.

Then learn the important features in either the User Manual(https://nusmv.fbk.eu/NuSMV/userman/index-v2.html) or the Tutorial(https://nusmv.fbk.eu/NuSMV/tutorial/index.html), so you will know how to execute the generated `.smv` model files.
