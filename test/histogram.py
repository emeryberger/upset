#!/usr/bin/env python3

import click
import subprocess
import os
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

@click.command()
@click.option(
    '--environment',
    default='',
    help='String of env variables for the second run (e.g. "VAR1=val1 VAR2=val2").'
)
@click.option(
    '--runs',
    default=1000,
    help='Number of times to run a program for each scenario.'
)
@click.option(
    '--program',
    default="setmeup.py",
    help='The program to run for each scenario.'
)
@click.option(
    '--maxrange',
    default=100,
    help='Maximum range of numbers.'
)
def main(environment, runs, program, maxrange):
    """
    Runs a program a specified number of times in two scenarios:
    1) vanilla (no environment variables)
    2) with the environment variables provided on the command line
    And then compares the distributions of the returned numbers.
    """

    # --- 1) Collect results for the vanilla scenario ---
    vanilla_results = []
    for _ in range(runs):
        # Run program in "vanilla" mode
        result = subprocess.check_output(["python3", program])
        # Decode the output to a string, strip whitespace, convert to int
        vanilla_results.append(int(result.decode().strip()))

    # --- 2) Collect results for the environment-variables scenario ---
    # Make a copy of the current environment and add (or overwrite) variables
    env_dict = os.environ.copy()
    if environment:
        for kv in environment.split():
            k, v = kv.split("=", 1)
            env_dict[k] = v

    env_results = []
    for _ in range(runs):
        # Run with extra environment vars
        result = subprocess.check_output(["python3", program], env=env_dict)
        env_results.append(int(result.decode().strip()))

    # --- 3) Put results into a pandas DataFrame for plotting ---
    df = pd.DataFrame({
        "value": vanilla_results + env_results,
        "scenario": ["vanilla"] * runs + ["env"] * runs
    })

    # --- 4) Create a single plot comparing distributions ---
    sns.histplot(
        data=df,
        x="value",
        hue="scenario",
        multiple="dodge",
        binwidth=1,
        binrange=(0, maxrange)
    )
    plt.title("Distribution (vanilla vs. environment)")
    plt.xlabel(f"Number Returned by {program}")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
