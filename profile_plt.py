import sys
import typing
import numpy as np
import pandas as pd
import matplotlib.pylab as plt


class Doc:
    """Plot density profile calculated by LAMMPS
    It gets the name of the input file and returns a plot of the ave-
    rage profile over time.
    Input:
        sys.argv[1]: profile filename
    output:
        a JPG or/and EPS plot
    """


class Profile:
    """Read profile file"""
    def __init__(self, filename) -> None:
        self.file: str = filename
        del filename

    def read_profile(self) -> pd.DataFrame:
        """read profile and return DataFrame of average"""
        with open(self.file, 'r') as f:
            all_lines = f.readlines()
        self.get_header(all_lines)

    def get_header(self, all_lines: list[str]) -> None:
        for line in all_lines[0:10]:
            if line.startswith("#"):
                pass
            else:
                print(self.process_header(line))
                break

    def process_header(self, line: str) -> tuple[int, int, int]:
        time_step: int
        num_rows: int
        nbins: int
        _ll: list[str] = line.strip().split(' ')
        ll: list[int] = [int(item) for item in ll]
        time_step, num_rows, nbins = ll
        del _ll, ll
        return time_step, num_rows, nbins


filename: str = sys.argv[1]
f = Profile(filename)
f.read_profile()
