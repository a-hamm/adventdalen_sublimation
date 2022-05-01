import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from datetime import datetime,timedelta
import h5py
import sys,os
plt.ion()

obs = pd.read_csv('../debug_transient/observation.dat',
                  sep = ' ', comment='#')
sd = pd.read_csv('../debug_transient/snowdepth.csv')
sd['time'] = pd.to_datetime(sd['time'], format='%d.%m.%Y')
r = pd.date_range(start=pd.to_datetime(sd['time']).min(), end=pd.to_datetime(sd['time']).max())
sd = sd.set_index('time').reindex(r).fillna(np.nan).rename_axis('time').reset_index()

plt.bar(sd.time, sd.snowdepth/100, alpha=0.5, color = 'grey', label = 'observed')
plt.plot(sd.time, obs['snow depth [m]'], label = 'modeled')
plt.legend()

with h5py.File('../debug_transient/ats_vis_surface_data.h5','r') as d:
    a_key = list(d['surface-cell_volume.cell.0'].keys())[0]
    surf_area = d['surface-cell_volume.cell.0'][a_key][:].sum() # m^2

# load data
df = pandas.read_csv('../debug_transient/observation.dat', comment='#',sep=' ')

# process
time = df['time [d]']
P = df['rain precipitation [m d^-1]']
SM = df['snowmelt [m d^-1]']
ET = df['evapotranspiration [m d^-1]']
Q = df['runoff generation [mol d^-1]']/55500./surf_area
diff = P + SM - ET - Q
water = (df['surface water content [mol]'] + df['subsurface water content [mol]']) / 55500 / surf_area

error = np.cumsum(diff) - (water - water[0])
max_error = error.max()
S = df['snow precipitation [m d^-1]']
#S_ET = df['snow evaporation [m d^-1]']
#diff_snow = S - SM - S_ET
snow = df['snow water content [mol]'] / 55500 / surf_area
#error_snow = np.cumsum(diff_snow) - (snow - snow[0])
#max_error_snow = error_snow.max()

fig = plt.figure()

ax = fig.add_subplot(3,1,1)
ax.plot(time, np.cumsum(P), label='P')
ax.plot(time, np.cumsum(SM), label='SM')
ax.plot(time, np.cumsum(ET), label='ET')
ax.plot(time, np.cumsum(Q), label='Q')
ax.plot(time, water - water[0], 'k', label='water')
ax.plot(time, np.cumsum(diff), 'k--', label='P+SM-ET-Q')
ax.plot(time, error, '-.', color='grey', label='error')
ax.legend(frameon=False,ncol=2)

ax.set_title(f'Cumulative sums of fluxes (Inf err: {max_error})')
ax.set_xlabel('time [d]')
ax.set_ylabel('cumulative flux [m]')


ax = fig.add_subplot(3,1,2)
ax.plot(time, P, label='P')
ax.plot(time, SM, label='SM')
ax.plot(time, ET, label='ET')
ax.plot(time, Q, label='Q')
ax.plot(time, error[1:] - error[:-1], '-.', color='grey', label='delta error')
ax.legend(frameon=False,ncol=2)
ax.set_title('fluxes')
ax.set_xlabel('time [d]')
ax.set_ylabel('flux [m / d]')

ax = fig.add_subplot(3,1,3)
ax.plot(time, np.cumsum(S), label='P_snow')
ax.plot(time, np.cumsum(SM), label='SM')
ax.plot(time, snow - snow[0], 'k', label='snow depth')
ax.plot(time, error, '-.', color='grey', label='error')
ax.legend(frameon=False, ncol=2)
ax.set_ylabel('cumulative flux [m]')
ax.set_xlabel('time [d]')
plt.tight_layout()
plt.show()
