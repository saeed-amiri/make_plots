from cProfile import label
import pandas as pd
import matplotlib
import matplotlib.pylab as plt
import sys
# plt.style.use('science')
# plt.style.use(['science','ieee'])


class Doc:
    """reading the inforamtion about the wall time
    and return the `speedup plot` for the proposal"""

class ReadTime:
    """read wall times"""
    def __init__(self,
                 fname: str  # timewall file name
                 ) -> None:
        df: pd.DataFrame = self.read_times(fname)  # DataFrame of the data
        df = self.get_speed_up(df)
        self.df = self.set_idl(df)

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
        df['cores'] = [item*96 for item in df['nodes']]
        return df
    
    def set_idl(self,
                df: pd.DataFrame  # df from the file
                ) -> pd.DataFrame:
        """make a ideal speed up"""
        m: float  # slop of the line
        m = (df['spd'][2]-df['spd'][1])/(df['nodes'][2]-df['nodes'][1])
        idl: list[float]  # ideal speed up
        idl = [m*(item-1)+1 for item in df['nodes']]
        df['idl'] = idl
        return df


class PlotDf:
    """plot speed up"""
    def __init__(self,
                 df: pd.DataFrame  # Dataframe to plot from ReadTime
                 ) -> None:
        self.mk_plt(df)

    def mk_plt(self,
               df: pd.DataFrame
               ) -> None:
        """make plot"""
        width = 426.79135
        _, ax = plt.subplots(1, figsize=self.set_sizes(width))
        ax.plot(df['nodes'][:-3], df['spd'][:-3],
                c='k',
                markersize=5,
                marker='^',
                ls=':',
                mfc='r',
                mec='r',
                label='test')
        ax.plot(df['nodes'][:9], df['idl'][:9], label='Ideal')
        xticks = [96, 960, 1920, 2880, 3840]
        xlocs = [1, 10, 20, 30, 40]
        ylocs = [1, 5, 10]
        yticks = [1, 5, 10]
        ax.set_ylim(0,12.5)
        ax.set_xticks(xlocs)
        ax.set_xticklabels(xticks)
        ax.set_yticks(ylocs)
        ax.set_yticklabels(yticks)
        ax.set_xlabel('Number of processes')
        ax.set_ylabel('Speedup')
        plt.legend()
        plt.savefig('spd.jpeg',
                    dpi=300,
                    transparent=True,
                    bbox_inches = 'tight' )


    def set_sizes(self,
                  width: float,  # width of the graph
                  fraction=1) -> None:
        """set figure dimennsion"""
        fig_width_pt = width*fraction
        inches_per_pt = 1/72.27
        golden_ratio = (5**0.5 - 1)/2
        fig_width_in = fig_width_pt * inches_per_pt
        fig_height_in = fig_width_in * golden_ratio*1
        fig_dim = (fig_width_in, fig_height_in)
        return fig_dim

if __name__ == '__main__':
    data = ReadTime(sys.argv[1])
    df: pd.DataFrame = data.df  # Data to plot
    plots = PlotDf(df)
