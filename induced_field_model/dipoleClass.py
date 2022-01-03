#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 20:17:02 2020

@author: davidaguillard
"""
from constants import *

class dipoleClass:

    def __init__(self, location, b_felt, chi, volume):
        self.loc = location
        self.s = chi
        self.b = b_felt
        self.v = volume

    def magnetizeDipole(self, b_felt, chi):
        self.b = b_felt
        self.s = chi

#     def get_Location(self):
#         location = self.loc
#         return(location)

# x = dipole(0, 5, 2)

# x.loc = 5
# print(x.loc)

# x.get_location = 4
# print(x.get_Location)
