import pulp
from pulp import LpVariable

# 时间段列表
time = ["No_Breeding", "Breeding", "Pregnancy", "Milk", "Fattening", "Rest"]

# 羊栏容量限制
max_ewe_pens = 112

# 创建线性规划问题
problem = pulp.LpProblem("OptimalSheepBreeding", pulp.LpMaximize)

# 定义变量
G = {}  # 字典，存储每个时间段内的种公羊数量
M = {}  # 字典，存储每个时间段内的基础母羊数量
L = {}  # 字典，存储每个时间段内的羔羊数量
for t in time:
    G[t] = pulp.LpVariable(f"Number_of_Rams_{t}", lowBound=0, cat=pulp.LpInteger)
    M[t] = pulp.LpVariable(f"Number_of_Ewes_{t}", lowBound=0, cat=pulp.LpInteger)
    L[t] = pulp.LpVariable(f"Number_of_Lambs_{t}", lowBound=0, cat=pulp.LpInteger)

# 定义目标函数
# 最大化年化出栏羊只数量
problem += pulp.lpSum(3.1 * L[t] for t in time[2:5])

# 添加约束条件
for t in time:
    # 种公羊与基础母羊的比例约束
    problem += G[t] >= (1 / 50) * M[t]

    # 羊栏容量约束
    if t == "No_Breeding":
        problem += (1 / 14) * M[t] + (1 / 4) * G[t] <= max_ewe_pens
    elif t == "Breeding":
        problem += (1 / 14) * M[t] <= max_ewe_pens
    elif t == "Pregnancy":
        problem += (1 / 8) * M[t] <= max_ewe_pens
    elif t == "Nursing":
        problem += (1 / 6) * M[t] <= max_ewe_pens
    elif t == "Fattening":
        problem += (1 / 14) * L[t] <= max_ewe_pens
    elif t == "Rest":
        problem += (1 / 14) * L[t] <= max_ewe_pens

    # 受孕率约束
    if t == "Breeding":
        problem += M[t] <= 0.95 * M["No_Breeding"]

    # 羔羊数量约束
    if t == "Pregnancy":
        problem += L[t] == 3.1 * 0.70 * M["Breeding"]

    # 羔羊夭折率约束
    if t != "No_Breeding" and t != "Breeding":
        problem += L[t] >= 0.85 * L[time[time.index(t) - 1]]
    if t != "No_Breeding":
        problem += M[t] >= 0.01 * M["No_Breeding"]
        problem += L[t] >= 0.01 * L["No_Breeding"]
# 添加最优解约束
problem += G['No_Breeding'] == 14
problem += M['No_Breeding'] == 672
problem += L['No_Breeding'] == 0

# 解决线性规划问题
problem.solve()

# 打印结果和生产计划
if problem.status == pulp.LpStatusOptimal:
    print("Optimal Solution Found:")
    for t in time:
        print(f"时间段 {t}:")
        print(f"公羊数量 (G): {int(G[t].varValue)}")
        print(f"母羊数量 (M): {int(M[t].varValue)}")
        print(f"羔羊数量 (L): {int(L[t].varValue)}")
    # 计算年化出栏羊只数量
    annual_lambs = sum(int(L[t].varValue) for t in time[2:5])
    print("年化出栏羊只数量:", annual_lambs)
else:
    print("No optimal solution found. Please check constraints.")
# 创建字典存储每个时间段内需要的羊栏数量
pen_capacity = {}
for t in time:
    if t == "No_Breeding":
        pen_capacity[t] = (1 / 14) * int(M[t].varValue) + (1 / 4) * int(G[t].varValue)
    elif t == "Breeding":
        pen_capacity[t] = (1 / 14) * int(M[t].varValue)
    elif t == "Pregnancy":
        pen_capacity[t] = (1 / 8) * int(M[t].varValue)
    elif t == "Milk":
        pen_capacity[t] = (1 / 6) * int(M[t].varValue)
    elif t == "Fattening":
        pen_capacity[t] = (1 / 14) * int(L[t].varValue)
    elif t == "Rest":
        pen_capacity[t] = (1 / 14) * int(L[t].varValue)

# 创建字典存储每个时间段内羊栏内的公羊、母羊和羔羊的数量配置
pen_allocation = {}
for t in time:
    pen_allocation[t] = {
        "rams": int(G[t].varValue),
        "ewes": int(M[t].varValue),
        "lambs": int(L[t].varValue)
    }

# 打印每个时间段内的羊栏容量和配置
for t in time:
    print(f"时间段 {t}:")
    print(f"羊栏容量: {int(pen_capacity[t])} 栏")
    print(f"羊栏内配置:")
    print(f"公羊数量: {pen_allocation[t]['rams']}")
    print(f"母羊数量: {pen_allocation[t]['ewes']}")
    print(f"羔羊数量: {pen_allocation[t]['lambs']}")
    print("--------------")
