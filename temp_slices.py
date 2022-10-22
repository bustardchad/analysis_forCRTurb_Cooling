# plots slices of density for various times

import yt
from yt.units import dimensions
from yt.units import pc

yt.enable_parallelism()

# conversion factors
Myr = 1.
kpc = 1.

# conversion factors
denstocgs = 6.85e-27
edenstocgs = 6.54e-11
prestocgs = 6.54e-11
#temptocgs = 0.6*1.67e-24*prestocgs/(denstocgs*1.38e-16)
temptocgs = prestocgs/(denstocgs)


def _tmp(field, data):
 return data['temperature']*temptocgs

yt.add_field(('gas', u'tmp'), function = _tmp,sampling_type='local', units="K",display_name=r"Temperature", dimensions=dimensions.temperature)


plotvar = 'tmp'
varmax = 5.e8
varmin = 1.e3

ts = yt.DatasetSeries('../cr.out1.0006*',parallel=10)
for ds in ts.piter():
 time = ds.current_time.v/Myr
 dd = ds.all_data()
 print(dd.quantities.extrema(plotvar))
 slc = yt.SlicePlot(ds, 'z', plotvar, fontsize=20) #,origin='native', center=[0.9*kpc, 0*pc, 0*pc])
 slc.set_zlim(plotvar, varmin, varmax)
 slc.set_cmap(field=plotvar, cmap='inferno')
 slc.set_xlabel('x (kpc)')
 slc.set_ylabel('y (kpc)')
 slc.annotate_title("t = %3.0f Myr" % time)
 slc.save()
