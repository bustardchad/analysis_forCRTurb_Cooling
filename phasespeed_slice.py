# plots slices of density for various times

import yt
from yt.units import dimensions
from yt.units import pc
from yt import YTQuantity
import numpy as np
yt.enable_parallelism()

# conversion factors
edenstocgs = 6.54e-11
denstocgs = 6.85e-27
Myr = 1.
kpc = 1.
eddy = (3.0856e21/4e6)/3.155e13
scale = 1.0

def _pcr(field, data):
 return ds.arr(data['Ec'].v*edenstocgs/(3.*scale), 'g/(cm*s**2)')
def _pth(field, data):
 return ds.arr(data['press'].v*edenstocgs/scale, 'g/(cm*s**2)')
def _pmag(field, data):
 return ds.arr(((data['Bcc1']**2+data['Bcc2']**2 +data['Bcc3']**2)/2.).v*edenstocgs/scale, 'g/(cm*s**2)')
def _ptot(field, data):
 return (data['pmag']+data['pth']+data['pcr'])*scale    # keep original nonscaled values for the total pressure

yt.add_field(('gas', u'pcr'), function = _pcr,sampling_type='local', units="g/(cm*s**2)", dimensions=dimensions.pressure)
yt.add_field(('gas', u'pth'), function = _pth, sampling_type='local',units="g/(cm*s**2)", dimensions=dimensions.pressure)
yt.add_field(('gas', u'pmag'), function = _pmag, sampling_type='local',units="g/(cm*s**2)", dimensions=dimensions.pressure)
yt.add_field(('gas', u'ptot'), function = _ptot, sampling_type='local',units="g/(cm*s**2)", dimensions=dimensions.pressure)


def _vph(field, data):
  dens = denstocgs*data['rho']
  return np.sqrt((data['ptot'])/dens)

yt.add_field(('gas', u'vph'), function = _vph,sampling_type='local', units="cm/s",display_name=r"v$_{ph}$", dimensions=dimensions.velocity)



plotvar = 'vph'
#varmax = 1.e-24
varmax = 5.e8
#varmax = 2.3e-27
varmin = 1.e6

ts = yt.DatasetSeries('../cr.out1.0001*',parallel=10)
for ds in ts.piter():
 dd = ds.all_data()
# time = ds.current_time.v/eddy
 time = ds.current_time.v/Myr
 print(dd.quantities.extrema(plotvar))
 print(dd.quantities.extrema('pcr'))
 print(dd.quantities.extrema('pth'))
 print(dd.quantities.extrema('pmag'))
 """
 slc = yt.SlicePlot(ds, 'z', plotvar,fontsize=20)
 slc.set_zlim(plotvar, varmin, varmax)
 slc.set_cmap(field=plotvar, cmap='dusk')
 slc.set_xlabel('x')
 slc.set_ylabel('y')
# slc.annotate_title(r"t = %3.1f $\tau_{eddy}$" % time)
 slc.annotate_title(r"t = %3.1f Myr" % time)
 slc.save()
 """
