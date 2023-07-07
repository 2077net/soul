import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model

df_1 = pd.read_excel(".\data\广告费.xlsx")
df_2 = pd.read_excel(".\data\销售表.xlsx")

df_1["投放日期"] = pd.to_datetime(df_1["投放日期"])
df_1 = df_1.set_index("投放日期", drop=True)
df_2 = df_2[["日期", "销售码洋"]]
df_2["日期"] = pd.to_datetime(df_2["日期"])
df_2 = df_2.set_index("日期", drop=True)
# 按月统计总额
df_x = df_1.resample("M").sum().to_period("M")  # 广告投入
df_y = df_2.resample("M").sum().to_period("M")  # 销售收入
# x=广告费，y=销售收入
x = pd.DataFrame(df_x["支出"])
y = pd.DataFrame(df_y["销售码洋"])
print(x)
print(y)
# 建模分析
model = linear_model.LinearRegression()  # 线性回归模型
model.fit(x, y)
y_pre = model.predict(x)
plt.rc("font", family="SimHei", size=10)
plt.figure("电商平台销售数据分析预测")
plt.scatter(x, y, color="blue")
plt.plot(x, y_pre, color="black")
plt.xlabel("广告费")
plt.ylabel("销售收入")
plt.subplots_adjust(left=0.2)
plt.show()
data = np.array([150000,100000])
data = data.reshape(2, 1)
print("销售预测",model.predict(data))