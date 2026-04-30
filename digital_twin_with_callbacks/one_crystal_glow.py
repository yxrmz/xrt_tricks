# -*- coding: utf-8 -*-
"""

__author__ = "Konstantin Klementiev", "Roman Chernikov"
__date__ = "2026-04-30"

Created with xrtQook






"""

import numpy as np
import sys
import os
sys.path.append(r"C:\GitHub\xrt")
import xrt.backends.raycing.sources as rsources
import xrt.backends.raycing.screens as rscreens
import xrt.backends.raycing.materials as rmats
import xrt.backends.raycing.materials.elemental as rmatsel
import xrt.backends.raycing.materials.compounds as rmatsco
import xrt.backends.raycing.materials.crystals as rmatscr
import xrt.backends.raycing.oes as roes
import xrt.backends.raycing.apertures as rapts
import xrt.backends.raycing.figure_error as rfe
import xrt.backends.raycing.run as rrun
import xrt.backends.raycing as raycing
import xrt.plotter as xrtplot
import xrt.runner as xrtrun

os.environ["EPICS_CA_ADDR_LIST"] = "127.0.0.1"
os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"

from functools import partial
from epics import PV, get_pv

crystalSi01 = rmats.crystals_basic.CrystalSi(
    a=5.4307717932001225,
    d=3.1354575567115175,
    V=160.17128543981727,
    elements=['Si'],
    quantities=[1.0],
    table=r"Chantler",
    name=r"crystalSi01")


def build_beamline():
    myTestBeamline = raycing.BeamLine(
        name=r"myTestBeamline")

    myTestBeamline.bendingMagnet01 = rsources.synchr.BendingMagnet(
        bl=myTestBeamline,
        name=r"bendingMagnet01",
        center=[0, 0, 0],
        eE=3.0,
        eI=0.5,
        eSigmaX=94.86832980505137,
        eSigmaZ=4.47213595499958,
        xPrimeMax=0.5,
        zPrimeMax=0.5,
        eMin=9990.0,
        eMax=10010.0,
        rho=10.00692285594456)

    myTestBeamline.oe01 = roes.base.OE(
        bl=myTestBeamline,
        name=r"oe01",
        center=[0.0, 20000.0, 0.0],
        pitch=r"auto",
        material=crystalSi01,
        order=1)

    myTestBeamline.screen01 = rscreens.Screen(
        bl=myTestBeamline,
        name=r"screen01",
        center=[0, 21000, r"auto"],
        x=[1.0, -0.0, 0.0],
        z=[0.0, 0.0, 1.0],
        limPhysX=[-20.0, 20.0],
        limPhysY=[-10.0, 10.0],
        cLimits=[0.0, 0.0],
        histShape=[512.0, 256.0])

    return myTestBeamline


def run_process(myTestBeamline):
    bendingMagnet01_global = myTestBeamline.bendingMagnet01.shine(
        withAmplitudes=False)

    oe01_global, oe01_local = myTestBeamline.oe01.reflect(
        beam=bendingMagnet01_global)

    screen01_local = myTestBeamline.screen01.expose(
        beam=oe01_global)

    outDict = {
        'bendingMagnet01_global': bendingMagnet01_global,
        'oe01_global': oe01_global,
        'oe01_local': oe01_local,
        'screen01_local': screen01_local}
    return outDict


rrun.run_process = run_process



def define_plots():
    plots = []

    plot01 = xrtplot.XYCPlot(
        beam=r"screen01_local",
        xaxis=xrtplot.XYCAxis(
            label=r"x"),
        yaxis=xrtplot.XYCAxis(
            label=r"z"),
        caxis=xrtplot.XYCAxis(
            label=r"energy",
            unit=r"eV"),
        title=r"plot01",
        fluxFormatStr=r"%g")
    plots.append(plot01)
    return plots


def callback_update_oe(beamline=None, oeName=None, argName=None,
                       pvname=None, value=None, **kw):
    try:
        oeid = beamline.oenamesToUUIDs.get(oeName)
        cglw = beamline.blViewer.customGlWidget
        cglw.update_beamline(
                oeid, {argName: value*2})
    except Exception:
        pass


def main():
    myTestBeamline = build_beamline()
    get_pv("TST:MIRROR1:Pitch", callback=partial(
           callback_update_oe,
           beamline=myTestBeamline, oeName='oe01', argName='pitch'))

    get_pv("TST:MIRROR1:Height", callback=partial(
           callback_update_oe,
           beamline=myTestBeamline, oeName='oe01', argName='center.z'))

    myTestBeamline.glow()
#    E0 = 0.5 * (myTestBeamline.bendingMagnet01.eMin +
#                myTestBeamline.bendingMagnet01.eMax)
#    myTestBeamline.alignE=E0
#    plots = define_plots()
#    xrtrun.run_ray_tracing(
#        plots=plots,
#        backend=r"raycing",
#        beamLine=myTestBeamline)


if __name__ == '__main__':
    main()
