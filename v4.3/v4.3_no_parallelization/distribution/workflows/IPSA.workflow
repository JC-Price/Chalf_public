### CHALF SETTINGS ###
chalf=True

## CHALF LIGHT SEARCH SETTINGS ##
chalf.search.light=True
chalf.search.residues=chmy

## CHALF FILTER SETTINGS ##
chalf.filter.min=0.0
chalf.filter.max=3.48
chalf.filter.rsq=0.8
chalf.filter.ci_filter=False
chalf.filter.ci_value=0.35
chalf.filter.optimize=rsq
chalf.filter.sig_only=False

## CHALF FITTING OPTIONS ##
chalf.fitting.min_pts=4
chalf.fitting.outlier_trimming=True
chalf.fitting.outlier_cutoff=2
chalf.fitting.zero_criteria=remove

## CHALF GRAPHING OPTIONS ##
chalf.graphing.graph=False
chalf.graphing.file_type=jpg
chalf.graphing.min=0.0
chalf.graphing.max=3.48
chalf.graphing.rsq=0.8
chalf.graphing.ci_filter=False
chalf.graphing.ci_value=0.35

## CHALF EXPERIMENTAL OPTIONS ##
chalf.experimental.sg.smooth=False
chalf.experimental.sg.window=5
chalf.experimental.sg.order=2
chalf.experimental.wf.window_fit=False
chalf.experimental.wf.window=6
chalf.experimental.ms.mutations=False

### QUALITY CONTROL SETTINGS ###
qc=True

## QUALITY CONTROL SEARCH SETTINGS ##
qc.search.residues=chmy

## QUALITY CONTROL FILTER OPTIONS ##
qc.filter.min=0.0
qc.filter.max=3.48
qc.filter.rsq=0.8
qc.filter.ci_filter=False
qc.filter.ci_value=0.35
qc.filter.optimize=rsq

### VISUALIZATION SETTINGS ###

## QUALITY CONTROL REPORT ##
visualization.qc.report=True
visualization.qc.open=False

## RESIDUE MAPPER ##
visualization.rm=False
visualization.rm.file_type=jpg
visualization.rm.min=0.0
visualization.rm.max=3.48

# TRENDLINES #
visualization.rm.trendlines.trendline=True
visualization.rm.trendlines.min=5
visualization.rm.trendlines.window=3

# OTHER OPTIONS #
visualization.rm.other.all_curves=True
visualization.rm.other.reference_stats=True
visualization.rm.other.rm_trendline_stats=False
visualization.rm.other.mutation_search=False
visualization.rm.other.advanced=

## COMBINED RESIDUE MAPPER ##
visualization.crm=True
visualization.crm.file_type=jpg
visualization.crm.min=0.0
visualization.crm.max=3.48

# TRENDLINES #
visualization.crm.trendlines.trendline=True
visualization.crm.trendlines.min=5
visualization.crm.trendlines.window=3

# OTHER OPTIONS #
visualization.crm.other.all_curves=True
visualization.crm.other.reference_stats=True
visualization.crm.other.crm_trendline_stats=False
visualization.crm.other.shared_only=True
visualization.crm.other.mutation_search=False
visualization.crm.other.advanced=

## DELTA MAPPER OPTIONS ##
visualization.dm=True
visualization.dm.file_type=jpg
visualization.dm.min=-3.48
visualization.dm.max=3.48

# TRENDLINES #
visualization.dm.trendlines.trendline=True
visualization.dm.trendlines.min=5
visualization.dm.trendlines.window=3

# KDE OPTIONS #
visualization.dm.kde.min_pts=3
visualization.dm.sig_filter=False
visualization.dm.sig_value=0.05

# OTHER OPTIONS #
visualization.dm.other.all_curves=True
visualization.dm.other.reference_stats=True
visualization.dm.other.dm_trendline_stats=False
visualization.dm.other.mutation_search=False
visualization.dm.other.advanced=

## COMBINED SITE ##
visualization.cs=False
visualization.cs.file_type=jpg
visualization.cs.min=0.0
visualization.cs.max=3.48
