# -*- coding: utf-8 -*-
"""

__author__ = "Konstantin Klementiev", "Roman Chernikov"
__date__ = "2022-11-17"

Created with xrtQook




"""

import numpy as np
import sys
sys.path.append(r"D:\xrt-1.5.0")
import xrt.backends.raycing.sources as rsources
import xrt.backends.raycing.screens as rscreens
import xrt.backends.raycing.materials as rmats
import xrt.backends.raycing.oes as roes
import xrt.backends.raycing.apertures as rapts
import xrt.backends.raycing.run as rrun
import xrt.backends.raycing as raycing
import xrt.plotter as xrtplot
import xrt.runner as xrtrun

Be = rmats.Material(
    elements=r"Be",
    rho=1.8,
    name=r"Beryllium")


def build_beamline():
    beamLine = raycing.BeamLine()

    beamLine.undulator01 = rsources.Undulator(
        bl=beamLine,
        center=[0, 0, 0],
        xPrimeMax=0.025,
        zPrimeMax=0.025,
        targetE=[9000, 3],
        eMin=8999,
        eMax=9001,
        targetOpenCL=r"auto",
        precisionOpenCL=r"auto",
        name='U1')

    beamLine.paraboloidFlatLens01 = roes.ParaboloidFlatLens(
        bl=beamLine,
        shape='round',
        focus=1,
        t=5,
        zmax=6,
        center=[0, 10000, 0],
        nCRL=40,
        material=Be,
        name='ParaFlat')

    beamLine.undulator02 = rsources.Undulator(
        bl=beamLine,
        center=[5, 0, 0],
        xPrimeMax=0.025,
        zPrimeMax=0.025,
        targetE=[9000, 3],
        eMin=8999,
        eMax=9001,
        targetOpenCL=r"auto",
        precisionOpenCL=r"auto",
        name="U2")

    beamLine.FlatParaboloidLens02 = roes.FlatParaboloidLens(
        bl=beamLine,
        shape='round',
        focus=1,
        t=5,
        zmax=6,
        center=[5, 10000, 0],
        nCRL=40,
        material=Be,
        name='FlatPara')

    beamLine.undulator03 = rsources.Undulator(
        bl=beamLine,
        center=[10, 0, 0],
        xPrimeMax=0.025,
        zPrimeMax=0.025,
        targetE=[9000, 3],
        eMin=8999,
        eMax=9001,
        targetOpenCL=r"auto",
        precisionOpenCL=r"auto",
        name="U3")

    beamLine.DoubleParaboloidLens03 = roes.DoubleParaboloidLens(
        bl=beamLine,
        shape='round',
        focus=1,
        t=10,
        zmax=12,
        center=[10, 10000, 0],
        nCRL=40,
        material=Be,
        name='DoublePara')

    beamLine.screen01 = rscreens.Screen(
        bl=beamLine,
        name='Screen1',
        center=[0, 50000, 0])

    beamLine.screen02 = rscreens.Screen(
        bl=beamLine,
        name='Screen2',
        center=[5, 50000, 0])

    beamLine.screen03 = rscreens.Screen(
        bl=beamLine,
        name='Screen3',
        center=[10, 50000, 0])

    return beamLine


def run_process(beamLine):
    undulator01beamGlobal = beamLine.undulator01.shine()
    undulator02beamGlobal = beamLine.undulator02.shine()
    undulator03beamGlobal = beamLine.undulator03.shine()

    Lens01beamGlobal, Lens01beamLocal1, Lens01beamLocal2 = beamLine.paraboloidFlatLens01.multiple_refract(
        beam=undulator01beamGlobal)

    screen01beamLocal = beamLine.screen01.expose(
        beam=Lens01beamGlobal)

    Lens02beamGlobal, Lens02beamLocal1, Lens02beamLocal2 = beamLine.FlatParaboloidLens02.multiple_refract(
        beam=undulator02beamGlobal)

    screen02beamLocal = beamLine.screen02.expose(
        beam=Lens02beamGlobal)

    Lens03beamGlobal, Lens03beamLocal1, Lens03beamLocal2 = beamLine.DoubleParaboloidLens03.multiple_refract(
        beam=undulator03beamGlobal)

    screen03beamLocal = beamLine.screen03.expose(
        beam=Lens03beamGlobal)

    outDict = {
        'undulator01beamGlobal': undulator01beamGlobal,
        'undulator02beamGlobal': undulator02beamGlobal,
        'undulator03beamGlobal': undulator03beamGlobal,

        'Lens01beamGlobal': Lens01beamGlobal,
        'Lens01beamLocal1': Lens01beamLocal1,
        'Lens01beamLocal2': Lens01beamLocal2,

        'Lens02beamGlobal': Lens02beamGlobal,
        'Lens02beamLocal1': Lens02beamLocal1,
        'Lens02beamLocal2': Lens02beamLocal2,

        'Lens03beamGlobal': Lens03beamGlobal,
        'Lens03beamLocal1': Lens03beamLocal1,
        'Lens03beamLocal2': Lens03beamLocal2,

        'screen01beamLocal': screen01beamLocal,
        'screen02beamLocal': screen02beamLocal,
        'screen03beamLocal': screen03beamLocal,
        }
    beamLine.prepare_flow()
    return outDict


rrun.run_process = run_process



def define_plots():
    plots = []

    plot01 = xrtplot.XYCPlot(
        beam=r"screen01beamLocal01",
        xaxis=xrtplot.XYCAxis(
            label=r"x"),
        yaxis=xrtplot.XYCAxis(
            label=r"z"),
        caxis=xrtplot.XYCAxis(
            label=r"energy",
            unit=r"eV"),
        title=r"plot01")
    plots.append(plot01)
    return plots


def main():
    beamLine = build_beamline()
    beamLine.glow()
#    E0 = 0.5 * (beamLine.undulator01.eMin +
#                beamLine.undulator01.eMax)
#    beamLine.alignE=E0
#    plots = define_plots()
#    xrtrun.run_ray_tracing(
#        plots=plots,
#        backend=r"raycing",
#        beamLine=beamLine)


if __name__ == '__main__':
    main()
