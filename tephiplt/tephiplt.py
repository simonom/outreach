'''script to demonstrate the equations underlying the tephigram'''
# based on EART23001: Atmospheric Physics and Weather (University of Manchester)
# Simon O'Meara 2020: simon.omeara@manchester.ac.uk
# other helpful resource(s): http://homepages.see.leeds.ac.uk/~chmjbm/arran/radiosondes.pdf

# -----------------------------------------------------------------------------------
# dependencies
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.transforms import Affine2D
import matplotlib.ticker as ticker
import ipdb
import scipy.constants as si
import math

# ------------------------------------------------------------------------------------
fig1, ax1 = plt.subplots() # initiate plot

# the anti-clockwise transformation needed to rotate plots away
# from conventional design of orthogonal with respect to screen
# angle - note this enables pressure to decrease with vertical in
# plot
trans = Affine2D().rotate_deg(315)
trans_data = trans + ax1.transData

# set temperature ranges & interval (oC) --------------------------------
Tmin = -120. # minimum
Tmax = 120. # maximum
Tint = 10. # interval within temperature range (oC and K)

# ------------------------------------------------------------------------------------
# temperature range (oC)
T_oC = (np.arange(Tmin, Tmax+0.1, Tint)).reshape(1, -1)

# potential temperature range (oC)
theta_oC = (np.arange(Tmax, Tmin-0.1, -Tint)).reshape(-1, 1)

# repeat temperatures over a matrix of changing potential
# temperature in rows and changing temperature in columns
T_oC = np.repeat(T_oC, theta_oC.shape[0], axis=0)
theta_oC = np.repeat(theta_oC, T_oC.shape[1], axis=1)

# first plot (just T and potential temperature lines) -------------------
# the isotherms to plot
Tlevels = np.arange(Tmin, Tmax+0.1, Tint)

# plotting temperature contours
tephi0 = ax1.contour(T_oC, theta_oC, T_oC, Tlevels, colors = 'black', linewidths = 0.5, linestyles = 'solid', transform = trans_data)

# contour labels
labels = [] # empty contour labels list
for it in range(len(Tlevels)):
	labels.append(str(r'T=%s $\rm{^oC}$') %Tlevels[it])
fmt2 = {}
for l, s in zip(tephi0.levels[0::2], labels[0::2]):
    fmt2[l] = s
ax1.clabel(tephi0, tephi0.levels[0::2], inline = False, fmt = fmt2, fontsize = 10)


# plotting potential temperature contours
tephi0 = ax1.contour(T_oC, theta_oC, theta_oC, Tlevels, colors = 'black', linewidths = 0.5,  linestyles = 'solid', transform = trans_data)

# contour labels
labels = [] # empty contour labels list
for it in range(len(Tlevels)):
	labels.append(str(r'$\rm{\theta}$=%s $\rm{^oC}$') %Tlevels[it])
fmt2 = {}
for l, s in zip(tephi0.levels[0::2], labels[0::2]):
   fmt2[l] = s
ax1.clabel(tephi0, tephi0.levels[0::2], inline=False, fmt=fmt2, fontsize=10)

ax1.set_ylim([-5, 100])
ax1.set_xlim([-70, 60])
# turn off ticks on axis
plt.tick_params(axis = 'both', which = 'both', bottom = 0, left = 0, labelbottom = 0, labelleft = 0)
plt.draw()
plt.pause(1) # pause

# calculating pressures based on combinations of 
# temperature and potential temperature -------------------------------------

T_K = T_oC+273.15 # convert to K
theta_K = theta_oC+273.15 # convert to K

# ratio of specific heat capacity at constant pressure to 
# specific heat capacity at constant volume for dry air
gamma = 1.4

# pressure at temperature-potential temperature combination
# recall: theta = T(1.e3./P)**((gamma-1.)/gamma), where T in K, P in hPa 
# and gamma is ratio of specific heat capacity at constant pressure to 
# specific heat capacity at constant volume for dry air
P = 1.e3/((theta_K/T_K)**(gamma/(gamma-1)))

# second plot (just pressure = 1000 hPa) ---------------------------------------
# note 1000 hPa is treated here as the pressure representative of the Earth surface
levels = np.arange(1000., 1001., 100) # the isobar(s) to display
# plot pressure as contour lines
tephi1 = ax1.contour(T_oC, theta_oC, P, levels, colors = 'green', transform = trans_data)

