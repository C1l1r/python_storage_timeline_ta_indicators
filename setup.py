from setuptools import setup, find_packages

with open("README.md", 'r') as f:
      long_description = f.read()

setup(name='python_storage_timeline_ta_indicators',
      version='0.1',
      description='Tool to calculate technical analysis indicators in a continuous time series data',
      long_description = long_description,
      author='Oleksandr Namchuk',
      author_email='c1l1rua@gmail.com',
      url='https://github.com/C1l1r/python_storage_timeline_ta_indicators',
      packages=find_packages(),
      install_requires=['plotly', 'numpy', 'pandas', 'ta-lib', 'pandas_ta', 'tensorflow', 'matplotlib', 'seaborn', 'sklearn', '']
     )
#%%

#%%

#%%

#%%
