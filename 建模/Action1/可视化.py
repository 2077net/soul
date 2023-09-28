import matplotlib.pyplot as plt
import random
import random
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
plt.rcParams['font.family'] = 'SimHei'

def simulate_parameters():
    success_rate = random.uniform(0.7, 0.9)  # 种羊成功率的均匀分布
    lamb_per_birth = random.randint(1, 3)  # 分娩羔羊数量的离散分布
    lamb_mortality_rate = random.uniform(0.01, 0.05)  # 羔羊死亡率的均匀分布
    lactation_duration = random.randint(35, 45)  # 哺乳时间的离散分布
    return success_rate, lamb_per_birth, lamb_mortality_rate, lactation_duration

# 模拟参数
num_samples = 1000  # 模拟次数
success_rates = []
lamb_per_births = []
lamb_mortality_rates = []
lactation_durations = []

for _ in range(num_samples):
    success_rate, lamb_per_birth, lamb_mortality_rate, lactation_duration = simulate_parameters()
    success_rates.append(success_rate)
    lamb_per_births.append(lamb_per_birth)
    lamb_mortality_rates.append(lamb_mortality_rate)
    lactation_durations.append(lactation_duration)

# 创建子图
plt.figure(figsize=(15, 5))

# 成功率分布
plt.subplot(221)
plt.hist(success_rates, bins=20, density=True, alpha=0.7, color='b')
plt.title('成功率分布')
plt.xlabel('成功率')
plt.ylabel('概率密度')

# 分娩羔羊数量分布
plt.subplot(222)
plt.hist(lamb_per_births, bins=[1, 2, 3, 4], density=True, alpha=0.7, color='g')
plt.title('分娩羔羊数量分布')
plt.xlabel('羔羊数量')
plt.ylabel('概率密度')

# 羔羊死亡率分布
plt.subplot(223)
plt.hist(lamb_mortality_rates, bins=20, density=True, alpha=0.7, color='r')
plt.title('羔羊死亡率分布')
plt.xlabel('死亡率')
plt.ylabel('概率密度')

# 哺乳时间分布
plt.subplot(224)
plt.hist(lactation_durations, bins=[35, 40, 45, 50], density=True, alpha=0.7, color='y')
plt.title('哺乳时间分布')
plt.xlabel('哺乳时间')
plt.ylabel('概率密度')

plt.tight_layout()
plt.show()
