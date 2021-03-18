# import matplotlib.pyplot as plt
# import matplotlib.cbook as cbook
# import matplotlib.dates as mdate
# import matplotlib.ticker as mtick
# import time
# import numpy as np
# import pandas as pd

# stations = ['ST102', 'ST105']

# df_rawData = pd.read_csv('rawdata.csv')

# #  a list with all the data, if there were multiple devices, this would not be efficient solution
# ST102_data = []
# ST105_data = []

# for ind in df_rawData.index:
#     if(df_rawData['StationID'][ind] == "ST102"):
#         print("Station 102 Here")
#         data_entry = (df_rawData['timestamp'][ind],df_rawData['pm10'][ind],df_rawData['pm2_5'][ind],df_rawData['so2'][ind])
#         ST102_data.append(data_entry)
#     else:
#         print("Station 105 Here")
#         data_entry = (df_rawData['timestamp'][ind],df_rawData['pm10'][ind],df_rawData['pm2_5'][ind],df_rawData['so2'][ind])
#         ST105_data.append(data_entry)


# # print(ST102_data)
# # print(ST105_data)

# ST102_fig, (ST102_ax_pm10,ST102_ax_pm2_5,ST102_ax_so2) = plt.subplots(3,sharex=True)
# ST102_x_times = []
# ST102_pm10 = []
# ST102_pm2_5 = []
# ST102_so2 = []

# for data in ST102_data:
#     ST102_x_times.append(data[0])
#     # index 1 is pm10
#     ST102_pm10.append(data[1])
#     # index 2 is pm2_5
#     ST102_pm2_5.append(data[2])
#     # index 3 is so2
#     ST102_so2.append(data[3])

# # create subplot for pm10
# ST102_ax_pm10.set_title("ST102 pm10 raw data")
# ST102_ax_pm10.plot(ST102_x_times,ST102_pm10)
# # create subplot for pm2_5
# ST102_ax_pm2_5.set_title("ST102 pm2_5 raw data")
# ST102_ax_pm2_5.plot(ST102_x_times,ST102_pm2_5)
# # create subplot for so2
# ST102_ax_so2.set_title("ST102 so2 raw data")
# ST102_ax_so2.plot(ST102_x_times,ST102_so2)

# plt.gcf().autofmt_xdate()

# plt.gca().xaxis.set_major_locator(mtick.FixedLocator(ST102_x_times))
# plt.gca().xaxis.set_major_formatter(
#     mtick.FuncFormatter(lambda pos,_: time.strftime("%d-%m-%Y %H:%M:%S",time.localtime(pos)))
#     )
# plt.tight_layout()

# # plt.show()




# ST105_fig, (ST105_ax_pm10,ST105_ax_pm2_5,ST105_ax_so2) = plt.subplots(3,sharex=True)
# ST105_x_times = []
# ST105_pm10 = []
# ST105_pm2_5 = []
# ST105_so2 = []

# for data in ST105_data:
#     ST105_x_times.append(data[0])
#     # index 1 is pm10
#     ST105_pm10.append(data[1])
#     # index 2 is pm2_5
#     ST105_pm2_5.append(data[2])
#     # index 3 is so2
#     ST105_so2.append(data[3])

# # create subplot for pm10
# ST105_ax_pm10.set_title("ST105 pm10 raw data")
# ST105_ax_pm10.plot(ST105_x_times,ST105_pm10)
# # create subplot for pm2_5
# ST105_ax_pm2_5.set_title("ST105 pm2_5 raw data")
# ST105_ax_pm2_5.plot(ST105_x_times,ST105_pm2_5)
# # create subplot for so2
# ST105_ax_so2.set_title("ST105 so2 raw data")
# ST105_ax_so2.plot(ST105_x_times,ST105_so2)

# plt.gcf().autofmt_xdate()

# plt.gca().xaxis.set_major_locator(mtick.FixedLocator(ST105_x_times))
# plt.gca().xaxis.set_major_formatter(
#     mtick.FuncFormatter(lambda pos,_: time.strftime("%d-%m-%Y %H:%M:%S",time.localtime(pos)))
#     )
# plt.tight_layout()

# plt.show()


import numpy as np
import matplotlib.pyplot as plt

plt.axis([0, 10, 0, 1])

i = 0
while(True):
    y = np.random.random()
    plt.scatter(i, y)
    i = i + 1
    plt.pause(2)

plt.show()
