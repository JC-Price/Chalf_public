
### CHALF SETTINGS ###
#run_chalf_checkBox
chalf=False

## CHALF LIGHT SEARCH SETTINGS ##

#light_search_checkBox
chalf.search.light=True

#aa_a_checkBox
#aa_c_checkBox
#aa_d_checkBox
#aa_e_checkBox
#aa_f_checkBox
#aa_g_checkBox
#aa_h_checkBox
#aa_i_checkBox
#aa_k_checkBox
#aa_l_checkBox
#aa_m_checkBox
#aa_n_checkBox
#aa_p_checkBox
#aa_q_checkBox
#aa_r_checkBox
#aa_s_checkBox
#aa_t_checkBox
#aa_v_checkBox
#aa_w_checkBox
#aa_y_checkBox
chalf.search.residues=ymch

## CHALF FILTER SETTINGS ##

#chalf_min_doubleSpinBox
chalf.filter.min=0
#chalf_max_doubleSpinBox
chalf.filter.max=3.48
#rsq_doubleSpinBox
chalf.filter.rsq=0.8
#CI_filter_checkBox
chalf.filter.ci_filter=False
#CI_doubleSpinBox
chalf.filter.ci_value=0.35
#fit_opt_comboBox
chalf.filter.optimize=rsq
#sig_only_checkBox
chalf.filter.sig_only=False

## CHALF FITTING OPTIONS ##

#min_pts_spinBox
chalf.fitting.min_pts=4
#trimming_checkBox
chalf.fitting.outlier_trimming=True
#out_cut_spinBox
chalf.fitting.outlier_cutoff=2
#chalf_zero_criteria_comboBox
chalf.fitting.zero_criteria=remove

## CHALF GRAPHING OPTIONS ##

#graph_curves_checkBox
chalf.graphing.graph=False
#graphing_filetype_comboBox
chalf.graphing.file_type=jpg
#graph_chalf_min_doubleSpinBox
chalf.graphing.min=0
#graph_chalf_max_doubleSpinBox
chalf.graphing.max=0
#graph_rsq_doubleSpinBox
chalf.graphing.rsq=0.8
#graph_ci_checkBox
chalf.graphing.ci_filter=False
#graph_ci_doubleSpinBox
chalf.graphing.ci_value=0.35

## CHALF EXPERIMENTAL OPTIONS ##

# SAVITSKY GOLAY #

#sg_checkBox
chalf.experimental.sg.smooth=False
#sg_window_spinBox
chalf.experimental.sg.window=5
#sg_order_spinBox
chalf.experimental.sg.order=2

# WINDOWED FITTING #

#windowed_fitting_checkBox
chalf.experimental.wf.window_fit=False
#wf_window_spinBox
chalf.experimental.wf.window=6

# MUTATION SEARCH #

#mutation_search_checkBox
chalf.experimental.ms.mutations=True

### QUALITY CONTROL SETTINGS ###

#qc_checkBox
qc=True

## QUALITY CONTROL SEARCH SETTINGS ##

#qc_a_checkBox
#qc_c_checkBox
#qc_d_checkBox
#qc_e_checkBox
#qc_f_checkBox
#qc_g_checkBox
#qc_h_checkBox
#qc_i_checkBox
#qc_k_checkBox
#qc_l_checkBox
#qc_m_checkBox
#qc_n_checkBox
#qc_p_checkBox
#qc_q_checkBox
#qc_r_checkBox
#qc_s_checkBox
#qc_t_checkBox
#qc_v_checkBox
#qc_w_checkBox
#qc_y_checkBox
qc.search.residues=ymch

## QUALITY CONTROL FILTER OPTIONS ##

#qc_chalf_min_doubleSpinBox
qc.filter.min=0
#qc_chalf_max_doubleSpinBox
qc.filter.max=3.48
#qc_rsq_doubleSpinBox
qc.filter.rsq=0.8
#qc_ci_checkBox
qc.filter.ci_filter=False
#qc_ci_doubleSpinBox
qc.filter.ci_value=0.35
#qc_priority_comboBox
qc.filter.optimize=rsq


