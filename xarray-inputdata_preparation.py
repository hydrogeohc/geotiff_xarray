
# coding: utf-8

# # Interoperability with Xarray: Geotiff to Netcdf 
# 
# Xarray supports direct serialization and I/O to several file formats including pickle, netCDF, OPeNDAP (read-only), GRIB1/2 (read-only), and HDF by integrating with third-party libraries. Additional serialization formats for 1-dimensional data are available through pandas.

# ### Import libraries

# In[1]:

get_ipython().magic(u'matplotlib inline')

import glob
import pandas as pd
import xarray as xr
import os


# ###  Function for creating pandas DatetimeIndex for your raster files
# This function reads the time stamp in the Geotiff file name formatted by VAR_YYYYMM_location.tif (e.g. AET_198010_ok.tif)

# In[14]:

def readfiletime(flist):
    datetimecollect=[]
    for eachfile in flist:
        obj=os.path.basename(eachfile).split('_')[1]
        datetimecollect.append(pd.datetime.strptime(obj,'%Y%m').strftime('%Y-%m-%d'))
    return(pd.DatetimeIndex(datetimecollect))


# ### Loading all your raster files 

# In[3]:

os.chdir('../data')
os.getcwd()


# In[4]:

filenames = glob.glob('*.tif')
filenames
readfiletime(filenames)


# ### Create time dimension for xarray dataset

# In[5]:

time = xr.Variable('time', readfiletime(filenames))


# ### Define x, y dimension in xarray dataset

# In[7]:

chunks = {'x': 5490, 'y': 5490, 'band': 1} # x: your data arrays # y: your data arrays


# ### Concat data arrays along time dimension 

# In[8]:

da = xr.concat([xr.open_rasterio(f, chunks=chunks) for f in filenames], dim=time)


# ### Export xarray dataset to netCDF format

# In[15]:

da.to_netcdf('AET_ok.nc')


# ## Interoperability
# 
# Below is a quick example of how to export a time series from a netdf to Pandas dataframe in order to 
# 
# **1) View a Table, 2) Plot a single time series, and 3) Export to csv.**

# In[16]:

# select certain spatial subset to pandas dataframe
t_series = da.isel(x=200, y=200).to_pandas()
t_series.head()


# In[18]:

t_series.plot()


# In[17]:

# export pandas dataframe to csv format
t_series.to_csv('AET_ok.csv')


# In[ ]:



