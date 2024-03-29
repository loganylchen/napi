# AUTOGENERATED! DO NOT EDIT! File to edit: ../000_guppy.ipynb.

# %% auto 0
__all__ = ['GuppyCalledRead', 'get_signal_of_seq_loc']

# %% ../000_guppy.ipynb 2
import numpy as np


# %% ../000_guppy.ipynb 3
class GuppyCalledRead(object):
    '''
    GuppyCalledRead is a class that contains the following attributes:
    1. read: the fast5 read object
    2. basecall_analysis: the basecall analysis name
    3. segmentation_analysis: the segmentation analysis name
    4. group_id: the group id of the basecall analysis
    5. move_table: the move table of the basecall analysis
    6. segmentation_summary: the segmentation summary of the segmentation analysis
    7. basecall_summary: the basecall summary of the basecall analysis
    8. first_sample_template: the first sample template of the segmentation analysis
    9. block_stride: the block stride of the basecall analysis
    10. current_signal: the current signal of the read
    11. sequence_length: the sequence length of the read
    12. move_list: the move list of the read

    The following methods are available:
    1. loading_necessary(): load the necessary attributes of the read
    2. loading_base_possibility(): load the base possibility of the read
    3. loading_seq(): load the sequence of the read
    4. get_template_signal(): get the template signal of the read
    5. get_signal_of_seq_loc(start,end): get the signal of the seq loc

    Args:
        fast5_read: the fast5 read object
    '''
    def __init__(self, fast5_read,scale=True):
        self.read = fast5_read
        self.scale = scale
        self.loading_necessary()

    def loading_necessary(self):
        self.basecall_analysis = self.read.get_latest_analysis('Basecall_1D')
        self.segmentation_analysis = self.read.get_latest_analysis(
            'Segmentation')
        self.group_id = self.basecall_analysis.replace('Basecall_1D_', '')
        move_table = self.read.get_analysis_dataset(
            self.basecall_analysis, 'BaseCalled_template/Move')
        self.segmentation_summary = self.read.get_summary_data(self.segmentation_analysis)
        self.basecall_summary = self.read.get_summary_data(self.basecall_analysis)
        self.first_sample_template = self.segmentation_summary['segmentation']['first_sample_template']
        self.block_stride = self.basecall_summary['basecall_1d_template']['block_stride']
        self.current_signal = self.read.get_raw_data(scale=self.scale)[self.first_sample_template:].astype(np.double)
        self.sequence_length = self.basecall_summary['basecall_1d_template']['sequence_length']
        self._move_table_to_list(move_table)
    
    def _move_table_to_list(self,move_table):
        self.move_list = []
        index = -1
        move_table_list = move_table.tolist()
        while index < len(move_table):
            try:
                index = move_table_list.index(1, index+1)
                self.move_list.append(index*self.block_stride)
            except ValueError:
                self.move_list.append(move_table.shape[0]*self.block_stride)
                break

    def loading_base_possibility(self):
        self.trace_table = self.read.get_analysis_dataset(
            self.basecall_analysis, 'BaseCalled_template/Trace')
        # The Trace order is: A, C, G, U, A', C', G', U'.
        # The flip possibility is the first 4 columns, the flop possibility is the last 4 columns.
        def _overlap_sum(alist, number):
            return alist[0:number]+alist[number:2*number]
        base_pos = []
        for i in self.trace_table:
            base_pos.append(np.array(_overlap_sum(i/i.sum(), 4)))
        self.base_possibility = np.array(base_pos).repeat(self.block_stride, axis=0)
    
    def loading_seq(self):
        _, self.seq, _, self.qual, _ = self.read.get_analysis_dataset(
            self.basecall_analysis, 'BaseCalled_template/Fastq').split('\n')

    def get_template_signal(self):
        return self.current_signal

    def get_signal_of_seq_loc(self,start,end):
        # TODO: how to using move table and current signal to get the signal of the seq
        _move_start = self.sequence_length-end-1 
        _move_end = self.sequence_length-start 
        return self.current_signal[self.move_list[_move_start]:self.move_list[_move_end]]

    def return_data(self):
        return self.current_signal,self.move_list,self.sequence_length

    def __repr__(self):
        return f'GuppyCalledRead: {self.read.get_read_id()}'


        


# %% ../000_guppy.ipynb 4
def get_signal_of_seq_loc(current_signal,move_list,sequence_length,start,end):
    _move_start = sequence_length-end-1 
    _move_end = sequence_length-start 
    return current_signal[move_list[_move_start]:move_list[_move_end]]  