# contour labels
fmt2 = {} # empty dictionary
labels = ['1000 hPa' ]
for l, s in zip(tephi1.levels, labels):
    fmt2[l] = s
ax1.clabel(tephi1, tephi1.levels, inline = True, fmt = fmt2, fontsize = 10)

plt.draw()
plt.pause(1) # pause presentation

# third plot (all pressures (hPa)) ---------------------------------------------
levels = np.arange(3.e2, 9.01e2, 1e2) # the isobar(s) to display
# plot pressure as contour lines
tephi2 = ax1.contour(T_oC, theta_oC, P, levels, colors = 'green', transform = trans_data)

# contour labels
fmt2 = {} # empty dictionary
labels = ['300 hPa', '400 hPa', '500 hPa', '600 hPa', '700 hPa', '800 hPa', '900 hPa']
for l, s in zip(tephi2.levels[1::2], labels[1::2]):
    fmt2[l] = s
ax1.clabel(tephi2, tephi2.levels[1::2], inline = True, fmt = fmt2, fontsize = 10)

plt.draw()
plt.pause(1) # pause

# fourth plot (wet bulb potential temperature (oC)) --------------------
# latent heat of vapourisation (J/kg) for water as a function of temperature
# doi.org/10.1002/qj.49711046626
Lw = 1.91846e6*(T_K/(T_K-33.91))**2.
Rw = 462. # J/kg.K energy per unit mass of water vapour per unit temperature
# ratio of latent heat of vapourisation to R
A = -Lw/Rw
# reference saturation vapour pressure at 0 oC (hPa) (Dry and Moist Air lecture)
esvp0 = 6.1
exp0 = A/273.15 # reference exponential index at 0 oC (dimensionless)

# saturation vapour pressure at all temperatures (hPa)
esvp = esvp0*(np.exp(A/T_K-exp0))


# latent heat of vapourisation (J/kg) for water as a function of temperature
# doi.org/10.1002/qj.49711046626
Lw = 1.91846e6*(T_K/(T_K-33.91))**2.

# rate of change of r (water mixing ratio) with temperature from saturated 
# adiabatic lapse rate 
# equation (Convection and SALR lecture), note the first term results from the 
# differentiation of r = 5e_svp/8P with respect to T, where e_svp is given by the 
# esvp equation above (/K)
drdT = 5.*(-A/(T_K**2.))*esvp/(8.*P)

# specific heat capacity of dry air (J/K.kg) (Convection and SALR lecture)
Cp = 1004.

# saturated adiabatic lapse rate (Dry and Moist Air lecture) (K/m)
Gamm = si.g/(Cp+Lw*drdT)

# prepare for storing wet bulb potential temperarure (oC)
thetaw_oC = np.zeros((theta_oC.shape))
# assume same as dry potential temperature to begin (oC)
thetaw_oC[:, :] = theta_oC[:, :] 

# wet bulb potential temperatures at reference pressure (oC) is the same as for
# the actual temperature and the potential temperature
thetaw_oC[np.arange(theta_oC.shape[0]-1, -1, -1), np.arange(0, theta_oC.shape[1], 1)] = theta_oC[np.arange(theta_oC.shape[0]-1, -1, -1), np.arange(0, theta_oC.shape[1], 1)]

R = si.R*1.e3/28.966 # specific gas constant for air (m2/(K.s^2))

R = si.R*1.e3/18. # specific gas constant for water vapour (m2/(K.s^2))

Gammr = si.g/1004 # dry adiabatic lapse rate (K/m)

# ratio of isotherm adjacent to hypotenuse
mn = (T_K[0, 1]-T_K[0, 0])/((T_K[0, 1]-T_K[0, 0])**2.+(theta_K[1, 0]-theta_K[0, 0])**2.)**0.5
# scaling factor for wet bulb potential temperature estimation
mn = (T_K[0, 1]-T_K[0, 0])*mn

