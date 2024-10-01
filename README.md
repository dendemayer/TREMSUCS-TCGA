# TREMSUCS README:  

"TREMSUCS" a tool to choose, harvest and analyse expression and methylation data
of the TCGA-projects for revealing Biomarkers which indicate treatment success.

## got to the documentation:  
[Documentation](https://dendemayer.github.io/TREMSUCS-TCGA/#)  
## an example Report html file can be downloaded here:  
[example Report download link](https://media.githubusercontent.com/media/dendemayer/TREMSUCS-TCGA/main/suppl/report.html?download=true).  
This report file has a size of about 300 MB.  
Due to the large size of the report it is recommend to download it first before
exploration, but a direct link for your browser is given here:  
[direct link for browser](https://www.bioinf.uni-leipzig.de/~gabor/report.html).  

# installing from github.com:
```bash
$ git clone https://github.com/dendemayer/TREMSUCS-TCGA.git
$ cd TREMSUCS-TCGA
$ pip install .
```

# Start the pipeline interactively or via CLI:

- To start the analysis with help of the interactive mode, call the pipeline
  without any argument:  

```bash
$ TREMSUCS
```

- Calling the help or the manual page:  

```bash
$ TREMSUCS --help
$ man TREMSUCS
```

- example configuration with CLI:  

```bash
TREMSUCS -p TCGA-HNSC -p TCGA-CESC -p TCGA-LUSC -d cisplatin -d carboplatin,paclitaxel -d carboplatin -o TreSucM -c 40 -e metilene -t 5 -t 10 -C 8 -C 5 -e DESeq2
```
- content of help page:  

```
Usage: TREMSUCS [OPTIONS]  
  
  "TREMSUCS" a tool to choose, harvest and analyse expression and methylation  
  data of the TCGA-projects for revealing Biomarkers which indicate treatment  
  success predictions.  
  
  Calling the pipeline without any argument starts the interactive mode to  
  help setting all needed parameters for the analysis.  
  
Options:  
  -o, --out_path TEXT    path to save the result files  [default:  
                         /homes/biertruck/gabor/TREMSUCS]  
  -p, --project TEXT     TCGA project(s) to be applied. Any TCGA project can  
                         be chosen, like: -p TCGA-CESC -p TCGA-HNSC ...  
  -d, --drugs TEXT       drug(s), like: -d drug1 -d drug2 or  
                         drugcombination(s), like: -d drug1,drug2  
  -c, --cores INTEGER    number of cores provided to snakemake  [default: 1]  
  -C, --cutoff FLOAT     Cut-off parameter. Enter none, one or several like:
                         -C 5 -C 8
                         
                         You can estimate an appropriate cutoff value by
                         running your analysis wtih default cutoff and
                         checking out the created report html for the survival
                         time distribution. See man TREMSUCS for further
                         clarification of the Cutoff parameter  [default: 0]
  -t, --threshold FLOAT  threshold parameter. Enter none, one or several like:
                         -t 5 -t 10
                         
                         It is advised for the user not to exceed a threshold
                         value of 20 since it is unlikely to gain any
                         significance for the survival analysis with an
                         exaggerated exclusion of patients. See man TREMSUCS
                         for further clarification of the threshold parameter
                         [default: 0]
  -e, --execute TEXT     choose which pipeline shall be executed  [default:  
                         DESeq2, metilene]  
  -N, --dryrun           snakemake dryrun  
  -D, --download         if set, just download raw and meta data for given  
                         projects and analysis types, revise them, link them,  
                         but do not run any analysis  
  -v, --version          printing out version information: Version 1.0  
  --help                 Show this message and exit.  
```
