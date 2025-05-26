"""Tests for agent_test_dataset module.

Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0
"""

import json
import pytest
import tempfile
import yaml
from awslabs.agent_test.agent_test_dataset import AgentEvaluationDataset, AgentTestCase
from pathlib import Path


class TestAgentTestCase:
    """Test AgentTestCase dataclass."""

    def test_agent_test_case_creation(self):
        """Test creating an AgentTestCase."""
        test_case = AgentTestCase(
            input="What's the weather?", expected_tools=['get_weather'], description='Weather test'
        )
        assert test_case.input == "What's the weather?"
        assert test_case.expected_tools == ['get_weather']
        assert test_case.description == 'Weather test'

    def test_agent_test_case_without_description(self):
        """Test creating an AgentTestCase without description."""
        test_case = AgentTestCase(input="What's the time?", expected_tools=['get_time'])
        assert test_case.input == "What's the time?"
        assert test_case.expected_tools == ['get_time']
        assert test_case.description is None


class TestAgentEvaluationDataset:
    """Test AgentEvaluationDataset class."""

    def test_dataset_initialization(self):
        """Test dataset initialization."""
        test_cases = [AgentTestCase('input1', ['tool1']), AgentTestCase('input2', ['tool2'])]
        dataset = AgentEvaluationDataset(test_cases)
        assert len(dataset.test_cases) == 2
        assert dataset.test_cases[0].input == 'input1'
        assert dataset.test_cases[1].input == 'input2'

    def test_dataset_iteration(self):
        """Test dataset iteration."""
        test_cases = [AgentTestCase('input1', ['tool1']), AgentTestCase('input2', ['tool2'])]
        dataset = AgentEvaluationDataset(test_cases)

        # Test iteration
        iterated_cases = list(dataset)
        assert len(iterated_cases) == 2
        assert iterated_cases[0].input == 'input1'
        assert iterated_cases[1].input == 'input2'

    def test_from_yaml_valid_file(self):
        """Test loading from valid YAML file."""
        yaml_content = [
            {
                'input': "What's the weather?",
                'expected_tools': ['get_weather'],
                'description': 'Weather test',
            },
            {'input': "What's the time?", 'expected_tools': ['get_time']},
        ]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(yaml_content, f)
            yaml_path = f.name

        try:
            dataset = AgentEvaluationDataset.from_yaml(yaml_path)
            assert len(dataset.test_cases) == 2
            assert dataset.test_cases[0].input == "What's the weather?"
            assert dataset.test_cases[0].expected_tools == ['get_weather']
            assert dataset.test_cases[0].description == 'Weather test'
            assert dataset.test_cases[1].input == "What's the time?"
            assert dataset.test_cases[1].expected_tools == ['get_time']
            assert dataset.test_cases[1].description is None
        finally:
            Path(yaml_path).unlink()

    def test_from_yaml_file_not_found(self):
        """Test loading from non-existent YAML file."""
        with pytest.raises(FileNotFoundError):
            AgentEvaluationDataset.from_yaml('non_existent_file.yaml')

    def test_from_yaml_invalid_yaml(self):
        """Test loading from invalid YAML file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write('invalid: yaml: content: [')
            yaml_path = f.name

        try:
            with pytest.raises(yaml.YAMLError):
                AgentEvaluationDataset.from_yaml(yaml_path)
        finally:
            Path(yaml_path).unlink()

    def test_from_json_valid_file(self):
        """Test loading from valid JSON file."""
        json_content = [
            {
                'input': "What's the weather?",
                'expected_tools': ['get_weather'],
                'description': 'Weather test',
            },
            {'input': "What's the time?", 'expected_tools': ['get_time']},
        ]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(json_content, f)
            json_path = f.name

        try:
            dataset = AgentEvaluationDataset.from_json(json_path)
            assert len(dataset.test_cases) == 2
            assert dataset.test_cases[0].input == "What's the weather?"
            assert dataset.test_cases[0].expected_tools == ['get_weather']
            assert dataset.test_cases[0].description == 'Weather test'
            assert dataset.test_cases[1].input == "What's the time?"
            assert dataset.test_cases[1].expected_tools == ['get_time']
            assert dataset.test_cases[1].description is None
        finally:
            Path(json_path).unlink()

    def test_from_json_file_not_found(self):
        """Test loading from non-existent JSON file."""
        with pytest.raises(FileNotFoundError):
            AgentEvaluationDataset.from_json('non_existent_file.json')

    def test_from_json_invalid_json(self):
        """Test loading from invalid JSON file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{invalid json content')
            json_path = f.name

        try:
            with pytest.raises(json.JSONDecodeError):
                AgentEvaluationDataset.from_json(json_path)
        finally:
            Path(json_path).unlink()

    def test_from_json_missing_required_fields(self):
        """Test loading from JSON with missing required fields."""
        json_content = [
            {
                'input': "What's the weather?",
                # missing expected_tools
            }
        ]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(json_content, f)
            json_path = f.name

        try:
            with pytest.raises(TypeError):
                AgentEvaluationDataset.from_json(json_path)
        finally:
            Path(json_path).unlink()
