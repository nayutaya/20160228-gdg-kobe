
# タイトルをトークン化する。
# [[category, title], ...] -> [[category, title, tokens], ...]

import sys
import msgpackutil

sys.path.append(".")
import context as ctx

if len(sys.argv) <= 2:
    print("Usage: " + sys.argv[0] + " infile outfile", file=sys.stderr)
    exit(1)

infile  = sys.argv[1]
outfile = sys.argv[2]
print("infile   = " + infile)
print("outfile  = " + outfile)

print("loading...")
in_records = msgpackutil.load(infile)

print("tokenize...")
out_records = []
for index, (category, title) in enumerate(in_records):
    if index % 100 == 0:
        print(str(index) + "/" + str(len(in_records)))
    tokens = ctx.tokenizer.tokenize(title)
    out_records.append([category, title, tokens])

print("dumping...")
msgpackutil.dump(outfile, out_records)

print("ok")
