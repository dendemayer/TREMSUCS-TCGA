.. toctree::
   :maxdepth: 2
   :caption: Contents:

Documentation: TREMSUCS for TCGA
***************************************

"TREMSUCS" a tool to choose, harvest and analyse expression and methylation data
of the TCGA-projects for revealing Biomarkers which indicate treatment success.

Example report:
---------------

An example report can be downloaded here_.
[https://media.githubusercontent.com/media/dendemayer/TREMSUCS-TCGA/main/suppl/report.html?download=true]

Be aware that this report has a size of about 300 MB.

.. _here: https://media.githubusercontent.com/media/dendemayer/TREMSUCS-TCGA/main/suppl/report.html?download=true

Installing from github.com:
------------------------------------------

.. code-block:: bash

    $ git clone https://github.com/dendemayer/TREMSUCS-TCGA.git
    $ cd TREMSUCS-TCGA
    $ pip install .

To start the analysis with help of the interactive mode, call the pipeline
without any argument:

.. code-block:: bash

   $ TREMSUCS

Calling the help or the manual page: 

.. code-block:: bash

   $ TREMSUCS --help
   $ man TREMSUCS

Help Page of the pipeline:
--------------------------

.. click:: shared.modules.main:call_with_options
   :prog: TREMSUCS

Short tutorial:
---------------
Usage of the interactive mode:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following example composition of projects, drugs and parameters creates the
configuration given in the example report here_.

The same configuration can be applied by issuing the following command (the
number of cores hereby can be adjusted and would also give the same results):

.. code-block:: bash

   $ TREMSUCS -p TCGA-CESC -p TCGA-HNSC -p TCGA-LUSC -d cisplatin -d carboplatin,paclitaxel \
   -d carboplatin -o /scr/TREMSUCS_out -c 40 -t 5 -t 10 -t 20 -C 5 -C 8

Calling the pipeline without any argument starts the interactive mode:

.. code-block:: text


   $ TREMSUCS

    OUTPUT_PATH:             /homes/biertruck/gabor/TREMSUCS
    SCRIPT_PATH:             /homes/biertruck/gabor/phd/test_git_doc/TREMSUCS/src/shared/modules
    PIPELINES executed:      ['DESeq2', 'metilene']

    which projects do you want to include in your analysis:

     0:     TCGA-CESC           Cervical Squamous Cell Carcinoma and Endocervical Adenocarcinoma      
     1:     TCGA-HNSC           Head and Neck Squamous Cell Carcinoma                                 
     2:     TCGA-LUSC           Lung Squamous Cell Carcinoma                                          
     3:     TCGA-ESCA           Esophageal Carcinoma                                                  
     4:     TCGA-BRCA           Breast Invasive Carcinoma                                             
     5:     TCGA-GBM            Glioblastoma Multiforme                                               
     6:     TCGA-OV             Ovarian Serous Cystadenocarcinaoma                                    
     7:     TCGA-LUAD           Lung Adenocarcinoma                                                   
     8:     TCGA-UCEC           Uterine Corpus Endometrial Carinoma                                   
     9:     TCGA-KIRC           kindney renal clear cell carcinoma                                    
    10:     TCGA-LGG            brain lower grade glioma                                              
    11:     TCGA-THCA           thyroid carcinoma                                                     
    12:     TCGA-PRAD           prostate adenocarcinoma                                               
    13:     TCGA-SKCM           skin cutaneous melanoma                                               
    14:     TCGA-COAD           colon adenocarcinoma                                                  
    15:     TCGA-STAD           stomach adenocarcinoma                                                
    16:     TCGA-BLCA           bladder urothelial carcinoma                                          
    17:     TCGA-LIHC           liver hepatocellular carcinoma                                        
    18:     TCGA-KIRP           kidney renal papillary cell carcinoma                                 
    19:     TCGA-SARC           sarcoma                                                               
    20:     TCGA-PAAD           pancreatic adenocarcinoma                                             
    21:     TCGA-PCPG           pheochromocytoma and paraganglioma                                    
    22:     TCGA-READ           rectum adenocarcinoma                                                 
    23:     TCGA-TGCT           testicular germcelltumors                                             
    24:     TCGA-THYM           thymoma                                                               
    25:     TCGA-KICH           kidney chromophobe                                                    
    26:     TCGA-ACC            adrenochordical carcinoma                                             
    27:     TCGA-MESO           mesothelioma                                                          
    28:     TCGA-UVM            uveal melanoma                                                        
    29:     TCGA-DLBC           lymphoid neoplasm diffuse large b-cell lymphoma                       
    30:     TCGA-UCS            uterine carcinoma                                                     
    31:     TCGA-CHOL           cholangiocarcinoma                                                    
    enter your choices one by one, when you are done, simply press "Enter": 

As suggested, you can now, one by one include the projects you are interested in.
A default OUTPUT_PATH is also already given together with the default analysis
types "DESeq" and "metilene". Those defaults can also be adjusted in next steps
with help of the interactive mode.

To recreate the example set, the first three projects have to be selected,
afterwards the following prompt is given:

.. code-block:: text


    you choose:
    PROJECTS:        ['TCGA-CESC', 'TCGA-HNSC', 'TCGA-LUSC']

    which therapy approach do you want to include in your analysis:

     0: cisplatin                                TCGA-CESC: 103 TCGA-HNSC: 64 TCGA-LUSC: 1         
     1: carboplatin,paclitaxel                   TCGA-CESC: 5 TCGA-HNSC: 26 TCGA-LUSC: 14          
     2: 5-fluorouracil,cisplatin                 TCGA-CESC: 5 TCGA-HNSC: 2 TCGA-LUSC: 0            
     3: carboplatin                              TCGA-CESC: 3 TCGA-HNSC: 6 TCGA-LUSC: 3            
     4: carboplatin,cisplatin,paclitaxel         TCGA-CESC: 3 TCGA-HNSC: 0 TCGA-LUSC: 1            
     5: cisplatin,gemcitabine                    TCGA-CESC: 3 TCGA-HNSC: 0 TCGA-LUSC: 9            
     6: paclitaxel                               TCGA-CESC: 2 TCGA-HNSC: 1 TCGA-LUSC: 0            
     7: erbitux                                  TCGA-CESC: 1 TCGA-HNSC: 9 TCGA-LUSC: 0            
     8: cisplatin,vectibix                       TCGA-CESC: 0 TCGA-HNSC: 5 TCGA-LUSC: 0            
     9: carboplatin,erbitux,paclitaxel           TCGA-CESC: 0 TCGA-HNSC: 4 TCGA-LUSC: 0            
    10: cisplatin,erbitux                        TCGA-CESC: 0 TCGA-HNSC: 3 TCGA-LUSC: 0            
    11: carboplatin,cisplatin,erbitux,paclitaxel TCGA-CESC: 0 TCGA-HNSC: 3 TCGA-LUSC: 0            
    12: carboplatin,cisplatin                    TCGA-CESC: 0 TCGA-HNSC: 2 TCGA-LUSC: 0            
    13: docetaxel,erbitux                        TCGA-CESC: 0 TCGA-HNSC: 2 TCGA-LUSC: 0            
    14: cisplatin,docetaxel                      TCGA-CESC: 0 TCGA-HNSC: 1 TCGA-LUSC: 10           
    15: carboplatin,docetaxel                    TCGA-CESC: 0 TCGA-HNSC: 1 TCGA-LUSC: 3            
    16: cisplatin,vinorelbine                    TCGA-CESC: 0 TCGA-HNSC: 0 TCGA-LUSC: 21           
    17: carboplatin,vinorelbine                  TCGA-CESC: 0 TCGA-HNSC: 0 TCGA-LUSC: 8            
    18: cisplatin,etoposide                      TCGA-CESC: 0 TCGA-HNSC: 0 TCGA-LUSC: 7            
    19: carboplatin,gemcitabine                  TCGA-CESC: 0 TCGA-HNSC: 0 TCGA-LUSC: 5            
    20: cisplatin,pemetrexed                     TCGA-CESC: 0 TCGA-HNSC: 0 TCGA-LUSC: 3            
    21: cisplatin,docetaxel,gemcitabine          TCGA-CESC: 0 TCGA-HNSC: 0 TCGA-LUSC: 2            
    22: carboplatin,gemcitabine,paclitaxel       TCGA-CESC: 0 TCGA-HNSC: 0 TCGA-LUSC: 2            
    23: carboplatin,cisplatin,vinorelbine        TCGA-CESC: 0 TCGA-HNSC: 0 TCGA-LUSC: 2            
    24: carboplatin,docetaxel,gemcitabine        TCGA-CESC: 0 TCGA-HNSC: 0 TCGA-LUSC: 2            
    25: carboplatin,docetaxel,paclitaxel         TCGA-CESC: 0 TCGA-HNSC: 0 TCGA-LUSC: 2            
    26: gemcitabine                              TCGA-CESC: 0 TCGA-HNSC: 0 TCGA-LUSC: 2            

    enter your choices one by one, when you are done, simply press "Enter": 

Here are therapies listed where the maximum of a row is greater than 1. We
apply row 0, 1 and 3 to include cisplatin, the combination of carboplatin and
paclitaxel and cases which got solely treated with carboplatin. In the
following, every other parameter is requested. With the next prompt, the
default OUTPUT_PATH can be confirmed or replaced:

.. code-block:: text
    
    do you want to keep the default OUTPUT_PATH of:                                  
    /homes/biertruck/gabor/TREMSUCS                                                  
    if so, press ENTER, if not, enter your custom output path:                       
                                                                                 
In this example, we confirm the suggested OUTPUT_PATH and are asked to confirm
or set the number of cores which shall be invoked into the analyses:

.. code-block:: text


    do you want to keep the default number of cores invoked of 1?                    
    if so, press ENTER, if not, enter the number of cores:                           
    40                                                                               

We set the cores to 40 and then can decide which analysis approaches shall be
triggered, per default, DESeq2 and metilene based biomarker predictions are
produced:

.. code-block:: text


    which pipeline do you want to include into your analysis                         
    press ENTER if DESeq2 and metilene (default) or                                  
    1 for DESeq2 or                                                                  
    2 for metilene                                                                   
                                                                                 
We confirm the default of those two analyses and can set the cutoff values, if
we want to add those at all:

.. code-block:: text


    do you want to add one or multiple cutoffs?                                      
    it is recommend to choose cutoff values between 5 and 10 years                   
    if not, just press ENTER, if so enter the coutoffs one by one:                   
    5                                                                                
    8                                                                                
                                                                                 
Like the example set, we add here a cutoff of 5 and 8. Then the thresholds are
requested:

.. code-block:: text


    do you want to add one or multiple thresholds?                                   
    it is recommend to choose threshold values which do not exceed a value of 50     
    if not, just press ENTER, if so enter the thresholds one by one:                 
    5                                                                                
    10                                                                               
    20                                                                               

We apply thresholds of 5, 10 and 20. All mandatory and optional parameters are
set with that and are finally listed before the whole approach is started:

.. code-block:: text
                                                                                 

    OUTPUT_PATH:             /homes/biertruck/gabor/TREMSUCS                         
    PROJECT:                 ['TCGA-CESC', 'TCGA-HNSC', 'TCGA-LUSC']                 
    DRUGS:                   ['carboplatin', 'carboplatin,paclitaxel', 'cisplatin']  
    pipelines executed:      ['DESeq2', 'metilene']                                  
    cores:                  40                                                       
    cutoff:                 [0, 5, 8]                                                
    threshold:              [0, 5, 10, 20]                                           
    press ENTER to start or q to quit:                                               

If something went wrong, you can quit now and start over, or of course start the analysis.

The cutoff and threshold parameter:
-----------------------------------
Cutoff:
^^^^^^^

The cutoff parameter can be used to replace the vital status classification
with a classification based on a minimum survival time.  If the parameter is
set, patients are assigned to a group depending on whether or not they survived
longer then the specified value.  In figure 1 an example is given for patients
out of CESC, HNSC and LUSC without any limitation to treatment. With a cutoff
of 8 years, 3 dead patients are grouped with the alive cohort (Figure 2).
Applying a cutoff of 5 groups an additional 7 dead cases to the alive cohort
(Figure 3). This parameter is applied before the analysis steps. It is possible
to apply multiple cutoff values to one run.
The alteration of the survival data of just a few patients can have a
noticeable impact on the overall outcomes, but it should not exceed the maximum
value of the survivaltime of the dead patients cohort, since then no change
would be propagated. To figure out an appropriate custom value, 
you can first run the analysis with the default cutoff and refer to the
created report. Within the patient_overview section, the survival data of
the given cohort is shown. On the basis on the data plotted there, a second run
can be started with a custom cutoff of interest. Already created results will
not be overwritten but incorporated with the new ones based on the chosen
cutoff. The final ranking gives then the same aggregation as if both, the
default and the custom cutoff would have been started together, since the
default is always calculated and incorporated within the analysis.
The custom cutoff should also make medically sense, e.g., stating that an
survivaltime of one year shall be categorized as treatment success makes little
sense and would not enhance the significance of the final results.

.. only:: latex

    .. figure:: _images/cutoff_default.pdf
        :scale: 80 %
        :alt: Default Cutoff 0

        Dead and alive grouping without a cutoff (default).

    .. figure:: _images/cutoff_with_8.pdf
        :scale: 80 %
        :alt: Default Cutoff 8

        Dead and alive grouping with a cutoff of 8.

    .. figure:: _images/cutoff_with_5.pdf
        :scale: 80 %
        :alt: Default Cutoff 5

        Dead and alive grouping without a of 5.

.. only:: html

    .. figure:: _images/cutoff_default.svg
        :alt: Default Cutoff 0

        Figure 1: Dead and alive grouping without a cutoff (default).

    .. figure:: _images/cutoff_with_8.svg
        :alt: Default Cutoff 8

        Figure 2: Dead and alive grouping with a cutoff of 8.

    .. figure:: _images/cutoff_with_5.svg
        :alt: Default Cutoff 5

        Figure 3: Dead and alive grouping without a of 5.

Threshold:
^^^^^^^^^^

The threshold parameter facilitates a modulation in the validation steps.
Each previously identified marker, either a differentially methylated
position or a differentially expressed gene of each patient, is grouped
into the UP or DOWN regulated set depending on the mean of medians of all
values. In the following, the Kaplan Meier estimations for each of these
two groups are calculated. Incorporating values close to the mean of
medians might be detrimental to the significance of the survival
analyses. With the threshold, an upper and lower bound around the mean of
medians is calculated (figure 4) and patient-data between those boundaries is
excluded from the survival analysis. Here, the threshold gives the
distance of the bounds from the mean of medians in percent of the mean of
medians.

It is advised for the user not to exceed a threshold value of 20
since it is unlikely to gain any significance for the survival analysis with
an exaggerated exclusion of patients.

.. only:: latex

    .. figure:: _images/standalone_subfigure6-crop.pdf
        :scale: 80 %
        :alt: threshold

        Threshold example for ENSG00000204187. The panels on the left side
        show the exclusion of patients which are linked to the data in between
        the threshold bounds. On the right side the belonging Kaplan Meier plot
        is shown. 

.. only:: html

    .. figure:: _images/standalone_subfigure6-crop.svg
        :alt: threshold
        :scale: 200 %

        Figure 4: 
        Threshold example for ENSG00000204187. The panels on the left side
        show the exclusion of patients which are linked to the data in between
        the threshold bounds. On the right side the belonging Kaplan Meier plot
        is shown. 

In figure 5, the survival p-values of the 10 most
significant genes for patients from the TCGA-CESC cohort with the
therapeutic combination of carboplatin, carboplatin and paclitaxel
(combined) and cisplatin are shown. With increasing threshold,
incrementally improvement of the p-value for ENSG00000204187 (emphasized in
red) is visible together with a higher difference of the life expectancies.
Increasing the threshold will lower the size of the data base for p-value
estimation, which can also result in increasing p-values. In figure
5, an example is the gene ENSG00000204832
emphasized in green.

.. only:: latex

    .. figure:: _images/standalone_subfigure7-crop.pdf
        :scale: 80 %
        :alt: threshold

        Survival p-values and mean life differences for the first 10
        most significant genes found by DESeq2, gathered from base plots, with
        a cutoff of 0. Succession of ENSGs is genomic coordinate wise.  

.. only:: html

    .. figure:: _images/standalone_subfigure7-crop.svg
        :alt: threshold
        :scale: 160 %

        Figure 5: Survival p-values and mean life differences for the first 10
        most significant genes found by DESeq2, gathered from base plots, with
        a cutoff of 0. Succession of ENSGs is genomic coordinate wise.  


