
# テスト用データ、学習用データを抽出する。
# [[category, title, tokens, vector], ...] -> [[category, title, tokens, vector], ...] + [[category, title, tokens, vector], ...]

import sys
import random
import msgpackutil

if len(sys.argv) <= 3:
    print("Usage: " + sys.argv[0] + " infile testfile trainfile", file=sys.stderr)
    exit(1)

infile    = sys.argv[1]
testfile  = sys.argv[2]
trainfile = sys.argv[3]
print("infile    = " + infile)
print("testfile  = " + testfile)
print("trainfile = " + trainfile)

print("loading...")
in_records = msgpackutil.load(infile)

rail_records  = [record for record in in_records if record[0] == "rail"]
other_records = [record for record in in_records if record[0] == "other"]

print("rail_records.len  = " + str(len(rail_records)))
print("other_records.len = " + str(len(other_records)))

# 乱数シードを固定する。
random.seed(0)

random.shuffle(rail_records)
random.shuffle(other_records)

# テスト用データをを取り出す。
num_of_test_records = 1000
test_records = []
test_records.extend(rail_records[0:num_of_test_records])
del rail_records[0:num_of_test_records]
test_records.extend(other_records[0:num_of_test_records])
del other_records[0:num_of_test_records]
random.shuffle(test_records)

# 学習用データを取り出す。
train_records = []
train_records.extend(rail_records)
train_records.extend(other_records)
random.shuffle(train_records)

print("test_records.len  = " + str(len(test_records)))
print("train_records.len = " + str(len(train_records)))

print("dumping...")
msgpackutil.dump(testfile, test_records)
msgpackutil.dump(trainfile, train_records)
