#!/usr/bin/env python
"""
Generic python script.
"""
__author__ = "Alex Drlica-Wagner"
import pandas as pd
import fitsio

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('filename')
    args = parser.parse_args()
    
    data = pd.read_csv(args.filename).to_records(index=False)
    data.dtype.names = [n.upper() for n in data.dtype.names]
    outfile = args.filename.replace('.csv','.fits')

    print('Writing %s...'%outfile)
    fitsio.write(outfile,data,clobber=True)
