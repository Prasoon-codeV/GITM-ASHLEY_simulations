#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 11:27:49 2024

@author: qingyuzhu
"""

import sys                                                                      
sys.path.append('/glade/work/prasoonv/gitm/library_ext/libpy') # Change it  

import numpy as np                                                              
import os                                                                       
from glob import glob                                                           
import datetime as dt  
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker

from set_polar_plots import set_polar_plot, add_axvcolorbar1                                    
from cmap_mylib import make_mid                                                 
                                                                                
from gitm_parms import gitm_contourf, gitm_contour  
from set_figs import add_str 

time_ref=dt.datetime(2012,3,21) 


path = '/glade/work/prasoonv/gitm/'
output_type = '2dall' # '2dall' or '3dall'
by_nature = ['by_neg_10/', 'by_pos_10/']
precip = ['no_precip/', 'e_precip/']
by = by_nature[0]
prec = precip[1]

data_fn = ''
if output_type == '2dall':
    data_pt = path + f'code/2dall/20120318/ashley/{by}output/2dall_final/{prec}'
    data_fn = data_pt + 'combined_parms_2dall.npz'

if output_type == '3dall':
    data_pt = path + f'3DYNAMO/3dall/20120318/ashley/outputs/{by}3dall_final/'
    data_fn = data_pt + 'combined_parms_3dall_398km.npz'
#data_fn = 'path_to_file' # Change it


data=np.load(data_fn)                                                           
ut=data['ut']                                                                   
lon=data['glon']                                                                
lat=data['glat']                                                                
rho=data['Rho']*1e12                                                                                   
pot=data['pot']/1000  
int_jh=data['int_jh']*1000
#print(int_jh)

save_pt=data_pt + 'sum_plot/'
if not os.path.exists(save_pt):
    os.makedirs(save_pt)


nut=len(ut)
cmap=make_mid(256)

"""
Change the figure size and parameters in the subplots_adjust
"""
fig,axes=plt.subplots(4,6,figsize=(56,60),subplot_kw={'projection': 'polar'})
plt.subplots_adjust(left=0.08,right=0.92,bottom=0.05,top=0.92,wspace=0.25,hspace=0.5)

for iut in range(nut):
    
     
    
    ut_in=ut[iut]
    
    if ut_in<0:
        continue
    
    
    time1=time_ref+dt.timedelta(seconds=round(ut_in*3600))
    print (time1)
    
    time_str=time1.strftime("%Y%m%d_%H%MUT")
    
    irow = int(iut/6)
    icol = iut - irow * 6
    
    
    
    #%%
    ax = axes[irow,icol]
    
    vmin=0                                                                    
    vmax=6     # Change it                                        
    cs_step=0.2                                                             
    cb_step=2
    
    parm=rho[iut]
    fp=lat>0                                                                    
    pot_max=round(parm[:,fp].max(),1)                                             
    pot_min=round(parm[:,fp].min(),1)                                             
    add_str(str(pot_max),ax,fig,72,'r',4,0,-0.01,'center','center')             
    add_str(str(pot_min),ax,fig,72,'b',1,0,-0.01,'center','center') 
    
    
    ang=lon/180*np.pi                                                           
    r=90-lat
    
    ang,r=np.meshgrid(ang,r)                                                    
    ang=ang.T                                                                   
    r=r.T                                                                       
                                                                                
    ang_offset=ut_in/12*np.pi-np.pi/2
    im=gitm_contourf(ax,parm,vmin,vmax,cs_step,cmap,ang,r,ang_offset)

    # Change the parameters if needed
    set_polar_plot(fig,ax,                                                      
                   50,32,'k','k',                                               
                   time_str,0.04,32,'magenta',                                            
                   32,5,32,8,0) 
    
    
    
save_fn = save_pt+by[:-1]+'.jpg'
print(save_fn)
plt.savefig(save_fn) # Change it
#plt.show()
#plt.close()
