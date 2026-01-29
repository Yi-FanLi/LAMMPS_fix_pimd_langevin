import numpy as np

header = []
natom = None
ntype = None
anum = []
atype = []
entries = []

with open('conf.128', "r") as f:
    while True:
        line = f.readline()
        if "Atoms" in line:
            break
    for i in range(16):
        line = f.readline()
        header.append(line)
        line = line.split()
        if len(line) > 0 and line[-1] == "atoms":
            natom = int(line[0])
    for i in range(natom):
        line = f.readline().split()
        anum.append(int(line[0]))
        atype.append(int(line[1]))
        entries.append([float(x) for x in line[2:]])

idx = np.argsort(anum)
anum = [anum[i] for i in idx]
atype = [atype[i] for i in idx]
entries = [entries[i] for i in idx]
bonds = []
molIDs = [i for i in range(1, natom//3+1)] + [x for i in range(1, natom//3 + 1) for x in (i, i)] + [i for i in range(1, natom//3+1)]
charges = [6] * (natom//3) + [1] * (2*natom//3) + [-8] * (natom//3)

ii = natom+1
for i in range(natom):
    if atype[i] == 1:
        anum.append(ii)
        atype.append(3)
        bonds.append((anum[i], ii))
        ii += 1
        entries.append(entries[i])

with open('conf.lr', 'w') as f:
    for line in header:
        f.write(line)
        if line.split() and line.split()[-2:] == ["atom", "types"]:
            f.write(f'{len(bonds)} bonds\n')
            f.write(f"1 bond types\n")
    for i in range(len(anum)):
        entry = " ".join([str(x) for x in entries[i][:-3]])
        entry += " " + " ".join([f"{int(x):d}" for x in entries[i][-3:]])
        f.write(f"{anum[i]} {molIDs[i]} {atype[i]} {charges[i]} {entry}\n")
    f.write("\nBonds\n\n")
    for i, (a1, a2) in enumerate(bonds):
        f.write(f"{i+1} 1 {a1} {a2}\n")