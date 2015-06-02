"""
.. todo::

    WRITEME
"""
import os
import logging

import numpy
from theano.compat.six.moves import xrange

from pylearn2.datasets import cache, dense_design_matrix
from pylearn2.expr.preprocessing import global_contrast_normalize
from pylearn2.utils import contains_nan
from pylearn2.utils import serial
from pylearn2.utils import string_utils


_logger = logging.getLogger(__name__)

def bi(im_in):

    hist, bins = numpy.histogram(im_in, bins=256)
    av = im_in.mean()

    av1 = 0.0
    av2 = 0.0
    max_no = 0
    max = 0.0
    for i in range(256):
        data = 0.0
        count1 = 0.0
        count2 = 0.0
        bp1 = 0.0
        bp2 = 0.0
        tmp = 0
        for j in range(i):
            count1 += hist[j]
            data += hist[j] * j

        if count1 != 0:
            av1 = data/count1
            for j in range(i):
                bp1 += ((j-av1)**2) * hist[j]
            bp1 /= count1
            
        data = 0

        for j in range(i, 256):
            count2 += hist[j]
            data += hist[j] * j

        if count2 != 0:
            av2 = data/count2
            for j in range(i, 256):
                bp2 += ((j-av2)**2) * hist[j]

            bp2 /= count2
        
        class1 = count1 * bp1 + count2 * bp2
        class2 = count1 * ((av1 -av)**2) + count2 * ((av2-av)**2)

        tmp = class2 / class1

        if max<tmp:
            max = tmp
            max_no = i

    return max_no


def _grayscale(a):
    return a.reshape(a.shape[0], 3, 32, 32).mean(1).reshape(a.shape[0], -1)

class CIFAR10MONO(dense_design_matrix.DenseDesignMatrix):

    def __init__(self, which_set, start=None, stop=None):
        
        dtype = 'float32'
        ntrain = 50000
        nvalid = 0
        ntest = 10000

        self.img_shape = (3, 32, 32)
        self.img_size = numpy.prod(self.img_shape)

        fnames = ['data_batch_%i' % i for i in range(1, 6)]
        datasets = {}
        datapath = os.path.join(
            string_utils.preprocess('${PYLEARN2_DATA_PATH}'),
            'cifar10', 'cifar-10-batches-py')
        for name in fnames + ['test_batch']:
            fname = os.path.join(datapath, name)
            if not os.path.exists(fname):
                raise IOError(fname + " was not found.")
            datasets[name] = cache.datasetCache.cache_file(fname)

        lenx = numpy.ceil((ntrain + nvalid) / 10000.) * 10000 # = 50000
        x = numpy.zeros((lenx, self.img_size), dtype=dtype)
        y = numpy.zeros((lenx, 1), dtype='uint8')
        y_test = numpy.zeros((lenx, 1), dtype='uint8')

        nloaded = 0
        for i, fname in enumerate(fnames):
            _logger.info('loading file %s' % datasets[fname])
            data = serial.load(datasets[fname])
            x[i*10000:(i+1)*10000, :] = data['data'] / 255.0
            nloaded += 10000
            if nloaded >= ntrain + nvalid + ntest:
                break

        x_train = _grayscale(x)

        # expect val
        for i in range(ntrain):
            y[i, 0] = bi(x_train[i])            
            

        # load test data
        _logger.info('loading file %s' % datasets['test_batch'])
        data = serial.load(datasets['test_batch'])
        xt = data['data'][0:ntest] / 255.0

        x_test = _grayscale(xt)

        # proess this data
        Xs = { 'train': x_train[0:ntrain],
               'test': x_test[0:ntest]}

        for i in range(ntest):
            y_test[i, 0] = bi(x_test[i])

        Ys = { 'train': y[0:ntrain],
               'test': y_test[0:ntest]}
            

        X = numpy.cast['float32'](Xs[which_set])
        y = Ys[which_set]

        if which_set == 'test':
            y = y.reshape((y.syape[0], 1))
            

        view_converter = dense_design_matrix.DefaultViewConverter((32, 32, 1))
        super(CIFAR10MONO, self).__init__(X=X, y=y, view_converter=view_converter, y_labels=10)

    def adjust_for_viewer(self, X):
        
        return numpy.clip(X*2. -1., -1., 1.)

    def adjust_to_be_viewed_with(self, X, other, per_example=False):
        return self.adjust_for_viewer(X)

    def get_test_set(self):
        args = {}
        args.update(self.args)
        del args['self']
        args['which_set'] = 'test'
        args['shart'] = None
        args['stop'] = None
        return CIFAR10MONO(**args)
