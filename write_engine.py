"""Run this once to regenerate engine.py cleanly."""
import os

patterns = [
    ('starts_with_0_ends_with_1', '0(0+1)*1', 'All binary strings that start with 0 and end with 1',
     ['01','001','011','0101','00001'], ['10','00','1','0','110'],
     ['0 -> Must begin with 0','(0+1)* -> Any middle','1 -> Must end with 1'],
     [('Empty','e','Rejected'),('Minimum','01','Accepted')], '0(0+1)*1', 'Already optimal.'),
    ('starts_with_1_ends_with_0', '1(0+1)*0', 'All binary strings that start with 1 and end with 0',
     ['10','110','100','1010','11110'], ['01','11','0','1','001'],
     ['1 -> Must begin with 1','(0+1)* -> Any middle','0 -> Must end with 0'],
     [('Empty','e','Rejected'),('Minimum','10','Accepted')], '1(0+1)*0', 'Already optimal.'),
    ('even_number_of_0s', '1*(01*01*)*', 'All binary strings with an even number of 0s',
     ['','11','00','1001','0011'], ['0','100','001','10'],
     ['1* -> Any number of 1s','(01*01*)* -> Pairs of 0s separated by 1s'],
     [('Empty','e','Accepted - zero 0s is even'),('Single 0','0','Rejected')], '1*(01*01*)*', 'Already minimal.'),
    ('does_not_contain_11', '(0+10)*(1+e)', 'All binary strings that do not contain 11 as a substring',
     ['','0','1','01','10','010','101'], ['11','011','110','111','0110'],
     ['(0+10)* -> Blocks of 0 or 10, no two consecutive 1s','(1+e) -> Optionally end with a single 1'],
     [('Empty','e','Accepted'),('11','11','Rejected')], '(0+10)*(e+1)', 'Already optimal.'),
    ('containing_00', '(0+1)*00(0+1)*', 'Strings containing 00 as a substring',
     ['00','100','001','1001','0011'], ['0','1','01','10','101'],
     ['(0+1)* -> Any prefix','00 -> Required substring','(0+1)* -> Any suffix'],
     [('Empty','e','Rejected'),('Just 00','00','Accepted')], '(0+1)*00(0+1)*', 'Already optimal.'),
    ('does_not_end_with_01', '(0+1)*0 + (0+1)*11 + e', 'Strings that do not end with 01',
     ['e','0','1','10','11','100','111'], ['01','001','101','1101'],
     ['(0+1)*0 -> Ends with 0','(0+1)*11 -> Ends with 11','e -> Empty string'],
     [('Empty','e','Accepted'),('01','01','Rejected')], '(0+1)*0 + (0+1)*11 + e', 'Already optimal.'),
    ('odd_number_of_1s', '0*(10*10*)*10*', 'Strings with odd number of 1s',
     ['1','01','10','001','110','111'], ['','0','11','1010','0110'],
     ['0* -> Leading zeros','(10*10*)* -> Even pairs of 1s','10* -> One final 1 making total odd'],
     [('Empty','e','Rejected'),('Single 1','1','Accepted')], '0*(10*10*)*10*', 'Already optimal.'),
    ('starts_with_1_not_end_with_10', '1(0+1)*(0+11)', 'Strings that start with 1 and do not end with 10',
     ['11','100','111','1011','1001'], ['10','110','1010','10110'],
     ['1 -> Must start with 1','(0+1)* -> Any middle','(0+11) -> Must end with 0 or 11'],
     [('Empty','e','Rejected'),('10','10','Rejected - ends with 10')], '1(0+1)*(0+11)', 'Already optimal.'),
    ('ends_with_1_no_00', '(1+01)*1', 'Strings ending with 1 and do not contain 00',
     ['1','11','01','101','011'], ['001','0011','100','00'],
     ['(1+01)* -> Blocks of 1 or 01, never two consecutive 0s','1 -> Must end with 1'],
     [('Empty','e','Rejected'),('Single 1','1','Accepted')], '(1+01)*1', 'Already optimal.'),
    ('does_not_end_with_11', '(0+1)*(0+10)', 'Strings that do not end with 11',
     ['0','10','00','010','110'], ['11','011','111','0011'],
     ['(0+1)* -> Any prefix','(0+10) -> Must end with 0 or 10 (not 11)'],
     [('Empty','e','Rejected'),('11','11','Rejected')], '(0+1)*(0+10)', 'Already optimal.'),
    ('begin_00_end_11', '00(0+1)*11', 'Strings that begin with 00 and end with 11',
     ['0011','00011','00111','000111','001011'], ['00','11','0111','0001'],
     ['00 -> Must start with 00','(0+1)* -> Any middle','11 -> Must end with 11'],
     [('Empty','e','Rejected'),('Minimum','0011','Accepted')], '00(0+1)*11', 'Already optimal.'),
    ('exactly_two_0s', '1*01*01*', 'Strings with exactly two 0s',
     ['00','100','001','010','1001'], ['0','000','1','11','0001'],
     ['1* -> Any leading 1s','0 -> First 0','1* -> Any 1s between','0 -> Second 0','1* -> Any trailing 1s'],
     [('Empty','e','Rejected'),('Minimum','00','Accepted')], '1*01*01*', 'Already optimal.'),
    ('every_0_followed_by_11', '(1+011)*', 'Strings where every 0 is followed by 11',
     ['e','1','11','011','1011','01111'], ['0','01','010','001'],
     ['(1+011)* -> Either a lone 1, or 0 always followed by 11, repeated'],
     [('Empty','e','Accepted'),('Single 0','0','Rejected')], '(1+011)*', 'Already optimal.'),
    ('begin_or_end_with_00_or_11', '(00+11)(0+1)* + (0+1)*(00+11)', 'Strings that begin or end with 00 or 11',
     ['00','11','001','110','0010','1100'], ['01','10','010','101'],
     ['(00+11)(0+1)* -> Starts with 00 or 11','(0+1)*(00+11) -> Ends with 00 or 11'],
     [('Empty','e','Rejected'),('00','00','Accepted')], '(00+11)(0+1)* + (0+1)*(00+11)', 'Already optimal.'),
    ('starts_with_1_even_length', '1(0+1)((0+1)(0+1))*', 'Strings starting with 1 and even length',
     ['10','11','1010','1100','1111'], ['1','0','101','100','111'],
     ['1 -> Starts with 1','(0+1) -> Second symbol','((0+1)(0+1))* -> Remaining pairs keep length even'],
     [('Empty','e','Rejected'),('10','10','Accepted')], '(1(0+1)(0+1))*', 'Already optimal.'),
    ('contains_both_101_and_010', '(0+1)*101(0+1)*010(0+1)* + (0+1)*010(0+1)*101(0+1)*',
     'Strings containing both 101 and 010 as substrings',
     ['101010','010101','1010100','0101010'], ['101','010','111','000'],
     ['(0+1)*101(0+1)*010(0+1)* -> 101 before 010','(0+1)*010(0+1)*101(0+1)* -> 010 before 101'],
     [('Only 101','101','Rejected'),('Only 010','010','Rejected')],
     '(0+1)*101(0+1)*010(0+1)* + (0+1)*010(0+1)*101(0+1)*', 'Already optimal.'),
    ('atleast_two_cs_over_cb', '(b+c)*c(b+c)*c(b+c)*',
     'All strings with at least two c\'s over alphabet {c, b}',
     ['cc','bcc','ccb','bcbc','cbbc','cbc','bccb'],
     ['b','c','bb','bbb',''],
     [
         '(b+c)* -> Any prefix of b or c',
         'c      -> First required c',
         '(b+c)* -> Any symbols between',
         'c      -> Second required c',
         '(b+c)* -> Any suffix of b or c',
     ],
     [('Empty','e','Rejected'),('Single c','c','Rejected - only one c'),
      ('No c','bbb','Rejected'),('Minimum valid','cc','Accepted')],
     '(b+c)*c(b+c)*c(b+c)*',
     'Already optimal. The two mandatory c symbols cannot be collapsed further.'),
]

