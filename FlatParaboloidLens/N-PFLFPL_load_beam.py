# -*- coding: utf-8 -*-
"""

__author__ = "Konstantin Klementiev", "Roman Chernikov"
__date__ = "2022-11-01"

Created with xrtQook

"""

#import matplotlib
#matplotlib.use('agg')

import numpy as np
import sys
sys.path.append(r"/opt/xray/xrt-1.4.0/python3.6/site-packages")
#sys.path.append(r"c:/github/xrt")
import xrt.backends.raycing.sources as rsources
import xrt.backends.raycing.screens as rscreens
import xrt.backends.raycing.materials as rmats
import xrt.backends.raycing.oes as roes
import xrt.backends.raycing.apertures as rapts
import xrt.backends.raycing.run as rrun
import xrt.backends.raycing as raycing
import xrt.plotter as xrtplot
import xrt.runner as xrtrun


from customOE import FlatParaboloidLens
roes.FlatParaboloidLens = FlatParaboloidLens
roes.__allSectioned__['My custom OEs'] = ('FlatParaboloidLens',)


showIn3D= False

Si111 = rmats.CrystalSi(
    hkl=[1, 1, 1],
    d=3.13474,
    rho=2.336,
    table=r"Chantler total",
    name=r"Si111")

lens_Be = rmats.Material(
    elements=r"Be",
    kind=r"lens",
    rho=1.848,
    name=None)

screen_pos = 59100
load_pos = 59092.825
zmax=1.
t=0.025



def build_beamline(E):
    P23_U32 = raycing.BeamLine()

    P23_U32.E = E

    if showIn3D:
        P23_U32.source = rsources.GeometricSource(
            P23_U32, 'CollimatedSource', nrays=1e5,
            dx=0.5, dz=0.5, distxprime=None, distzprime=None, energies=(E*1e3,))   


    P23_U32.pfl1 = roes.ParaboloidFlatLens(
        bl=P23_U32,
        center=[0, 87894-load_pos-1000-7*(zmax+t), 0],
        material=lens_Be,
        focus=0.025,
        zmax=zmax,
        t=t,
        nCRL=1)

    P23_U32.fpl1 = roes.FlatParaboloidLens(
        bl=P23_U32,
#        center=[0, 87894-load_pos-1000-6*(zmax+t), 0],
        center=[0, 87894-load_pos-1000-7*(zmax+t)+t, 0],
        material=lens_Be,
        focus=0.025,
        zmax=zmax,
        t=t,
        nCRL=1)


    P23_U32.pfl2 = roes.ParaboloidFlatLens(
        bl=P23_U32,
        center=[0, 87894-load_pos-1000-5*(zmax+t), 0],
        material=lens_Be,
        focus=0.025,
        zmax=zmax,
        t=t,
        nCRL=1)

    P23_U32.fpl2 = roes.FlatParaboloidLens(
        bl=P23_U32,
#        center=[0, 87894-load_pos-1000-4*(zmax+t), 0],
        center=[0, 87894-load_pos-1000-5*(zmax+t)+t, 0],
        material=lens_Be,
        focus=0.025,
        zmax=zmax,
        t=t,
        nCRL=1)


    P23_U32.pfl3 = roes.ParaboloidFlatLens(
        bl=P23_U32,
        center=[0, 87894-load_pos-1000-3*(zmax+t), 0],
        material=lens_Be,
        focus=0.025,
        zmax=zmax,
        t=t,
        nCRL=1)

    P23_U32.fpl3 = roes.FlatParaboloidLens(
        bl=P23_U32,
#        center=[0, 87894-load_pos-1000-2*(zmax+t), 0],
        center=[0, 87894-load_pos-1000-3*(zmax+t)+t, 0],
        material=lens_Be,
        focus=0.025,
        zmax=zmax,
        t=t,
        nCRL=1)

    P23_U32.pfl4 = roes.ParaboloidFlatLens(
        bl=P23_U32,
        center=[0, 87894-load_pos-1000-1*(zmax+t), 0],
        material=lens_Be,
        focus=0.025,
        zmax=zmax,
        t=t,
        nCRL=1)

    P23_U32.fpl4 = roes.FlatParaboloidLens(
        bl=P23_U32,
#        center=[0, 87894-load_pos-1000+1*(zmax+t), 0],
        center=[0, 87894-load_pos-1000-1*(zmax+t)+t, 0],
        material=lens_Be,
        focus=0.025,
        zmax=zmax,
        t=t,
        nCRL=1)


    P23_U32.pfl5 = roes.ParaboloidFlatLens(
        bl=P23_U32,
#        center=[0, 87894-load_pos-1000+2*(zmax+t), 0],
        center=[0, 87894-load_pos-1000+1*(zmax+t), 0],
        material=lens_Be,
        focus=0.025,
        zmax=zmax,
        t=t,
        nCRL=1)

    P23_U32.fpl5 = roes.FlatParaboloidLens(
        bl=P23_U32,
#        center=[0, 87894-load_pos-1000+3*(zmax+t), 0],
        center=[0, 87894-load_pos-1000+1*(zmax+t)+t, 0],
        material=lens_Be,
        focus=0.025,
        zmax=zmax,
        t=t,
        nCRL=1)


    P23_U32.pfl6 = roes.ParaboloidFlatLens(
        bl=P23_U32,
#        center=[0, 87894-load_pos-1000+4*(zmax+t), 0],
        center=[0, 87894-load_pos-1000+3*(zmax+t), 0],
        material=lens_Be,
        focus=0.025,
        zmax=zmax,
        t=t,
        nCRL=1)

    P23_U32.fpl6 = roes.FlatParaboloidLens(
        bl=P23_U32,
#        center=[0, 87894-load_pos-1000+5*(zmax+t), 0],
        center=[0, 87894-load_pos-1000+3*(zmax+t)+t, 0],
        material=lens_Be,
        focus=0.025,
        zmax=zmax,
        t=t,
        nCRL=1)


    P23_U32.pfl7 = roes.ParaboloidFlatLens(
        bl=P23_U32,
#        center=[0, 87894-load_pos-1000+6*(zmax+t), 0],
        center=[0, 87894-load_pos-1000+5*(zmax+t), 0],
        material=lens_Be,
        focus=0.025,
        zmax=zmax,
        t=t,
        nCRL=1)

    P23_U32.fpl7 = roes.FlatParaboloidLens(
        bl=P23_U32,
#        center=[0, 87894-load_pos-1000+7*(zmax+t), 0],
        center=[0, 87894-load_pos-1000+5*(zmax+t)+t, 0],
        material=lens_Be,
        focus=0.025,
        zmax=zmax,
        t=t,
        nCRL=1)


    P23_U32.screen_sample = rscreens.Screen(
        bl=P23_U32,
        name=r"U32_screen_DCM",
        center=[0, 87894-screen_pos, 0])

    return P23_U32


