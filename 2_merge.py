
# 2つのMessagePack形式ファイルを結合する。
# [[...], ...] + [[...], ...] -> [[...], ...]

import sys
import msgpackutil

if len(sys.argv) <= 3:
    print("Usage: " + sys.argv[0] + " infile1 infile2 outfile", file=sys.stderr)
    exit(1)

infile1 = sys.argv[1]
infile2 = sys.argv[2]
outfile = sys.argv[3]
print("infile1 = " + infile1)
print("infile2 = " + infile2)
print("outfile = " + outfile)

print("loading...")
in_records1 = msgpackutil.load(infile1)
in_records2 = msgpackutil.load(infile2)

print("processing...")
out_records = []
out_records.extend(in_records1)
out_records.extend(in_records2)
print("in_records1.len = " + str(len(in_records1)))
print("in_records2.len = " + str(len(in_records2)))
print("out_records.len = " + str(len(out_records)))

print("dumping...")
msgpackutil.dump(outfile, out_records)

print("ok")
