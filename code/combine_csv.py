'''
Combine two csv files.
'''

import pandas as pd
import glob
import os
import argparse

if __name__=='__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-c','--csv',help='Path to files')
    
    args = parser.parse_args()
    
    files = [b for b in args.csv.split(',')]
    
    f1 = pd.read_csv(files[0])
    f2 = pd.read_csv(files[1])
    
    combo = pd.concat((f1,f2))
    combo.to_csv(files[0][0:7]+'.csv')
    
