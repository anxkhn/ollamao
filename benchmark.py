import requests
import os
import time
from packaging import version
import re


def measure_latency(ip_address, port=11434):
    try:
        start_time = time.time()
        response = requests.get(f"http://{ip_address}:{port}", timeout=5)
        end_time = time.time()
        response.raise_for_status()
        latency_ms = (end_time - start_time) * 1000
        return latency_ms
    except requests.RequestException:
        return None


def get_ollama_info(ip_address, port=11434):
    base_url = f"http://{ip_address}:{port}"
    version_url = f"{base_url}/api/version"
    try:
        response = requests.get(base_url, timeout=5)
        response.raise_for_status()
        if "Ollama is running" in response.text:
            info = {"running": True}
            try:
                version_response = requests.get(version_url, timeout=5)
                version_response.raise_for_status()
                info["version"] = version_response.json()["version"]
            except (requests.RequestException, KeyError):
                info["version"] = None
                print(f"Could not get Ollama server version for {ip_address}.")
            return info
        else:
            return {"running": False, "version": None}
    except requests.RequestException as e:
        print(f"Could not connect to Ollama server at {ip_address}:{port}. Error: {e}")
        return None


def main():
    ip_list_file = "ip_list.txt"
    benchmark_file = "benchmark.md"
    port = 11434
    unique_ips = set()
    try:
        with open(ip_list_file, "r") as f:
            for line in f:
                ips = re.findall(
                    r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b",
                    line,
                )
                unique_ips.update(ips)
    except FileNotFoundError:
        print(f"Error: File '{ip_list_file}' not found.")
        return
    server_data = []
    for ip_address in unique_ips:
        ollama_info = get_ollama_info(ip_address, port)
        if ollama_info and ollama_info["running"]:
            latency = measure_latency(ip_address, port)
            if latency is not None:
                server_data.append(
                    {
                        "ip": ip_address,
                        "version": ollama_info["version"],
                        "latency": latency,
                    }
                )
            else:
                print(f"Could not measure latency for {ip_address}")

    def version_sort_key(item):
        if item["version"] is None:
            return (0,)
        try:
            return tuple(map(int, item["version"].split(".")))
        except ValueError:
            return (0,)

    sorted_data = sorted(server_data, key=lambda x: (version_sort_key(x), x["latency"]))
    with open(benchmark_file, "w") as f:
        f.write("# Ollama Server Benchmark\n\n")
        f.write("| IP Address | Version | Latency (ms) |\n")
        f.write("|------------|---------|--------------|\n")
        for server in sorted_data:
            version_str = server["version"] if server["version"] else "N/A"
            f.write(
                f"| {server['ip']} | {version_str} | {server['latency']:.2f} |\n"
            )  # Format latency
    print(f"Benchmark results written to '{benchmark_file}'")


if __name__ == "__main__":
    main()
