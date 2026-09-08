# -*- coding: utf-8 -*-
"""Generate _data/publications.yml and _data/pubtags.yml.

This file is the source of truth for the publications page. Edit the entries
here and rerun; never hand-edit the generated YAML, or the next run will
silently revert it.

    python tools/build-publications.py .          (from the repo root)

Then check `git diff _data/publications.yml` to confirm only what you intended
changed.

Conventions
    authors   * corresponding, &dagger; co-first, lab members in <strong>.
              The PI token is {Z}; other members are bolded automatically from
              the LAB set below, so add new members there.
    status    published | inpress | preprint | review
    methods   keys from METHOD_TAGS; bio from BIO_TAGS

CrossRef gives citations and author order but records neither co-first nor
corresponding authorship - read the publisher's page for those, or ask the PI.
"""
import io, os, sys

Z = "<strong>Zhang NR</strong>"

# ---------------------------------------------------------------- tag registry
# key, label, colour
METHOD_TAGS = [
    ("sc",  "Single Cell",                   "#dceafa", "#7aa8d8"),
    ("sp",  "Spatial Omics",                 "#d5f0e2", "#79c4a0"),
    ("int", "Integration",                   "#e6ddf7", "#a48fd4"),
    ("bc",  "Batch Correction",              "#dee0f7", "#8f95d6"),
    ("di",  "Denoising/Imputation",          "#d3eff2", "#77c3cc"),
    ("dc",  "Deconvolution",                 "#d6f2ea", "#77cbb6"),
    ("lr",  "Long Read",                     "#e0f2d3", "#9ecb78"),
    ("cn",  "DNA Copy Number",               "#fbe6cd", "#dfa960"),
    ("te",  "Tumor Evolution",               "#fbdcd2", "#e09b83"),
    ("lt",  "Lineage Tracing",               "#fbefc9", "#dcc164"),
    ("gr",  "Gene Regulation",               "#f7dcf0", "#d491c5"),
    ("de",  "Differential Expression",       "#d2f0ec", "#74c8bd"),
    ("pa",  "Pathway Analysis",              "#e9f0cc", "#bcc86c"),
    ("ai",  "AI and Deep Learning",          "#eeddf7", "#bb8fd6"),
    ("vd",  "Variant Detection",             "#f7e2da", "#d9a48f"),
    ("cp",  "Change-Point & Scan Statistics","#fbdde6", "#dd8fa8"),
    ("np",  "Nonparametric Methods",         "#f7dde9", "#d78fae"),
    ("ci",  "Causal Inference",              "#fadadd", "#dd8f96"),
]

BIO_TAGS = [
    ("can", "Cancer",             "#b3252c"),
    ("imm", "Immunology",         "#1a6fb0"),
    ("kid", "Kidney",             "#0e7c66"),
    ("age", "Aging",              "#7d3fb5"),
    ("neu", "Neuroscience",       "#c2620c"),
    ("cvd", "Cardiovascular",     "#a81a6d"),
    ("inf", "Infectious Disease", "#4f7d14"),
    ("gi",  "Gastrointestinal",   "#3b4bad"),
]

SOFTWARE = {
    "NicheDE":      "https://github.com/kaishumason/NicheDE",
    "CellANOVA":    "https://github.com/Janezjz/cellanova",
    "Alleloscope":  "https://github.com/seasoncloud/Alleloscope",
    "Clonalscope":  "https://github.com/seasoncloud/Clonalscope",
    "cTP-net":      "https://github.com/zhouzilu/cTPnet",
    "DENDRO":       "https://github.com/zhouzilu/DENDRO",
    "DESCEND":      "https://github.com/jingshuw/descend",
    "MuSiC":        "https://github.com/xuranw/MuSiC",
    "SAVER":        "https://github.com/mohuangx/SAVER",
    "SAVER-X":      "https://github.com/jingshuw/SAVERX",
    "SCALE":        "https://github.com/yuchaojiang/SCALE",
    "TASC":         "https://github.com/scrna-seq/TASC",
    "Canopy":       "https://cran.r-project.org/web/packages/Canopy/",
    "FALCON":       "https://cran.r-project.org/web/packages/falcon/index.html",
    "FALCON-X":     "https://cran.r-project.org/web/packages/falconx/index.html",
    "CODEX2":       "https://github.com/yuchaojiang/CODEX2",
    "iCNV":         "https://github.com/zhouzilu/iCNV",
    "MARATHON":     "https://github.com/yuchaojiang/MARATHON",
    "SWAN":         "https://bitbucket.org/charade/swan/overview",
    "gCat":         "https://cran.r-project.org/web/packages/gCat/index.html",
    "gSeg":         "https://cran.r-project.org/web/packages/gSeg/index.html",
    "leapp":        "https://cran.r-project.org/web/packages/leapp/index.html",
    "Semblance":    "https://cran.r-project.org/web/packages/Semblance/index.html",
    "seqCBS":       "https://cran.r-project.org/web/packages/seqCBS/index.html",
    "MaxFuse":      "https://github.com/shuxiaoc/maxfuse",
    "Tilted-CCA":   "https://github.com/linnykos/tiltedCCA",
    "TRIPOD":       "https://github.com/yuchaojiang/TRIPOD",
    "SCPA":         "https://github.com/jackbibby1/SCPA",
    "multiomeFate": "https://github.com/nancyrzhanglab/multiomeFate",
    "Longcell":     "https://github.com/yuntianf/Longcell",
    "SpotGLM":      "https://github.com/kaishumason/SpotGLM",
    "SPARROW":      "https://github.com/kaishumason/SPARROW",
    # located by reading each paper's own Code Availability section
    "CoPro":        "https://github.com/Zhen-Miao/CoPro",
    "Clonotrace":   "https://github.com/yuntianf/Clonotrace",
    "TraceBind":    "https://github.com/lyx-lin/TraceBind",
    "CellSpectra":  "https://github.com/kloetzerka/CellSpectra",
    "miniQuant":    "https://github.com/Augroup/miniQuant",
    "scmtVT":       "https://github.com/jiazhen-rong/scmtVT",
    "SUMMIT":       "https://github.com/jiazhen-rong/SUMMIT",
    "CACTI":        "https://github.com/kaishumason/CACTI_Proximity_Test",
    "GRAPPLE":      "https://github.com/jingshuw/GRAPPLE",
    "SVEngine":     "https://bitbucket.org/charade/svengine",
    "CLOSE":        "https://github.com/xfwang/CLOSE",
    "DBiT-plus":    "https://github.com/Janezjz/DBiT-plus",
    "Transcriptional Dyscoordination":
                    "https://github.com/EddieYang1222/transcriptional-dyscoordination",
}

