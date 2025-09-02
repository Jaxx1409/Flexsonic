# raw_to_csv.py
# Usage: python raw_to_csv.py data_raw/flex_log.txt data_processed/gesture_parsed.csv

import re, argparse, csv

parser = argparse.ArgumentParser()
parser.add_argument("infile")
parser.add_argument("outfile")
args = parser.parse_args()

pattern = re.compile(
    r"Thumb:\s*(-?\d+)\s*\|\s*Index:\s*(-?\d+)\s*\|\s*Middle:\s*(-?\d+)\s*\|\s*Ring:\s*(-?\d+)\s*\|\s*Pinky:\s*(-?\d+)",
    re.IGNORECASE
)

rows = []
with open(args.infile, "r", errors="ignore") as f:
    for line in f:
        m = pattern.search(line)
        if m:
            t, idx, mid, ring, pink = m.groups()
            rows.append([int(t), int(idx), int(mid), int(ring), int(pink)])

if not rows:
    print("No matches found. Check infile path and log format.")
else:
    with open(args.outfile, "w", newline="") as out:
        w = csv.writer(out)
        w.writerow(["Thumb","Index","Middle","Ring","Pinky"])
        w.writerows(rows)
    print(f"Wrote {len(rows)} rows to {args.outfile}")
