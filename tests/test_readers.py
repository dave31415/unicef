from unicef import parse_old


def test_read_breast_feeding_values():
    tol = 1e-7
    data = parse_old.parse_mics_breastfeeding()

    value = data['Sex']['Male']['Children 12-15 months']['Percent breastfed (Continued breastfeeding at 1 year) [3]']
    expected = 95.76357893911755
    assert (value - expected) < tol

    value = data['Sex']['Female']['Children 12-15 months']['Percent breastfed (Continued breastfeeding at 1 year) [3]']
    expected = 94.92525944783988
    assert (value - expected) < tol

    value = data['Religion of household head']['Islam']['Children 20-23 months']['Percent breastfed (Continued breastfeeding at 2 years) [4]']
    expected = 86.65590185936487
    assert (value - expected) < tol

    value = data['Area']['Urban']['Children 20-23 months']['Number of children']
    expected =  262.19502505593204
    assert (value - expected) < tol

    expected_keys = [u'Division', u'Area', u"Mother's education", u'Sex', u'Religion of household head',
                     u'Total', u'Wealth index quintile']
    assert data.keys() == expected_keys


def test_read_breast_feeding_columns():
    data = parse_old.parse_mics_breastfeeding()
    keys = data['Sex']['Female']['Children 0-5 months'].keys()
    n_keys = len(keys)
    print keys
    assert n_keys == 3


def test_totals_totals():
    data = parse_old.parse_mics_breastfeeding()
    keys = data['Total']['Total'].keys()
    expected = [u'Children 12-15 months', u'Children 20-23 months', u'Children 0-5 months']
