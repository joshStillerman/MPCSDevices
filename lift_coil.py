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
import MPCSContract
class LIFT_COIL(MPCSContract._MPCSContract):
    """

    Lift Coil for levitated bagel.

    Dnventually there will be 2 one top and one bottom, for now
    there is only 1

    The lift coil accepts a demand as a floating point value from -1. to 1. to
    tell the chopper about the duty cycle and direction.

    The physical quanity being controled is Volts in the coil.

    HAL is done by PCS
    Rate is 500 Hz
    Immuttable Parameters
       Direction
       Number of Turns
       Z_Pos  (do we need top and bottom ? or is this the pos of the middle ?)
       Radius
       Raw_Shape
       Phys_Shape
       Raw_Type
       Phys_Type
    Muttable Parameters
       Voltage setting on PS
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
          'value': '3cdd2a9a-b2f7-4ff2-b018-4cebbfaaf866',
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
          'help':'The name of this actuator coil'
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
          'path': '.PARAMETERS.IMMUTTABLE:DIRECTION', 
          'type': 'text', 
          'value': "up", 
          'options': ('no_write_shot','write_once',), 
          'help': 'Is the coil pointing up or down (right hand rule)'
        },
        {
          'path': '.PARAMETERS.IMMUTTABLE:TURNS', 
          'type': 'numeric', 
          'value': 100, 
          'options': ('no_write_shot','write_once',), 
          'help': 'Number of turns in the coil'
        },
        {
          'path': '.PARAMETERS.IMMUTTABLE:R', 
          'type': 'numeric', 
          'value': .05, 
          'options': ('no_write_shot','write_once',), 
          'help':'Radius of coil in M'
        },
        {
          'path': '.PARAMETERS.IMMUTTABLE:Z', 
          'type': 'numeric', 
          'value': .07, 
          'options': ('no_write_shot','write_once',), 
          'help':'Distance of coil from center in M'
        },
        {
          'path': '.PARAMETERS.IMMUTTABLE:RAW_SHAPE',
          'type': 'numeric',
          'value': 1,
          'options': ('no_write_shot','write_once',),
          'help':'Shape of data on the wire'
        },
        {
          'path': '.PARAMETERS.IMMUTTABLE:PHYS_SHAPE',
          'type': 'numeric',
          'value': 1,
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
          'value': 500,
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
          'path': '.PARAMETERS.MUTTABLE', 
          'type': 'structure'
        },
        {
          'path': '.PARAMETERS.MUTTABLE:PS_VOLT', 
          'type': 'numeric', 
          'value': 18, 
          'options': ('no_write_shot',), 
          'help': 'Power Supply Voltage Setting'
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
        head = super(LIFT_COIL, LIFT_COIL).Add(*a, **ka)
        head.this_guid.record = str(uuid.uuid4())
        return head
