#!/usr/bin/env python3
"""
Parse GitHub Actions workflow timing data and calculate performance metrics.
"""

import json
from datetime import datetime
from typing import Dict, List, Tuple

def parse_time(time_str: str) -> datetime:
    """Parse ISO 8601 timestamp."""
    return datetime.fromisoformat(time_str.replace('Z', '+00:00'))

def calculate_duration(start: str, end: str) -> int:
    """Calculate duration in seconds between two timestamps."""
    start_time = parse_time(start)
    end_time = parse_time(end)
    return int((end_time - start_time).total_seconds())

def extract_step_duration(steps: List[Dict], step_name: str) -> int:
    """Extract duration for a specific step."""
    for step in steps:
        if step['name'] == step_name:
            return calculate_duration(step['started_at'], step['completed_at'])
    return 0

def format_duration(seconds: int) -> str:
    """Format duration in minutes and seconds."""
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes}m {secs}s"

def calculate_percentage_change(baseline: int, value: int) -> str:
    """Calculate percentage change from baseline."""
    if baseline == 0:
        return "N/A"
    change = ((value - baseline) / baseline) * 100
    sign = "+" if change > 0 else ""
    return f"{sign}{change:.1f}%"

# Workflow run data
workflows = [
    {
        "name": "test-baseline",
        "run_id": "16666952853",
        "data": {"total_count":1,"jobs":[{"id":47175109278,"run_id":16666952853,"workflow_name":"Build Zed","head_branch":"test-baseline","run_url":"https://api.github.com/repos/depot/zed-test/actions/runs/16666952853","run_attempt":1,"node_id":"CR_kwDOPUJXr88AAAAK-9sKng","head_sha":"680ae6d4b0e35e7089abe9bb464223ac73af42d0","url":"https://api.github.com/repos/depot/zed-test/actions/jobs/47175109278","html_url":"https://github.com/depot/zed-test/actions/runs/16666952853/job/47175109278","status":"completed","conclusion":"success","created_at":"2025-08-01T05:16:20Z","started_at":"2025-08-01T05:16:21Z","completed_at":"2025-08-01T05:44:59Z","name":"build","steps":[{"name":"Set up job","status":"completed","conclusion":"success","number":1,"started_at":"2025-08-01T05:16:37Z","completed_at":"2025-08-01T05:16:38Z"},{"name":"Checkout code","status":"completed","conclusion":"success","number":2,"started_at":"2025-08-01T05:16:38Z","completed_at":"2025-08-01T05:16:56Z"},{"name":"Install system dependencies","status":"completed","conclusion":"success","number":3,"started_at":"2025-08-01T05:16:56Z","completed_at":"2025-08-01T05:17:40Z"},{"name":"Install Rust","status":"completed","conclusion":"success","number":4,"started_at":"2025-08-01T05:17:40Z","completed_at":"2025-08-01T05:17:49Z"},{"name":"Setup Rust toolchain","status":"completed","conclusion":"success","number":5,"started_at":"2025-08-01T05:17:49Z","completed_at":"2025-08-01T05:18:06Z"},{"name":"Run tests","status":"completed","conclusion":"success","number":6,"started_at":"2025-08-01T05:18:06Z","completed_at":"2025-08-01T05:33:17Z"},{"name":"Build Zed (release)","status":"completed","conclusion":"success","number":7,"started_at":"2025-08-01T05:33:17Z","completed_at":"2025-08-01T05:44:57Z"},{"name":"Post Checkout code","status":"completed","conclusion":"success","number":14,"started_at":"2025-08-01T05:44:57Z","completed_at":"2025-08-01T05:44:57Z"},{"name":"Complete job","status":"completed","conclusion":"success","number":15,"started_at":"2025-08-01T05:44:57Z","completed_at":"2025-08-01T05:44:57Z"}],"check_run_url":"https://api.github.com/repos/depot/zed-test/check-runs/47175109278","labels":["depot-ubuntu-latest-8"],"runner_id":185123,"runner_name":"depot-g34jmw54wh","runner_group_id":1,"runner_group_name":"default"}]}
    },
    {
        "name": "test-mold",
        "run_id": "16666952977",
        "data": {"total_count":1,"jobs":[{"id":47175109505,"run_id":16666952977,"workflow_name":"Build Zed","head_branch":"test-mold","run_url":"https://api.github.com/repos/depot/zed-test/actions/runs/16666952977","run_attempt":1,"node_id":"CR_kwDOPUJXr88AAAAK-9sLgQ","head_sha":"d120735c82caeaf1a866f975aed2420e017c4605","url":"https://api.github.com/repos/depot/zed-test/actions/jobs/47175109505","html_url":"https://github.com/depot/zed-test/actions/runs/16666952977/job/47175109505","status":"completed","conclusion":"success","created_at":"2025-08-01T05:16:21Z","started_at":"2025-08-01T05:16:21Z","completed_at":"2025-08-01T05:45:25Z","name":"build","steps":[{"name":"Set up job","status":"completed","conclusion":"success","number":1,"started_at":"2025-08-01T05:16:37Z","completed_at":"2025-08-01T05:17:15Z"},{"name":"Checkout code","status":"completed","conclusion":"success","number":2,"started_at":"2025-08-01T05:17:15Z","completed_at":"2025-08-01T05:17:33Z"},{"name":"Install system dependencies","status":"completed","conclusion":"success","number":3,"started_at":"2025-08-01T05:17:33Z","completed_at":"2025-08-01T05:18:15Z"},{"name":"Install Rust","status":"completed","conclusion":"success","number":4,"started_at":"2025-08-01T05:18:15Z","completed_at":"2025-08-01T05:18:25Z"},{"name":"Setup Rust toolchain","status":"completed","conclusion":"success","number":5,"started_at":"2025-08-01T05:18:25Z","completed_at":"2025-08-01T05:18:42Z"},{"name":"Run tests","status":"completed","conclusion":"success","number":6,"started_at":"2025-08-01T05:18:42Z","completed_at":"2025-08-01T05:33:58Z"},{"name":"Build Zed (release)","status":"completed","conclusion":"success","number":7,"started_at":"2025-08-01T05:33:58Z","completed_at":"2025-08-01T05:45:23Z"},{"name":"Post Checkout code","status":"completed","conclusion":"success","number":14,"started_at":"2025-08-01T05:45:23Z","completed_at":"2025-08-01T05:45:23Z"},{"name":"Complete job","status":"completed","conclusion":"success","number":15,"started_at":"2025-08-01T05:45:23Z","completed_at":"2025-08-01T05:45:23Z"}],"check_run_url":"https://api.github.com/repos/depot/zed-test/check-runs/47175109505","labels":["depot-ubuntu-latest-8"],"runner_id":185134,"runner_name":"depot-v5nwfgqsm8","runner_group_id":1,"runner_group_name":"default"}]}
    },
    {
        "name": "test-mold-tests-only",
        "run_id": "16666953136",
        "data": {"total_count":1,"jobs":[{"id":47175109963,"run_id":16666953136,"workflow_name":"Build Zed","head_branch":"test-mold-tests-only","run_url":"https://api.github.com/repos/depot/zed-test/actions/runs/16666953136","run_attempt":1,"node_id":"CR_kwDOPUJXr88AAAAK-9sNSw","head_sha":"fc0364e9edc6e242088b8debdbe8a495dbc90e35","url":"https://api.github.com/repos/depot/zed-test/actions/jobs/47175109963","html_url":"https://github.com/depot/zed-test/actions/runs/16666953136/job/47175109963","status":"completed","conclusion":"success","created_at":"2025-08-01T05:16:21Z","started_at":"2025-08-01T05:16:22Z","completed_at":"2025-08-01T05:44:58Z","name":"build","steps":[{"name":"Set up job","status":"completed","conclusion":"success","number":1,"started_at":"2025-08-01T05:16:44Z","completed_at":"2025-08-01T05:16:46Z"},{"name":"Checkout code","status":"completed","conclusion":"success","number":2,"started_at":"2025-08-01T05:16:46Z","completed_at":"2025-08-01T05:17:03Z"},{"name":"Install system dependencies","status":"completed","conclusion":"success","number":3,"started_at":"2025-08-01T05:17:03Z","completed_at":"2025-08-01T05:17:53Z"},{"name":"Install Rust","status":"completed","conclusion":"success","number":4,"started_at":"2025-08-01T05:17:53Z","completed_at":"2025-08-01T05:18:02Z"},{"name":"Setup Rust toolchain","status":"completed","conclusion":"success","number":5,"started_at":"2025-08-01T05:18:02Z","completed_at":"2025-08-01T05:18:19Z"},{"name":"Run tests","status":"completed","conclusion":"success","number":6,"started_at":"2025-08-01T05:18:19Z","completed_at":"2025-08-01T05:33:31Z"},{"name":"Build Zed (release)","status":"completed","conclusion":"success","number":7,"started_at":"2025-08-01T05:33:31Z","completed_at":"2025-08-01T05:44:56Z"},{"name":"Post Checkout code","status":"completed","conclusion":"success","number":14,"started_at":"2025-08-01T05:44:56Z","completed_at":"2025-08-01T05:44:57Z"},{"name":"Complete job","status":"completed","conclusion":"success","number":15,"started_at":"2025-08-01T05:44:57Z","completed_at":"2025-08-01T05:44:57Z"}],"check_run_url":"https://api.github.com/repos/depot/zed-test/check-runs/47175109963","labels":["depot-ubuntu-latest-8"],"runner_id":185152,"runner_name":"depot-h9z014vhnn","runner_group_id":1,"runner_group_name":"default"}]}
    },
    {
        "name": "test-nightly",
        "run_id": "16666953292",
        "data": {"total_count":1,"jobs":[{"id":47175110411,"run_id":16666953292,"workflow_name":"Build Zed","head_branch":"test-nightly","run_url":"https://api.github.com/repos/depot/zed-test/actions/runs/16666953292","run_attempt":1,"node_id":"CR_kwDOPUJXr88AAAAK-9sPCw","head_sha":"6c11f42381bf9ba6824d6f6316348fe554b456fa","url":"https://api.github.com/repos/depot/zed-test/actions/jobs/47175110411","html_url":"https://github.com/depot/zed-test/actions/runs/16666953292/job/47175110411","status":"completed","conclusion":"success","created_at":"2025-08-01T05:16:22Z","started_at":"2025-08-01T05:16:23Z","completed_at":"2025-08-01T05:42:25Z","name":"build","steps":[{"name":"Set up job","status":"completed","conclusion":"success","number":1,"started_at":"2025-08-01T05:16:38Z","completed_at":"2025-08-01T05:16:39Z"},{"name":"Checkout code","status":"completed","conclusion":"success","number":2,"started_at":"2025-08-01T05:16:39Z","completed_at":"2025-08-01T05:16:58Z"},{"name":"Install system dependencies","status":"completed","conclusion":"success","number":3,"started_at":"2025-08-01T05:16:58Z","completed_at":"2025-08-01T05:17:41Z"},{"name":"Install Rust","status":"completed","conclusion":"success","number":4,"started_at":"2025-08-01T05:17:41Z","completed_at":"2025-08-01T05:17:51Z"},{"name":"Setup Rust toolchain","status":"completed","conclusion":"success","number":5,"started_at":"2025-08-01T05:17:51Z","completed_at":"2025-08-01T05:18:07Z"},{"name":"Run tests","status":"completed","conclusion":"success","number":6,"started_at":"2025-08-01T05:18:07Z","completed_at":"2025-08-01T05:33:32Z"},{"name":"Build Zed (release)","status":"completed","conclusion":"success","number":7,"started_at":"2025-08-01T05:33:32Z","completed_at":"2025-08-01T05:42:23Z"},{"name":"Post Checkout code","status":"completed","conclusion":"success","number":14,"started_at":"2025-08-01T05:42:23Z","completed_at":"2025-08-01T05:42:23Z"},{"name":"Complete job","status":"completed","conclusion":"success","number":15,"started_at":"2025-08-01T05:42:23Z","completed_at":"2025-08-01T05:42:24Z"}],"check_run_url":"https://api.github.com/repos/depot/zed-test/check-runs/47175110411","labels":["depot-ubuntu-latest-8"],"runner_id":185130,"runner_name":"depot-ljjtr0dk97","runner_group_id":1,"runner_group_name":"default"}]}
    },
    {
        "name": "test-cache",
        "run_id": "16666953446",
        "data": {"total_count":1,"jobs":[{"id":47175110834,"run_id":16666953446,"workflow_name":"Build Zed","head_branch":"test-cache","run_url":"https://api.github.com/repos/depot/zed-test/actions/runs/16666953446","run_attempt":1,"node_id":"CR_kwDOPUJXr88AAAAK-9sQsg","head_sha":"3bbfd9027b0358b4acf60936c936aad21be8d1bc","url":"https://api.github.com/repos/depot/zed-test/actions/jobs/47175110834","html_url":"https://github.com/depot/zed-test/actions/runs/16666953446/job/47175110834","status":"completed","conclusion":"success","created_at":"2025-08-01T05:16:23Z","started_at":"2025-08-01T05:16:23Z","completed_at":"2025-08-01T05:41:38Z","name":"build","steps":[{"name":"Set up job","status":"completed","conclusion":"success","number":1,"started_at":"2025-08-01T05:16:38Z","completed_at":"2025-08-01T05:16:39Z"},{"name":"Checkout code","status":"completed","conclusion":"success","number":2,"started_at":"2025-08-01T05:16:39Z","completed_at":"2025-08-01T05:16:58Z"},{"name":"Install system dependencies","status":"completed","conclusion":"success","number":3,"started_at":"2025-08-01T05:16:58Z","completed_at":"2025-08-01T05:17:37Z"},{"name":"Install Rust","status":"completed","conclusion":"success","number":4,"started_at":"2025-08-01T05:17:37Z","completed_at":"2025-08-01T05:17:46Z"},{"name":"Setup Rust toolchain","status":"completed","conclusion":"success","number":5,"started_at":"2025-08-01T05:17:46Z","completed_at":"2025-08-01T05:18:03Z"},{"name":"Cache cargo dependencies","status":"completed","conclusion":"success","number":6,"started_at":"2025-08-01T05:18:03Z","completed_at":"2025-08-01T05:18:05Z"},{"name":"Run tests","status":"completed","conclusion":"success","number":7,"started_at":"2025-08-01T05:18:05Z","completed_at":"2025-08-01T05:32:48Z"},{"name":"Build Zed (release)","status":"completed","conclusion":"success","number":8,"started_at":"2025-08-01T05:32:48Z","completed_at":"2025-08-01T05:41:29Z"},{"name":"Post Cache cargo dependencies","status":"completed","conclusion":"success","number":15,"started_at":"2025-08-01T05:41:29Z","completed_at":"2025-08-01T05:41:37Z"},{"name":"Post Checkout code","status":"completed","conclusion":"success","number":16,"started_at":"2025-08-01T05:41:37Z","completed_at":"2025-08-01T05:41:37Z"},{"name":"Complete job","status":"completed","conclusion":"success","number":17,"started_at":"2025-08-01T05:41:37Z","completed_at":"2025-08-01T05:41:37Z"}],"check_run_url":"https://api.github.com/repos/depot/zed-test/check-runs/47175110834","labels":["depot-ubuntu-latest-8"],"runner_id":185151,"runner_name":"depot-09szz2sbxr","runner_group_id":1,"runner_group_name":"default"}]}
    },
    {
        "name": "test-cranelift",
        "run_id": "16666953832",
        "data": {"total_count":1,"jobs":[{"id":47175111754,"run_id":16666953832,"workflow_name":"Build Zed","head_branch":"test-cranelift","run_url":"https://api.github.com/repos/depot/zed-test/actions/runs/16666953832","run_attempt":1,"node_id":"CR_kwDOPUJXr88AAAAK-9sUSg","head_sha":"47d5e9cd81008161e936e7277311225297bf52b0","url":"https://api.github.com/repos/depot/zed-test/actions/jobs/47175111754","html_url":"https://github.com/depot/zed-test/actions/runs/16666953832/job/47175111754","status":"completed","conclusion":"success","created_at":"2025-08-01T05:16:24Z","started_at":"2025-08-01T05:16:25Z","completed_at":"2025-08-01T05:41:54Z","name":"build","steps":[{"name":"Set up job","status":"completed","conclusion":"success","number":1,"started_at":"2025-08-01T05:17:17Z","completed_at":"2025-08-01T05:17:18Z"},{"name":"Checkout code","status":"completed","conclusion":"success","number":2,"started_at":"2025-08-01T05:17:18Z","completed_at":"2025-08-01T05:17:35Z"},{"name":"Install system dependencies","status":"completed","conclusion":"success","number":3,"started_at":"2025-08-01T05:17:35Z","completed_at":"2025-08-01T05:18:15Z"},{"name":"Install Rust","status":"completed","conclusion":"success","number":4,"started_at":"2025-08-01T05:18:15Z","completed_at":"2025-08-01T05:18:25Z"},{"name":"Install depot CLI","status":"completed","conclusion":"success","number":5,"started_at":"2025-08-01T05:18:25Z","completed_at":"2025-08-01T05:18:25Z"},{"name":"Setup Rust toolchain","status":"completed","conclusion":"success","number":6,"started_at":"2025-08-01T05:18:25Z","completed_at":"2025-08-01T05:18:42Z"},{"name":"Cache cargo dependencies","status":"completed","conclusion":"success","number":7,"started_at":"2025-08-01T05:18:42Z","completed_at":"2025-08-01T05:18:44Z"},{"name":"Run tests","status":"completed","conclusion":"success","number":8,"started_at":"2025-08-01T05:18:44Z","completed_at":"2025-08-01T05:19:31Z"},{"name":"Build Zed (release)","status":"completed","conclusion":"success","number":9,"started_at":"2025-08-01T05:19:31Z","completed_at":"2025-08-01T05:41:48Z"},{"name":"Post Cache cargo dependencies","status":"completed","conclusion":"success","number":17,"started_at":"2025-08-01T05:41:48Z","completed_at":"2025-08-01T05:41:52Z"},{"name":"Post Checkout code","status":"completed","conclusion":"success","number":18,"started_at":"2025-08-01T05:41:52Z","completed_at":"2025-08-01T05:41:52Z"},{"name":"Complete job","status":"completed","conclusion":"success","number":19,"started_at":"2025-08-01T05:41:52Z","completed_at":"2025-08-01T05:41:52Z"}],"check_run_url":"https://api.github.com/repos/depot/zed-test/check-runs/47175111754","labels":["depot-ubuntu-latest-8"],"runner_id":185129,"runner_name":"depot-64qw9g1l7t","runner_group_id":1,"runner_group_name":"default"}]}
    },
    {
        "name": "test-cranelift-revert",
        "run_id": "16666953899",
        "data": {"total_count":1,"jobs":[{"id":47175112016,"run_id":16666953899,"workflow_name":"Build Zed","head_branch":"test-cranelift-revert","run_url":"https://api.github.com/repos/depot/zed-test/actions/runs/16666953899","run_attempt":1,"node_id":"CR_kwDOPUJXr88AAAAK-9sVUA","head_sha":"bccc39e5f5f363b22df77328591e101f705368a7","url":"https://api.github.com/repos/depot/zed-test/actions/jobs/47175112016","html_url":"https://github.com/depot/zed-test/actions/runs/16666953899/job/47175112016","status":"completed","conclusion":"success","created_at":"2025-08-01T05:16:25Z","started_at":"2025-08-01T05:16:25Z","completed_at":"2025-08-01T05:54:15Z","name":"build","steps":[{"name":"Set up job","status":"completed","conclusion":"success","number":1,"started_at":"2025-08-01T05:17:00Z","completed_at":"2025-08-01T05:17:02Z"},{"name":"Checkout code","status":"completed","conclusion":"success","number":2,"started_at":"2025-08-01T05:17:02Z","completed_at":"2025-08-01T05:17:19Z"},{"name":"Install system dependencies","status":"completed","conclusion":"success","number":3,"started_at":"2025-08-01T05:17:19Z","completed_at":"2025-08-01T05:18:01Z"},{"name":"Install Rust","status":"completed","conclusion":"success","number":4,"started_at":"2025-08-01T05:18:01Z","completed_at":"2025-08-01T05:18:10Z"},{"name":"Install depot CLI","status":"completed","conclusion":"success","number":5,"started_at":"2025-08-01T05:18:10Z","completed_at":"2025-08-01T05:18:10Z"},{"name":"Setup Rust toolchain","status":"completed","conclusion":"success","number":6,"started_at":"2025-08-01T05:18:10Z","completed_at":"2025-08-01T05:18:27Z"},{"name":"Cache cargo dependencies","status":"completed","conclusion":"success","number":7,"started_at":"2025-08-01T05:18:27Z","completed_at":"2025-08-01T05:18:29Z"},{"name":"Run tests","status":"completed","conclusion":"success","number":8,"started_at":"2025-08-01T05:18:29Z","completed_at":"2025-08-01T05:33:46Z"},{"name":"Build Zed (release)","status":"completed","conclusion":"success","number":9,"started_at":"2025-08-01T05:33:46Z","completed_at":"2025-08-01T05:54:05Z"},{"name":"Post Cache cargo dependencies","status":"completed","conclusion":"success","number":17,"started_at":"2025-08-01T05:54:05Z","completed_at":"2025-08-01T05:54:14Z"},{"name":"Post Checkout code","status":"completed","conclusion":"success","number":18,"started_at":"2025-08-01T05:54:14Z","completed_at":"2025-08-01T05:54:14Z"},{"name":"Complete job","status":"completed","conclusion":"success","number":19,"started_at":"2025-08-01T05:54:14Z","completed_at":"2025-08-01T05:54:14Z"}],"check_run_url":"https://api.github.com/repos/depot/zed-test/check-runs/47175112016","labels":["depot-ubuntu-latest-8"],"runner_id":185127,"runner_name":"depot-5wmw4ntrf2","runner_group_id":1,"runner_group_name":"default"}]}
    },
    {
        "name": "test-nextest",
        "run_id": "16666954096",
        "data": {"total_count":1,"jobs":[{"id":47175112502,"run_id":16666954096,"workflow_name":"Build Zed","head_branch":"test-nextest","run_url":"https://api.github.com/repos/depot/zed-test/actions/runs/16666954096","run_attempt":1,"node_id":"CR_kwDOPUJXr88AAAAK-9sXNg","head_sha":"2c58890851fae39aa880eb7c8e24a13fffc04564","url":"https://api.github.com/repos/depot/zed-test/actions/jobs/47175112502","html_url":"https://github.com/depot/zed-test/actions/runs/16666954096/job/47175112502","status":"completed","conclusion":"success","created_at":"2025-08-01T05:16:25Z","started_at":"2025-08-01T05:16:26Z","completed_at":"2025-08-01T05:48:41Z","name":"build","steps":[{"name":"Set up job","status":"completed","conclusion":"success","number":1,"started_at":"2025-08-01T05:16:42Z","completed_at":"2025-08-01T05:16:43Z"},{"name":"Checkout code","status":"completed","conclusion":"success","number":2,"started_at":"2025-08-01T05:16:43Z","completed_at":"2025-08-01T05:17:02Z"},{"name":"Install system dependencies","status":"completed","conclusion":"success","number":3,"started_at":"2025-08-01T05:17:02Z","completed_at":"2025-08-01T05:17:45Z"},{"name":"Install Rust","status":"completed","conclusion":"success","number":4,"started_at":"2025-08-01T05:17:45Z","completed_at":"2025-08-01T05:17:54Z"},{"name":"Install depot CLI","status":"completed","conclusion":"success","number":5,"started_at":"2025-08-01T05:17:54Z","completed_at":"2025-08-01T05:17:54Z"},{"name":"Install cargo-nextest","status":"completed","conclusion":"success","number":6,"started_at":"2025-08-01T05:17:54Z","completed_at":"2025-08-01T05:17:55Z"},{"name":"Setup Rust toolchain","status":"completed","conclusion":"success","number":7,"started_at":"2025-08-01T05:17:55Z","completed_at":"2025-08-01T05:18:11Z"},{"name":"Cache cargo dependencies","status":"completed","conclusion":"success","number":8,"started_at":"2025-08-01T05:18:11Z","completed_at":"2025-08-01T05:18:14Z"},{"name":"Run tests","status":"completed","conclusion":"success","number":9,"started_at":"2025-08-01T05:18:14Z","completed_at":"2025-08-01T05:30:22Z"},{"name":"Build Zed (release)","status":"completed","conclusion":"success","number":10,"started_at":"2025-08-01T05:30:22Z","completed_at":"2025-08-01T05:48:30Z"},{"name":"Post Cache cargo dependencies","status":"completed","conclusion":"success","number":19,"started_at":"2025-08-01T05:48:30Z","completed_at":"2025-08-01T05:48:40Z"},{"name":"Post Checkout code","status":"completed","conclusion":"success","number":20,"started_at":"2025-08-01T05:48:40Z","completed_at":"2025-08-01T05:48:40Z"},{"name":"Complete job","status":"completed","conclusion":"success","number":21,"started_at":"2025-08-01T05:48:40Z","completed_at":"2025-08-01T05:48:40Z"}],"check_run_url":"https://api.github.com/repos/depot/zed-test/check-runs/47175112502","labels":["depot-ubuntu-latest-8"],"runner_id":185135,"runner_name":"depot-718hp2m3dv","runner_group_id":1,"runner_group_name":"default"}]}
    },
    {
        "name": "test-depot",
        "run_id": "16666953655",
        "data": {"total_count":1,"jobs":[{"id":47175111280,"run_id":16666953655,"workflow_name":"Build Zed","head_branch":"test-depot","run_url":"https://api.github.com/repos/depot/zed-test/actions/runs/16666953655","run_attempt":1,"node_id":"CR_kwDOPUJXr88AAAAK-9sScA","head_sha":"73fd58487bd612a3a6d30966d055b581953efa9a","url":"https://api.github.com/repos/depot/zed-test/actions/jobs/47175111280","html_url":"https://github.com/depot/zed-test/actions/runs/16666953655/job/47175111280","status":"completed","conclusion":"success","created_at":"2025-08-01T05:16:23Z","started_at":"2025-08-01T05:16:24Z","completed_at":"2025-08-01T06:02:09Z","name":"build","steps":[{"name":"Set up job","status":"completed","conclusion":"success","number":1,"started_at":"2025-08-01T05:16:40Z","completed_at":"2025-08-01T05:16:42Z"},{"name":"Checkout code","status":"completed","conclusion":"success","number":2,"started_at":"2025-08-01T05:16:42Z","completed_at":"2025-08-01T05:17:00Z"},{"name":"Install system dependencies","status":"completed","conclusion":"success","number":3,"started_at":"2025-08-01T05:17:00Z","completed_at":"2025-08-01T05:17:42Z"},{"name":"Install Rust","status":"completed","conclusion":"success","number":4,"started_at":"2025-08-01T05:17:42Z","completed_at":"2025-08-01T05:17:51Z"},{"name":"Install depot CLI","status":"completed","conclusion":"success","number":5,"started_at":"2025-08-01T05:17:51Z","completed_at":"2025-08-01T05:17:51Z"},{"name":"Setup Rust toolchain","status":"completed","conclusion":"success","number":6,"started_at":"2025-08-01T05:17:51Z","completed_at":"2025-08-01T05:18:08Z"},{"name":"Cache cargo dependencies","status":"completed","conclusion":"success","number":7,"started_at":"2025-08-01T05:18:08Z","completed_at":"2025-08-01T05:18:10Z"},{"name":"Run tests","status":"completed","conclusion":"success","number":8,"started_at":"2025-08-01T05:18:10Z","completed_at":"2025-08-01T05:33:41Z"},{"name":"Build Zed (release)","status":"completed","conclusion":"success","number":9,"started_at":"2025-08-01T05:33:41Z","completed_at":"2025-08-01T06:01:59Z"},{"name":"Post Cache cargo dependencies","status":"completed","conclusion":"success","number":17,"started_at":"2025-08-01T06:01:59Z","completed_at":"2025-08-01T06:02:07Z"},{"name":"Post Checkout code","status":"completed","conclusion":"success","number":18,"started_at":"2025-08-01T06:02:07Z","completed_at":"2025-08-01T06:02:08Z"},{"name":"Complete job","status":"completed","conclusion":"success","number":19,"started_at":"2025-08-01T06:02:08Z","completed_at":"2025-08-01T06:02:08Z"}],"check_run_url":"https://api.github.com/repos/depot/zed-test/check-runs/47175111280","labels":["depot-ubuntu-latest-8"],"runner_id":185136,"runner_name":"depot-tth6bbb763","runner_group_id":1,"runner_group_name":"default"}]}
    }
]

