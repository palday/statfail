def run(n=20, effect_size=.5, confound_size=.5, runs=10000):
    effect = np.random.randn(runs, n) + effect_size
    confound = np.random.randn(runs, n) + confound_size
    group1 = np.random.randn(runs, n)
    group2 = np.random.randn(runs, n)

    unconfounded_results = scipy.stats.ttest_rel(group1 + effect, group2, axis=1)[1]
    confounded_results = scipy.stats.ttest_rel(group1 + effect + confound, group2, axis=1)[1]
    stim_tests = scipy.stats.ttest_1samp(confound.T, 0)[1]

    sig_stimtests = np.where(stim_tests < .05)
    insig_stimtests = np.where(stim_tests > .05)
    assert(len(stim_tests) == runs)

    # Fake effect (not detected) 
    # stimuli not classified as confounded
    # significant effect with confounds
    nonrejected_insign_in_conf = np.intersect1d(insig_stimtests, np.where(confounded_results < .05)[0])
    no_alarm = unconfounded_results[np.intersect1d(nonrejected_insign_in_conf, 
                                                   np.where(unconfounded_results > .05)[0])]

    # Fake effect (not detected) 
    # stimuli classified as confounded
    # significant effect with confounds
    rejected_sign_in_conf = np.intersect1d(sig_stimtests, np.where(confounded_results < .05)[0])
    good_alarm = unconfounded_results[np.intersect1d(rejected_sign_in_conf, 
                                                     np.where(unconfounded_results > .05)[0])]

    # Real effect (falsely rejected) 
    # stimuli classified as confounded
    # significant effect without confounds
    false_rejection = unconfounded_results[np.intersect1d(sig_stimtests, 
                                                          np.where(unconfounded_results < .05)[0])]

    return no_alarm, good_alarm, false_rejection