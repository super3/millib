import pytest
import copy
from tasks import convert_btc_log, IncorrectValue

VALID_DATA = {'timestamp': 'Fri, 29 Nov 2013 12:04:30 -0000',
              '24h_avg': 1052.01,
              'bid': 1096.51,
              'last': 1099.07,
              'ask': 1098.87,
              'total_vol': 117275.74}


def test_convert_btc_log_with_valid_data():
    # copy data to avoid side effect
    data = copy.deepcopy(VALID_DATA)
    converted = convert_btc_log(data)

    assert converted['24h_avg'] == 1052.01
    assert converted['bid'] == 1096.51
    assert converted['last'] == 1099.07
    assert converted['ask'] == 1098.87
    assert converted['total_vol'] == 117275.74
    assert converted['unix_timestamp'] == 1385726670


def test_convert_btc_log_with_invalid_data():

    for key in ('24h_avg', 'ask', 'bid', 'last', 'total_vol',):
        data = copy.deepcopy(VALID_DATA)
        data[key] = 'some incorrect value'

        with pytest.raises(IncorrectValue):
            convert_btc_log(data)

    data = copy.deepcopy(VALID_DATA)
    data['timestamp'] = '2013/2013/2013'

    with pytest.raises(IncorrectValue):
        convert_btc_log(data)