#!/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import requests
import json
import string
import subprocess
import sys
import os,argparse

version='0.2.25'

def get_django(django_url=None,url_port=8000,ids=None,list_tag=False,data=None):
    if django_url is None:
        django_url='http://xxx.xxx.xxx.xxx:xxxx/list/'
    else:
        if url_port is None:
            django_url_arr=django_url.split(':')
            if len(django_url_arr) == 1:
                url_port=8000
            else:
                url_port=django_url_arr[1]
        django_url='http://{0}:{1}/list/'.format(django_url_arr[0],url_port)

    ss = requests.Session()
    rc={}
    if data is not None:
        rc=data
    if list_tag or ids == 'all':
        host_url='{0}'.format(django_url)
        try:
            r = ss.post(host_url, verify=False)
        except requests.exceptions.RequestException as e:
            return False
        json_data=json.loads(r.text)
        if ids is None:
            return json_data

    if ids is None:
        return False

    if ids == 'all':
        ids=''
        for ii in json_data:
           if ids == '' or ids == 'all':
               ids='{0}'.format(ii)
           else:
               ids='{0},{1}'.format(ids,ii)

    for ii in ids.split(','):
        if not ii in rc.keys(): 
            host_url='{0}{1}/'.format(django_url,ii)
            try:
                r = ss.post(host_url, verify=False)
            except requests.exceptions.RequestException as e:
                return False
            try:
                json_data=json.loads(r.text)
            except:
                return False
            rc[json_data['id']]={}
            rc[json_data['id']]={'code':json_data['code'],'crelay':json_data['crelay']}

    return rc


def rshell(cmd,dbg=False):
    Popen=subprocess.Popen
    PIPE=subprocess.PIPE
    STDOUT=subprocess.STDOUT
    if dbg:
       p = Popen('set -x\n'+ cmd + '\n', shell=True, stdout=PIPE, stderr=STDOUT, executable='/bin/bash',bufsize=1)
    else:
       p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT, executable='/bin/bash',bufsize=1)
    for line in iter(p.stdout.readline, b''):
       print(line.decode('utf-8').rstrip())
    p.stdout.close()
    p.wait()
    return p.returncode,'',''


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='ksh options')
    parser.add_argument('otherthings',nargs='*')
    parser.add_argument('-v','--version', action='version', version='%(prog)s '+version)
    parser.add_argument('--list',action='store_true', dest='list', help='get function list')
    parser.add_argument('-l','--lib_idx', action='store', dest='lib_idx', help='Server Item Numbers(ex:1,2,3...) for functions')
    parser.add_argument('-r','--run', action='store_true', dest='run', help='Get Library and run a shell',default='run')
    parser.add_argument('-p','--print', action='store_true', dest='print', help='Print got functions')
    parser.add_argument('-f','--file', action='store', dest='shell_file', help='Run a shell script file',metavar="FILE")
    parser.add_argument('-d','--dbg', action='store_true', dest='dbg', help='Run with DBG mode')

    args = parser.parse_args()

    if args.list:
        cmd=get_django(list_tag=True)
        for ii in sorted(cmd, key=cmd.get):
            print('%05s : %s' %(ii, cmd[ii]))
        sys.exit(0)

    #print(len(sys.argv),sys.argv)
    if args.lib_idx is None:
       print('{0} --help for help'.format(sys.argv[0]))
       sys.exit(0)
    

    kdict=get_django(ids=args.lib_idx)
    ref=None
    if kdict is False:
        print('Something wrong function numbers({0})'.format(args.lib_idx))
        sys.exit(0)
        
    if kdict is not None:
        for ii in kdict.keys():
            if len(kdict[ii]['crelay']) > 0:
               for jj in kdict[ii]['crelay'].split(','):
                   if not jj in kdict.keys():
                       if ref is None:
                           ref='{0}'.format(jj)
                       else:
                           ref='{0},{1}'.format(ref,jj)
    if ref is not None:
       kdict=get_django(ids=ref,data=kdict)
    cmd=None
    if kdict is not None:
       for ii in kdict.keys():
           if cmd is None:
               cmd='{0}'.format(string.replace(kdict[ii]['code'],'\r',''))
           else:
               cmd='{0}\n\n{1}'.format(cmd,string.replace(kdict[ii]['code'],'\r',''))


    if cmd is None:
        print('Something wrong function numbers({0})'.format(args.lib_idx))
        sys.exit(0)

    if args.shell_file:
        f=open(args.shell_file,'r')
        shell_cmd=f.read()
        f.close()
        cmd='{0}\n\n{1}'.format(cmd,shell_cmd)

    if args.otherthings:
        cmd='{0}\n\n{1}'.format(cmd,args.otherthings[0])

    if args.print:
        #print('#!/bin/bash\n{0}'.format(cmd))
        print(cmd)
        sys.exit(0)

    if args.run:
        ex=rshell(cmd,args.dbg)
        sys.exit(ex[0])
