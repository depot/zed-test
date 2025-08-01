#!/usr/bin/env python3
import json
from datetime import datetime

def parse_duration(start_time, end_time):
    """Parse ISO timestamps and return duration in minutes and seconds"""
    start = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
    end = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
    duration = end - start
    total_seconds = int(duration.total_seconds())
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes}m {seconds}s", total_seconds

def extract_step_duration(steps, step_name):
    """Extract duration for a specific step"""
    for step in steps:
        if step['name'] == step_name:
            return parse_duration(step['started_at'], step['completed_at'])
    return "Not found", 0

# Workflow data from the API responses
workflows = {
    "test-baseline": {
        "run_id": 16666952853,
        "steps": [
            {"name":"Set up job","started_at":"2025-08-01T05:16:37Z","completed_at":"2025-08-01T05:16:38Z"},
            {"name":"Checkout code","started_at":"2025-08-01T05:16:38Z","completed_at":"2025-08-01T05:16:56Z"},
            {"name":"Install system dependencies","started_at":"2025-08-01T05:16:56Z","completed_at":"2025-08-01T05:17:40Z"},
            {"name":"Install Rust","started_at":"2025-08-01T05:17:40Z","completed_at":"2025-08-01T05:17:49Z"},
            {"name":"Setup Rust toolchain","started_at":"2025-08-01T05:17:49Z","completed_at":"2025-08-01T05:18:06Z"},
            {"name":"Run tests","started_at":"2025-08-01T05:18:06Z","completed_at":"2025-08-01T05:33:17Z"},
            {"name":"Build Zed (release)","started_at":"2025-08-01T05:33:17Z","completed_at":"2025-08-01T05:44:57Z"}
        ]
    },
    "test-mold": {
        "run_id": 16666952977,
        "steps": [
            {"name":"Set up job","started_at":"2025-08-01T05:16:37Z","completed_at":"2025-08-01T05:17:15Z"},
            {"name":"Checkout code","started_at":"2025-08-01T05:17:15Z","completed_at":"2025-08-01T05:17:33Z"},
            {"name":"Install system dependencies","started_at":"2025-08-01T05:17:33Z","completed_at":"2025-08-01T05:18:15Z"},
            {"name":"Install Rust","started_at":"2025-08-01T05:18:15Z","completed_at":"2025-08-01T05:18:25Z"},
            {"name":"Setup Rust toolchain","started_at":"2025-08-01T05:18:25Z","completed_at":"2025-08-01T05:18:42Z"},
            {"name":"Run tests","started_at":"2025-08-01T05:18:42Z","completed_at":"2025-08-01T05:33:58Z"},
            {"name":"Build Zed (release)","started_at":"2025-08-01T05:33:58Z","completed_at":"2025-08-01T05:45:23Z"}
        ]
    },
    "test-mold-tests-only": {
        "run_id": 16666953136,
        "steps": [
            {"name":"Set up job","started_at":"2025-08-01T05:16:44Z","completed_at":"2025-08-01T05:16:46Z"},
            {"name":"Checkout code","started_at":"2025-08-01T05:16:46Z","completed_at":"2025-08-01T05:17:03Z"},
            {"name":"Install system dependencies","started_at":"2025-08-01T05:17:03Z","completed_at":"2025-08-01T05:17:53Z"},
            {"name":"Install Rust","started_at":"2025-08-01T05:17:53Z","completed_at":"2025-08-01T05:18:02Z"},
            {"name":"Setup Rust toolchain","started_at":"2025-08-01T05:18:02Z","completed_at":"2025-08-01T05:18:19Z"},
            {"name":"Run tests","started_at":"2025-08-01T05:18:19Z","completed_at":"2025-08-01T05:33:31Z"},
            {"name":"Build Zed (release)","started_at":"2025-08-01T05:33:31Z","completed_at":"2025-08-01T05:44:56Z"}
        ]
    },
    "test-nightly": {
        "run_id": 16666953292,
        "steps": [
            {"name":"Set up job","started_at":"2025-08-01T05:16:38Z","completed_at":"2025-08-01T05:16:39Z"},
            {"name":"Checkout code","started_at":"2025-08-01T05:16:39Z","completed_at":"2025-08-01T05:16:58Z"},
            {"name":"Install system dependencies","started_at":"2025-08-01T05:16:58Z","completed_at":"2025-08-01T05:17:41Z"},
            {"name":"Install Rust","started_at":"2025-08-01T05:17:41Z","completed_at":"2025-08-01T05:17:51Z"},
            {"name":"Setup Rust toolchain","started_at":"2025-08-01T05:17:51Z","completed_at":"2025-08-01T05:18:07Z"},
            {"name":"Run tests","started_at":"2025-08-01T05:18:07Z","completed_at":"2025-08-01T05:33:32Z"},
            {"name":"Build Zed (release)","started_at":"2025-08-01T05:33:32Z","completed_at":"2025-08-01T05:42:23Z"}
        ]
    },
    "test-cache": {
        "run_id": 16666953446,
        "steps": [
            {"name":"Set up job","started_at":"2025-08-01T05:16:38Z","completed_at":"2025-08-01T05:16:39Z"},
            {"name":"Checkout code","started_at":"2025-08-01T05:16:39Z","completed_at":"2025-08-01T05:16:58Z"},
            {"name":"Install system dependencies","started_at":"2025-08-01T05:16:58Z","completed_at":"2025-08-01T05:17:37Z"},
            {"name":"Install Rust","started_at":"2025-08-01T05:17:37Z","completed_at":"2025-08-01T05:17:46Z"},
            {"name":"Setup Rust toolchain","started_at":"2025-08-01T05:17:46Z","completed_at":"2025-08-01T05:18:03Z"},
            {"name":"Cache cargo dependencies","started_at":"2025-08-01T05:18:03Z","completed_at":"2025-08-01T05:18:05Z"},
            {"name":"Run tests","started_at":"2025-08-01T05:18:05Z","completed_at":"2025-08-01T05:32:48Z"},
            {"name":"Build Zed (release)","started_at":"2025-08-01T05:32:48Z","completed_at":"2025-08-01T05:41:29Z"}
        ]
    },
    "test-cranelift": {
        "run_id": 16666953832,
        "steps": [
            {"name":"Set up job","started_at":"2025-08-01T05:17:17Z","completed_at":"2025-08-01T05:17:18Z"},
            {"name":"Checkout code","started_at":"2025-08-01T05:17:18Z","completed_at":"2025-08-01T05:17:35Z"},
            {"name":"Install system dependencies","started_at":"2025-08-01T05:17:35Z","completed_at":"2025-08-01T05:18:15Z"},
            {"name":"Install Rust","started_at":"2025-08-01T05:18:15Z","completed_at":"2025-08-01T05:18:25Z"},
            {"name":"Install depot CLI","started_at":"2025-08-01T05:18:25Z","completed_at":"2025-08-01T05:18:25Z"},
            {"name":"Setup Rust toolchain","started_at":"2025-08-01T05:18:25Z","completed_at":"2025-08-01T05:18:42Z"},
            {"name":"Cache cargo dependencies","started_at":"2025-08-01T05:18:42Z","completed_at":"2025-08-01T05:18:44Z"},
            {"name":"Run tests","started_at":"2025-08-01T05:18:44Z","completed_at":"2025-08-01T05:19:31Z"},
            {"name":"Build Zed (release)","started_at":"2025-08-01T05:19:31Z","completed_at":"2025-08-01T05:41:48Z"}
        ]
    }
}

