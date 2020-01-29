import numpy as np

from pyface.qt import QtCore, QtGui

from traits.api import Bool, Float
from traitsui.api import BasicEditorFactory
from traitsui.qt4.editor import Editor
from traitsui.qt4.image_editor import QImageView

COLORTABLE=[QtGui.qRgb(0,0,0), QtGui.qRgb(255,255,255)]
#for i in range(256): COLORTABLE.append()


class _BoolArrayEditor(Editor):
    def init(self, parent):
        self.control = QImageView()
        self._widget = QtGui.QWidget()

        self.update_editor()

        # Set up timed events
        self._widget.timer = QtCore.QTimer()
        self._widget.timer.start(self.factory.update_ms)
        self._widget.timer.timeout.connect(self.object.evolve_board)
        self._widget.timer.timeout.connect(self.update_editor)

    def update_editor(self):
        img = QtGui.QImage(
            self.object.board.astype(np.int8).data,
            self.object.board_size[1],
            self.object.board_size[0],
            QtGui.QImage.Format_Indexed8
        )
        img.setColorTable(COLORTABLE)
        self.control.setPixmap(QtGui.QPixmap.fromImage(img))

#    def init_board


class BoolArrayEditor(BasicEditorFactory):

    scale = Bool
    allow_upscaling = Bool
    preserve_aspect_ratio = Bool
    allow_clipping = Bool

    update_ms = Float(60/1000)

    klass = _BoolArrayEditor
