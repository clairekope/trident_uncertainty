import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import pandas as pd
import numpy as np

halo_marker_dict = {'2392' : 'o', '4123' : 'x', '5016' : 'v', '5036' : '*', '8508' : 'D'} ##set which marker I want for each halo
halo_names_dict = {'2392'  :  'Hurricane' ,'2878'  :  'Cyclone' , '4123'  :  'Blizzard' , '5016'  :  'Squall' ,'5036'  :  'Maelstrom' , '8508'  :  'Tempest'} ##set FOGGIE names

def get_halo_names(num): ##get the FOGGIE name for each halo ID 
    if str(num) in halo_names_dict.keys():
        halo_name = halo_names_dict[str(num)]
    return halo_name


rs_lis = [2.0, 2.5] ##list of rs to analyze, true


ion_dict = {'C_I' : 'silver', 'C_II' : 'darkgrey', 'C_III' : 'grey', 'C_IV' : 'dimgrey', 'Si_I' : 'bisque', 'Si_II' : 'navajowhite', 'Si_III' : 'blanchedalmond', 'Si_IV' : 'moccasin', 'Fe_I' : 'salmon', 'Fe_II' : 'tomato', 'Fe_III' : 'maroon', 'N_I' : 'limegreen', 'N_II' : 'forestgreen', 'N_III' :'olivedrab' , 'N_IV' :'seagreen' , 'N_V' : 'green' , 'O_I' : 'cornflowerblue', 'O_II' : 'royalblue', 'O_III' :'blue', 'O_IV' : 'mediumblue', 'O_V' : 'darkblue', 'O_VI' : 'navy', 'Mg_I' : 'aqua', 'Mg_II' : 'cyan', 'S_I' : 'cornsilk', 'S_II' : 'lemonchiffon', 'S_III' : 'khaki', 'S_IV' : 'gold', 'S_V' : 'goldenrod', 'S_VI' : 'darkgoldenrod'} ##dictionary of ions to colors

##set the legends to be the way I want them
legend_elements = [Line2D([0], [0], lw= 0, color = 'k', marker = 'o', label = 'Hurricane'), Line2D([0], [0],  lw= 0, color = 'k', marker = 'x', label = 'Cyclone'), Line2D([0], [0],  lw= 0, color = 'k', marker = 'v', label = 'Squall'), Line2D([0], [0], lw= 0, color = 'k', marker = '*', label = 'Maelstrom'), Line2D([0], [0], lw= 0, color = 'k', marker = 'D', label = 'Tempest')]

for ion in ion_dict.keys():
    legend_patch = Patch(fc = ion_dict[ion], label = ion)
    legend_elements.append(legend_patch)

