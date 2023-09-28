import pulp
from pulp import LpVariable



# 创建线性规划问题(最大化出栏羊只数）
N_cont = pulp.LpProblem("OSB", pulp.LpMaximize)
# 添加种公羊和基础母羊的数量变量
Gy = LpVariable("Gy", lowBound=0, cat="Integer")
My = LpVariable("My", lowBound=0, cat="Integer")
# 定义目标函数
N_cont += 3.1 * My - (1 / 50) * Gy

# 添加约束条件

N_cont += (1 / 14) * My + (1 / 4) * Gy <= 112
                                 #非交配期羊栏容量的约束条件。
N_cont += (1 / 14) * My <= 112  #交配期羊栏容量的约束条件。
N_cont += (1 / 8) * My <= 112   #怀孕期羊栏容量的约束条件
N_cont += (1 / 6) * My <= 112   #哺乳期羊栏容量的约束条件
N_cont += (1 / 14) * My <= 112  #育肥期羊栏容量的约束条件
N_cont += (1 / 14) * My <= 112  #休整期羊栏容量的约束条件
N_cont += Gy >= (1 / 50) * My   #种公羊与基础母羊的比例配置的约束条件
N_cont += 3.1 * My - (1 / 50) * Gy >= 1500
                                 #确保年化出栏羊只数量不低于最小值
# 求解线性规划问题
N_cont.solve()

# 计算年出栏羊只数量
N_goal = int(3.1 * int(My.varValue))


print('-------------------------------------------------------------------------------')
# 打印最优解结果
if N_cont.status == pulp.LpStatusOptimal:
    print("最优解:")
    print("种公羊数量:", int(Gy.varValue))
    print("基础母羊数量:", int(My.varValue))
    print("最大年化出栏羊只数量:", int(N_goal))
    if N_goal >= 1500:
        print("该养殖场每年出栏数量达到或超过1500只，无缺口。")
    else:
        print("该养殖场每年出栏数量不足1500只，缺口为:", 1500 - N_goal, "只羊。")

else:
    print("未找到最优解，请检查约束条件。")
print('-------------------------------------------------------------------------------')
#估算年化出栏羊只数量的范围:
# 创建线性规划问题,将最大化改为最小化
problem = pulp.LpProblem("OSB", pulp.LpMinimize)
# 定义目标函数（最小化年化出栏羊只数量）
problem += 3.1 * My - (1 / 50) * Gy
# 添加约束条件
problem += (1 / 14) * My + (1 / 4) * Gy <= 112
                                 #非交配期羊栏容量的约束条件。
problem += (1 / 14) * My <= 112  #交配期羊栏容量的约束条件。
problem += (1 / 8) * My <= 112   #怀孕期羊栏容量的约束条件
problem += (1 / 6) * My <= 112   #哺乳期羊栏容量的约束条件
problem += (1 / 14) * My <= 112  #育肥期羊栏容量的约束条件
problem += (1 / 14) * My <= 112  #休整期羊栏容量的约束条件
problem += Gy >= (1 / 50) * My   #种公羊与基础母羊的比例配置的约束条件
problem += 3.1 * My - (1 / 50) * Gy >= 1500
                                 #确保年化出栏羊只数量不低于最小值
problem.solve()
#打印结果
if problem.status == pulp.LpStatusOptimal:
    print("种公羊数量:", int(Gy.varValue))
    print("基础母羊数量:", int(My.varValue))
    N_mingoal = int(3.1* int(My.varValue))
    print("最小年化出栏羊只数量:", int(N_mingoal))
    FanWei=[N_mingoal,N_goal,]
    print("年化出栏羊只数量的范围:",FanWei)
else:
    print("No optimal solution found. Please check constraints.")