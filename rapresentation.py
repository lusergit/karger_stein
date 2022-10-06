import csv
import os
import numpy as np
import matplotlib.pyplot as plt

# Result rapresentation

# All the functions defined here want the data as a list of tuples in
# the form
# `(name, time, discovery time, #vertices, #edges, solution)`


def print_table(data):
    fstr = "{:<25}{:<12}{:<12}{:<15}{:<15}{:<13}"
    print(fstr.format("name", "time", "d_time", "n_vertices", "n_edges", "sol"))
    print("-"*80)
    for (afile, time, d_time, sol, n, m) in data:
        print(fstr.format(afile, time, d_time, n, m, sol))


def write_to_csv(data, file_name):
    with open(file_name, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)


def read_csv(file_name):
    tmp = []
    to_ret = []
    with open(file_name, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            tmp += (tuple(row),)
    for (afile, time, d_time, n, m, sol) in to_ret:
        to_ret += [(afile, int(time), int(d_time), int(n), int(m), int(sol))]
    return to_ret


def ks_complex(n):
    return (n**2)*(np.log(n) ** 3)

def sw_complex(n,m):
    return (n*m) + ((n**2)*np.log(n))

def save_plot(name):
    run_path = "figs"
    # mkdir for figures if not available
    os.makedirs(run_path, exist_ok=True)
    to_save = os.path.join(run_path, "{}.png".format(name))
    plt.savefig(to_save, format='png', transparent=True, dpi=300)
    print("Saved plot to {}".format(to_save))

def plot3D(data, alg_name, f):
    print("Plotting ...")
    times = [time for (afile, time, d_time, sol, n, m) in data]
    n = [n for (afile, time, d_time, sol, n, m) in data]
    m = [m for (afile, time, d_time, sol, n, m) in data]
    
    limit = max(max(n), max(m))
    x = np.linspace(0, limit, 100)
    y = np.linspace(0, limit, 100)
    X, Y = np.meshgrid(x,y)
    c = max([t / f(n,m) for t, n, m in zip(times, n, m)])
    Z = c*f(X,Y)

    # Close other active plots
    plt.clf()
    plt.cla()
    plt.close()
    
    # New plot
    ax = plt.axes(projection='3d')
    ax.plot_surface(X, Y, Z, cmap='PiYG', alpha=0.5)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z');

    ax.scatter(n,m,times, label="{} runs".format(alg_name))
    ax.legend()
    save_plot(alg_name)

def plot(data, alg_name, f):
    print("Plotting ...")
    times = [time for (afile, time, d_time, sol, n, m) in data]
    n = [n for (afile, time, d_time, sol, n, m) in data]

    # calc coefficent in order to see a better function
    c = max([t / f(n) for t, n in zip(times, n)])

    # plot against n^2(log n)^3
    x = range(max(n) + 1)
    y = [c*f(n) for n in x]
    
    # Close other active plots
    plt.clf()
    plt.cla()
    plt.close()
    
    # New plot
    ax = plt.gca()
    ax.scatter(n, times, label="{} runs".format(alg_name))

    ax.plot(x, y, 'y', label='complexity function')
    ax.legend()
    plt.xlabel("input nodes")
    plt.ylabel("run time")
    save_plot(alg_name)