import csv
import itertools

min_support = float(input("Enter the minimum support value: "))
min_confidence = float(input("Enter the minimim confidence value: "))

def join_step(dict1, k):
    return_list = []
    keys = list(dict1.keys())
    
    for key in range(len(keys) - 1):
        slice_list = keys[key+1:]
        #print(keys)
        #print(slice_list)
        for x in range(len(slice_list)):
            join_list = []
            join_list.append(keys[key])
            join_list.append(slice_list[x])
            return_list.append(join_list)
        
    return return_list
                


def read_file(file):
    file_list = []
    with open(file, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            file_list.append(row)
    return file_list

def support_calc(min_support, freq_dict, transacton_num):
    support_dict = {}
    for item, freq_num in freq_dict.items():
        support_val = freq_num / transacton_num
        if support_val >= min_support:
            print("item being added {}".format(item))
            support_dict[item] = support_val
    return support_dict

def confidence_calc(min_confidence, combination_support_dict):
    association_dict = {}
    for item_set, support_val in combination_support_dict.items():
        if isinstance(item_set,str):
            continue
        list_item = list(item_set)
        
        #print("Association rules {}".format(association_rule))
        item_set_size = len(item_set)
        if len(item_set) == 2:
            support_left_val = combination_support_dict[item_set[0]]
            conf = round(support_val / support_left_val,2)
            print("conf val: {}".format(conf))
            association = str(item_set[0]) + "=>" + str(item_set[1])
            if conf >= min_confidence:
                association_dict[association] = [support_val, conf]
        else:
            while item_set_size-1 > 1:
                association_rule = list(itertools.combinations(list_item, item_set_size-1))
                print("association rule: {}".format(association_rule))
                for x in association_rule:
                    left_side = set(x)
                    right_side = set(item_set) - set(x)
                    
                    print("left itemset side: {}".format(left_side))
                    print("right itemset side: {}".format(right_side))
                    conf = round(support_val / combination_support_dict[x],2)
                    if conf >= min_confidence:
                        association = str(left_side) + "=>" + str(right_side)
                        association_dict[association] = [support_val, conf]
                item_set_size -= 1
        """
        if len(association_rule) > 2:
            for assoc in association_rule:
                support_left_val = combination_support_dict[assoc]
                conf = support_val / support_left_val
                print("conf val: {}".format(conf))
                if conf >= min_confidence:
                    confidence_dict[assoc] = conf
        else:
            support_left_val = combination_support_dict[item_set[0]]
            conf = support_val / support_left_val
            print("conf val: {}".format(conf))
            if conf >= min_confidence:
                confidence_dict[]
        """
    return association_dict



def apriori_alg(min_support, min_confidence, file_values):
    freq_dict = {}
    transacton_num = 0
    for row in file_values:
        transacton_num += 1
        for item in row:
            if item in freq_dict.keys():
                val = freq_dict[item]
                freq_dict[item] = val + 1
            else:
                freq_dict[item] = 1
    #print(freq_dict)

    # We need to get support value after we have added up the number of same items
    sup_dic_l1 = support_calc(min_support, freq_dict, transacton_num)
    item_sets = []
    item_sets.append(list(sup_dic_l1.keys()))
    #print(sup_dic_l1)
    comb_itemset_dic = {}
    comb_itemset_dic.update(sup_dic_l1)
    # Since range is n-1 we need to do 21 to run for 20 transactions
    for i in range(2,21):
        # Need to do the join step
        keys = list(sup_dic_l1.keys())
        keys = list(itertools.combinations(keys, i))
        item_sets.append(keys)

        if keys == []:
            continue
        freq_dict_c2 = {}
        for row in file_values:
            for item_set in keys:
                check = all(item in row for item in item_set)
                if check is True:
                    #print("Item set: {}".format(item_set))
                    #print("row: {}".format(row))
                    #print("yes")
                    if tuple(item_set) in freq_dict_c2.keys():
                        val = freq_dict_c2[tuple(item_set)]
                        freq_dict_c2[tuple(item_set)] = val + 1
                    else:
                        freq_dict_c2[tuple(item_set)] = 1
        #print(freq_dict_c2)
        sup_dic_l = support_calc(min_support, freq_dict_c2, transacton_num)
        if not sup_dic_l:
            continue
        print("support dict: {}".format(sup_dic_l))
        comb_itemset_dic.update(sup_dic_l)
        #sup_dic_l2
        #print(item_sets)
    print(comb_itemset_dic)
    conf_dict = confidence_calc(min_confidence, comb_itemset_dic)
    print(conf_dict)
                

def brute_force(min_support, min_confidence, file_values):
    single_item_transactions = {}
    transaction_num = 0
    for row in file_values:
        transaction_num += 1
        for item in row:
            if item in single_item_transactions.keys():
                val = single_item_transactions[item]
                single_item_transactions[item] = val + 1
            else:
                single_item_transactions[item] = 1
    
    single_item_keys = single_item_transactions.keys()
    double_item_set = list(itertools.combinations(single_item_keys,2))
    #print(single_item_keys)
    #print(double_item_set)

    single_item_support = support_calc(min_support, single_item_transactions, transaction_num)
    print(single_item_support)

    double_item_freq = {}
    for item_set in double_item_set:
        for row in file_values:
            key_list = double_item_freq.keys()
            if set(item_set).issubset(row):
                if item_set in key_list:
                    val = double_item_freq[item_set]
                    double_item_freq[item_set] = val + 1
                else:
                    double_item_freq[item_set] = 1
    #print(double_item_freq)
    double_item_support = support_calc(min_support, double_item_freq, transaction_num)
    print(double_item_support)


file_read = read_file('db1.txt')
#print(file_read)
#apriori_alg(min_support, min_confidence, file_read)
brute_force(min_support, min_confidence, file_read)