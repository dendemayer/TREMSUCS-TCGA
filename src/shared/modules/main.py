import os
import click
from shared.modules import choose_therapy
from shared.modules import download_with_api
from tcga_metilene.modules import main_metilene
from tcga_deseq.modules import main_deseq
import snakemake
from itertools import compress
# import re

SCRIPT_PATH = os.path.split(__file__)[0]
with open(os.path.join(SCRIPT_PATH, 'version.txt'), 'r') as f:
    version = f.readline().strip()

pipeline_list = ['DESeq2', 'metilene']


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(version)
    ctx.exit()


HOME = os.getenv('HOME')


@click.command()
@click.option('--out_path', '-o', default=os.path.join(HOME, 'TCGA-pipelines'),
              show_default=True,
              help='path to save the result files')
@click.option('--project', '-p', default=[], multiple=True,
              help='TCGA project to be applied. Any TCGA project can be' +
              ' chosen, like: ' +
              '-p TCGA-CESC -p TCGA-HNSC ...')
@click.option('--drugs', '-d', default=[], multiple=True, show_default=False,
              help='drug(s), like: -d drug1 -d drug2 ' +
              'or drugcombination(s), like: -d drug1,drug2')
@click.option('--cores', '-c', default=1, multiple=False, show_default=True,
              type=int, help='number of cores provided to snakemake',
              required=False)
@click.option('--cutoff', '-C', default=[0], multiple=True, show_default=True,
              type=float, help='Cut-off parameter',
              required=False)
@click.option('--threshold', '-t', default=[0], multiple=True, show_default=True,
              type=float, help='threshold parameter',
              required=False)
@click.option('--execute', '-e', default=pipeline_list, multiple=True,
              show_default=True, help='choose which pipeline shall be\
              executed')
@click.option('--dryrun', '-D', default=False, multiple=False,
              show_default=True, is_flag=True, help='snakemake dryrun',
              required=False)
@click.option('--report', '-r', default=False, multiple=False,
              show_default=True, is_flag=True, help='just create a report',
              required=False)
@click.option('--version', '-v',
              help='printing out version information: {}'.format(version),
              is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)
