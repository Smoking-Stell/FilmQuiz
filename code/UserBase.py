import csv

"""
Works with base of data

"""


def take_base():

    """
    Converts base from csv to array

    :return: array of data
    """

    base_of_users = []
    with open("base.csv", encoding='utf-8') as r_file:
        file_reader = csv.reader(r_file, delimiter=",")
        for row in file_reader:
            base_of_users.append(row)
    return base_of_users


def rewrite_base(base):

    """
    Write in csv new information

    :param base: information
    :return:
    """

    with open("base.csv", mode='w', encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=",", lineterminator="\n")
        for i in range(len(base)):
            file_writer.writerow([base[i][0], base[i][1]])


def update_base(user_id, points):

    """
    Update base with new points for the user

    :param user_id: user id
    :param points: points of user
    :return:
    """


    base = take_base()
    t = int(base[user_id][1]) + points
    base[user_id][1] = str(t)
    rewrite_base(base)


def check_in_base(usr):

    """
    Check existing of user in base

    :param usr: user name
    :return: -1 or number of user in table
    """

    base = take_base()
    for i in range(len(base)):
        if base[i][0] == usr:
            return i
    return -1


def push(usr):

    """
    Add new user

    :param usr: user name
    :return: id of the user
    """

    base = take_base()
    user_id = len(base)
    base.append([usr, "0"])
    rewrite_base(base)
    return user_id


def get_sorted_base():

    """
    Gives sorted dictionary of users

    :return: diction in increase order
    """

    diction = {}
    sorted_diction = {}
    base = take_base()

    for i in base:
        diction[i[0]] = int(i[1])
    sorted_keys = sorted(diction, key=diction.get)

    for i in sorted_keys:
        sorted_diction[i] = diction[i]

    return sorted_diction
