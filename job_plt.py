from cProfile import label
import sys
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pylab as plt
plt.style.use('science')

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
        if 'Step' in columns:
            columns.remove('Step')
        for col in columns:
            plt.plot(self.df.index, self.df[col],
                     label=f'Average: {np.mean(self.df[col][500:]):.4f}')
            plt.ylabel(col)
            plt.xlabel('Step')
            plt.legend()
            plt.show()  
        return plt


if __name__ == '__main__':
    job = PlotJob()
