# upset

`upset` fuzzes addresses at a fine grain, making addresses highly
unlikely to be repeated in the same sequence.  If your code has any
dependencies on memory addresses, `upset` is almost certain to expose
them.

While many programs may depend on such addressses (especially C++
programs), `upset` is particularly useful for Python code. In Python,
objects without `__hash__` functions (including strings) use a default
hash function based on the object's memory address. While this leads
to non-deterministic ordering in `set`s, the predictability of the
addresses returned by standard memory allocators means that, within a
single run, there is not much randomization and so the non-determinism
may not be exposed. By contrast, `upset`'s thorough randomization
approach makes it almost certain that sets will exhibit a wide range
of orders.

## Building `upset`

To build the `upset` package for Python, run the following command.

```bash
python3 -m pip install .
```

`upset`'s shared library (`libupset.so`/`.dylib`) can also be built and used directly.

```bash
mkdir build
cd build
cmake ..
make
``

## Using `upset`

To upset Python programs:

```bash
python3 -m upset yourprogram.py
python3 -m upset -m pytest
```

To upset C/C++/Rust programs:

```bash
cd build
LD_PRELOAD=$(PWD)/libupset.so your_program               # Linux
DYLD_INSERT_LIBRARIES=$(PWD)/libupset.dylib your_program # Mac
```

## Testing `upset`


```bash
python3 -m pytest # will fail and report a small number of randomizations
python3 -m upset -m pytest # will almost certainly succeed
```

