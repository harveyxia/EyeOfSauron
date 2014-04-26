import subprocess
import ldap
from pprint import pprint

nodeList = [ "aphid", "lion", "macaw", "bumblebee", "monkey", "cardinal",
             "newt", "chameleon", "peacock", "cicada", "perch", "cobra",
             "python", "cricket", "dolphin", "rhino", "frog", "scorpion",
             "swan", "gator", "termite", "giraffe", "tick", "grizzly", "tiger",
             "hare", "turtle", "hippo", "viper", "hornet", "jaguar", "zebra",
             "kangaroo", "ladybug"]

def main():
    # open ldap connection
    l = ldap.open("directory.yale.edu")
    l.simple_bind("", "")

    zoo_users = traverse_zoo()
    users = count_users(zoo_users)

    pprint(users)

    l.unbind_s()

def traverse_zoo():
    zoo_users = []
    for node in nodeList:
        users = subprocess.check_output(['ssh', 'hx52@' + node, 'users'])
        zoo_users.append(users.strip('\n').split(' '))
    return zoo_users

def count_users(zoo_users):
    users = {}
    for netid in zoo_users:
        user = search_ldap(netid)
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

    # print result_set
    info = result_set[0][0][1]
    name = info['cn']
    year = info['class']
    college = info['college']
    
    return name + ': ' + year + ', ' college

if __name__ == "__main__":
    main()