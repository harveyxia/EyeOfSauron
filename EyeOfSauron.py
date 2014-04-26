import subprocess
import ldap

l = ldap.open("directory.yale.edu")
l.simple_bind("", "")

def search_ldap(netid):
    baseDN = 'ou=People,o=yale.edu'
    searchScope = ldap.SCOPE_SUBTREE
    retrieveAttributes = None
    searchFilter = netid

    ldap_result_id = l.search(baseDN, searchScope, searchFilter, retrieveAttributes)
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
    print result_set
    return result_set

l.unbind_s()