import boto3
import configparser
import moto
import os
import pytest
import sys
from loguru import logger


# Get the log level from the environment variable
log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()

logger.remove()
logger.add(sys.stdout, level=log_level)


@pytest.fixture
def moto_env(monkeypatch):
    """Set up the moto environment."""
    monkeypatch.setenv('AWS_ACCESS_KEY_ID', 'test')
    monkeypatch.setenv('AWS_SECRET_ACCESS_KEY', 'test')
    monkeypatch.setenv('AWS_SECURITY_TOKEN', 'test')
    monkeypatch.setenv('AWS_DEFAULT_REGION', 'us-west-2')


@pytest.fixture
def moto_mock_aws():
    """Mock the AWS environment."""
    with moto.mock_aws():
        yield


@pytest.fixture
def moto_cloudwatch_client():
    """Get the CloudWatch client."""
    return boto3.client('cloudwatch')


@pytest.fixture
def boto3_profile_name():
    """Get the boto3 profile name."""
    return 'test-profile'


@pytest.fixture
def boto3_profile(boto3_profile_name):
    """Get the boto3 profile."""
    config = configparser.ConfigParser()
    config[boto3_profile_name] = {
        'aws_access_key_id': 'test',  # pragma: allowlist secret
        'aws_secret_access_key': 'test',  # pragma: allowlist secret
    }

    return config


@pytest.fixture
def boto3_profile_path(boto3_profile, tmp_path, monkeypatch):
    """Get the boto3 profile path."""
    path = tmp_path / '.aws/credentials'
    path.parent.mkdir(exist_ok=True)
    with path.open('w') as fp:
        boto3_profile.write(fp)

    monkeypatch.setenv('AWS_SHARED_CREDENTIALS_FILE', str(path))

    return path
