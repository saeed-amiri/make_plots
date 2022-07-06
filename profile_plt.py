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
        time_step, num_rows, nbins = self.get_header(all_lines)
        num = int(NSTEP / STEP)
        print(num)
        for n_block in range(5):
            if n_block == 0:
                i_line = self.line_zero + (n_block * num_rows)
            else:
                i_line = f_line + 1
            f_line = i_line + num_rows
            block = all_lines[i_line:f_line]
            self.get_blocks(block)

    def get_header(self, all_lines: list[str]) -> None:
        line_zero = 0
        for line in all_lines[0:10]:
            if line.startswith("#"):
                line_zero += 1
            else:
                time_step, num_rows, nbins = self.process_header(line)
                self.line_zero = line_zero + 1
                break
        return time_step, num_rows, nbins

    def get_blocks(self, block: list[str]) -> pd.DataFrame:
        """get every block of data"""
        columns = ['ind', 'bin_center', 'g_r', 'coord_r']
        block = [item.strip().split(' ') for item in block]
        df = pd.DataFrame(block, columns=columns)
        df = df.astype({'ind': int,
                        'bin_center': float,
                        'g_r': float,
                        'coord_r': float})
        return df

    def process_header(self, line: str) -> tuple[int, int, int]:
        time_step: int
        num_rows: int
        nbins: int
        _ll: list[str] = line.strip().split(' ')
        ll: list[int] = [int(item) for item in _ll]
        time_step, num_rows, nbins = ll
        del _ll, ll
        return time_step, num_rows, nbins


STEP = 1000
NSTEP = 2500000
filename: str = sys.argv[1]
f = Profile(filename)
f.read_profile()
