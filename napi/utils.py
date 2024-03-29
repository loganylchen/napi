# AUTOGENERATED! DO NOT EDIT! File to edit: ../001_utils.ipynb.

# %% auto 0
__all__ = ['FORMAT', 'log', 'REGION_SIZE', 'loading_signal', 'retrieve_signal_by_loc']

# %% ../001_utils.ipynb 2
from ont_fast5_api.fast5_interface import get_fast5_file
import numpy as np

import logging
from rich.logging import RichHandler


# %% ../001_utils.ipynb 3
from .worker import process_worker
from .guppy import GuppyCalledRead, get_signal_of_seq_loc

# %% ../001_utils.ipynb 4
FORMAT = "|%(message)s"
logging.basicConfig(
    level=logging.WARNING, format=FORMAT, datefmt="[%Y-%m-%d,%X]", handlers=[RichHandler(rich_tracebacks=True)]
)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


# %% ../001_utils.ipynb 5
REGION_SIZE =5 

# %% ../001_utils.ipynb 6
def _remove_extremism_normalization(signal):
    return np.array(signal[(0<signal)&(signal<200)],dtype=np.double)

# %% ../001_utils.ipynb 7
def _load_signal(params):
    log.debug(f'loading signal for {params["read_id"]}')
    fast5_file = params['fast5_file']
    read_id = params['read_id']
    with get_fast5_file(f'{fast5_file}') as fast5:
        return read_id, GuppyCalledRead(fast5.get_read(read_id)).return_data()


# %% ../001_utils.ipynb 8
def loading_signal(read_list,fast5_dir,fast5_df,thread=2):
    target_reads_df = fast5_df.loc[fast5_df['read_id'].isin(read_list),:]
    fast5_files = target_reads_df['filename'].unique()
    params_list = []
    for fast5_file in fast5_files:
        for read_id in list(target_reads_df.loc[target_reads_df['filename'] == fast5_file,'read_id']):
            params_list.append({
                'fast5_file': f'{fast5_dir}/{fast5_file}', 'read_id': read_id})
    tmp_loading = process_worker(_load_signal,params_list,thread,desc='loading signal')
    target_signals = {}
    for i,j in tmp_loading:
        target_signals[i]=j
    return target_signals

# %% ../001_utils.ipynb 9
def retrieve_signal_by_loc(signals_d,locs_d):
    loc_signal_d = dict()
    for read_id in signals_d:
        if read_id in locs_d:
            log.debug(f'Retrieving locus signal of {read_id}')
            loc_signal_d[read_id] = _remove_extremism_normalization(get_signal_of_seq_loc(
                *signals_d[read_id], locs_d[read_id]-REGION_SIZE, locs_d[read_id]+REGION_SIZE))
    log.debug(f'loc_signal_d: {len(loc_signal_d)}, signals_d: {len(signals_d)}, locs_d: {len(locs_d)}')
    return loc_signal_d

