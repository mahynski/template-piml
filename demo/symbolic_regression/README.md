# Background

This is a demonstration of symbolic regression which takes 4 variables, (x, y, dx/dt, dy/dt),
and tries to predict the acceleration, (d2x/dt2, d2y/dt2), from these states. In fact, the
data provided is only a hypothetical residual, assuming we have already accounted for (0, -8.0)
in each direction already. The data is from an ideal ballistic motion simulation so the correct
answer should be a constant value of (0, -1.8). See the `node/` directory for details.

# Execution

Run the demo files from the command line for the best results. The first time these are run some
Julia files will be automatically installed.

~~~bash
uv run pysr_demo_individual.py
~~~

~~~bash
uv run pysr_demo_combined.py
~~~
