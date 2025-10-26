import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import MatplotlibSettings
import ROOT




###############################################################################
## taken from:https://higgshunter.wordpress.com/2013/04/18/error-band-graph-in-pyroot/
## Edited by : HH :)
## some deprecated methods changed, added return
import ctypes ## HH: this is needed for ctypes variable type, ROOT.Double is obsolete!
def DrawErrorBand(graph):
    isErrorBand = graph.GetErrorYhigh(0) != -1 and graph.GetErrorYlow(0) != -1
    npoints     = graph.GetN()

    if not isErrorBand:
        graph.Draw("l")
        return

    # Declare individual TGraph objects used in drawing error band
    central, min, max = ROOT.TGraph(), ROOT.TGraph(), ROOT.TGraph()
    shapes = []
    for i in range((npoints-1)*4):
        shapes.append(ROOT.TGraph())

    # Set ownership of TGraph objects
    ROOT.SetOwnership(central, False)
    ROOT.SetOwnership(    min, False)
    ROOT.SetOwnership(    max, False)
    for shape in shapes:
        ROOT.SetOwnership(shape, False)

    # Get data points from TGraphAsymmErrors
    x, y, ymin, ymax = [], [], [], []
    xs, ys=[],[] ### HH
    for i in range(npoints):
        tmpX, tmpY =ctypes.c_double(0.), ctypes.c_double(0.) ## HH: using "ROOT.Double" will raise error
        graph.GetPoint(i, tmpX, tmpY)
        x.append(tmpX)
        y.append(tmpY)
        ymin.append(tmpY.value - graph.GetErrorYlow(i)) ## HH
        ymax.append(tmpY.value + graph.GetErrorYhigh(i)) ## HH
        #xs.append(tmpX.value) ## HH
        #ys.append(tmpY.value) ## HH
    xs = np.array([item.value for item in x]) ## HH
    ys = np.array([item.value for item in y]) ## HH
    ymins = np.array(ymin) ## HH
    ymaxs = np.array(ymax) ## HH
    # Fill central, min and max graphs
    for i in range(npoints):
        central.SetPoint(i, x[i], y[i])
        min.SetPoint(i, x[i], ymin[i])
        max.SetPoint(i, x[i], ymax[i])

    # Fill shapes which will be shaded to create the error band
    for i in range(npoints-1):
        for version in range(4):
            shapes[i+(npoints-1)*version].SetPoint((version+0)%4, x[i],   ymax[i])
            shapes[i+(npoints-1)*version].SetPoint((version+1)%4, x[i+1], ymax[i+1])
            shapes[i+(npoints-1)*version].SetPoint((version+2)%4, x[i+1], ymin[i+1])
            shapes[i+(npoints-1)*version].SetPoint((version+3)%4, x[i],   ymin[i])

    # Set attributes to those of input graph
    central.SetLineColor(graph.GetLineColor())
    central.SetLineStyle(graph.GetLineStyle())
    central.SetLineWidth(graph.GetLineWidth())
    min.SetLineColor(graph.GetLineColor())
    min.SetLineStyle(graph.GetLineStyle())
    max.SetLineColor(graph.GetLineColor())
    max.SetLineStyle(graph.GetLineStyle())
    for shape in shapes:
        shape.SetFillColor(graph.GetFillColor())
        shape.SetFillStyle(graph.GetFillStyle())

    # Draw
    for shape in shapes:
        shape.Draw("f")
    min.Draw("l")
    max.Draw("l")
    central.Draw("l")
    ROOT.gPad.RedrawAxis()
    res=[xs,ys,ymins,ymaxs] ## HH
    return res #HH
###############################################################################

modelfolder=['./comparision-other-group/NLO-dijet','./comparision-other-group/NNLO-dijet']

Q2=[10,100]
# Initialize empty dictionaries
xv_S   = {}
yv_S   = {}
ymin_S = {}
ymax_S = {}
xv_g   = {}
yv_g   = {}
ymin_g = {}
ymax_g = {}


for q_2 in Q2:
    f1 = ROOT.TFile(modelfolder[0]+"/out.root","READ")
    f2 = ROOT.TFile(modelfolder[1]+"/out.root","READ")
    #f2.ls()
    q2_str = str(q_2)
    address= "SaveDPDFTGraph/Q2_" + q2_str + "__xpom_0.0030;1"
    maral1=f1.Get(address)
    # maral2=f2.Get(address)
    # #maral2.ls()
    maral12=maral1.Get("DPDF_ErrorsSymm;1/")
    # maral22=maral2.Get("DPDF_ErrorsSymm;1/")
    NLO_sigma=maral12.Get("SIGMA;1")
    NLO_gluon=maral12.Get("gluon;1")
    # NNLO_sigma=maral22.Get("SIGMA;1")
    # NNLO_gluon=maral22.Get("gluon;1")

    # store in arrays for plotting with matplotlib
    xv_S[q2_str], yv_S[q2_str], ymin_S[q2_str], ymax_S[q2_str] = DrawErrorBand(NLO_sigma)
    xv_g[q2_str], yv_g[q2_str], ymin_g[q2_str], ymax_g[q2_str] = DrawErrorBand(NLO_gluon)

