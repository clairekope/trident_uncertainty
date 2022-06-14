# from sal_the_snake import *
import salsa
from salsa.utils import check_rays
import numpy as np
import pandas as pd
import argparse
import sys
import os
import matplotlib.pyplot as plt
import yt  
from mpi4py import MPI

comm = MPI.COMM_WORLD

print(f"Let's do some math, kids")

parser = argparse.ArgumentParser(description = "Preliminary constants for SALSA pipeline.")
parser.add_argument('--ds', nargs='?', action='store', required=True, dest='path', help='Path where rays and output data will be stored. Directory should contain three other directories called "data", "rays", and "visuals" for program to run smoothly.')
parser.add_argument('--nrays', action='store', dest='nrays', default=4, type=int, help='The number of rays to be generated.')
parser.add_argument('--abun', action='store', dest='file_path', default=argparse.SUPPRESS, help='Path to abundance file, if any. Defaults to solar abundances.')
parser.add_argument('--halo', action='store', dest='ds_file', default='/mnt/research/galaxies-REU/sims/FOGGIE/halo_002392/nref11c_nref9f/RD0020/RD0020', help='Path to halo data.')

args = parser.parse_args()
dic_args = vars(args)

path = os.path.expandvars(os.path.expanduser(args.path))
if not os.path.exists(path+"/data"):
	print(f"PULL YOUT SHIT TOGETHER. MAKING THE DIRECTORIES YOU SHOULD HAVE ALREADY MADE")
	# os.makedirs(path)
	os.mkdir(path+"/data")
	os.mkdir(path+"/rays")

def generate_names(length, add=''):

	"""
	Returns a list of generic names for multiplots anda list of generic names for raw data. These lists are typically passed to run_sal()
	
	:length: length of lists to be generated. Do not account for indexing starting at zero.
	
	:add: Additional relevant information for keeping track of multiplots and data later on. Default add=''
	"""
	ndigits = len(str(length))
	saved_filename_list = []
	
	for i in range(length): ##made this so that it would sort correctly for making plots
		m= i+1
		n_len = len(str(m))
		n_zeros = ndigits - n_len
		k = "0" * n_zeros + str(m)
		saved_filename_list.append(f'data_AbundanceRow{k}{add}')
		
	return saved_filename_list

#preliminary shenanigans -- load halo data; define handy variables; plant the seed, as it were
ds = yt.load(args.ds_file)
center = ds.arr([23876.757358761424, 23842.452527236022, 22995.717805638298], 'kpc')
gal_vel = ds.arr([-0.02410298432958413, -136.9259851493111, -147.88486721075668], 'km/s')
other_fields=['density', 'temperature', 'metallicity', 'radius']
max_impact=15 #kpc
units_dict = dict(density='g/cm**3', metallicity='Zsun')

ray_num = f'{0:0{len(str(args.nrays))}d}'
ray_file=f'{path}/rays/ray{ray_num}.h5'

np.random.seed(11)

#get those rays babyyyy

# CK: Check that rays already exist, and that the have the additional fields contained
# in the third argument (empty for now; might become a user parameter)
check = check_rays(path+"/rays", args.nrays, [])
if not check:
    print("WARNING: rays not found. Generating new ones.")
    salsa.generate_lrays(ds, center.to('code_length'), args.nrays, max_impact, length=600, field_parameters={'bulk_velocity', gal_vel}, ion_list=['H I'], fields=other_fields, out_dir=(path + "/rays"))

ray_list=[]
for i in range(args.nrays):
    if len(str(i)) != len(str(args.nrays)):
        n = len(str(args.nrays)) - 1
        
        ray_list.append(f'{path}/rays/ray{i: 0{n}d}.h5')
    else:
        ray_list.append(f'{path}/rays/ray{i}.h5')

# CK: Taking a hint from SALSA on how to divvy up the ray list across procs
ray_arr = np.array(ray_list)
ray_files_split = np.array_split(ray_arr, comm.size)
my_rays = ray_files_split[ comm.rank ]

ion_list = ['C II', 'C IV', 'O VI']

# if 'use_SolAb' == False:
if 'file_path' in dic_args:
	abun = pd.read_csv(args.file_path, delim_whitespace=True)
	nrows = len(abun)
	saved = generate_names(nrows)
	for row_num in range(nrows):
		for i in ion_list:
			abundances = abun.iloc[row_num].to_dict()
			abs_ext = salsa.AbsorberExtractor(ds, ray_file, ion_name = i, velocity_res =20, abundance_table = abundances, calc_missing=True)
			df = salsa.get_absorbers(abs_ext, my_rays, method='spice', fields=other_fields, units_dict=units_dict)
			df.to_csv(f'{args.path}/data/{saved[row_num]}_{i.replace(" ", "_")}.txt', sep = ' ')
			print("Go look at your data!")

else:
	nrows = 0
	saved = generate_names(nrows)
	for i in ion_list:
		abs_ext = salsa.AbsorberExtractor(ds, ray_file, ion_name = i, abundance_table = None, calc_missing=True)
		df = salsa.get_absorbers(abs_ext, my_rays, method='spice', fields=other_fields, units_dict=units_dict)
		df.to_csv(f'{args.path}/data/data_SolAb_{i.replace(" ", "_")}.txt', sep = ' ')
		print("Go look at your data!")