# ------------------------------------------------------------------- the works
# (authors, year, title, venue, detail, doi, preprint_doi, status, software, methods, bio)
# status: "published" | "preprint" | "review"
P = []
def add(authors, year, title, venue, detail, doi, pre, status, sw, methods, bio):
    P.append(dict(authors=authors, year=year, title=title, venue=venue, detail=detail,
                  doi=doi, preprint=pre, status=status, software=sw,
                  methods=methods, bio=bio))

# ---- in review / preprint -------------------------------------------------
add(f"Mason K&dagger;, Jiang Y&dagger;, Kl&#246;tzer KA, {Z}*", 2025,
    "Ultra-scalable differential testing for spatial omics",
    "Nature Biotechnology", "(in press)", None, None, "inpress", ["SpotGLM","SPARROW"],
    ["sp","de","sc"], [])

add(f"Miao Z, Qu Y, Huang S, Laux L, Peters S, Aristel A, Zhang Z, {Z}*", 2026,
    "Dissecting the coordinated progression of cell states in spatial transcriptomics with CoPro",
    "bioRxiv", "", None, "10.64898/2026.04.17.719309", "preprint", ["CoPro"],
    ["sp","sc","pa"], [])

add(f"Fu Y, Mathew D, Wang M, Chen XE, Lin KZ, Schaff D, Shaffer SM, Pardoll DM, Jackson C, {Z}*", 2025,
    "Deciphering cell fate and clonal dynamics via integrative single-cell lineage modeling",
    "bioRxiv", "", None, "10.1101/2025.09.01.673503", "preprint", ["multiomeFate"],
    ["sc","lt","int"], ["can"])

add(f"Yang Y, Hess PR, Huang S, Teneche MG, Wang H, Miller KN, Davis AE, Miciano C, Li KY, Mamde S, Yip K, Ren B, Yang Q, Smoot E, Wang A, Johnson B, Wilson P, Adams PD, {Z}*", 2026,
    "A measure of transcriptional dyscoordination for quantifying aging in single cells",
    "bioRxiv", "", None, "10.64898/2026.01.24.701460", "preprint", ["Transcriptional Dyscoordination"],
    ["sc","np"], ["age"])

add(f"Bracht SA, Rong J, Gier RA, DeMarshall M, Golden H, Dhakal D, {Z}*, Shaffer SM*", 2025,
    "Mitochondrial clone tracing within spatially intact human tissues",
    "bioRxiv", "", None, "10.1101/2025.07.11.664452", "preprint", ["SUMMIT"],
    ["sp","lt","sc"], ["gi"])

add(f"Wang M, Fu Y, Bom S, Ning Y, Matthews D, Zhang M, Lucas CH, Choi J, {Z}, Jackson CM*", 2025,
    "Dual checkpoint blockade of glioblastoma with anti-PD-1 and anti-LAG-3 promotes expansion of tumor-reactive T cell clones along a unique pathway of differentiation",
    "bioRxiv", "", None, "10.1101/2025.09.06.674490", "preprint", ["Clonotrace"],
    ["sc","lt"], ["can","imm","neu"])

add(f"Qiu J, Ye D, Chen XE, Dangle N, Yoshor B, Zhang T, Shao Y, {Z}, Minn AJ*", 2024,
    "Targeting interferon-driven inflammatory memory prevents epigenetic evolution of cancer immunotherapy resistance",
    "bioRxiv", "", None, "10.1101/2024.08.13.607862", "preprint", [],
    ["sc","gr"], ["can","imm"])

add(f"Bartolo L, Afroze S, Lin Y, Ansari A, Pan Y-G, Liu C, {Z}, Naji A, Su LF*", 2025,
    "Intestinal immune dysregulation fuels islet autoimmunity in type 1 diabetes",
    "In review", "", None, None, "review", [],
    ["sc"], ["imm","gi"])

add(f"Chen XE&dagger;, Lin KZ&dagger;, Schaff D&dagger;, Vander Velde R, Cote C, Huang S, Minn AJ, Shaffer SM*, {Z}*", 2025,
    "Temporal and clonal resolution of cellular evolution under stress",
    "In review", "", None, None, "review", [],
    ["sc","lt","te"], ["can"])

# ---- 2026 ------------------------------------------------------------------
add(f"Enninful A&dagger;, Zhang Z&dagger;, Klymyshyn D, Ingalls M, Yang M, Zong H, &hellip;, {Z}, &hellip;, Xu ML*, Ma Z*, Fan R*", 2026,
    "Integration of imaging-based and sequencing-based spatial omics mapping on the same tissue section via DBiTplus",
    "Nature Methods", "23, 1827&ndash;1839", "10.1038/s41592-025-02948-0",
    "10.1101/2024.11.07.622523", "published", ["DBiT-plus"], ["sp","int","sc"], [])

