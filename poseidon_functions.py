import os
import math
import plotter

if __name__ == "__main__":
    x = [i*0.005 for i in range(20000)]
    y = []
    for i in x:
        if i < 0.01:
            y.append(43)
        else:
            y.append(40 * (math.log(100)-math.log(i)) / (math.log(100)-math.log(0.01)) + 3)
    dataset = [y]
    plotter.draw("line", 
                 dataset, 
                 "target.png", 
                 xylabels=["Rate per weight", "Target delay (us)"], 
                 figure_size=(4.5,4),
                 x_axis=x,
                 xscale="log",
                 markersize=0,
                 linewidth=3,
                 ylim=(0, 46),
                 xticks=[0.01, 0.1, 1, 10, 100],
                 xticks_labels=[".01", ".1", "1", "10", "100"])
    

    x = [i*0.1 for i in range(1000)]
    y = []
    for i in x[1:]:
        if i < 0.01:
            y.append(43)
        else:
            y.append(40 * (math.log(100)-math.log(i)) / (math.log(100)-math.log(0.01)) + 3)
    dataset = [y]
    plotter.draw("line", 
                 dataset, 
                 "target_part.png", 
                 xylabels=["Rate (Gbps, log-scale)", "Target QD (us)"], 
                 figure_size=(4,3.5),
                 x_axis=x[1:],
                 xscale="log",
                 markersize=0,
                 linewidth=3,
                 ylim=(-2, 35),
                 xticks=[0.1, 1, 10, 100],
                 xticks_labels=["0.1", "1", "10", "100"])
    

    x = [i*0.1-20 for i in range(400)]
    y = []
    for i in x:
        u = math.exp(1/40*i*(math.log(100)-math.log(0.01))*0.25)
        if u < 0.4:
            u = 0.4
        elif u > 2.5:
            u = 2.5
        y.append(u)
    dataset = [y]
    plotter.draw("line", 
                 dataset, 
                 "update.png", 
                 xylabels=["Target - Delay (us)", "Update ratio"], 
                 figure_size=(4.5,4),
                 x_axis=x,
                 yscale='log',
                 markersize=0,
                 linewidth=3,
                 yticks=[0.4, 0.6, 0.8, 1.0, 1.5, 2.0, 2.5],
                 yticks_labels=[0.4, 0.6, 0.8, 1.0, 1.5, 2.0, 2.5],
                 xticks=[-20, -10, 0, 10, 20],
                 xticks_labels=[-20, -10, 0, 10, 20])