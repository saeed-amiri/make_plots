import sys
import typing
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pylab as plt
from scipy.interpolate import interp1d
from scipy import stats,interpolate
from scipy.signal import savgol_filter
from scipy.optimize import curve_fit


class Doc:
    """Plot density profile calculated by LAMMPS
    It gets the name of the input file and returns a plot of the ave-
    rage profile over time.
    Input:
        sys.argv[1]: profile filename
    output:
        a PNG or/and EPS plot
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
        for n_block in range(num):
            if n_block == 0:
                i_line = self.line_zero + (n_block * num_rows)
            else:
                i_line = f_line + 1
            f_line: int = i_line + num_rows
            block = all_lines[i_line:f_line]
            if n_block == 0:
                _df = self.get_blocks(block)
            else:
                _df += self.get_blocks(block)
        self.get_info(_df/num)
        return _df/num

    def get_header(self, all_lines: list[str]) -> tuple[int, int, int]:
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
        columns: list[str] = ['chunk', 'coord1', 'count', 'density_mass']
        df_block: list[list[str]] = [item.strip().split(' ') for item in block]
        df = pd.DataFrame(df_block, columns=columns)
        df = df.astype({'chunk': int,
                        'coord1': float,
                        'density_mass': float,
                        'count': float})
        df['coord1'] -= df['coord1'].min()

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
    
    def get_info(self, df):
        """print put the infos about densities"""
        # print(df['density_mass'].min(), df['density_mass'].max())
        x_values = [0, 40, 62, 110, 130, 170]
        x_index = [self.find_nearest(df['coord1'], item) for item in x_values]
        print(f'{self.file}:\n')
        for i in range(len(x_index)-1):
            x_i = x_index[i]
            x_j = x_index[i+1]
            print(f'\tave[{x_i}:{x_j}]:{df["density_mass"][x_i:x_j].min()}')
        print(f'max value {self.file}: {np.max(df["density_mass"])}')
        print(f'\n')
        self.x_index = x_index

    def find_nearest(self, array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return idx

class PlotProfile:
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
        plt.plot(self.df['coord1'][:-2],
                 self.df['density_mass'][:-2],
                 label=self.name,
                 color = self.color
                 )
        # print(self.df['density_mass'].max())
        # print(f'r max: {self.df["coord1"].max()}')
        self.axis()
        plt.legend(fontsize= 10)

    def axis(self) -> None:
        """set axis lables, ranges, ..."""
        # xticks = np.linspace(self.df['coord1'][0],
                            #  self.df['coord1'].iloc[-1], num=5
                            #  )
        # xticks = [np.round(item) for item in xticks]
        x_values = [0, 50, 60, 110, 125, 172.9]
        x_index = [self.find_nearest(df['coord1'], item) for item in x_values]
        plt.xlabel(r'$r/A$', fontsize=13)
        plt.ylabel(r'${\rho\,/\,(kgm ^{-3})}$', fontsize=14)
        plt.xticks(x_values, fontsize=9)
        plt.grid(True, alpha=0.5, ls=':')
    
    def find_nearest(self, array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return idx


STEP = 10000
NSTEP = 1000000
files: typing.Any = sys.argv[1:]
plt.figure(figsize=(16/3, 3), dpi=300)
font = {'weight' : 'normal',
        'size'   : 13}

matplotlib.rc('font', **font)
colors = ['black', 'red']
outname: str = ''
for i, filename in enumerate(files):
    name = filename.strip().split('.')[0]
    f = Profile(filename)
    df = f.read_profile()
    plot = PlotProfile(df, name, colors[i])
    plot.plot_df()
    outname += name
outname = f"{outname}_profile.png"
# plt.title('density profiles')
plt.tight_layout()
plt.savefig(outname, transparent=True, dpi=300)
plt.show()
