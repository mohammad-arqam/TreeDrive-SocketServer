import argparse
import subprocess
import time
from multiprocessing import Process, Queue, Event


TEST_FILENAME = "test_file.txt"
TOTAL_DOWNLOADS = 100
CLIENT_COUNTS = list(range(1, 51))  # Fixed set: 1 to 50 clients

# Create a dummy file to test
with open(TEST_FILENAME, "w") as f:
    f.write("Hello TreeDrive!" * 100)

def upload_file_once(hostname):
    subprocess.run(
        ["python3", "client.py", "admin", hostname],
        input=f"PUSH {TEST_FILENAME}\nQUIT\n",
        text=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        timeout=60
    )

def client_get_task(username, hostname, queue):
    try:
        proc = subprocess.Popen(
            ["python3", "client.py", username, hostname],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text=True
        )
        cmd = "".join([f"GET {TEST_FILENAME}\n" for _ in range(TOTAL_DOWNLOADS)])
        proc.stdin.write(cmd)
        proc.stdin.flush()
        start = time.time()
        proc.stdin.write("QUIT\n")
        proc.stdin.flush()
        proc.communicate(timeout=300)
        end = time.time()
        latency = end - start
        throughput = TOTAL_DOWNLOADS / latency if latency > 0 else 0
        queue.put((latency, throughput))
    except Exception:
        queue.put((None, None))

def client_idle_task(username, hostname, stop_event):
    try:
        proc = subprocess.Popen(
            ["python3", "client.py", username, hostname],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text=True
        )
        stop_event.wait()
        proc.communicate(input="QUIT\n", timeout=60)  # fixed newline issue
    except Exception:
        pass

def run_test_incrementally(hostname):
    queue = Queue()
    all_results = []

    for i in range(1, len(CLIENT_COUNTS) + 1):
        processes = []
        stop_event = Event()

        # Start idle clients
        for j in range(i - 1):
            p = Process(target=client_idle_task, args=(f"user{j}", hostname, stop_event))
            p.start()
            processes.append(p)

        # Start the active downloading client
        active = Process(target=client_get_task, args=(f"user{i-1}", hostname, queue))
        active.start()
        processes.append(active)

        # Wait for download to complete
        latency, throughput = queue.get()
        all_results.append((latency, throughput))
        print(f"Clients connected: {i}, Download latency: {latency:.2f} seconds, Throughput: {throughput:.2f} downloads/sec")

        # Signal all idle clients to disconnect
        stop_event.set()

        # Wait for all to exit
        for p in processes:
            p.join()

    return all_results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("hostname", help="Server hostname")
    args = parser.parse_args()
    hostname = args.hostname

    upload_file_once(hostname)

    print(f"Running download tests where each new client downloads with increasing connected users...")
    run_test_incrementally(hostname)

if __name__ == "__main__":
    main()