def run_process(P23_U32):

    if showIn3D:
        loaded_beam = P23_U32.source.shine()
    else:
        loaded_beam = rsources.Beam(copyFrom='beam_after_mono_%02dkeV.npy'%P23_U32.E)

    paraboloidFlatLens01beamGlobal01, paraboloidFlatLens01beamLocal101, paraboloidFlatLens01beamLocal201 = P23_U32.pfl1.multiple_refract(
        beam=loaded_beam)

    flatParaboloidLens01beamGlobal01, flatParaboloidLens01beamLocal101, flatParaboloidLens01beamLocal201 = P23_U32.fpl1.multiple_refract(
        beam=paraboloidFlatLens01beamGlobal01)


    paraboloidFlatLens02beamGlobal01, paraboloidFlatLens02beamLocal101, paraboloidFlatLens02beamLocal201 = P23_U32.pfl2.multiple_refract(
        beam=flatParaboloidLens01beamGlobal01)

    flatParaboloidLens02beamGlobal01, flatParaboloidLens02beamLocal101, flatParaboloidLens02beamLocal201 = P23_U32.fpl2.multiple_refract(
        beam=paraboloidFlatLens02beamGlobal01)


    paraboloidFlatLens03beamGlobal01, paraboloidFlatLens03beamLocal101, paraboloidFlatLens03beamLocal201 = P23_U32.pfl3.multiple_refract(
        beam=flatParaboloidLens02beamGlobal01)

    flatParaboloidLens03beamGlobal01, flatParaboloidLens03beamLocal101, flatParaboloidLens03beamLocal201 = P23_U32.fpl3.multiple_refract(
        beam=paraboloidFlatLens03beamGlobal01)


    paraboloidFlatLens04beamGlobal01, paraboloidFlatLens04beamLocal101, paraboloidFlatLens04beamLocal201 = P23_U32.pfl4.multiple_refract(
        beam=flatParaboloidLens03beamGlobal01)

    flatParaboloidLens04beamGlobal01, flatParaboloidLens04beamLocal101, flatParaboloidLens04beamLocal201 = P23_U32.fpl4.multiple_refract(
        beam=paraboloidFlatLens04beamGlobal01)


    paraboloidFlatLens05beamGlobal01, paraboloidFlatLens05beamLocal101, paraboloidFlatLens05beamLocal201 = P23_U32.pfl5.multiple_refract(
        beam=flatParaboloidLens04beamGlobal01)

    flatParaboloidLens05beamGlobal01, flatParaboloidLens05beamLocal101, flatParaboloidLens05beamLocal201 = P23_U32.fpl5.multiple_refract(
        beam=paraboloidFlatLens05beamGlobal01)


    paraboloidFlatLens06beamGlobal01, paraboloidFlatLens06beamLocal101, paraboloidFlatLens06beamLocal201 = P23_U32.pfl6.multiple_refract(
        beam=flatParaboloidLens05beamGlobal01)

    flatParaboloidLens06beamGlobal01, flatParaboloidLens06beamLocal101, flatParaboloidLens06beamLocal201 = P23_U32.fpl6.multiple_refract(
        beam=paraboloidFlatLens06beamGlobal01)


    paraboloidFlatLens07beamGlobal01, paraboloidFlatLens07beamLocal101, paraboloidFlatLens07beamLocal201 = P23_U32.pfl7.multiple_refract(
        beam=flatParaboloidLens06beamGlobal01)

    flatParaboloidLens07beamGlobal01, flatParaboloidLens07beamLocal101, flatParaboloidLens07beamLocal201 = P23_U32.fpl7.multiple_refract(
        beam=paraboloidFlatLens07beamGlobal01)


    screen02beamLocal01 = P23_U32.screen_sample.expose(
        beam=flatParaboloidLens07beamGlobal01)
        #beam=loaded_beam)

    outDict = {
        'loaded_beam': loaded_beam,
        'paraboloidFlatLens01beamGlobal01': paraboloidFlatLens01beamGlobal01,
        'paraboloidFlatLens01beamLocal101': paraboloidFlatLens01beamLocal101,
        'paraboloidFlatLens01beamLocal201': paraboloidFlatLens01beamLocal201,
        'flatParaboloidLens01beamGlobal01': flatParaboloidLens01beamGlobal01,
        'flatParaboloidLens01beamLocal101': flatParaboloidLens01beamLocal101,
        'flatParaboloidLens01beamLocal201': flatParaboloidLens01beamLocal201,
        'paraboloidFlatLens02beamGlobal01': paraboloidFlatLens02beamGlobal01,
        'paraboloidFlatLens02beamLocal101': paraboloidFlatLens02beamLocal101,
        'paraboloidFlatLens02beamLocal201': paraboloidFlatLens02beamLocal201,
        'flatParaboloidLens02beamGlobal01': flatParaboloidLens02beamGlobal01,
        'flatParaboloidLens02beamLocal101': flatParaboloidLens02beamLocal101,
        'flatParaboloidLens02beamLocal201': flatParaboloidLens02beamLocal201,
        'paraboloidFlatLens03beamGlobal01': paraboloidFlatLens03beamGlobal01,
        'paraboloidFlatLens03beamLocal101': paraboloidFlatLens03beamLocal101,
        'paraboloidFlatLens03beamLocal201': paraboloidFlatLens03beamLocal201,
        'flatParaboloidLens03beamGlobal01': flatParaboloidLens03beamGlobal01,
        'flatParaboloidLens03beamLocal101': flatParaboloidLens03beamLocal101,
        'flatParaboloidLens03beamLocal201': flatParaboloidLens03beamLocal201,
        'paraboloidFlatLens04beamGlobal01': paraboloidFlatLens04beamGlobal01,
        'paraboloidFlatLens04beamLocal101': paraboloidFlatLens04beamLocal101,
        'paraboloidFlatLens04beamLocal201': paraboloidFlatLens04beamLocal201,
        'flatParaboloidLens04beamGlobal01': flatParaboloidLens04beamGlobal01,
        'flatParaboloidLens04beamLocal101': flatParaboloidLens04beamLocal101,
        'flatParaboloidLens04beamLocal201': flatParaboloidLens04beamLocal201,
        'paraboloidFlatLens05beamGlobal01': paraboloidFlatLens05beamGlobal01,
        'paraboloidFlatLens05beamLocal101': paraboloidFlatLens05beamLocal101,
        'paraboloidFlatLens05beamLocal201': paraboloidFlatLens05beamLocal201,
        'flatParaboloidLens05beamGlobal01': flatParaboloidLens05beamGlobal01,
        'flatParaboloidLens05beamLocal101': flatParaboloidLens05beamLocal101,
        'flatParaboloidLens05beamLocal201': flatParaboloidLens05beamLocal201,
        'paraboloidFlatLens06beamGlobal01': paraboloidFlatLens06beamGlobal01,
        'paraboloidFlatLens06beamLocal101': paraboloidFlatLens06beamLocal101,
        'paraboloidFlatLens06beamLocal201': paraboloidFlatLens06beamLocal201,
        'flatParaboloidLens06beamGlobal01': flatParaboloidLens06beamGlobal01,
        'flatParaboloidLens06beamLocal101': flatParaboloidLens06beamLocal101,
        'flatParaboloidLens06beamLocal201': flatParaboloidLens06beamLocal201,
        'paraboloidFlatLens07beamGlobal01': paraboloidFlatLens07beamGlobal01,
        'paraboloidFlatLens07beamLocal101': paraboloidFlatLens07beamLocal101,
        'paraboloidFlatLens07beamLocal201': paraboloidFlatLens07beamLocal201,
        'flatParaboloidLens07beamGlobal01': flatParaboloidLens07beamGlobal01,
        'flatParaboloidLens07beamLocal101': flatParaboloidLens07beamLocal101,
        'flatParaboloidLens07beamLocal201': flatParaboloidLens07beamLocal201,
        'screen02beamLocal01': screen02beamLocal01
	}
    if showIn3D:
        P23_U32.prepare_flow()    
    return outDict


