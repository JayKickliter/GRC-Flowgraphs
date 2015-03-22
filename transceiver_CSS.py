#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: IEEE 802.15.4 Transceiver using CSS PHY
# Description: IEEE 802.15.4 Transceiver using CSS PHY
# Generated: Sat Mar 21 18:49:04 2015
##################################################

execfile("/Users/jay/.grc_gnuradio/ieee802_15_4_oqpsk_phy.py")
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import fosphor
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import foo
import ieee802_15_4
import osmosdr
import pmt
import time
import wx

class transceiver_CSS(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="IEEE 802.15.4 Transceiver using CSS PHY")

        ##################################################
        # Variables
        ##################################################
        self.text_msg = text_msg = "Hello World, this is GNU Radio using the IEEE 802.15.4 CSS PHY!"
        self.freq = freq = 2480000000
        self.samp_rate = samp_rate = 4e6
        self.msg_interval = msg_interval = 1000
        self.gain = gain = 20
        self.cur_freq = cur_freq = freq
        self.c = c = ieee802_15_4.css_phy(chirp_number=4, phy_packetsize_bytes=len(text_msg)+15)

        ##################################################
        # Blocks
        ##################################################
        self.nb = self.nb = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
        self.nb.AddPage(grc_wxgui.Panel(self.nb), "RX Waterfall")
        self.nb.AddPage(grc_wxgui.Panel(self.nb), "RX FFT")
        self.nb.AddPage(grc_wxgui.Panel(self.nb), "RX Time")
        self.nb.AddPage(grc_wxgui.Panel(self.nb), "RX Symbols")
        self.Add(self.nb)
        _gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_gain_sizer,
        	value=self.gain,
        	callback=self.set_gain,
        	label="TX/RX Gain",
        	converter=forms.int_converter(),
        	proportion=0,
        )
        self._gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_gain_sizer,
        	value=self.gain,
        	callback=self.set_gain,
        	minimum=1,
        	maximum=100,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=int,
        	proportion=1,
        )
        self.Add(_gain_sizer)
        self._freq_chooser = forms.radio_buttons(
        	parent=self.GetWin(),
        	value=self.freq,
        	callback=self.set_freq,
        	label="Channel",
        	choices=[1000000 * (2400 + 5 * (i - 10)) for i in range(11, 27)],
        	labels=[i for i in range(11, 27)],
        	style=wx.RA_HORIZONTAL,
        )
        self.Add(self._freq_chooser)
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "bladerf" )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(2, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(True, 0)
        self.osmosdr_source_0.set_gain(gain, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna("", 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
          
        _msg_interval_sizer = wx.BoxSizer(wx.VERTICAL)
        self._msg_interval_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_msg_interval_sizer,
        	value=self.msg_interval,
        	callback=self.set_msg_interval,
        	label="Message interval [ms]",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._msg_interval_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_msg_interval_sizer,
        	value=self.msg_interval,
        	callback=self.set_msg_interval,
        	minimum=1,
        	maximum=5000,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_msg_interval_sizer)
        self.ieee802_15_4_oqpsk_phy_0 = ieee802_15_4_oqpsk_phy()
        self.ieee802_15_4_mac_0 = ieee802_15_4.mac(True)
        self.fosphor_wx_sink_c_0 = fosphor.wx_sink_c(
        	self.nb.GetPage(0).GetWin()
        )
        self.fosphor_wx_sink_c_0.set_fft_window(window.WIN_BLACKMAN_hARRIS)
        self.fosphor_wx_sink_c_0.set_frequency_range(0, samp_rate)
        self.nb.GetPage(0).Add(self.fosphor_wx_sink_c_0.win)
        self.foo_periodic_msg_source_0 = foo.periodic_msg_source(pmt.intern("Hello World!"), 1000000, -1, True, False)
        self._cur_freq_static_text = forms.static_text(
        	parent=self.GetWin(),
        	value=self.cur_freq,
        	callback=self.set_cur_freq,
        	label="Current center frequency",
        	converter=forms.float_converter(),
        )
        self.Add(self._cur_freq_static_text)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_message_debug_0 = blocks.message_debug()

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.foo_periodic_msg_source_0, 'out'), (self.ieee802_15_4_mac_0, 'app in'))    
        self.msg_connect((self.ieee802_15_4_mac_0, 'app out'), (self.blocks_message_debug_0, 'print_pdu'))    
        self.msg_connect((self.ieee802_15_4_mac_0, 'pdu out'), (self.ieee802_15_4_oqpsk_phy_0, 'txin'))    
        self.msg_connect((self.ieee802_15_4_oqpsk_phy_0, 'rxout'), (self.ieee802_15_4_mac_0, 'pdu in'))    
        self.connect((self.ieee802_15_4_oqpsk_phy_0, 0), (self.blocks_null_sink_0, 0))    
        self.connect((self.osmosdr_source_0, 0), (self.fosphor_wx_sink_c_0, 0))    
        self.connect((self.osmosdr_source_0, 0), (self.ieee802_15_4_oqpsk_phy_0, 0))    


    def get_text_msg(self):
        return self.text_msg

    def set_text_msg(self, text_msg):
        self.text_msg = text_msg
        self.set_c(ieee802_15_4.css_phy(chirp_number=4, phy_packetsize_bytes=len(self.text_msg)+15))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.set_cur_freq(self.freq)
        self._freq_chooser.set_value(self.freq)
        self.osmosdr_source_0.set_center_freq(self.freq, 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.fosphor_wx_sink_c_0.set_frequency_range(0, self.samp_rate)

    def get_msg_interval(self):
        return self.msg_interval

    def set_msg_interval(self, msg_interval):
        self.msg_interval = msg_interval
        self._msg_interval_slider.set_value(self.msg_interval)
        self._msg_interval_text_box.set_value(self.msg_interval)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self._gain_slider.set_value(self.gain)
        self._gain_text_box.set_value(self.gain)
        self.osmosdr_source_0.set_gain(self.gain, 0)

    def get_cur_freq(self):
        return self.cur_freq

    def set_cur_freq(self, cur_freq):
        self.cur_freq = cur_freq
        self._cur_freq_static_text.set_value(self.cur_freq)

    def get_c(self):
        return self.c

    def set_c(self, c):
        self.c = c

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable realtime scheduling."
    tb = transceiver_CSS()
    tb.Start(True)
    tb.Wait()
