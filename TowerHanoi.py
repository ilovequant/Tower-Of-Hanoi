# -*- coding: utf-8 -*-
"""
Created on Thu May 10 14:27:16 2018

@author: SIMC
"""

import numpy as np
import itertools


def get_moved_state(state):             
    '''
    generate states of all possible movements   
    '''
        
    disc_to_move = np.zeros(len(state))
    disc_no_left = np.zeros(len(state))
    disc_no_right = np.zeros(len(state))
    comp = np.array(state)
 		     # find the lightest disk in each stack
    for i in range(1, len(state)):             
        for j in range(i):
            if comp[i] == comp[j]:
                disc_to_move [i] = 3            # if identical, not the minimum disk, break the inner loop
                break
            if comp[i] - comp[j] == 1:
                disc_no_left [i] = 1       # if one left disk is 1 left than to_move_disk, then no left move, mark the position
            if comp[i] - comp[j] == -1:
                disc_no_right [i] = 1     # if one left disk is 1 right than to_move_disk, then no right move, mark the position

    moved_states = list()
    for i in range(len(state)):                                   
        if disc_to_move [i] != 3 and disc_no_left [i] == 0 and disc_no_right [i] ==0:              # disks okay to move left or right
                state_list_L = list(state)
                state_list_R = list(state)
                if state_list_R[i] + 1 < len(state) :                                
                    state_list_R[i] = state_list_R[i] + 1
                if state_list_L[i] -1 >= 0:
                    state_list_L[i] = state_list_L[i] - 1  
        
        elif disc_to_move [i] != 3 and disc_no_left [i] == 1 and disc_no_right[i] == 0:           # disks okay to move right only
                state_list_L = list(state)
                state_list_R = list(state)
                if state_list_R[i] + 1 < len(state) :
                    state_list_R[i] =  state_list_R[i] + 1

        elif disc_to_move [i] != 3 and disc_no_left [i] == 0 and disc_no_right[i] == 1:           # disks okay to move left only
                state_list_L = list(state)
                state_list_R = list(state)
                if state_list_L[i] -1 >= 0:
                    state_list_L[i] =  state_list_L[i] - 1  
                    
        else:
            break
                    
        if tuple(state_list_L) == state and tuple(state_list_R) != state:                        # append updated right moved state
            moved_states.append(tuple(state_list_R))
        
        elif tuple(state_list_L) != state and tuple(state_list_R) == state:                      # append updated left moved state
            moved_states.append(tuple(state_list_L))
            
        elif tuple(state_list_L) != state and tuple(state_list_R) != state:                      # append states with both the left and right move
            moved_states.append(tuple(state_list_R))
            moved_states.append(tuple(state_list_L))
            
    return moved_states
     

def Ctr_Comp(N, M, T):     
    '''
    computer center of mass in T moves
    N is the number of discs
    M is the kilos of discs
    '''
    states = list(itertools.product(range(1), repeat=M))                # initial list
    state_list = states[0]
    ctr_mass_num = np.zeros(N)
    ctr_mass_den = np.zeros(N)
    ctr_mass = 0
    for n in range(T):                                                  # compute the center of mass in T moves
         next_state = get_moved_state(tuple(state_list))
         state1 = next_state[np.random.choice(len(next_state))]
         state_list = list(state1)
         for i in range(N):
             ctr_mass_num[i] += (i+1)*state_list[i]
             ctr_mass_den[i] += state_list[i]
         ctr_mass = sum(ctr_mass_num)/sum(ctr_mass_den)
    return ctr_mass
        

def Stats(N, M, T, play_times):      
    '''
    simulations, compute play_times average stats
    '''         
    stat = np.zeros(play_times)
    for n in range(play_times):
        stat[n] = Ctr_Comp(N, M, T)
    print(np.mean(stat), np.std(stat))

N = 3                                 # number of discs in the Towers of Hanoi game
M = 3                                 # number of positions
T = 16                                # number of moves
Stats(N, M, T, 10000)



'''
M = 3, N = 3, T = 16,   mean: 1.23001610868
M = 3, N = 3, T = 16,   standard deviation: 0.183213610693
M = 6, N = 6, T = 256, mean: 2.02272188437
M = 6, N = 6, T = 256, standard deviation: 0.250712928445
'''
