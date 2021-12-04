import re
import glob

def remove_comments(string):
    pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
    # first group captures quoted strings (double or single)
    # second group captures comments (//single-line or /* multi-line */)
    regex = re.compile(pattern, re.MULTILINE|re.DOTALL)
    def _replacer(match):
        # if the 2nd group (capturing comments) is not None,
        # it means we have captured a non-quoted (real) comment string.
        if match.group(2) is not None:
            return "" # so we will return empty to remove the comment
        else: # otherwise, we will return the 1st group
            return match.group(1) # captured quoted-string
    return regex.sub(_replacer, string)

def clean_json(string):
    string = re.sub(",[ \t\r\n]+}", "}", string)
    string = re.sub(",[ \t\r\n]+\]", "]", string)
    return string

def put_missing_commas(string):
    pattern = r"[}\]][ \t\r\n]*[{\[]"
    def _replacer(match):
        word = match[0]
        return word[0] + ',' + word[1:]
    return re.sub(pattern, _replacer, string)

for file in glob.glob("./etk800_sample/*.jbeam"):
    with open(file, 'r') as f:
        s = f.read()
    s = remove_comments(s)
    s = clean_json(s)
    s = put_missing_commas(s)
    with open(file, 'w') as f:
        f.write(s)

