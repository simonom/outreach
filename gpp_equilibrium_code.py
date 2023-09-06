#python code to estimate equilibrium gas-particle partitioning and return the
#resulting secondary organic particulate mass concentration

# import dependencies
import numpy as np
import scipy.constants as si
import matplotlib.pyplot as plt

# start of section to provide inputs --------------------
# molar mass of components (g/mol)
y_MM = np.array((1.e2, 5.e2))
# pure component saturation vapour pressure of components (Pa)
PsatPa = np.array((1.e-2, 1.e-5)) 
# temperature (K)
temper = 298.15
# mass concentrations of components in gas phase with time (ug/m3), where 
# rows are time through experiment and columns are components
y_mc = np.array(([1.e0, 0.0], [3.e-1, 7.e-1]))

# times through experiment that concentrations given at (s)
time = np.array((0., 2.7e3))
# seed particle concentration (ug/m3)
seed = 1.
# end of section to provide inputs-------------------------

def equil_partit(y_MM, PsatPa, temper, y_mc, time):
	
	# effective saturation concentrations of components (ug/m3)
	Cstar = 10.**6*y_MM*PsatPa/(8.314*temper)
	
	# prepare results (condensable fraction) array
	cf = np.zeros((len(time), y_mc.shape[1]))

	# loop through times to estimate organic particulate mass (ug/m3)
	# at each time through experiment
	for it in range(len(time)):
 		
		# prepare starting estimate condensable fraction array
		fi_est = np.zeros((y_mc.shape[1]))
		
		# get second estimate of condensable fraction
		se_est = ((1+Cstar/(sum(fi_est*y_mc[it, :])+seed))**-1)
		
		# if nothing to condense, move onto next time
		if (sum(se_est) == 0):
			continue

		# iterate until first guess and second guess converge
		# (necessary since the organics contribute to the particle mass)
		while (np.abs(sum(fi_est)-sum(se_est))/sum(se_est) > 1.e-2):
			
			# new first estimate
			fi_est[:] = se_est[:]
			
			# new second estimate
			se_est = ((1+Cstar/(sum(fi_est*y_mc[it, :])+seed))**-1)

		cf[it, :] = se_est

	# sum over components (ug/m3) for equilibrium organic
	# particulate mass concentration at every time step
	p_sum = np.sum(cf*y_mc[:, :], axis = 1)

	# remove these components from gas-phase (ug/m3)
	y_mc -= cf*y_mc[:, :]

	# sum of components in gas-phase (ug/m3)
	g_sum = np.sum(y_mc, axis=1) 


	# plot total gas- and particle-phase mass 
	# concentration of organics (ug/m3) with time
	fig, (ax0) = plt.subplots(1, 1, figsize=(14, 7))
	ax0.plot(time, p_sum, label = 'secondary organics in particle phase')
	ax0.plot(time, g_sum, label = 'organics in gas phase')
	ax0.set_xlabel('Time through experiment (s)')
	ax0.set_ylabel('Mass concentration (ug/m3)')
	ax0.legend()
	plt.show()
	
	return(p_sum)

# call function to get total particle concentration 
# at every time step (ug/m3)
p_sum = equil_partit(y_MM, PsatPa, temper, y_mc, time)
