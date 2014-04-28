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

# open ldap connection
l = ldap.open("directory.yale.edu")
l.simple_bind("", "")

def main():
    zoo_users = traverse_zoo()
    users = count_users(zoo_users)

    pprint(users)

    l.unbind_s()

def traverse_zoo():
    zoo_users = []
    for node in nodeList:
        try:
            users = subprocess.check_output(['ssh', 'hx52@' + node, 'users'])
            [zoo_users.append(user) for user in users.strip('\n').split(' ')]
        except subprocess.CalledProcessError, e:
            print e.output
    return zoo_users

def count_users(zoo_users):
    users = {}
    for netid in zoo_users:
        user = search_ldap(netid)
        if user:
            if user not in users:
                users.update({user : 1 })
            else:
                users[user] += 1
    return users

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