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
y1=pd.DataFrame(df_x["支出"])
y2=pd.DataFrame(df_y["销售码洋"])
#可视化
fig = plt.figure()
plt.rc("font",family="SimHei",size=11)
ax_1=fig.add_subplot(111)
plt.title("电商平台销售收入与广告投入分析line图")
x=[0,1,2,3,4,5,6,7,8,9,10,11]
plt.xticks(x,["1月","2月","3月","4月","5月","6月","7月","8月","9月","10月","11月","12月"])
ax_1.plot(x,y1,color="blue",linewidth=2,linestyle="-",marker="o",label="广告费")
plt.legend(loc="upper left")
ax_2=ax_1.twinx()#添加坐标轴
ax_2.plot(x,y2,color="red",linewidth=2,linestyle="--",marker="o",label="销售收入")
plt.subplots_adjust(right=0.83)
plt.legend(loc="upper center")
plt.show()
