#!/bin/python
# Kage Park 
# Convert JSON data to SHELL format
import json
import ast
import sys
import copy

def extract_dict(val,k=None):
    rc=[]
    if type(val) is dict:
        for ek in val.keys():
           if k is None:
               nk=ek
           else:
               nk='{0}/{1}'.format(k,ek)
           if type(val[ek]) is dict:
               nrc=extract_dict(val[ek],nk)
               for i in nrc:
                   rc.append(i)
           else:
               rc.append('''{0}="{1}"'''.format(nk,val[ek]))
    else:
        pass
    return rc

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('{0} v{1}'.format(sys.argv[0],'0.1'))
        print('Convert JSON data to SHELL Format or get data for finding key name in JSON data')
        print('')
        print('{0} [<key field>|None|""] <json>'.format(sys.argv[0]))
        print('')
        print("example)")
        print(" <json> is {A:{B:{C:D,E:F}}}")
        print(" Get C value")
        print("   <key field> is A/B/C")
        print(" Get E value")
        print("   <key field> is A/B/E")
        print(" Whole data")
        print("   <key field> is None or ''")
        sys.exit()

    key=sys.argv[1]
    if key == 'None' or key == 'none' or key == 'NONE':
        key_a=[]
    else:
        key_a=key.split('/')
    json_str=''
    for i in sys.argv[2:]:
        if json_str == '':
            json_str='''{0}'''.format(i)
        else:
            json_str='''{0}{1}'''.format(json_str,i)

    try:
        info=ast.literal_eval(json_str)
    except:
        print('not JSON format')
        sys.exit()

    if len(key_a) == 0:
        for i in extract_dict(info):
            print(i)
    else:
        for k in key_a:
            if k in info:
                info=info[k]
            else:
                print('key({0}) not found'.format(k))
                sys.exit()
        print(info) 
