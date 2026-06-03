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

### 6. Pathway Analysis (Reactome)

**Input:** `Shared_genes_final.xlsx`  
**Output:** Reactome pathway enrichment tables and pathway hierarchy annotations  

Script:

- `5.Pathway_analysis/script6_reactome_pathway_analysis.R`

This module performs pathway-level functional annotation of the identified genes using Reactome-based enrichment analysis. Gene symbols are mapped to Entrez identifiers and analysed using the `ReactomePA` R package. In addition, pathway hierarchy information is retrieved via the Reactome Content Service API to provide higher-level functional context.

The analysis is performed at the single-gene level and results are aggregated to generate a comprehensive mapping of pathway involvement across the final gene set.

---

### 7. Single-Cell Expression Mapping

**Input:** `Shared_genes_final.xlsx`  
**Output:** cell-type expression matrices, tau specificity scores, and cross-organ concordance analysis  

Script:

- `6.Single_cell_expression/script7_cellxgene_expression_mapping.py`

This module maps the expression of the final gene set across human vascular cell populations using the CellxGene Census dataset. Analyses are performed on heart and brain vascular compartments, including endothelial, pericyte, and smooth muscle cell populations.

The workflow computes normalized gene expression, cell-type specificity using the Tau index, and cross-organ concordance based on mean expression profiles. This enables evaluation of tissue- and cell-type-specific expression patterns of the identified genes.

---

### 8. Network Analysis (Cytoscape)

**Input:** `Shared_genes_final.xlsx`  
**Output:** gene interaction network visualizations and Cytoscape session files  

This module performs network-based functional association analysis using Cytoscape (v3.10.3) with the GeneMANIA plugin (v3.5.3).

The network is constructed using the final gene set without the addition of external genes, and network weighting is set to automatic. The resulting network integrates multiple functional association sources, including co-expression, pathway co-membership, and predicted functional relationships.

The network is interpreted as a representation of gene functional relatedness and prioritization rather than evidence of direct mechanistic interaction or causality.

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
