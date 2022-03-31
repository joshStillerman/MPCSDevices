# MPCSDevices

A set of MDSplus devices to deal with MPCS data contracts.

To use clone this repo
```
git clone https://github.com/joshStillerman/MPCSDevices.git
```
add the new directory to the MDS_PYDEVICEPATH
```
export MDS_PYDEVICE_PATH="$MDS_PYDEVICE_PATH;$PWD/MPCSDevices"
```
Then you can add a lift_coil device to your tree:
```
jas@mfews-jas:~/MPCSDevices$ mdstcl
TCL> edit /new test
TCL> add node top_coil/model=lift_coil
TCL> dir ***

\TEST::TOP

 :TOP_COIL    

Total of 1 node.

\TEST::TOP:TOP_COIL

 :CHECK_ACTION :COMMENT      :CONF_ACTION  :GUID         :START_ACTION
 :STOP_ACTION 

  PARAMETERS    SIGNALS     

Total of 8 nodes.

\TEST::TOP:TOP_COIL.PARAMETERS

  CONFIG        RECIPE      

Total of 2 nodes.

\TEST::TOP:TOP_COIL.SIGNALS

 :DEMAND       :MAX_MISSING  :PHASE        :RATE        

Total of 4 nodes.

\TEST::TOP:TOP_COIL.PARAMETERS.CONFIG

 :DIRECTION    :R            :TURNS        :Z           

Total of 4 nodes.

\TEST::TOP:TOP_COIL.PARAMETERS.RECIPE

 :PS_VOLT     

Total of 1 node.

\TEST::TOP:TOP_COIL.SIGNALS:DEMAND

 :HAL         

Total of 1 node.


Grand total of 21 nodes.
TCL>
```
