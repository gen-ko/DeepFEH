import tensorflow as tf

from tensorflow.contrib.distributions import Categorical


class PolicyNet(object):
    def __init__(self, lr,  s_len, a_len):
        self.s = tf.placeholder(dtype=tf.float32, shape=(None, s_len), name='s')

        t1 = tf.layers.dense(
                inputs=self.s,
                units=16,
                activation=tf.nn.relu,
                use_bias=True,
                kernel_initializer=tf.keras.initializers.glorot_uniform(),
                bias_initializer=tf.zeros_initializer(),
                kernel_regularizer=None,
                bias_regularizer=None,
                activity_regularizer=None,
                trainable=True,
                name='t1')

        t2 = tf.layers.dense(
                inputs=t1,
                units=16,
                activation=tf.nn.relu,
                use_bias=True,
                kernel_initializer=tf.keras.initializers.glorot_uniform(),
                bias_initializer=tf.zeros_initializer(),
                kernel_regularizer=None,
                bias_regularizer=None,
                activity_regularizer=None,
                trainable=True,
                name='t2')

        t3 = tf.layers.dense(
                inputs=t2,
                units=16,
                activation=tf.nn.relu,
                use_bias=True,
                kernel_initializer=tf.keras.initializers.glorot_uniform(),
                bias_initializer=tf.zeros_initializer(),
                kernel_regularizer=None,
                bias_regularizer=None,
                activity_regularizer=None,
                trainable=True,
                name='t3')

        self.p = tf.layers.dense(
                inputs=t3,
                units=a_len,
                activation=tf.nn.softmax,
                use_bias=True,
                kernel_initializer=tf.keras.initializers.glorot_uniform(),
                bias_initializer=tf.zeros_initializer(),
                kernel_regularizer=None,
                bias_regularizer=None,
                activity_regularizer=None,
                trainable=True,
                name='p')

        self.dist = Categorical(probs=self.p)
        self.a = self.dist.sample()

        self.G = tf.placeholder(dtype=tf.float32, shape=[None], name='G')
        self.a_acted = tf.placeholder(dtype=tf.int32, shape=[None], name='a_acted')

        a_indices = tf.stack([tf.range(tf.shape(self.a_acted)[0], dtype=tf.int32), self.a_acted], axis=1)
        self.gathered_p = tf.gather_nd(params=self.p, indices=a_indices)
        self.logpi = tf.log(self.gathered_p)

        self.loss = -tf.reduce_mean(self.G * self.logpi)
        self.train_op = tf.train.AdamOptimizer(lr).minimize(self.loss)
        self.sess = tf.Session()
        init = tf.global_variables_initializer()
        self.sess.run(init)
        self.saver = tf.train.Saver()
        return

    def predict(self, s):
        return self.sess.run(self.a, {self.s: s})[0]

    def fit(self, s, a_acted, G):
        self.sess.run(self.train_op, {self.s: s, self.a_acted: a_acted, self.G: G})
        return

    def save(self, path: str):
        self.saver.save(self.sess, path)
        return

    def load(self, path: str):
        self.saver.restore(self.sess, path)
        return
    
    
class CriticNet(object):
    def __init__(self, lr,  s_len):
        with tf.variable_scope("critic"):
            self.s = tf.placeholder(dtype=tf.float32, shape=(None, s_len), name='s')
    
            t1 = tf.layers.dense(
                    inputs=self.s,
                    units=16,
                    activation=tf.nn.relu,
                    use_bias=True,
                    kernel_initializer=tf.keras.initializers.glorot_uniform(),
                    bias_initializer=tf.zeros_initializer(),
                    kernel_regularizer=None,
                    bias_regularizer=None,
                    activity_regularizer=None,
                    trainable=True,
                    name='t1')
    
            t2 = tf.layers.dense(
                    inputs=t1,
                    units=16,
                    activation=tf.nn.relu,
                    use_bias=True,
                    kernel_initializer=tf.keras.initializers.glorot_uniform(),
                    bias_initializer=tf.zeros_initializer(),
                    kernel_regularizer=None,
                    bias_regularizer=None,
                    activity_regularizer=None,
                    trainable=True,
                    name='t2')
    
            t3 = tf.layers.dense(
                    inputs=t2,
                    units=16,
                    activation=tf.nn.relu,
                    use_bias=True,
                    kernel_initializer=tf.keras.initializers.glorot_uniform(),
                    bias_initializer=tf.zeros_initializer(),
                    kernel_regularizer=None,
                    bias_regularizer=None,
                    activity_regularizer=None,
                    trainable=True,
                    name='t3')
    
            v = tf.layers.dense(
                    inputs=t3,
                    units=1,
                    activation=None,
                    use_bias=True,
                    kernel_initializer=tf.keras.initializers.glorot_uniform(),
                    bias_initializer=tf.zeros_initializer(),
                    kernel_regularizer=None,
                    bias_regularizer=None,
                    activity_regularizer=None,
                    trainable=True,
                    name='v')
            
            self.v = tf.reshape(v, shape=[-1])
    
            self.R = tf.placeholder(dtype=tf.float32, shape=[None], name='R')
            
            self.loss = tf.losses.mean_squared_error(
                        labels=self.R,
                        predictions=self.v
                        )

            self.train_op = tf.train.AdamOptimizer(lr).minimize(self.loss)
            self.sess = tf.Session()
            init = tf.global_variables_initializer()
            self.sess.run(init)
            self.saver = tf.train.Saver()
        return

    def predict(self, s):
        return self.sess.run(self.v, {self.s: s})

    def fit(self, s, R):
        self.sess.run(self.train_op, {self.s: s, self.R: R})
        return

    def save(self, path: str):
        self.saver.save(self.sess, path)
        return

    def load(self, path: str):
        self.saver.restore(self.sess, path)
        return