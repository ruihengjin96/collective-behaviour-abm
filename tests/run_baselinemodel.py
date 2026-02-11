# examples/run_monolithic.py

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from temp.boid_predator_v3 import main  

if __name__ == "__main__":
    main() 