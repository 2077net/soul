import pandas as pd
import  matplotlib.pyplot as plt
df_1 = pd.read_excel(".\data\广告费.xlsx")
df_2 = pd.read_excel(".\data\销售表.xlsx")
print(df_1)
print(df_2)
df_1["投放日期"]=pd.to_datetime(df_1["投放日期"])
df_1=df_1.set_index("投放日期",drop=True)
df_2=df_2[["日期","销售码洋"]]
df_2["日期"]=pd.to_datetime(df_2["日期"])
df_2=df_2.set_index("日期",drop=True)
#按月统计总额
df_x=df_1.resample("M").sum().to_period("M")#广告投入
df_y=df_2.resample("M").sum().to_period("M")#销售收入
#x=广告费，y=销售收入
x=pd.DataFrame(df_x["支出"])
y=pd.DataFrame(df_y["销售码洋"])
#可视化
plt.rc("font",family="SimHei",size=11)
plt.figure("xx电商平台销售收入与广告投入分析")
plt.scatter(x,y,color='blue')
plt.xlabel("广告费")
plt.ylabel("销售收入")
plt.subplots_adjust(left=0.15)
plt.show()