nlp_rules = [
    (['begin or end'],                       'begin_or_end_with_00_or_11'),
    (['start or end'],                       'begin_or_end_with_00_or_11'),
    (['start', '00', 'end', '11'],           'begin_00_end_11'),
    (['begin', '00', 'end', '11'],           'begin_00_end_11'),
    (['start', '1', 'not end', '10'],        'starts_with_1_not_end_with_10'),
    (['start', '1', 'do not end', '10'],     'starts_with_1_not_end_with_10'),
    (['start', '1', 'even length'],          'starts_with_1_even_length'),
    (['start', '1', 'even'],                 'starts_with_1_even_length'),
    (['ending', '1', 'not contain', '00'],   'ends_with_1_no_00'),
    (['end', '1', 'no', '00'],               'ends_with_1_no_00'),
    (['end', '1', 'not contain', '00'],      'ends_with_1_no_00'),
    (['both', '101', '010'],                 'contains_both_101_and_010'),
    (['contain', '101', '010'],              'contains_both_101_and_010'),
    (['every 0', 'followed by', '11'],       'every_0_followed_by_11'),
    (['every', '0', 'followed', '11'],       'every_0_followed_by_11'),
    (['exactly two', '0'],                   'exactly_two_0s'),
    (['exactly 2', '0'],                     'exactly_two_0s'),
    (['does not end', '01'],                 'does_not_end_with_01'),
    (['do not end', '01'],                   'does_not_end_with_01'),
    (['not end', '01'],                      'does_not_end_with_01'),
    (['does not end', '11'],                 'does_not_end_with_11'),
    (['do not end', '11'],                   'does_not_end_with_11'),
    (['not end', '11'],                      'does_not_end_with_11'),
    (['odd number', '1'],                    'odd_number_of_1s'),
    (['odd', '1'],                           'odd_number_of_1s'),
    (['does not contain', '11'],             'does_not_contain_11'),
    (['not contain', '11'],                  'does_not_contain_11'),
    (['without', '11'],                      'does_not_contain_11'),
    (['no', '11'],                           'does_not_contain_11'),
    (['containing', '00'],                   'containing_00'),
    (['contain', '00'],                      'containing_00'),
    (['even', 'number', '0'],                'even_number_of_0s'),
    (['even', '0'],                          'even_number_of_0s'),
    (['start', '0', 'end', '1'],             'starts_with_0_ends_with_1'),
    (['begin', '0', 'end', '1'],             'starts_with_0_ends_with_1'),
    (['start', '1', 'end', '0'],             'starts_with_1_ends_with_0'),
    (['begin', '1', 'end', '0'],             'starts_with_1_ends_with_0'),
    (['atleast two', 'c'],                   'atleast_two_cs_over_cb'),
    (['at least two', 'c'],                  'atleast_two_cs_over_cb'),
    (['atleast 2', 'c'],                     'atleast_two_cs_over_cb'),
    (['at least 2', 'c'],                    'atleast_two_cs_over_cb'),
    (['two c', '{c'],                        'atleast_two_cs_over_cb'),
    (['two c', 'sigma'],                     'atleast_two_cs_over_cb'),
    (['two c'],                              'atleast_two_cs_over_cb'),
]

