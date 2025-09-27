import re


def parse_string(string):
    # Replace all \' and \" with \\' and \\"
    
    def replacer(m):
        matched_str = m.group(0)  # ex. \\\"
        matched_esc = m.group(1)  # ex. \"
        return matched_str[0:-2] + "\\" + matched_esc  # ex. \\\\"
    
    # matches ' or " with odd number of \ behind
    string = re.sub(r"(?<!\\)(?:\\\\)*(\\['\"])", replacer, string)

    # Parse the string with standard unicode escapes (\n, \t, \xhh, etc.)
    string = string.encode().decode("unicode-escape")

    # Use custom escape \|
    string = string.replace("\\|", "|")

    return string


def parse_boolean(string):
    if string in ["1", "t", "true"]:
        return True
    if string in ["0", "f", "false"]:
        return False
    raise ValueError(f"Invalid boolean literal: {string}")