add(f"Schaff DL, White PE, Cote CJ, Watterson GE, Lin KZ, Fasse AJ, {Z}, Shaffer SM*", 2026,
    "Pre-existing cell states predict resistance to multiple treatments",
    "Cell Genomics", "6, 101191", "10.1016/j.xgen.2026.101191", None, "published", [],
    ["sc","lt","te"], ["can"])

add(f"Lin Y, Wang H, Wilson PC*, {Z}*", 2026,
    "Robust footprinting with sample-specific Tn5 bias correction for bulk and single cell ATAC-seq",
    "Nature Communications", "17", "10.1038/s41467-026-73164-3",
    "10.1101/2025.10.17.683160", "published", ["TraceBind"], ["gr","sc"], [])

add(f"Sussman JH&dagger;, Oldridge DA&dagger;, Yu W&dagger;, Chen C-H, Zellmer AM, Rong J, &hellip;, {Z}, De Raedt T, Cole K, Tan K*", 2026,
    "A longitudinal single-cell and spatial multiomic atlas of pediatric high-grade glioma",
    "Cell Reports Medicine", "7, 102766", "10.1016/j.xcrm.2026.102766",
    "10.1101/2024.03.06.583588", "published", [], ["sc","sp"], ["can","neu"])

# ---- 2025 ------------------------------------------------------------------
add(f"Wu C-Y, Rong J, Sathe A, Hess PR, Lau BT, Grimes SM, Huang S, Ji HP*, {Z}*", 2025,
    "Cancer subclone detection based on DNA copy number in single-cell and spatial omic sequencing data",
    "Nature Methods", "22, 1846&ndash;1856", "10.1038/s41592-025-02773-5", None, "published",
    ["Clonalscope"], ["cn","te","sc","sp"], ["can"])

add(f"Kl&#246;tzer KA, Abedini A, Li S, Balzer MS, Liang X, Levinsohn J, &hellip;, Halmos B, {Z}*, Susztak K*", 2025,
    "Analysis of individual patient pathway coordination in a cross-species single-cell kidney atlas",
    "Nature Genetics", "57, 1922&ndash;1934", "10.1038/s41588-025-02285-0", None, "published",
    ["CellSpectra"], ["pa","sc","int"], ["kid"])

add(f"Yu W, Biyik-Sit R, Uzun Y, Chen C-H, Thadi A, Sussman JH, &hellip;, {Z}, Maris JM, Tan K*", 2025,
    "Longitudinal single-cell multiomic atlas of high-risk neuroblastoma reveals chemotherapy-induced tumor microenvironment rewiring",
    "Nature Genetics", "57, 1142&ndash;1154", "10.1038/s41588-025-02158-6", None, "published",
    [], ["sc","int"], ["can"])

add(f"Li H, Wang D, Gao Q, Tan P, Wang Y, Cai X, Li A, Zhao Y, Thurman AL, Malekpour SA, Zhang Y, Sala R, Cipriano A, Wei C-L, Sebastiano V, Song C, {Z}, Au KF*", 2025,
    "Improving gene isoform quantification with miniQuant",
    "Nature Biotechnology", "44, 477&ndash;489", "10.1038/s41587-025-02633-9", None, "published",
    ["miniQuant"], ["lr","di","gr"], [])

add(f"Fu Y*, Kim H, Roy S, Huang S, Adams JI, Grimes SM, Lau BT, Sathe A, Ji HP*, {Z}*", 2025,
    "Single cell and spatial alternative splicing analysis with Nanopore long read sequencing",
    "Nature Communications", "16, 6654", "10.1038/s41467-025-60902-2", None, "published",
    ["Longcell"], ["lr","sc","sp","gr"], ["can"])

add(f"Gier RA, Bracht SA, Rong J, Reyes Hueros RLA, Wahlsten ML, Cote C, &hellip;, Falk GW, {Z}, Shaffer SM*", 2025,
    "Clonal cell states link gastroesophageal junction tissues with metaplasia and cancer",
    "Nature Communications", "16, 10952", "10.1038/s41467-025-66302-w", None, "published",
    ["scmtVT"], ["sc","lt","te"], ["can","gi"])

# ---- 2024 ------------------------------------------------------------------
add(f"Zhang Z, Mathew D, Lim TL, Mason K, Martinez CM, Huang S, Wherry EJ, Susztak K, Minn AJ, Ma Z*, {Z}*", 2024,
    "Recovery of biological signals lost in single-cell batch integration with CellANOVA",
    "Nature Biotechnology", "43, 1861&ndash;1877", "10.1038/s41587-024-02463-1", None, "published",
    ["CellANOVA"], ["bc","int","sc"], ["imm","kid"])

add(f"Xu J&dagger;, Chen C&dagger;, Sussman JH, Yoshimura S, Vincent T, P&#246;l&#246;nen P, &hellip;, {Z}, &hellip;, Mullighan CG, Tan K*, Teachey DT*", 2024,
    "A multiomic atlas identifies a treatment-resistant, bone marrow progenitor-like cell population in T cell acute lymphoblastic leukemia",
    "Nature Cancer", "6, 102&ndash;122", "10.1038/s43018-024-00863-5", None, "published",
    [], ["sc","int"], ["can"])

add(f"Mason K, Sathe A, Hess PR, Rong J, Wu C-Y, Furth E, Susztak K, Levinsohn J, Ji HP, {Z}*", 2024,
    "Niche-DE: niche-differential gene expression analysis in spatial transcriptomics data identifies context-dependent cell-cell interactions",
    "Genome Biology", "25, 14", "10.1186/s13059-023-03159-6", "10.1101/2023.01.03.522646",
    "published", ["NicheDE"], ["sp","de","sc"], ["can"])

