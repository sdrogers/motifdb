# -*- coding: utf-8 -*-

import glob
import os

METADATA_FIELDS = ['COMMENT','NAME','ANNOTATION','SHORT_ANNOTATION']

def load_db(db_list,db_path):
    # loads the dbs listed in the list
    # items in the list should be folder names in the dirctory indicated by db_path
    filenames = []
    for dir_name in db_list:
        glob_path = os.path.join(db_path,dir_name,'*.m2m')
        print "Looking in {}".format(glob_path)
        new_filenames = glob.glob(glob_path)
        filenames += new_filenames
        print "\t Found {}".format(len(new_filenames))

    print "Found total of {} motif files".format(len(filenames))

    metadata = {}
    spectra = {}

    for filename in filenames:
        motif_name = os.path.split(filename)[-1]
        spectra[motif_name],metadata[motif_name] = parse_m2m(filename)

    return spectra,metadata

def parse_m2m(filename):
    metadata = {}
    spectrum = {}
    with open(filename,'r') as f:
        for line in f:
            if line.startswith('#'):
                # it's some metadata
                tokens = line.split()
                key = tokens[0][1:]
                if key in METADATA_FIELDS:
                    new_value = " ".join(tokens[1:])
                    if not key in metadata:
                        metadata[key] = new_value
                    else:
                        # is it a list already?
                        current_value = metadata[key]
                        if isinstance(current_value,list):
                            metadata[key].append(new_value)
                        else:
                            metadata[key] = [current_value].append(new_value)
                else:
                    print "Found unknown key ({}) in {}".format(key,filename)
            elif len(line)>0:
                mz,intensity = line.split(',')
                spectrum[mz] = float(intensity)
    return spectrum,metadata


