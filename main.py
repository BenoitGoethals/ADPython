# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import ldap3
from ldap3 import Server, Connection, SIMPLE, SYNC, ASYNC, SUBTREE, ALL, ALL_ATTRIBUTES, SAFE_SYNC, core, LEVEL

from simple_ad import ActiveDirectory


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.



    # Create the Server object with the given address.

    server = Server('192.168.0.189', port=389, use_ssl=False, get_info='ALL')

    # Create a connection object, and bind with the given DN and password.
    try:

        conn = Connection(server, user="benoit\\administrator", password="R@nger&1401!",
                                fast_decoder=True, auto_bind=True, auto_referrals=True, check_names=False,
                                read_only=True,
                                lazy=False, raise_exceptions=False)
        print(server.info)
        print(get_child_ou_dns(dn="DC=benoit,DC=be", connection=conn))
        print(get_all_ad_hosts(conn))
        conn.search('DC=benoit,DC=be', '(objectclass=person)')
        print(conn.entries)
        results = conn.search('DC=benoit,DC=be',
                              "(&(objectClass=person)(sAMAccountName=" + 'benoit' + "))",
                              ldap3.SUBTREE,
                              attributes=['*'])
        print(conn.entries)
    except core.exceptions.LDAPBindError as e:
        # If the LDAP bind failed for reasons such as authentication failure.
        print('LDAP Bind Failed: ', e)

    # Press the green button in the gutter to run the script.

def get_all_ad_hosts(connection):
    results = list()
    elements = connection.extend.standard.paged_search(
        search_base='DC=benoit,DC=be',
        search_filter='(&(objectCategory=computer)(!(userAccountControl:1.2.840.113556.1.4.803:=2)))',
        search_scope=SUBTREE,
        attributes=['whenCreated', 'operatingSystem',
            'operatingSystemServicePack', 'name', 'lastLogon',
            'memberOf', 'whenChanged'],
        paged_size=100)
    for element in elements:
        host = dict()
        if 'dn' in element:
            host['dn'] = element['dn']
            host['name'] = element['attributes'][u'name'][0]
            host['memberOf'] = element['attributes'][u'memberOf']
            results.append(host)
    return(results)

def get_child_ou_dns(dn, connection):
    results = list()
    elements = connection.extend.standard.paged_search(
        search_base=dn,
        search_filter='(objectCategory=organizationalUnit)',
        search_scope=LEVEL,
        paged_size=100)
    for element in elements:
        if 'dn' in element:
            if element['dn'] != dn:
                if 'dn' in element:
                    results.append(element['dn'])
    return(results)
if __name__ == '__main__':
    print_hi('PyCharm')


# See PyCharm help at https://www.jetbrains.com/help/pycharm/