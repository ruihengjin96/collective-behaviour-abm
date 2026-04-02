import sys
from abmsim.ui_tk import run

# Set scenario from command-line arguments
# Usage: python temp/run_model_tk.py --social --predation --classdiff
kwargs = {}
if '--no-social' in sys.argv:
    kwargs['enable_social'] = False
if '--no-predation' in sys.argv:
    kwargs['enable_predation'] = False
if '--use-class-diff' in sys.argv:
    kwargs['enable_classdiff'] = True

run(**kwargs)
