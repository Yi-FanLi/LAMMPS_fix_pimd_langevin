#!/usr/bin/env python3
import argparse, glob, math, re
from typing import List, Tuple

FLOAT = float

# Match CELL line in the comment; capture the first 6 numbers if present
CELL_NUM_RE = re.compile(r'CELL[^\d\-+eE]*([\-+0-9.eE\s]+)')

def parse_cell_L(comment: str, tol_rel: float = 1e-6) -> float:
    """
    Extract L from comment containing CELL. Accepts:
      CELL = a b c
      CELL a b c alpha beta gamma
    Assumes cubic box at origin -> returns L.
    """
    m = CELL_NUM_RE.search(comment)
    if not m:
        raise RuntimeError("CELL not found in comment line. Expected e.g. 'CELL = a b c [alpha beta gamma]'.")
    nums = [FLOAT(x) for x in m.group(1).split()]
    if len(nums) < 3:
        raise RuntimeError("CELL found but fewer than 3 numbers.")
    a, b, c = nums[0], nums[1], nums[2]
    # Enforce/relax cubic: allow tiny drift
    mean = (a + b + c) / 3.0
    if mean == 0.0:
        raise RuntimeError("CELL has zero box length.")
    def close(u,v): 
        return abs(u - v) <= tol_rel * max(1.0, abs(u), abs(v))
    if not (close(a,b) and close(b,c)):
        # Still proceed but use the average and warn in stdout
        print(f"[warn] Non-cubic CELL detected in comment (a,b,c)=({a},{b},{c}). Using L=mean={mean}.")
        return mean
    return a  # cubic

def xyz_frames(path: str):
    """Yield (natoms, comment, atoms) with atoms as list of (sym, x, y, z)."""
    with open(path, "r") as f:
        while True:
            line = f.readline()
            if not line:
                break
            line = line.strip()
            if not line:
                continue
            try:
                n = int(line)
            except ValueError:
                raise RuntimeError(f"Expected atom count in {path}, got: {line!r}")
            comment = f.readline()
            if not comment:
                raise RuntimeError(f"Incomplete frame in {path} (missing comment)")
            comment = comment.rstrip("\n")
            atoms = []
            for _ in range(n):
                row = f.readline()
                if not row:
                    raise RuntimeError(f"Incomplete atom list in {path}")
                t = row.split()
                if len(t) >= 4 and not _is_float(t[0]):
                    sym = t[0]; x, y, z = map(FLOAT, t[1:4])
                else:
                    sym = "X"; x, y, z = map(FLOAT, t[:3])
                atoms.append((sym, x, y, z))
            yield n, comment, atoms

def _is_float(s: str) -> bool:
    try:
        float(s); return True
    except Exception:
        return False

def build_type_map(atoms) -> dict:
    order, seen = [], set()
    for sym, *_ in atoms:
        if sym not in seen:
            seen.add(sym); order.append(sym)
    return {sym: i+1 for i, sym in enumerate(order)}

def convert(pattern: str, outpath: str, t0: int, dt: int, types_mode: str, sort_files: bool):
    files = glob.glob(pattern)
    if not files:
        raise SystemExit(f"No files match pattern {pattern!r}")
    if sort_files:
        files.sort()

    timestep = t0
    natoms_ref = None
    type_map = None

    with open(outpath, "w") as out:
        for path in files:
            for n, comment, atoms in xyz_frames(path):
                if natoms_ref is None:
                    natoms_ref = n
                    if types_mode == "from-symbol":
                        type_map = build_type_map(atoms)
                elif n != natoms_ref:
                    raise RuntimeError(f"Frame in {path} has {n} atoms, expected {natoms_ref}.")

                # Read L from CELL in the comment (cubic, origin at 0)
                L = parse_cell_L(comment)

                out.write("ITEM: TIMESTEP\n")
                out.write(f"{timestep}\n")
                out.write("ITEM: NUMBER OF ATOMS\n")
                out.write(f"{n}\n")
                out.write("ITEM: BOX BOUNDS pp pp pp\n")
                out.write(f"0 {L:.15g}\n0 {L:.15g}\n0 {L:.15g}\n")
                out.write("ITEM: ATOMS id type x y z\n")

                for i, (sym, x, y, z) in enumerate(atoms, start=1):
                    atype = 1 if types_mode == "single" else type_map.get(sym, 1)
                    out.write(f"{i} {atype} {x:.6g} {y:.6g} {z:.6g}\n")

                timestep += dt
    print(f"Wrote {outpath} with frames from {len(files)} file(s).")

def main():
    ap = argparse.ArgumentParser(description="XYZ → LAMMPS dump using CELL (cubic, origin at 0).")
    ap.add_argument("pattern", help="Glob for input XYZ files, e.g. 'simulation.pos_*.xyz'")
    ap.add_argument("-o", "--output", default="dump.lammpstrj", help="Output LAMMPS dump path")
    ap.add_argument("--t0", type=int, default=0, help="Starting timestep (default 0)")
    ap.add_argument("--dt", type=int, default=1, help="Timestep increment per frame (default 1)")
    ap.add_argument("--types", choices=["single","from-symbol"], default="from-symbol",
                    help="Atom type assignment (default from-symbol)")
    ap.add_argument("--sort", action="store_true", help="Sort files lexicographically")
    args = ap.parse_args()
    convert(args.pattern, args.output, args.t0, args.dt, args.types, args.sort)

if __name__ == "__main__":
    main()
