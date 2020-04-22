from itertools import combinations

notation_table = {}

def to_binary_string(n, num):
    ret_str = bin(num)[2:]
    num_len = len(ret_str)
    if num_len < n:
        ret_str = "0" * (n - num_len) + ret_str
    return ret_str

def make_count_dic(n, li):
    dic = {}
    for i in li:
        cnt = 0
        tmp = i
        while tmp > 0:
            if tmp % 2 == 1:
                cnt += 1
            tmp //= 2
        if not cnt in dic:
            dic[cnt] = []
        binary_string = to_binary_string(n, i)
        dic[cnt].append(binary_string)
        notation_table[binary_string] = (i, )
    return dic

def find_primary_implicant(dic):
    new_dic = {}
    for cycle, i in enumerate(dic):
        if cycle == len(dic) - 1:
            break
        for j in range(len(dic[i])):
            for k in range(len(dic[i+1])):
                possible_merge, binary_string = is_implicant(dic[i][j], dic[i+1][k])
                if possible_merge:
                    if not i in new_dic:
                        new_dic[i] = set()
                    new_dic[i].add(binary_string)
                    notation_table[binary_string] = notation_table[dic[i][j]] + notation_table[dic[i+1][k]]
        if i in new_dic:
            new_dic[i] = list(new_dic[i])
    return new_dic

def is_implicant(bstr1, bstr2):
    ret = False
    bstrli = list(bstr1)
    for i in range(len(bstr1)):
        if (bstr1[i] == '-') ^ (bstr2[i] == '-'):
            ret = False
            break
        elif ret == False and bstr1[i] != bstr2[i]:
            ret = True
            bstrli[i] = '-'
        elif ret == True and bstr1[i] != bstr2[i]:
            ret = False
            break
    if not ret:
        bstrli = []
    return ret, "".join(bstrli)

def quine_mccloskey(n, li1, li2):
    li3 = []
    li3.extend(li1)
    li3.extend(li2)
    li3.sort()
    li4 = []
    li4.append(make_count_dic(n, li3))
    i = 0
    while True:
        dic = find_primary_implicant(li4[i])
        if len(dic) == 0:
            break
        li4.append(dic)
        i += 1
        output_code_set = ()
        li4.append({})
        for ones_num in li4[i]:
            for bstr in li4[i][ones_num]:
                output_code_set += notation_table[bstr]
        output_code_set = set(output_code_set)
        for ones_num in li4[i-1]:
            for bstr in li4[i-1][ones_num]:
                is_in_output = False
                for num in notation_table[bstr]:
                    if not num in output_code_set:
                        is_in_output = True
                        break
                if is_in_output:
                    if not ones_num in li4[i+1]:
                        li4[i+1][ones_num] = []
                    li4[i+1][ones_num].append(bstr)
        li4[i-1], li4[i+1] = li4[i+1], li4[i-1]
        del li4[i+1]
    while True:
        if not {} in li4:
            break
        li4.remove({})

    pi_li = []
    for i in range(len(li4)):
        pi_li.append([])
        for j in li4[i]:
            pi_li[i].extend(li4[i][j])

    input_li = make_numberset_list(pi_li, li1)
    difference_of_sets(input_li)

    for i in range(len(input_li)):
        column_dominace_optimization(input_li[i], pi_li[i])
        row_dominace_optimization(input_li[i], pi_li[i])

    result = make_possible_cases(input_li, pi_li)

    return result

def make_possible_cases(input_li, all_pi_li):
    total_pi_li = []
    total_input_set = set()
    possible_case = []
    for i in range(len(all_pi_li)):
        total_pi_li.extend(all_pi_li[i])
        total_input_set |= input_li[i]

    for i in range(1, len(total_pi_li) + 1):
        for pis in combinations(total_pi_li, i):
            containing = set()
            for j in pis:
                containing |= set(notation_table[j])
            if total_input_set == total_input_set & containing:
                possible_case.append(pis)
    return possible_case

def make_numberset_list(li, correct_input_list):
    new_li = []
    filter_set = set(correct_input_list)
    for i in range(len(li)):
        input_set = set()
        for j in range(len(li[i])):
            input_set |= set(notation_table[li[i][j]]) & filter_set
        new_li.append(input_set)
    return new_li

def difference_of_sets(li):
    for i in range(len(li) - 1):
        li[i] = li[i] - li[i+1]

def what_belongs_to(num, pi_li):
    ret = set()
    for pi in pi_li:
        if num in notation_table[pi]:
            ret.add(pi)
    return ret

def row_dominace_optimization(input_set, pi_li):
    remove_set = set()
    for pis in combinations(pi_li, 2):
        num_set0 = set(notation_table[pis[0]]) & input_set
        num_set1 = set(notation_table[pis[1]]) & input_set
        if num_set0 == num_set0 & num_set1:
            remove_set.add(pis[0])
        elif num_set1 == num_set0 & num_set1:
            remove_set.add(pis[1])
    for i in list(remove_set):
        pi_li.remove(i)

def column_dominace_optimization(input_set, pi_li):
    remove_set = set()
    for nums in combinations(list(input_set), 2):
        num_set0 = what_belongs_to(nums[0], pi_li)
        num_set1 = what_belongs_to(nums[1], pi_li)
        if num_set0 == num_set0 & num_set1:
            remove_set.add(nums[1])
        elif num_set1 == num_set0 & num_set1:
            remove_set.add(nums[0])
    for i in list(remove_set):
        input_set.remove(i)

if __name__ == "__main__":
    # li1 = [0, 2, 5, 6, 7, 8, 9, 13]
    li1 = list(map(int, input("m: ").split(' ')))
    # li2 = [1, 12, 15]
    li2 = list(map(int, input("don't care: ").split(' ')))
    # n = 4
    n = int(input("n: "))
    print("result: ")
    print(quine_mccloskey(n, li1, li2))