import glob
import re
import numpy as np

pattern = re.compile(
    r"Performance:\s+([0-9.]+)\s+ns/day,\s+([0-9.]+)\s+hours/ns,\s+([0-9.]+)\s+timesteps/s,\s+([0-9.]+)\s+([kM])atom-step/s"
)

scale_to_katom = {"k": 1.0, "M": 1e3}

results = {}

folders = sorted(glob.glob("*gpu"))
print("Folders:", folders)

for folder in folders:
    log_path = f"{folder}/log.0"
    print("Reading:", log_path)

    try:
        with open(log_path, "r") as f:
            for line in f:
                if not line.startswith("Performance:"):
                    continue

                print(line.rstrip())

                m = pattern.search(line)
                if not m:
                    print(f"Warning: Performance line did not match regex in {log_path}")
                    break

                ns_per_day, hrs_per_ns, steps_per_s, rate, prefix = m.groups()

                ns_per_day = float(ns_per_day)
                hrs_per_ns = float(hrs_per_ns)
                steps_per_s = float(steps_per_s)

                # Convert to katom-step/s
                katom_steps_per_s = float(rate) * scale_to_katom[prefix]

                results[folder] = {
                    "ns/day": ns_per_day,
                    "hours/ns": hrs_per_ns,
                    "timesteps/s": steps_per_s,
                    "katom-step/s": katom_steps_per_s,
                }
                break
    except FileNotFoundError:
        print(f"Warning: {log_path} not found.")

# Assemble output
rows = []
for folder in sorted(results.keys()):
    m = re.match(r"(\d+)", folder)
    if not m:
        print(f"Warning: cannot parse GPU count from folder name: {folder}")
        continue

    gpu = int(m.group(1))
    metrics = results[folder]

    s_per_timestep = 1.0 / metrics["timesteps/s"]

    rows.append([
        gpu,
        metrics["ns/day"],
        metrics["hours/ns"],
        metrics["timesteps/s"],
        metrics["katom-step/s"],
        s_per_timestep,
    ])

rows = np.array(sorted(rows, key=lambda x: x[0]), dtype=float)

header = "gpu ns/day hours/ns timesteps/s katom-step/s s/timestep"
print(rows)

np.savetxt("output.dat", rows, header=header, fmt="%.6f")
