
# モデルをトレーニングする。

import sys
import random
import more_itertools
import tensorflow as tf
import numpy as np
import msgpackutil
import vectorizer as ve

sys.path.append(".")
import context as ctx

if len(sys.argv) <= 5:
    print("Usage: " + sys.argv[0] + " dictfile testfile trainfile modelfile datadir", file=sys.stderr)
    exit(1)

dictfile  = sys.argv[1]
testfile  = sys.argv[2]
trainfile = sys.argv[3]
modelfile = sys.argv[4]
datadir   = sys.argv[5]
print("dictfile  = " + dictfile)
print("testfile  = " + testfile)
print("trainfile = " + trainfile)
print("modelfile = " + modelfile)
print("datadir   = " + datadir)

print("loading...")
dictionary    = ve.TermDictionary.load(dictfile)
test_records  = msgpackutil.load(testfile)
train_records = msgpackutil.load(trainfile)
train_rail_records  = [record for record in train_records if record[0] == "rail"]
train_other_records = [record for record in train_records if record[0] == "other"]
print("test_records.len        = " + str(len(test_records)))
print("train_records.len       = " + str(len(train_records)))
print("train_rail_records.len  = " + str(len(train_rail_records)))
print("train_other_records.len = " + str(len(train_other_records)))

# 乱数シードを固定する。
random.seed(0)
np.random.seed(0)
tf.set_random_seed(0)

with tf.Graph().as_default():
    model = ctx.make_model(num_of_terms=len(dictionary.terms))

    feed_dict_test = model.make_feed_dict(test_records)

    init = tf.initialize_all_variables()

    with tf.Session() as sess:
        saver = tf.train.Saver()
        summary_writer = tf.train.SummaryWriter(datadir, graph_def=sess.graph_def)
        sess.run(init)

        print("training...")
        print("num_of_steps = " + str(ctx.num_of_steps))
        for step in range(ctx.num_of_steps):
            print("step#" + str(step))

            random.shuffle(train_rail_records)
            random.shuffle(train_other_records)

            chunked_records = []
            chunked_records.extend(train_rail_records[0:50])
            chunked_records.extend(train_other_records[0:50])
            random.shuffle(chunked_records)

            feed_dict_train = model.make_feed_dict(chunked_records)
            sess.run(model.training_op, feed_dict=feed_dict_train)

            if step % 5 == (5 - 1):
                summary_str = sess.run(model.summary_op, feed_dict=feed_dict_test)
                summary_writer.add_summary(summary_str, step)

            if step % 10 == (10 - 1):
                test_loss = sess.run(model.loss_op, feed_dict=feed_dict_test)
                test_acc  = sess.run(model.accuracy_op, feed_dict=feed_dict_test)
                print("step#" + str(step) + " -> loss: " + str(test_loss) + " / accuracy: " + str(test_acc))

        saver.save(sess, modelfile)
