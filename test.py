import numpy as np 
import matplotlib.pyplot as plt

def f(x,y):
    r_anchor = np.exp(np.log(200) - (y - 3 * 200) / (40 * 200) * (np.log(200)-np.log(0.2)))
    return pow(r_anchor / x, 0.25)
    # return (np.exp(np.log(200)-y) / x)**(0.25)


R_list = [0.2]
B = 12
for i in range(1,1000):
    R_list.append(R_list[i-1] * f(R_list[i-1], np.sum(R_list)-len(R_list)*B) )

print(R_list)
plt.plot(np.arange(1000), R_list)
plt.show()