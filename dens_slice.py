# plots slices of density for various times

import yt
from yt.units import dimensions
from yt.units import pc
from yt import YTQuantity
yt.enable_parallelism()

# conversion factors
edenstocgs = 6.54e-11
denstocgs = 6.85e-27
Myr = 1.
kpc = 1.
eddy = (3.0856e21/4e6)/3.155e13


def _dens(field, data):
  return denstocgs*data['rho']

yt.add_field(('gas', u'dens'), function = _dens, sampling_type='local', units="g/cm**3",display_name=r"Density")



plotvar = 'dens'
#varmax = 1.e-24
varmax = 2.E-24
#varmax = 2.3e-27
varmin = 2.E-27

ts = yt.DatasetSeries('../cr.out1.0006*',parallel=10)
for ds in ts.piter():
# time = ds.current_time.v/eddy
 time = ds.current_time
 slc = yt.SlicePlot(ds, 'z', plotvar,fontsize=20)
 slc.set_zlim(plotvar, varmin, varmax)
 slc.set_cmap(field=plotvar, cmap='dusk')
 slc.set_xlabel('x')
 slc.set_ylabel('y')
# slc.annotate_title(r"t = %3.1f $\tau_{eddy}$" % time)
 slc.annotate_title(r"t = %3.1f Myrs" % time)
 slc.save()
