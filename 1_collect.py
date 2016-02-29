
# テキストファイルからタイトルを読み込み、カテゴリを付加し、MessagePack形式で書き出す。
# "title\n..." -> [[category, title], ...]

import sys
import msgpackutil

if len(sys.argv) <= 3:
    print("Usage: " + sys.argv[0] + " category infile outfile", file=sys.stderr)
    exit(1)

category = sys.argv[1]
infile   = sys.argv[2]
outfile  = sys.argv[3]
print("category = " + category)
print("infile   = " + infile)
print("outfile  = " + outfile)

print("loading...")
with open(infile, "r") as file:
    in_records = [line.rstrip() for line in file]

print("processing...")
out_records = [[category, title] for title in in_records]
out_records.sort()

print("dumping...")
msgpackutil.dump(outfile, out_records)

print("ok")
