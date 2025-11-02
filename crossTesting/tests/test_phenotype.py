import pytest
from pyUpdatedto3.phenotype import pheno

# You can reuse the mock functions defined in conftest.py
# by listing them as arguments to your test function.


def test_pheno_ocellaris_same_parents(mock_fmtIt, mock_newPhen):
    """Tests the case where both parents are ocellaris and have the same genotype."""
    genotype = "Sf/+"
    parent1 = 'Amphiprion ocellaris "Black Ice"'
    parent2 = 'Amphiprion ocellaris "Black Ice"'

    result = pheno(genotype, parent1, parent2)

    expected = '<i>Amphiprion ocellaris</i> "Black Ice"), Sf/+)'
    assert result == expected
    # Additional assertions to check if the mock functions were called correctly can be added.
    # For example, mock_newPhen.assert_called_once()


def test_pheno_mocha_genetics_ocellaris_same_parents(mock_fmtIt):
    """Tests the specific case involving "Mocha genetics"."""
    genotype = "+/+"
    parent1 = 'Amphiprion "Black Ice"'
    parent2 = 'Amphiprion "Black Ice"'

    result = pheno(genotype, parent1, parent2)

    assert result == "Amphiprion (Mocha genetics)"


def test_pheno_percula_and_ocellaris(mock_fmtIt):
    """Tests the cross between percula and ocellaris."""
    genotype = "P/+"
    parent1 = "Amphiprion percula"
    parent2 = "Amphiprion ocellaris"

    result = pheno(genotype, parent1, parent2)

    assert result == 'Amphiprion "Percularis"'


def test_pheno_unknown_parents(mock_fmtIt):
    """Tests the final 'else' block."""
    genotype = "Unknown"
    parent1 = "ParentA"
    parent2 = "ParentB"

    result = pheno(genotype, parent1, parent2)

    assert result == "Unknown phenotype"
