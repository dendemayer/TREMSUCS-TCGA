import pandas as pd
import os
import re
"""
:param: OUTPUT_PATH: path for pipeline outputs
:type: OUTPUT_PATH: str
:param: PROJECT: list of projects chosen
:type: PROJECT: list of str
:param: DRUGS_title: merged drug title out of multiple drugs
:type: DRUGS_title: str
:workflow_type: either methylation data or rna-count data
:type: workflow_type: str
:param: SCRIPT_PATH: path to the pipeline script
:type: SCRIPT_PATH: str

meta_info.dat and nationwidechildren are linked through:
meta_info.dat -> associated_entities.0.case_id
nationwide... -> bcr_patient_uuid
whats needed is col "id" out of meta_info.dat for sep
downloadeta_info.dat
and nationwidechildren are linked through:

.. _function_3:
.. code-block:: bash

    # for executing this step via terminal, issue -f 3 to your call,
    # example:
    $ python main_metilene.py -p TCGA-CESC -d cisplatin -f 3
"""
# 'resources/GCv36_Manifests/TCGA-CESC.tsv':, links the case_id to the datafile
manifest_file = snakemake.input[0]

# nationwidechildrens.org_biospecimen_aliquot_cesc.txt:
aliq_table_path = snakemake.input[1]

# nationwidechildrens.org_clinical_drug_cesc.txt:
drug_table_path = snakemake.input[2]

# nationwidechildrens.org_clinical_patient_cesc.txt:
patient_table_path = snakemake.input[3]

# nationwidechildrens.org_clinical_follow_up_v4.0_cesc.txt:
vital_table_path = snakemake.input[4]

# nationwidechildrens.org_biospecimen_sample_cesc.txt
sample_table_path = snakemake.input[5]

drug_out_path = snakemake.output[0]
complete_path = snakemake.output[1]

# we filter the output on the pipeline applied on, if Deseq2, than we filter
# the table on htseq files, if metilene, than we use the HumanMethylation450
PROJECT = [snakemake.wildcards[1]]
pipeline = snakemake.wildcards[2]

file_type = ''
if pipeline == 'Deseq2':
    file_type = 'htseq'
elif pipeline == 'metilene':
    file_type = 'HumanMethylation450'

# # aliquot table contains info about which file is used,
# # to be combined with manifest TCGA-CESC.tsv (mani_DF)
# combine a filtered TCGA-CESC.tsv on the filetype with the aliq_DF
aliq_DF = pd.read_table(aliq_table_path).loc[2:, :]
aliq_DF['bcr_patient_uuid'] = aliq_DF['bcr_patient_uuid'].str.lower()

# # ## merge aliquot ids from TCGA-CESC.tsv (mani_DF) with
# # nationwidechildrens.org_biospecimen_aliquot_cesc
mani_DF = pd.read_table(manifest_file)  # join on 'aliquot_ids'
# # this mani_DF can be filtered right away on the workflow_type:
# workflow_filter = mani_DF['workflow_type'] == workflow_type
mani_DF = mani_DF[mani_DF['filename'].str.contains(file_type)]
mani_DF.rename({'aliquot_ids': 'bcr_aliquot_uuid'}, axis=1, inplace=True)
mani_DF['bcr_aliquot_uuid'] = mani_DF['bcr_aliquot_uuid'].str.lower()
mani_DF['case_ids'] = mani_DF['case_ids'].str.lower()
mani_DF.rename({'case_ids': 'bcr_patient_uuid'}, axis=1, inplace=True)

# # drug_table contains info which therapy is used
# # nationwidechildrens.org_clinical_drug_cesc.txt
drug_DF = pd.read_table(drug_table_path).loc[2:, :]
drug_DF['bcr_patient_uuid'] = drug_DF['bcr_patient_uuid'].str.lower()

