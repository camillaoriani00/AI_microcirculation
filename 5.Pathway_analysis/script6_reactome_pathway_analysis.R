# ==========================================================
# Reactome pathway analysis
# Input:
# Shared_genes_final.xlsx
# Output:
# Reactome_pathways.xlsx
# Reactome_pathways_hierarchy.xlsx
# ==========================================================

library(readxl)
library(writexl)
library(dplyr)
library(ReactomePA)
library(AnnotationDbi)
library(org.Hs.eg.db)
library(httr)
library(jsonlite)

# ----------------------------------------------------------
# Configuration
# ----------------------------------------------------------

INPUT_FILE <- "Shared_genes_final.xlsx"
OUTPUT_PATHWAYS <- "Reactome_pathways.xlsx"
OUTPUT_HIERARCHY <- "Reactome_pathways_hierarchy.xlsx"

# ----------------------------------------------------------
# Load genes
# ----------------------------------------------------------

genes_df <- read_excel(INPUT_FILE)
# expected column containing gene symbols
gene_symbols <- unique(na.omit(genes_df$Gene))

# ----------------------------------------------------------
# Convert SYMBOL -> ENTREZ
# ----------------------------------------------------------

gene_ids <- AnnotationDbi::select(
org.Hs.eg.db,
keys = gene_symbols,
keytype = "SYMBOL",
columns = c("ENTREZID")
)

gene_ids <- gene_ids[!is.na(gene_ids$ENTREZID), ]

# ----------------------------------------------------------
# Single-gene Reactome annotation
# ----------------------------------------------------------

combined_results <- data.frame()

for (i in seq_len(nrow(gene_ids))) {
    entrez_id <- gene_ids$ENTREZID[i]
    gene_symbol <- gene_ids$SYMBOL[i]

    cat("Processing:", gene_symbol, "\n")

    result <- tryCatch(
        enrichPathway(
            gene = entrez_id,
            organism = "human"
        ),
        error = function(e) NULL
    )

    if (!is.null(result) && nrow(as.data.frame(result)) > 0) {

        tmp <- as.data.frame(result)

        tmp$GeneSymbol <- gene_symbol

        combined_results <- bind_rows(
            combined_results, tmp)
    }
}

write_xlsx(combined_results, OUTPUT_PATHWAYS)

# ----------------------------------------------------------
# Reactome hierarchy retrieval
# ----------------------------------------------------------

get_pathway_hierarchy <- function(pathway_id){
    if(is.na(pathway_id)) return(NA)

    url <- paste0(
        "https://reactome.org/ContentService/data/event/",
        pathway_id,
        "/ancestors"
    )

    response <- tryCatch(
        GET(url),
        error = function(e) NULL
    )

    if(is.null(response)) return(NA)

    if(status_code(response) != 200) return(NA)

    json_str <- content(
        response,
        "text",
        encoding = "UTF-8"
    )

    ancestors <- fromJSON(json_str)

    if(is.null(ancestors))
        return(NA)

    if(
        is.list(ancestors) &&
        length(ancestors) == 1
    ){
        ancestors <- ancestors[[1]]
    }

    if(
        "displayName" %in% names(ancestors)
    ){
        return(
            paste(
                ancestors$displayName,
                collapse = " > "
            )
        )
    }

    return(NA)
}

combined_results$Hierarchy <- sapply(
combined_results$ID,
get_pathway_hierarchy
)

write_xlsx(
combined_results,
OUTPUT_HIERARCHY
)

cat("\nAnalysis completed.\n")
