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
import sip



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
        self.dec = dec = 1
        self.audio_rate = audio_rate = 48000
        self.samp_rate = samp_rate = audio_rate*dec
        self.xlating_taps = xlating_taps = firdes.low_pass(1.0, samp_rate, 1000,400, window.WIN_HAMMING, 6.76)
        self.vco_max = vco_max = 2500
        self.v_fsk = v_fsk = 1
        self.t_bit = t_bit = 0.022
        self.f_space = f_space = 2125
        self.f_mark = f_mark = 2295

        ##################################################
        # Blocks
        ##################################################

        self.zeromq_pub_sink_0 = zeromq.pub_sink(gr.sizeof_float, 1, 'tcp://127.0.0.1:4444', 100, False, (-1), '', True, True)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_fcc(1, xlating_taps, ((f_space+f_mark)/2), samp_rate)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_vector_source_x_0 = blocks.vector_source_b((90,69,82,79), True, 1, [])
        self.blocks_vco_f_0 = blocks.vco_f(samp_rate, (2*np.pi*vco_max), v_fsk)
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(8)
        self.blocks_uchar_to_float_1 = blocks.uchar_to_float()
        self.blocks_uchar_to_float_0 = blocks.uchar_to_float()
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_char*1, (int(samp_rate*t_bit)))
        self.blocks_null_source_0 = blocks.null_source(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(((f_mark-f_space)/vco_max))
        self.blocks_add_const_vxx_0 = blocks.add_const_ff((f_space/vco_max))
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf((samp_rate/(2*np.pi*(f_mark-f_space))))


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_vco_f_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_null_source_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_uchar_to_float_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.blocks_uchar_to_float_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_uchar_to_float_1, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_uchar_to_float_1, 0), (self.zeromq_pub_sink_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.blocks_vco_f_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_unpack_k_bits_bb_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.blocks_uchar_to_float_1, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.analog_quadrature_demod_cf_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "fskMod")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_dec(self):
        return self.dec

    def set_dec(self, dec):
        self.dec = dec
        self.set_samp_rate(self.audio_rate*self.dec)

    def get_audio_rate(self):
        return self.audio_rate

    def set_audio_rate(self, audio_rate):
        self.audio_rate = audio_rate
        self.set_samp_rate(self.audio_rate*self.dec)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_xlating_taps(firdes.low_pass(1.0, self.samp_rate, 1000, 400, window.WIN_HAMMING, 6.76))
        self.analog_quadrature_demod_cf_0.set_gain((self.samp_rate/(2*np.pi*(self.f_mark-self.f_space))))
        self.blocks_repeat_0.set_interpolation((int(self.samp_rate*self.t_bit)))
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)

    def get_xlating_taps(self):
        return self.xlating_taps

    def set_xlating_taps(self, xlating_taps):
        self.xlating_taps = xlating_taps
        self.freq_xlating_fir_filter_xxx_0.set_taps(self.xlating_taps)

    def get_vco_max(self):
        return self.vco_max

    def set_vco_max(self, vco_max):
        self.vco_max = vco_max
        self.blocks_add_const_vxx_0.set_k((self.f_space/self.vco_max))
        self.blocks_multiply_const_vxx_0.set_k(((self.f_mark-self.f_space)/self.vco_max))

    def get_v_fsk(self):
        return self.v_fsk

    def set_v_fsk(self, v_fsk):
        self.v_fsk = v_fsk

    def get_t_bit(self):
        return self.t_bit

    def set_t_bit(self, t_bit):
        self.t_bit = t_bit
        self.blocks_repeat_0.set_interpolation((int(self.samp_rate*self.t_bit)))

    def get_f_space(self):
        return self.f_space

    def set_f_space(self, f_space):
        self.f_space = f_space
        self.analog_quadrature_demod_cf_0.set_gain((self.samp_rate/(2*np.pi*(self.f_mark-self.f_space))))
        self.blocks_add_const_vxx_0.set_k((self.f_space/self.vco_max))
        self.blocks_multiply_const_vxx_0.set_k(((self.f_mark-self.f_space)/self.vco_max))
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(((self.f_space+self.f_mark)/2))

    def get_f_mark(self):
        return self.f_mark

    def set_f_mark(self, f_mark):
        self.f_mark = f_mark
        self.analog_quadrature_demod_cf_0.set_gain((self.samp_rate/(2*np.pi*(self.f_mark-self.f_space))))
        self.blocks_multiply_const_vxx_0.set_k(((self.f_mark-self.f_space)/self.vco_max))
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
