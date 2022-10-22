# plots slices of density for various times

import yt
from yt.units import dimensions
from yt.units import pc
import numpy as np

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

def _pmag(field, data):
 return ds.arr((data['Bcc1']**2+data['Bcc2']**2 + data['Bcc3']**2)/2., 'g/(cm*s**2)')

def _va(field, data):
 return ds.arr((data['pmag'])/np.sqrt(data['density']), 'cm/s') # keep original nonscaled values for the total pressure

def _beta(field, data):
 return ds.arr(data['pressure']/data['pmag'], '') # keep original nonscaled values for the total pressure

yt.add_field(('gas', u'pmag'),sampling_type='local', function = _pmag,units='g/(cm*s**2)',display_name=r"$P_{B}$")
yt.add_field(('gas', u'va'),sampling_type='local', function = _va,units='cm/s',display_name=r"$v_{A}$")
yt.add_field(('gas', u'beta'),sampling_type='local', function = _beta,units='',display_name=r"plasma $\beta$")



plotvar = 'beta'
varmax = 1.E3
varmin = 1.E-2

ts = yt.DatasetSeries('../cr.out1.0006*',parallel=10)
for ds in ts.piter():
 time = ds.current_time.v/Myr
 dd = ds.all_data()
 print(dd.quantities.extrema(plotvar))
 slc = yt.SlicePlot(ds, 'z', plotvar, fontsize=20) #,origin='native', center=[0.9*kpc, 0*pc, 0*pc])
 #slc.set_zlim(plotvar, varmin, varmax)
 slc.set_cmap(field=plotvar, cmap='plasma')
 slc.set_xlabel('x (kpc)')
 slc.set_ylabel('y (kpc)')
 slc.annotate_title("t = %3.0f Myr" % time)
 slc.save()

plotvar = 'va'
varmax = 1.E7
varmin = 1.E4

ts = yt.DatasetSeries('../cr.out1.0006*',parallel=10)
for ds in ts.piter():
 time = ds.current_time.v/Myr
 dd = ds.all_data()
 print(dd.quantities.extrema(plotvar))
 slc = yt.SlicePlot(ds, 'z', plotvar, fontsize=20) #,origin='native', center=[0.9*kpc, 0*pc, 0*pc])
 #slc.set_zlim(plotvar, varmin, varmax)
 slc.set_cmap(field=plotvar, cmap='plasma')
 slc.set_xlabel('x (kpc)')
 slc.set_ylabel('y (kpc)')
 slc.annotate_title("t = %3.0f Myr" % time)
 slc.save()
