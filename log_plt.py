import sys
from click import style
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pylab as plt
plt.style.use('science')
font = {'size'   : 14}

matplotlib.rc('font', **font)

class Doc:
    """read log.lammps and extract thermo_style output and plot them.
    This script reads the log without 'time_reset 0' and appends all
    the thermo after time_reset to a DataFrame.
    The thermo_style must include 'Step' key, the rest is arbitrary
    and also during the simulation the thermo_style should reamin the
    same.
    Input:
        log.lammps
    Output:
        pd.DataFrame to csv and plots
    """


def set_sizes(width, fraction=1) -> tuple[float, float]:
    """set figure dimennsion"""
    fig_width_pt = width*fraction
    inches_per_pt = 1/72.27
    golden_ratio = (5**0.5 - 1)/2
    fig_width_in = fig_width_pt * inches_per_pt
    fig_height_in = fig_width_in * golden_ratio*0.66
    fig_dim = (fig_width_in, fig_height_in)
    return fig_dim
    

class ReadLog:
    """read log.lammps"""
    def __init__(self) -> None:
        fname = sys.argv[1]
        self.read_log(fname)

    def read_log(self, fname: str) -> None:
        """reading the file"""
        lines: list[str]  # A list of the thermo lines
        header: str  # A str of the thermo_style
        lines, header = self.get_lines(fname)
        self.df = self.mk_df(lines, header)
        # self.write_df()

    def get_lines(self, fname: str) -> tuple[list[str], str, int, int]:
        run_count: int = 0  # Run counter
        line_count: int = 0  # Keep track of the lines
        self.run_list: list[int] = []  # The number of thermo for each fix
        run: bool = False  # If line starts with 'run'
        loop: bool = False  # If line starts with 'Loop'
        step: bool = False  # If line starts with 'Step'
        head: str  # To save the columns name for the DataFrame
        line_list: list[str] = []  # To save the thermo line line
        with open(fname, 'r') as f:
            while True:
                line = f.readline()
                if line.strip().startswith('run'):
                    run = True
                    run_count += 1
                    self.run_list.append(line_count)
                elif line.strip().startswith('Step'):
                    step = True
                    head = line.strip()
                elif line.strip().startswith('Loop'):
                    step = False
                    run = False
                elif line and not loop:
                    if run and step:
                        line_list.append(line.strip())
                        line_count += 1
                if not line:
                    break
        print(f'Number of runs: {run_count}\n'
              f'header: {head}')
        return line_list, head

    def mk_df(self, lines: list[str], header: str) -> pd.DataFrame:
        """make DataFrame from the list of the lines"""
        columns_names: list[str] = self.break_header(header)
        line_list: list[list[str]] = self.break_lines(lines)
        df = pd.DataFrame(line_list, columns=columns_names)
        df.drop_duplicates(subset=['Step'], inplace=True)
        return df

    def break_header(self, header: str) -> list[str]:
        return header.split(' ')

    def break_lines(self, lines: list[str]) -> list[list[str]]:
        """break the lines of the thermo-lines"""
        temp: list[str] = [item.split(' ') for item in lines]
        # remove empty chars
        return [[sub_item for sub_item in item if sub_item] for item in temp]

    def write_df(self) -> None:
        """write the DataFrame to a file"""
        fout = 'thermo.data'
        self.df.to_csv(fout, sep=' ', index=False)
        print(f'output file: {fout}')


class PlotJob(ReadLog):
    """plot all the column in the job average file"""
    def __init__(self) -> None:
        super().__init__()
        p = self.plot_columns()
        # p.show()

    def plot_columns(self) -> plt:
        """plot all the columns"""
        columns = list(self.df.head())
        self.df = self.df.astype(dtype=float)
        self.df['x_axis'] = self.df.index.copy()
        self.df['x_axis'] /= 1000
        self.run_list = [item/1000 for item in self.run_list]
        width = 426.79135
        if 'Step' in columns:
            columns.remove('Step')
        for col in columns:
            _, ax = plt.subplots(1, figsize=set_sizes(width))
            i_loc = self.df.index[-500]
            j_loc = self.df.index[-1]
            ax.plot(self.df['x_axis'], self.df[col],
                    label=f'Average: {np.mean(self.df[col][i_loc:j_loc]):.4f}')
            for xloc in self.run_list[1:]:
                plt.axvline(x=xloc, color='k', ls=':')
            plt.axvline(x=i_loc/1000, color='b', ls='--', label='Average line')
            if col == 'Density':
                ax.hlines(0.73,
                          xmin=1.0,
                          xmax=self.df.index[-1]/1000,
                          colors='r', ls='--',
                          label=r'$\rho_{\text{exp.}}$ = 0.73')
            ax.set_ylabel(col)
            ax.set_xlabel('time [ns]')
            plt.legend()
            out_name = f'{col}.png'
            plt.savefig(out_name)
        return plt


if __name__ == "__main__":
    job = PlotJob()    
