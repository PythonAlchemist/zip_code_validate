import pytest
import pandas as pd
from create_map import load_zip_data, check_valid_zip, parse_zip_str


@pytest.fixture
def mock_zip_data(tmp_path):
    """Create a mock zip_data.csv file for testing"""
    data = {
        "PHYSICAL ZIP": [12345, 67890],
        "PHYSICAL ZIP 4": [1234, 5678],
        "Data": ["A", "B"],
    }
    df = pd.DataFrame(data)
    csv_path = tmp_path / "zip_data.csv"
    df.to_csv(csv_path, index=False)
    return str(csv_path)


def test_load_zip_data(mock_zip_data):
    """Test the load_zip_data function"""
    path = mock_zip_data
    df = load_zip_data(path)
    # Perform assertions on the DataFrame
    assert isinstance(df, pd.DataFrame)
    assert df.index.names == ["PHYSICAL ZIP", "PHYSICAL ZIP 4"]


@pytest.mark.parametrize(
    "zip_str, expected",
    [
        ("00601", (601, None)),
        ("00601-9998", (601, 9998)),
        ("00601-99", (601, None)),
        ("006019998", (601, 9998)),
        ("0060", (None, None)),
        ("28262", (28262, None)),
        ("28262-1234", (28262, 1234)),
        ("28262-123", (28262, None)),
        ("28262-9191", (28262, 9191)),
    ],
)
def test_parse_zip_str(zip_str, expected):
    """Test the parse_zip_str function"""
    zip, zip4 = parse_zip_str(zip_str)
    assert zip == expected[0]
    assert zip4 == expected[1]


@pytest.mark.parametrize(
    "zip_obj, expected",
    [
        ((601, None), 1),
        ((601, 9998), 1),
        ((None, None), 0),
        ((None, 9998), 0),
        ((601, 99), 0),
    ],
)
def test_check_valid_zip(mock_zip_data, zip_obj, expected):
    """Test the check_valid_zip function"""
    path = mock_zip_data
    df = load_zip_data(path)
    result = check_valid_zip(df, zip_obj)
    assert result == expected
