import os
import math
import plotter

MAX_RATE = 100 * 1000000000
MIN_RATE = 1 * 1000000000
MAX_DELAY = 0.0004 
MIN_DELAY = 0.00003

class Sim:
    def __init__(self, epoch, bw, delay):
        self.epoch = epoch
        self.flows = []
        self.link = Link(bw, delay)
        self.log = []

    def NextEpoch(self):
        curr_depth = self.link.queue_depth
        for f in self.flows:
            f.UpdateRate(self.link.queue_depth)
        for f in self.flows:
            self.link.enqueue(f.GetNextSendSize(self.epoch))
        self.link.dequeue(self.epoch)

        tmp_log = []
        print(self.flows[0].rate / 1000000000, self.flows[1].rate / 1000000000, self.link.queue_depth)
        for f in self.flows:
            tmp_log.append(f.rate / 1000000000)
        tmp_log.append(curr_depth)
        self.log.append(tmp_log)

    def AddFlow(self, rate, demand=100*1000000000):
        self.flows.append(Flow(rate, demand))

    def RunFor(self, epoch):
        for _ in range(epoch):
            self.NextEpoch()

class Link:
    def __init__(self, bw, qd):
        self.bandwidth = bw  # bps
        self.queue_depth = qd  # b

    def enqueue(self, data_size):
        self.queue_depth += data_size
    
    def dequeue(self, epoch):
        self.queue_depth -= self.bandwidth * epoch
        if self.queue_depth < 0:
            self.queue_depth = 0

class Flow:
    def __init__(self, sr, demand = 100 * 1000000000):
        self.rate = sr
        self.demand = demand
    
    def GetNextSendSize(self, epoch):
        return self.rate * epoch  # bps
    
    def UpdateRate(self, delay):
        r_link = math.exp(math.log(MAX_RATE) - (delay - MIN_DELAY * MAX_RATE) / (MAX_DELAY * MAX_RATE) * (math.log(MAX_RATE)-math.log(MIN_RATE)))
        
        ratio = pow(r_link / self.rate, 1)
        # ratio = r_link / self.rate
        # ratio = 1 + (ratio - 1) * 0.25

        self.rate *= ratio
        if self.rate > self.demand:
            self.rate = self.demand

def Target(rate):
    delay = (math.log(MAX_RATE) - math.log(rate)) / (math.log(MAX_RATE)-math.log(MIN_RATE)) * MAX_DELAY * MAX_RATE + MIN_DELAY * MAX_RATE
    return delay

