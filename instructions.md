
# 🧠 Distributed Collatz Conjecture with `sshp` + Ray

This guide walks you through using [**Ray**](https://docs.ray.io) for distributed computation of the **Collatz Conjecture**, launched across multiple machines using [**sshp**](https://github.com/bahamas10/sshp).

---

## 📦 Requirements

- Python 3.7+
- Ray installed on all machines: `pip install ray`
- `sshp` installed on controller machine: `npm install -g sshp`
- SSH access between controller and workers (passwordless recommended)
- All machines must be on the same network or reachable

---

## 🖥️ 1. Define Your Hosts

Create a file named `hosts.txt` with your SSH hosts (one per line):

```txt
user@worker1.local
user@worker2.local
user@worker3.local
```

> 💡 Test SSH: `ssh user@worker1.local`

---

## ⚙️ 2. Install Ray on All Machines

```bash
pip install ray
```

You can push this with `sshp`:

```bash
sshp -h hosts.txt -c "pip install ray"
```

---

## 🚀 3. Start the Ray Cluster

### ▶️ On Controller (Ray Head Node)

```bash
ray start --head --port=6379
```

Note the printed IP address (e.g. `192.168.1.100`).

---

### ▶️ Use `sshp` to Start Ray Workers

```bash
sshp -h hosts.txt -c "ray start --address='192.168.1.100:6379'"
```

> Replace `192.168.1.100` with your controller’s IP.

---

## 🧪 4. Save the Collatz Driver Script

Save this as `collatz_ray.py` on the **controller** machine:

```python
import ray

@ray.remote
def collatz_range(start, end):
    max_steps = 0
    n_with_max = 0
    for n in range(start, end):
        steps = 0
        x = n
        while x != 1:
            x = x // 2 if x % 2 == 0 else 3 * x + 1
            steps += 1
        if steps > max_steps:
            max_steps = steps
            n_with_max = n
    return (n_with_max, max_steps)

def main():
    ray.init(address="auto")
    chunks = [(i, i + 10000) for i in range(1, 1000000, 10000)]
    futures = [collatz_range.remote(start, end) for start, end in chunks]
    results = ray.get(futures)

    overall_max = max(results, key=lambda x: x[1])
    print(f"Max steps: {overall_max[1]} at n = {overall_max[0]}")

if __name__ == "__main__":
    main()
```

---

## ▶️ 5. Run the Driver

```bash
python3 collatz_ray.py
```

You’ll see output like:

```
Max steps: 178 at n = 837799
```

---

## 🧹 6. Stop Ray Cluster

### On All Nodes (including controller):

```bash
ray stop
```

Or from the controller via `sshp`:

```bash
sshp -h hosts.txt -c "ray stop"
ray stop  # on the controller itself
```

---

## 📁 Optional Enhancements

- Add logging to file per node
- Export results to CSV
- Use larger ranges or support for saving partial results

---

## 🛠️ Troubleshooting

- **"Connection refused"**: Check firewall or port 6379
- **"Worker failed to connect"**: Make sure IP is reachable and not behind NAT
- **SSH issues**: Use `sshp -i yourkey.pem` if needed

---

Let me know if you'd like:
- A shell script to automate all steps
- Docker-based Ray + Collatz runner
- Web UI to monitor task progress
