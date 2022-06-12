from doctest import register_optionflag
from numpy import arange
from matplotlib import pyplot
from scipy.stats import norm
import matplotlib.pyplot as plt


def main(scenario):
    issuelist={}

    """
    for i in scenario.regions:
        for j in i.issues:
            issuelist.append({str(j.issue.name + "-" + i.name):(j.mean, j.variance, j.importance)})

    for i in scenario.parties:
        for j in i.issues:
            issuelist.append({str(j.issue.name + "-" + i.name):(j.mean, j.variance)})
    """

    for i in scenario.issues:
        for j in i.parties:
            if i.name in issuelist:
                issuelist[i.name][j.party.name]=(j.mean, j.variance)

            else:
                issuelist[i.name]={}
                issuelist[i.name][j.party.name]=(j.mean, j.variance)
        for j in i.regions:
            if i.name in issuelist:
                issuelist[i.name][j.region.name]=(j.mean, j.variance, j.importance)

            else:
                issuelist[i.name]={}
                issuelist[i.name][j.region.name]=(j.mean, j.variance, j.importance)

    #print(issuelist)

    """
    for i in scenario.issues:
        for j in i.regions:
            x_regionalaxis=arange(-10, 10, 0.01)
            print(j.mean, j.variance)
            y_regionalaxis=norm.pdf(x_regionalaxis, j.mean, j.variance)
            y_regionalaxis=y_regionalaxis*(j.region.population/sum(y_regionalaxis))

            curve1,= plt.plot(y_regionalaxis,y_regionalaxis)
            curve1.set_color("black")   
            print("Population: " + str(round(sum(y_regionalaxis))))

    for i in scenario.parties:

        print(i.name)
    """