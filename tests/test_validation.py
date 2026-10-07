#!/usr/bin/env python3
"""Test validation rules."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

def test_versions_file_exists():
    assert os.path.exists(os.path.join(ROOT, "data", "versions.yaml"))

def test_common_schema_exists():
    assert os.path.exists(os.path.join(ROOT, "schema", "common.schema.json"))

def test_timeout_types_hpp_exists():
    assert os.path.exists(os.path.join(ROOT, "include", "sim800_at_timeouts", "timeout_types.hpp"))
