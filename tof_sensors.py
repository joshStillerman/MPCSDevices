#
# Copyright (c) 2018, Massachusetts Institute of Technology All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# Redistributions in binary form must reproduce the above copyright notice, this
# list of conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
import MDSplus
import time
import datetime
import numpy as np

class TOF_SENSORS(MDSplus.Device):
    """

    Optical TOF sensors for levitated bagel.

    Set of 4 distance sensors for the levitated bagel.

    This will arrive on the MSdn as 4 floats at 100Hz
    
    The physical quanity being controled is m.

    HAL is done by PCS
    Rate is 100 Hz
    Immuttable Parameters
       raw_shape
       raw_type
       phys_shape
       phys_type
       r[4]
       z[4]
       phi[4]
    Muttable Parameters
      none
    Communications:
       SDN

    Methods:
       check - make sure Recipe matches, what else
       configure
       start
       stop

    debugging() - is debugging enabled.
                  Controlled by environment variable DEBUG_DEVICES
    """

    parts = [
        {
          'path': ':GUID',
          'type': 'text',
          'value': 'f71fdc7a-affe-4163-b4b1-3951a4f9dc1f',
          'options': ('write_once', 'no_write_shot',)
        },
        {
          'path': ':THIS_GUID',
          'type': 'text',
          'options': ('write_once', 'no_write_shot',),
          'help':'The GUID of this instance.'
        },
        {
          'path': ':NAME',
          'type': 'text',
          'options': ('write_once', 'no_write_shot',),
          'help':'The name of this set of optical sensors'
        },
        {
          'path': ':COMMENT', 
          'type': 'text', 
          'options': ('no_write_shot',)
        },
        {
          'path': '.PARAMETERS', 
          'type': 'structure'
        },
        {
          'path': '.PARAMETERS.IMMUTTABLE', 
          'type': 'structure', 
          'help': 'Parameters with fixed values for this contract'
        },
        {
          'path': '.PARAMETERS.IMMUTTABLE:RAW_SHAPE',
          'type': 'numeric',
          'value': MDSplus.Int32Array([4]),
          'options': ('no_write_shot','write_once',),
          'help':'Shape of data on the wire'
        },
        {
          'path': '.PARAMETERS.IMMUTTABLE:PHYS_SHAPE',
          'type': 'numeric',
          'value': MDSplus.Int32Array([4]),
          'options': ('no_write_shot','write_once',),
          'help':'Shape of data in physics Units'
        },
        {
          'path': '.PARAMETERS.IMMUTTABLE:RAW_TYPE',
          'type': 'text',
          'value': 'float',
          'options': ('no_write_shot','write_once',),
          'help':'Type of the data on the wire'
        },
        {
          'path': '.PARAMETERS.IMMUTTABLE:PHYS_TYPE',
          'type': 'text',
          'value': 'float',
          'options': ('no_write_shot','write_once',),
          'help':'Type of the data in physics units'
        },
        {
          'path': '.PARAMETERS.IMMUTTABLE:RATE',
          'type': 'numeric',
          'value': 100,
          'options': ('no_write_shot','write_once',),
          'help':'rate in Hz'
        },
        {
          'path': '.PARAMETERS.IMMUTTABLE:PHASE',
          'type': 'numeric',
          'value': 0.0,
          'options': ('no_write_shot','write_once',),
          'help':'Phase of timing relative to even second'
        },
        { 
          'path': '.PARAMETERS.IMMUTTABLE:R',
          'type': 'numeric',
          'value': MDSplus.Float64Array([.02, .02, .02, .02]),
          'options': ('no_write_shot','write_once',),
          'help':'radius the sensors in m'
        },
        {
          'path': '.PARAMETERS.IMMUTTABLE:Z',
          'type': 'numeric',
          'value': MDSplus.Float64Array([.068, .068, .068, .068]),
          'options': ('no_write_shot','write_once',),
          'help':'z position of the sensors in m'
        },
        {
          'path': '.PARAMETERS.IMMUTTABLE:PHI',
          'type': 'numeric',
          'value': MDSplus.Float64Array([0., 90., 180., 270.]),
          'options': ('no_write_shot','write_once',),
          'help':'angle of the sensors in degrees'
        },
        {
          'path': '.PARAMETERS.MUTTABLE', 
          'type': 'structure'
        },
        {
          'path': '.SIGNALS',
          'type': 'structure'
        },
        {
          'path': '.SIGNALS:HEIGHT', 
          'type': 'SIGNAL',
          'options': ('no_write_model', 'write_once',), 
          'help':'The heights as measured by the for sensors'
        },
        {
          'path': '.SIGNALS:HEIGHT:HAL',
          'type': 'text',
          'value': '_out := _in * [1.,1.,1., 1.] + [0., 0., 0., 0.]', 
          'options': ('no_write_shot',),
          'help':'Expression to make values from demand voltages'
        },
        {
          'path': '.SIGNALS:MAX_MISSING',
          'type': 'numeric',
          'value': 1,
          'options': ('no_write_shot',),
          'help':'Maximum allowed missing samples'
        },
        {
          'path': '.COMMS',
          'type': 'structure',
        },
        {
          'path': '.COMMS:TRANSPORT',
          'type': 'text',
          'value': 'SDN',
          'options': ('no_write_shot','write_once',),
          'help':'Use SDN for communication'
        },
        {
          'path': '.COMMS:ADDRESS',
          'type': 'text',
          'value': '244.0.0.0',
          'options': ('no_write_shot','write_once',),
          'help':'Multicast address'
        },
        {
          'path': '.COMMS:PORT',
          'type': 'numeric',
          'value': 1234,
          'options': ('no_write_shot','write_once',),
          'help':'Multicast address'
        },
        {
          'path': '.COMMS:NAME',
          'type': 'text',
          'options': ('write_once', 'no_write_shot',),
          'help':'Name string to send with the message'
        },
        {
          'path': ':CHECK_ACTION', 
          'type': 'action',
          'valueExpr': "Action(Dispatch('S','CHECK',50,None),Method(None,'CHECK',head))", 
          'options': ('no_write_shot',)
        },
        {
          'path': ':CONF_ACTION', 
          'type': 'action',
          'valueExpr': "Action(Dispatch('S','CONFIG',50,None),Method(None,'CONFIG',head))", 
          'options': ('no_write_shot',)
        },
        {
          'path': ':START_ACTION', 
          'type': 'action',
          'valueExpr': "Action(Dispatch('S','PREPULSE',50,None),Method(None,'START',head))", 
          'options': ('no_write_shot',)
        },
        {
          'path': ':STOP_ACTION', 
          'type': 'action',
          'valueExpr': "Action(Dispatch('S','DONE',50,None),Method(None,'STOP',head))", 
          'options': ('no_write_shot',)
        },
    ]

    debug = None

    def debugging(self):
        import os
        if self.debug == None:
            self.debug = os.getenv("DEBUG_DEVICES")
        return(self.debug)

    @staticmethod
    def Add(*a, **ka):
        import uuid
        head = super(TOF_SENSORS, TOF_SENSORS).Add(*a, **ka)
        head.this_guid.record = str(uuid.uuid4())
        return head

