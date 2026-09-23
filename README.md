## PW1 - Lab A: Reproducible Foundations

**What I built:**
- Built a radioactive decay simulation using pure Python loops and vectorized NumPy code.
- Set up conda environment tracking, .gitignore rules, and full Git workflow.

## Results & Performance Comparison
- **N0**: 200,000 atoms
- **Pure-Python loop execution time**: 11.11722 seconds
- **NumPy execution time**:          0.0003 seconds
- **Speed-up factor**: 42860.36x faster than pure-Python loop

**Tests:** all passing? yes

**Conclusion:**
- Vectorized operations with NumPy dramatically increase execution speed compared to standard Python loops.
- Automated unit tests with pytest ensure code correctness, while Conda environment files maintain reproducibility across different machines.

**Reproducibility test (Stretch Goal):**
- Tested code on a partner's machine: environment built seamlessly without modifications, and all pytest cases passed without errors.

## PW1 Lab B
**What the data showed:** The data demonstrates an exponential decay process over time, with the count decreasing rapidly at first and then leveling off. 
**Match with analytical law:** The observed data points closely match the analytical decay curve ($N_{0}e^{-\lambda t}$), confirming that the analytical law accurately describes the observed phenomenon.
**Snakemake Pipeline:** The Snakemake pipeline automates the generation of the plot, ensuring `figure.png` is only rebuilt if the input dataset (`decay_observed.csv`) or the python script (`plot.py`) changes.x