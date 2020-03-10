'''code to simulate PM2.5 concentrations (ug/m3)  in UK'''

# import required modules
import numpy as np
import matplotlib.pyplot as plt

# time array (24 hour period, every 10 minutes)
time = np.linspace(0.0, 24.0, num=24.0*6.0)

# nearby emissions based on traffic and domestic heating emissions
# traffic
traff_contr = np.sin((time/24.0)*(np.pi*5.0)+(np.pi*(3/4)))
# double amplitude of sin function
traff_contr = traff_contr*2.0
# modify sin function by shifting all values upwards by same amount
traff_contr += 2.5
# minimum level from traffic during night time
quiet_traff_time = time<6.0
quiet_traff_time += time>22.0
traff_contr[quiet_traff_time] = 0.1

plt.plot(time, traff_contr)
plt.show()
