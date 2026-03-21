# Changelog
All notable changes to this project will be documented in this file.
The format is based on Keep a Changelog,
and this project adheres to Semantic Versioning.

## [To-Do List] (Priority, Difficulty)

### GUI and interactivity
- ~~Add start, stop, close buttons (High)~~
- ~~Add sliders for number of boids and predators (High)~~
- ~~Add sliders for other parameters as appropriate (High)~~
- **Make the size of the window dynamic. (Mid, Mid)**
- **Rearrange the order of widgets and separate the widgets more clearly (Mid, Low)**


### Model structure and logic
- ~~Disable refuge geometry for now (High, Low)~~
- **Write a random movement rule, test it with one agent (High, High)**
- Make a pseudocode version of the model's logic and interaction rules (High)
- Examine the rules and overall logic, and think about potential restructuring/reorganization of the model (High)
- Rethink the file structure (e.g., how are interaction rules grouped into different files, and whether the file names are intuitive and good for building upon them in the future)

### Model functionalities
- Write a function that runs headless simulation for specified number of runs and collects basic data of each agent (High)

### Naming things
- Rename certain functions to make them more intuitive (Mid)
- Brainstorm short, accurate and unique package names (Mid)

## [Unreleased]
### Added
### Changed
### Fixed

## [0.0.1] - 2026-03-16
- Added more interaction options in the interface

### Added
- Added 2 more sliders for interactive interface, for the global variables `CATCH_DIST` (the distance between a predator and a boid below which the boid is considered "eaten") and `SPEED_LIMIT` (speed limit for boids, although currently it affects boids and predators differently, which should be examined later) | The main changes are located in ui_tk.py, where tk variables are defined and passed onto `loop()` which contains `model.step()`, the main update function for the model
- Added 2 input boxes for customizing numbers of boids and predators to be initiated, and a button to apply the newly entered values.
- Added buttons for starting and stopping the simulation, and for resetting the arena. 

## [0.0.0] - 2026-02-14
- Model now functions the same as the previous single-file model

### Added
- Instruction on installation and running the model in README
- Brief description of the model (WIP)

### Changed
- Moved original single-file model `boid_predator_v3.py`, and 2 scripts that run the model, namely `run_baselinemodel.py` and `run_model_tk.py` into the temp/ folder.