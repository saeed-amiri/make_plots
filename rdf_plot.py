import re
import sys
import typing
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pylab as plt


class Doc:
    """Plot rdf calculated by LAMMPS
    It gets the name of the input file and returns a plot of the ave-
    rage rdf over time.
    Input:
        sys.argv[1]: rdf filename
    output:
        a PNG or/and EPS plot
    """


class Rdf:
    """Read rdf file"""
    def __init__(self, filename) -> None:
        self.file: str = filename
        del filename

    def read_profile(self) -> pd.DataFrame:
        """read profile and return DataFrame of average"""
        with open(self.file, 'r') as f:
            all_lines = f.readlines()
        time_step, num_rows = self.get_header(all_lines)
        num = int(NSTEP / STEP)
        start = 0
        for n_block in range(start,num+1):
            if n_block == start:
                i_line = self.line_zero + (n_block * num_rows)
            else:
                i_line = f_line + 1
            f_line: int = i_line + num_rows
            block = all_lines[i_line:f_line]
            if n_block == start:
                _df = self.get_blocks(block)
            else:
                _df += self.get_blocks(block)
            div = num-start
        return _df/div

    def get_header(self, all_lines: list[str]) -> tuple[int, int]:
        line_zero = 0
        for line in all_lines[0:10]:
            if line.startswith("#"):
                line_zero += 1
            else:
                time_step, num_rows = self.process_header(line)
                self.line_zero = line_zero + 1
                break
        return time_step, num_rows

    def get_blocks(self, block: list[str]) -> pd.DataFrame:
        """get every block of data"""
        columns: list[str] = ['chunk', 'c1', 'c2', 'c3']
        df_block: list[list[str]] = [item.strip().split(' ') for item in block]
        df = pd.DataFrame(df_block, columns=columns)
        df = df.astype({'chunk': int,
                        'c1': float,
                        'c3': float,
                        'c2': float})
        return df

    def process_header(self, line: str) -> tuple[int, int]:
        time_step: int
        num_rows: int
        nbins: int
        _ll: list[str] = line.strip().split(' ')
        ll: list[int] = [int(item) for item in _ll]
        time_step, num_rows = ll
        del _ll, ll
        return time_step, num_rows


class PlotRdf:
    """plot all the profile on one tableau"""
    def __init__(self,
                 df: pd.DataFrame,
                 filename: str,
                 color: str) -> None:
        self.df = df
        self.name = filename
        self.color = color
        del df

    def plot_df(self) -> None:
        plt.plot(self.df['c1'],
                 self.df['c2'],
                 label=self.name,
                 color = self.color
                 )
        self.axis()
        plt.legend()

    def axis(self) -> None:
        """set axis lables, ranges, ..."""
        plt.xlabel(r'$r/A$', fontsize=13)
        plt.ylabel(r'$g(r)$', fontsize=13)


STEP = 1000
NSTEP = 2500000
files: typing.Any = sys.argv[1:]
plt.figure(figsize=(16/3, 3), dpi=180)
font = {'weight' : 'normal',
        'size'   : 13}

matplotlib.rc('font', **font)
colors = ['red', 'black', 'blue']
outname: str = ''
for i, filename in enumerate(files):
    name = filename.strip().split('.')[0]
    outname += name
    name = name.split('RDF_')[1]
    name = re.sub('_', '', name)
    name = f"g$_{{{name}}}$"
    f = Rdf(filename)
    df = f.read_profile()
    plot = PlotRdf(df, name, colors[i])
    plot.plot_df()
outname = f"{outname}_rdf.png"
plt.title('RDF')
plt.tight_layout()
plt.savefig(outname, transparent=True)
plt.show()
