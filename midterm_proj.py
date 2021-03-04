import csv
import time

min_support = float(input("Enter the minimum support value: "))
min_confidence = float(input("Enter the minimim confidence value: "))

# Replacement for itertools combinations
# Use of recursion
def join_step(keys_list, k):
    # Used as recursion check
    if k == 0:
        return [[]]
    
    return_list = []
    for key_index in range(0, len(keys_list)):
        n = keys_list[key_index]
        remList = keys_list[key_index + 1:]

        for m in join_step(remList, k - 1):
            return_list.append([n] + m)
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
            association = str(item_set[0]) + "=>" + str(item_set[1])
            if conf >= min_confidence:
                association_dict[association] = [support_val, conf]
            support_left_val = combination_support_dict[item_set[1]]
            flipped_rule_conf = round(support_val/support_left_val,2)
            flipped_association = str(item_set[1]) + "=>" + str(item_set[0])
            if flipped_rule_conf >= min_confidence:
                association_dict[flipped_association] = [support_val, flipped_rule_conf]
        else:
            while item_set_size-1 > 1:
                association_rule = join_step(list_item, item_set_size-1)
                for x in association_rule:
                    left_side = set(x)
                    right_side = set(item_set) - set(x)
                    
                    conf = round(support_val / combination_support_dict[tuple(sorted(x))],2)

                    if conf >= min_confidence:
                        association = str(left_side) + "=>" + str(right_side)
                        association_dict[association] = [support_val, conf]
                item_set_size -= 1
    return association_dict



def apriori_alg(min_support, min_confidence, file):
    freq_dict = {}
    transacton_num = 0
    # Get data set initially
    file_values = read_file(file)
    for row in file_values:
        transacton_num += 1
        for item in row:
            if item in freq_dict.keys():
                val = freq_dict[item]
                freq_dict[item] = val + 1
            else:
                freq_dict[item] = 1

    # We need to get support value after we have added up the number of same items
    sup_dic_l1 = support_calc(min_support, freq_dict, transacton_num)
    item_sets = []
    item_sets.append(list(sup_dic_l1.keys()))
    comb_itemset_dic = {}
    comb_itemset_dic.update(sup_dic_l1)
    # Since range is n-1 we need to do 21 to run for 20 transactions
    keys = list(sup_dic_l1.keys())
    
    for i in range(2,21):
        # Need to do the join step
        if keys == []:
            break
        keys_item_set = join_step(keys, i)
        #print("Keys item set {}".format(keys_item_set))
        item_sets.append(keys)

        if keys_item_set == []:
            break
        freq_dict_c2 = {}
        # Scan dataset each time when we try to calculate the support.
        # This is so we don't keep this information in memory.
        file_values = read_file(file)
        for row in file_values:
            for item_set in keys_item_set:
                item_set = tuple(sorted(item_set))
                check = all(item in row for item in item_set)
                if check is True:
                    if tuple(item_set) in freq_dict_c2.keys():
                        val = freq_dict_c2[tuple(item_set)]
                        freq_dict_c2[tuple(item_set)] = val + 1
                    else:
                        freq_dict_c2[tuple(item_set)] = 1
        sup_dic_l = support_calc(min_support, freq_dict_c2, transacton_num)
        if not sup_dic_l:
            keys = []
            continue
        comb_itemset_dic.update(sup_dic_l)        
        list_item_set = list(sup_dic_l.keys())
        keys = []
        for item_set in list_item_set:
            for item in item_set:
                if item not in keys:
                    keys.append(item)
        
    #print(comb_itemset_dic)
    conf_dict = confidence_calc(min_confidence, comb_itemset_dic)
    print(conf_dict)
                

