#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: FSK Modulator
# Author: Ben Cometto
# GNU Radio version: 3.10.10.0

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import analog
import math
from gnuradio import blocks
import pmt
from gnuradio import digital
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import zeromq
import numpy as np



class fskMod(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "FSK Modulator", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("FSK Modulator")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "fskMod")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 48000
        self.xlating_taps = xlating_taps = firdes.low_pass(1.0, samp_rate, 1000,400, window.WIN_HAMMING, 6.76)
        self.vco_max = vco_max = 2500
        self.v_fsk = v_fsk = 1
        self.t_bit = t_bit = 0.016
        self.f_space = f_space = 1800
        self.f_mark = f_mark = 2400

        ##################################################
        # Blocks
        ##################################################

        self.zeromq_push_sink_0 = zeromq.push_sink(gr.sizeof_float, 1, 'tcp://localhost:4444', 100, False, (-1), True)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_fcc(1, xlating_taps, ((f_space+f_mark)/2), samp_rate)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_uchar_to_float_1 = blocks.uchar_to_float()
        self.blocks_throttle2_0_0 = blocks.throttle( gr.sizeof_float*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_float*1, 'C:\\Users\\C25Dante.Cometto\\447_finalproject\\nocodeword.dat', False, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.intern("example_tag"))
        self.analog_simple_squelch_cc_0 = analog.simple_squelch_cc((-70), 1)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf((samp_rate/(2*np.pi*(f_mark-f_space))))


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.analog_simple_squelch_cc_0, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle2_0_0, 0))
        self.connect((self.blocks_throttle2_0_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.blocks_uchar_to_float_1, 0), (self.zeromq_push_sink_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.blocks_uchar_to_float_1, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.analog_simple_squelch_cc_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "fskMod")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_xlating_taps(firdes.low_pass(1.0, self.samp_rate, 1000, 400, window.WIN_HAMMING, 6.76))
        self.analog_quadrature_demod_cf_0.set_gain((self.samp_rate/(2*np.pi*(self.f_mark-self.f_space))))
        self.blocks_throttle2_0_0.set_sample_rate(self.samp_rate)

    def get_xlating_taps(self):
        return self.xlating_taps

    def set_xlating_taps(self, xlating_taps):
        self.xlating_taps = xlating_taps
        self.freq_xlating_fir_filter_xxx_0.set_taps(self.xlating_taps)

    def get_vco_max(self):
        return self.vco_max

    def set_vco_max(self, vco_max):
        self.vco_max = vco_max

    def get_v_fsk(self):
        return self.v_fsk

    def set_v_fsk(self, v_fsk):
        self.v_fsk = v_fsk

    def get_t_bit(self):
        return self.t_bit

    def set_t_bit(self, t_bit):
        self.t_bit = t_bit

    def get_f_space(self):
        return self.f_space

    def set_f_space(self, f_space):
        self.f_space = f_space
        self.analog_quadrature_demod_cf_0.set_gain((self.samp_rate/(2*np.pi*(self.f_mark-self.f_space))))
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(((self.f_space+self.f_mark)/2))

    def get_f_mark(self):
        return self.f_mark

    def set_f_mark(self, f_mark):
        self.f_mark = f_mark
        self.analog_quadrature_demod_cf_0.set_gain((self.samp_rate/(2*np.pi*(self.f_mark-self.f_space))))
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(((self.f_space+self.f_mark)/2))




def main(top_block_cls=fskMod, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
