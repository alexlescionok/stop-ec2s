from src import functions
import pytest

### get_instances()
@pytest.mark.parametrize(
    "invalid_input,description",
    [
        (12345, "int input"),
        (None, "None input"),
        (['list'], "list input"),
    ]
)
def test_get_instances_non_string_input(invalid_input, description):
    """Test function to confirm that get_instances() only accepts a string argument and raises a TypeError exception is the argument is not a string.
    
    Parameters
    ----------
    invalid_input: !str
        The argument that will cause get_instances() to raise a TypeError exception.
    description: str
        A description to include in the pytest.fail() message.
    """
    try:
        with pytest.raises(TypeError, match="string_to_match must be a string"):
            functions.get_instances(invalid_input)
    except AssertionError:
        pytest.fail(f"Expected TypeError when passing {description} to get_instances")


def test_get_instances_matching_string(mocker):
    """Test function to confirm that get_instances() returns a list with an EC2 id (fake) if there are running EC2 instances that match the supplied string.
    
    Parameters
    ----------
    mocker: pytest_mock.plugin.MockerFixture
        A wrapper around Python’s built-in unittest.mock module, designed to integrate smoothly with pytest.
    """
    matching_string_fake_response = [
        {
            'Reservations': [
                {'Instances': [{'InstanceId': 'i-mock-id'}]}
            ]
        }
    ]
    mocker.patch.object(functions.paginator, 'paginate', return_value=matching_string_fake_response)
    result = functions.get_instances("matching-string")
    assert result == ['i-mock-id'], "Should be [i-mock-id]"

def test_get_instances_non_matching_string(mocker):
    """Test function to confirm that get_instances() returns an empty list if there are no running EC2 instances that match the supplied string.
    
    Parameters
    ----------
    mocker: pytest_mock.plugin.MockerFixture
        A wrapper around Python’s built-in unittest.mock module, designed to integrate smoothly with pytest.
    """
    non_matching_string_fake_response = [
        {
            'Reservations': []
        }
    ]
    mocker.patch.object(functions.paginator, 'paginate', return_value=non_matching_string_fake_response)
    result = functions.get_instances("non-matching-string")
    assert result == [], "Should be []"

### get_instances()