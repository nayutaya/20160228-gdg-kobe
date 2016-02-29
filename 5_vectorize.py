
# タイトルをベクトル化する。
# [[term, index], ...] + [[category, title, tokens], ...] -> [[category, title, tokens, vector], ...]

import sys
import msgpackutil
import vectorizer as ve

if len(sys.argv) <= 3:
    print("Usage: " + sys.argv[0] + " dictfile infile outfile", file=sys.stderr)
    exit(1)

dictfile = sys.argv[1]
infile   = sys.argv[2]
outfile  = sys.argv[3]
print("dictfile = " + dictfile)
print("infile   = " + infile)
print("outfile  = " + outfile)

print("loading...")
dictionary = ve.TermDictionary.load(dictfile)
vectorizer = ve.TermVectorizer(dictionary)
in_records = msgpackutil.load(infile)

print("dictionary.terms = " + str(len(dictionary.terms)))
print("in_records.len   = " + str(len(in_records)))

print("processing...")
out_records = []
for (index, (category, title, tokens)) in enumerate(in_records):
    if index % 1000 == 0:
        print(str(index) + "/" + str(len(in_records)))
    vector = vectorizer.vectorize(tokens)
    out_records.append([category, title, tokens, vector])

print("dumping...")
msgpackutil.dump(outfile, out_records)

print("ok")
