# -*- coding: utf-8 -*-
import subprocess
import sys


def cache_results(func):
    cache = {}

    def _wrapped(user):
        if cache.get(user):
            return cache.get(user)

        output = func(user)

        cache[user] = output
        return output

    return _wrapped


@cache_results
def finger(user):
    """Gets LDAP information about a given user.

    :type user: str
    :param user: yelp handle of employee (e.g. aaronloo)
    """
    try:
        result = subprocess.check_output([
            'finger',
            user,
        ])
    except subprocess.CalledProcessError:
        print(
            'Unknown user: {}'.format(user),
            file=sys.stderr,
        )
        # Don't complain loudly, because we still want to process rows.
        return {
            'name': 'Unknown',
            'team': 'Unknown',
            'title': user,
            'manager': 'Unknown',
            'disabled': True,
        }

    # Expected Output of finger:
    #     <name> | <team> | <title> | <location> | Manager: <manager's name> | <tenure>
    data = list(
        map(
            lambda x: x.strip(),
            result.decode('utf-8').split('|'),
        )
    )
    # If an account is disabled, they don't have a manager.
    if data[5] == 'Account is disabled':
        manager = None
        disabled = True
    else:
        manager = data[4][len('Manager: '):]
        disabled = False

    return {
        'name': data[0].split(' (')[0],
        'team': data[1],
        'title': data[2],
        'manager': manager,
        'disabled': disabled,
    }