### VISUALIZATION SETTINGS ###

## QUALITY CONTROL REPORT ##

#qc_vis_generate_checkBox
visualization.qc.report=True
#qc_vis_open_checkBox
visualization.qc.open=False

## RESIDUE MAPPER ##

#rm_checkBox
visualization.rm=True
#rm_filetype_comboBox
visualization.rm.file_type=jpg
#rm_chalf_low_doubleSpinBox
visualization.rm.min=0
#rm_chalf_high_doubleSpinBox
visualization.rm.max=3.48

# TRENDLINES #

#rm_trendline_checkBox
visualization.rm.trendlines.trendline=True
#rm_trendline_min_spinBox
visualization.rm.trendlines.min=5
#rm_trendline_window_spinBox
visualization.rm.trendlines.window=3

# OTHER OPTIONS #

#rm_allsites_checkBox
visualization.rm.other.all_curves=True
#rm_stats_reference_checkBox
visualization.rm.other.reference_stats=True
#rm_trendline_stats_checkBox
visualization.rm.other.rm_trendline_stats=True
#rm_custom_fasta_checkBox
visualization.rm.other.mutation_search=False
#rm_custom_ann_path_lineEdit
visualization.rm.other.advanced=


## COMBINED RESIDUE MAPPER ##

#crm_checkBox
visualization.crm=True
#crm_filetype_comboBox
visualization.crm.file_type=jpg
#crm_chalf_low_doubleSpinBox
visualization.crm.min=0
#crm_chalf_high_doubleSpinBox
visualization.crm.max=3.48

# TRENDLINES #

#crm_trendline_checkBox
visualization.crm.trendlines.trendline=True
#crm_trendline_min_spinBox
visualization.crm.trendlines.min=5
#crm_trendline_window_spinBox
visualization.crm.trendlines.window=3

# OTHER OPTIONS #

#crm_allsites_checkBox
visualization.crm.other.all_curves=True
#crm_stats_reference_checkBox
visualization.crm.other.reference_stats=True
#crm_trendline_stats_checkBox
visualization.crm.other.crm_trendline_stats=True
#crm_custom_fasta_checkBox
visualization.crm.other.mutation_search=False
#crm_custom_ann_path_lineEdit
visualization.crm.other.advanced=


## DELTA MAPPER OPTIONS ##

#dm_checkBox
visualization.dm=True
#dm_filetype_comboBox
visualization.dm.file_type=jpg
#dm_chalf_low_doubleSpinBox
visualization.dm.min=-3.48
#dm_chalf_high_doubleSpinBox
visualization.dm.max=3.48

# TRENDLINES #

#dm_trendline_checkBox
visualization.dm.trendlines.trendline=True
#dm_trendline_min_spinBox
visualization.dm.trendlines.min=5
#dm_trendline_window_spinBox
visualization.dm.trendlines.window=3

# KDE OPTIONS #

#dm_kde_min_spinBox
visualization.dm.kde.min_pts=3
#dm_kde_sig_cutoff_checkBox
visualization.dm.sig_filter=False
#dm_kde_sig_cutoff_doubleSpinBox
visualization.dm.sig_value=0.05

# OTHER OPTIONS #

#dm_allsites_checkBox
visualization.dm.other.all_curves=True
#dm_stats_reference_checkBox
visualization.dm.other.reference_stats=True
#dm_trendline_stats_checkBox
visualization.dm.other.dm_trendline_stats=True
#dm_custom_fasta_checkBox
visualization.dm.other.mutation_search=False
#dm_custom_ann_path_lineEdit
visualization.dm.other.advanced=


## COMBINED SITE ##

#cs_checkBox
visualization.cs=False
#cs_filetype_comboBox
visualization.cs.file_type=jpg
#cs_chalf_low_doubleSpinBox
visualization.cs.min=0
#cs_chalf_high_doubleSpinBox
visualization.cs.max=3.48