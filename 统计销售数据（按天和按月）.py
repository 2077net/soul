import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_excel(".\\data\\销售表.xlsx")
df =df[["日期","销售码洋"]]
print(df)
df["日期"]=pd.to_datetime(df["日期"])
df_one=df.set_index("日期",drop=True)#设置日期为索引
#按天统计销售数据
df_data=df_one.resample("D").sum().to_period("D")
df_data_1=df_one.resample("M").sum().to_period("M")
print(df_data)
print()
#设置可视化显示
plt.rc("font",family="SimHei",size=10)
fig =plt.figure(figsize=(9,5))
ax =fig.subplots(1,2)
ax[0].set_title("按天分析销售数据")
df_data.plot(ax=ax[0],color="blue")
ax[0].set_title("按月分析销售数据")
df_data_1.plot(ax=ax[1],color="green")
plt.subplots_adjust(top=0.95,bottom=0.15)
plt.show()
