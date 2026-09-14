# PW1 --- Lab A Report

## Results & Performance Comparison
- **N0**: 200,000 atoms
- **Pure-Python loop execution time**: 11.11722 seconds
- **NumPy execution time**:          0.0003 seconds
- **Speed-up factor**: 42860.36x faster than pure-Python loop

## Test Suite Status
- Ran `pytest -v`
- All 3 tests passed (`test_starts_at_N0`, `test_rejects_negative_rate`, `test_matches_law`).

## Conclusion
Vectorized operations in NumPy outperform standard Python loops by orders of magnitude when simulating radioactive decay for large particle sets.