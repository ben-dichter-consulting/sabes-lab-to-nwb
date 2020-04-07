# Import relevant modules

import numpy as np
import datetime
from dateutil.tz import tzlocal
import pytz
import h5py
from hdmf.backends.hdf5 import H5DataIO
import hdf5storage
import os
from pynwb import NWBFile, NWBHDF5IO, ProcessingModule
from pynwb.device import Device
from pynwb.base import TimeSeries
from pynwb.ecephys import ElectrodeGroup, SpikeEventSeries


# Load the .mat files containing sorted spikes

path_to_files = 'C:/Users/Admin/Desktop/Ben Dichter/nwbn-conversion-tools/datafiles'

# Open info file
fname0 = 'indy_20160407_02.mat'
fpath0 = os.path.join(path_to_files, fname0)
f_info = hdf5storage.loadmat(fpath0)
#f_info = h5py.File(fpath0)
info = f_info.keys()
#f_info['spikes']


# Create a new NWB file instance

session_start_time = datetime.datetime(2016,4,7,tzinfo=pytz.timezone("America/Los_Angeles"))
experiment_description = 'The behavioral task was to make self-paced reaches to targets arranged in a grid (e.g. 8x8) without gaps or pre-movement delay intervals.'

nwb = NWBFile(session_description='Multichannel Sensorimotor Cortex Electrophysiology', 
              identifier='indy_20160407_02', 
              session_start_time=session_start_time,
              experimenter='Joseph E. ODoherty',
              lab='Sabes lab',
              institution='University of California, San Francisco',
              experiment_description='experiment_description',
              session_id='indy_20160407_02')


# Create Device and ElectrodeGroup and adding electrode information to nwb.


# M1

#Create device
device_M1 = Device('Recording_Device_M1')
nwb.add_device(device_M1)

# Create electrode group
electrode_group_M1 = ElectrodeGroup(name='ElectrodeArray_M1', description="96 Channels Electrode Array", 
                                    location="Motor Cortex", 
                                    device=device_M1)

# Add metadata about each electrode in the group
for idx in np.arange(96):
    nwb.add_electrode(x=np.nan, y=np.nan, z=np.nan,
                      imp=np.nan,
                      location='M1', filtering='none',
                      group=electrode_group_M1)


# S1

# Create device
device_S1 = Device('Recording_Device_S1')
nwb.add_device(device_S1)

# Create electrode group
electrode_group_S1 = ElectrodeGroup(name='ElectrodeArray_S1', description="96 Channels Electrode Array", 
                                    location="Somatosensory Cortex", 
                                    device=device_S1)

# Add metadata about each electrode in the group
for idx in np.arange(96):
    nwb.add_electrode(x=np.nan, y=np.nan, z=np.nan,
                      imp=np.nan,
                      location='S1', filtering='none',
                      group=electrode_group_S1)


#Store unsorted spike waveforms data in acquisition group


# M1

# Create electrode table region
electrode_table_region_M1 = nwb.create_electrode_table_region(list(range(96)), 'the 96 electrodes in the array M1')

# Create SpikeEventSeries container to store unsorted spike waveform data.
description = 'Unsorted spike event waveform "snippets". Each waveform corresponds to a timestamp in "spikes".'
comments = 'Waveform samples are in microvolts.'
ephys_ts_M1 = SpikeEventSeries(name='M1 Spike Events',
                            data=f_info['wf'][0:96,:][:,0],
                            timestamps=f_info['spikes'][0:96,:][:,0],
                            electrodes=electrode_table_region_M1,
                            resolution=4.096e-05,
                            conversion=1e-6,
                            description=description,
                            comments=comments)

nwb.add_acquisition(ephys_ts_M1)


# S1

# Create electrode table region
electrode_table_region_S1 = nwb.create_electrode_table_region(list(range(96)), 'the 96 electrodes in the array S1')

# Create SpikeEventSeries container to store unsorted spike waveform data.
description = 'Unsorted spike event waveform "snippets". Each waveform corresponds to a timestamp in "spikes".'
comments = 'Waveform samples are in microvolts.'
ephys_ts_S1 = SpikeEventSeries(name='S1 Spike Events',
                            data=f_info['wf'][96:192,:][:,0],
                            timestamps=f_info['spikes'][96:192,:][:,0],
                            electrodes=electrode_table_region_S1,
                            resolution=4.096e-05,
                            conversion=1e-6,
                            description=description,
                            comments=comments)

nwb.add_acquisition(ephys_ts_S1)

# Check the stored data
print(nwb.acquisition)


# Associate electrodes with units

nwb.add_unit_column('waveform_snippets', 'spike event waveform snippets')

# M1
for j in np.arange(96):
    
    nwb.add_unit(electrodes=[j],spike_times=np.ravel(f_info['spikes'][0:96,:][j,1]),electrode_group=electrode_group_M1,
                waveform_snippets=f_info['wf'][0:96,:][j,1])
    nwb.add_unit(electrodes=[j],spike_times=np.ravel(f_info['spikes'][0:96,:][j,2]),electrode_group=electrode_group_M1,
                waveform_snippets=f_info['wf'][0:96,:][j,2])

# S1
for j in np.arange(96):
    
    nwb.add_unit(electrodes=[j],spike_times=np.ravel(f_info['spikes'][96:192,:][j,1]),electrode_group=electrode_group_S1,
                waveform_snippets=f_info['wf'][96:192,:][j,1])
    nwb.add_unit(electrodes=[j],spike_times=np.ravel(f_info['spikes'][96:192,:][j,2]),electrode_group=electrode_group_S1,
                waveform_snippets=f_info['wf'][96:192,:][j,2])