for ir in range(theta_oC.shape[0]): # loop through rows

	# column where bottom left to top right diagonal met
	cd = Gamm.shape[1]-ir
	
	# below reference pressure (higher altitudes)
	# height (m) between columns in this row
	delz = (np.log(P[ir, 1:cd]/P[ir, 0:cd-1])/-si.g)*R*((T_K[ir, 1:cd]+T_K[ir, 0:cd-1])/2.)
	# temperature change following dry adiabatic lapse rate
	delTr = delz*Gammr
	# change in temperature following saturated adiabatic cooling
	delT = delz*Gamm[ir, 0:cd-1]
	# change in temperature effect on saturated adiabatic isotherms
	delTn = np.flip(np.cumsum(np.flip(mn-(delT/delTr)*mn)))
	# saturated adiabatic temperature isopleth
	thetaw_oC[ir, 0:cd-1] -= delTn
	
	# above reference pressure (lower altitudes)
	# height (m) between columns in this row
	delz = (np.log(P[ir, cd::]/P[ir, cd-1:-1])/-si.g)*R*((T_K[ir, cd::]+T_K[ir, cd-1:-1])/2.)
	# temperature change following dry adiabatic lapse rate
	delTr = delz*Gammr
	# change in temperature following saturated adiabatic cooling
	delT = delz*Gamm[ir, cd::]
	# change in temperature effect on saturated adiabatic isotherms
	delTn = np.cumsum(mn-(delT/delTr)*mn)
	# saturated adiabatic temperature isopleth
	thetaw_oC[ir, cd::] += delTn

# plot wet bulb potential temperature contours
tephi3 = ax1.contour(T_oC, theta_oC, thetaw_oC, Tlevels, colors = 'black', linewidths = 0.1, linestyles = '-', transform = trans_data)

# contour labels
labels = [] # empty contour labels list
for it in range(len(Tlevels)):
	labels.append(str(r'$\rm{\theta_w}$=%s $\rm{^oC}$') %Tlevels[it])
fmt2 = {}
for l, s in zip(tephi3.levels[0::2], labels[0::2]):
   fmt2[l] = s
ax1.clabel(tephi3, tephi3.levels[0::2], inline = False, fmt = fmt2, fontsize = 10)

plt.draw()
plt.pause(1) # pause

# fifth isopleth (mass mixing ratio of water (g of water/kg dry air)) ----------

# using ideal gas equation, estimate mass (kg) of water vapour in 1m3 of air 
# based on pressure, note hPa converted to Pa
mw = (esvp*1e2*1.)/(Rw*T_K)
mw = mw*1e3 # convert to g from kg

# using ideal gas equation estimate mass of dry air, note hPa 
# converted to Pa
ma = (P*1e2*1.)/(R*T_K)

r = mw/ma # the mass mixing ratio (g of water/kg of dry air)

# state water mixing ratios to plot
rlevels = [0.15, 0.8, 2., 3., 5., 7., 9., 12., 16., 20., 28.]

# plot water mixing ratio contours
tephi4 = ax1.contour(T_oC, theta_oC, r, rlevels, colors = 'black', linewidths = 0.5, linestyles = '--', transform = trans_data)

# contour labels
labels = [r'0.15 $\rm{g\, kg^{-1}}$', r'0.8 $\rm{g\, kg^{-1}}$', r'2 $\rm{g\, kg^{-1}}$', r'3 $\rm{g\, kg^{-1}}$', r'5 $\rm{g\, kg^{-1}}$', r'7 $\rm{g\, kg^{-1}}$', r'9 $\rm{g\, kg^{-1}}$', r'12 $\rm{g\, kg^{-1}}$', r'16 $\rm{g\, kg^{-1}}$', r'20 $\rm{g\, kg^{-1}}$', r'28 $\rm{g\, kg^{-1}}$']
fmt2 = {}
for l, s in zip(tephi4.levels, labels):
   fmt2[l] = s
ax1.clabel(tephi4, tephi4.levels, inline = False, fmt = fmt2, fontsize = 10)

plt.draw()
plt.pause(1) # pause



# finally plot example measurements -------------------

# measure temperatures (oC)
measT = 80, 60, 50, 15, 15, 15, 15
xT = -50, -55, -60, -60, -35, -10, 15

# measured wet-bulb temperature (oC)
measwT = 5, 5, 6, 7, 7, 7, 7
xwT = -90, -80, -75, -68, -35, -10, 5

# plot measurements
plt.plot(xT, measT, '-r', transform = trans_data)
plt.plot(xwT, measwT, '-b', transform = trans_data)

plt.draw()
plt.pause(1000) # pause


# end of script ---------------------------------------------------