def brute_force(min_support, min_confidence, file):
    k_items_frequent = True
    k = 2
    support_dict = {}
    
    single_item_transactions = {}
    transaction_num = 0
    file_values = read_file(file)
    for row in file_values:
        transaction_num += 1
        for item in row:
            if item in single_item_transactions.keys():
                val = single_item_transactions[item]
                single_item_transactions[item] = val + 1
            else:
                single_item_transactions[item] = 1

    single_item_support = support_calc(min_support, single_item_transactions, transaction_num)

    single_item_keys = list(single_item_transactions.keys())
    support_dict.update(single_item_support)
    while k_items_frequent:
        list_item_set = join_step(single_item_keys, k)
        
        item_freq = {}
        # Scan dataset each time when we try to calculate the support.
        # This is so we don't keep this information in memory.
        # As said in the frequently asked questions section
        file_values = read_file(file)
        for item_set in list_item_set:
            item_set = tuple(sorted(item_set))
            for row in file_values:
                key_list = item_freq.keys()
                if set(item_set).issubset(row):
                    if item_set in key_list:
                        val = item_freq[item_set]
                        item_freq[item_set] = val + 1
                    else:
                        item_freq[item_set] = 1
        #print(double_item_freq)
        item_support = support_calc(min_support, item_freq, transaction_num)
        
        support_dict.update(item_support)
        if not item_support:
            break

        k += 1
    conf_dict = confidence_calc(min_confidence, support_dict)
    print(conf_dict)

'''
# Database 1
print("Running Database 1")
db1_start_apriori_time = time.time()
apriori_alg(min_support, min_confidence, 'db1.txt')
db1_time_apriori_alg = time.time() - db1_start_apriori_time
print("Apriori Algorithm Runtime: {}".format(db1_time_apriori_alg))
db1_start_brute_time = time.time()
brute_force(min_support, min_confidence, 'db1.txt')
db1_time_brute_alg = time.time() - db1_start_brute_time
print("Brute Force Runtime: {}".format(db1_time_brute_alg))


# Database 2
print("Running Database 2")
db2_start_apriori_time = time.time()
apriori_alg(min_support, min_confidence, 'db2.txt')
db2_time_apriori_alg = time.time() - db2_start_apriori_time
print("Apriori Algorithm Runtime: {}".format(db2_time_apriori_alg))
db2_start_brute_time = time.time()
brute_force(min_support, min_confidence, 'db2.txt')
db2_time_brute_alg = time.time() - db2_start_brute_time
print("Brute Force Runtime: {}".format(db2_time_brute_alg))


# Database 3
print("Running Database 3")
db3_start_apriori_time = time.time()
apriori_alg(min_support, min_confidence, 'db3.txt')
db3_time_apriori_alg = time.time() - db3_start_apriori_time
print("Apriori Algorithm Runtime: {}".format(db3_time_apriori_alg))
db3_start_brute_time = time.time()
brute_force(min_support, min_confidence, 'db3.txt')
db3_time_brute_alg = time.time() - db3_start_brute_time
print("Brute Force Runtime: {}".format(db3_time_brute_alg))

# Database 4
print("Running Database 4")
db4_start_apriori_time = time.time()
apriori_alg(min_support, min_confidence, 'db4.txt')
db4_time_apriori_alg = time.time() - db4_start_apriori_time
print("Apriori Algorithm Runtime: {}".format(db4_time_apriori_alg))
db4_start_brute_time = time.time()
brute_force(min_support, min_confidence, 'db4.txt')
db4_time_brute_alg = time.time() - db4_start_brute_time
print("Brute Force Runtime: {}".format(db4_time_brute_alg))
'''
# Database 5
print("Running Database 5")
db5_start_apriori_time = time.time()
apriori_alg(min_support, min_confidence, 'db5.txt')
db5_time_apriori_alg = time.time() - db5_start_apriori_time
print("Apriori Algorithm Runtime: {}".format(db5_time_apriori_alg))
db5_start_brute_time = time.time()
brute_force(min_support, min_confidence, 'db5.txt')
db5_time_brute_alg = time.time() - db5_start_brute_time
print("Brute Force Runtime: {}".format(db5_time_brute_alg))
