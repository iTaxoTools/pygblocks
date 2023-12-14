from itaxotools.pygblocks import ConservationDegree, Options, analyze_column


def test_column_basic():
    options = Options(IS=2, FS=3, CP=0, BL1=0, BL2=0)
    assert analyze_column("AAA-", options) == (ConservationDegree.NonConserved, True)
    assert analyze_column("ACGT", options) == (ConservationDegree.NonConserved, False)
    assert analyze_column("AACC", options) == (ConservationDegree.Conserved, False)
    assert analyze_column("AAAC", options) == (ConservationDegree.HighlyConserved, False)
    assert analyze_column("AAAA", options) == (ConservationDegree.HighlyConserved, False)
