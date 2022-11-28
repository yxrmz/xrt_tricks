This example is based on xrt 1.5.0, here I show 
1) How to add custom OE class (here we add FlatParaboloidLens based on ParaboloidFlatLens)
2) How to make it avaiable in xrtQook - see the top of oes.py
3) How to add multiple sources / multiple beam paths in xrtQook

oes.py replaces the file in xrt/backends/raycing.\
Change the path in flatparalens_test.py sys.path.append() according to your environment

![output](dual_para_flat.png)
