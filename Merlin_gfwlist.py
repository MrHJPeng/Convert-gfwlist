#!/usr/bin/env python  
#coding=utf-8
#  
# Generate a list of dnsmasq rules with ipset for gfwlist
#  
# Copyright (C) 2014 http://www.shuyz.com   
# Ref https://github.com/gfwlist/gfwlist   
# Gfwlist before decode https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt
# BASE64 decode website: http://www.bejson.com/enc/base64/
# Creat a file named "gfwlisttmp" with decoded gfwlist before running this script

import urllib.request
import re
import os
import datetime
import base64
import shutil

mydnsip = '127.0.0.1'
mydnsport = '7913'
ipsetname = 'gfwlist'
# Extra Domain;
EX_DOMAIN=[ \
'.google.com', \
'.google.com.hk', \
'.google.com.tw', \
'.google.com.sg', \
'.google.co.jp', \
'.blogspot.com', \
'.blogspot.sg', \
'.blogspot.hk', \
'.blogspot.jp', \
'.gvt1.com', \
'.gvt2.com', \
'.gvt3.com', \
'.1e100.net', \
'.blogspot.tw', \
'.whatismyip.com', \
'.twitch.tv', \
'.digitalocean.com', \
'.namecheap.com' \
]
# 上面添加gfwlist外还想要强制走代理的域名

# the url of gfwlist
baseurl = 'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt'
# match comments/title/whitelist/ip address
comment_pattern = '^\!|\[|^@@|^\d+\.\d+\.\d+\.\d+'
domain_pattern = '([\w\-\_]+\.[\w\.\-\_]+)[\/\*]*' 
homedir =os.path.dirname(__file__).replace('\\','/')
tmpfile = homedir + '/gfwlisttmp'
# do not write to router internal flash directly
outfile = homedir + '/gfwlist.conf'
# 此处为生成路径
#outfile = './dnsmasq_list.conf'
fs =  open(outfile, 'w')
# # fs.write('# gfw list ipset rules for dnsmasq\n')
# # fs.write('# updated on ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')
# # fs.write('#\n')

# print ('fetching list...')
# content = urllib.request.urlopen(baseurl, timeout=15).read().decode('base64')

# # write the decoded content to file then read line by line
# tfs = open(tmpfile, 'w')
# tfs.write(content)
# tfs.close()
tfs = open(tmpfile, 'r')

print ('page content fetched, analysis...')

# remember all blocked domains, in case of duplicate records
domainlist = []


for line in tfs.readlines():        
        if re.findall(comment_pattern, line):
                print ('this is a comment line: ' + line)
                #fs.write('#' + line)
        else:
                domain = re.findall(domain_pattern, line)
                if domain:
                        try:
                                found = domainlist.index(domain[0])
                                print (domain[0] + ' exists.')
                        except ValueError:
                                print ('saving ' + domain[0])
                                domainlist.append(domain[0])
                                fs.write('server=/.%s/%s#%s\n'%(domain[0],mydnsip,mydnsport))
                                fs.write('ipset=/.%s/%s\n'%(domain[0],ipsetname))
                else:
                        print ('no valid domain in this line: ' + line)
                                        
tfs.close()        

for each in EX_DOMAIN:
        fs.write('server=/%s/%s#%s\n'%(each,mydnsip,mydnsport))
        fs.write('ipset=/%s/%s\n'%(each,ipsetname))

print ('write extra domain done')

fs.close();

print ('done!')