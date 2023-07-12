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


showIn3D = False

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

load_pos = 59100
zmax = 1
t = 0.05

def build_beamline(E):
    P23_U32 = raycing.BeamLine()

    P23_U32.E = E
    if showIn3D:
        P23_U32.source = rsources.GeometricSource(
            P23_U32, 'CollimatedSource', nrays=1e5,
            dx=0.5, dz=0.5, distxprime=None, distzprime=None, energies=(E*1e3,))

    P23_U32.crl_1 = roes.ParaboloidFlatLens(
        bl=P23_U32,
        name=None,
        center=[0, 87894-load_pos-1000-7*(zmax+t), 0],
        material=lens_Be,
        focus=0.025,
        zmax=zmax,
        t=t,
        nCRL=7) # focus for 10 keV, nCRL=7

    P23_U32.crl_2 = roes.FlatParaboloidLens(
        bl=P23_U32,
        name=None,
        center=[0, 87894-load_pos-1000+7*(zmax+t), 0],
        material=lens_Be,
        focus=0.025,
        zmax=zmax,
        t=t,
        nCRL=7) # focus for 10 keV, nCRL=7

    P23_U32.screen_sample = rscreens.Screen(
        bl=P23_U32,
        name=r"U32_screen_DCM",
        center=[0, 87894-load_pos, 0])

    return P23_U32


def run_process(P23_U32):

    if showIn3D:
        loaded_beam = P23_U32.source.shine()
    else:
        loaded_beam = rsources.Beam(
                copyFrom='beam_after_mono_%02dkeV.npy' % P23_U32.E)

    paraboloidFlatLens01beamGlobal02, paraboloidFlatLens01beamLocal102, paraboloidFlatLens01beamLocal202 = P23_U32.crl_1.multiple_refract(
        beam=loaded_beam)

    flatParaboloidLens01beamGlobal02, flatParaboloidLens01beamLocal102, flatParaboloidLens01beamLocal202 = P23_U32.crl_2.multiple_refract(
        beam=paraboloidFlatLens01beamGlobal02)

    screen02beamLocal01 = P23_U32.screen_sample.expose(
        beam=flatParaboloidLens01beamGlobal02)

    outDict = {
        'loaded_beam': loaded_beam,
        'paraboloidFlatLens01beamGlobal02': paraboloidFlatLens01beamGlobal02,
        'paraboloidFlatLens01beamLocal102': paraboloidFlatLens01beamLocal102,
        'paraboloidFlatLens01beamLocal202': paraboloidFlatLens01beamLocal202,
        'flatParaboloidLens01beamGlobal02': flatParaboloidLens01beamGlobal02,
        'flatParaboloidLens01beamLocal102': flatParaboloidLens01beamLocal102,
        'flatParaboloidLens01beamLocal202': flatParaboloidLens01beamLocal202,
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
        title=r"N-PFL_N-FPL_%02dkeV.png"%E,
        fluxFormatStr=r"%g",
        saveName=r"N-PFL_N-FPL_%02dkeV.png"%E,)
    plots.append(plot_sample)

    return plots

def afterScript(P23_U32, plots, E):
    for plot in plots:
        print(P23_U32.screen_sample.center)
        with open('results_N-PFL_N-FPL.dat', 'a') as f:
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

    with open('results_N-PFL_N-FPL.dat', 'w') as f:
        f.write("# energy (keV), cx (mm), cy (mm), dx (mm), dy (mm), flux, GoodRays\n")
    #for E in energies:
    #    main(E[0]/1e3)
    E = 10 # keV
    main(E)
