import yt
from yt.units.yt_array import YTQuantity
from yt.units import dimensions
import numpy as np
from numpy import *
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import h5py
from yt.fields import interpolated_fields
from yt.fields.field_detector import \
    FieldDetector
from yt.utilities.linear_interpolators import \
    BilinearFieldInterpolator

from mpl_toolkits.axes_grid1 import AxesGrid

fig = plt.figure()



pUnit = YTQuantity(1, 'cm**2/s**2')

# conversion factors
denstocgs = 6.85e-27
edenstocgs = 6.54e-11
Myr = 1.
kpc = 1.


def _d(field, data):
  return data['density']*denstocgs
def _Bmag(field, data):
  return data['magnetic_field_magnitude']*np.sqrt(edenstocgs)


yt.add_field(('gas', u'd'), function = _d,sampling_type='local', units="g/cm**3",display_name=r"Density", dimensions=dimensions.density)
yt.add_field(('gas', u'Bmag'), function = _Bmag,sampling_type='local', units="code_magnetic",display_name=r"|B| (Gauss)")



# See http://matplotlib.org/mpl_toolkits/axes_grid/api/axes_grid_api.html
grid = AxesGrid(fig, (0.099,0.085,0.81,0.83),
                nrows_ncols = (1, 2),
                axes_pad = 0.15,
                label_mode = "L",
                share_all = True,
                cbar_location="right",
                cbar_mode="single",
                cbar_size="3%",
                cbar_pad="0%",
                aspect=False )

#ts = yt.DatasetSeries("../cr.out1.0*")
#ds = yt.load('ionAlfven_Damping/noClumpsNearBoundary/L5_alpha1_5/cr.out1.00040.athdf')
ds = yt.load('../cr.out1.00030.athdf')
dd = ds.all_data()

print(dd.quantities.extrema('Bmag'))
plotvar = "cell_mass"

time = str(ds.current_time.in_units('Myr'))
time = (time[:3]) if len(time) > 3 else time
t = "t = {} Myrs".format(str(time))
p = yt.PhasePlot(dd, "d", "Bmag", plotvar,weight_field=None,fractional=[False,False,True])



# plot.set_cmap(field="magnetic_field_magnitude", cmap='viridis')
# plot.set_cmap(field="nenh_interp", cmap='viridis')
p.set_cmap(field=plotvar, cmap='plasma')
# plot.set_xlim(1.E-30,1.E-23)
# plot.set_xlim(1.E-27,8.E-24)
p.set_xlim(1.E-27,5.E-23)
# plot.set_ylim(1.E-9,1.E-5)
p.set_ylim(1.E-7,5.E-5)
#       plot.set_zlim(1.E-8,1.E-2)
# plot.set_unit('cell_mass', 'Msun')
#p.set_zlim(field='collision', zmin=1.E-5, zmax=1.E-2)
p.set_zlim(field=plotvar, zmin=1.E-5, zmax=1.E-2)
p.annotate_title(r"snapshot 30")

# This forces the ProjectionPlot to redraw itself on the AxesGrid axes.
plot = p.plots[plotvar]
plot.figure = fig
plot.axes = grid[0].axes

# only for i = 0
plot.cax = grid.cbar_axes[0]

# Actually redraws the plot.
p._setup_plots()

# Modify the axes properties **after** p._setup_plots() so that they
# are not overwritten.
plot.axes.xaxis.set_minor_locator(
     plt.LogLocator(base=10.0, subs=[2.0,5.0,8.0]) )

ds = yt.load('../cr.out1.00040.athdf')
dd = ds.all_data()

plotvar = "cell_mass"
time = str(ds.current_time.in_units('Myr'))
time = (time[:3]) if len(time) > 3 else time
t = "t = {} Myrs".format(str(time))
p = yt.PhasePlot(dd, "d", "Bmag", plotvar,weight_field=None,fractional=[False,False,True])



# plot.set_cmap(field="magnetic_field_magnitude", cmap='viridis')
# plot.set_cmap(field="nenh_interp", cmap='viridis')
p.set_cmap(field=plotvar, cmap='plasma')
# plot.set_xlim(1.E-30,1.E-23)
# plot.set_xlim(1.E-27,8.E-24)
p.set_xlim(1.E-27,5.E-23)
# plot.set_ylim(1.E-9,1.E-5)
#p.set_ylim(1.E-13,5.E-12)
p.set_ylim(1.E-7,5.E-5)
#       plot.set_zlim(1.E-8,1.E-2)
# plot.set_unit('cell_mass', 'Msun')
p.set_zlim(field=plotvar, zmin=1.E-5, zmax=1.E-2)
p.annotate_title(r"snapshot 40")

# This forces the ProjectionPlot to redraw itself on the AxesGrid axes.
plot = p.plots[plotvar]
plot.figure = fig
plot.axes = grid[1].axes

# only for i = 0
#plot.cax = grid.cbar_axes[0]

# Actually redraws the plot.
p._setup_plots()

# Modify the axes properties **after** p._setup_plots() so that they
# are not overwritten.
plot.axes.xaxis.set_minor_locator(
     plt.LogLocator(base=10.0, subs=[2.0,5.0,8.0]) )


#plot.annotate_title(r"$v_{st} = v_{A}^{ion}$ + Ion-Neutral Damping")
plt.savefig('multiplot_phasePlot_dens_B.pdf')
        