add(f"Mathew D, Marmarelis ME, Foley C, Bauml JM, Ye D, Ghinnagow R, Ngiow SF, Klapholz M, Jun S, Zhang Z, Zorc R, Diehn M, Hwang W-T, {Z}, Langer CJ, Wherry EJ, Minn AJ*", 2024,
    "Combined JAK inhibition and PD-1 immunotherapy for non-small cell lung cancer patients",
    "Science", "384, eadf1329", "10.1126/science.adf1329", None, "published",
    [], ["sc"], ["can","imm"])

add(f"Malamon JS&dagger;, Farrell JJ&dagger;, Xia LC, Dombroski BA, Das RG, Way J, &hellip;, {Z}, &hellip;, Schellenberg GD, Lee WP&dagger;*, Vardarajan BN&dagger;*", 2024,
    "A comparative study of structural variant calling in WGS from Alzheimer's disease families",
    "Life Science Alliance", "7, e202302181", "10.26508/lsa.202302181", None, "published",
    [], ["vd"], ["neu"])

# ---- 2023 ------------------------------------------------------------------
add(f"Chen S&dagger;, Zhu B&dagger;, Huang S, Hickey JW, Lin KZ, Snyder M, Greenleaf WJ, Nolan GP, {Z}*, Ma Z*", 2023,
    "Integration of spatial and single-cell data across modalities with weakly linked features",
    "Nature Biotechnology", "42, 1096&ndash;1106", "10.1038/s41587-023-01935-0",
    "10.1101/2023.01.12.523851", "published", ["MaxFuse"], ["int","sp","sc"], [])

add(f"Lin KZ, {Z}*", 2023,
    "Quantifying common and distinct information in single-cell multimodal data with tilted canonical correlation analysis",
    "PNAS", "120, e2303647120", "10.1073/pnas.2303647120", "10.1101/2022.10.07.511320",
    "published", ["Tilted-CCA"], ["int","sc","np"], [])

add(f"Hickey JW, Becker WR, Nevins SA, Horning A, Perez AE, Zhu C, &hellip;, {Z}, &hellip;, Nolan GP*, Greenleaf WJ*, Snyder M*", 2023,
    "Organization of the human intestine at single-cell resolution",
    "Nature", "619, 572&ndash;584", "10.1038/s41586-023-05915-x", None, "published",
    [], ["sp","sc"], ["gi"])

# ---- 2022 ------------------------------------------------------------------
add(f"Bibby JA, Agarwal D, Freiwald T, Kunz N, Merle NS, West EE, Singh P, Larochelle A, Chinian F, Mukherjee S, Afzali B, Kemper C*, {Z}*", 2022,
    "Systematic single-cell pathway analysis to characterize early T cell activation",
    "Cell Reports", "41, 111697", "10.1016/j.celrep.2022.111697", None, "published",
    ["SCPA"], ["pa","sc"], ["imm"])

add(f"Jiang Y, Harigaya Y, Zhang Z, Zhang H, Zang C, {Z}*", 2022,
    "Nonparametric single-cell multiomic characterization of trio relationships between transcription factors, target genes, and cis-regulatory regions",
    "Cell Systems", "13, 737&ndash;751.e4", "10.1016/j.cels.2022.08.004", None, "published",
    ["TRIPOD"], ["gr","sc","np","int"], [])

add(f"Cucolo L, Chen Q, Qiu J, Yu Y, Klapholz M, Budinich KA, Zhang Z, Shao Y, Brodsky IE, Jordan MS, Gilliland DG, {Z}, Shi J, Minn AJ*", 2022,
    "The interferon-stimulated gene RIPK1 regulates cancer cell intrinsic and extrinsic resistance to immune checkpoint blockade",
    "Immunity", "55, 671&ndash;685.e10", "10.1016/j.immuni.2022.03.007", None, "published",
    [], ["sc"], ["can","imm"])

add(f"Sathe A, Mason K, Grimes SM, Zhou Z, Lau BT, Bai X, Su A, Tan X, Lee H, Suarez CJ, Nguyen Q, Poultsides G, {Z}, Ji HP*", 2022,
    "Colorectal cancer metastases in the liver establish immunosuppressive spatial networking between tumor-associated SPP1+ macrophages and fibroblasts",
    "Clinical Cancer Research", "29, 244&ndash;260", "10.1158/1078-0432.CCR-22-2041",
    "10.1101/2020.09.01.273672", "published", ["CACTI"], ["sp","sc"], ["can","imm","gi"])

# ---- 2021 ------------------------------------------------------------------
add(f"Wu C-Y, Lau BT, Kim HS, Sathe A, Grimes SM, Ji HP, {Z}*", 2021,
    "Integrative single-cell analysis of allele-specific copy number alterations and chromatin accessibility in cancer",
    "Nature Biotechnology", "39, 1259&ndash;1269", "10.1038/s41587-021-00911-w", None, "published",
    ["Alleloscope"], ["cn","sc","int","gr","te"], ["can"])

add(f"Navin NE, Rozenblatt-Rosen O, {Z}", 2021,
    "New frontiers in single-cell genomics",
    "Genome Research", "31, ix&ndash;x", "10.1101/gr.276129.121", None, "published",
    [], ["sc"], [])

add(f"Wang J, Zhao Q, Bowden J, Hemani G, Davey Smith G, Small DS, {Z}", 2021,
    "Causal inference for heritable phenotypic risk factors using heterogeneous genetic instruments",
    "PLoS Genetics", "17, e1009575", "10.1371/journal.pgen.1009575", None, "published",
    ["GRAPPLE"], ["ci"], [])

