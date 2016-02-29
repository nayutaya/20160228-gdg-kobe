
import tensorflow as tf

import normalizer as no
import tokenizer as to
import mlp

categories   = ["rail", "other"]
num_of_steps = 500
tokenizer    = to.NormalizedTokenizer(
    normalizer=no.BasicNormalizer(),
    tokenizer=to.LetterBigramTokenizer())

def make_model(num_of_terms):
    optimizer = tf.train.AdamOptimizer(0.01)
    model = mlp.MultiLayerPerceptron(optimizer=optimizer, categories=categories, num_of_terms=num_of_terms, num_of_hidden_nodes=100)
    print("model.optimizer           = " + str(type(model.optimizer)))
    print("model.num_of_categories   = " + str(model.num_of_categories))
    print("model.num_of_terms        = " + str(model.num_of_terms))
    print("model.num_of_hidden_nodes = " + str(model.num_of_hidden_nodes))
    return model
