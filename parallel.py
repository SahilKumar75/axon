"""Process pool helper for the bootstrap heavy scorers.

The bootstraps are CPU bound and the GIL is on in this interpreter, so threads
buy nothing here and processes are the only real option. Workers must be top
level functions taking picklable data, which is why the scorers pass plain
lists rather than closures.

Determinism is the hard requirement. Every bootstrap seeds its own
random.Random(seed) from scratch, so a task's result does not depend on how many
other tasks ran, on the order they ran in, or on whether they ran at all. Output
is therefore byte identical to the serial version, which is checked in the
scorers rather than assumed.
"""

import os
from concurrent.futures import ProcessPoolExecutor


def workers_default():
    return max(1, (os.cpu_count() or 2) - 1)


def pmap(fn, items, workers=None):
    """Map fn over items, in order, using processes when it is worth it."""
    items = list(items)
    workers = workers_default() if workers is None else workers
    if workers <= 1 or len(items) <= 1 or os.environ.get("AXON_SERIAL"):
        return [fn(x) for x in items]
    with ProcessPoolExecutor(max_workers=min(workers, len(items))) as pool:
        return list(pool.map(fn, items))
