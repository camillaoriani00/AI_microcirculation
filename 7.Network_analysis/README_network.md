# Network Analysis

## Overview

Network analysis was conducted using Cytoscape (version 3.10.3) with the GeneMANIA plugin (version 3.5.3).

The analysis was performed on the final gene set identified through the AI-assisted literature mining pipeline. GeneMANIA was configured to use only the submitted genes, without adding additional related genes to the network. Network weighting was left at the default automatic setting provided by the plugin.

## Input

* Final gene list (`Shared_genes_final.xlsx`)

## Software

* Cytoscape v3.10.3
* GeneMANIA plugin v3.5.3

## Parameters

* Query genes: final shared gene set
* Additional genes: 0
* Network weighting: Automatic
* Organism: Homo sapiens
* Default GeneMANIA data sources

## Interpretation

The resulting network integrates multiple sources of functional association, including but not limited to:

* Co-expression
* Pathway co-membership
* Physical interactions
* Genetic interactions
* Predicted functional relationships
* Shared protein domains

The network should be interpreted as a representation of functional relatedness and gene prioritization. Edges do not constitute direct evidence of mechanistic interaction or causality.

## Reproducibility

To reproduce the analysis:

1. Open Cytoscape (v3.10.3 or later).
2. Launch the GeneMANIA plugin.
3. Import the final gene list.
4. Set "Genes to return" to 0.
5. Keep network weighting set to "Automatic".
6. Run the analysis using Homo sapiens as the reference organism.

