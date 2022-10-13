import numpy as np
import matplotlib.pyplot as plt

atomic_number = {
    'H' : 1,  'He': 2,  'Li': 3,
    'Be': 4,  'B' : 5,  'C' : 6,
    'N' : 7,  'O' : 8,  'F' : 9,
    'Ne': 10, 'Na': 11, 'Mg': 12,
    'Al': 13, 'Si': 14, 'P' : 15,
    'S' : 16, 'Cl': 17, 'Ar': 18,
    'K' : 19, 'Ca': 20, 'Sc': 21,
    'Ti': 22, 'V' : 23, 'Cr': 24,
    'Mn': 25, 'Fe': 26, 'Co': 27,
    'Ni': 28, 'Cu': 29, 'Zn': 30}

atomic_symb = {v:k for k,v in atomic_number.items()}

solar_abundance = np.array([1.00e+00, 1.00e-01, 2.04e-09,
    2.63e-11, 6.17e-10, 2.45e-04,
    8.51e-05, 4.90e-04, 3.02e-08,
    1.00e-04, 2.14e-06, 3.47e-05,
    2.95e-06, 3.47e-05, 3.20e-07,
    1.84e-05, 1.91e-07, 2.51e-06,
    1.32e-07, 2.29e-06, 1.48e-09,
    1.05e-07, 1.00e-08, 4.68e-07,
    2.88e-07, 2.82e-05, 8.32e-08,
    1.78e-06, 1.62e-08, 3.98e-08])

abuns = np.genfromtxt("abundances_AGB_massive_yields_halo8508_z2.0.txt", skip_header=1)

abuns -= solar_abundance
abuns /= solar_abundance

abuns = abuns[:,:26]

x = np.arange(1,27)

fig, ax = plt.subplots(figsize=(8,5))

ax.axhline(0, color='gray', ls='--')

#ax.plot(solar_abundance, color="black")
# C15 LC18 (1)
ax.plot(x, abuns[1], color="olive", label="C15 L18 Ravg") # assuming mix = avg
# C15 N13 (3)
ax.plot(x, abuns[2], color="darkred", label="C15 N13 0.0-HNe")
ax.plot(x, abuns[3], color="firebrick", label="C15 N13 0.5-HNe")
ax.plot(x, abuns[4], color="indianred", label="C15 N13 1.0-HNe")
# K10 K06 (3)
ax.plot(x, abuns[5], color="darkturquoise", label="K10 K06 0.0-HNe")
ax.plot(x, abuns[6], color="c", label="K10 K06 0.5-HNe")
ax.plot(x, abuns[7], color="teal", label="K10 K06 1.0-HNe")
# K10 LC18 (4)
ax.plot(x, abuns[8], color="peru", label="K10 LC18 R000") # set R; 0 km/s
ax.plot(x, abuns[9], color="chocolate", label="K10 LC18 R150")
ax.plot(x, abuns[10], color="sienna", label="K10 LC18 R300")
ax.plot(x, abuns[11], color="saddlebrown", label="K10 LC18 Ravg")
# nugrid MESA (5)
ax.plot(x, abuns[15], color="mediumorchid", label="NuGrid delay")
ax.plot(x, abuns[16], color="darkviolet", label="NuGrid delay-wind")
ax.plot(x, abuns[17], color="blueviolet", label="NuGrid mix")
ax.plot(x, abuns[18], color="rebeccapurple", label="NuGrid rapid")
ax.plot(x, abuns[19], color="indigo", label="NuGrid Ye") # ritter et al "in prep"
# nugrid other (4)
ax.plot(x, abuns[13], color="cornflowerblue", label="NuGrid K06")
ax.plot(x, abuns[20], color="royalblue", label="NuGrid N13")
ax.plot(x, abuns[12], color="darkgreen", label="C15 NuGrid delay")
ax.plot(x, abuns[14], color="forestgreen", label="K10 NuGrid delay")

ax.set_ylim(-2,60)
ax.set_xlim(0.5,26.5)

ax.set_ylabel("Relative Difference from Solar", fontsize='large')
ax.set_xlabel("Element", fontsize='large')

labs = x #[1,5,10,15,20,25,30]
ax.set_xticks(labs[:26])
ax.set_xticklabels([atomic_symb[i] for i in labs[:26]])

ax.legend(ncol=2)
fig.tight_layout()
fig.savefig("abundances_AGB_massive_halo8508_z2.0.pdf")
