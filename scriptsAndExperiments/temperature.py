import numpy as np
from matplotlib import pyplot as plt


plt.title("Probability as a function of the temperature")
plt.xlabel('T')
plt.ylabel('P')
plt.grid(True)
X = np.array([400,900,390,1000,550])
labels = X
X=X/np.amin(X)
print(X)
T=np.linespace(0.01,5,100)
list_of_sum_denominators=[]
for t in T:
    Y = np.array(np.sum(np.power(X,-1/t)))
    list_of_sum_denominators.append(Y)
sum_denominator = np.array(list_of_sum_denominators)
print(sum_denominator)
for x, label in zip(X, labels):
    Y = np.power(x, -1 / T)
    Pr=np.array(Y/sum_denominator)
    plt.plot(T,Pr, label=label)
    plt.show(block=False)
    plt.legend(bbox_to_anchor=(1, 1),
               bbox_transform=plt.gcf().transFigure)
plt.show(block=False)
plt.waitforbuttonpress()


# TODO : Write the code as explained in the instructions
