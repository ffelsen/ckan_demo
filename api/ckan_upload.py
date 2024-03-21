from ckanapi import RemoteCKAN
import io 
import requests
import csv
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
import numpy as np
import os

def get_plot(filepath):
    df = pd.read_csv(filepath)
    
    
    x = df['Raman shift [cm^-1]']
    y = df['Intensity [a.u.]']
    
    peaks = find_peaks(y, prominence=1)[0]
    
    def gauss(x,A,s,m):
        return A*np.exp(-0.5*((x-m)/s)**2)
    
    def fit_fun(x , A1,s1,m1,A2,s2,m2):
        return gauss(x,A1,s1,m1)+gauss(x,A2,s2,m2)
    
    pars, cov = curve_fit(fit_fun, x,y, p0=[1,100,x[peaks[0]],1,100,x[peaks[1]]])
    
    fig,(ax1,ax2) =plt.subplots(ncols=2, figsize=(10,5))
    ax1.plot(x,y)
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

    
    for p in peaks:
        ax1.axvline(x[p], c='k')
        ax1.text(x[p]+10,y[p], '%.1f'%x[p],bbox=props)
    ax1.set_title('peak detection')
    ax2.set_title('peak fit')
    ax2.plot(x,y, c='k',alpha=0.2)
    ax2.plot(x,gauss(x,*pars[:3]))
    ax2.plot(x,gauss(x,*pars[3:]))
    ax2.plot(x,fit_fun(x,*pars), lw=2, c='k')
    
    for ax in (ax1,ax2):
        ax.set_xlabel(df.columns[1])
        ax.set_ylabel(df.columns[2])
        ax.set_xlim(1000,1500)
    plt.tight_layout()
    plt.savefig('temp.png')
    
    with open('temp.png', 'rb') as f:
        byte_im = f.read()
    return byte_im


def make_spectrum_entry(ckan, filepath, entry_name, meta_data):
    package = ckan.action.package_create(name = entry_name, **meta_data)
    with open(filepath) as csvdata:

        res = ckan.call_action(action='resource_create', data_dict={'package_id':meta_data['title'],
                                                              #'url':'https://dummyvalue.de', 
                                                              'description': 'experimental data',
                                                              'format': 'CSV',
                                                              'name': 'raman spectrum '+entry_name,
                                                              'resource_type':'raman spectrum raw'}, 
                                                              files={'upload': csvdata})
    
    view = ckan.call_action(action='resource_view_create', data_dict={'resource_id':res['id'],
                                                                      'view_type':'recline_view',
                                                                      'title':'spec_view'})
    
    res = ckan.call_action(action='resource_create', data_dict={'package_id':meta_data['title'],
                                                          #'url':'https://dummyvalue.de', 
                                                          'description': 'processed data',
                                                          'format': 'PNG',
                                                          'name': 'analysis plot '+entry_name,
                                                          'resource_type':'analysis plot'}, 
                                                          files={'upload': get_plot(filepath)})  

    return True 
    
session = requests.Session()
session.verify = False

data_path = 'csvs/data'

samples = os.listdir(data_path)

files = os.listdir(data_path)


# The CKAN Hosts 
server_url = 'https://localhost:5000'
ckan_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJmamtOQUNCZmN6YnI1bHZ4XzlzdVhlS1E0RThXclN3SFJZb1U3Y0dKVDBVIiwiaWF0IjoxNzExMDMwODgwfQ.AtFA3O6ikp11TKzJHwzuOnvZNVLaRzcvUb0kAtNBfxU'
with RemoteCKAN(server_url, apikey=ckan_token, session=session) as test: 

    for sample in samples:
        files = os.listdir(data_path+'/'+sample)
        for filename in files[:1]:
            filepath = data_path+'/'+sample+'/'+filename

            entry_name = filename.split('.')[0]
            
            meta_data = {'title' : entry_name,
                     'author' : 'Frederic Felsen', 
                     'author_email' : 'frederic.felsen@tum.de', 
                     'maintainer' : 'admin', 
                     'maintainer_email' : 'admin@ckan.de', 
                     'license_id' : 'CC-BY',
                     'groups' : [{'name':'stein_group'}],
                     'tags' : [{'name':'raman',},{'name':sample}],
                     'owner_org' : 'eco',}
            
            make_spectrum_entry(test, filepath, entry_name, meta_data)
    
