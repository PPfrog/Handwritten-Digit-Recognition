import time
import random
"""
CSC1002
Use the following functions to implement kNN models
"""
def dot(v, w):
    """v_1 * w_1 + ... + v_n * w_n"""
    return sum(v_i * w_i for v_i, w_i in zip(v, w))

def input_data(p_file_name):
    l_vector = list()
    l_vector_dict = dict()
    with open(p_file_name, 'r') as l_file:
        l_file_list = list()
        for item in l_file:
            item = item.strip('\n')
            l_file_list.append(item)
    for line in l_file_list:
        if len(line) == 2:
            if l_vector_dict.get(line[1])  is None:
                l_vector_dict[line[1]] = list()
            l_vector_dict[line[1]].append(l_vector)
            l_vector = list()
        else:
            for i in line:
                if i != ' ':
                    l_vector.append(int(i))
    return l_vector_dict

def output_result(training_result_dict,testing_result_dict):
    l_total_sample = 0
    l_total_correct = 0
    l_total_test = 0
    print('-' * 40)
    print('Training Info'.center(40))
    print('-' * 40)
    for i in range(10):#1!!!
        print((str(i)+' =' + training_result_dict[str(i)].rjust(4)).center(40))
        l_total_sample += int(training_result_dict[str(i)])
    print('-'*40)
    print(('Total Sample = %d' % l_total_sample).center(40))
    print('-'*40)
    print('-'*40)
    print('Testing Info'.center(40))
    print('-'*40)
    for i in range(10):#!!!!
        print((str(i) + ' ='+ testing_result_dict[str(i)][0].rjust(4)\
                      + ',' + testing_result_dict[str(i)][1].rjust(4)\
                      + ',' + testing_result_dict[str(i)][2].rjust(4)).center(40))
        l_total_correct += int(testing_result_dict[str(i)][0])
        l_total_test += int(testing_result_dict[str(i)][0])+\
                        int(testing_result_dict[str(i)][1])
    l_correct_rate = l_total_correct/l_total_test
    print('-'*40)
    print(('Accuracy = %.2f%%' % (l_correct_rate * 100)).center(40))
    print(('Correct/Total = %d/%d' % (l_total_correct, l_total_test)).center(40))
    print('-'*40)
    print('End of Training @', \
    time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))


