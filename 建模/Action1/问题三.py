import random
import pulp
from pulp import LpVariable

# 模拟参数的概率分布
def simulate_parameters():
    success_rate = random.uniform(0.7, 0.9)  # 种羊成功率的均匀分布
    lamb_per_birth = random.randint(1, 3)  # 分娩羔羊数量的离散分布
    lamb_mortality_rate = random.uniform(0.01, 0.05)  # 羔羊死亡率的均匀分布
    lactation_duration = random.randint(35, 45)  # 哺乳时间的离散分布
    return success_rate, lamb_per_birth, lamb_mortality_rate, lactation_duration

# 问题一模型
def problem_one_model(success_rate, lamb_per_birth, lamb_mortality_rate, lactation_duration):
    # 创建线性规划问题(最大化出栏羊只数）
    N_cont = pulp.LpProblem("OSB", pulp.LpMaximize)
    # 添加种公羊和基础母羊的数量变量
    Gy = LpVariable("Gy", lowBound=0, cat="Integer")
    My = LpVariable("My", lowBound=0, cat="Integer")
    # 定义目标函数
    N_cont += 3.1 * My - (1 / 50) * Gy

    # 添加约束条件
    N_cont += (1 / 14) * My + (1 / 4) * Gy <= 112
    N_cont += (1 / 14) * My <= 112
    N_cont += (1 / 8) * My <= 112
    N_cont += (1 / 6) * My <= 112
    N_cont += (1 / 14) * My <= 112
    N_cont += (1 / 14) * My <= 112
    N_cont += Gy >= (1 / 50) * My
    N_cont += 3.1 * My - (1 / 50) * Gy >= 1500

    # 求解线性规划问题
    N_cont.solve()

    # 计算年出栏羊只数量
    N_goal = int(3.1 * int(My.varValue))
    return N_goal

# 问题二模型
def problem_two_model(success_rate, lamb_per_birth, lamb_mortality_rate, lactation_duration):
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
    problem += pulp.lpSum(3.1 * L[t] for t in time[2:5])

    # 添加约束条件
    for t in time:
        problem += G[t] >= (1 / 50) * M[t]

        if t == "No_Breeding":
            problem += (1 / 14) * M[t] + (1 / 4) * G[t] <= max_ewe_pens
        elif t == "Breeding":
            problem += (1 / 14) * M[t] <= max_ewe_pens
        elif t == "Pregnancy":
            problem += (1 / 8) * M[t] <= max_ewe_pens
        elif t == "Milk":
            problem += (1 / 6) * M[t] <= max_ewe_pens
        elif t == "Fattening":
            problem += (1 / 14) * L[t] <= max_ewe_pens
        elif t == "Rest":
            problem += (1 / 14) * L[t] <= max_ewe_pens

        if t == "Breeding":
            problem += M[t] <= 0.95 * M["No_Breeding"]

        if t == "Pregnancy":
            problem += L[t] == 3.1 * 0.70 * M["Breeding"]

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

    # 计算年化出栏羊只数量
    annual_lambs = sum(int(L[t].varValue) for t in time[2:5])
    return annual_lambs

# 模拟多个场景
num_scenarios = 210  # 模拟的场景数
results = []

for _ in range(num_scenarios):
    success_rate, lamb_per_birth, lamb_mortality_rate, lactation_duration = simulate_parameters()


    production_plan = problem_one_model(success_rate, lamb_per_birth, lamb_mortality_rate, lactation_duration)


    space_requirements = problem_two_model(success_rate, lamb_per_birth, lamb_mortality_rate, lactation_duration)

    results.append((success_rate, lamb_per_birth, lamb_mortality_rate, lactation_duration, production_plan, space_requirements))

# 风险分析
# 计算年化出栏羊只数量的均值和标准差
mean_annual_output = sum(result[-2] for result in results) / num_scenarios
std_deviation_annual_output = (sum((result[-2] - mean_annual_output) ** 2 for result in results) / num_scenarios) ** 0.5

# 计算风险度量，如VaR或CVaR
alpha = 0.05  # 置信水平
sorted_outputs = sorted(result[-2] for result in results)
var_annual_output = sorted_outputs[int(alpha * num_scenarios)]
cvar_annual_output = sum(output for output in sorted_outputs if output <= var_annual_output) / (alpha * num_scenarios)

print("平均年羔羊产量:", mean_annual_output)
print("羔羊年产量标准差:", std_deviation_annual_output)
print(f"VaR ({alpha * 100}%):", var_annual_output)
print(f"CVaR ({alpha * 100}%):", cvar_annual_output)
# 问题三模型
def problem_three_model(success_rate, lamb_per_birth, lamb_mortality_rate, lactation_duration):
    # 创建线性规划问题(最大化出栏羊只数）
    N_cont = pulp.LpProblem("OSB", pulp.LpMaximize)
    # 添加种公羊和基础母羊的数量变量
    Gy = LpVariable("Gy", lowBound=0, cat="Integer")
    My = LpVariable("My", lowBound=0, cat="Integer")
    # 定义目标函数
    N_cont += 3.1 * My - (1 / 50) * Gy

    # 添加约束条件
    N_cont += (1 / 14) * My + (1 / 4) * Gy <= 112
    N_cont += (1 / 14) * My <= 112
    N_cont += (1 / 8) * My <= 112
    N_cont += (1 / 6) * My <= 112
    N_cont += (1 / 14) * My <= 112
    N_cont += (1 / 14) * My <= 112
    N_cont += Gy >= (1 / 50) * My
    N_cont += 3.1 * My - (1 / 50) * Gy >= 1500

    # 求解线性规划问题
    N_cont.solve()

    # 计算年出栏羊只数量
    N_goal = int(3.1 * int(My.varValue))
    return N_goal

# 模拟参数的概率分布
success_rate, lamb_per_birth, lamb_mortality_rate, lactation_duration = simulate_parameters()

# 使用模型求解问题一
result_problem_one = problem_one_model(success_rate, lamb_per_birth, lamb_mortality_rate, lactation_duration)

# 使用模型求解问题二
result_problem_two = problem_two_model(success_rate, lamb_per_birth, lamb_mortality_rate, lactation_duration)

# 使用模型求解问题三
result_problem_three = problem_three_model(success_rate, lamb_per_birth, lamb_mortality_rate, lactation_duration)

# 输出结果
print("问题一：最大化出栏羊只数")
print("年出栏羊只数量：", result_problem_one)

print()

print("问题二：最大化羔羊出栏总重量")
print("羔羊出栏总数量：", result_problem_two)

print()

print("问题三：最大化出栏羊只数，考虑死亡率和哺乳时间")
print("年出栏羊只数量：", result_problem_three)