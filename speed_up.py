import pandas as pd
import matplotlib
import matplotlib.pylab as plt
import sys

class Doc:
    """reading the inforamtion about the wall time
    and return the `speedup plot` for the proposal"""


class ReadTime:
    """read wall times"""
    def __init__(self,
                 fname: str  # timewall file name
                 ) -> None:
        df: pd.DataFrame = self.read_times(fname)  # DataFrame of the data
        self.df = self.get_speed_up(df)

    def read_times(self,
                   fname: str  # timewall file name
                   ) -> pd.DataFrame:
        df = pd.read_csv(fname, sep=' ', header=0)
        return df
    
    def get_speed_up(self,
                     df: pd.DataFrame  # df from the file
                     ) -> pd.DataFrame:
        """add speed up column to the df"""
        spd: list[float]  # speed up column
        spd = [item/df['ns/day'][0] for item in df['ns/day']]
        df['spd'] = spd
        return df
    
if __name__ == '__main__':
    data = ReadTime(sys.argv[1])
