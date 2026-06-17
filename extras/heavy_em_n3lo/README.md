In order to compute the pre-tabulated aN3LO heavy coefficient functions,
first run:

```sh
python produce_grids.py
```

to generate the kinematic values `xi` and `eta` from which the coefficient
functions will be tabulated on.

Then, run the following command to compute the coefficient functions:

```sh
./generate_grids.sh
```
