import matplotlib.pyplot as plt


def scatterplot(data, dtype, sep=False):
    """scatter plot of temperature/humidity/heat index"""
    if sep:
        pass
    else:
        a = plt.plot(data['Time'], data[dtype], ls=None, lw=0.0, marker='.')
        print('Complete')
    return
