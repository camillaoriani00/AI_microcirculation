"""
Single-cell expression mapping

Input:
Shared_genes_final.xlsx

Output:
heart_mean_expression.csv
brain_mean_expression.csv
tau_index.csv
cross_organ_concordance.csv
"""

import pandas as pd
import numpy as np
import scanpy as sc
import cellxgene_census
from scipy.stats import spearmanr

# ----------------------------------------------------------
# Configuration
# ----------------------------------------------------------

INPUT_FILE = "Shared_genes_final.xlsx"

HEART_TISSUES = [
"heart",
"heart left ventricle",
"heart right ventricle"
]

BRAIN_TISSUES = [
"brain",
"cerebral cortex",
"hippocampus",
"cerebellum"
]

# ----------------------------------------------------------
# Load genes
# ----------------------------------------------------------

genes_df = pd.read_excel(INPUT_FILE)

GENES = (
genes_df["Gene"]
.dropna()
.unique()
.tolist()
)

# ----------------------------------------------------------
# Census query
# ----------------------------------------------------------

def query_organ(census, tissues, label):

```
tissue_filter = " or ".join(
    [
        f"tissue_general == '{t}'"
        for t in tissues
    ]
)

obs_filter = (
    "organism_ontology_term_id == "
    "'NCBITaxon:9606' and "
    f"({tissue_filter})"
)

adata = cellxgene_census.get_anndata(
    census=census,
    organism="Homo sapiens",
    obs_value_filter=obs_filter,
    var_value_filter=f"feature_name in {GENES}"
)

vascular_mask = (
    adata.obs["cell_type"]
    .str.lower()
    .str.contains(
        "endothelial|pericyte|smooth muscle",
        na=False
    )
)

adata = adata[vascular_mask].copy()

adata.obs["organ"] = label

return adata
```

# ----------------------------------------------------------
# Open Census
# ----------------------------------------------------------

census = cellxgene_census.open_soma(
census_version="stable"
)

heart = query_organ(
census,
HEART_TISSUES,
"heart"
)

brain = query_organ(
census,
BRAIN_TISSUES,
"brain"
)

census.close()

# ----------------------------------------------------------
# Normalization
# ----------------------------------------------------------

for adata in [heart, brain]:

```
sc.pp.normalize_total(
    adata,
    target_sum=1e4
)

sc.pp.log1p(adata)
```

# ----------------------------------------------------------
# Mean expression
# ----------------------------------------------------------

def mean_expression(adata):

```
expr = pd.DataFrame(
    adata.X.toarray(),
    columns=adata.var["feature_name"]
)

expr["cell_type"] = (
    adata.obs["cell_type"].values
)

return (
    expr.groupby("cell_type")
    .mean()
)
```

heart_mean = mean_expression(heart)

brain_mean = mean_expression(brain)

heart_mean.to_csv(
"heart_mean_expression.csv"
)

brain_mean.to_csv(
"brain_mean_expression.csv"
)

# ----------------------------------------------------------
# Tau specificity
# ----------------------------------------------------------

def tau_index(df):

```
n = df.shape[0]

xhat = (
    df /
    df.max(axis=0)
)

tau = (
    (1 - xhat)
    .sum(axis=0)
    /(n-1)
)

return tau
```

tau_df = pd.DataFrame({
"tau_heart":
tau_index(heart_mean),
"tau_brain":
tau_index(brain_mean)
})

tau_df.to_csv(
"tau_index.csv"
)

# ----------------------------------------------------------
# Concordance
# ----------------------------------------------------------

common_genes = (
heart_mean.columns
.intersection(
brain_mean.columns
)
)


heart_avg = (
heart_mean[common_genes]
.mean(axis=0)
)

brain_avg = (
brain_mean[common_genes]
.mean(axis=0)
)

rho, pval = spearmanr(
heart_avg,
brain_avg
)

concordance = pd.DataFrame({
"gene": common_genes,
"heart_expression":
heart_avg.values,
"brain_expression":
brain_avg.values
})

concordance.to_csv(
"cross_organ_concordance.csv",
index=False
)

print(
f"Spearman rho={rho:.3f}, "
f"p={pval:.4g}"
)

print("Analysis completed.")
