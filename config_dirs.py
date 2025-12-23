# config_dirs.py
# -------------------------------
# Centralized configuration for directory paths and filenames
# Modify only this file to adapt the pipeline to a different environment
# -------------------------------

# Root directory of the repository
ROOT_DIR = "/path/to/INNOVA_FINAL"

# -------------------------------
# 1.1 Data retrieval
# -------------------------------
# Output of script 1.1 (local CSV)
OUTPUT_1_1_PMIDS = f"{ROOT_DIR}/1.1.Data_retrival/PMIDS_2000_2024.csv"

# -------------------------------
# 1.2 Putting data together
# -------------------------------
# Input of script 1.2 = output of 1.1
INPUT_1_2_PMIDS = OUTPUT_1_1_PMIDS

# Output of script 1.2 = input of OpenAI script
OUTPUT_1_2_OPENAI_INPUT = f"{ROOT_DIR}/2.OpenAI/OpenAI_Input.xlsx"

# -------------------------------
# 2. OpenAI processing
# -------------------------------
# Input Excel file
OPENAI_INPUT = OUTPUT_1_2_OPENAI_INPUT

# Output folder for individual analysis results
OPENAI_ANALYSIS_RESULTS_DIR = f"{ROOT_DIR}/2.OpenAI/analysis_results"

# Full combined output CSV (input of script 4)
OPENAI_FULL_OUTPUT = f"{ROOT_DIR}/2.OpenAI/OpenAI_full_output.csv"

# -------------------------------
# 3. Perplexity analysis
# -------------------------------
# Input of script 4 = output of OpenAI
PERPLEXITY_INPUT = OPENAI_FULL_OUTPUT

# Output of script 4
STANDARDIZED_GENES_OUTPUT = f"{ROOT_DIR}/3.Perplexity/standardized_genes_final.csv"

# -------------------------------
# 4. Cleaning and extracting results (script 5)
# -------------------------------
# Input of script 5 = output of Perplexity
CLEANING_INPUT = STANDARDIZED_GENES_OUTPUT

# Output of script 5
FINAL_OUTPUT = f"{ROOT_DIR}/4.Clean_and_extract_results/Shared_genes_final.xlsx"
