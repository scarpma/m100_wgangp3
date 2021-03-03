#!/usr/bin/env python
# coding: utf-8

from db_utils import *

def build_critic(fs, fm, init_sigma, init_mean, alpha):
    """
    fs = 20 dimensione filtro
    fm = 4 numero di filtri
    init_sigma = 0.2 varianza distribuzione normale per l'inizializzazione
        dei pesi del  modello
    init_mean = 0.0 media distribuzione normale per l'inizializzazione dei
        pesi del  modello
    """
    reg = l2(l=0.001)
    #reg = l1(l=0.001)

    input_ = Input(shape=(SIG_LEN, CHANNELS))

    # SMALL FILTERS CONVOLUTIONS
    y = input_
    small_fs = 11
    y = Conv1D(fm//16, small_fs, strides=1, padding='same', kernel_regularizer=reg,
        bias_regularizer=reg, kernel_initializer=RandomNormal(init_mean,
            init_sigma))(y)
    y = ReLU(negative_slope=alpha)(y)
    y = Conv1D(fm//8, small_fs, strides=1, padding='same', kernel_regularizer=reg,
        bias_regularizer=reg, kernel_initializer=RandomNormal(init_mean,
            init_sigma))(y)
    y = ReLU(negative_slope=alpha)(y)
    y = Conv1D(fm//8, small_fs, strides=1, padding='same', kernel_regularizer=reg,
        bias_regularizer=reg, kernel_initializer=RandomNormal(init_mean,
            init_sigma))(y)
    y = ReLU(negative_slope=alpha)(y)
    y = reduce_mean(y, axis=-2)


    # LARGE FILTERS CONVOLUTIONS
    x = input_
    #2000x1
    x = Conv1D(fm//16, fs, strides=2, padding='same', kernel_regularizer=reg,
        bias_regularizer=reg, kernel_initializer=RandomNormal(init_mean,
            init_sigma))(x)
    #d.add(ELU())
    x = ReLU(negative_slope=alpha)(x)
    #
    x = Conv1D(fm//8, fs, strides=2, padding='same', kernel_regularizer=reg,
        bias_regularizer=reg, kernel_initializer=RandomNormal(init_mean,
            init_sigma))(x)
    #d.add(ELU())
    x = ReLU(negative_slope=alpha)(x)
    #
    x = Conv1D(fm//4, fs, strides=2, padding='same', kernel_regularizer=reg,
        bias_regularizer=reg, kernel_initializer=RandomNormal(init_mean,
            init_sigma))(x)
    #d.add(ELU())
    x = ReLU(negative_slope=alpha)(x)
    #
    x = Conv1D(fm//2, fs, strides=2, padding='same', kernel_regularizer=reg,
        bias_regularizer=reg, kernel_initializer=RandomNormal(init_mean,
            init_sigma))(x)
    #d.add(ELU())
    x = ReLU(negative_slope=alpha)(x)
    #
    x = Conv1D(fm, fs, strides=5, padding='same', kernel_regularizer=reg,
        bias_regularizer=reg, kernel_initializer=RandomNormal(init_mean,
            init_sigma))(x)
    #d.add(ELU())
    x = ReLU(negative_slope=alpha)(x)
    #
    x = Concatenate()([ Flatten()(x), Flatten()(y)] ) 
    #
    x = Dense(1, kernel_regularizer=reg, bias_regularizer=reg)(x)
    #1x1
    #d.summary()
    model = Model(input_, x)
    model.summary()

    return model




if __name__ == '__main__':
    fs = 100
    fm = 128
    init_sigma = 0.02
    init_mean = 0.01
    alpha = 0.3
    noise_dim = 100
    critic = build_critic(fs, fm, init_sigma, init_mean, alpha)
