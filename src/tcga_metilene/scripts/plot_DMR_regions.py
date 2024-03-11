from matplotlib import pyplot as plt
import os
import pandas as pd
import seaborn as sns
import statistics as st
import sys

if 'snakemake' in dir():
    sys.stdout = sys.stderr = open(snakemake.log[0], 'w')

    print('# snakemake inputs:')
    [ print(f'{i[0]} = "{i[1]}"') for i in snakemake.input.items()]

    print('# snakemake output:')
    [ print(f'{i[0]} = "{i[1]}"') for i in snakemake.output.items()]

    print('# snakemake wildcards:')
    [ print(f'{i[0]} = "{i[1]}"') for i in snakemake.wildcards.items()]

    metilene_intersect = snakemake.input.metilene_intersect
    pdf_boxplot_out = snakemake.output.pdf_boxplot_out
    pdf_lineplot_out = snakemake.output.pdf_lineplot_out
    project = snakemake.wildcards.project
    drug_combi = snakemake.wildcards.drug_combi
    gender = snakemake.wildcards.gender
    cutoff = snakemake.wildcards.cutoff
    DMR = snakemake.wildcards.DMR
else:
    # snakemake inputs:
    metilene_intersect = "/scr/palinca/gabor/TCGA-pipeline_7_pval_prod/TCGA-CESC/metilene/metilene_output/carboplatin_carboplatin,paclitaxel_cisplatin/female/cutoff_0/metilene_intersect.tsv"
    script_file = "/homes/biertruck/gabor/phd/test_git_doc/tcga_piplines/src/shared/../tcga_metilene/scripts/plot_DMR_regions.py"
    # snakemake output:
    pdf_boxplot_out = "/scr/palinca/gabor/TCGA-pipeline_7_pval_prod/TCGA-CESC/metilene/metilene_output/carboplatin_carboplatin,paclitaxel_cisplatin/female/cutoff_0/metilene_intersect_boxplot_beta_value_chr20_58850459_58852155.pdf"
    pdf_lineplot_out = "/scr/palinca/gabor/TCGA-pipeline_7_pval_prod/TCGA-CESC/metilene/metilene_output/carboplatin_carboplatin,paclitaxel_cisplatin/female/cutoff_0/metilene_intersect_lineplot_median_beta_value_chr20_58850459_58852155.pdf"
    # snakemake wildcards:
    output_path = "/scr/palinca/gabor/TCGA-pipeline_7_pval_prod"
    project = "TCGA-CESC"
    drug_combi = "carboplatin_carboplatin,paclitaxel_cisplatin"
    gender = "female"
    cutoff = "cutoff_0"
    DMR = "chr20_58850459_58852155"
    project = 'TCGA-CESC'
    drug_combi = 'carboplatin_carboplatin,paclitaxel_cisplatin'
    gender = 'female'

###############################################################################
#                                   test set                                  #
###############################################################################

# (Pdb) num_cols
# 3
# # snakemake inputs:
# metilene_intersect = "/scr/palinca/gabor/TCGA-pipeline_5/TCGA-CESC_TCGA-HNSC/metilene/metilene_output/carboplatin_carboplatin,paclitaxel_cisplatin/female_male/cutoff_5/metilene_intersect.tsv"
# # snakemake output:
# pdf_boxplot_out = "/scr/palinca/gabor/TCGA-pipeline_5/TCGA-CESC_TCGA-HNSC/metilene/metilene_output/carboplatin_carboplatin,paclitaxel_cisplatin/female_male/cutoff_5/metilene_intersect_boxplot_beta_value_chr8_140238482_140238568_temp.pdf"
# pdf_lineplot_out = "/scr/palinca/gabor/TCGA-pipeline_5/TCGA-CESC_TCGA-HNSC/metilene/metilene_output/carboplatin_carboplatin,paclitaxel_cisplatin/female_male/cutoff_5/metilene_intersect_lineplot_median_beta_value_chr8_140238482_140238568_temp.pdf"
# # snakemake wildcards:
# output_path = "/scr/palinca/gabor/TCGA-pipeline_5"
# project = "TCGA-CESC_TCGA-HNSC"
# drug_combi = "carboplatin_carboplatin,paclitaxel_cisplatin"
# gender = "female_male"
# cutoff = "cutoff_5"
# DMR = "chr8_140238482_140238568"

# (Pdb) num_cols
# 53
# different width functions needed for box and lineplot:
# box plot: 53 cols: -> 20 width y=0.24⋅x+7.280000000000001
# lineplot: 53 cols: -> 13 width y=0.16⋅x+4.52

# box plot: 3 cols: -> 8 width
# lineplot: 3 cols: -> 5 width

# box fct:

