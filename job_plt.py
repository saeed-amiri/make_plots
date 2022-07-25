from cProfile import label
import sys
from typing import Tuple
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pylab as plt
plt.style.use('science')

def set_sizes(width, fraction=1) -> Tuple[float, float]:
    """set figure dimennsion"""
    fig_width_pt = width*fraction
    inches_per_pt = 1/72.27
    golden_ratio = (5**0.5 - 1)/2
    fig_width_in = fig_width_pt * inches_per_pt
    fig_height_in = fig_width_in * golden_ratio
    fig_dim = (fig_width_in, fig_height_in)
    return fig_dim

class Doc:
    """"plot job_average
    Input:
        job_average made by mk_job_out.py
    Output:
        A dir contains all the jpg pictures
    """


class ReadJob:
    """read job_average"""
    def __init__(self) -> None:
        fname = sys.argv[1]
        self.df = self.read_job(fname)

    def read_job(self, fname: str) -> pd.DataFrame:
        """read job_average file"""
        df = pd.read_csv(fname, sep='\t')
        df.index += 1
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
            fig, ax = plt.subplots(1, figsize=set_sizes(width))
            ax.plot(self.df.index, self.df[col],
                     label=f'Average: {np.mean(self.df[col][500:]):.4f}')
            ax.set_ylabel(col)
            ax.set_xlabel('Step')
            plt.legend()
            out_name = f'{col}.png'
            plt.savefig(out_name)
            # plt.show()  
        return plt


if __name__ == '__main__':
    job = PlotJob()
