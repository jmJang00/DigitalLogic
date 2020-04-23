from itertools import combinations

notation_table = {}

def binary_string_formatting(n, num):
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
        binary_string = binary_string_formatting(n, i)
        dic[cnt].append(binary_string)
        notation_table[binary_string] = (i, )
    return dic

def merge_implicants(dic):
    new_dic = {}
    for cycle, i in enumerate(dic):
        if cycle == len(dic) - 1:
            break
        for j in range(len(dic[i])):
            for k in range(len(dic[i+1])):
                possible_merge, binary_string = can_merge(dic[i][j], dic[i+1][k])
                if possible_merge:
                    if not i in new_dic:
                        new_dic[i] = set()
                    new_dic[i].add(binary_string)
                    notation_table[binary_string] = notation_table[dic[i][j]] + notation_table[dic[i+1][k]]
        if i in new_dic:
            new_dic[i] = list(new_dic[i])
    return new_dic

def can_merge(bstr1, bstr2):
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

        if possible_case:
            break

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

def notation_to_formula(notation):
    notation_to_formula.alphabet_alignment = "abcdefghijklmnopqrstuvwxyz"
    formula_element = []
    for minterm in notation:
        replacement = ""
        for iter, literal in enumerate(minterm):
            if literal == "-":
                continue
            replacement += notation_to_formula.alphabet_alignment[iter]
            if literal == "0":
                replacement += "'"
        formula_element.append(replacement)
    return " + ".join(formula_element)

def quine_mccloskey(n, implicant_li, dont_care_li):
    operating_li = []
    operating_li.extend(implicant_li)
    operating_li.extend(dont_care_li)
    operating_li.sort()
    list_of_count_dic = []
    list_of_count_dic.append(make_count_dic(n, operating_li))
    i = 0
    while True:
        dic = merge_implicants(list_of_count_dic[i])
        if len(dic) == 0:
            break
        list_of_count_dic.append(dic)
        i += 1
        output_code_set = ()
        list_of_count_dic.append({})
        for ones_num in list_of_count_dic[i]:
            for bstr in list_of_count_dic[i][ones_num]:
                output_code_set += notation_table[bstr]
        output_code_set = set(output_code_set)
        for ones_num in list_of_count_dic[i-1]:
            for bstr in list_of_count_dic[i-1][ones_num]:
                is_in_output = False
                for num in notation_table[bstr]:
                    if not num in output_code_set:
                        is_in_output = True
                        break
                if is_in_output:
                    if not ones_num in list_of_count_dic[i+1]:
                        list_of_count_dic[i+1][ones_num] = []
                    list_of_count_dic[i+1][ones_num].append(bstr)
        list_of_count_dic[i-1], list_of_count_dic[i+1] = list_of_count_dic[i+1], list_of_count_dic[i-1]
        del list_of_count_dic[i+1]
    while True:
        if not {} in list_of_count_dic:
            break
        list_of_count_dic.remove({})

    pi_li = []
    for i in range(len(list_of_count_dic)):
        pi_li.append([])
        for j in list_of_count_dic[i]:
            pi_li[i].extend(list_of_count_dic[i][j])

    input_li = make_numberset_list(pi_li, implicant_li)
    difference_of_sets(input_li)

    for i in range(len(input_li)):
        column_dominace_optimization(input_li[i], pi_li[i])
        row_dominace_optimization(input_li[i], pi_li[i])

    result = make_possible_cases(input_li, pi_li)

    return result

if __name__ == "__main__":
    # li1 = [0, 2, 5, 6, 7, 8, 9, 13]
    li1 = list(map(int, input("m: ").split(' ')))
    # li2 = [1, 12, 15]
    li2 = list(map(int, input("don't care: ").split(' ')))
    # n = 4
    n = int(input("n: "))
    print("result: ", end='')
    if li2[0] == "-1":
        li2.clear()
    result = quine_mccloskey(n, li1, li2)
    print(result)
    for i in result:
        print(notation_to_formula(i))