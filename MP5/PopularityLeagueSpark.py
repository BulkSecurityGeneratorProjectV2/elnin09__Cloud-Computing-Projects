#!/usr/bin/env python

#Execution Command: spark-submit PopularityLeagueSpark.py dataset/links/ dataset/league.txt
import sys
from pyspark import SparkConf, SparkContext
import re

conf = SparkConf().setMaster("local").setAppName("PopularityLeague")
conf.set("spark.driver.bindAddress", "127.0.0.1")
sc = SparkContext(conf = conf)

lines = sc.textFile(sys.argv[1], 1) 

#TODO

leagueIds = sc.textFile(sys.argv[2], 1)

words = re.split("\\n|\\s",leagueIds)

#TODO

output = open(sys.argv[3], "w")

sys.stdout = output

def mapperfunction(line):
    retval=list()
    key,value = (line.rstrip('\n')).split(':',1);
    values = re.split(" ",value.lstrip(' '));
    for i in values:
        retval.append((i,key.rstrip('\n')))
    return retval

def mapfunction(x):
    if(x is None):
        return
    
    #print(x)
    key,value = x
    retval = list()
    retval.append((key,1))
    retval.append((value,0))
    return retval

def reducehelper(x):
    retval = list()
    if(int(x[1]) == 0):
        retval.append(x[0])
    return retval 



wcflatmap = lines.flatMap(lambda x:mapperfunction(x))
#print(wcflatmap.take(10))
wc = wcflatmap.flatMap(lambda x: mapfunction(x));
#print(wc.take(30))
wcreduce = wc.reduceByKey(lambda a, b: a + b)
#print(wcreduce.take(30))
#wcreduce = wcreduce.flatMap(lambda x: reducehelper(x));
#print(wcreduce.take(30))


valuesorted = wcreduce.sortBy(lambda a: -a[1])
valuesorted = valuesorted.take(10)



finallist = valuesorted.sort(key = lambda x: x[0])
for i in valuesorted:
    print('%s\t%s' % (i[0], i[1]) )


#TODO
#write results to output file. Foramt for each line: (key + \t + value +"\n")

sc.stop()

