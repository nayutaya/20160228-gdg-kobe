
# タイトルのトークン列から辞書を生成する。
# [[category, title, tokens], ...] -> [term, ...]

import sys
import msgpackutil
import vectorizer as ve

if len(sys.argv) <= 2:
    print("Usage: " + sys.argv[0] + " infile outfile", file=sys.stderr)
    exit(1)

infile  = sys.argv[1]
outfile = sys.argv[2]
print("infile  = " + infile)
print("outfile = " + outfile)

print("loading...")
in_records = msgpackutil.load(infile)

print("processing...")
# generator = ve.TermDictionaryGenerator()
generator = ve.TermFrequencyDictionaryGenerator(minimum=5)
for index, (category, title, tokens) in enumerate(in_records):
    if index % 1000 == 0:
        print(str(index) + "/" + str(len(in_records)))
    generator.update(tokens)

dictionary = generator.to_dictionary()
print("dictionary.terms = " + str(len(dictionary.terms)))

print("dumping...")
dictionary.save(outfile)
