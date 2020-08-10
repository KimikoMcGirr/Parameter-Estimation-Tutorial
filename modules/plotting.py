import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import fsolve
from scipy.integrate import odeint
import seaborn as sns
from model import *
import pandas as pd
import warnings

import model
import EA
import h5py
import os
import pathlib


def get_sim_data(folder, num_sims=None):
    try:
        my_abs_path = os.path.exists(folder)
    except FileNotFoundError:
        print("Folder not found ¯\_(ツ)_/¯")
    else:
        all_mses = []
        all_params = []
        empty_data = 0
        for i, loaded_data in enumerate(pathlib.Path(folder).glob('*.hdf5')):
            if num_sims:
                if i > num_sims-1:
                    break
            if os.path.getsize(loaded_data) > 0:
                f = h5py.File(loaded_data, 'r')
                all_mses.append(np.array(f['best_error']))
                all_params.append(np.array(f['top_params']))
            else:
                empty_data += 1

    print("Number of runs collected: " + str(len(all_params)))
    print("Number of sims without data: " + str(empty_data))

    x = all_params[0]
    # print(x)
    print(len(x))
    last_mses = [all_mses[i][len(all_mses[0])-1] for i in range(len(all_mses[0]))]
    last_params = [all_params[i][len(all_params[0])-1] for i in range(len(all_params))]
    print(last_mses)
    print(len(last_mses))
    1/0

    last_mses = np.array(last_mses)
    last_params = np.array(last_params)
    all_mses = np.array(all_mses)
    all_params = np.array(all_params)

    print('Best last gen MSE: ' + str(np.sort(last_mses)[0]))
    print('Mean last gen MSEs of top 5%: ' + str(np.mean(np.sort(last_mses)[:round(len(last_mses)*0.05)])))

    f.close()

    return all_params, last_params, all_mses, last_mses

def plt_param_ranges(labelnames, dims, runs_sort, num_plt, synth_data=None, save_fig=''):
    # fig, (ax1) = plt.subplots(1, 1, figsize=(3,3))
    fig, (ax1) = plt.subplots(1, 1, figsize=(2.5,1.5))

#     pal = sns.set_palette(param_colors.get(m_name))

    # Hide the right and top spiness
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)

    # Only show ticks on the left and bottom spines
    ax1.yaxis.set_ticks_position('left')
    ax1.xaxis.set_ticks_position('bottom')

    major_ticks = np.arange(-2, 2.1, 1)
    ax1.set_yticks(major_ticks)

    #data handling
    df_param = pd.DataFrame(runs_sort[1][:num_plt])
    df_param.columns = labelnames
    df_param_log = df_param.apply(np.log10)
    df_melt = df_param_log.melt(var_name='param', value_name='vals')

    df_error = pd.DataFrame(runs_sort[0][:num_plt], columns=['error'])
    mses_df=df_error['error'].copy()
    mses_df = pd.concat([mses_df]*5, ignore_index=True)
    df_plot = pd.concat([df_melt,mses_df], axis=1)

    pal = sns.light_palette("purple", reverse=True, as_cmap=True )
#     cmap    = sns.light_palette("seagreen", reverse=False, as_cmap=True )
    # Normalize to the range of possible values from df["c"]
    norm = matplotlib.colors.Normalize(vmin=df_error['error'].min(), vmax=df_error['error'].max())
    # create a color dictionary (value in c : color from colormap)
    colors = {}
    for cval in df_plot["error"]:
        colors.update({cval : pal(norm(cval))})

    with sns.axes_style("whitegrid"):
        plt.bar(range(0,len(labelnames)),height=dims[0],bottom=dims[1],align='center',tick_label=labelnames, color='#dcdcdc',alpha = 0.8)
        ax1 = sns.swarmplot(x='param',y='vals', data = df_plot, hue='error', palette=colors, size=5) #size 3
        ax1.set_xticklabels(labelnames,rotation=90)
#         plt.xlabel('Parameters', fontsize=20, fontweight='medium')


    plt.grid(color='#606060', which='major', axis='y', linestyle='solid')
    if synth_data.any:
#         synth_data['param']=synth_data.index
#         synth_data.melt(var_name='param', value_name='vals')
        print(synth_data)
        ax1 = sns.swarmplot(data = synth_data, color = 'black', size=8, alpha=1, marker='*')
    ax1.set_ylabel('')
    ax1.set_xlabel('')

    plt.gca().legend_.remove()
    divider = make_axes_locatable(plt.gca())
    ax_cb = divider.new_horizontal(size="5%", pad=0.05)
    fig.add_axes(ax_cb)
    cb1 = matplotlib.colorbar.ColorbarBase(ax_cb, cmap=pal,
                                    norm=norm)
    if save_fig:
        plt.savefig(fig_folder+save_fig, dpi=300,bbox_inches='tight')
    plt.show()
