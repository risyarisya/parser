import numpy as np
import pickle
import theano
import pylearn2.datasets.mymnist as mymnist
import pylab
import matplotlib.pyplot as plt
from pylearn2.space import VectorSpace

def simulate(inputs, model):
    space = VectorSpace(inputs.shape[1])
    X = space.get_theano_batch()
    Y = model.fprop(space.format_as(X, model.get_input_space()))
    f = theano.function([X], Y)

    print(Y)
    return Y

def countCorrectResults(outputs, labels):
    correct = 0

    i = 0
    
    for output, label in zip(outputs, labels):
#          if int(output[0]*255) == int(label[0]*255):
#              correct += 1

#          print(label[0])
          
#          pylab.plot(output[0], label[0], 'bo')
#          pylab.ylim(0, 1)
#          pylab.xlim(0, 1)

#          diff[i] = int(output[0]*255)-int(label[0]*255)
#         listData.append(int(output[0]))
#         listData.append(int(label[0]))
          l = "%s, %s\n" % (output[0], label[0])
#          f.write(l)
#         csvWriter.writerow(listData)
#          i += 1
#          print(output[0], ",", label[0])
#        if np.argmax(output) == label:
#            correct += 1
#    pylab.show()
#    pylab.savefig("result1.png")
#    pylab.hist(diff, 20)
#    pylab.show()

    return correct

def score(dataset, model):
    
    outputs = simulate(dataset.X, model)
    correct = countCorrectResults(outputs, dataset.y)
    return {
        'correct': correct,
        'total': len(dataset.X)
    }

model = pickle.load(open('dae_cnn.pkl', "rb"))
test_data = mymnist.MYMNIST(which_set='test')

print ('%(correct)d / %(total)d' % score(test_data, model))
