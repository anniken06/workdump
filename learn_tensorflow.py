import os; os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # silences TensorFlow binary was not compiled to use: AVX2

""" NOTES:
Setup:
- $ pip install tensorflow numpy

TensorFlow:
- Input -> Computational Graph (DAG) -> Output
- Feedback input feeds into an unrolled clone of the DAG to avoid infinite cycles; number of iterations = number of unrolls
-- Or, cyclic graphs can be modelled by unrolling acyclic graphs over a finite number of iterations
- Graphical computation -> allows computational parallelization

Computational Graph:
- Edges: (Tensors) multidimensional arrays that represent the data to be transformed
- Nodes: (Operators) computations that does transformations on the input

Tensors:
- Rank: number of dimensions
- Shape: number of elements for each dimension
- Data Type: data type for each element

TensorBoard
- $ tensorboard --logdir="samplemaster"
-- Automatically updates using the newest log file


https://app.pluralsight.com/player?course=tensorflow-understanding-foundations&author=janani-ravi&name=tensorflow-understanding-foundations-m3&clip=3&mode=live
"""


import tensorflow as tf
import numpy as np


write_dir = './samplemaster'

###########################################################
## Graph Definition
# tf.constants are immutable, name can be seen in tensorboard
a = tf.constant(6, name='constant_a') 
b = tf.constant(3, name='constant_b')
c = tf.constant(10, name='constant_c')
d = tf.constant(5, name='constant_d')

mul = tf.multiply(a, b, name='mul')
div = tf.div(c, d, name='div')
addn = tf.add_n([mul, div], name='addn')

###########################################################
## Graph Execution
sess = tf.Session()
print("addn result: ", sess.run(addn))

writer = tf.summary.FileWriter(write_dir, sess.graph)
writer.close()
sess.close()

###########################################################
## Numpy + Tensorflow = <3
print("Numpy Data Types == Tensorflow Data Types: ", np.int32 == tf.int32)

###########################################################
## Tensor properties shenanigans
sess = tf.Session()
zeroD = tf.constant(5)
print("zeroD rank: ", sess.run(tf.rank(zeroD)))
oneD = tf.constant(["How", "are", "you?"])
print("oneD rank: ", sess.run(tf.rank(oneD)))
twoD = tf.constant([[1.0, 2.3], [1.5, 2.911]])
print("twoD rank: ", sess.run(tf.rank(twoD)))
threeD = tf.constant([[[1, 2], [3, 4]], [[1, 2], [3, 4]]])
print("threeD rank: ", sess.run(tf.rank(threeD)))
sess.close()

###########################################################
## Reduce and Placeholders
x = tf.placeholder(tf.int32, shape=[3], name='name_x')
y = tf.placeholder(tf.int32, shape=[3], name='name_y')
sum_x = tf.reduce_sum(x, name='sum_x')
prod_y = tf.reduce_prod(y, name='prod_y')
final_div = tf.div(sum_x, prod_y, name='final_div')
final_mean = tf.reduce_mean([sum_x, prod_y], name='final_mean')

sess = tf.Session()
print("sum(x): ", sess.run(sum_x, feed_dict={x: [100, 200, 300]}))
print("prod(y): ", sess.run(prod_y, feed_dict={y: [1, 2, 3]}))
print("sum(x) / prod(y): ", sess.run(final_div, feed_dict={x: [10, 20, 30], y: [1, 2, 3]}))
print("mean(sum(x), prod(y)): ", sess.run(final_mean, feed_dict={x: [1000, 2000, 3000], y: [10, 20, 30]}))
writer = tf.summary.FileWriter(write_dir, sess.graph)
writer.close()
sess.close()   

###########################################################
## NEXT
