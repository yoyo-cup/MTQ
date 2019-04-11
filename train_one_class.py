################For Train
from os.path import join
from typing import Tuple

import copy
import numpy as np
import torch

from torch.utils.data import DataLoader
from tqdm import tqdm

from datasets.base import OneClassDataset
from models.base import BaseModule
from models.loss_functions import SumLoss

import math



class OneClassTrainHelper(object):
    """
    Performs tests for one-class datasets (MNIST or CIFAR-10).
    """


    def __init__(self, dataset, model, optimizer, lam, checkpoints_dir, train_epoch=100, batch_size = 100):

        # type: (OneClassDataset, BaseModule, str, str) -> None
        """
        Class constructor.

        :param dataset: dataset class.
        :param model: pytorch model to train.
        :param checkpoints_dir: directory holding checkpoints for the model.
        :param output_file: text file where to save results.
        """
        self.dataset = dataset
        self.model = model
        self.name = model.name

        self.checkpoints_dir = checkpoints_dir
        self.train_epoch = train_epoch
        self.optimizer = optimizer
        self.batch_size = batch_size


        self.cl = self.dataset.normal_class

        # class for computing loss
        self.loss = SumLoss(self.model.name,lam=lam)


    def train_every_epoch(self, epoch):
            
            self.model.train()
            epoch_loss = 0
            epoch_recloss = 0
            epoch_nllk = 0

            loader = DataLoader(self.dataset, batch_size=self.batch_size)
            print(len(loader))

            for batch_idx, (x,y) in tqdm(enumerate(loader), desc=f'Training models for {self.dataset}'):
                # Clear grad for every batch

                self.model.zero_grad()
                
                # x_tra
                x = x.to('cuda')

                if self.name == 'LSA':
                    x_r = self.model(x)
                    self.loss.lsa(x, x_r)

                elif self.name == 'LSA_EN':
                    x_r, z, z_dist = self.model(x)
                    self.loss.lsa_en(x, x_r, z, z_dist)
                
                elif self.name in ['LSA_SOS', 'LSA_MAF']:
                    x_r, z, s, log_jacob_T_inverse = self.model(x)
                    self.loss.lsa_flow(x,x_r,s,log_jacob_T_inverse)
                
                elif self.name in ['SOS', 'MAF']:
                    s, log_jacob_T_inverse = self.model(x)
                    self.loss.flow(s,log_jacob_T_inverse)
                
                elif self.name == 'EN':
                    z_dist = model(x)
                    self.loss.en(z_dist)



                # backward average loss along batch
                (self.loss.total_loss).backward()

                # update params
                self.optimizer.step()

                epoch_loss = + self.loss.total_loss
                if self.name in ['LSA','LSA_EN','LSA_SOS','LSA_MAF']:
                    epoch_recloss =+ self.loss.reconstruction_loss
                    epoch_nllk = + self.loss.epoch_nllk

            # print epoch result
            print('Train Epoch: {} \tLoss: {:.6f}\tRec: {:.6f},Nllk: {:.6f}'.format(
                        epoch, epoch_loss, epoch_recloss,epoch_nllk))


    def validate(self, epoch, model, valid_dataset, prefix = 'Validation'):

        model.eval()
        val_loss = 0

        loader = DataLoader(valid_dataset,batch_size=100)


        pbar = tqdm(total=len(loader.dataset))
        pbar.set_description('Eval')

        for batch_idx, (x,y) in enumerate(loader):
        
            x = x.to('cuda')

            with torch.no_grad():
                if self.name == 'LSA':
                    x_r = self.model(x)
                    self.loss.lsa(x, x_r)

                elif self.name == 'LSA_EN':
                    x_r, z, z_dist = self.model(x)
                    self.loss.lsa_en(x, x_r, z, z_dist)
                
                elif self.name in ['LSA_SOS', 'LSA_MAF']:
                    x_r, z, s, log_jacob_T_inverse = self.model(x)
                    self.loss.lsa_flow(x,x_r,s,log_jacob_T_inverse)
                
                elif self.name in ['SOS', 'MAF']:
                    s, log_jacob_T_inverse = self.model(x)
                    self.loss.flow(s,log_jacob_T_inverse)
                
                elif self.name == 'EN':
                    z_dist = model(x)
                    self.loss.en(z_dist)


                val_loss += self.loss.total_loss.item()
            
            pbar.update(x.size(0))
            pbar.set_description('Val_loss: {:.6f}'.format(
                val_loss / pbar.n))

        return val_loss



    





    def train_one_class_classification(self):
        # type: () -> None
        """
        Actually performs trains.
        """     
        best_validation_epoch = 0
        best_validation_loss = float('inf')

        valid_dataset = self.dataset

        valid_dataset.val(self.cl)

        for epoch in range(self.train_epoch):
            # train every epoch
            
            self.train_every_epoch(epoch)
            
            # validate
            validation_loss = self.validate(epoch, self.model,valid_dataset)



            if epoch- best_validation_epoch >= 30: # converge?

                break 
            
            if validation_loss < best_validation_loss:
                best_validation_loss = validation_loss
                best_validation_epoch = epoch
                print(join(self.checkpoints_dir,f'{self.cl}{self.model.name}.pkl'))

                torch.save(self.model.state_dict(), join(self.checkpoints_dir,f'{self.dataset.normal_class}{self.model.name}.pkl'))
    
                
            print(f'Best_epoch at :{best_validation_epoch} with valid_loss:{best_validation_loss}' ) 

        print("Training finish! Normal_class:>>>>>",self.cl)

        
    

