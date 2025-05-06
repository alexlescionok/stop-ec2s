from src import functions
import pytest

### get_instances()
@pytest.mark.parametrize(
    "non_string_input,non_string_description",
    [
        (12345, "int input"),
        (None, "None input"),
        (["list"], "list input"),
    ]
)
def test_get_instances_non_string_input(non_string_input, non_string_description):
    """Test function to confirm that get_instances() only accepts a string argument and raises a TypeError exception is the argument is not a string.
    
    Parameters
    ----------
    non_string_input: !str
        The argument that will cause get_instances() to raise a TypeError exception.
    non_string_description: str
        A description to include in the pytest.fail() message.
    """
    try:
        with pytest.raises(TypeError, match="string_to_match must be a string. Ending operation here."):
            functions.get_instances(non_string_input)
    except AssertionError:
        pytest.fail(f"Expected TypeError when passing {non_string_description} to get_instances().")


def test_get_instances_matching_string(mocker):
    """Test function to confirm that get_instances() returns a list with an EC2 id (mock) if there are running EC2 instances that match the supplied string.
    
    Parameters
    ----------
    mocker: pytest_mock.plugin.MockerFixture
        A wrapper around Python’s built-in unittest.mock module, designed to integrate smoothly with pytest.
    """
    matching_string_mock_response = [
        {
            "Reservations": [
                {"Instances": [{"InstanceId": "i-mock-id"}]}
            ]
        }
    ]
    mocker.patch.object(functions.paginator, "paginate", return_value=matching_string_mock_response)
    result = functions.get_instances("matching-string")
    assert result == ["i-mock-id"], "Should be [i-mock-id]"

def test_get_instances_non_matching_string(mocker):
    """Test function to confirm that get_instances() returns an empty list if there are no running EC2 instances that match the supplied string.
    
    Parameters
    ----------
    mocker: pytest_mock.plugin.MockerFixture
        A wrapper around Python’s built-in unittest.mock module, designed to integrate smoothly with pytest.
    """
    non_matching_string_mock_response = [
        {
            "Reservations": []
        }
    ]
    mocker.patch.object(functions.paginator, "paginate", return_value=non_matching_string_mock_response)
    result = functions.get_instances("non-matching-string")
    assert result == [], "Should be []"

### stop_instances()
@pytest.mark.parametrize(
    "non_list_input,non_list_description",
    [
        (12345, "int input"),
        (None, "None input"),
        ("string", "string input"),
    ]
)
def test_stop_instances_non_list_input(non_list_input, non_list_description):
    """Test function to confirm that stop_instances() only accepts a list argument and raises a TypeError exception is the argument is not a list.
    
    Parameters
    ----------
    non_list_input: !list
        The argument that will cause stop_instances() to raise a TypeError exception.
    non_list_description: str
        A description to include in the pytest.fail() message.
    """
    try:
        with pytest.raises(TypeError, match="instances must be a list. Ending operation here."):
            functions.stop_instances(non_list_input)
    except AssertionError:
        pytest.fail(f"Expected TypeError when passing {non_list_description} to stop_instances().")

def test_stop_instances_success(mocker):
    """Test function to confirm that stop_instances() returns a dictionary with the following format: {"success": True, "stopped_instances": [ids]}.
    
    Parameters
    ----------
    mocker: pytest_mock.plugin.MockerFixture
        A wrapper around Python’s built-in unittest.mock module, designed to integrate smoothly with pytest.
    """
    mock_instance_ids = ["i-mock-id-1", "i-mock-id-2", "i-mock-id-3"]
    mock_response = {
        "StoppingInstances": [{"InstanceId": id} for id in mock_instance_ids]
    }
    mock_stop_instances = mocker.patch.object(functions.ec2_client, "stop_instances", return_value=mock_response)
    result = functions.stop_instances(mock_instance_ids)

    mock_stop_instances.assert_called_once_with(InstanceIds=mock_instance_ids)
    assert result == {
        "success": True,
        "stopped_instances": mock_instance_ids
    }

def test_stop_instances_exception(mocker):
    """Test that stop_instances() gracefully handles exceptions and returns a dictionary with the following format: {"success": False, "error": "<value>"}.
    
    Parameters
    ----------
    mocker: pytest_mock.plugin.MockerFixture
        A wrapper around Python’s built-in unittest.mock module, designed to integrate smoothly with pytest.
    """
    mock_instance_ids = ["i-mock-id-1", "i-mock-id-2", "i-mock-id-3"]
    error_message = "Simulated boto3 error"

    # Mock ec2_client.stop_instances to raise an Exception
    mocker.patch.object(functions.ec2_client, "stop_instances", side_effect=Exception(error_message))

    result = functions.stop_instances(mock_instance_ids)

    # Check that the function handled the error properly
    assert result["success"] is False
    assert error_message in result["error"]