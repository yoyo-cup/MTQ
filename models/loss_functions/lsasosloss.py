import torch
import torch.nn as nn

from models.loss_functions.autoregression_loss import AutoregressionLoss
from models.loss_functions.reconstruction_loss import ReconstructionLoss

from models.loss_functions.flow_loss import FlowLoss
from models.loss_functions.qtloss import QTLoss

class LSASOSLoss(nn.Module):
    """
    Implements the loss of a LSA model.
    It is a sum of the reconstruction loss and the autoregression loss.
    """
    def __init__(self, quantile_flag = False, lam=1):
        # type: (int, float) -> None
        """
        Class constructor.

        :param cpd_channels: number of bins in which the multinomial works.
        :param lam: weight of the autoregression loss.
        """
        super(LSASOSLoss, self).__init__()

        self.lam = lam

        # Set up loss modules
        self.reconstruction_loss_fn = ReconstructionLoss()
        
        if quantile_flag:
            self.autoregression_loss_fn = QTLoss()
        else:
            self.autoregression_loss_fn = FlowLoss()

        # Numerical variables
        self.reconstruction_loss = None
        self.autoregression_loss = None

        self.total_loss = None
        self.quantile_flag = quantile_flag

    def forward(self, x, x_r, s, z, nagtive_log_jacob, average = True):
        # type: (torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor) -> torch.Tensor
        """
        Forward propagation.

        :param x: the batch of input samples.
        :param x_r: the batch of reconstructions.
        :param z: the batch of latent representations.
        :param z_dist: the batch of estimated cpds.
        :return: the loss of the model (averaged along the batch axis).
        """
        # Compute pytorch loss
        rec_loss = self.reconstruction_loss_fn(x, x_r,average)
        
        if self.quantile_flag:
            arg_loss = self.autoregression_loss_fn(z, nagtive_log_jacob, average)
        else:
            arg_loss = self.autoregression_loss_fn(s,nagtive_log_jacob,average)
        
        tot_loss = rec_loss + self.lam * arg_loss

        # Store numerical
        self.reconstruction_loss = rec_loss
        self.autoregression_loss = arg_loss
        self.total_loss = tot_loss

        return tot_loss