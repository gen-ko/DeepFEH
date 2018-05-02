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

        self.p1 = tf.layers.dense(
                inputs=t3,
                units=8,
                activation=tf.nn.softmax,
                use_bias=True,
                kernel_initializer=tf.keras.initializers.glorot_uniform(),
                bias_initializer=tf.zeros_initializer(),
                kernel_regularizer=None,
                bias_regularizer=None,
                activity_regularizer=None,
                trainable=True,
                name='p1')
        
        self.p2 = tf.layers.dense(
                inputs=t3,
                units=6,
                activation=tf.nn.softmax,
                use_bias=True,
                kernel_initializer=tf.keras.initializers.glorot_uniform(),
                bias_initializer=tf.zeros_initializer(),
                kernel_regularizer=None,
                bias_regularizer=None,
                activity_regularizer=None,
                trainable=True,
                name='p2')
        
        self.p3 = tf.layers.dense(
                inputs=t3,
                units=5,
                activation=tf.nn.softmax,
                use_bias=True,
                kernel_initializer=tf.keras.initializers.glorot_uniform(),
                bias_initializer=tf.zeros_initializer(),
                kernel_regularizer=None,
                bias_regularizer=None,
                activity_regularizer=None,
                trainable=True,
                name='p3')
        
        self.p4 = tf.layers.dense(
                inputs=t3,
                units=5,
                activation=tf.nn.softmax,
                use_bias=True,
                kernel_initializer=tf.keras.initializers.glorot_uniform(),
                bias_initializer=tf.zeros_initializer(),
                kernel_regularizer=None,
                bias_regularizer=None,
                activity_regularizer=None,
                trainable=True,
                name='p4')
        
        self.p5 = tf.layers.dense(
                inputs=t3,
                units=5,
                activation=tf.nn.softmax,
                use_bias=True,
                kernel_initializer=tf.keras.initializers.glorot_uniform(),
                bias_initializer=tf.zeros_initializer(),
                kernel_regularizer=None,
                bias_regularizer=None,
                activity_regularizer=None,
                trainable=True,
                name='p5')
        
        self.p6 = tf.layers.dense(
                inputs=t3,
                units=5,
                activation=tf.nn.softmax,
                use_bias=True,
                kernel_initializer=tf.keras.initializers.glorot_uniform(),
                bias_initializer=tf.zeros_initializer(),
                kernel_regularizer=None,
                bias_regularizer=None,
                activity_regularizer=None,
                trainable=True,
                name='p6')
        
        
        
        self.dist1 = Categorical(probs=self.p1)
        self.dist2 = Categorical(probs=self.p2)
        self.dist3 = Categorical(probs=self.p3)
        self.dist4 = Categorical(probs=self.p4)
        self.dist5 = Categorical(probs=self.p5)
        self.dist6 = Categorical(probs=self.p6)
                

        self.G = tf.placeholder(dtype=tf.float32, shape=[None], name='G')
        self.a_acted = tf.placeholder(dtype=tf.int32, shape=[None], name='a_acted')

        
        self.a1 = tf.placeholder(dtype=tf.int8, shape=[None], name='a1')
        self.a2 = tf.placeholder(dtype=tf.int8, shape=[None], name='a2')
        self.a3 = tf.placeholder(dtype=tf.int8, shape=[None], name='a3')
        self.a4 = tf.placeholder(dtype=tf.int8, shape=[None], name='a4')
        self.a5 = tf.placeholder(dtype=tf.int8, shape=[None], name='a5')
        self.a6 = tf.placeholder(dtype=tf.int8, shape=[None], name='a6')
        
        a1idx = tf.stack([tf.range(tf.shape(self.a1)[0], dtype=tf.int32), self.a1], axis=1)
        a2idx = tf.stack([tf.range(tf.shape(self.a2)[0], dtype=tf.int32), self.a2], axis=1)
        a3idx = tf.stack([tf.range(tf.shape(self.a3)[0], dtype=tf.int32), self.a3], axis=1)
        a4idx = tf.stack([tf.range(tf.shape(self.a4)[0], dtype=tf.int32), self.a4], axis=1)
        a5idx = tf.stack([tf.range(tf.shape(self.a5)[0], dtype=tf.int32), self.a5], axis=1)
        a6idx = tf.stack([tf.range(tf.shape(self.a6)[0], dtype=tf.int32), self.a6], axis=1)
        
        self.logp1 = tf.log(tf.gather_nd(params=self.p1, indices=a1idx))
        self.logp2 = tf.log(tf.gather_nd(params=self.p2, indices=a2idx))
        self.logp3 = tf.log(tf.gather_nd(params=self.p3, indices=a3idx))
        self.logp4 = tf.log(tf.gather_nd(params=self.p4, indices=a4idx))
        self.logp5 = tf.log(tf.gather_nd(params=self.p5, indices=a5idx))
        self.logp6 = tf.log(tf.gather_nd(params=self.p6, indices=a6idx))
        

        self.loss = -tf.reduce_mean(self.G * (self.logp1 + self.logp2 + self.logp3 + self.logp4 + self.logp5 + self.logp6))
        self.train_op = tf.train.AdamOptimizer(lr).minimize(self.loss)
        self.sess = tf.Session()
        init = tf.global_variables_initializer()
        self.sess.run(init)
        self.saver = tf.train.Saver()
        return

    def predict(self, s):
        return self.sess.run([self.p1, self.p2, self.p3, self.p4, self.p5, self.p6], {self.s: s})[0]

    def fit(self, s, a1, a2, a3, a4, a5, a6, G):
        self.sess.run(self.train_op, {self.s: s, self.a1: a1, self.a2: a2, self.a3: a3, self.a4: a4, self.a5: a5, self.a6: a6, self.G: G})
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