add(f"Zhao Q*, Wang J, Miao Z, {Z}, Hennessy S, Small DS, Rader DJ", 2021,
    "A Mendelian randomization study of the role of lipoprotein subfractions in coronary artery disease",
    "eLife", "10, e58361", "10.7554/eLife.58361", None, "published",
    [], ["ci"], ["cvd"])

# ---- 2020 ------------------------------------------------------------------
add(f"Zhou Z, Xu B, Minn AJ, {Z}*", 2020,
    "DENDRO: genetic heterogeneity profiling and subclone detection by single-cell RNA sequencing",
    "Genome Biology", "21, 10", "10.1186/s13059-019-1922-x", None, "published",
    ["DENDRO"], ["te","sc","cn"], ["can"])

add(f"Zhou Z, Ye C, Wang J, {Z}*", 2020,
    "Surface protein imputation from single cell transcriptomes by deep neural networks",
    "Nature Communications", "11, 651", "10.1038/s41467-020-14391-0", None, "published",
    ["cTP-net"], ["ai","di","sc"], [])

add(f"Agarwal D, Wang J, {Z}*", 2020,
    "Data denoising and post-denoising corrections in single cell RNA sequencing",
    "Statistical Science", "35, 112&ndash;128", "10.1214/19-STS7560", None, "published",
    [], ["di","sc"], [])

add(f"Mukherjee S, Agarwal D, {Z}, Bhattacharya BB", 2020,
    "Distribution-free multisample tests based on optimal matchings with applications to single cell genomics",
    "Journal of the American Statistical Association", "117, 627&ndash;638",
    "10.1080/01621459.2020.1791131", None, "published", [], ["np","sc"], [])

add(f"Rozenblatt-Rosen O, Regev A, Oberdoerffer P, Nawy T, Hupalowska A, &hellip;, {Z}, &hellip; (Human Tumor Atlas Network)", 2020,
    "The Human Tumor Atlas Network: charting tumor transitions across space and time at single-cell resolution",
    "Cell", "181, 236&ndash;249", "10.1016/j.cell.2020.03.053", None, "published",
    [], ["sc","sp"], ["can"])

# ---- 2019 ------------------------------------------------------------------
add(f"Wang X, Park J, Susztak K, {Z}*, Li M*", 2019,
    "Bulk tissue cell type deconvolution with multi-subject single-cell expression reference",
    "Nature Communications", "10, 380", "10.1038/s41467-018-08023-x", None, "published",
    ["MuSiC"], ["dc","sc"], ["kid"])

add(f"Wang J, Agarwal D, Huang M, Hu G, Zhou Z, Ye C, {Z}*", 2019,
    "Data denoising with transfer learning in single-cell transcriptomics",
    "Nature Methods", "16, 875&ndash;878", "10.1038/s41592-019-0537-1", None, "published",
    ["SAVER-X"], ["di","ai","sc"], [])

add(f"Benci JL, Johnson LR, Choa R, Xu Y, Qiu J, Zhou Z, &hellip;, {Z}, &hellip;, Wolchok JD, Kambayashi T, Minn AJ*", 2019,
    "Opposing functions of interferon coordinate adaptive and innate immune responses to cancer immune checkpoint blockade",
    "Cell", "178, 933&ndash;948.e14", "10.1016/j.cell.2019.07.019", None, "published",
    [], ["sc"], ["can","imm"])

add(f"Nguyen S, Deleage C, Darko S, Ransier A, Truong DP, Agarwal D, &hellip;, {Z}, &hellip;, Deeks SG, Buggert M, Betts MR*", 2019,
    "Elite control of HIV is associated with distinct functional and transcriptional signatures in lymphoid tissue CD8+ T cells",
    "Science Translational Medicine", "11, eaax4077", "10.1126/scitranslmed.aax4077", None,
    "published", [], ["sc"], ["imm","inf"])

add(f"Pauly D, Agarwal D, Dana N, Sch&#228;fer N, Biber J, Wunderlich KA, &hellip;, {Z}, &hellip;, Stambolian D, Li M, Grosche A*", 2019,
    "Cell-type-specific complement expression in the healthy and diseased retina",
    "Cell Reports", "29, 2835&ndash;2848.e4", "10.1016/j.celrep.2019.10.084",
    "10.1101/413088", "published", [], ["sc","de"], ["imm","neu"])

add(f"Agarwal D, {Z}*", 2019,
    "Semblance: an empirical similarity kernel on probability spaces",
    "Science Advances", "5, eaau9630", "10.1126/sciadv.aau9630", None, "published",
    ["Semblance"], ["np"], [])

# ---- 2018 ------------------------------------------------------------------
add(f"Huang M, Wang J, Torre E, Dueck H, Shaffer S, Bonasio R, Murray JI, Raj A, Li M, {Z}*", 2018,
    "SAVER: gene expression recovery for single-cell RNA sequencing",
    "Nature Methods", "15, 539&ndash;542", "10.1038/s41592-018-0033-z", "10.1101/138677",
    "published", ["SAVER"], ["di","sc"], [])

add(f"Wang J, Huang M, Torre E, Dueck H, Shaffer S, Murray JI, Raj A, Li M, {Z}*", 2018,
    "Gene expression distribution deconvolution in single-cell RNA sequencing",
    "PNAS", "115, E6437&ndash;E6446", "10.1073/pnas.1721085115", "10.1101/227033",
    "published", ["DESCEND"], ["dc","sc"], [])

add(f"Jiang Y*, Wang R, Urrutia E, Anastopoulos IN, Nathanson KL, {Z}*", 2018,
    "CODEX2: full-spectrum copy number variation detection by high-throughput DNA sequencing",
    "Genome Biology", "19, 202", "10.1186/s13059-018-1578-y", None, "published",
    ["CODEX2"], ["cn"], ["can"])

