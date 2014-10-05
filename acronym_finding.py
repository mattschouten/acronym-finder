import re

basic_regex = r'\b([A-Z]{2,})\b'
expanded_regex = r'([A-Z][\w\-]+(?:[, ]{1,2}[A-Z][\w\-]+)+)[ .,]{0,2}' + ' \(' + basic_regex + '\)'
expanded_tolerant_regex = r'([A-Z][\w\-]+(?:[ ][\w\-]+)?(?:[, ]{1,2}[A-Z][\w\-]+)+)[ .,]{0,2}' + ' \(' + basic_regex + '\)'
# [, ]{1,2} and [ .,]{0,2} handle ", Inc." and similar things.

def find_all_acronyms(text):
    acronyms = find_acronyms(text)

    expanded = find_expanded_acronyms(text)
    acronyms = combine_acronyms(acronyms, expanded)

    return acronyms

def find_acronyms(text):
    acronyms = {}

    for m in re.finditer(basic_regex, text):
        acronyms[m.group()] = ['']

    return acronyms

def find_expanded_acronyms(text):
    acronyms = {}

    for m in re.finditer(expanded_tolerant_regex, text):
        expansion, acronym = m.groups()

        expansion = fix_divided_expansion(expansion, acronym, m)
        expansion = strip_extraneous_words(expansion, acronym)

        add_expansion(acronyms, acronym, expansion)

    return acronyms

def strip_extraneous_words(expansion, acronym):
    exp = expansion.split(' ')

    # Basic case where everything matches up nicely
    if expansion[0] == acronym[0] and len(exp) <= len(acronym):
        return expansion

    # At least two words in the expansion, two characters in the acronym,
    # the first two expansion words have the same first letter, 
    # BUT the acronym does not start with a double letter.
    # (might be corner cases in here, but this should get the most common cases)
    while len(exp) > 1 and len(acronym) > 1 and \
          exp[0][0] == exp[1][0] and acronym[0] != acronym[1]:
        del exp[0]

    # Simple case where the first word of the expansion doesn't match the first letter of the acronym
    while len(exp) > 0 and exp[0][0] != acronym[0]:
        del exp[0]

    expansion = ' '.join(exp)

    return expansion

def fix_divided_expansion(expansion, acronym, match):
    # Need to remember that sometimes, words are CamelCaseCapitalized or 
    # have random letters pulled out from the middle of a word to make an acronym
    # more pronounceable.  So we can't rely on a count...but we can backtrack 
    # and see what we come up with.

    # Use a count to see if we're in the ballpark
    words_in_expansion = re.split('\W+', expansion)
    if len(words_in_expansion) >= len(acronym): 
        return expansion

    # And check caps for embedded acronyms (Acme Leopard Polident-ha = ALPha; ALPha Beta Company)
    caps_in_expansion = re.split('[A-Z]', expansion)
    if len(caps_in_expansion) >= len(acronym):
        return expansion


    # Grab a reasonable chunk of the string preceding the expansion
    start = match.start() - 100
    if start < 0: start = 0

    preceding = match.string[start:match.start()-1]
    pre = re.split('\W+', preceding)

    lowercase_count = 0
    candidates = []
    while len(pre) > 0 and lowercase_count < 2:
        curr = pre.pop()
        if curr == '': continue

        if curr[0].lower() == curr[0]:
            lowercase_count += 1
        else:
            lowercase_count = 0

        candidates.insert(0, curr)

    candidates = candidates[lowercase_count:]
    
    new_expansion = (' '.join(candidates) + ' ' + expansion).strip()

    return new_expansion

def combine_acronyms(first, second):
	''' Note this does not do any deep copying of the values... '''
	combined = first.copy() 
	for k in second.keys():
		if k in combined:
			combined[k] = list(set(combined[k] + second[k]))
			if len(combined[k]) > 1 and '' in combined[k]:
				combined[k].remove('')
		else:
			combined[k] = second[k]

	return combined

def add_expansion(acronyms, acronym, expansion):
        if acronym not in acronyms:
            acronyms[acronym] = [expansion]
        elif expansion not in acronyms[acronym]:
            acronyms[acronym].append(expansion)

def find_unused_acronyms(found_acronyms, defined_acronyms):
    unused = {k:v for (k,v) in defined_acronyms.items() if k not in found_acronyms}
    return unused


