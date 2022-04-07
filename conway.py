# -*- coding: utf-8 -*-
"""
The Game of Life (GoL) module named in honour of John Conway

This module defines the classes required for the GoL simulation.

Created on Tue Jan 15 12:21:17 2019

@author: shakes
"""
import numpy as np
from scipy import signal
import rle
from scipy.ndimage import convolve

class GameOfLife:
    '''
    Object for computing Conway's Game of Life (GoL) cellular machine/automata
    '''
    def __init__(self, N=256, finite=False, fastMode=False):
        self.grid = np.zeros((N,N), np.int)
        self.neighborhood = np.ones((3,3), np.int) # 8 connected kernel
        self.neighborhood[1,1] = 0 #do not count centre pixel
        self.finite = finite
        self.fastMode = fastMode
        self.aliveValue = 1
        self.deadValue = 0
        
    def getStates(self):
        '''
        Returns the current states of the cells
        '''
        return self.grid
    
    def getGrid(self):
        '''
        Same as getStates()
        '''
        return self.getStates()
               
    def evolve(self):
        '''
        Given the current states of the cells, apply the GoL rules:
        - Any live cell with fewer than two live neighbors dies, as if by underpopulation.
        - Any live cell with two or three live neighbors lives on to the next generation.
        - Any live cell with more than three live neighbors dies, as if by overpopulation.
        - Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction
        '''
        
        def helper(r,c):
            neighborSum = 0
            directions = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]
            for x,y in directions:
                if 0 <= r + y< n and 0 <= c + x < n and self.grid[r+y][c+x] == 1:
                    neighborSum += 1
                    
            if self.grid[r][c] == 1:
                if neighborSum < 2:
                    return 0
                elif 2 <= neighborSum <= 3:
                    return 1
                else:
                    return 0
            else:
                if neighborSum == 3:
                    return 1
                else:
                    return 0
       
        
        #get weighted sum of neighbors
        n = self.getGrid().shape[0]
        tmp = np.zeros((n,n), np.int)
        
        if self.fastMode:
         #evolving using convolution
            '''kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]],int)
            convolved_grid = convolve(self.grid, kernel, mode="wrap")
            
            print(convolved_grid)
            next_board = (((self.grid == 1) & (convolved_grid > 1) & (convolved_grid < 4)) | ((self.grid == 0) (convolved_grid == 3))).astype(int)'''
            kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]],int)
            board = np.copy(self.grid)
            
            neighbor_sums = signal.convolve2d(self.grid, kernel, mode='same', boundary="wrap")

            # If fewer than 2 neighbors, cell is dead.
            board[neighbor_sums < 2] = 0
            # If 2 neighbors, cell stays in its state.
            # If 3 neighbors, cell becomes or stays active.
            board[neighbor_sums == 3] = 1
            # If >3 neighbors, cell dies
            board[neighbor_sums > 3] = 0   
            
            self.grid = board
        
        #PART A & E CODE HERE
       
        
        else:
            # iterate 2D using the helper function

            for r in range(n):
                for c in range(n):
                    tmp[r][c] = helper(r,c)
                   
             
            #implement the GoL rules by thresholding the weights
            #PART A CODE HERE
            for row in range (n):
                for column in range (n):
                    self.grid[row][column] = tmp[row][column]


            #update the grid
            #self.grid = tmp#UNCOMMENT THIS WITH YOUR UPDATED GRID
    
    def insertBlinker(self, index=(0,0)):
        '''
        Insert a blinker oscillator construct at the index position
        '''
        self.grid[index[0], index[1]+1] = self.aliveValue
        self.grid[index[0]+1, index[1]+1] = self.aliveValue
        self.grid[index[0]+2, index[1]+1] = self.aliveValue
        
    def insertGlider(self, index=(0,0)):
        '''
        Insert a glider construct at the index position
        '''
        self.grid[index[0], index[1]+1] = self.aliveValue
        self.grid[index[0]+1, index[1]+2] = self.aliveValue
        self.grid[index[0]+2, index[1]] = self.aliveValue
        self.grid[index[0]+2, index[1]+1] = self.aliveValue
        self.grid[index[0]+2, index[1]+2] = self.aliveValue
        
    def insertGliderGun(self, index=(0,0)):
        '''
        Insert a glider construct at the index position
        '''
        self.grid[index[0]+1, index[1]+25] = self.aliveValue
        
        self.grid[index[0]+2, index[1]+23] = self.aliveValue
        self.grid[index[0]+2, index[1]+25] = self.aliveValue
        
        self.grid[index[0]+3, index[1]+13] = self.aliveValue
        self.grid[index[0]+3, index[1]+14] = self.aliveValue
        self.grid[index[0]+3, index[1]+21] = self.aliveValue
        self.grid[index[0]+3, index[1]+22] = self.aliveValue
        self.grid[index[0]+3, index[1]+35] = self.aliveValue
        self.grid[index[0]+3, index[1]+36] = self.aliveValue
        
        self.grid[index[0]+4, index[1]+12] = self.aliveValue
        self.grid[index[0]+4, index[1]+16] = self.aliveValue
        self.grid[index[0]+4, index[1]+21] = self.aliveValue
        self.grid[index[0]+4, index[1]+22] = self.aliveValue
        self.grid[index[0]+4, index[1]+35] = self.aliveValue
        self.grid[index[0]+4, index[1]+36] = self.aliveValue
        
        self.grid[index[0]+5, index[1]+1] = self.aliveValue
        self.grid[index[0]+5, index[1]+2] = self.aliveValue
        self.grid[index[0]+5, index[1]+11] = self.aliveValue
        self.grid[index[0]+5, index[1]+17] = self.aliveValue
        self.grid[index[0]+5, index[1]+21] = self.aliveValue
        self.grid[index[0]+5, index[1]+22] = self.aliveValue
        
        self.grid[index[0]+6, index[1]+1] = self.aliveValue
        self.grid[index[0]+6, index[1]+2] = self.aliveValue
        self.grid[index[0]+6, index[1]+11] = self.aliveValue
        self.grid[index[0]+6, index[1]+15] = self.aliveValue
        self.grid[index[0]+6, index[1]+17] = self.aliveValue
        self.grid[index[0]+6, index[1]+17] = self.aliveValue
        self.grid[index[0]+6, index[1]+23] = self.aliveValue
        self.grid[index[0]+6, index[1]+25] = self.aliveValue
        
        self.grid[index[0]+7, index[1]+11] = self.aliveValue
        self.grid[index[0]+7, index[1]+17] = self.aliveValue
        self.grid[index[0]+7, index[1]+25] = self.aliveValue
        
        self.grid[index[0]+8, index[1]+12] = self.aliveValue
        self.grid[index[0]+8, index[1]+16] = self.aliveValue
        
        self.grid[index[0]+9, index[1]+13] = self.aliveValue
        self.grid[index[0]+9, index[1]+14] = self.aliveValue
        
    def insertFromPlainText(self, txtString, pad=0):
        '''
        Assumes txtString contains the entire pattern as a human readable pattern without comments
        '''
        file = open("glider.txt", 'r')
        row = 0

        for line in file:
            text = line.split()
            #print(str(text[0])[0])
            column = 0
            if str(text[0])[0] != "!":
                #print(column)
                #print(row)
                #print(text)
                for val in str(text[0]):
                    #print(val)

                    if val == ".":
                        #print("yes")
                        self.grid[row+pad][column+pad] = 0
                    if val == "O" or val == "o":
                        #print("no")
                        self.grid[row+pad][column+pad] = 1
                    column += 1
                row += 1
        


    def insertFromRLE(self, rleString, pad=0):
        '''
        Given string loaded from RLE file, populate the game grid
        '''
        rle_parser = rle.RunLengthEncodedParser(rleString)
        file =rle_parser.human_friendly_pattern.split("\n")
        N = max(rle_parser.size_x,rle_parser.size_y)
        self.grid = np.zeros((N,N), np.int)
        
        row = 0
        #print(file)
        for line in file[0:-1]:
            #print((str(line)))
            column = 0
            for val in str(line):
                #print(val)
                #print(row, "col" ,column)
                    #print(val)
                if val == ".":
                    #print("yes")
                    self.grid[row][column] = 0
                if val == "O" or val == "o":
                    #print("no")
                    self.grid[row][column] = 1
                column += 1
            row += 1
        

        