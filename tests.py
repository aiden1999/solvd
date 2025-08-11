import time
from solvd.sudoku.common.box_lookup_tables import BUTTERFLY_LOOKUP, CROSS_LOOKUP

# Test JUST the lookup performance
start = time.time()
for r in range(12):
    for c in range(12):
        result = BUTTERFLY_LOOKUP[(r, c)]  # Just the lookup
butterfly_time = time.time() - start

start = time.time()
for r in range(6, 15):
    for c in range(21):
        result = CROSS_LOOKUP[(r, c)]  # Just the lookup
for r in range(6):
    for c in range(6, 15):
        result = CROSS_LOOKUP[(r, c)]
        result = CROSS_LOOKUP[(r + 15, c)]
cross_time = time.time() - start

print(f"Butterfly lookup: {butterfly_time:.4f}s")
print(f"Cross lookup: {cross_time:.4f}s")
