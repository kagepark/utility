#!/usr/bin/python
# Enhanced sorting function from old my shell code by Kage
# Kage Park at 2018/09/12
# Sort strings
import sys,select
import argparse
version='0.2.2'


def ksort(string=None,new_line='\n',field_id=None,field_symbol='space',reverse=False,print_field=None,num=False):
    if string is None:
        return False

    sort_arr=[]
    line_arr=string.split(new_line)
    if field_id is None or field_symbol is None:
        if reverse:
            if num:
               return sorted(line_arr,reverse=True,key=float)
            else:
               return sorted(line_arr,reverse=True)
        else:
            if num:
               return sorted(line_arr,key=float)
            else:
               return sorted(line_arr)
    else:
        sort_dict={}
        for ii in list(line_arr):
            if field_symbol == 'space':
                ii_tmp=ii.split()
            else:
                ii_tmp=ii.split(field_symbol)
            if len(ii_tmp) < field_id-1:
               print('ignore field_id({0}) at "{1}" string'.format(field_id,ii))
            else:
               if print_field is None:
                   sort_dict[ii_tmp.pop(field_id)]=ii
               else:
                   tmp=''
                   for ss in print_field.split(','):
                       if len(ii_tmp) < int(ss)-1:
                           print('out of range print_field({0})'.format(ss))
                       else:
                           if tmp == '':
                               tmp='{0}'.format(ii_tmp[int(ss)]) 
                           else:
                               if field_symbol == 'space':
                                   tmp='{0} {1}'.format(tmp,ii_tmp[int(ss)]) 
                               else:
                                   tmp='{0}{1}{2}'.format(tmp,field_symbol,ii_tmp[int(ss)]) 
                   sort_dict[ii_tmp.pop(field_id)]=tmp
        if reverse:
            if num:
                sort_dict_keys=sorted(sort_dict.keys(),reverse=True,key=float)
            else:
                sort_dict_keys=sorted(sort_dict.keys(),reverse=True)
        else:
            if num:
                sort_dict_keys=sorted(sort_dict.keys(),key=float)
            else:
                sort_dict_keys=sorted(sort_dict.keys())
        for jj in sort_dict_keys:
            sort_arr.append(sort_dict[jj])
        return sort_arr

if __name__ == "__main__":
    if len(sys.argv) < 2:
       print('{0} --help for help'.format(sys.argv[0]))
       sys.exit()

    parser = argparse.ArgumentParser(
       prog='ksort',
       description='ksort for sorting string lines or sorting string lines in file',

       epilog='''
example)
sorting string:
./ksort "1
6
9
3
2
7"

reverse sorting string:
./ksort -r "1
6
9
3
2
7"

sorting file size :
./ksort -i 4 -s space "$(ls -l)"

sorting file size reverse:
./ksort -i 4 -s space -r "$(ls -l)"

sorting file size, and print size and filename:
./ksort -i 4 -s space -p 8,4 "$(ls -l)"
       ''',
       formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('otherthings',nargs='*')
    parser.add_argument('-v','--version', action='version', version='%(prog)s '+version)
    parser.add_argument('-i','--field_id', action='store', dest='id', help='sorting filed id (start from 0), only one',type=int)
    parser.add_argument('-s','--field_symbol', default='space', action='store', dest='symbol', help='field spliting symbol (default: white space) (ex: " " for only one space, ":" for :)')
    parser.add_argument('-p','--print_field', action='store', dest='printid', help="print field id(start from 0) (ex: 1,3,...), it should need -i")
    parser.add_argument('-n','--newline', action='store', dest='newline', help="new line symbol (default: Linux (\\n))")
    parser.add_argument('-r','--reverse', action='store_true', dest='reverse', help='reverse sort')
    parser.add_argument('-m','--num', action='store_true', dest='num', help='numerical sort')
    parser.add_argument('-f','--file', action='store', dest='filename', help='Input text file',metavar="FILE")
    args = parser.parse_args()
    new_line='\n'
    if args.newline:
       new_line=args.newline


    strings=None
    if select.select([sys.stdin,],[],[],0.0)[0]:
        for line in sys.stdin:
           if strings is None:
               strings='{0}'.format(line)
           else:
               strings='{0}{1}{2}'.format(strings,new_line,line)
    if args.otherthings:
        if strings is None:
            strings=args.otherthings[0]
        else:
            strings='{0}{1}{2}'.format(strings,new_line,args.otherthings[0])
    if args.filename:
        f=open(args.shell_file,'r')
        if strings is None:
            strings=f.read()
        else:
            strings='{0}{1}{2}'.format(strings,new_line,f.read())
        f.close()
    
    ksort_a=ksort(string=strings,field_symbol=args.symbol,field_id=args.id,reverse=args.reverse,print_field=args.printid,new_line=new_line,num=args.num)
    if not type(ksort_a) is bool:
        for ii in ksort_a:
            print(ii)

