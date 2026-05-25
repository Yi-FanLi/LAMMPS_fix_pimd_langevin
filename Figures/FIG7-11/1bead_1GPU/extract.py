import glob
import re
import numpy as np

pattern = re.compile(
    r"Performance:\s+([0-9.]+)\s+ns/day,\s+([0-9.]+)\s+hours/ns,\s+([0-9.]+)\s+timesteps/s,\s+([0-9.]+)\s+katom-step/s"
)

results = {}

folders = sorted(glob.glob("*h2o"))
print(folders)

for folder in folders:
    log_path = f"{folder}/log.0"
    try:
        with open(log_path, "r") as f:
            for line in f:
                if line.startswith("Performance:"):
                    match = pattern.search(line)
                    if match:
                        ns_per_day, hrs_per_ns, steps_per_s, katom_steps_per_s = map(float, match.groups())
                        results[folder] = {
                            "ns/day": ns_per_day,
                            "hours/ns": hrs_per_ns,
                            "timesteps/s": steps_per_s,
                            "katom-step/s": katom_steps_per_s,
                        }
                    break
    except FileNotFoundError:
        print(f"Warning: {log_path} not found.")

gpus = []
outputs = []
# Print results
for folder, metrics in sorted(results.items()):
    match = re.match(r"(\d+)", folder)
    if match:
        number = int(match.group(1))	
    gpus.append([number])
    print(f"{number} h2o: {metrics}")
    outputs.append(list(metrics.values()))

gpus = np.array(gpus)
outputs = np.array(outputs)
time_per_step = 1/outputs[:, 2]
#print(np.c_[gpus, outputs, time_per_step])
header = "h2o ns/day hours/ns timesteps/s katom-step/s s/timestep"
outputs_total = np.c_[gpus, outputs, time_per_step]
outputs_total = outputs_total[np.argsort(outputs_total[:, 0])]
print(outputs_total)
np.savetxt("output.dat", outputs_total, header=header, fmt="%.4f")
#np.savetxt("output.dat", np.c_[gpus, outputs, time_per_step], header=header, fmt="%.4f")
