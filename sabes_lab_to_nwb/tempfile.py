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

path_to_files = 'C:/Users/Admin/Desktop/Ben Dichter/Sabes lab/datafiles'

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
electrode_group_M1 = ElectrodeGroup(name='ElectrodeArrayM1', description="96 Channels Electrode Array", 
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
electrode_group_S1 = ElectrodeGroup(name='ElectrodeArrayS1', description="96 Channels Electrode Array", 
                                    location="Somatosensory Cortex", 
                                    device=device_S1)

# Add metadata about each electrode in the group
for idx in np.arange(96):
    nwb.add_electrode(x=np.nan, y=np.nan, z=np.nan,
                      imp=np.nan,
                      location='S1', filtering='none',
                      group=electrode_group_S1)


#Store spike waveforms data in acquisition group


# M1

description = 'Spike event waveform "snippets" of M1. Each waveform corresponds to a timestamp in "spikes".'
comments = 'Waveform samples are in microvolts.'

# For each electrode i
for i in np.arange(96):
    
    # Create electrode table region for each electrode
    electrode_table_region_M1 = nwb.create_electrode_table_region([i], 'electrode i in array M1')
    
    # For each unit k
    for k in np.arange(3):
        
        data = f_info['wf'][i,k]
        timestamps = np.ravel(f_info['spikes'][i,k])
        
        # For units with no spike, the data array shape is saved as (48,0).
        # So, we transpose it
        if timestamps.shape==(0,):
            data = data.T
        
        # Create SpikeEventSeries container
        ephys_ts_M1 = SpikeEventSeries(name='M1 Spike Events electrode {0} and unit {1}'.format(i,k),
                                    data=data,
                                    timestamps=timestamps,
                                    electrodes=electrode_table_region_M1,
                                    resolution=4.096e-05,
                                    conversion=1e-6,
                                    description=description,
                                    comments=comments)
        
        # Store spike waveform data
        nwb.add_acquisition(ephys_ts_M1)


# S1

description = 'Spike event waveform "snippets" of S1. Each waveform corresponds to a timestamp in "spikes".'
comments = 'Waveform samples are in microvolts.'

# For each electrode i
for i in np.arange(96,192):
    
    # Create electrode table region for each electrode
    electrode_table_region_S1 = nwb.create_electrode_table_region([i], 'electrode i in array S1')
    
    # For each unit k
    for k in np.arange(3):
        
        data = f_info['wf'][i,k]
        timestamps = np.ravel(f_info['spikes'][i,k])
        
        # For units with no spike, the data array shape is saved as (48,0).
        # So, we transpose it
        if timestamps.shape==(0,):
            data = data.T
        
        # Create SpikeEventSeries container
        ephys_ts_S1 = SpikeEventSeries(name='S1 Spike Events electrode {0} and unit {1}'.format(i,k),
                                    data=data,
                                    timestamps=timestamps,
                                    electrodes=electrode_table_region_S1,
                                    resolution=4.096e-05,
                                    conversion=1e-6,
                                    description=description,
                                    comments=comments)
        
        # Store spike waveform data
        nwb.add_acquisition(ephys_ts_S1)


# Check the stored data
print(nwb.acquisition)


# Associate electrodes with units

# M1
for j in np.arange(96):
    nwb.add_unit(electrodes=[j],spike_times=np.ravel(f_info['spikes'][j,1]),electrode_group=electrode_group_M1)
    nwb.add_unit(electrodes=[j],spike_times=np.ravel(f_info['spikes'][j,2]),electrode_group=electrode_group_M1)

# S1
for j in np.arange(96,192):
    nwb.add_unit(electrodes=[j],spike_times=np.ravel(f_info['spikes'][j,1]),electrode_group=electrode_group_S1)
    nwb.add_unit(electrodes=[j],spike_times=np.ravel(f_info['spikes'][j,2]),electrode_group=electrode_group_S1)


# Save NWB to file:

fname_nwb = 'indy_20160407_02.nwb'
fpath_nwb = os.path.join(path_to_files, fname_nwb)
with NWBHDF5IO(fpath_nwb, mode='w') as io:
    io.write(nwb)
print('File saved with size: ', os.stat(fpath_nwb).st_size/1e6, ' mb')


# Load NWB:

io = NWBHDF5IO(fpath_nwb, mode='r')
nwbfile = io.read()
