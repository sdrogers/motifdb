# code to extract an MS2LDA experiment from the server and turn it into motifdb format
import sys
import getopt
import os
import requests
import csv




def main():

    short_options = "e:o:p:ahs:"
    found_options, the_rest = getopt.getopt(sys.argv[1:],short_options)
    
    all_motifs = False
    output_name_prefix = None

    experiment_id = None
    output_dir = None

    server_address = "http://ms2lda.org/"


    for option,argument in found_options:
        if option == '-h':
            usage()
            return
        if option == '-e':
            experiment_id = argument
        if option == '-o':
            output_dir = argument
        if option == '-p':
            output_name_prefix = argument
        if option == '-a':
            all_motifs = True
        if option == '-s':
            server_address = s

    
    if experiment_id == None or output_dir == None:
        usage()
        return

    process(experiment_id,output_dir,output_name_prefix,all_motifs,server_address)


def process(experiment_id,output_dir,output_name_prefix,all_motifs,server_address):
    url_sub = 'get_annotated_topics'
    if all_motifs:
        url_sub = 'get_all_topics'
    url = server_address + 'basicviz/{}/{}'.format(url_sub,experiment_id)
    print "Fetching from: {}".format(url)
    response = requests.get(url)

    annotations = {}
    spec = {}

    for name,annotation,short_annotation in response.json()[0]:
        annotations[name] = (annotation,short_annotation)
    for name,s in response.json()[1]:
        spec[name] = {}
        for f,i in s:
            spec[name][f] = i

    for name,(annotation,short_annotation) in annotations.items():
        if output_name_prefix:
            filename = output_dir + os.sep + output_name_prefix + '_' + name + '.m2m'
        else:
            filename = output_dir + os.sep + name + '.m2m'
        with open(filename,'w') as f:
            writer = csv.writer(f,delimiter = ',',dialect='excel')
            if output_name_prefix:
                writer.writerow(['#NAME ' + output_name_prefix + '_' +name])
            else:
                writer.writerow(['#NAME ' + name])
            writer.writerow(['#DESCRIPTION ' + "Automatically generated from experiment {} from {}".format(experiment_id,server_address)])

            if annotation:
                writer.writerow(['#ANNOTATION ' + " ".join(annotation.encode('utf8').split(','))])
            if short_annotation:
                writer.writerow(['#SHORT_ANNOTATION ' + " ".join(short_annotation.encode('utf8').split(','))])

            s = zip(spec[name].keys(),spec[name].values())
            s = sorted(s,key = lambda x: x[1],reverse = True)
            for f,i in s:
                writer.writerow([f,i])


def usage():
    print "typical usage: python extract_from_server.py -e <experiment_id> -o <output_dir> -p <output_name_prefix>"
    print "additional options: -h (help), -a (return all motifs, not just those that have been annotated), -s <server_address>"
    

if __name__ == '__main__':
    main()
