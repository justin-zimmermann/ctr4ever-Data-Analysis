#!/usr/bin/env python
# -*- coding: latin-1 -*-
import os
import re
import pandas
import cairo


#store crash cove course records, write original top 10 in may 2009
record = {'174': ['2009-01-12', '1', "1'18''48"],
          '493': ['2008-12-10', '1', "1'18''74"],
          '488': ['2009-01-20', '1', "1'18''75"],
          '345': ['2009-04-15', '1', "1'18''76"],
          '3': ['2008-12-19', '1', "1'18''81"],
          '482': ['2009-03-03', '1', "1'18''89"],
          '28': ['2008-05-14', '1', "1'18''91"],
          '513': ['2009-02-19', '1', "1'18''92"],
          '111': ['2008-11-30', '1', "1'18''93"],
          '5': ['2009-03-16', '1', "1'18''95"]}


#open player info
player = pandas.read_csv('../data/player.csv', index_col=0)

#regex string to search for crash cove records
#cc_re = "[1-9]{1,3}.[1-9]{1,3}.[1-9]{1,3}.[1-9]{1,3} [1-9]^4-[1-9]^2-[1-9]^2 [1-9]^2 [1-9]*[']*[1-9]+''[1-9]^2"

#iterate over all days of all years 2009-2018:
#TODO: do more tracks, build frames with cairo

banned_list = ['485', '492', '518', '613', '855']

for year in range(2009, 2019):
    print(year)
    for month in range(1, 13):
        for day in range(1, 32):
            files = []
            for f in os.listdir('../data/log_records/%s' % year):
                with open('../data/log_records/%s/%s' % (year, f), 'r', encoding="latin-1") as file:
                    for line in file:
                        if re.search("%s-0*%s-0*%s" % (year, month, day), line):
                            for i, segment in enumerate(line.split()):
                                if segment == "1" and f[:-4] not in banned_list:
                                    record[f[:-4]] = line.split()[i-1:i+2]
            with open('output/%s.%s.%s.txt' % (year, month, day), 'w') as out:
                key_list = record.keys()
                sorted_key = sorted(key_list, key=lambda k: record[k][2].replace('\'', ''))
                sorted_name = dict()
                for i, key in enumerate(sorted_key):
                    if int(key) in player.index:
                        sorted_name[i] = player['Player_Name'][int(key)]
                    else:
                        sorted_name[i] = '--banned--'
                for i in range(10):
                    out.write("%s %s %s\n" % (sorted_name[i], sorted_key[i], record[sorted_key[i]]))

