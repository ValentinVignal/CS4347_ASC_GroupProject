from __future__ import print_function, division

import torch
import numpy as np

# import PyTorch Functionalities
import torch.nn.functional as F
import torch.nn as nn

# Importation of personal classes
import Pytorch.DenseNet.DenseNetPerso_spectrum as dnp_s
import Pytorch.DenseNet.DenseNetPerso_audio as dnp_a
import Pytorch.DenseNet.DenseNetPerso_features as dnp_f
import Pytorch.DenseNet.DenseNetPerso_fmstd as dnp_fmstd
import Pytorch.DenseNet.DenseNetPerso_final as dnp_final

# Ignore warnings
import warnings
warnings.filterwarnings("ignore")


class DenseNetPerso(
    dnp_s.DenseNetPerso_spectrum,
    dnp_a.DenseNetPerso_audio,
    dnp_f.DenseNetPerso_features,
    dnp_fmstd.DenseNetPerso_fmstd,
    dnp_final.DenseNetPerso_final,
    nn.Module
):
    def __init__(self, dn_parameters, input_parameters):
        # the main DenseNet model -- this function initializes the layers.
        super(DenseNetPerso, self).__init__()

        # Definition of the parameters
        self.dn_parameters = dn_parameters
        self.input_parameters = input_parameters


        # Initialisation of the weights of the Neural Network
        self.init_spectrum()
        self.init_audio()
        self.init_features()
        self.init_fmstd()
        self.init_final()

    def forward(self, x_spectrum, x_audio, x_features, x_fmstd):
        # feed-forward propagation of the model. Here we have the inputs, which is propagated through the layers
        # x_spectrum has dimension (batch_size, channels, h = buffersSize/2 + 1, w=nbBuffers)
        # - for this model (16, 2, ?, ?)
        # x_audio has dimension (batch_size, channels, audio len)
        # - for this model (16, 2, ?)
        # x_features has dimension (batch_size, 2 * nbFeatures, w = nbBuffers)
        # - for this model (16, 2 * 5, ?)
        # x_fmstd has dimension (batch_size, 2 * 2 * nbFeatures)
        # - for this model (16, 2 * 2 * 5)

        #Computation of the different NN and concatenation
        x_spectrum = self.forward_spectrum(x_spectrum)
        x = x_spectrum

        x_audio = self.forward_audio(x_audio)
        x = torch.cat((x, x_audio), dim=1)

        x_features = self.forward_features(x_features)
        x = torch.cat((x, x_features), dim=1)

        x_fmstd = self.forward_fmstd(x_fmstd)
        x = torch.cat((x, x_fmstd), dim=1)

        # Computation of the last layers
        x = self.forward_final(x)

        return F.log_softmax(x, dim=1)

