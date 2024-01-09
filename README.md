# quasi-prime-humancasestudy
Repo for human quasi prime case study and manuscript for Mouratidis, Konnaris, Chantzi, and Chan et al. from Dr. Ilias Georgakopolous-Soares Lab at Penn State University.

<p align="center">
<img src="https://github.com/Georgakopoulos-Soares-lab/quasi-prime-humancasestudy/blob/efcd5cd179df945f34051073364aa08c9d4d787a/qp_schematic_dna_FIG1.png?raw=true" width=50% height=50%>
</p>

Data Directory
- hg38_QPs_genes_symbols.txt (Nucleic Quasi-prime gene symbols - Genes that align with Nucleic quasi-prime regions)
- allen_all.rds (Allen Brain Institute - Human M1 Primary Motor Cortex)
- MRCONSO.RRF (UMLS data)
- gnomad.v2.1.1.all_lofs.txt (Gnomad LoF data)
- gnomad.v2.1.1.lof_metrics.by_gene.txt (Gnomad LoF data)
- ENCFF250UJY.bed
- ENCFF250UJY.tsv
- hg38_QPs_coordinates.bed
- hg38_QPs_coordinates.bed_control.bed
- distributions.zip
  
Code:
- qp-singlecell-published.Rmd (R Markdown file for all single cell plots)
- constraintandpLOF.ipynb (Jupyter Notebook file for constraint and pLOF variant analysis plots)
- Regulome_plot.ipynb (Jupyter Notebook file for Regulome analysis plots)
- QP_chipseq_enrichment.ipynb (Jupyter Notebook file for chipseq enrichment analysis plots)
- QP_extraction/generate_test_data.py (Generate sample data for quasi-prime extraction example)
- QP_extraction/quasi_prime_extractor.py (Show example of QP_extraction of a single species or taxonomy)
- tissue_specificity.ipynb (Jupyter Notebook file for quasi-prime gene expression across tissues)
- distributions/plots.ipynb (Jupyter Notebook file to plot enrichment data in distributions.zip)
