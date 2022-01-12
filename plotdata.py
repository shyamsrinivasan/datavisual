import matplotlib.pyplot as plt


def scatterplot(data, dtype, sep=False):
    """scatter plot of temperature/humidity/heat index"""
    if sep:
        if dtype == 'all':
            fig, ax = plt.subplots(3, 1)
            dtype = ['Temperature', 'Humidity', 'Heat Index']
            for id, itype in enumerate(dtype):
                ax[id].plot(data['Time'], data[itype], ls=None, lw=0.0, marker='.')
                ax[id].set_ylabel(itype)
            ax[2].set_xlabel('Date/Time')
        else:   # len(dtype) = 1
            fig, ax = plt.subplots(1, 1)
            ax.plot(data['Time'], data[dtype], ls=None, lw=0.0, marker='.')
            ax.set_ylabel(dtype)
            ax.set_xlabel('Date/Time')
    else:
        fig, ax = plt.subplots(1, 1)
        ax.plot(data['Time'], data[dtype], ls=None, lw=0.0, marker='.')
        ax.set_xlabel('Date/Time')
        ax.set_ylabel(dtype)
    fig.show()
    print('Complete')
    return
