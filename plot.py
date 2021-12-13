import matplotlib.pyplot  as plt

FUN_DIR="./results/NSGAII/run1/FUN.NSGAII.BeamNGProblem"
VAR_DIR="./results/NSGAII/run1/VAR.NSGAII.BeamNGProblem"
fun_file=open(FUN_DIR,'r')
var_file=open(VAR_DIR,'r')
changedParams=[]
initial = [7000, 0.14, 44, 1, 3000, 1550,  0.325]
lower_bound = [6000, 0.1, 30, 0.8, 2500, 1250, 0.3]
upper_bound = [8000, 0.18, 60, 1.2, 3500, 1850, 0.35]
numLines=0
changeTimes=[0]*len(initial)
changePercent=[0]*len(initial)
for fun_line in fun_file:
    var_line=var_file.readline()
    params=var_line.split()
    objectives=fun_line.split()
    paramIndex=[0]*len(initial)
    numLines += 1
    for i in range(len(initial)):
        original = initial[i]
        deviation = abs(float(params[i]) - original)
        width = upper_bound[i] - lower_bound[i]
        change_precision = deviation / width
        change_ratio = deviation / original

        # precision A
        if (width >= 1000):
            beta = 0.005
        elif (width >= 100):
            beta = 0.01
        elif (width >= 1):
            beta = 0.02
        else:
            beta = 0.04
        if change_precision >= beta:
            paramIndex[i]+=1
            changeTimes[i]+=1
    changedParams.append(paramIndex)
# print(changedParams)
print(changeTimes)
for i in range(len(initial)):
    changePercent[i]=changeTimes[i]/numLines
print(changePercent)

# plt.boxplot(changedParams)
# plt.show()