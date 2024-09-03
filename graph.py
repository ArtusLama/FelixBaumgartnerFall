import matplotlib.pyplot as plt


def plot_graph(x, y, title, x_label, y_label):
    plt.figure()
    plt.plot(x, y, label=title)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(linestyle='--')
    plt.show()