out = ['PATTERNS = {']
for key, re, desc, valid, invalid, expl, edges, alt, opt in patterns:
    ec = [{'case': c, 'string': s, 'verdict': v} for c, s, v in edges]
    out.append(f'    {key!r}: {{')
    out.append(f'        "re": {re!r},')
    out.append(f'        "description": {desc!r},')
    out.append(f'        "valid": {valid!r},')
    out.append(f'        "invalid": {invalid!r},')
    out.append(f'        "explanation": {expl!r},')
    out.append(f'        "edge_cases": {ec!r},')
    out.append(f'        "alternative": {alt!r},')
    out.append(f'        "optimization": {opt!r},')
    out.append('    },')
out.append('}')
out.append('')
out.append('''
def get_all_patterns():
    return [{"key": k, "description": v["description"], "re": v["re"]} for k, v in PATTERNS.items()]

def get_pattern(key):
    return PATTERNS.get(key)

def validate_string(key, binary_string):
    pattern = PATTERNS.get(key)
    if not pattern:
        return {"error": "Pattern not found: {}".format(key)}
    result = _check(key, binary_string)
    return {"pattern": key, "re": pattern["re"],
            "input": binary_string if binary_string else "empty",
            "accepted": result, "verdict": "Accepted" if result else "Rejected"}

def _check(key, s):
    if key == "starts_with_0_ends_with_1":      return len(s) >= 2 and s[0]=="0" and s[-1]=="1"
    if key == "starts_with_1_ends_with_0":      return len(s) >= 2 and s[0]=="1" and s[-1]=="0"
    if key == "even_number_of_0s":              return s.count("0") % 2 == 0
    if key == "does_not_contain_11":            return "11" not in s
    if key == "containing_00":                  return "00" in s
    if key == "does_not_end_with_01":           return not s.endswith("01")
    if key == "odd_number_of_1s":               return s.count("1") % 2 == 1
    if key == "starts_with_1_not_end_with_10":  return s.startswith("1") and not s.endswith("10")
    if key == "ends_with_1_no_00":              return s.endswith("1") and "00" not in s
    if key == "does_not_end_with_11":           return not s.endswith("11")
    if key == "begin_00_end_11":                return s.startswith("00") and s.endswith("11") and len(s) >= 4
    if key == "exactly_two_0s":                 return s.count("0") == 2
    if key == "every_0_followed_by_11":
        i = 0
        while i < len(s):
            if s[i] == "0":
                if i+2 >= len(s) or s[i+1] != "1" or s[i+2] != "1":
                    return False
            i += 1
        return True
    if key == "begin_or_end_with_00_or_11":     return len(s) >= 2 and (s[:2] in ("00","11") or s[-2:] in ("00","11"))
    if key == "starts_with_1_even_length":      return s.startswith("1") and len(s) % 2 == 0
    if key == "contains_both_101_and_010":      return "101" in s and "010" in s
    if key == "atleast_two_cs_over_cb":         return s.count("c") >= 2
    return False
''')

out.append('_NLP_RULES = [')
for kws, key in nlp_rules:
    out.append(f'    ({kws!r}, {key!r}),')
out.append(']')
out.append('')
out.append('''
def match_natural_language(text):
    lower = text.lower()
    for keywords, key in _NLP_RULES:
        if all(kw in lower for kw in keywords):
            p = PATTERNS[key]
            return {"matched": True, "key": key, "re": p["re"], "description": p["description"],
                    "explanation": p["explanation"], "valid": p["valid"], "invalid": p["invalid"],
                    "edge_cases": p["edge_cases"], "alternative": p["alternative"],
                    "optimization": p["optimization"]}
    return {"matched": False, "error": "Could not match your description. Try rephrasing.",
            "suggestions": [v["description"] for v in PATTERNS.values()]}
''')

path = os.path.join(os.path.dirname(__file__), 'regex_engine', 'engine.py')
with open(path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
print(f'Written {len(out)} lines to {path}')