add(f"Zhou Z, Wang W, Wang L-S, {Z}*", 2018,
    "Integrative DNA copy number detection and genotyping from sequencing and array-based platforms",
    "Bioinformatics", "34, 2349&ndash;2355", "10.1093/bioinformatics/bty104", None, "published",
    ["iCNV"], ["cn","int"], [])

add(f"Urrutia E, Chen H, Zhou Z, {Z}*, Jiang Y*", 2018,
    "Integrative pipeline for profiling DNA copy number and inferring tumor phylogeny",
    "Bioinformatics", "34, 2126&ndash;2128", "10.1093/bioinformatics/bty057", None, "published",
    ["MARATHON"], ["cn","te"], ["can"])

add(f"Wang X, Jiang Y, {Z}, Small DS", 2018,
    "Sensitivity analysis and power for instrumental variable studies",
    "Biometrics", "74, 1150&ndash;1160", "10.1111/biom.12873", None, "published",
    [], ["ci"], [])

add(f"Zhang H, {Z}, Li M, Reilly MP*", 2018,
    "First giant steps toward a cell atlas of atherosclerosis",
    "Circulation Research", "122, 1632&ndash;1634", "10.1161/CIRCRESAHA.118.313076", None,
    "published", [], ["sc"], ["cvd"])

# ---- 2017 ------------------------------------------------------------------
add(f"Jiang Y, {Z}*, Li M*", 2017,
    "SCALE: modeling allele-specific gene expression by single-cell RNA sequencing",
    "Genome Biology", "18, 74", "10.1186/s13059-017-1200-8", None, "published",
    ["SCALE"], ["gr","sc"], [])

add(f"Jia C, Hu Y, Kelly D, Kim J, Li M*, {Z}*", 2017,
    "Accounting for technical noise in differential expression analysis of single-cell RNA sequencing data",
    "Nucleic Acids Research", "45, 10978&ndash;10988", "10.1093/nar/gkx754", None, "published",
    ["TASC"], ["de","sc","di"], [])

add(f"Chen H, Jiang Y, Maxwell KN, Nathanson KL, {Z}*", 2017,
    "Allele-specific copy number estimation by whole exome sequencing",
    "Annals of Applied Statistics", "11, 1169&ndash;1192", "10.1214/17-AOAS1043", None,
    "published", ["FALCON-X"], ["cn"], ["can"])

add(f"Xia LC, Bell JM, Wood-Bouwens C, Chen JJ, {Z}*, Ji HP*", 2017,
    "Identification of large rearrangements in cancer genomes with barcode linked reads",
    "Nucleic Acids Research", "46, e19", "10.1093/nar/gkx1193", None, "published",
    ["SWAN"], ["vd"], ["can"])

add(f"Maxwell KN, Wubbenhorst B, Wenz BM, De Sloover D, Pluta J, Emery L, &hellip;, {Z}, &hellip;, Feldman M, Domchek SM, Nathanson KL*", 2017,
    "BRCA locus-specific loss of heterozygosity in germline BRCA1 and BRCA2 carriers",
    "Nature Communications", "8, 319", "10.1038/s41467-017-00388-9", None, "published",
    [], ["cn"], ["can"])

add(f"Garman B, Anastopoulos IN, Krepler C, Brafford P, Sproesser K, Jiang Y, &hellip;, {Z}, Davies MA, Herlyn M, Nathanson KL*", 2017,
    "Genetic and genomic characterization of 462 melanoma patient-derived xenografts, tumor biopsies, and cell lines",
    "Cell Reports", "21, 1936&ndash;1952", "10.1016/j.celrep.2017.10.052", None, "published",
    [], ["cn"], ["can"])

add(f"Wang X, Chen H, {Z}", 2017,
    "DNA copy number profiling using single-cell sequencing",
    "Briefings in Bioinformatics", "19, 731&ndash;736", "10.1093/bib/bbx004", None, "published",
    [], ["cn","sc"], [])

# ---- 2016 ------------------------------------------------------------------
add(f"Jiang Y, Qiu Y, Minn AJ, {Z}*", 2016,
    "Assessing intratumor heterogeneity and tracking longitudinal and spatial clonal evolutionary history by next-generation sequencing",
    "PNAS", "113, E5528&ndash;E5537", "10.1073/pnas.1522203113", None, "published",
    ["Canopy"], ["te","cn"], ["can"])

add(f"Xia LC, Sakshuwong S, Hopmans ES, Bell JM, Grimes SM, Siegmund DO, Ji HP*, {Z}*", 2016,
    "A genome-wide approach for detecting novel insertion-deletion variants of mid-range size",
    "Nucleic Acids Research", "44, e126", "10.1093/nar/gkw481", None, "published",
    ["SWAN","SVEngine"], ["vd","cp"], [])

add(f"{Z}, Yakir B, Xia LC, Siegmund DO", 2016,
    "Scan statistics on Poisson random fields with applications in genomics",
    "Annals of Applied Statistics", "10, 726&ndash;755", "10.1214/15-AOAS892", None,
    "published", [], ["cp"], [])

add(f"Wang X, Chen M, Yu X, Pornputtapong N, Chen H, {Z}, Powers RS, Krauthammer M*", 2016,
    "Global copy number profiling of cancer genomes",
    "Bioinformatics", "32, 926&ndash;928", "10.1093/bioinformatics/btv676", None, "published",
    ["CLOSE"], ["cn"], ["can"])

# ---- 2015 ------------------------------------------------------------------
add(f"Chen H, {Z}", 2015,
    "Graph-based change-point detection",
    "Annals of Statistics", "43, 139&ndash;176", "10.1214/14-AOS1269", None, "published",
    ["gSeg"], ["cp","np"], [])

