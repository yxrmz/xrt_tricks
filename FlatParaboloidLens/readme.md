This example is based on xrt master branch, here I show 
1) How to add custom OE class (here we add FlatParaboloidLens based on ParaboloidFlatLens)
3) How to add multiple sources / multiple beam paths in xrtQook

To run this example download and extract xrt master branch from https://github.com/kklmn/xrt
Navigate to xrt/gui and put *customOE.py* from this repository next to *xrtQookStart.py*

Edit *xrtQookStart.py* adding the following lines above `if __name__ == '__main__':`

```
import xrt.backends.raycing.oes as roe
from customOE import FlatParaboloidLens
roe.FlatParaboloidLens = FlatParaboloidLens
roe.__allSectioned__['My custom OEs'] = ('FlatParaboloidLens',)
```

Run *xrtQookStart.py* and load *para_flat_dual_undulator.xml*

If you now run Glow you will be able to see two beams from two sources going through two sets of lenses, like on the picture below.

![output](dual_para_flat.png)