# # sample table contains info about tumor site:
sample_DF = pd.read_table(sample_table_path).loc[2:, :]
sample_DF['bcr_sample_uuid'] = sample_DF['bcr_sample_uuid'].str.lower()
sample_DF['bcr_patient_uuid'] = sample_DF['bcr_patient_uuid'].str.lower()
# # constrain samples to use on primary tumor samples:
primary_tumor_filter = sample_DF['sample_type'] == 'Primary Tumor'
sample_DF = sample_DF[primary_tumor_filter]

# # follow_up table (vital_DF) contains info like vital status and survival
# # times:
# # nationwidechildrens.org_clinical_follow_up_v4.0_cesc
# # proj_low_suf = PROJECT.replace('TCGA-', '').lower()
vital_base = os.path.basename(vital_table_path)
print(f'\nusing {vital_base} as clinical followup resource\n')
vital_DF = pd.read_csv(vital_table_path, sep='\t').loc[2:, :]
vital_DF['bcr_patient_uuid'] = vital_DF['bcr_patient_uuid'].str.lower()

# # nationwidechildrens.org_clinical_patient_cesc.txt'
# # patient_DF contains the gender info
patient_DF = pd.read_table(patient_table_path).loc[2:, :]
patient_DF['bcr_patient_uuid'] = patient_DF['bcr_patient_uuid'].str.lower()
# # it occurs that the col naming for age_at_diagnosis varies, check that:
# # nationwidechildrens.org_clinical_patient_cesc_columns -> age_at_diagnosis
# # nationwidechildrens.org_clinical_patient_hnsc_columns ->
# # age_at_initial_pathologic_diagnosis
# # -> harmonize the col to age_at_diagnosis
col_str = ' '.join(patient_DF.columns.to_list())
age_at_dia = re.findall('age_at.*?_diagnosis', col_str)[0]
patient_DF.rename({age_at_dia: 'age_at_diagnosis'}, axis=1, inplace=True)

# # [312 rows x 28 columns]:
#############################TODO
aliq_mani_DF = pd.merge(aliq_DF, mani_DF, on='bcr_aliquot_uuid')
########################################################################
# # ## END merge aliquot ids from TCGA-CESC.tsv with nation...aliquot..tsv ##
# # ######################## concat the drugnames in drug_DF:
# # this can be done before any merging steps with other tables:
# # the drugs are in col: pharmaceutical_therapy_drug_name
# # -> nupis must be converted to a single appearance, the drugs are
# # concantenatet via comma, correct misspelled drugnames:


def apply_list(value):
    # combined therapies are joined via '_' thats not allowed to be part of the
    # name, replace with '-'
    value = value.replace('_', '-')
    # correct wrong spellings:
    if re.search("palixtaxel", value):
        return "paclitaxel"
    if re.search("premetrexed", value):
        return "pemetrexed"
    if re.search("ironotecan", value):
        return "irinotecan"
    if (re.search("5-flurouracil", value) or
        re.search("5-fu", value) or re.search("5fu", value) or
        re.search("5 fu", value) or
        re.search("fluorouracil", value) or
        re.search("fluorouracil", value) or
            re.search("fluoruracil", value)):
        return "5-fluorouracil"
    if re.search("cisplatinum", value):
        return "cisplatin"
    if re.search("vinorelbin", value):
        return "vinorelbine"

    # ##harmonize synonyms:
    if re.search("cisplatin-xrt", value):
        return "cisplatin"
    if re.search("carboplatinum", value):
        return "carboplatin"
    if re.search("taxotere", value):
        return "docetaxel"
    if re.search("taxol", value) or re.search("abraxane", value):
        return "paclitaxel"
    if re.search("navelbine", value):
        return "vinorelbine"
    if re.search("cetuximab", value):
        return "erbitux"
    if re.search("erlotinib", value):
        return "tarceva"
    if re.search("panitumumab", value):
        return "vectibix"
    if re.search("paraplatin", value):
        return "carboplatin"
    if re.search("vepesid", value):
        return "etoposide"
    if re.search("gemzar", value):
        return "gemcitabine"
    if re.search("ironotecan", value):
        return "irinotecan"
    if re.search("alimta", value):
        return "pemetrexed"
    # for BRCA merge arimidex and anastrozole:
    if re.search("anastrozole", value):
        return "arimidex"
    else:
        return value


