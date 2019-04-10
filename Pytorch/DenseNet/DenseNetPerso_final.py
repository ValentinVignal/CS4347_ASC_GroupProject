from __future__ import print_function, division

import torch
import numpy as np

# import PyTorch Functionalities
import torch.nn.functional as F
import torch.nn as nn

# Ignore warnings
import warnings
warnings.filterwarnings("ignore")


class DenseNetPerso_final(nn.Module):
    def init_final(self):
        # Initialisation of the weights of the features part of the NN
        super(DenseNetPerso_final, self).__init__()

        ##### Fully connected layers #####
        self.nn_final_fc = nn.ModuleList([])
        for i in range(self.dn_parameters['final']['nb_layers']):
            if i == 0:
                # Fully Connected
                self.nn_final_fc.append(
                    nn.Linear(
                        self.input_parameters['final']['len'],
                        self.dn_parameters['final']['layers_size'][i]
                    )
                )
            else:
                # Fully Connected
                self.nn_final_fc.append(
                    nn.Linear(
                        self.dn_parameters['final']['layers_size'][i-1],
                        self.dn_parameters['final']['layers_size'][i]
                    )
                )
            if i != self.dn_parameters['final']['nb_layers'] - 1:
                # Relu
                """ --> To do during forward computation"""
                # Dropout
                self.nn_final_fc.append(nn.Dropout(0.2))

    def forward_final(self, x):
        # feed-forward propagation of the model.
        # x_spectrum has dimension (batch_size, concatenation of precedent layers)
        # - for this model (16, ?)

        # Computation of the fully connected layers of the NN
        ifc = 0
        for i in range(self.dn_parameters['final']['nb_layers']):
            x = self.nn_final_fc[ifc](x)    # Fully connected
            ifc += 1
            if i != self.dn_parameters['final']['nb_layers'] - 1:
                x = F.relu(x)
                x = self.nn_final_fc[ifc](x)
                ifc += 1

        return x
