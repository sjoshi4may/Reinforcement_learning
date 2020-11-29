#!/usr/bin/env python3
from tkinter import *
from tkinter import messagebox
import pandas as pd
import numpy as np
import pickle
import sys
from collections import Counter
def disable_buttons():
    for button in buttons:
        button.config(state = DISABLED)
# button clicked functions
def b_click(b):
    global clicked, count, cur_state
    pos_x, pos_y = b._name.split('_')[-1]
    pos_x,pos_y = int(pos_x),int(pos_y)
    
    if b['text']=='' and clicked == True:
        b['text'] = 'X'
        cur_state['state'][pos_x,pos_y]=-1
        
        count+=1
        
        game_over_flag,winner_flag = check_winner(cur_state)
        game_over(game_over_flag,winner_flag)
        
        if game_over_flag is False:
            pos_x,pos_y = ai_move(cur_state,val_states)
            check = f'{pos_x}{pos_y}'
            for button in buttons:
                if button._name.split('_')[-1] == check:
                    button['text']='O'
                    break
            cur_state['state'][pos_x,pos_y] = 1
        
            count+=1
            game_over_flag,winner_flag = check_winner(cur_state)
            game_over(game_over_flag,winner_flag)
    
    elif b['text']=='' and clicked == False:
        messagebox.showerror("Tic Tac Toe", "Hey, Wait for your turn!")
    else:
        messagebox.showerror("Tic Tac Toe", "Hey, Pick another box!")


        
# AI agent helper functions


def ai_move(cur_state,val_states):
    test = pickle.loads(pickle.dumps(cur_state['state']))
    pos_states = []
    for row,col in np.argwhere(test==0):
        test[row,col] = 1
        st = pickle.loads(pickle.dumps(val_states[val_states['state'].apply(lambda x: (x==test).all())]))
        pos_states.append(st)
        test[row,col]=0
    pos_states = pd.concat(pos_states)
    explore_exploit_flag = np.random.choice(['exploit','explore'],p=[1,0])
    if explore_exploit_flag=='explore':
        next_stg = pickle.loads(pickle.dumps(pos_states.sample(1,weights=pos_states['probability']).squeeze()))            
    else:
        next_stg = pickle.loads(pickle.dumps(pos_states[pos_states['probability']==pos_states['probability'].max()].sample(1).squeeze()))
    
    return np.argwhere(next_stg['state']!=cur_state['state'])[0]


def check_winner(cur_state):
    global winner_flag
    test = cur_state['state']
    res = np.concatenate([test.sum(axis=0),test.sum(axis=1)])
    res = np.append(res,np.array(np.trace(test) ))
    res = np.append(res,np.array(np.trace(np.fliplr(test))))
    counts = Counter(res)
    
    if len(test[test==0])<1:
        game_over_flag = True
        winner_flag = 'Draw'
        disable_buttons()
    
    elif counts.get(3,0)>=1:
        winner_flag = False
        game_over_flag = True
        disable_buttons()
        
    elif counts.get(-3,0)>=1:
        winner_flag = True
        game_over_flag = True
        disable_buttons()
    else:
        game_over_flag = False
        
    return game_over_flag, winner_flag

def game_over(game_over_flag,winner_flag):
    if game_over_flag is True:
        if winner_flag is True:
            messagebox.showinfo('Congratulation, You Win!')
        elif winner_flag is False:
            messagebox.showinfo('Aww, You lost')
        else:
            messagebox.showinfo('It\'s a draw.')
            
            
root = Tk()
root.title("Tic-Tac-Toe")

# X starts so true

def reset():
    global b1,b2,b3,b4,b5,b6,b7,b8,b9,clicked, count,winner_flag, game_over_flag, val_states, cur_state, buttons
    
    winner_flag = False
    game_over_flag = False
    clicked = True
    count = 0 
    val_states = pd.read_pickle('./tic_tac_toe_rand_agnt_policy.pkl')

    initial_state = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    cur_state = pickle.loads(pickle.dumps(val_states.loc[val_states['state'].apply(lambda x: (x==initial_state).all())].squeeze())) 

# Buttons
    b1 = Button(root,text='',font=('Helvetica',20),height=3,width=6,bg='blue',command=lambda:b_click(b1))
    b2 = Button(root,text='',font=('Helvetica',20),height=3,width=6,bg='blue',command=lambda:b_click(b2))
    b3 = Button(root,text='',font=('Helvetica',20),height=3,width=6,bg='blue',command=lambda:b_click(b3))    
    b4 = Button(root,text='',font=('Helvetica',20),height=3,width=6,bg='blue',command=lambda:b_click(b4))
    b5 = Button(root,text='',font=('Helvetica',20),height=3,width=6,bg='blue',command=lambda:b_click(b5))
    b6 = Button(root,text='',font=('Helvetica',20),height=3,width=6,bg='blue',command=lambda:b_click(b6))
    b7 = Button(root,text='',font=('Helvetica',20),height=3,width=6,bg='blue',command=lambda:b_click(b7))
    b8 = Button(root,text='',font=('Helvetica',20),height=3,width=6,bg='blue',command=lambda:b_click(b8))
    b9 = Button(root,text='',font=('Helvetica',20),height=3,width=6,bg='blue',command=lambda:b_click(b9))

    b1._name = 'button_00'
    b2._name = 'button_01'
    b3._name = 'button_02'
    b4._name = 'button_10'
    b5._name = 'button_11'
    b6._name = 'button_12'
    b7._name = 'button_20'
    b8._name = 'button_21'
    b9._name = 'button_22'
    
# grid buttons to screen
    b1.grid(row=0,column=0)
    b2.grid(row=0,column=1)
    b3.grid(row=0,column=2)

    b4.grid(row=1,column=0)
    b5.grid(row=1,column=1)
    b6.grid(row=1,column=2)

    b7.grid(row=2,column=0)
    b8.grid(row=2,column=1)
    b9.grid(row=2,column=2)

    buttons = [b1,b2,b3,b4,b5,b6,b7,b8,b9]

# Create Menu

my_menu = Menu(root)
root.config(menu=my_menu)

# create options
options = Menu(my_menu,tearoff = False)
my_menu.add_cascade(label = "Options", menu = options)
options.add_command(label="Reset game", command=reset)
reset()
root.mainloop()