add(f"Chen H, Bell JM, Zavala NA, Ji HP, {Z}*", 2015,
    "Allele-specific copy number profiling by next-generation DNA sequencing",
    "Nucleic Acids Research", "43, e23", "10.1093/nar/gku1252", None, "published",
    ["FALCON"], ["cn"], ["can"])

add(f"Jiang Y, Oldridge DA, Diskin SJ, {Z}*", 2015,
    "CODEX: a normalization and copy number variation detection method for whole exome sequencing",
    "Nucleic Acids Research", "43, e39", "10.1093/nar/gku1363", None, "published",
    ["CODEX2"], ["cn"], ["can"])

add(f"Cushing A, Kamali A, Winters M, Hopmans ES, Bell JM, Grimes SM, Xia LC, {Z}, Moss RB, Holodniy M, Ji HP*", 2015,
    "Emergence of hemagglutinin mutations during the course of influenza infection",
    "Scientific Reports", "5, 16178", "10.1038/srep16178", None, "published",
    [], ["vd"], ["inf"])

add(f"Peixoto LL, Wimmer ME, Poplawski SG, Tudor JC, Kenworthy CA, Liu S, Mizuno K, Garcia BA, {Z}, Giese KP, Abel T*", 2015,
    "Memory acquisition and retrieval impact different epigenetic processes that regulate gene expression",
    "BMC Genomics", "16, S5", "10.1186/1471-2164-16-S5-S5", None, "published",
    [], ["gr","de"], ["neu"])

add(f"Yue M, Han X, De Masi L, Zhu C, Ma X, Zhang J, &hellip;, {Z}, Rankin SC, Schifferli DM*", 2015,
    "Allelic variation contributes to bacterial host specificity",
    "Nature Communications", "6, 8754", "10.1038/ncomms9754", None, "published",
    [], ["vd"], ["inf"])

# ---- 2014 ------------------------------------------------------------------
add(f"Nadauld LD, Garcia S, Natsoulis G, Bell JM, Miotke L, Hopmans ES, &hellip;, {Z}, Ford JM, Kuo CJ*, Ji HP*", 2014,
    "Metastatic tumor evolution and organoid modeling implicate TGFBR2 as a cancer driver in diffuse gastric cancer",
    "Genome Biology", "15, 428", "10.1186/s13059-014-0428-9", None, "published",
    [], ["te","cn"], ["can","gi"])

# ---- 2013 ------------------------------------------------------------------
add(f"Chen H, {Z}", 2013,
    "Graph-based tests for two-sample comparisons of categorical data",
    "Statistica Sinica", "23, 1479&ndash;1503", "10.5705/ss.2012.125s", None, "published",
    ["gCat"], ["np"], [])

add(f"Natsoulis G&dagger;, {Z}&dagger;, Welch K, Bell JM, Ji HP*", 2013,
    "Identification of insertion deletion mutations from deep targeted resequencing",
    "Journal of Data Mining in Genomics &amp; Proteomics", "4, 132",
    "10.4172/2153-0602.1000132", None, "published", [], ["vd"], [])

# ---- 2012 ------------------------------------------------------------------
add(f"Muralidharan O, Natsoulis G, Bell JM, Newburger D, Xu H, Kela I, Ji HP, {Z}*", 2012,
    "A cross-sample statistical model for SNP detection in short-read sequencing data",
    "Nucleic Acids Research", "40, e5", "10.1093/nar/gkr851", None, "published",
    [], ["vd"], [])

add(f"Flaherty P, Natsoulis G, Muralidharan O, Winters M, Buenrostro J, Bell JM, Brown S, Holodniy M, {Z}, Ji HP*", 2012,
    "Ultrasensitive detection of rare mutations using next-generation targeted resequencing",
    "Nucleic Acids Research", "40, e2", "10.1093/nar/gkr861", None, "published",
    [], ["vd"], [])

add(f"Shen JJ, {Z}*", 2012,
    "Change-point model on nonhomogeneous Poisson processes with application in copy number profiling by next-generation DNA sequencing",
    "Annals of Applied Statistics", "6, 476&ndash;496", "10.1214/11-AOAS517", None, "published",
    ["seqCBS"], ["cp","cn"], [])

add(f"Muralidharan O, Natsoulis G, Bell JM, Ji HP, {Z}*", 2012,
    "Detecting mutations in mixed sample sequencing data using empirical Bayes",
    "Annals of Applied Statistics", "6, 1047&ndash;1067", "10.1214/12-AOAS538", None,
    "published", [], ["vd"], [])

add(f"{Z}, Siegmund DO", 2012,
    "Model selection for high-dimensional, multi-sequence change-point problems",
    "Statistica Sinica", "22, 1507&ndash;1538", "10.5705/ss.2010.257", None, "published",
    [], ["cp"], [])

add(f"Sun Y, {Z}, Owen AB", 2012,
    "Multiple hypothesis testing adjusted for latent variables, with an application to the AGEMAP gene expression data",
    "Annals of Applied Statistics", "6, 1664&ndash;1688", "10.1214/12-AOAS561", None,
    "published", ["leapp"], ["bc","de"], ["age"])

# ---- 2011 ------------------------------------------------------------------
add(f"Chen H, Xing H, {Z}*", 2011,
    "Estimation of parent specific DNA copy number in tumors using high-density genotyping arrays",
    "PLoS Computational Biology", "7, e1001060", "10.1371/journal.pcbi.1001060", None,
    "published", [], ["cn"], ["can"])

add(f"Siegmund DO, Yakir B, {Z}", 2011,
    "Detecting simultaneous variant intervals in aligned sequences",
    "Annals of Applied Statistics", "5, 645&ndash;668", "10.1214/10-AOAS400", None,
    "published", [], ["cp"], [])

