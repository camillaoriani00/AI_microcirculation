# AI Microcirculation Pipeline

This repository contains a pipeline for extracting and standardizing associations between genes/variables and vascular diseases from PubMed abstracts. It uses OpenAI for text analysis, intermediate processing, Perplexity scoring, and result cleaning.

The pipeline is organized in sequential modules implemented as Jupyter notebooks to ensure reproducibility and transparency for academic research.

---

## Pipeline Structure

### 1. 1.1 Data Retrieval
**Input:** online data sources  
**Output:** CSV file with PMIDs for analysis  
Script:  
- `1.1.Data_retrival/script1_fetch_records.ipynb`

---

### 2. 1.2 Putting Data Together
**Input:** output from `script1_fetch_records.ipynb`  
**Output:** `OpenAI_Input.xlsx`, ready for OpenAI analysis  
Script:  
- `1.2.Putting_data_together/script2_put_data_together.ipynb`

---

### 3. 2.OpenAI
**Input:** `OpenAI_Input.xlsx`  
**Output:** aggregated analysis in `OpenAI_full_output.csv`  
Script:  
- `2.OpenAI/script3_openAI_run_batches.ipynb`

This module uses OpenAI GPT-4 to analyze abstracts and extract variables/genes associated with vascular diseases.  

---

### 4. 3.Perplexity
**Input:** `OpenAI_full_output.csv`  
**Output:** `standardized_genes_final.csv` with scoring and normalization  
Script:  
- `3.Perplexity/script4_perplexity.ipynb`

---

### 5. 4.Clean and Extract Results
**Input:** `standardized_genes_final.csv`  
**Output:** final cleaned results for downstream analysis  
Script:  
- `4.Clean_and_extract_results/script5_clean_and_extract_genes.ipynb`

---

## Requirements and Setup

### Python / Conda Environment

Use the provided `environment.yml` file to recreate the environment:

```bash
conda env create -f env/environment.yml
conda activate innova_env


## Configuration of Directories

All file paths and directories used by the pipeline are managed in a single configuration file:

- `config_dirs.py`

Users should edit only this file to set their local paths for inputs and outputs.  
Each script reads the paths from `config_dirs.py`, so the pipeline can be executed without modifying the notebooks themselves.
