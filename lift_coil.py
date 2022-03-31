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

if MDSplus.version.ispy2:
    def tostr(x):
        return x

    def tobytes(x):
        return x
else:
    def tostr(x):
        return b if isinstance(b, str) else b.decode('utf-8')

    def tobytes(x):
        return s if isinstance(s, bytes) else s.encode('utf-8')


class LIFT_COIL(MDSplus.Device):
    """

    Lift Coil for levitated bagel.

    Dnventually there will be 2 one top and one bottom, for now
    there is only 1

    The lift coil accepts a demand as a floating point value from -1. to 1. to
    tell the chopper about the duty cycle and direction.

    The physical quanity being controled is Volts in the coil.

    HAL is done by PCS
    Rate is 500 Hz
    Recipe
       Voltage setting on PS
    Configuration
       Direction
       Number of Turns
       Z_Pos  (do we need top and bottom ? or is this the pos of the middle ?)
       Radius
    Communications:
       SDN

    Methods:
       check - make sure Recipe matches, what else
       configure
       start
       stop

    debugging() - is debugging enabled.
                  Controlled by environment variable DEBUG_DEVICES

    THINK ABOUT:  Config values here?  or references, if here can check against current truth
    THINK ABOUT:  Recipe values here?  or references, if here can check against current truth

    """

    parts = [
        {
          'path': ':GUID',
          'type': 'text',
          'value': '3cdd2a9a-b2f7-4ff2-b018-4cebbfaaf866',
          'options': ('no_write_shot',)
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
          'path': '.PARAMETERS.CONFIG', 
          'type': 'structure', 
          'help': 'Configuration parameters are parameters that in general do not change'
        },
        {
          'path': '.PARAMETERS.CONFIG:DIRECTION', 
          'type': 'text', 
          'value': "up", 
          'options': ('no_write_shot',), 
          'help': 'Is the coil pointing up or down (right hand rule)'
        },
        {
          'path': '.PARAMETERS.CONFIG:TURNS', 
          'type': 'numeric', 
          'value': 100, 
          'options': ('no_write_shot',), 
          'help': 'Number of turns in the coil'
        },
        {
          'path': '.PARAMETERS.CONFIG:R', 
          'type': 'numeric', 
          'value': .05, 
          'options': ('no_write_shot',), 
          'help':'Radius of coil in M'
        },
        {
          'path': '.PARAMETERS.CONFIG:Z', 
          'type': 'numeric', 
          'value': .07, 
          'options': ('no_write_shot',), 
          'help':'Distance of coil from center in M'
        },
        {
          'path': '.PARAMETERS.RECIPE', 
          'type': 'structure'
        },
        {
          'path': '.PARAMETERS.RECIPE:PS_VOLT', 
          'type': 'numeric', 
          'value': 18, 
          'options': ('no_write_shot',), 
          'help':'Power Supply Voltage Setting'
        },
        {
          'path': '.SIGNALS',
          'type': 'structure'
        },
        {
          'path': '.SIGNALS:DEMAND', 
          'type': 'signal',  
          'options': ('no_write_model', 'write_once',), 
          'help':'Demand voltage requested'
        },
        {
          'path': '.SIGNALS:DEMAND:HAL',
          'type': 'text',
          'value': '_out := _in * 1. + 0.',
          'options': ('no_write_shot',),
          'help':'Expression to make values from demand voltages'
        },
        {
          'path': '.SIGNALS:RATE',
          'type': 'numeric',
          'value': 500,
          'options': ('no_write_shot',),
          'help':'rate in Hz'
        },
        {
          'path': '.SIGNALS:PHASE',
          'type': 'numeric',
          'value': 0.0,
          'options': ('no_write_shot',),
          'help':'Phase of timing relative to even second'
        },
        {
          'path': '.SIGNALS:MAX_MISSING',
          'type': 'numeric',
          'value': 1,
          'options': ('no_write_shot',),
          'help':'Maximum allowed missing samples'
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
