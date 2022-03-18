# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 19:10:44 2022

@author: User
"""
import pandas as pd
import numpy as np
from word2number import w2n
import math, discord, random
import dataframe_image as dfi
import matplotlib.pyplot as plt
from sklearn import linear_model

class Dataframe:
    def __init__(self, df=[], frame_flag=False, cleaning=False, n=[], reg_flag=False):
        self.df = df
        self.frame_flag = frame_flag
        self.cleaning = cleaning
        self.n = n
        self.reg_flag = reg_flag
        
    def load(self, filename, sep=","):
        self.filename = filename
        self.df = pd.read_csv(filename, sep=sep)
        self.cleaning = False
        self.frame_flag = True
        
    def unload(self):
        if self.frame_flag:
            self.df = []
            self.n = []
            self.cleaning = False
            self.reg_flag = False
            self.frame_flag = False            
            return True
        else:
            return False
        
    def clean(self):
        if self.frame_flag:
            self.df.rename(columns={"salary($)":'salary'},inplace=True)
            self.df.rename(columns={"test_score(out of 10)":'test_score'},inplace=True)
            self.df.rename(columns={"interview_score(out of 10)":'interview_score'},inplace=True)
            self.df.experience = self.df.experience.fillna("zero")
            self.df.experience = self.df.experience.apply(w2n.word_to_num)
            median_experience = math.floor(self.df['experience'].mean())
            self.df.loc[self.df.experience == 0, 'experience'] = median_experience
            median_t_score = math.floor(self.df['test_score'].mean())
            self.df['test_score'] = self.df['test_score'].fillna(median_t_score)
            median_i_score = math.floor(self.df['interview_score'].mean())
            self.df['interview_score'] = self.df['interview_score'].fillna(median_i_score)
            self.cleaning = True        
            return True
        else:
            return False
        
    def showFrame(self, filename1="dataframe.png", filename2="dataframe.csv"):
        if self.frame_flag:
            frame_short = self.df.head(11)
            image = discord.File(filename1)
            data = discord.File(filename2)
            dfi.export(frame_short,filename1)
            self.df.to_csv(filename2,mode='w',index=False)
            return(image, data)
        else:
            return False
    
    def showGraph(self, filename="graph.png"):
        if self.frame_flag:
        
            if self.cleaning:
                # %matplotlib inline
                plt.xlabel('Salary')
                plt.ylabel('Experience')
                image = discord.File(filename)
                plt.scatter(self.df.salary,self.df.experience,color='red',marker='.')
                if self.reg_flag:
                    plt.scatter(self.n,self.df.experience,color='blue',marker='+')
                plt.savefig("graph.png")
                plt.close()
                return image    
                
            else:
                return "False"
                
        else:
            return False
    
    def Regression(self):
        if self.frame_flag:
            if self.cleaning:
                reg = linear_model.LinearRegression()
                reg.fit(self.df[['experience','test_score','interview_score']],self.df['salary'])
                self.n = []
                for i in range(50):
                    self.n = np.append(self.n,reg.predict([[random.randint(1, 15),random.randint(5, 10),random.randint(5,10)]]))
                self.reg_flag = True
                return True
            else:
                return "False"

        else:
            return False