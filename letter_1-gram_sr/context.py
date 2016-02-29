
import tensorflow as tf

import normalizer as no
import tokenizer as to
import sr

categories   = ["rail", "other"]
num_of_steps = 500
tokenizer    = to.NormalizedTokenizer(
    normalizer=no.BasicNormalizer(),
    tokenizer=to.LetterUnigramTokenizer())

def make_model(num_of_terms):
    optimizer = tf.train.GradientDescentOptimizer(0.01)
    model = sr.SoftmaxRegressions(optimizer=optimizer, categories=categories, num_of_terms=num_of_terms)
    print("model.optimizer         = " + str(type(model.optimizer)))
    print("model.num_of_categories = " + str(model.num_of_categories))
    print("model.num_of_terms      = " + str(model.num_of_terms))
    return model