def model_1():
    print('Beginning of Training @', \
    time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    training_result_dict = {}
    testing_result_dict = {}
    training_vector_dict = input_data('digit-training.txt')
    testing_vector_dict = input_data('digit-testing.txt')
    for n_test in '0123456789':
        for v_test in testing_vector_dict[n_test]:
            comparing_dict = {}
            comparing_list = []
            for n_train in '0123456789':
                mid_list = []
                for v_train in training_vector_dict[n_train]:
                    mid_list.append(dot(v_test, v_train))
                comparing_dict[n_train] = max(mid_list)
            for key, val in comparing_dict.items():
                comparing_list.append((val, key))
            comparing_list.sort(reverse=True)
            if comparing_list[0][1] == n_test:
                if testing_result_dict.get(n_test) is None:
                    testing_result_dict[n_test] = [1, 0, '0%']
                else:
                    testing_result_dict[n_test][0] += 1
            else:
                if testing_result_dict.get(n_test) is None:
                    testing_result_dict[n_test] = [0, 1, '0%']
                else:
                    testing_result_dict[n_test][1] += 1

    for num in '0123456789':
        training_result_dict[num] = training_result_dict.get(num, 0) + \
                                    len(training_vector_dict[num])
        training_result_dict[num] = str(training_result_dict[num])
        for res_list in testing_result_dict.values():
            res_list[2] = str(int(res_list[0]/(res_list[1]+res_list[0])*100))+'%'
    for item in testing_result_dict.values():
        for i in range(2):
            item[i] = str(item[i])
    output_result(training_result_dict, testing_result_dict)

def predict_1():    
    training_vector_dict = input_data('digit-training.txt')
    predict_vector_list = []
    predict_result_list = []
    predict_vector_dict = input_data('digit-predict.txt')
    for i in predict_vector_dict['0']:
        predict_vector_list.append(i)
    for vec in predict_vector_list:
        comparing_list = []
        comparing_dict = {}
        for n_train in '0123456789':
            mid_list = []
            for v_train in training_vector_dict[n_train]:
                mid_list.append(dot(vec, v_train))
            comparing_dict[n_train] = max(mid_list)
        for key, val in comparing_dict.items():
            comparing_list.append((val, key))
        comparing_list.sort(reverse=True)
        predict_result_list.append(comparing_list[0][1])
    for i in predict_result_list:
        print(i)


def model_2():
    print('Beginning of Training @', \
    time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    training_result_dict = {}
    testing_result_dict = {}
    training_vector_dict = input_data('digit-training.txt')
    testing_vector_dict = input_data('digit-testing.txt')    
    for n_test in '0123456789':
        for v_test in testing_vector_dict[n_test]:
            comparing_dict = {}
            comparing_weighted_dict = {}
            comparing_list = []
            for n_train in '0123456789':
                index_list = []
                for i in range(10):
                    index_list.append(random.randint(0, len(training_vector_dict[n_train])-1))
                mid_list = []
                for index in index_list:
                    mid_list.append(dot(v_test, training_vector_dict[n_train][index]))
                comparing_dict[n_train] = mid_list
            dot_sum = 0
            for key, val in comparing_dict.items():
                for i in val:
                    dot_sum += i
            for key, val in comparing_dict.items():
                for i in val:
                    comparing_weighted_dict[key] = comparing_weighted_dict.get(key, 0) + i
            for key, val in comparing_dict.items():
                for i in val:
                    comparing_weighted_dict[key] = comparing_weighted_dict[key]/dot_sum
            for key, val in comparing_weighted_dict.items():
                comparing_list.append((val, key))

            comparing_list.sort(reverse=True)
            if comparing_list[0][1] == n_test:
                if testing_result_dict.get(n_test) is None:
                    testing_result_dict[n_test] = [1, 0, '0%']
                else:
                    testing_result_dict[n_test][0] += 1
            else:
                if testing_result_dict.get(n_test) is None:
                    testing_result_dict[n_test] = [0, 1, '0%']
                else:
                    testing_result_dict[n_test][1] += 1

    for num in '0123456789':
        training_result_dict[num] = training_result_dict.get(num, 0) + \
                                    len(training_vector_dict[num])
        training_result_dict[num] = str(training_result_dict[num])
        for res_list in testing_result_dict.values():
            res_list[2] = str(int(res_list[0]/(res_list[1]+res_list[0])*100))+'%'
    for item in testing_result_dict.values():
        for i in range(2):
            item[i] = str(item[i])
    output_result(training_result_dict, testing_result_dict)
def predict_2():
    training_vector_dict = input_data('digit-training.txt')
    predict_vector_list = []
    predict_result_list = []
    predict_vector_dict = input_data('digit-predict.txt')
    for i in predict_vector_dict['0']:
        predict_vector_list.append(i)
    for vec in predict_vector_list:
        comparing_list = []
        comparing_dict = {}
        comparing_weighted_dict = {}
        for n_train in '0123456789':
            index_list = []
            for i in range(10):
                index_list.append(random.randint(0, len(training_vector_dict[n_train])-1))
            mid_list = []
            for index in index_list:
                mid_list.append(dot(vec, training_vector_dict[n_train][index]))
            comparing_dict[n_train] = mid_list
        dot_sum = 0
        for key, val in comparing_dict.items():
            for i in val:
                dot_sum += i
        for key, val in comparing_dict.items():
            for i in val:
                comparing_weighted_dict[key] = comparing_weighted_dict.get(key, 0) + i
        for key, val in comparing_dict.items():
            for i in val:
                comparing_weighted_dict[key] = comparing_weighted_dict[key]/dot_sum
        for key, val in comparing_weighted_dict.items():
            comparing_list.append((val, key))
        comparing_list.sort(reverse=True)
        predict_result_list.append(comparing_list[0][1])
    for i in predict_result_list:
        print(i)
def main():
    model_1()
    predict_1()
    model_2()
    predict_2()
main()