for rs in rs_lis: ##we want one graph per redshift
    for halo in halo_marker_dict.keys(): ##all the halos
        name = get_halo_names(halo)
        for ion in ion_dict.keys(): ##all the ions
            try:
                ds = pd.read_csv(f'/mnt/gs18/scratch/users/f0104093/cgm_abundance_variance/halo{halo}/redshift{rs}/stats/{halo}_z{rs}_{ion}_abun_all-model-families_all-clumps.csv', delim_whitespace = True)
                if len(ds['density']) != 0: ##only use data where there actually is something
                    med_col_dens = ds["median_col_desnity"] ##plot the spread of the median vs the median col dens
                    col_dens_spread = ds["mad_for_col_desnity"]
                    plt.scatter(med_col_dens, col_dens_spread, c = ion_dict[ion], marker = halo_marker_dict[halo])
                    print('plotted!')
                else:
                    print(f'No {ion} in halo {halo} z{rs}')
            except FileNotFoundError: ##handles if ion was not done for some reason
                print(f'This halo, {halo_names_dict[halo]}, had something wierd going on')
                continue
      
    plt.title(f"MAD of Column Density vs Column Density, Redshift {rs}") 
    plt.legend(handles = legend_elements, ncol = 3, bbox_to_anchor=(1,0), loc="lower left")
    plt.xlabel("Median log(Column Density)")
    plt.ylabel("MAD of log(Column Density)")
    plt.savefig(f'/mnt/gs18/scratch/users/f0104093/cgm_abundance_variance/graphs/mad_vs_med_z{rs}.png', bbox_inches='tight') ##make sure it saves to the right place with the right name
    plt.close() ##so the rest doesn't plot on top of this data
    ##a simmilar process is used for the rest of these plots, simply with different quantities
    
    for halo in halo_marker_dict.keys():
        name = get_halo_names(halo)
        for ion in ion_dict.keys():
            try:
                ds = pd.read_csv(f'/mnt/gs18/scratch/users/f0104093/cgm_abundance_variance/halo{halo}/redshift{rs}/stats/{halo}_z{rs}_{ion}_abun_all-model-families_all-clumps.csv', delim_whitespace = True)
                if len(ds['density']) != 0:
                    med_col_dens = ds["median_col_desnity"] ##density and median column density
                    dens = ds["density"]
                    plt.scatter(med_col_dens, dens, c = ion_dict[ion], marker = halo_marker_dict[halo])
                    print('plotted!')
                else:
                    print(f'No {ion} in halo {halo} z{rs}')
            except FileNotFoundError:
                print(f'This halo, {halo_names_dict[halo]}, had something wierd going on')
                continue
      
    plt.title(f"Density vs Column Density, Redshift {rs}")
    plt.yscale('log') ##has to be plotted on a log scale
    plt.legend(handles = legend_elements, ncol = 3, bbox_to_anchor=(1,0), loc="lower left")
    plt.xlabel("Median log(Column Density)")
    plt.ylabel("log(Density)")
    plt.savefig(f'/mnt/gs18/scratch/users/f0104093/cgm_abundance_variance/graphs/dens_vs_med_z{rs}.png', bbox_inches='tight')
    plt.close()
    
    for halo in halo_marker_dict.keys():
        name = get_halo_names(halo)
        for ion in ion_dict.keys():
            try:
                ds = pd.read_csv(f'/mnt/gs18/scratch/users/f0104093/cgm_abundance_variance/halo{halo}/redshift{rs}/stats/{halo}_z{rs}_{ion}_abun_all-model-families_all-clumps.csv', delim_whitespace = True)
                if len(ds['density']) != 0:
                    med_col_dens = ds["median_col_desnity"] ##temperature and median column density
                    temp = ds["temperature"]
                    plt.scatter(med_col_dens, temp, c = ion_dict[ion], marker = halo_marker_dict[halo])
                    print('plotted!')
                else:
                    print(f'No {ion} in halo {halo} z{rs}')
            except FileNotFoundError:
                print(f'This halo, {halo_names_dict[halo]}, had something wierd going on')
                continue
      
    plt.title(f"Temperature vs Column Density, Redshift {rs}")
    plt.yscale('log') 
    plt.legend(handles = legend_elements, ncol = 3, bbox_to_anchor=(1,0), loc="lower left")
    plt.xlabel("Median log(Column Density)")
    plt.ylabel("log(Temperature)")
    plt.savefig(f'/mnt/gs18/scratch/users/f0104093/cgm_abundance_variance/graphs/temp_vs_med_z{rs}.png', bbox_inches='tight')
    plt.close()
    
    for halo in halo_marker_dict.keys():
        name = get_halo_names(halo)
        for ion in ion_dict.keys():
            try:
                ds = pd.read_csv(f'/mnt/gs18/scratch/users/f0104093/cgm_abundance_variance/halo{halo}/redshift{rs}/stats/{halo}_z{rs}_{ion}_abun_all-model-families_all-clumps.csv', delim_whitespace = True)
                if len(ds['density']) != 0:
                    med_col_dens = ds["median_col_desnity"] ##distance from galaxy vs median col dens
                    dist = ds["distance_from_galaxy"]
                    plt.scatter(med_col_dens, dist, c = ion_dict[ion], marker = halo_marker_dict[halo])
                    print('plotted!')
                else:
                    print(f'No {ion} in halo {halo} z{rs}')
            except FileNotFoundError:
                print(f'This halo, {halo_names_dict[halo]}, had something wierd going on')
                continue
      
    plt.title(f"Distance vs Column Density, Redshift {rs}")
    plt.legend(handles = legend_elements, ncol = 3, bbox_to_anchor=(1,0), loc="lower left")
    plt.xlabel("Median log(Column Density)")
    plt.ylabel("Distance from Galaxy")
    plt.savefig(f'/mnt/gs18/scratch/users/f0104093/cgm_abundance_variance/graphs/dist_vs_med_z{rs}.png', bbox_inches='tight')
    plt.close()

    for halo in halo_marker_dict.keys():
        name = get_halo_names(halo)
        for ion in ion_dict.keys():
            try:
                ds = pd.read_csv(f'/mnt/gs18/scratch/users/f0104093/cgm_abundance_variance/halo{halo}/redshift{rs}/stats/{halo}_z{rs}_{ion}_abun_all-model-families_all-clumps.csv', delim_whitespace = True)
                if len(ds['density']) != 0:
                    col_dens_spread = ds["mad_for_col_desnity"] ##MAD of col dens vs density
                    dens = ds["density"]
                    plt.scatter(dens, col_dens_spread, c = ion_dict[ion], marker = halo_marker_dict[halo])
                    print('plotted!')
                else:
                    print(f'No {ion} in halo {halo} z{rs}')
            except FileNotFoundError:
                print(f'This halo, {halo_names_dict[halo]}, had something wierd going on')
                continue
      
    plt.title(f"Density vs Spread of Column Density , Redshift {rs}")
    plt.xscale('log')
    plt.legend(handles = legend_elements, ncol = 3, bbox_to_anchor=(1,0), loc="lower left")
    plt.ylabel("MAD of Median log(Column Density)")
    plt.xlabel("log(Density)")
    plt.savefig(f'/mnt/gs18/scratch/users/f0104093/cgm_abundance_variance/graphs/dens_vs_mad_z{rs}.png', bbox_inches='tight')
    plt.close()
    
    for halo in halo_marker_dict.keys():
        name = get_halo_names(halo)
        for ion in ion_dict.keys():
            try:
                ds = pd.read_csv(f'/mnt/gs18/scratch/users/f0104093/cgm_abundance_variance/halo{halo}/redshift{rs}/stats/{halo}_z{rs}_{ion}_abun_all-model-families_all-clumps.csv', delim_whitespace = True)
                if len(ds['density']) != 0:
                    col_dens_spread = ds["mad_for_col_desnity"] ##MAD of col dons vs temperature
                    temp = ds["temperature"]
                    plt.scatter(temp, col_dens_spread, c = ion_dict[ion], marker = halo_marker_dict[halo])
                    print('plotted!')
                else:
                    print(f'No {ion} in halo {halo} z{rs}')
            except FileNotFoundError:
                print(f'This halo, {halo_names_dict[halo]}, had something wierd going on')
                continue
      
    plt.title(f"Temperature vs Spread of Column Density, Redshift {rs}")
    plt.xscale('log')
    plt.legend(handles = legend_elements, ncol = 3, bbox_to_anchor=(1,0), loc="lower left")
    plt.ylabel("MAD of Median log(Column Density)")
    plt.xlabel("log(Temperature)")
    plt.savefig(f'/mnt/gs18/scratch/users/f0104093/cgm_abundance_variance/graphs/temp_vs_mad_z{rs}.png', bbox_inches='tight')
    plt.close()
    
    for halo in halo_marker_dict.keys():
        name = get_halo_names(halo)
        for ion in ion_dict.keys():
            try:
                ds = pd.read_csv(f'/mnt/gs18/scratch/users/f0104093/cgm_abundance_variance/halo{halo}/redshift{rs}/stats/{halo}_z{rs}_{ion}_abun_all-model-families_all-clumps.csv', delim_whitespace = True)
                if len(ds['density']) != 0:
                    col_dens_spread = ds["mad_for_col_desnity"] ##MAD of col dens vs distance from galaxy
                    dist = ds["distance_from_galaxy"]
                    plt.scatter(dist, col_dens_spread, c = ion_dict[ion], marker = halo_marker_dict[halo])
                    print('plotted!')
                else:
                    print(f'No {ion} in halo {halo} z{rs}')
            except FileNotFoundError:
                print(f'This halo, {halo_names_dict[halo]}, had something wierd going on')
                continue
      
    plt.title(f"Distance vs Spread of Column Density, Redshift {rs}")
    plt.legend(handles = legend_elements, ncol = 3, bbox_to_anchor=(1,0), loc="lower left")
    plt.ylabel("MAD of Median log(Column Density)")
    plt.xlabel("Distance from Galaxy")
    plt.savefig(f'/mnt/gs18/scratch/users/f0104093/cgm_abundance_variance/graphs/dist_vs_mad_z{rs}.png', bbox_inches='tight')
    plt.close()
    
    for halo in halo_marker_dict.keys():
        name = get_halo_names(halo)
        for ion in ion_dict.keys():
            try:
                ds = pd.read_csv(f'/mnt/gs18/scratch/users/f0104093/cgm_abundance_variance/halo{halo}/redshift{rs}/stats/{halo}_z{rs}_{ion}_abun_all-model-families_all-clumps.csv', delim_whitespace = True)
                if len(ds['density']) != 0:
                    med_col_dens = ds["median_col_desnity"] ##median col dens vs frequency of clumps splitting or getting shorter
                    num_spl_sho = ds["num_split_or_short"]
                    plt.scatter(med_col_dens, num_spl_sho, c = ion_dict[ion], marker = halo_marker_dict[halo])
                    print('plotted!')
                else:
                    print(f'No {ion} in halo {halo} z{rs}')
            except FileNotFoundError:
                print(f'This halo, {halo_names_dict[halo]}, had something wierd going on')
                continue
      
    plt.title(f"Frequency of Split or Short Clumps vs Column Density, Redshift {rs}")
    plt.legend(handles = legend_elements, ncol = 3, bbox_to_anchor=(1,0), loc="lower left")
    plt.xlabel("Median log(Column Density)")
    plt.ylabel("Number of Split or Short Clumps")
    plt.savefig(f'/mnt/gs18/scratch/users/f0104093/cgm_abundance_variance/graphs/freq_vs_med_z{rs}.png', bbox_inches='tight')
    plt.close()
    
    for halo in halo_marker_dict.keys():
        name = get_halo_names(halo)
        for ion in ion_dict.keys():
            try:
                ds = pd.read_csv(f'/mnt/gs18/scratch/users/f0104093/cgm_abundance_variance/halo{halo}/redshift{rs}/stats/{halo}_z{rs}_{ion}_abun_all-model-families_all-clumps.csv', delim_whitespace = True)
                if len(ds['density']) != 0:
                    elem_mad = ds["mad_of_element"] ##MAD of elemental abundance vs MAD of the col dens
                    col_dens_spread = ds["mad_for_col_desnity"]
                    plt.scatter(elem_mad,col_dens_spread, c = ion_dict[ion], marker = halo_marker_dict[halo])
                    print('plotted!')
                else:
                    print(f'No {ion} in halo {halo} z{rs}')
            except FileNotFoundError:
                print(f'This halo, {halo_names_dict[halo]}, had something wierd going on')
                continue
      
    plt.title(f"MAD of Elemental Abundance vs MAD of Column Density, Redshift {rs}")
    plt.xscale('log')
    plt.legend(handles = legend_elements, ncol = 3, bbox_to_anchor=(1,0), loc="lower left")
    plt.xlabel("log(MAD of Elemental Abundance)")
    plt.ylabel("MAD of log(Column Density)")
    plt.savefig(f'/mnt/gs18/scratch/users/f0104093/cgm_abundance_variance/graphs/mad_vs_elem_mad_z{rs}.png', bbox_inches='tight')
    plt.close()
    
    ##this one is different because it's a histogram and not a scatter plot
    diff_list = [] ##initalize list to be put into a histogram
    for halo in halo_marker_dict.keys():
        name = get_halo_names(halo)
        for ion in ion_dict.keys():
            try:
                ds = pd.read_csv(f'/mnt/gs18/scratch/users/f0104093/cgm_abundance_variance/halo{halo}/redshift{rs}/stats/{halo}_z{rs}_{ion}_abun_all-model-families_all-clumps.csv', delim_whitespace = True)
                if len(ds['density']) != 0:
                    diff = ds["diff_from_solar_abun"] ##get the data from data tables
                    for value in diff:
                        if value != 'NaN' and value != np.NaN: ##filter out the NaNs
                            diff_list.append(value) ##make the list of values
                else:
                    print(f'No {ion} in halo {halo} z{rs}')
            except FileNotFoundError:
                print(f'This halo, {halo_names_dict[halo]}, had something wierd going on')
                continue
                    
      
    plt.hist(diff_list, bins = 5) ##make the histogram
    plt.title(f"Diffrence between Solar Abundance and Median Column Density, Redshift {rs}") ##needs a better title but I can't think of one right now
    plt.ylabel("frequency")
    plt.xlabel("dex of the difference between Solar Abundance Column Density and Median Column Density") ##has to be in dex(order of magnitude) because of how sal the super snake works
    plt.savefig(f'/mnt/gs18/scratch/users/f0104093/cgm_abundance_variance/graphs/solar_diff_z{rs}.png', bbox_inches='tight')
    plt.close()

print('All done!')
