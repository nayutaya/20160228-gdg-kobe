
# モデルを使って予測する。

import sys
import tensorflow as tf
import numpy as np
import msgpackutil
import vectorizer as ve

sys.path.append(".")
import context as ctx

if len(sys.argv) <= 2:
    print("Usage: " + sys.argv[0] + " dictfile modelfile", file=sys.stderr)
    exit(1)

dictfile  = sys.argv[1]
modelfile = sys.argv[2]
print("dictfile  = " + dictfile)
print("modelfile = " + modelfile)

print("loading...")
dictionary = ve.TermDictionary.load(dictfile)
vectorizer = ve.TermVectorizer(dictionary)

with tf.Graph().as_default():
    model = ctx.make_model(num_of_terms=len(dictionary.terms))

    with tf.Session() as sess:
        saver = tf.train.Saver()
        saver.restore(sess, modelfile)

        # title = "本日は晴天なり。"
        title = "京浜東北線、大宮―大船間で一時運転見合わせ　人身事故"
        # title = "青函トンネルで再び避難訓練、今回は順調　北海道新幹線"
        # title = "ヤンキース田中がパパに　妻の里田まいさん、男児出産"
        print(title)
        tokens = ctx.tokenizer.tokenize(title)
        print(tokens)
        term_ids = vectorizer.vectorize(tokens)
        print(term_ids)
        in_ary = model.make_term_vector(term_ids)
        in_np = np.array([in_ary])
        print(in_np)
        out = sess.run(model.output_op, feed_dict={model.input_ph: in_np})
        print(out)
        cat = np.argmax(out)
        print(cat)
        print(model.categories[cat])
