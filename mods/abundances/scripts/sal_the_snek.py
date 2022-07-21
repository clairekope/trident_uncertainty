import salsa
from salsa.utils import check_rays
import trident
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
parser.add_argument('--halo_dir', action='store', dest='halo_dir', default='/mnt/research/galaxies-REU/sims/FOGGIE', help='Path to halo data.')
parser.add_argument('--pat', action='store', dest='pattern', default=2392, type=int, help='Halo pattern file ID')
parser.add_argument('--rshift', action='store', dest='rs', default=20, type=int, help='Redshift file IDs')
parser.add_argument('--it', nargs='?', action='store', dest='itable', default = None, help='Path to custom ionization table. If left blank, trident defaults to whatever ionization table it is currently using' )

args = parser.parse_args()
dic_args = vars(args)

def get_true_rs(val): ##define how to get actual rshift numbers
    if val == 20:
        true_rs = '2.0'
    elif val == 18:
        true_rs = '2.5'
    return true_rs

halo_names_dict = {'2392'  :  'Hurricane' ,'2878'  :  'Cyclone' , '4123'  :  'Blizzard' , '5016'  :  'Squall' ,'5036'  :  'Maelstrom' , '8508'  :  'Tempest'}

def get_halo_names(num):
    if str(num) in halo_names_dict.keys():
        halo_name = halo_names_dict[str(num)]
    return halo_name

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

# defining analysis parameters
# Note: these dictionaries are temporary and should most likely be included in the arguments at some point

# EDIT THIS LINE TO LOCAL FOGGIE LOCATION

foggie_dir = "/mnt/home/tairaeli/astro_libs/foggie/foggie/halo_infos"

# set desired halo pattern
halo = args.pattern

# set redshift info
rshift = args.rs
true_rs = get_true_rs(rshift)
# takes in the foggie halo info directory
# outputs a dictionary of galactic center locations/velocities for all redshifts in each halo pattern
# NOTE: this function is temporary and has some hard-coded variables that will need to be changed
def foggie_defunker(foggie_dir):
    # initializing dictionary to store all of the galactic center data
    center_dat = {}

    # some hardcoded pipelies that will need to be changed
    cen_dat = pd.read_csv(f"/mnt/home/tairaeli/astro_libs/foggie/foggie/halo_infos/00{halo}/nref11c_nref9f/halo_c_v", sep = '|', names = ['null','redshift','name','xc','yc','zc','xv','yv','zv','null2'])
    
    # making some fixes specific to these files
    cen_dat = cen_dat.drop(0)
    cen_dat = cen_dat.drop(columns = ['null','null2'])
    
    # isolating data to a specific redshift 
    rs_dat = cen_dat[cen_dat['name'] == ' RD00'+str(rshift)+' ']
    
    # making 2 branches to store the position and velocity data of the galactic center
    center_dat['pos'] = [float(rs_dat["xc"]),float(rs_dat["yc"]),float(rs_dat["zc"])]
    center_dat['vel'] = [float(rs_dat["xv"]),float(rs_dat["yv"]),float(rs_dat["zv"])]
     
    return center_dat

# fetching the galactic center data for all halo patterns and redshifts
center_dat = foggie_defunker(foggie_dir)

# identifying the path argument as a variable
path = os.path.expandvars(os.path.expanduser(args.path))

# creating variable names for data bin locations
halo_path = path+'/halo'+f'{halo}'
rs_path = halo_path + '/redshift'+f'{true_rs}'
ray_path = rs_path +'/rays'
dat_path = rs_path +'/data'
vis_path = rs_path +'/visuals'

# creating dictionaries to store all of our data (if they don't already exist)
if os.path.exists(halo_path) == False:
    os.mkdir(path+'/halo'+f'{halo}')
    
if os.path.exists(rs_path) == False:
    os.mkdir(ray_path) 
    os.mkdir(dat_path)
    os.mkdir(vis_path)

# load halo data
ds = yt.load(f'{args.halo_dir}/halo_00{halo}/nref11c_nref9f/RD00{rshift}/RD00{rshift}')

ion_list = ['C II', 'C IV', 'O VI']

trident.ion_balance.add_ion_fields(ds, ions = ion_list, ionization_table = args.itable)
# defining analysis parameters
# Note: these dictionaries are temporary and should most likely be included in the arguments at some point
center = ds.arr(center_dat['pos'], 'kpc')
gal_vel = ds.arr(center_dat['vel'], 'km/s')
other_fields=['density', 'temperature', 'metallicity']
max_impact=15 #kpc
units_dict = dict(density='g/cm**3', metallicity='Zsun')

ray_num=f'{0:0{len(str(args.nrays))}d}'
ray_file=f'{ray_path}/ray{ray_num}.h5'

np.random.seed(11)

#get those rays babyyyy
# CK: Check that rays already exist, and that the have the additional fields contained
# in the third argument (empty for now; might become a user parameter)
check = check_rays(ray_path, args.nrays, [])
if not check:
    print("WARNING: rays not found. Generating new ones.")
    salsa.generate_lrays(ds, center.to('code_length'), args.nrays, max_impact, length=600, field_parameters={'bulk_velocity':gal_vel}, ion_list=['H I'], fields=other_fields, out_dir=ray_path)

ray_list=[]
for i in range(args.nrays):
    if len(str(i)) != len(str(args.nrays)):
        n = len(str(args.nrays)) - 1
    
        ray_list.append(f'{ray_path}/ray{i: 0{n}d}.h5')
    else:
        ray_list.append(f'{ray_path}/ray{i}.h5')
    
    # CK: Taking a hint from SALSA on how to divvy up the ray list across procs
    ray_arr = np.array(ray_list)
    ray_files_split = np.array_split(ray_arr, comm.size)
    my_rays = ray_files_split[ comm.rank ]
    
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
                        df.to_csv(f'{dat_path}/{saved[row_num]}_{i.replace(" ", "_")}.txt', sep = ' ')
                        print("Go look at your data!")
    
    else:
        nrows = 0
        saved = generate_names(nrows)
        for i in ion_list:
                abs_ext = salsa.AbsorberExtractor(ds, ray_file, ion_name = i, abundance_table = None, calc_missing=True)
                df = salsa.get_absorbers(abs_ext, my_rays, method='spice', fields=other_fields, units_dict=units_dict)
                df.to_csv(f'{dat_path}/data_SolAb_{i.replace(" ", "_")}.txt', sep = ' ')
                print("Go look at your data!")