# snakemake inputs:
# metilene_intersect = "/scr/palinca/gabor/TCGA-pipeline_5/TCGA-CESC_TCGA-HNSC/metilene/metilene_output/carboplatin_carboplatin,paclitaxel_cisplatin/female_male/cutoff_5/metilene_intersect.tsv"
# # snakemake output:
# pdf_boxplot_out = "/scr/palinca/gabor/TCGA-pipeline_5/TCGA-CESC_TCGA-HNSC/metilene/metilene_output/carboplatin_carboplatin,paclitaxel_cisplatin/female_male/cutoff_5/metilene_intersect_boxplot_beta_value_chr6_32095336_32097234_temp.pdf"
# pdf_lineplot_out = "/scr/palinca/gabor/TCGA-pipeline_5/TCGA-CESC_TCGA-HNSC/metilene/metilene_output/carboplatin_carboplatin,paclitaxel_cisplatin/female_male/cutoff_5/metilene_intersect_lineplot_median_beta_value_chr6_32095336_32097234_temp.pdf"
# # snakemake wildcards:
# output_path = "/scr/palinca/gabor/TCGA-pipeline_5"
# project = "TCGA-CESC_TCGA-HNSC"
# drug_combi = "carboplatin_carboplatin,paclitaxel_cisplatin"
# gender = "female_male"
# cutoff = "cutoff_5"
# DMR = "chr6_32095336_32097234"

###############################################################################
#                                   test set                                  #
###############################################################################

# # snakemake inputs:
# metilene_intersect = "/scr/palinca/gabor/TCGA-pipeline_2/TCGA-CESC_TCGA-HNSC_TCGA-LUSC/metilene/metilene_output/carboplatin_carboplatin,paclitaxel_cisplatin/female/cutoff_0/metilene_intersect.tsv"
# # snakemake output:
# pdf_boxplot_out = "/scr/palinca/gabor/TCGA-pipeline_2/TCGA-CESC_TCGA-HNSC_TCGA-LUSC/metilene/metilene_output/carboplatin_carboplatin,paclitaxel_cisplatin/female/cutoff_0/metilene_intersect_boxplot_beta_value_chrX_72306008_72308502.pdf"
# pdf_lineplot_out = "/scr/palinca/gabor/TCGA-pipeline_2/TCGA-CESC_TCGA-HNSC_TCGA-LUSC/metilene/metilene_output/carboplatin_carboplatin,paclitaxel_cisplatin/female/cutoff_0/metilene_intersect_lineplot_median_beta_value_chrX_72306008_72308502.pdf"
# # snakemake wildcards:
# output_path = "/scr/palinca/gabor/TCGA-pipeline_2"
# project = "TCGA-CESC_TCGA-HNSC_TCGA-LUSC"
# drug_combi = "carboplatin_carboplatin,paclitaxel_cisplatin"
# gender = "female"
# cutoff = "cutoff_0"
# DMR = "chrX_72306008_72308502"


# make use of MI:
# # (Pdb) DF_DMR.index.names
# # FrozenList(['Chromosome', 'Start', 'End', 'region'])
# # (Pdb) DF_DMR.columns.names
# # FrozenList(['vital_status', 'case_id', 'drugs', 'gender', 'projects'])
DF_DMR = pd.read_table(metilene_intersect, header=[0, 1, 2, 3, 4], index_col=[0, 1, 2, 3], na_values='.')
# out of the MI index parse the regions:
# # (Pdb) DF_DMR.index.names
# # FrozenList(['Chromosome', 'Start', 'End', 'region'])

# range_list = pd.Index(
#     [i[3] for i in DF_DMR.index.tolist()]).value_counts().index.to_list()
project_list = pd.Index(
    [i[4] for i in DF_DMR.columns]).value_counts().index.to_list()
palette_len = len(project_list) * 2


# for plotting access each DMR seperately:
# do not loop over every range out of the intersect table since the DMR are
# requested already by the input function:
# def return_plot_DMR_regions_plot(metilene_intersect_tables): in modules/bed_intersect_metilene.py
# for range_ in range_list:
# limit the DF to the recent region:
try:
    DF_to_plot = DF_DMR.loc[(slice(None), slice(None), slice(None), DMR), :]
except Exception as e:
    # KeyError('chr19_58228367_58228578') in meta table TCGA-LUSC/metilene/metilene_output/carboplatin_carboplatin,paclitaxel_cisplatin_paclitaxel/female_male/cutoff_0/metilene_complement_intersect.tsv
 # vital_status |          |          |                         | alive              | dead               | dead
 # chr19        | 58228368 | 58228369 | chr19_58228367_58228578 | .                  | .                  | .
 # chr19        | 58228412 | 58228413 | chr19_58228367_58228578 | .                  | .                  | .
 # chr19        | 58228437 | 58228438 | chr19_58228367_58228578 | .                  | .                  | .
 # chr19        | 58228439 | 58228440 | chr19_58228367_58228578 | .                  | .                  | .
 # --> found ranges for cases for which we dont have the
    print(e)
    print(DF_DMR)
    open(pdf_boxplot_out, 'a').close()
    open(pdf_lineplot_out, 'a').close()
    os._exit(0)
