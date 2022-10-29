import re
from tabulate import tabulate

from scripts import iptables


def _parse_rules(rules_raw: list[str]) -> list[str]:
    """
    This is meant to parse the table that comes from the
    `sudo iptables -L --line-numbers` command into a format
    that is suitable to display in QtListView
    """
    if not isinstance(rules_raw, list):
        raise ValueError(f"Cannot parse {type(rules_raw)} need list[str]")
    if not rules_raw:
        raise ValueError("Input to _parse_rules is empty")

    # Detects Comments
    comments_re = re.compile(r'/\*.*\/')

    in_chain = False
    headers, table = [], []

    result = []

    for line in rules_raw:
        line = line.strip()
        if line == '':
            if in_chain:
                headers.append('extra')
                if table:
                    result += tabulate(table, headers=headers).split('\n')
                else:
                    result += tabulate([""]).split('\n')

                headers, table = [], []
                in_chain = False
            continue
        if line.startswith('Chain'):
            result.append(line)
            continue
        if line.startswith('target') \
                or line.startswith('num'):

            headers = line.split()
            in_chain = True
            continue
        if in_chain:
            parts = line.split()
            begin = parts[:len(headers)]
            extra = ' '.join(parts[len(headers):])
            # comments are too wide and usually redundant - strip out
            extra = comments_re.sub('', extra)
            table.append(begin + [extra])
    return result


def viewRules() -> list[str]:
    rules_str = iptables.viewRules()

    return _parse_rules(rules_str)


def addRule(*args):
    iptables.addRule(*args)


def removeRule(*args):
    iptables.removeRule(*args)


def changeChainPolicy(*args):
    iptables.changeChainPolicy(*args)