drug_DF['pharmaceutical_therapy_drug_name'] = drug_DF[
    'pharmaceutical_therapy_drug_name'].str.lower()
# correct drugnames of all indexes:
drug_DF['pharmaceutical_therapy_drug_name'] = drug_DF[
    'pharmaceutical_therapy_drug_name'].apply(apply_list)
# those nupis are from the drug table!
######################## why dropping them again???
# nupi -> not unique patient index, they are not dropped, they are merged and
# the invoked drugs are sorted, commaseperated and merged into one row
not_uniq_filt = drug_DF['bcr_patient_barcode'].value_counts() > 1
not_uniq_patient_index = not_uniq_filt[not_uniq_filt].index
drug_DF = drug_DF.set_index('bcr_patient_barcode', drop=False)
# out of the multiple drugs, drop duplicates, make a sorted list:

for nupi in not_uniq_patient_index:
    sorted_drug_list = sorted(drug_DF.loc[nupi, :][
            'pharmaceutical_therapy_drug_name'].drop_duplicates(
            ).to_list())
    # correct the drugs within the list:
    # print(f'sorted_drug_list before correction:\n{sorted_drug_list}')
    # for index, value in enumerate(sorted_drug_list):
    #     sorted_drug_list[index] = apply_list(value)
    # print(f'sorted_drug_list after correction:\n{sorted_drug_list}\n')
    # now the duplicates for the nupi can be droped and the remaining
    # value for the drug can be the concatenated sorted, corrected drug
    # string:
    # from: https://stackoverflow.com/questions/
    # drug_DF.loc[nupi, :] = drug_DF.loc[nupi, :][~drug_DF.loc[nupi,
    # :].index.duplicated(keep='first')]
    # -> the "request" on the index asks 'which one is duplicated?', since
    # the first occurence is not 'yet' duplicated, this is False, every
    # followed repetition is a duplication and gives True, the complement
    # of this list accesses the first entry:
    # (Pdb) drug_DF.loc[nupi, :].index.duplicated()
    # array([False,  True,  True,  True,  True,  True,  True])
    # (Pdb) ~drug_DF.loc[nupi, :].index.duplicated()
    # array([ True, False, False, False, False, False, False])
    temp_nupi_row = drug_DF.loc[
        nupi, :][~drug_DF.loc[nupi, :].index.duplicated()]
    temp_nupi_row[
        'pharmaceutical_therapy_drug_name'] = ','.join(sorted_drug_list)
    # now this multiple index can be deleted and then concatenated with the
    # temp row.
    drug_DF.drop(nupi, inplace=True)
    drug_DF = pd.concat([drug_DF, temp_nupi_row])

######################## why dropping them again???
# combined drug therapies are now joined in one row per patient, temp save
# that table:

drug_DF.to_csv(drug_out_path, sep='\t', index=False)
print(f'saved {drug_out_path}')

# why is this needed again? -> because its the only link we have between
# case_id and the filenames... no not within aliq, that can be left begind...
# aliq_mani_drug_DF = pd.merge(aliq_mani_DF, drug_DF, on='bcr_patient_uuid')
aliq_mani_drug_DF = pd.merge(mani_DF, drug_DF, on='bcr_patient_uuid')

