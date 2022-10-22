# plots slices of density for various times

import yt
from yt.units import dimensions


def _magic(field, data):
     return (data['user_out_var14'])    # keep original nonscaled values for the total pressure

yt.add_field(('gas', u'magic'), function = _magic)

# conversion factors
denstocgs = 6.85e-27
Myr = 1.
kpc = 1.

#dir="./ionneutral/pres1/test_March20_vmax100/"
dir="./../"
base="cr.out2."

plotvar = 'magic'
#plotvar = 'cool'
varmin = 1.e-31
varmax = 1.e-27

times = range(0,46,1)



for i in times:
 ds = yt.load(dir+base+str(i).zfill(5)+'.athdf')
 dd = ds.all_data()
 print(ds.field_list)
 time = ds.current_time.v/Myr
# slc = yt.SlicePlot(ds, 'z', plotvar, origin='native', center=[1.5*kpc, 0, 0])
# slc.set_width((0.6*kpc, .25*kpc))

 print(dd.quantities.extrema("magic"))

 slc = yt.SlicePlot(ds, 'z', plotvar)
 slc.set_zlim(plotvar, varmin, varmax)
 slc.set_cmap(field=plotvar, cmap='plasma')
 slc.set_colorbar_label(plotvar,r"Cooling dE/dt")
 slc.set_log(plotvar, True)
 slc.annotate_title("t = %3.0f Myr" % time)
 slc.save()