def call_with_options(out_path, project, drugs, cores, execute, cutoff,
                      threshold, dryrun, report):
    '''
    TreMSuc, a tool to choose, harvest and analyse methylation and rna
    count data of the TCGA-projects with help of the package metilene and
    DEseq2.\n

    Build and activate the provided conda env:
    bash

        $ conda env create -f metilene_env.yaml

        $ conda activate metilene_pipeline

    call the script without any options to enter the interactive mode and set
    each option step by step:

        $ python main_metilene.py

    print help page:

        $ python main_metilene.py --help
    '''
    OUTPUT_PATH = out_path
    print("\nOUTPUT_PATH:\t\t", OUTPUT_PATH)
    # SCRIPT_PATH = script_path
    SCRIPT_PATH = os.path.split(__file__)[0]
    print("SCRIPT_PATH:\t\t", SCRIPT_PATH)
    # make sure that the pipelines to execute also exist, every entry must be
    # present in : ['DESeq2', 'metilene']
    temp_check = [True if i not in pipeline_list else False for i in execute]
    if True in temp_check:
        print('\nyou misspelled a pipeline name, make sure the ', end='')
        print(f'-e option set is within the set of {pipeline_list}, ', end='')
        print('wrong pipeline name: ', end='')
        print(f'{list(compress(execute, temp_check))}, ', end='')
        print('exiting now')
        os._exit(0)
    execute = sorted(list(execute))
    print("PIPELINES executed:\t", execute)
    project = [i.strip() for i in project]
    if len(project) == 0:
        PROJECT = choose_therapy.Choose_project()
        PROJECT = sorted(map(str.upper, PROJECT))
    else:
        PROJECT = sorted(map(str.upper, project))
    if len(drugs) == 0:
        DRUGS = choose_therapy.Choose_drugs(SCRIPT_PATH, PROJECT)
        DRUGS = sorted(map(str.lower, DRUGS))
    else:
        DRUGS = sorted(map(str.lower, drugs))

    cutoffs = list(cutoff)
    for index, cutoff in enumerate(cutoffs):
        if cutoff % 1 == 0:
            cutoffs[index] = round(cutoff)
    if 0 not in cutoffs:
        cutoffs.append(0)
    cutoffs = sorted(list(set(cutoffs)))

    thresholds = list(threshold)
    for index, threshold in enumerate(thresholds):
        if threshold % 1 == 0:
            thresholds[index] = round(threshold)
    if 0 not in thresholds:
        thresholds.append(0)
    threshold = sorted(list(set(thresholds)))

    thresh_list = [f'threshold_{str(i)}' for i in threshold]
    thresh_str = '_'.join(thresh_list)
    print('PROJECT:\t\t', PROJECT)
    print('DRUGS:\t\t\t', DRUGS)
    print(f'cores:\t\t\t{cores}')
    print(f'cutoff:\t\t\t{cutoffs}')
    print(f'threshold:\t\t{threshold}')


    shared_scriptdir = os.path.join(
        os.path.split(os.path.split(SCRIPT_PATH)[0])[0], 'shared')

    Snakemake_all_files = []

    Snakefile = os.path.join(os.path.split(SCRIPT_PATH)[0], 'Snakefile')
    config_file_shared = os.path.join(shared_scriptdir, 'config.yaml')

    # help files for both pipelines, like:
    # OUTPUT_PATH/metadata/gdc_manifest_20211029_data_release_31...,
    # gencode.v36.annotation
    help_file_list = download_with_api.download_help_files(
        OUTPUT_PATH, config_file_shared)
    Snakemake_all_files = Snakemake_all_files + help_file_list
    projects = '_'.join(PROJECT)
    def return_type(pipeline):
        if pipeline == "DESeq2":
            return "norm_count"
        elif pipeline == "metilene":
            return "beta_vals"
    types = [return_type(i) for i in execute]
    drug_str = '_'.join(DRUGS)

    # count_type = []  # the count type is later specified within either deseq or
    count_type = {'metilene': ['beta_vals'], 'DESeq2': ['norm_count']}
    # metilene main module, must be defined here already since it is also set in
    # the shared Snakefile
    config={'thresh': thresh_str, 'thresh_list': thresh_list, 'pipelines': execute, 'projects_str': projects, 'cutoffs': cutoffs, 'types': types, 'OUTPUT_PATH': OUTPUT_PATH, 'drug_str': drug_str, 'count_type': count_type}
    # once we have to call snakemake in prior, s.t. the manifest file is
    # present on which all the following selections are done on, make sure that
    # here the dryrun flag is not set to True
    # # TODO uncomment this !!!
    if not report:
        workflow =  snakemake.snakemake(snakefile=Snakefile,
                                        targets=Snakemake_all_files,
                                        rerun_triggers='mtime',
                                        workdir=OUTPUT_PATH, cores=cores,
                                        forceall=False, force_incomplete=True,
                                        dryrun=dryrun, use_conda=True,
                                        configfiles=[config_file_shared],
                                        config=config)
        if not workflow:
            print('snakemake execution failed, exiting now')
            os._exit(0)
    # TODO uncomment this !!!

    # auxfiles for both pipelines:
    # OUTPUT_PATH/PROJECT/aux_files/nationwidechildrens.....
    aux_file_list = download_with_api.download_aux_files(OUTPUT_PATH, PROJECT,
                                                         config_file_shared)

    Snakemake_all_files = Snakemake_all_files + aux_file_list

    def map_execute(pipeline):
        """
        translate here the applied pipeline which shall be executet:
        Datafiles: OUTPUT_PATH/PROJECT/Diffexpression/PROJECT_data_files/...
        """
        if pipeline == 'DESeq2':
            return 'htseq'
        elif pipeline == 'metilene':
            return 'HumanMethylation450'

    data_file_list = []
    file_types = map(map_execute, execute)
    for file_type in file_types:
        data_file_list = (data_file_list +
                          download_with_api.download_data_files(
                              OUTPUT_PATH, PROJECT, config_file_shared,
                              file_type))

    Snakemake_all_files = Snakemake_all_files + data_file_list

    print('running snakemake with\n')
    print(f'Snakefile:\t{Snakefile}')
    print(f'shared_scriptdir:\t{shared_scriptdir}')

    # also add the multi proj meta_info_druglist_merged_drugs_combined.tsv
    # which is just the concatenation of the single proj pendants:
    # by that those singl proj meta tables are created aswell
    merged_drugs_combined_list = []

    cutoffs_str = [f'cutoff_{str(i)}' for i in cutoffs]
    for pipeline in execute:
        for cutoff in cutoffs_str:
            merged_drugs_combined_list.append(os.path.join(
                OUTPUT_PATH, projects, pipeline, 'merged_meta_files', cutoff,
                'meta_info_druglist_merged_drugs_combined.tsv'))

    Snakemake_all_files = Snakemake_all_files + merged_drugs_combined_list

    # ########################################################################
    # # TODO uncomment this !!!
    # ########################################################################
    # # rerun_trggers='mtime' IMPORTANT -> the needed input data is generated via
    # # input function in shared snakefile for rule merge_meta_tables:
    # # without this option this rule would be ran everytime, since everything
    # # following is based on those aux file, every rule would be triggered
    # # then again
    if not report:
        workflow = snakemake.snakemake(snakefile=Snakefile,
                                    targets=Snakemake_all_files,
                                    workdir=OUTPUT_PATH, cores=cores,
                                    forceall=False, force_incomplete=True,
                                    dryrun=dryrun, use_conda=True,
                                    rerun_triggers='mtime',
                                    configfiles=[config_file_shared],
                                    config=config)
        if not workflow:
            print('snakemake execution failed, exiting now')
            os._exit(0)
    ########################################################################
    # TODO uncomment this !!!
    ########################################################################

    # to download every meta table :
    # run this command and exit here with os._exit(0)
    # temp=("-p TCGA-CESC" "-p TCGA-HNSC" "-p TCGA-LUSC" "-p TCGA-ESCA" "-p TCGA-BRCA" "-p TCGA-GBM" "-p TCGA-OV" "-p TCGA-LUAD" "-p TCGA-UCEC" "-p TCGA-KIRC" "-p TCGA-LGG" "-p TCGA-THCA" "-p TCGA-PRAD" "-p TCGA-SKCM" "-p TCGA-COAD" "-p TCGA-STAD" "-p TCGA-BLCA" "-p TCGA-LIHC" "-p TCGA-KIRP" "-p TCGA-SARC" "-p TCGA-PAAD" "-p TCGA-PCPG" "-p TCGA-READ" "-p TCGA-TGCT" "-p TCGA-THYM" "-p TCGA-KICH" "-p TCGA-ACC" "-p TCGA-MESO" "-p TCGA-UVM" "-p TCGA-DLBC" "-p TCGA-UCS" "-p TCGA-CHOL")
    # for i in ${temp[@]}; do echo tcga_pipelines -p $i -d cisplatin -o /scr/dings/PEVO/NEW_downloads_3/TCGA-pipelines_7 -c 40; done
    os._exit(0)

    # from here the shared modules and Snakemake scripts are getting pipeline
    # specific, hand over all outputfiles requested so far and enter the
    # pipeline specific main files:
    Snakemake_report_met = []
    Snakemake_report_des = []
    if 'metilene' in execute:
        print('entering metilene entry fct')
        Snakemake_report_met = main_metilene.entry_fct(OUTPUT_PATH, PROJECT,
                                                          DRUGS,
                                                          Snakemake_all_files,
                                                          cutoffs, threshold,
                                                          cores, 'metilene',
                                                          config_file_shared,
                                                          config, dryrun,
                                                          cutoffs_str, report)
    if 'DESeq2' in execute:
        print('entering deseq entry fct')
        Snakemake_report_des = main_deseq.entry_fct(OUTPUT_PATH, PROJECT,
                                                       DRUGS,
                                                       Snakemake_all_files,
                                                       threshold, cores,
                                                       'DESeq2',
                                                       config_file_shared,
                                                       config, dryrun,
                                                       cutoffs_str, report)

    Snakemake_report_files = Snakemake_report_des + Snakemake_report_met

    # # one or both pipelines are finished here, final aggregation over both
    # pipelines:

    # the final majority vote file, aggregated over all pipelines:
    # depending on the pipeline chosen:

    major_file = os.path.join(OUTPUT_PATH, projects, '_'.join(execute),
                              '_'.join(DRUGS), 'final_majority_vote.tsv.gz')
    major_file_pdf = os.path.join(OUTPUT_PATH, projects, '_'.join(execute),
                              '_'.join(DRUGS), 'final_majority_vote_pipeline_project_final.pdf')


    p_val_prod_sum = []
    if 'DESeq2' in execute:
        p_val_prod_sum.extend([os.path.join(OUTPUT_PATH, projects, 'DESeq2', 'DESeq2_output' , '_'.join(DRUGS), 'female_male', '-'.join(cutoffs_str), '_'.join([f'threshold_{str(i)}' for i in threshold]), 'DESeq2-norm_count_p_prod_sum.pdf')])
    if 'metilene' in execute:
        p_val_prod_sum.extend([os.path.join(OUTPUT_PATH, projects, 'metilene', 'metilene_output' , '_'.join(DRUGS), 'female_male', '-'.join(cutoffs_str), '_'.join([f'threshold_{str(i)}' for i in threshold]), 'metilene-beta_vals_p_prod_sum.pdf')])

    shared_pipeline_files = [major_file, major_file_pdf] + p_val_prod_sum
    Snakemake_report_files = Snakemake_report_files + shared_pipeline_files + p_val_prod_sum
    Snakemake_report_files.sort()

    if not report:
        workflow = snakemake.snakemake(snakefile=Snakefile, targets=shared_pipeline_files,
                                    workdir=OUTPUT_PATH, cores=cores,
                                    forceall=False, force_incomplete=True,
                                    dryrun=dryrun, use_conda=True,
                                    configfiles=[config_file_shared],
                                    rerun_triggers='mtime', config=config)
        if not workflow:
            print('snakemake execution failed, exiting now')
            os._exit(0)

    report_file = os.path.join(OUTPUT_PATH, projects, '_'.join(execute),
                               '_'.join(DRUGS), 'report.html')

    ###########################################################################
    #                            final REPORT creation                        #
    ###########################################################################
    # sort the report files according to their subcategory:

    # also with dryrun set, the report file would be created, catch that
    # beforehand:
    if not dryrun:
        workflow = snakemake.snakemake(snakefile=Snakefile, targets=Snakemake_report_files,
                                    workdir=OUTPUT_PATH, cores=cores,
                                    forceall=False, force_incomplete=True,
                                    use_conda=True,
                                    configfiles=[config_file_shared],
                                    rerun_triggers='mtime', config=config,
                                    report=report_file,
                                    report_stylesheet=os.path.join(
                                        os.path.split(__file__)[0], os.pardir,
                                        "report_src", "custom-stylesheet.css"))

        if not workflow:
            print('snakemake execution failed, exiting now')
            os._exit(0)