DF_to_plot_median = DF_to_plot.groupby( by=['vital_status', 'projects'], axis=1).median().reset_index('Start')
projects_list = [ i[4] for i in DF_to_plot.columns]
vital_array = [ i[0] for i in DF_to_plot.columns]
new_co_MI = pd.MultiIndex.from_arrays([vital_array, projects_list], names=('vital_status', 'projects'))
DF_to_plot.columns = new_co_MI
DF_to_plot.reset_index(level=[0,2,3], drop=True, inplace=True)
DF_to_plot = DF_to_plot.T.reset_index()
DF_to_plot['hue'] = DF_to_plot['vital_status'] + ' + ' + DF_to_plot['projects']
hue = DF_to_plot['hue'].to_list()
DF_to_plot = DF_to_plot.iloc[:, 2:-1]
hue = hue * DF_to_plot.shape[1]
DF_to_plot = DF_to_plot.melt()
num_cols = DF_to_plot['Start'].nunique()
# figsize = (0.09541062801932366*num_cols + 8.496376811594203, 5)
figsize = (0.24*num_cols+7.280000000000001, 5)
# figsize = (7, 5)
# figsize = (5, 8)
DF_to_plot.rename({'value': 'beta_value'}, axis=1, inplace=True)
DF_to_plot['hue'] = hue
DF_to_plot.sort_values(by=['Start', 'hue'], inplace=True)
range_title = DMR.split('_')
range_title = f'{range_title[0]}: {range_title[1]}-{range_title[2]}'
color_palette = sns.color_palette('coolwarm_r', palette_len)
sns.set(rc={'figure.figsize':figsize})
sns.set(style="ticks", palette=color_palette)
plot = sns.boxplot(x='Start', y='beta_value', hue='hue', data=DF_to_plot)
plt.title(f'DMR: {range_title}\n{project}, {drug_combi},\n{gender}, cutoff={cutoff}')
plot.set_xticklabels(plot.get_xticklabels(), rotation=45)
plt.legend(title='vital state and projects', bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.grid(axis='y')
plt.tight_layout()
print(f'saving {pdf_boxplot_out}')
plot.figure.savefig(pdf_boxplot_out)
plt.clf()
plt.cla()
plt.close()

plot = sns.violinplot(x='Start', y='beta_value', hue='hue', data=DF_to_plot)
plot.set_xticklabels(plot.get_xticklabels(), rotation=45)
plt.title(f'DMR: {range_title}\n{project}, {drug_combi},\n{gender}, cutoff={cutoff}')
plt.legend(title='vital state and projects', bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.grid(axis='y')
plt.tight_layout()
pdf_violinplot_out = pdf_boxplot_out.replace('boxplot', 'violinplot')
print(f'saving {pdf_violinplot_out}')
plot.figure.savefig(pdf_violinplot_out)
plt.clf()
plt.cla()
plt.close()

DF_to_plot = DF_DMR.loc[(slice(None), slice(None), slice(None), DMR), :]
DF_to_plot.columns = new_co_MI
DF_to_plot.reset_index(level=[0, 2, 3], drop=True, inplace=True)
DF_to_plot = DF_to_plot.T.reset_index()
DF_to_plot['hue'] = DF_to_plot['vital_status'] + ' + ' + DF_to_plot['projects']
DF_to_plot = DF_to_plot.drop(['vital_status', 'projects'], axis=1)
DF_to_plot = DF_to_plot.groupby('hue').median()
hue = DF_to_plot.index.to_list()
hue = hue * DF_to_plot.shape[1]
DF_to_plot = DF_to_plot.melt()
DF_to_plot['hue'] = hue
DF_to_plot.sort_values(by=['Start', 'hue'], inplace=True)
DF_to_plot.rename({'value': 'beta-value median'}, axis=1, inplace=True)
#     # ### plot just the median as linegraph:
#     DF_line_plot = DF_to_plot.groupby(
#         ['vital_state', 'project', 'Start']).median(
#     ).reset_index(
#         ['Start', 'vital_state', 'project']).rename(
#         {'mean_beta_value': 'median of means beta value'},
#         axis=1)
#     DF_line_plot['vital_proj'] = DF_line_plot['vital_state']\
#         + '_' + DF_line_plot['project']

# plt.figure(figsize=(15, 5))
#     # plt.rcParams["figure.autolayout"] = True
#     # DF_line_plot['Start'] =
#     # pd.Categorical(DF_line_plot['Start'])
# plt.figure()
# plt.ticklabel_format(
    # style='plain', axis='x', useOffset=False)
# # style='vital_proj', markers=True
# figsize = (0.09541062801932366*num_cols + 8.496376811594203, 5)
figsize = (0.16*num_cols+4.52,  5)
sns.set(rc={'figure.figsize':figsize})
sns.set(style="ticks", palette=color_palette)
plot = sns.lineplot(
    data=DF_to_plot,
    x="Start",
    marker='o',
    y="beta-value median", #  linewidth=3,
    hue="hue")
plt.title(f'DMR: {range_title}\n{project}, {drug_combi},\n{gender}, cutoff={cutoff}')


plot.set_xticks(DF_to_plot['Start'].value_counts().index.tolist()) # <--- set the ticks first
label_list = DF_to_plot['Start'].value_counts().index.astype('str').tolist()
plot.set_xticklabels(label_list)
plt.setp(plot.get_xticklabels(), rotation=90)



DF_DMR = DF_DMR.loc[(slice(None), slice(None), slice(None), DMR), :]
# median of medians:
# alive_median = DF_DMR.loc[:, 'alive'].median(axis=1).median()
# (Pdb) alive_median
# ((# 0.47273767353634655))
# this is the real alive median, without taking the median of medians, position
# wise:  ((# 0.3524210273792245)))
DF_DMR_alive = DF_DMR.loc[:, ('alive', slice(None), slice(None), slice(None), slice(None))]
alive_median = pd.concat([DF_DMR_alive.loc[:, i] for i in DF_DMR_alive ]).median()

DF_DMR_dead = DF_DMR.loc[:, ('dead', slice(None), slice(None), slice(None), slice(None))]
dead_median = pd.concat([DF_DMR_dead.loc[:, i] for i in DF_DMR_dead ]).median()

mean_of_medians = st.mean([alive_median, dead_median])

# overall_beta_median = DF_DMR.apply(lambda x: x.median(), axis=1).median()
# (Pdb) DF_DMR.loc[(slice(None), [3848400, 3848556], slice(None), slice(None)), (slice(None), slice(None), slice(None), slice(None), 'TCGA-LUSC')].apply(lambda x: x.mean(), axis=1)
# plt.hlines(overall_beta_median, ls = '--', label='median', xmin=0.5, xmax=0.5, colors='green')
# muted_green = sns.color_palette("muted")[2]  # You can adjust the index as needed
# sns.color_palette("muted")

# plt.axhline(alive_median, ls = '--', label='alive median', c=color_palette[0])
# plt.axhline(dead_median, ls = '--', label='dead median', c=color_palette[-1])
# plt.axhline(mean_of_medians, ls = '--', label='mean of medians', c=muted_green)
# plt.text(0,0 , "median of all medians")

# which position has the highest diff in terms of its median? -> this is going
# to be the position to check further
start_of_max = (DF_DMR.loc[:, 'alive'].median(axis=1) - DF_DMR.loc[:, 'dead'].median(axis=1)).abs().idxmax()[1]

max_diff = str(round((DF_DMR.loc[:, 'alive'].median(axis=1) - DF_DMR.loc[:, 'dead'].median(axis=1)).abs().max(), 2))

DF_DMR.loc[:, 'alive'].median(axis=1).loc[(slice(None), start_of_max, slice(None), slice(None))]
# alive_median_max_value = DF_DMR.loc[:, 'alive'].median(axis=1).loc[(slice(None), start_of_max, slice(None), slice(None))].values[0]
# dead_median_max_value = DF_DMR.loc[:, 'dead'].median(axis=1).loc[(slice(None), start_of_max, slice(None), slice(None))].values[0]
# v_list = [alive_median_max_value, dead_median_max_value]
#### v max is too short: (Pdb) max(v_list) 0.633338811350208 , 0.95 fits better, how can i access that?
#

# (Pdb) plt.figure().properties()['figheight']
# 4.8
# the vline min max goes from 0 to 1, depending on the y scale maxime, adjust
# the values where the actual data lies on:
# plt.axvline(start_of_max, ls = '--', label=f'max diff ({max_diff})', c=sns.color_palette("muted")[0], ymin=0, ymax=1)

legend = plt.legend(
    title='vital state of all projects',
    bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
for legobj in legend.legend_handles:
    legobj.set_linewidth(3.0)
#     # plt.legend(
#         # title='vital state of all projects',
#         # bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
#     # plt.legend(
#     # title='vital state of all projects', bbox_to_anchor=(1,
#     # 1))
plt.grid(axis='y')
plt.tight_layout()
print(f'saving {pdf_lineplot_out}')
plot.figure.savefig(pdf_lineplot_out)

plt.clf()
plt.close()