print("# GitHub Actions Workflow Timing Analysis")
print()
print("| Branch | Test Duration | Build Duration | Total Duration |")
print("|--------|---------------|----------------|----------------|")

for workflow_name, data in workflows.items():
    test_duration, test_seconds = extract_step_duration(data['steps'], 'Run tests')
    build_duration, build_seconds = extract_step_duration(data['steps'], 'Build Zed (release)')
    
    total_seconds = test_seconds + build_seconds
    total_minutes = total_seconds // 60
    total_remaining_seconds = total_seconds % 60
    total_duration = f"{total_minutes}m {total_remaining_seconds}s"
    
    print(f"| {workflow_name} | {test_duration} | {build_duration} | {total_duration} |")

print()
print("## Detailed Analysis")
print()

for workflow_name, data in workflows.items():
    test_duration, test_seconds = extract_step_duration(data['steps'], 'Run tests')
    build_duration, build_seconds = extract_step_duration(data['steps'], 'Build Zed (release)')
    
    print(f"### {workflow_name}")
    print(f"- Run ID: {data['run_id']}")
    print(f"- Test Duration: {test_duration} ({test_seconds} seconds)")
    print(f"- Build Duration: {build_duration} ({build_seconds} seconds)")
    print(f"- Combined: {test_seconds + build_seconds} seconds")
    print()