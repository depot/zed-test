#!/usr/bin/env python3
import json
from datetime import datetime

def parse_time(time_str):
    return datetime.fromisoformat(time_str.replace('Z', '+00:00'))

def calculate_duration(start, end):
    start_time = parse_time(start)
    end_time = parse_time(end)
    duration = end_time - start_time
    return duration.total_seconds() / 60  # Return in minutes

def analyze_run(data, run_name):
    parsed = json.loads(data)
    job = parsed['jobs'][0]
    
    # Total workflow duration
    total_duration = calculate_duration(job['started_at'], job['completed_at'])
    
    # Find specific steps
    test_step = None
    build_step = None
    
    for step in job['steps']:
        if step['name'] == 'Run tests':
            test_step = step
        elif step['name'] == 'Build Zed (release)':
            build_step = step
    
    test_duration = calculate_duration(test_step['started_at'], test_step['completed_at']) if test_step else 0
    build_duration = calculate_duration(build_step['started_at'], build_step['completed_at']) if build_step else 0
    
    print(f'{run_name}:')
    print(f'  Test time: {test_duration:.1f}m ({int(test_duration)}m {int((test_duration % 1) * 60)}s)')
    print(f'  Build time: {build_duration:.1f}m ({int(build_duration)}m {int((build_duration % 1) * 60)}s)')
    print(f'  Total time: {total_duration:.1f}m ({int(total_duration)}m {int((total_duration % 1) * 60)}s)')
    print()
    
    return test_duration, build_duration, total_duration

# Read the JSON data from GitHub API calls
import sys
import subprocess

print('=== Performance Regression Analysis ===')
print()

# Get data for each run
baseline_result = subprocess.run(['gh', 'api', 'repos/depot/zed-test/actions/runs/16666952853/jobs'], 
                                capture_output=True, text=True)
run1_result = subprocess.run(['gh', 'api', 'repos/depot/zed-test/actions/runs/16666948139/jobs'], 
                            capture_output=True, text=True)
run2_result = subprocess.run(['gh', 'api', 'repos/depot/zed-test/actions/runs/16666953655/jobs'], 
                            capture_output=True, text=True)

baseline_test, baseline_build, baseline_total = analyze_run(baseline_result.stdout, 'Baseline (16666952853)')
run1_test, run1_build, run1_total = analyze_run(run1_result.stdout, 'Run 1 (16666948139)')
run2_test, run2_build, run2_total = analyze_run(run2_result.stdout, 'Run 2 (16666953655)')

print('=== Regression Analysis ===')
print(f'Run 1 vs Baseline:')
print(f'  Test regression: +{run1_test - baseline_test:.1f}m ({((run1_test / baseline_test - 1) * 100):.1f}% increase)')
print(f'  Build regression: +{run1_build - baseline_build:.1f}m ({((run1_build / baseline_build - 1) * 100):.1f}% increase)')
print(f'  Total regression: +{run1_total - baseline_total:.1f}m ({((run1_total / baseline_total - 1) * 100):.1f}% increase)')
print()

print(f'Run 2 vs Baseline:')
print(f'  Test regression: +{run2_test - baseline_test:.1f}m ({((run2_test / baseline_test - 1) * 100):.1f}% increase)')
print(f'  Build regression: +{run2_build - baseline_build:.1f}m ({((run2_build / baseline_build - 1) * 100):.1f}% increase)')
print(f'  Total regression: +{run2_total - baseline_total:.1f}m ({((run2_total / baseline_total - 1) * 100):.1f}% increase)')
print()

print('=== Consistency Check ===')
print(f'Test time difference between runs: {abs(run1_test - run2_test):.1f}m')
print(f'Build time difference between runs: {abs(run1_build - run2_build):.1f}m')
print(f'Total time difference between runs: {abs(run1_total - run2_total):.1f}m')
print()

avg_test = (run1_test + run2_test) / 2
avg_build = (run1_build + run2_build) / 2
avg_total = (run1_total + run2_total) / 2

print('=== Average Regression (depot vs baseline) ===')
print(f'Average test regression: +{avg_test - baseline_test:.1f}m ({((avg_test / baseline_test - 1) * 100):.1f}% increase)')
print(f'Average build regression: +{avg_build - baseline_build:.1f}m ({((avg_build / baseline_build - 1) * 100):.1f}% increase)')
print(f'Average total regression: +{avg_total - baseline_total:.1f}m ({((avg_total / baseline_total - 1) * 100):.1f}% increase)')