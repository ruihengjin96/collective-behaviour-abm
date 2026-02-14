# Model overview
To be updated

# File descriptions
- `agents.py` – class definitions
- `config.py` – global parameters
- `environment.py` – geometric objects, e.g. refuge, feeding patch…
- `model.py` – the core model
- `ui_tk.py` – visualization

- `rules/boid_rules.py` – rules specific to class Boid
- `rules/predator_rules.py` – rules specific to class Predator
- `rules/shared_rules.py` – rules shared by all classes

- `temp/run_baselinemodel.py` – a script that runs the baseline model
- `temp/run_model_tk.py` – example script to run the model (i.e., entry point)
- `temp/boid_predator_v3.py` – baseline model (pre-modularization)


# How to run the model

## Clone and install
Clone the repository<br>

Create a virtual environment (optional but recommended)

Install in editable mode:
```
pip install -e .
```

## How to run the model in visualization mode
Inside the main directory, run:
```
python temp/run_model_tk.py
```

## How to run the model in simulation & data collection mode
To be updated...