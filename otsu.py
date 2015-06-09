from PIL import Image
import numpy
import os
import struct
from pylearn2.utils import serial

data_dir = "/Users/suzukiay/workspace/pyimage/cifar10"
data_dir_cifar10 = os.path.join(data_dir, "cifar-10-batches-py")

def bi(im_in):
    hist, bins = numpy.histogram(im_in, bins=256)
    av = im_in.mean()
    b = numpy.arange(256)

    av1 = 0.0
    av2 = 0.0
    max_no = 0
    max = 0.0
    for i in range(256):
        data1 = 0.0
        data2 = 0.0
        count1 = 0.0
        count2 = 0.0
        bp1 = 0.0
        bp2 = 0.0
        tmp = 0

        count1 = numpy.sum(hist[:i])
        data1 = numpy.sum((hist*b)[:i])

        if count1 != 0:
            av1 = data1/count1
            bp1 = numpy.sum((((b-av1)**2)*hist)[:i])/count1

        count2 = numpy.sum(hist[i:])
        data2 = numpy.sum((hist*b)[i:])

        if count2 != 0:
            av2 = data2/count2
            bp2 = numpy.sum((((b-av2)**2)*hist)[i:])/count2
        
        class1 = count1 * bp1 + count2 * bp2
        class2 = count1 * ((av1 -av)**2) + count2 * ((av2-av)**2)

        tmp = class2 / class1

        if max<tmp:
            max = tmp
            max_no = i

    return max_no

def _load_batch_cifar10(filename, dtype='float64'):
    path = os.path.join(data_dir_cifar10, filename)
#    batch = numpy.load(path)
    batch = serial.load(path)
    data = batch['data']
    return data.astype(dtype)

def _grayscale(a):
    return a.reshape(a.shape[0], 3, 32, 32).mean(1).reshape(a.shape[0], -1)

def cifar10(grayscale=True):
    x_train = []
    for k in range(5):
        x = _load_batch_cifar10("data_batch_%d" % (k+1), 'float64')
        x_train.append(x)

    x_train = numpy.concatenate(x_train, axis=0)
    
    #test
    x_test = _load_batch_cifar10("test_batch", 'float64')

    if grayscale:
        x_train = _grayscale(x_train)
        x_test = _grayscale(x_test)

    return x_train, x_test

def bi_lbl(im, lbl):
    for i in range(im.shape[0]):
        print("i=", i)
        th = bi(im[i])
        lbl += struct.pack('B', th)
    return lbl

def gray_data(im, data):
    for i in range(im.shape[0]):
        d = numpy.uint8(im[i].T.flatten('C'))
        ld = d.tolist()
        ad = struct.pack('1024B', *ld)
        data += ad
    return data


if __name__ == "__main__":
    train, test = cifar10()
    train_data = b''
    test_data = b''
    train_labl = b''
    test_labl = b''

    train_data += struct.pack('>4i', 2051, 50000, 32, 32)
    train_labl += struct.pack('>2i', 2049, 50000)
    test_data += struct.pack('>4i', 2051, 10000, 32, 32)
    test_labl += struct.pack('>2i', 2049, 10000)

#    train_labl = bi_lbl(train, train_labl)
#    test_labl = bi_lbl(test, test_labl)
    train_data = gray_data(train, train_data)
    test_data = gray_data(test, test_data)
 
    fp = open('CIFAR_MONO_train_data', 'wb')
    fp.write(train_data)
    fp.close()

#    fp = open('CIFAR_MONO_train_label', 'wb')
#    fp.write(train_labl)
#    fp.close()

    fp = open('CIFAR_MONO_test_data', 'wb')
    fp.write(test_data)
    fp.close()

#    fp = open('CIFAR_MONO_test_label', 'wb')
#    fp.write(test_labl)
#    fp.close()

    print("done.")
#    inim = Image.open("./img/16.jpg").convert('L')
#    th = bi(numpy.array(inim))
#    print(th)