rrun.run_process = run_process



def define_plots(E):
    plots = []

    plot_sample = xrtplot.XYCPlot(
        beam=r"screen02beamLocal01",
        xaxis=xrtplot.XYCAxis(
            label=r"x",
	    limits=[-.03, .03],
            fwhmFormatStr='%.6f'),
        yaxis=xrtplot.XYCAxis(
            label=r"z",
	    limits=[-.03, .03],
            fwhmFormatStr='%.6f'),
        caxis=xrtplot.XYCAxis(
            label=r"energy",
            unit=r"eV"),
        aspect=r"auto",
        title=r"N-PFLFPL_%02dkeV.png"%E,
        fluxFormatStr=r"%g",
        saveName=r"N-PFLFPL_%02dkeV.png"%E,)
    plots.append(plot_sample)

    return plots

def afterScript(P23_U32, plots, E):
    for plot in plots:
        print(P23_U32.screen_sample.center)
        with open('results_N-PFLFPL.dat', 'a') as f:
            shift_x = plot.cx + P23_U32.screen_sample.center[0]
            shift_y = plot.cy + P23_U32.screen_sample.center[2]
            f.write("%02d %.6f %.6f %.6f %.6f %5.2e %i\n"%(E, shift_x, shift_y, plot.dx, plot.dy, plot.flux, plot.nRaysGood))

def main(E):
    P23_U32 = build_beamline(E)
    if showIn3D:
        P23_U32.glow()
    plots = define_plots(E)
    xrtrun.run_ray_tracing(
        plots=plots,
        backend=r"raycing",
        beamLine=P23_U32,
        afterScript=afterScript, 
        afterScriptArgs=[P23_U32, plots, E]
    )


if __name__ == '__main__':
    energies = ([5000, 1], [10000, 3], [15000, 3], [20000, 7], [25000, 7], [30000, 7], [35000, 11], [40000, 11], [45000, 11])

    with open('results_N-PFLFPL.dat', 'w') as f:
        f.write("# energy (keV), cx (mm), cy (mm), dx (mm), dy (mm), flux, GoodRays\n")
    #for E in energies:
    #    main(E[0]/1e3)
    E = 10 # keV
    main(E)
