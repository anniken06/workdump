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
"""


import tensorflow as tf
import numpy as np


write_dir = './samplemaster'

###########################################################
print("Graph Definition==================================")
###########################################################
# tf.constants are immutable, name can be seen in tensorboard
a = tf.constant(6, name='constant_a') 
b = tf.constant(3, name='constant_b')
c = tf.constant(10, name='constant_c')
d = tf.constant(5, name='constant_d')

mul = tf.multiply(a, b, name='mul')
div = tf.div(c, d, name='div')
addn = tf.add_n([mul, div], name='addn')

###########################################################
print("Graph Execution===================================")
###########################################################
sess = tf.Session()
print("addn result: ", sess.run(addn))

writer = tf.summary.FileWriter(write_dir, sess.graph)
writer.close()
sess.close()

###########################################################
print("Tensor properties=================================")
###########################################################
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
print("Numpy Data Types == Tensorflow Data Types: ", np.int32 == tf.int32)

###########################################################
print("With-Context, Reduce, Fetches, and Placeholders===")
###########################################################
x = tf.placeholder(tf.int32, shape=[3], name='name_x')
y = tf.placeholder(tf.int32, shape=[3], name='name_y')
sum_x = tf.reduce_sum(x, name='sum_x')
prod_y = tf.reduce_prod(y, name='prod_y')
final_div = tf.div(sum_x, prod_y, name='final_div')
final_mean = tf.reduce_mean([sum_x, prod_y], name='final_mean')

with tf.Session() as sess:
    print("sum(x): ", sess.run(sum_x, feed_dict={x: [100, 200, 300]}))
    print("prod(y): ", sess.run(prod_y, feed_dict={y: [1, 2, 3]}))
    print("sum(x) / prod(y): ", sess.run(final_div, feed_dict={x: [10, 20, 30], y: [1, 2, 3]}))
    print("mean(sum(x), prod(y)): ", sess.run(final_mean, feed_dict={x: [1000, 2000, 3000], y: [10, 20, 30]}))
    print("intermediates of a new sum(x), prod(y): ", sess.run(fetches=[sum_x, prod_y], feed_dict={x: [1, 2, 3], y: [4, 5, 6]}))

###########################################################
print("Variables=========================================")
###########################################################
#tf.Variables are mutable tensors that persist across multiple sessions
number = tf.Variable(2)
multiplier = tf.Variable(1)

init_l = tf.variables_initializer([number, multiplier])
init_g = tf.global_variables_initializer()
result_number = number.assign(tf.multiply(number, multiplier))
result_multiplier = multiplier.assign_add(1)

with tf.Session() as sess:
    sess.run(init_l)
    print("Result number * multiplier = ", sess.run(result_number))
    print("Increment multiplier, new value = ", sess.run(result_multiplier))
    print("Reinitialization...")
    sess.run(init_g)
    for i in range(10):
        print("Result number * multiplier = ", sess.run(result_number))
        print("Increment multiplier, new value = ", sess.run(result_multiplier))

###########################################################
print("Graphs============================================")
###########################################################
g2 = tf.Graph()
with g2.as_default():
    with tf.Session() as sess:
        A = tf.constant([5, 7], tf.int32, name='A')
        x = tf.placeholder(tf.int32, name='x')
        y = tf.pow(A, x, name='y')
        print(sess.run(y, feed_dict={x: [3, 5]}))
        print(y.graph is g2)

default_graph = tf.get_default_graph()
with tf.Session() as sess:
    A = tf.constant([5, 7], tf.int32, name='A')
    x = tf.placeholder(tf.int32, name='x')
    y = A + x
    print(sess.run(y, feed_dict={x: [3, 5]}))
    print(y.graph is default_graph)

###########################################################
print("Scopes============================================")
###########################################################
A = tf.constant([4], tf.int32, name='A')
B = tf.constant([5], tf.int32, name='B')
C = tf.constant([6], tf.int32, name='C')
x = tf.placeholder(tf.int32, name='x')

with tf.name_scope("Equation_1"):  # y = Ax^2 + Bx + C
    Ax2 = tf.multiply(A, tf.pow(x, 2), name="Ax2")
    Bx = tf.multiply(B, x, name="Bx")
    y1 = tf.add_n([Ax2, Bx, C], name="calc_1")

with tf.name_scope("Equation_2"):  # y = Ax^2 + Bx^2
    Ax2 = tf.multiply(A, tf.pow(x, 2), name="Ax2")
    Bx2 = tf.multiply(B, tf.pow(x, 2), name="Bx2")
    y2 = tf.add_n([Ax2, Bx2], name="calc_1")

with tf.name_scope("Final_Sum"):
    y = y1 + y2

with tf.Session() as sess:
    print(sess.run(y, feed_dict={x: [10]}))
    writer = tf.summary.FileWriter(write_dir, sess.graph)
    writer.close()

###########################################################
print("Interactive Session===============================")
###########################################################
sess = tf.InteractiveSession()
A = tf.constant([4], tf.int32, name='A')
x = tf.placeholder(tf.int32, name='x')
y = A * x
print(y.eval(feed_dict={x: [5]}))  # equivalent to: tf.get_default_session().run(y)
sess.close()

###########################################################
print("Module 4===============================")
###########################################################
#https://app.pluralsight.com/player?course=tensorflow-understanding-foundations&author=janani-ravi&name=tensorflow-understanding-foundations-m3&clip=8&mode=live