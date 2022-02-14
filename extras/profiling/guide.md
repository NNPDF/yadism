# Profiling

Use `cProfile` to generate the profile file:
```shell
python -m cProfile -o output.prof script.py
```

## Flamegraph
Launch `flameprof` to generate the flamegraph:

```shell
flameprof output.prof > flames.svg
```

## Have a look to the profile output
It is also possible to read, sort and query in python the profiler's output,
have a quick look with:

```python
import pstats

p = pstats.Stats("output.prof")
p.sort_stats("cumulative").print_stats(10)
```

or read the [docs](https://docs.python.org/3/library/profile.html) for more commands.
