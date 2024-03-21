import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
from scipy.stats import kstat
from copy import copy
from tabulate import tabulate
from IPython.display import display, HTML
from scipy.signal import savgol_filter
import os 
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA, KernelPCA
from sklearn.linear_model import LinearRegression as LR
from sklearn.kernel_ridge import KernelRidge
import pandas as pd

def gauss(x, a, b, c):
    return a*np.exp(-(x-b)**2/(2*c**2))

def lorentzian(x, a, x0, gam ):
    return a * gam**2 / ( gam**2 + ( x - x0 )**2)

def generate_spectrum(x1,x2,x3):
    
    fac1 = 1 + x1*0.2
    if x2 > 0.2:
        fac2 = 1 + x2*0.3
    else:
        fac2 = 0
    fac3 = 1 + x3*0.2
    
    atot = 1 + (x1*x2)*0.2*np.random.rand()
    
    a1 = 2
    a2 = 0.4 * fac2
    a3 = 0.2 * fac3
    a4 = 2.5*a1 /(2*fac1)
    
    #g1 = lambda x: gauss(x, a1, 1200, 60)
    #g2 = lambda x: gauss(x, a2, 1100, 60)
    #g3 = lambda x: gauss(x, a3, 1300, 100)
    #g4 = lambda x: gauss(x, a4, 1400, 40)
    
    g1 = lambda x: lorentzian(x, a1, 1200, 60)
    g2 = lambda x: lorentzian(x, a2, 1100, 60)
    g3 = lambda x: lorentzian(x, a3, 1300, 100)
    g4 = lambda x: lorentzian(x, a4, 1400, 40)
    
    x = np.linspace(1000,1500,250)
    spec = g1(x) + g2(x) + g3(x) + g4(x)
    spec = spec + np.random.randn(*spec.shape)*0.2
    
    return spec * atot, g1(x)*atot, g2(x)*atot, g3(x)*atot, g4(x)*atot 


shifts =  np.linspace(1000,1500,250)

levels = np.linspace(0,1,4)
X,Y,Z = np.meshgrid(levels,levels, levels)

design = np.vstack([X.ravel(),Y.ravel(),Z.ravel()]).T

for i,config in enumerate(design):
	spec = generate_spectrum(*config)[0]

	df = pd.DataFrame(np.vstack([shifts, spec]).T, columns = ['Raman shift [cm^-1]','Intensity [a.u.]'])
	df.to_csv('data/spec_%s.csv'%(str(i).zfill(3)))


dfd = pd.DataFrame(design, columns = ['fac1','fac2','fac3'])
dfd.to_csv('design.csv')
