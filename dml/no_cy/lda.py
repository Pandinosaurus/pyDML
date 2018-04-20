#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Linear Discriminant Analysis (LDA)

A DML that tries to minimize kNN expected error.
"""

from __future__ import absolute_import
import numpy as np
from sklearn.utils.validation import check_X_y

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as skLDA


from .dml_algorithm import DML_Algorithm


class LDA(DML_Algorithm):
    def __init__(self,num_dims=None, thres=None):
        """
            num_dims: Number of dimensions for transformed data (ignored if num_dims > num_classes or thres specified)
            thres: Fraction of variability to keep. Data dimension will be reduced until the lowest dimension that keeps 'thres' explained variance.
        """

        self.num_dims = num_dims
        self.thres = thres
        self.sklda = skLDA(n_components=num_dims) 
        
        #Metadata
        self.nd_ = None
        self.acum_eig_ = None

    def transformer(self):
        return self.L_
    
    def metadata(self):
        return {'num_dims':self.nd_, 'acum_eig':self.acum_eig_}


    def fit(self,X,y):
        X, y = check_X_y(X,y)
        self.X_ = X
        self.y_ = y
        self.n_, self.d_ = X.shape

        self.sklda.fit(X,y)
        self.explained_variance = self.sklda.explained_variance_ratio_
        self.acum_variance = np.cumsum(self.explained_variance)

        if self.thres is None and self.num_dims is None:
            self.num_dims = self.d_
        elif not self.thres is None:
            for i, v in enumerate(self.acum_variance):
                if v >= self.thres:
                    self.num_dims = i+1
                    break
        self.num_dims = min(self.num_dims,len(self.explained_variance))

        self.L_ = self.sklda.scalings_.T[:self.num_dims,:]
        
        self.nd_ = self.num_dims
        self.acum_eig_ = self.acum_variance[self.num_dims-1]/self.acum_variance[-1]

        return self

    def transform(self,X=None):
        if X is None:
            X = self.X_

        Xcent=X-self.sklda.xbar_

        return DML_Algorithm.transform(self,Xcent)