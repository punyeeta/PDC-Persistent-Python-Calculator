#!/usr/bin/env python3
"""
Compute system metrics from log files.
Usage: python compute_metrics.py [run_duration_seconds]
"""

import re
import sys
from statistics import mean, median, stdev

def parse_latencies(worker_log_file='worker_log.txt'):
    """Extract latency values from worker log."""
    latencies = []
    try:
        with open(worker_log_file) as f:
            for line in f:
                # Match patterns like "Latency: 0.245s" or "Latency: X.XXXs"
                match = re.search(r'Latency:\s*([\d.]+)s', line)
                if match:
                    latencies.append(float(match.group(1)))
    except FileNotFoundError:
        print(f"Warning: {worker_log_file} not found")
    return latencies

def count_votes(log_file, keywords):
    """Count lines matching any keyword in log file."""
    count = 0
    try:
        with open(log_file) as f:
            for line in f:
                if any(kw.lower() in line.lower() for kw in keywords):
                    count += 1
    except FileNotFoundError:
        print(f"Warning: {log_file} not found")
    return count

def main():
    run_duration = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    
    # Count votes
    generated_count = count_votes('edge_log.txt', ['vote sent', 'generated', 'sending vote'])
    processed_count = count_votes('worker_log.txt', ['processed', 'upserted', 'vote processed'])
    
    # Extract latencies
    latencies = parse_latencies('worker_log.txt')
    
    # Compute metrics
    throughput = processed_count / run_duration if run_duration > 0 else 0
    success_rate = (processed_count / generated_count * 100) if generated_count > 0 else 0
    
    if latencies:
        latency_min = min(latencies)
        latency_median = median(latencies)
        latency_mean = mean(latencies)
        latency_p90 = sorted(latencies)[int(len(latencies) * 0.9)] if len(latencies) > 1 else latencies[0]
        latency_stdev = stdev(latencies) if len(latencies) > 1 else 0
    else:
        latency_min = latency_median = latency_mean = latency_p90 = latency_stdev = 0
    
    # Print results
    print("\n" + "="*60)
    print("SYSTEM METRICS REPORT")
    print("="*60)
    print(f"Run Duration:       {run_duration}s")
    print(f"Votes Generated:    {generated_count}")
    print(f"Votes Processed:    {processed_count}")
    print(f"\nThroughput:         {throughput:.2f} votes/sec")
    print(f"Success Rate:       {success_rate:.1f}%")
    print(f"\nLatency Stats:")
    print(f"  Min:              {latency_min:.3f}s")
    print(f"  Median:           {latency_median:.3f}s")
    print(f"  Mean:             {latency_mean:.3f}s")
    print(f"  P90:              {latency_p90:.3f}s")
    print(f"  StdDev:           {latency_stdev:.3f}s")
    print(f"  Sample Count:     {len(latencies)}")
    print("="*60 + "\n")

if __name__ == '__main__':
    main()