add(f"Efron B, {Z}", 2011,
    "False discovery rates and copy number variation",
    "Biometrika", "98, 251&ndash;271", "10.1093/biomet/asr018", None, "published",
    [], ["cp","cn"], [])

add(f"Natsoulis G, Bell JM, Xu H, Buenrostro JD, Ordonez H, Grimes S, Newburger D, Jensen M, Zahn JM, {Z}, Ji HP*", 2011,
    "A flexible approach for highly multiplexed candidate gene targeted resequencing",
    "PLoS ONE", "6, e21088", "10.1371/journal.pone.0021088", None, "published",
    [], ["vd"], [])

add(f"Siegmund DO, {Z}, Yakir B", 2011,
    "False discovery rate for scanning statistics",
    "Biometrika", "98, 979&ndash;985", "10.1093/biomet/asr057", None, "published",
    [], ["cp"], [])

# --------------------------------------------------------------------- roster
# Lab members (current + alumni, from pages/team.md), keyed by how each name is
# written in an author list. These are bolded like the PI's name.
LAB = {
    # current
    "Fu Y", "Mason K", "Zhang Z", "Rong J", "Chen XE", "Lin Y", "Yang Y",
    "Aristel A", "Mathew D", "Miao Z", "Adams JI", "Huang S", "Hess PR",
    # alumni
    "Lin KZ", "Lin K", "Wu C-Y", "Agarwal D", "Zhou Z", "Huang M", "Wang J",
    "Wang X", "Xia LC", "Jiang Y", "Chen H", "Shen JJ", "Sun Y",
}
# Same surname + initials as a lab member, but a different person.
NOT_LAB = {
    ("Global copy number profiling of cancer genomes", "Wang X"),   # Xuefeng Wang
}


def bold_lab(authors, title):
    """Bold lab members, leaving trailing markers (* and dagger) outside the tag."""
    out = []
    for piece in authors.split(", "):
        core = piece.replace("*", "").replace("&dagger;", "").strip()
        if core in LAB and (title, core) not in NOT_LAB:
            piece = piece.replace(core, "<strong>%s</strong>" % core, 1)
        out.append(piece)
    return ", ".join(out)


# ------------------------------------------------------------------ emit YAML
def q(s):
    if s is None:
        return "~"
    s = str(s).replace("\\", "\\\\").replace('"', '\\"')
    return '"' + s + '"'

root = sys.argv[1]
os.makedirs(os.path.join(root, "_data"), exist_ok=True)

with io.open(os.path.join(root, "_data", "pubtags.yml"), "w", encoding="utf-8", newline="\n") as f:
    f.write("# Tag registry for the publications page. Edit labels/colours here.\n")
    f.write("# 'fill' is the background (methodology); 'edge' its border.\n")
    f.write("# Biology tags use 'color' for bold text, no fill.\n\nmethod:\n")
    for k, label, fill, edge in METHOD_TAGS:
        f.write(f"  - key: {k}\n    label: {q(label)}\n    fill: {q(fill)}\n    edge: {q(edge)}\n")
    f.write("\nbio:\n")
    for k, label, color in BIO_TAGS:
        f.write(f"  - key: {k}\n    label: {q(label)}\n    color: {q(color)}\n")

with io.open(os.path.join(root, "_data", "publications.yml"), "w", encoding="utf-8", newline="\n") as f:
    f.write("# Publications, newest first. Rebuild the page by editing this file only.\n")
    f.write("# status: published | preprint | review\n")
    f.write("# methods/bio: keys from _data/pubtags.yml\n\n")
    for p in P:
        f.write(f"- title: {q(p['title'])}\n")
        f.write(f"  authors: {q(bold_lab(p['authors'], p['title']))}\n")
        f.write(f"  year: {p['year']}\n")
        f.write(f"  venue: {q(p['venue'])}\n")
        if p["detail"]:
            f.write(f"  detail: {q(p['detail'])}\n")
        f.write(f"  status: {p['status']}\n")
        if p["doi"]:
            f.write(f"  doi: {q(p['doi'])}\n")
        if p["preprint"]:
            f.write(f"  preprint: {q(p['preprint'])}\n")
        if p["software"]:
            f.write("  software:\n")
            for s in p["software"]:
                f.write(f"    - name: {q(s)}\n      url: {q(SOFTWARE[s])}\n")
        f.write(f"  methods: [{', '.join(p['methods'])}]\n")
        f.write(f"  bio: [{', '.join(p['bio'])}]\n\n")

# ------------------------------------------------------------------- reporting
mk = {k for k, _, _, _ in METHOD_TAGS}
bk = {k for k, _, _ in BIO_TAGS}
bad = [(p["title"][:50], t) for p in P for t in p["methods"] + p["bio"] if t not in mk | bk]
print(f"entries: {len(P)}   published: {sum(1 for p in P if p['status']=='published')}"
      f"   preprint: {sum(1 for p in P if p['status']=='preprint')}"
      f"   in review: {sum(1 for p in P if p['status']=='review')}")
print(f"with DOI: {sum(1 for p in P if p['doi'])}   with preprint link: {sum(1 for p in P if p['preprint'])}"
      f"   with software: {sum(1 for p in P if p['software'])}")
if bad:
    print("UNKNOWN TAGS:", bad)
print("\nmethodology tag counts:")
for k, label, _, _ in METHOD_TAGS:
    print(f"  {label:32s} {sum(1 for p in P if k in p['methods']):3d}")
print("biology tag counts:")
for k, label, _ in BIO_TAGS:
    print(f"  {label:32s} {sum(1 for p in P if k in p['bio']):3d}")
untagged = [p["title"][:60] for p in P if not p["methods"]]
if untagged:
    print("\nNO METHODOLOGY TAG:", untagged)
