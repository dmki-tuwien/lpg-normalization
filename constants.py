import os
import uuid

ALGORITHM_COL = "algorithm"
AVG_INC_COUNT_COL = "m6_avg_inc_count"
DATABASE_COL = "database"
DEPENDENCY_COL = "dependency"
EDGE_COUNT_COL = "no_edges"
GRAPH_COL = "graph"
GRAPH_SOURCE_COL = "graph_source"
INTER_FIRST_COL = "inter_first"
LABEL_COUNT_COL = "no_labels"
LP_POSSIBLE_COL = "lp_possible"
MAX_INC_COUNT_COL = "m5_max_inc_count"
METHOD_COL = "method"
METRIC_COL = "metric"
MINIMALITY_COL = "m7_minimality"
MINIMALITY_CLUSTER_COL = "m7_minimality_no_clusters"
MINIMALITY_MATCHES_COL = "m7_minimality_no_matches"
MINIMUM_COVER_COL = "min_cov_used"
NO_INTER_GRAPH_DEPS_COL = "no_inter_deps"
NO_INTRA_GRAPH_DEPS_COL = "no_intra_deps"
NODE_COUNT_COL = "no_nodes"
ORIGIN_OF_DEPS_COL = "dep_origin"
ORIGINAL_NF_COL = "original_nf"
PDF_METADATA = {
    # 'Title': '',
    'Author': 'The Orb of Evaluation',
    # 'Subject': '',
    # 'Keywords': 'plotnine, python',
    'Creator': 'The Dominion'
}
PROPERTY_COUNT_COL = "no_properties"
RED_COUNT_COL = "m8_red_count"
RUN_ID_COL = "run_id"
RUN_ID = str(uuid.uuid4())
SUBSET_COL = "subset"
TIMESTAMP_COL = "timestamp"
TYPES_COUNT_COL = "no_types"
VALUE_COL = "value"
