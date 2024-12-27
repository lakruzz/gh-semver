import os
import sys
import pytest

# Add the subdirectory containing the classes to the general class_path
sys.path.append(
    os.path.dirname(os.path.abspath(__file__))+"/../.."
)

from classes.ghutils import Ghutils

@pytest.fixture
def org_repo():
    return "lakruzz/reporeport"

@pytest.mark.ghutils
def test_ghutils_get_org_repo_from_current_directory(org_repo):
    # Arrange
    expected = org_repo
    # Act
    actual = Ghutils.get_org_repo_from_current_directory()
    # Assert
    assert actual == expected
    
@pytest.fixture
def api():
    return 'mongodb/mongo'

@pytest.mark.dev
def test_ghutils_query_github_incl_headers(api, die_on_error=False):
    # Arrange
    returncode, responsebody, responseheader = Ghutils.query_github_incl_header(f"repos/{api}", die_on_error)
    expected_org,expected_repo = api.split("/")
    expected_returncode = 0
    expected_status_text = '200 OK'
    expected_status_code = '200'
    expected_header_server = 'GitHub.com'
    
    #Assert
    assert returncode == expected_returncode
    assert expected_org in responsebody["owner"]["login"]
    assert expected_repo in responsebody["name"]
    assert expected_header_server in responseheader["Server"]
    assert responseheader["Status-Text"] == expected_status_text
    assert responseheader["Status-Code"] == expected_status_code
    
@pytest.fixture
def badapi():
    return "repos/not_veru_likkely/mongobongo"


def test_bad_ghutils_query_github_incl_headers(badapi, die_on_error=False):
    # Arrange
    returncode, responsebody, responseheader = Ghutils.query_github_incl_header(f"{badapi}", die_on_error)
    expected_returncode = 1
    expected_status_code = '404'
    
    #Assert
    assert returncode == expected_returncode
    assert responseheader["Status-Code"] == expected_status_code