import os
import uuid

AVG_INC_COUNT_COL = "m6_avg_inc_count"
DATABASE_COL = "database"
DEPENDENCY_COL = "dependency"
GRAPH_COL = "graph"
GRAPH_SOURCE_COL = "graph_source"
LP_POSSIBLE_COL = "lp_possible"
MAX_INC_COUNT_COL = "m5_max_inc_count"
METHOD_COL = "method"
METRIC_COL = "metric"
MINIMALITY_COL = "m7_minimality"
NO_INTER_GRAPH_DEPS_COL = "no_inter_deps"
NO_INTRA_GRAPH_DEPS_COL = "no_intra_deps"
ORIGIN_OF_DEPS_COL = "dep_origin"
ORIGINAL_NF_COL = "original_nf"
PDF_METADATA = {
    # 'Title': '',
    'Author': 'The Orb of Evaluation',
    # 'Subject': '',
    # 'Keywords': 'plotnine, python',
    'Creator': 'The Dominion'
}
RED_COUNT_COL = "m8_red_count"
RUN_ID_COL = "run_id"
RUN_ID = str(uuid.uuid4())
TIMESTAMP_COL = "timestamp"
VALUE_COL = "value"
