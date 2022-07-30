# This module modifies some of the routines in the matplotlib module. The code
# for the modified routines are copied here and modified.
# Copyright (c) 2012-2013 Matplotlib Development Team; All Rights Reserved

import wx
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import (
    NavigationToolbar2WxAgg as NavigationToolbar,
)
from matplotlib.figure import Figure
import os
import warnings
from scipy.io import savemat

from matplotlib.backends.backend_wx import error_msg_wx


class myToolbar(NavigationToolbar):
    # overwritten to save plot as .mat files
    def save_figure(self, *args):
        # Fetch the required filename and file type.
        filetypes, exts, filter_index = self.canvas._get_imagesave_wildcards()
        default_file = self.canvas.get_default_filename()
        dlg = wx.FileDialog(
            self.canvas,
            "Save to file",
            "",
            default_file,
            filetypes,
            wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
        )
        dlg.SetFilterIndex(filter_index)
        if dlg.ShowModal() == wx.ID_OK:
            dirname = dlg.GetDirectory()
            filename = dlg.GetFilename()
            print("Save file dir:%s name:%s" % (dirname, filename), 3, self)
            format = exts[dlg.GetFilterIndex()]
            _basename, ext = os.path.splitext(filename)
            if ext.startswith("."):
                ext = ext[1:]
            if ext in ("svg", "pdf", "ps", "eps", "png") and format != ext:
                # looks like they forgot to set the image type drop
                # down, going with the extension.
                warnings.warn(
                    "extension %s did not match the selected image type %s; going with %s"
                    % (ext, format, ext),
                    stacklevel=0,
                )
                format = ext
            if ext == "mat":
                savemat(os.path.join(dirname, filename), self.canvas.sweepResultDict)
            else:
                try:
                    self.canvas.print_figure(
                        os.path.join(dirname, filename), format=format
                    )
                except Exception as e:
                    error_msg_wx(str(e))


class myMatplotlibPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.points = self.axes.plot([0, 0])
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.canvas = FigureCanvas(self, -1, self.figure)
        self.canvas.filetypes["mat"] = "MATLAB"  # Add mat filetype to save file dialog
        self.toolbar = myToolbar(self.canvas)
        vbox.Add(self.canvas, 1, wx.EXPAND)
        vbox.Add(self.toolbar, 0, wx.EXPAND)
        self.SetSizer(vbox)
