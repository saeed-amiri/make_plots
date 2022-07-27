import sys
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pylab as plt
plt.style.use('science')


class Doc:
    """read the out file of the thermo output and plot all of the data
    Input:
        sys.argv[1] -> thermo output
    Output:
        png figs
    """


def set_sizes(width, fraction=1) -> tuple[float, float]:
    """set figure dimennsion"""
    fig_width_pt = width*fraction
    inches_per_pt = 1/72.27
    golden_ratio = (5**0.5 - 1)/2
    fig_width_in = fig_width_pt * inches_per_pt
    fig_height_in = fig_width_in * golden_ratio
    fig_dim = (fig_width_in, fig_height_in)
    return fig_dim


class ReadJob:
    """read the data file and return the DataFrame
    if any modification is needed should be done here"""
    def __init__(self) -> None:
        fname: str = sys.argv[1]  # Input file name
        self.df = self.read_data(fname)

    def read_data(self, fname: str) -> pd.DataFrame:
        """read the datafile and return a dataframe"""
        df = pd.read_csv(fname, sep=' ', header=0)
        return df


class PlotJob(ReadJob):
    """plot all the column in the job average file"""
    def __init__(self) -> None:
        super().__init__()
        p = self.plot_columns()
        p.show()

    def plot_columns(self) -> plt:
        """plot all the columns"""
        columns = list(self.df.head())
        width = 426.79135
        if 'Step' in columns:
            columns.remove('Step')
        for col in columns:
            _, ax = plt.subplots(1, figsize=set_sizes(width))
            i_loc = self.df.index[-500]
            j_loc = self.df.index[-1]
            ax.plot(self.df.index, self.df[col],
                    label=f'Average: {np.mean(self.df[col][i_loc:j_loc]):.4f}')
            plt.axvline(x=i_loc, color='r', label='average line')
            ax.set_ylabel(col)
            ax.set_xlabel('Step')
            plt.legend()
            out_name = f'{col}.png'
            plt.savefig(out_name)
        return plt


if __name__ == "__main__":
    job = PlotJob()
