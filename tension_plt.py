import sys
import matplotlib.pylab as plt
import pandas as pd
import matplotlib

def read_data(fname) -> pd.DataFrame:
    columns = ['TimeStep', 'v_Tension']
    df = pd.read_csv(fname, sep=' ', names=columns, skiprows=2)
    return df

def atom_to_newton(df) -> pd.DataFrame:
    atom_newton = 101325
    angestrom = 1e-10
    m_to_mili = 1e-3
    fms_to_ns = 1e-5
    df['v_Tension'] = -1 * df['v_Tension']*atom_newton*angestrom/m_to_mili
    df['TimeStep'] = df['TimeStep']*fms_to_ns
    return df


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
        plt.plot(self.df['TimeStep'],
                 self.df['v_Tension'],
                 label=self.name,
                 color = self.color
                 )
        self.axis()
        plt.legend()

    def axis(self) -> None:
        """set axis lables, ranges, ..."""
        plt.xlabel(r'time (ns)', fontsize=13)
        plt.ylabel(r'tension ($mN.m^{-1}$)', fontsize=13)


fname = sys.argv[1]
_df = read_data(fname)
df = atom_to_newton(_df)

plt.figure(figsize=(16/3, 3), dpi=180)
font = {'weight' : 'normal',
        'size'   : 13}
matplotlib.rc('font', **font)

colors = ['red', 'black', 'blue', 'grey']
outname: str = 'npt.png'
plot = PlotRdf(df, 'water/decane', colors[3])
plot.plot_df()
plt.tight_layout()
plt.savefig('tension.png', transparent=True)
plt.show()