aliq_mani_drug_sample_DF = pd.merge(aliq_mani_drug_DF, sample_DF, on='bcr_patient_uuid')
# join everything else on col 'bcr_patient_uuid
# [141 rows x 122 columns]:
complete_DF = aliq_mani_drug_sample_DF.merge(vital_DF, on='bcr_patient_uuid')
# [144 rows x 224 columns]
complete_DF = aliq_mani_drug_sample_DF.merge(patient_DF, on='bcr_patient_uuid')
# lowercase the vital_status and gender infos:
complete_DF['vital_status'] = complete_DF['vital_status'].str.lower()
complete_DF['gender'] = complete_DF['gender'].str.lower()
# in rare cases duplicates arise, they lead to the same filename and can
# be dropped here:
complete_DF.drop_duplicates(subset='bcr_patient_uuid', inplace=True)
# also add the survivaltime, followup and death_days_to into years:
# survivaltime            ║ NaN            ║ death_days_to
# years_to_last_follow_up ║ 3.0219178      ║ last_contact_days_to
# age_at_diagnosis        ║ 64.561643      ║ age_at_diagnosis
# age_at_diagnosis is already given in years

def days_to_years(value):
    try:
        year = float(value) / 365
        return year
    except ValueError:
        return pd.NA

# make years out of last_concact_days_to col:
complete_DF['survivaltime'] = complete_DF['death_days_to'].apply(
    days_to_years)
complete_DF['years_to_last_follow_up'] = complete_DF[
    'last_contact_days_to'].apply(days_to_years)
complete_DF.to_csv(complete_path, sep='\t', index=False)
print(f'saved {complete_path}')

# ############## keep compatibility with previous deseq routines,
# year of birth and year of death are actually not needed and also not
# refered to in the following steps...
# create a merge-table (DF_3t_both_with_DRUG_combi.tsv) in the form of:
# name                    ║ value          ║ equivalent of
#                                         meta_info_druglist_merged

# UUID                    ║ 00276f29-b-... ║ id
# case_id                 ║ 6ff12a54-1-... ║ bcr_patient_uuid
# gender                  ║ female         ║ gender
# vital_status            ║ alive          ║ vital_status
# drugnames               ║ cisplatin      ║ pharmaceutical_
#                                            therapy_drug_name
# survivaltime            ║ NaN            ║ death_days_to
# years_to_last_follow_up ║ 3.0219178      ║ last_contact_days_to
# #### this is omitted   -->>
# year_of_birth           ║ 1946           ║
# year_of_death           ║ NaN            ║
# #### this is omitted  <<--
# age_at_diagnosis        ║ 64.561643      ║ age_at_diagnosis
# PROJECT                 ║ TCGA-CESC      ║ project_id

# TODO integrate that into deseq part:
# this is DESeq2_pipeline specific:
# if workflow_type == 'HTSeq - Counts':
#     complete_DF.rename({'id': 'UUID', 'bcr_patient_uuid': 'case_id',
#                         'pharmaceutical_therapy_drug_name': 'drugnames',
#                         'death_days_to': 'survivaltime',
#                         'last_contact_days_to': 'years_to_last_follow_up',
#                         'project_id': 'PROJECT'}, axis=1, inplace=True)
#     # make years out of day specificatins: -> therefore set NaN correctly.
#     # that means str which cannot be converted to float are NaN
#     # float(complete_DF['death_days_to'].loc[0]) -> 570.0
#     # float(complete_DF['death_days_to'].loc[1]) -> *** ValueError: could
#     # not convert string to float: '[Not Applicable]'

#     def days_to_years(value):
#         try:
#             year = float(value) / 365
#             return year
#         except ValueError:
#             return np.nan

#     # make years out of last_concact_days_to col:
#     complete_DF['survivaltime'] = complete_DF['survivaltime'].apply(
#         days_to_years)
#     complete_DF['years_to_last_follow_up'] = complete_DF[
#         'years_to_last_follow_up'].apply(days_to_years)
#     # save that table with name DF_3t_both_with_DRUG_combi
#     log_path = os.path.join(PROJECT, 'DF_3t_both_with_DRUG_combi.tsv')
#     try:
#         complete_DF.to_csv(os.path.join(OUTPUT_PATH, log_path), sep='\t')
#         logger.info('create_merged_metatable_3:\t{}'.format(
#             os.path.join(log_path)))
#     except Exception as e:
#         print(f'Exception occured: {e}, could not save {log_path}')
#         print('exiting')
#         os._exit(0)
