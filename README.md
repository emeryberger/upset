# upset

fuzzes addresses (and thus, `set`s in Python)

## build

```bash
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=Release  ..
make
make install
```

## use (Mac)

```bash
DYLD_INSERT_LIBRARIES=/usr/local/libupset.dylib PYTHONMALLOC=malloc python3 test/setmeup.py
```

## use (Linux)

```bash
LD_PRELOAD=/usr/local/libupset.so PYTHONMALLOC=malloc python3 test/setmeup.py
```

## test (Mac)

```bash
cd test
python3 histogram.py --program setmeup.py --runs 1000 --maxrange 16 --environment="DYLD_INSERT_LIBRARIES=$PWD/../build/libupset.dylib PYTHONMALLOC=malloc"
open histogram.pdf
```