if __name__ == "__main__":
    sim = Sim(0.00005, 100*1000000000, Target(20*1000000000))
    sim.AddFlow(20*1000000000)
    sim.AddFlow(20*1000000000)
    sim.AddFlow(20*1000000000)
    sim.AddFlow(20*1000000000)
    sim.RunFor(20)
    
    dataset = [[] for i in range(len(sim.log[-1])-1)]
    xset = [[] for i in range(len(sim.log[-1])-1)]
    for i in range(len(sim.log)):
        for j in range(len(sim.log[i])-1):
            xset[j].append(i * 0.05)
            dataset[j].append(sim.log[i][j])
    plotter.draw("line", dataset, "op_rate.png", xylabels=["Time", "Throughput (Gbps)"], figure_size=(4,3.5), linewidth=3, x_axis=xset, markersize=0,
                #  ylim=(0,52),
                #  xticks=[0,5,10],
                #  xticks_labels=["0", "T1", "T2"],
                #  yticks=[0, 10, 20, 30, 40 ,50],
                #  yticks_labels=[0, 10, 20, 30, 40, 50],
                 legends=["flow 1", "flow 2", "flow 3", "new flow"],
                 legend_fontsize=12,
                 )

    ds = [[]]
    xset = [[]]
    for i in range(len(sim.log)):
        xset[0].append(i * 0.05)
        ds[0].append(sim.log[i][-1]/MAX_RATE*1000000)
    plotter.draw("line", ds, "op_queue.png", xylabels=["Time", "Queuing delay (us)"], figure_size=(4,3.5), linewidth=3, x_axis=xset, markersize=0,
                #  ylim=(8,14),
                #  xticks=[0,5,10],
                #  xticks_labels=["0", "T1", "T2"],
                #  yticks=[8, Target(45 * 1000000000) / MAX_RATE * 1000000, 11, Target(30 * 1000000000) / MAX_RATE * 1000000, 14],
                #  yticks_labels=[8, "T(50)", 11, "T(33)", 14],
                 )

    dataset = [[] for i in range(2)]
    xset = [[] for i in range(2)]
    xenergy = [[]]
    yenergy = [[]]
    for i in range(len(sim.log)):
        for j in range(2):
            xset[j].append(i * 0.05)
        xenergy[0].append(i * 0.05)
        rate = sim.log[i][0]
        queuing = sim.log[i][-1]/MAX_RATE*1000000
        # dataset[0].append(rate*7.22)
        # dataset[1].append(queuing*3)
        # yenergy[0].append(0.58*rate*7.22 + queuing*3)
        # dataset[0].append(pow(rate,2))
        # dataset[1].append(queuing*10.39)
        # yenergy[0].append(0.289*pow(rate,2) + queuing*10.39)
        # dataset[0].append(rate*144.8)
        # dataset[1].append(pow(queuing,2))
        # yenergy[0].append(1.15*rate*144.8 + pow(queuing,2))
        dataset[0].append(math.exp(rate))
        dataset[1].append(queuing * 1200000000)
        yenergy[0].append(0.023* math.exp(rate) + queuing * 1200000000)
    plotter.draw("line", dataset, "op_both.png", xylabels=["Time", "Energy"], figure_size=(4,3.5), linewidth=3, x_axis=xset, markersize=0,
                #  ylim=(8,14),
                #  xticks=[0,5,10],
                #  xticks_labels=["0", "T1", "T2"],
                #  yticks=[8, Target(45 * 1000000000) / MAX_RATE * 1000000, 11, Target(30 * 1000000000) / MAX_RATE * 1000000, 14],
                #  yticks_labels=[8, "T(50)", 11, "T(33)", 14],
                 legends=["rate", "queuing"],
                 legend_fontsize=12,
                 )
    plotter.draw("line", yenergy, "op_energy.png", xylabels=["Time", "Energy"], figure_size=(4,3.5), linewidth=3, x_axis=xenergy, markersize=0,
                #  ylim=(8,14),
                #  xticks=[0,5,10],
                #  xticks_labels=["0", "T1", "T2"],
                #  yticks=[8, Target(45 * 1000000000) / MAX_RATE * 1000000, 11, Target(30 * 1000000000) / MAX_RATE * 1000000, 14],
                #  yticks_labels=[8, "T(50)", 11, "T(33)", 14],
                 legends=["energy"],
                 legend_fontsize=12,
                 )



    sim = Sim(0.00005, 100*1000000000, Target(50*1000000000))
    sim.AddFlow(50*1000000000)
    sim.AddFlow(50*1000000000)
    sim.RunFor(100)
    sim.AddFlow(1*1000000000)
    sim.RunFor(100)
    
    dataset = [[] for i in range(len(sim.log[-1])-1)]
    xset = [[] for i in range(len(sim.log[-1])-1)]
    for i in range(len(sim.log)):
        for j in range(len(sim.log[i])-1):
            xset[j].append(i * 0.05)
            dataset[j].append(sim.log[i][j])
    plotter.draw("line", dataset, "routopia1_rate.png", xylabels=["Time", "Throughput (Gbps)"], figure_size=(4,3.5), linewidth=3, x_axis=xset, markersize=0,
                 ylim=(0,52),
                 xticks=[0,5,10],
                 xticks_labels=["0", "T1", "T2"],
                 yticks=[0, 10, 20, 30, 40 ,50],
                 yticks_labels=[0, 10, 20, 30, 40, 50],
                 legends=["flow 1", "flow 2", "new flow"],
                 legend_fontsize=12,
                 )

    ds = [[]]
    xset = [[]]
    for i in range(len(sim.log)):
        xset[0].append(i * 0.05)
        ds[0].append(sim.log[i][-1]/MAX_RATE*1000000)
    plotter.draw("line", ds, "routopia1_queue.png", xylabels=["Time", "Queuing delay (us)"], figure_size=(4,3.5), linewidth=3, x_axis=xset, markersize=0,
                 ylim=(8,14),
                 xticks=[0,5,10],
                 xticks_labels=["0", "T1", "T2"],
                 yticks=[8, Target(50 * 1000000000) / MAX_RATE * 1000000, 11, Target(100 / 3 * 1000000000) / MAX_RATE * 1000000, 14],
                 yticks_labels=[8, "T(50)", 11, "T(33)", 14],
                 )



    sim = Sim(0.00005, 100*1000000000, Target(45*1000000000))
    sim.AddFlow(45*1000000000)
    sim.AddFlow(45*1000000000)
    sim.AddFlow(10*1000000000, 10 * 1000000000)
    sim.RunFor(100)
    sim.flows[2].demand = 100 * 1000000000
    sim.RunFor(100)
    
    dataset = [[] for i in range(len(sim.log[-1]))]
    xset = [[] for i in range(len(sim.log[-1]))]
    for i in range(len(sim.log)):
        for j in range(len(sim.log[i])-1):
            xset[j].append(i * 0.05)
            dataset[j].append(sim.log[i][j])

    dataset[3].append(1)
    xset[3].append(99 * 0.05)
    for i in range(len(dataset[2])):
        if i >= 100:
            dataset[3].append(dataset[2][i])
            xset[3].append(xset[2][i])
        dataset[2][i] = 10
    plotter.draw("line", dataset, "routopia3_rate.png", xylabels=["Time", "Throughput (Gbps)"], figure_size=(4,3.5), linewidth=3, x_axis=xset, markersize=0,
                 ylim=(0,52),
                 xticks=[0,5,10],
                 xticks_labels=["0", "T1", "T2"],
                 yticks=[0, 10, 20, 30, 40 ,50],
                 yticks_labels=[0, 10, 20, 30, 40, 50],
                 legends=["flow 1", "flow 2", "flow 3", "new flow"],
                 legend_fontsize=12,
                 )

    ds = [[]]
    xset = [[]]
    for i in range(len(sim.log)):
        xset[0].append(i * 0.05)
        ds[0].append(sim.log[i][-1]/MAX_RATE*1000000)
    plotter.draw("line", ds, "routopia3_queue.png", xylabels=["Time", "Queuing delay (us)"], figure_size=(4,3.5), linewidth=3, x_axis=xset, markersize=0,
                 ylim=(8,14),
                 xticks=[0,5,10],
                 xticks_labels=["0", "T1", "T2"],
                 yticks=[8, Target(45 * 1000000000) / MAX_RATE * 1000000, 11, Target(100 / 3 * 1000000000) / MAX_RATE * 1000000, 14],
                 yticks_labels=[8, "T(45)", 11, "T(33)", 14],
                 )