
import tensorflow as tf
import numpy as np

# REF:
# * 落ちこぼれないためのTensorFlow Tutorialコード - Qiita
#   http://qiita.com/TomokIshii/items/92a266b805d7eee02b1d
# * TensorFlowのMLPコードで"Wine"を分類 - Qiita
#   http://qiita.com/TomokIshii/items/2cab778a3192d561a1ef

class MultiLayerPerceptron:
    def __init__(self, optimizer, categories, num_of_terms, num_of_hidden_nodes):
        self.optimizer           = optimizer
        self.categories          = categories
        self.num_of_categories   = len(self.categories)
        self.num_of_terms        = num_of_terms
        self.num_of_hidden_nodes = num_of_hidden_nodes

        self.input_ph      = tf.placeholder(tf.float32, [None, self.num_of_terms], name="input")
        self.supervisor_ph = tf.placeholder(tf.float32, [None, self.num_of_categories], name="supervisor")

        with tf.name_scope("inference") as scope:
            weight1_var    = tf.Variable(tf.truncated_normal([self.num_of_terms, self.num_of_hidden_nodes], stddev=0.1), name="weight1")
            weight2_var    = tf.Variable(tf.truncated_normal([self.num_of_hidden_nodes, self.num_of_categories], stddev=0.1), name="weight2")
            bias1_var      = tf.Variable(tf.zeros([self.num_of_hidden_nodes]), name="bias1")
            bias2_var      = tf.Variable(tf.zeros([self.num_of_categories]), name="bias2")
            hidden_op      = tf.nn.relu(tf.matmul(self.input_ph, weight1_var) + bias1_var)
            self.output_op = tf.nn.softmax(tf.matmul(hidden_op, weight2_var) + bias2_var)

        with tf.name_scope("loss") as scope:
            cross_entropy = -tf.reduce_sum(self.supervisor_ph * tf.log(self.output_op))
            l2_sqr        = tf.nn.l2_loss(weight1_var) + tf.nn.l2_loss(weight2_var)
            lambda_2      = 0.01
            self.loss_op  = cross_entropy + lambda_2 * l2_sqr
            tf.scalar_summary("loss", self.loss_op)

        with tf.name_scope("training") as scope:
            self.training_op = self.optimizer.minimize(self.loss_op)

        with tf.name_scope("accuracy") as scope:
            correct_prediction = tf.equal(tf.argmax(self.output_op, 1), tf.argmax(self.supervisor_ph, 1))
            self.accuracy_op   = tf.reduce_mean(tf.cast(correct_prediction, "float"))
            tf.scalar_summary("accuracy", self.accuracy_op)

        self.summary_op = tf.merge_all_summaries()

    def make_term_vector(self, term_ids):
        array = [0] * self.num_of_terms
        for term_id in term_ids: array[term_id] = 1
        return array

    def make_category_vector(self, category_id):
        array = [0] * self.num_of_categories
        array[category_id] = 1
        return array

    def make_feed_dict(self, records):
        c2i = {category:index for index, category in enumerate(self.categories)}
        term_tensor     = [self.make_term_vector(term_ids)          for (category, _, _, term_ids) in records]
        category_tensor = [self.make_category_vector(c2i[category]) for (category, _, _, term_ids) in records]
        return {
            self.input_ph:      np.array(term_tensor),
            self.supervisor_ph: np.array(category_tensor),
        }