# Process each workflow
results = []
baseline_test_time = None
baseline_build_time = None
baseline_total_time = None

for workflow in workflows:
    job = workflow["data"]["jobs"][0]
    steps = job["steps"]
    
    # Extract durations
    test_time = extract_step_duration(steps, "Run tests")
    build_time = extract_step_duration(steps, "Build Zed (release)")
    total_time = calculate_duration(job["started_at"], job["completed_at"])
    
    # Set baseline values
    if workflow["name"] == "test-baseline":
        baseline_test_time = test_time
        baseline_build_time = build_time
        baseline_total_time = total_time
    
    results.append({
        "name": workflow["name"],
        "run_id": workflow["run_id"],
        "test_time": test_time,
        "build_time": build_time,
        "total_time": total_time,
        "url": f"https://github.com/depot/zed-test/actions/runs/{workflow['run_id']}"
    })

# Print results
print("# GitHub Actions Workflow Performance Analysis")
print("## Zed Build Performance Testing Results")
print()

for result in results:
    test_change = calculate_percentage_change(baseline_test_time, result["test_time"])
    build_change = calculate_percentage_change(baseline_build_time, result["build_time"])
    total_change = calculate_percentage_change(baseline_total_time, result["total_time"])
    
    print(f"### {result['name']}")
    print(f"- **Test duration**: {format_duration(result['test_time'])} ({test_change} from baseline)")
    print(f"- **Build duration**: {format_duration(result['build_time'])} ({build_change} from baseline)")
    print(f"- **Total duration**: {format_duration(result['total_time'])} ({total_change} from baseline)")
    print(f"- **Workflow URL**: {result['url']}")
    print()

print("## Summary Table")
print()
print("| Branch | Test Duration | Test Change | Build Duration | Build Change | Total Duration | Total Change |")
print("|--------|---------------|-------------|----------------|--------------|----------------|--------------|")

for result in results:
    test_change = calculate_percentage_change(baseline_test_time, result["test_time"])
    build_change = calculate_percentage_change(baseline_build_time, result["build_time"])
    total_change = calculate_percentage_change(baseline_total_time, result["total_time"])
    
    print(f"| {result['name']} | {format_duration(result['test_time'])} | {test_change} | {format_duration(result['build_time'])} | {build_change} | {format_duration(result['total_time'])} | {total_change} |")