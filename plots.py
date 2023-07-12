#!/usr/bin/env python

# Import Required Packages
# ========================
import os, sys
import pickle
import time

import matplotlib.pyplot as plt
import seaborn as sns
sns.set(font_scale=1.2)
# Import the solvers
import solvers

########################################################################
import argparse
parser = argparse.ArgumentParser(description="parameter settings")
parser.add_argument("--weight",type=float,default=0.25)
parser.add_argument("--xi",type=float,default=0.01)
parser.add_argument("--pf",type=float,default=20.76)
parser.add_argument("--pa",type=float,default=44.75)
parser.add_argument("--theta",type=float,default=1.0)
parser.add_argument("--gamma",type=float,default=1.0)
parser.add_argument("--sitenum",type=int,default=10)
parser.add_argument("--time",type=int,default=200)
parser.add_argument("--dataname",type=str,default="tests")
parser.add_argument("--mix_in",type=int,default=2)
parser.add_argument("--mass_matrix",type=float,default=1)
parser.add_argument("--symplectic_integrator_num_steps",type=int,default=2)


args = parser.parse_args()
weight = args.weight
pf = args.pf
pa = args.pa
theta_multiplier = args.theta
gamma_multiplier = args.gamma
sitenum = args.sitenum
time = args.time
xi = args.xi
dataname = args.dataname
mix_in= args.mix_in
mass_matrix=args.mass_matrix
symplectic_integrator_num_steps=args.symplectic_integrator_num_steps

workdir = os.getcwd()
output_dir = workdir+"/output/"+dataname+"/pf_"+str(pf)+"_pa_"+str(pa)+"_time_"+str(time)+"/theta_"+str(theta_multiplier)+"_gamma_"+str(gamma_multiplier)+"/sitenum_"+str(sitenum)+"_xi_"+str(xi)+"/mix_in_"+str(mix_in)+"_mass_matrix_"+str(mass_matrix)+"_symplectic_integrator_num_steps_"+str(symplectic_integrator_num_steps)+"/weight_"+str(weight)+"/"
plotdir = workdir+"/plot/"+dataname+"/pf_"+str(pf)+"_pa_"+str(pa)+"_time_"+str(time)+"/theta_"+str(theta_multiplier)+"_gamma_"+str(gamma_multiplier)+"/sitenum_"+str(sitenum)+"_xi_"+str(xi)+"/mix_in_"+str(mix_in)+"_mass_matrix_"+str(mass_matrix)+"_symplectic_integrator_num_steps_"+str(symplectic_integrator_num_steps)+"/weight_"+str(weight)+"/"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
if not os.path.exists(plotdir):
    os.makedirs(plotdir)

with open(output_dir+'results.pcl', 'rb') as f:
    # Load the data from the file
    results = pickle.load(f)

fig, axes = plt.subplots(1, 1, figsize = (8,6))
for j in range(results['size']):
    plt.plot(results['uncertain_vals_tracker'][:, j], label=r"$\gamma_{%d}$"%(j+1))
plt.xlabel("Iteration")
plt.ylabel(r"$\gamma$")
plt.title(r"Trace Plot of $\gamma$")
legend = plt.legend(bbox_to_anchor=(1.05, 0.5), loc="center left", borderaxespad=0)
fig.tight_layout()
plt.subplots_adjust(right=0.7) # Adjust this value to fit your legend properly.

fig.savefig(plotdir +'gamma.png', bbox_extra_artists=(legend,), bbox_inches='tight', dpi = 100)
plt.close()


fig, axes = plt.subplots(1, 1, figsize = (8,6))
plt.plot(results['error_tracker'])
plt.xlabel("Iteration times")
plt.ylabel("Error")
plt.title("Error")
fig.savefig(plotdir +'error.png', dpi = 100)
plt.close()

for j in range(results['size']):
    fig, axes = plt.subplots(1, 1, figsize = (8,6))
    sns.histplot(results['collected_ensembles'][0][:, j], bins=100, label="Unadjusted", kde=False, color='blue')
    sns.histplot(results['collected_ensembles'][len(results['collected_ensembles'])-1][:, j], bins=100, label="Adjusted", kde=False, color='red')
    plt.xlabel(r"$\gamma_{%d}$"%(j+1))
    plt.ylabel("Distribution")
    plt.title(r"Distribution of $\gamma_{%d}$"%(j+1))
    plt.legend()
    fig.savefig(plotdir +'gamma_%d.png'%(j+1), dpi = 100)
    plt.close()