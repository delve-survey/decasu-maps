import argparse
import decasu
from datetime import datetime
from decasu.utils import op_str_to_code
from decasu.healpix_consolidator import HealpixConsolidator
from decasu import decasu_globals
import os
import numpy as np
import multiprocessing
import time
import esutil
import glob
from tqdm import tqdm
import healsparse as hsp

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Make survey property maps for DECam')

    parser.add_argument('-c', '--configfile', action='store', type=str, required=True,
                        help='YAML config file')
    parser.add_argument('-b', '--bands', action='store', type=str, required=False,
                        help='Bands to generate map for, comma delimited')
    parser.add_argument('-n', '--ncores', action='store', type=int, required=False,
                        default=1, help='Number of cores to run on.')
    parser.add_argument('-o', '--outputpath', action='store', type=str, required=True,
                        help='Output path')
    parser.add_argument('-k', '--keep_intermediate_files', action='store_true',
                        required=False, help='Keep intermediate files')

    args = parser.parse_args()
    
    if args.bands is None:
        bands = ["g"]

    else:
        bands = [b for b in args.bands.split(',')]
    
    print("bands ={}".format(bands))
    
    config = decasu.Configuration.load_yaml(args.configfile)
    print(config.map_types)
    outputpath=args.outputpath
    clear_intermediate_files=True
    if args.keep_intermediate_files:
        clear_intermediate_files=False
    
    fname_list = []
    mapfiles_list = []
    num=2
    for map_type in config.map_types.keys():
        for operation in config.map_types[map_type]:
                    op_code = op_str_to_code(operation)
                    for band in bands:
                        # Get full map filename
                        fname = os.path.join(outputpath, config.map_filename(band,
                                                                             map_type,
                                                                             op_code))
                        # Check if file exists
                        if os.path.isfile(fname):
                            print(fname,'found.')
                            continue

                        # Assemble all the individual pixel maps
                        fname_template = config.tile_map_filename_template(band,
                                                                           map_type,
                                                                           op_code)


                        mapfiles = sorted(glob.glob(os.path.join(outputpath,
                                                                 '????????????',
                                                                 fname_template)))
                        fname_list.append(fname)
                        mapfiles_list.append(mapfiles)
    subname_list = []
    for i in fname_list:
        sub_name_1 = i[:7]+'p0_'+i[7:]
        sub_name_2 = i[:7]+'p1_'+i[7:]
        subname_list = np.append(subname_list,[sub_name_1,sub_name_2])
        
    for i in range(len(fname_list)):
        if len(mapfiles_list[i]) == 0:
            print(fname_list[i],' skipped. len is',len(mapfiles_list[i]))
            continue
        mapfiles_p0 = mapfiles_list[i][:3000]
        mapfiles_p1 = mapfiles_list[i][3000:]
        clear_intermediate_files=False
        intermap_list = []
        while len(intermap_list) != 2:
            hsp.cat_healsparse_files(mapfiles_p0,subname_list[0],in_memory=False)
            intermap_list = [subname_list[0]]
            subname_list = subname_list[1:]

            hsp.cat_healsparse_files(mapfiles_p1,subname_list[0],in_memory=False)
            intermap_list = np.append(intermap_list,subname_list[0])
            subname_list = subname_list[1:]

            hsp.cat_healsparse_files(intermap_list,fname_list[i],in_memory=False)
            print(fname_list[i],' has been made...')
    
