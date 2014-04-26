#! /usr/bin/env python

import subprocess
import ldap
from pprint import pprint

nodeList = [ "aphid", "lion", "macaw", "bumblebee", "monkey", "cardinal",
             "newt", "chameleon", "peacock", "cicada", "perch", "cobra",
             "python", "cricket", "dolphin", "rhino", "frog", "scorpion",
             "swan", "gator", "termite", "giraffe", "tick", "grizzly", "tiger",
             "hare", "turtle", "hippo", "viper", "hornet", "jaguar", "zebra",
             "kangaroo", "ladybug"]

# Class for User, initialized with netID
class User:
    def __init__(self, netid):
        self.netid = netid
        self.info = ''
        self.nodes = {}
    def display(self):
        print self.info
        print(self.nodes)
        print('\n')

# open ldap connection
l = ldap.open("directory.yale.edu")
l.simple_bind("", "")

def main():
    zoo_users = traverse_zoo()

    count_users(zoo_users)

    for user in zoo_users:
        user.display()

    l.unbind_s()

# def traverse_zoo():
#     zoo_users = []
#     for node in nodeList:
#         users = subprocess.check_output(['ssh', 'hx52@' + node, 'users'])
#         [zoo_users.append(user) for user in users.strip('\n').split(' ')]
#     return zoo_users

# returns list of User objects
def traverse_zoo():
    user_objects = []
    for node in nodeList:
        output = subprocess.check_output(['ssh', 'hx52@' + node, 'who', '-u'])
        output = output.split('\n')[:-1]

        for line in output:
            line = line.split()
            user_objects.append(get_node_info(node, line))

    return user_objects

def get_node_info(node, output_line):
    if (output_line != []):
        user = User(output_line[0])
        comp = ''
        if (len(output_line) == 7):
            comp = output_line[6]

        info = [output_line[2], output_line[3], output_line[4], comp]
        user.nodes.update( { node: info } )
        return user

def count_users(zoo_users):
    # users = {}
    for user in zoo_users:
        netid = user.netid
        info = search_ldap(netid)
        if info:
            user.info = info
            # if user not in users:
            #     users.update({user : 1 })
            # else:
            #     users[user] += 1
    return

def search_ldap(netid):
    base = 'ou=People,o=yale.edu'
    scope = ldap.SCOPE_SUBTREE
    retrieveAttributes = None
    sfilter = 'uid=' + netid

    ldap_result_id = l.search(base, scope, sfilter, retrieveAttributes)
    result_set = []
    while 1:
            result_type, result_data = l.result(ldap_result_id, 0)
            if (result_data == []):
                    break
            else:
                    ## here you don't have to append to a list
                    ## you could do whatever you want with the individual entry
                    ## The appending to list is just for illustration.
                    if result_type == ldap.RES_SEARCH_ENTRY:
                            result_set.append(result_data)

    if (result_set != []):
        # print result_set
        info = result_set[0][0][1]
        name = info['cn'][0]
        year = info['class'][0]
        if 'college' in info:
            college = info['college'][0]
        else:
            college = info['o'][0]

        return name + ': ' + year + ', ' + college
    else:
        return None

if __name__ == "__main__":
    main()
