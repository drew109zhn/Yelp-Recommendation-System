import psycopg2
from collections import Counter
import macros as m
# get_user_id_command is psql command used to get users id that have more than 1000 reivew on yelp
item_based_command = "Select user_id, bus_id, stars \
                      from reviews;"

try:
    conn = psycopg2.connect("dbname=yelp user=vagrant")
except:
    print "Could not connect to the database yelp"
cur = conn.cursor()

def get_item_based_input_all():
    """
    :return: item-based algorithm only requires inidividual_id, businesses_id, ratings
    to proceed. Therefore, this function will only need to get all informations for reviews
    table to proceeed. Everything will be written into macros.item_based_fname
    """
    try:
        cur.execute(item_based_command)
    except:
        print "There were problems executing the command " + item_based_command
        exit(1, "Could not execute psql command")
    f = open(m.item_based_fname, 'w')
    for record in cur:
        for i in range(len(record) - 1):
            f.write(str(record[i]) + ",")
        f.write(str(record[-1]) + "\n")
    f.close()

def get_item_based_train_test(user_id, test_bus_id_list, train_fname, test_fname):
    """
    :param user_id: id of the user we are trying to recommend
    :param test_bus_id_list: list of businesses that this user has reviewed, but we will exclude from training data,
    so that we can test item_based after training. This list is the same as what is used to test in our original algorithm
    :param train_fname: name of file to store training data
    :param test_fname: name of file to store test data
    :return:
    """
    test_bus_id_cnt = Counter(test_bus_id_list) # convert from a list to a counter so that later on we can
                    # do massive sorting data into train/test files more quickly
    try:
        cur.execute(item_based_command)
    except:
        print "There were problems executing the command " + item_based_command
        exit(1, "Could not execute psql command")
    f_train = open(train_fname, 'w')
    f_test = open(test_fname, 'w')
    for record in cur:
        if (record[0] == user_id and test_bus_id_cnt[record[1]] > 0):
            # if the user_id and bus_id is in the test set, write data into test file
            for i in range(len(record) - 1):
                f_test.write(str(record[i]) + ",")
            f_test.write(str(record[-1]) + "\n")
        else:
            # if the user_id and bus_id are in the train set, write data into train file
            for i in range(len(record) - 1):
                f_train.write(str(record[i]) + ",")
            f_train.write(str(record[-1]) + "\n")
    f_train.close()
    f_test.close()

