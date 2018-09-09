"""
Description     : Simple Python implementation of the Apriori Algorithm

Usage:
    $python apriori.py -f DATASET.csv -s minSupport  -c minConfidence

    $python apriori.py -f DATASET.csv -s 0.15 -c 0.6
"""

import sys
import csv
from itertools import chain, combinations
from collections import defaultdict
from optparse import OptionParser


def subsets(arr):
    """ Returns non empty subsets of arr"""
    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])


def returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet):
        """calculates the support for items in the itemSet and returns a subset
       of the itemSet each of whose elements satisfies the minimum support"""
        _itemSet = set()
        localSet = defaultdict(int)

        for item in itemSet:
                for transaction in transactionList:
                        if item.issubset(transaction):
                                freqSet[item] += 1
                                localSet[item] += 1

        for item, count in list(localSet.items()):
                support = float(count)/len(transactionList)

                if support >= minSupport:
                        _itemSet.add(item)

        return _itemSet


def joinSet(itemSet, length):
        """Join a set with itself and returns the n-element itemsets"""
        return set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length])


def getItemSetTransactionList(data_iterator):
    transactionList = list()
    itemSet = set()
    for record in data_iterator:
        transaction = frozenset(record)
        transactionList.append(transaction)
        for item in transaction:
            itemSet.add(frozenset([item]))              # Generate 1-itemSets
    return itemSet, transactionList


def runApriori(data_iter, minSupport, minConfidence):
    """
    run the apriori algorithm. data_iter is a record iterator
    Return both:
     - items (tuple, support)
     - rules ((pretuple, posttuple), confidence)
    """
    itemSet, transactionList = getItemSetTransactionList(data_iter)

    freqSet = defaultdict(int)
    largeSet = dict()
    # Global dictionary which stores (key=n-itemSets,value=support)
    # which satisfy minSupport

    assocRules = dict()
    # Dictionary which stores Association Rules

    oneCSet = returnItemsWithMinSupport(itemSet,
                                        transactionList,
                                        minSupport,
                                        freqSet)

    currentLSet = oneCSet
    k = 2
    while(currentLSet != set([])):
        largeSet[k-1] = currentLSet
        currentLSet = joinSet(currentLSet, k)
        currentCSet = returnItemsWithMinSupport(currentLSet,
                                                transactionList,
                                                minSupport,
                                                freqSet)
        currentLSet = currentCSet
        k = k + 1

    def getSupport(item):
            """local function which Returns the support of an item"""
            return float(freqSet[item])/len(transactionList)

    toRetItems = []
    for key, value in list(largeSet.items()):
        toRetItems.extend([(tuple(item), getSupport(item))
                           for item in value])

    toRetRules = []
    for key, value in list(largeSet.items())[1:]:
        for item in value:
            _subsets = list(map(frozenset, [x for x in subsets(item)]))
            for element in _subsets:
                remain = item.difference(element)
                if len(remain) > 0:
                    confidence = getSupport(item)/getSupport(element)
                    if confidence >= minConfidence:
                        toRetRules.append(((tuple(element), tuple(remain)),
                                           confidence))
    return toRetItems, toRetRules


def printResults(items, rules):
    """prints the generated itemsets sorted by support and the confidence rules sorted by confidence"""

    for item, support in sorted(items, key=lambda item_support: item_support[1]):
        print("item: %s , %.3f" % (str(item), support))

		
		
    print("\n------------------------ RULES:")

    for rule, confidence in sorted(rules, key=lambda rule_confidence: rule_confidence[1]):
        pre, post = rule
        print("Rule: %s ==> %s , %.3f" % (str(pre), str(post), confidence))
		
	

	

def dataFromFile(fname):
        """Function which reads from the file and yields a generator"""
        file_iter = open(fname, 'rU')
        for line in file_iter:
                line = line.strip().rstrip(',')                         # Remove trailing comma
                record = frozenset(line.split(','))
                yield record

				


if __name__ == "__main__":

    optparser = OptionParser()
    optparser.add_option('-f', '--inputFile',
                         dest='input',
                         help='filename containing csv',
                         default=None)
    optparser.add_option('-s', '--minSupport',
                         dest='minS',
                         help='minimum support value',
                         default=0.15,
                         type='float')
    optparser.add_option('-c', '--minConfidence',
                         dest='minC',
                         help='minimum confidence value',
                         default=0.6,
                         type='float')

    (options, args) = optparser.parse_args()

    inFile = None
    if options.input is None:
            inFile = sys.stdin
    elif options.input is not None:
            inFile = dataFromFile(options.input)
    else:
            print('No dataset filename specified, system with exit\n')
            sys.exit('System will exit')

    minSupport = options.minS
    minConfidence = options.minC
	

	
    items, rules = runApriori(inFile, minSupport, minConfidence)

    printResults(items, rules)

import pandas as pd
from pandas import ExcelWriter



'''Add by eric 2017/10/03'''
output_list = []
support_num = []
support_df = pd.DataFrame()
for item, support in sorted(items, key=lambda item_support: item_support[1]):
	item = str(item)
	support_num.append(support)
	output_list.append(item)		

support_df['item'] = output_list
support_df['support'] = support_num


confid_df = pd.DataFrame()
pre_list = []
post_list = []
confid_list = []
for rule, confidence in sorted(rules, key=lambda rule_confidence: rule_confidence[1]):
    pre, post = rule
    pre_list.append(str(pre))
    post_list.append(str(post))
    confid_list.append(confidence)

confid_df['pre_item'] = pre_list
confid_df['post_item'] = post_list
confid_df['confidence'] = confid_list



writer = pd.ExcelWriter('support.xlsx', engine='xlsxwriter')
support_df.to_excel(writer, sheet_name='Sheet1')
writer.save()

writer = pd.ExcelWriter('confidence.xlsx', engine='xlsxwriter')
confid_df.to_excel(writer, sheet_name='Sheet1')
writer.save()

#print("item: %s , %.3f" % (str(item), support))

'''

'''



'''
with open('support_result.csv','w',newline='') as f:
	s=csv.writer(f,delimiter=' ',lineterminator='\n')
	
	for item, support in sorted(items, key=lambda item_support: item_support[1]):
		support_item = str(item)+','+ str(support)
		s.writerow(support_item)

		
with open('confident_result.csv','w',newline='') as f1:
	s=csv.writer(f1,delimiter=' ',lineterminator='\n')
	
	for rule, confidence in sorted(rules, key=lambda rule_confidence: rule_confidence[1]):
		pre, post = rule
		confidence_item = (str(pre)+ ',' + str(post) +','+  str(confidence)
		s.writerow(confidence_item)
'''	