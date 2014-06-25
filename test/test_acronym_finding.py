import unittest
import re

from acronym_finding import find_acronyms, find_expanded_acronyms, strip_extraneous_words, fix_divided_expansion, expanded_regex, find_all_acronyms, combine_acronyms, add_expansion


class TestAcronymFinding(unittest.TestCase):
	# assertDictEqual
	
	def test_acronyms_found(self):
			acronyms = find_acronyms('Hello')
			self.assertEqual(len(acronyms), 0)

			acronyms = find_acronyms('Did you work on the ABC project?')
			self.assertEqual(len(acronyms), 1)

			acronyms = find_acronyms("GE Corp built XYZ's froznoTRON")
			self.assertEqual(len(acronyms), 2)
			self.assertTrue('GE' in acronyms)
			self.assertTrue('XYZ' in acronyms)

			self.assertEqual(acronyms['GE'], [''])
			self.assertEqual(acronyms['XYZ'], [''])

	def test_find_expanded_acronyms(self):
			acronyms = find_expanded_acronyms('Howdy Neighbor')
			self.assertEqual(len(acronyms), 0)

			acronyms = find_expanded_acronyms('Did you work on the Alpha Beta Company (ABC) project?')
			self.assertEqual(len(acronyms), 1)
			self.assertTrue('ABC' in acronyms)
			self.assertEqual(acronyms['ABC'], ['Alpha Beta Company'])

			expansions = [ 'Different Expansions Fail', 'Dubious Expressions Fly' ]
			acronyms = find_expanded_acronyms(
							'{0} (DEF) if {1} (DEF)'.format(expansions[0], expansions[1]))
			self.assertEqual(len(acronyms), 1)
			self.assertTrue('DEF' in acronyms)
			self.assertEqual(len(acronyms['DEF']), 2)
			self.assertListEqual(acronyms['DEF'], expansions)

			# Make sure that the same expansion doesn't show up multiple times
			acronyms = find_expanded_acronyms(
							'{0} (DEF) if {1} (DEF) {0} (DEF)'.format(expansions[0], expansions[1]))
			self.assertEqual(len(acronyms), 1)
			self.assertTrue('DEF' in acronyms)
			self.assertEqual(len(acronyms['DEF']), 2)
			self.assertListEqual(acronyms['DEF'], expansions)
			#TODO:  Consider keeping a count of expansions.

			# Make sure that things like '..., Inc.' work ok
			acronyms = find_expanded_acronyms(
							'I think he works at My Favorite Company, Inc. (MFCI), or at least he used to.')
			self.assertEqual(len(acronyms), 1)
			self.assertTrue('MFCI' in acronyms)
			self.assertEqual('My Favorite Company, Inc', acronyms['MFCI'][0])
			# The period at the end of Inc is not expected to be captured - a proofreader could 
			# identify that afterward. 

	def test_expanded_acronyms_sentence_leading_caps(self):
			acronyms = find_expanded_acronyms('The New Old Cat Factory (NOCF) is big.')
			self.assertEqual(len(acronyms), 1)
			self.assertTrue('NOCF' in acronyms)
			self.assertEqual(acronyms['NOCF'], ['New Old Cat Factory'])

			acronyms = find_expanded_acronyms('Come visit The New Old Dog Factory (TNODF)')
			self.assertEqual(len(acronyms), 1)
			self.assertTrue('TNODF' in acronyms)
			self.assertEqual(acronyms['TNODF'], ['The New Old Dog Factory'])

	def test_sentence_leading_caps_strip(self):
			extraneous_expansion = 'The Noodle Flopper'
			expansion = 'Noodle Flopper'
			acronym = 'NF'

			self.assertEqual(strip_extraneous_words(extraneous_expansion, acronym), expansion)

			not_extraneous = 'The Leading Article Company'
			acronym = 'TLAC'

			self.assertEqual(strip_extraneous_words(not_extraneous, acronym), not_extraneous)

			text = 'Thus The Leading Article Company (TLAC) realized its need for following verbs.'
			self.assertEqual(strip_extraneous_words('Thus The Leading Article Company', acronym), not_extraneous)

			acronyms = find_expanded_acronyms(text)
			self.assertEqual(len(acronyms), 1)
			self.assertTrue('TLAC' in acronyms)
			self.assertEqual(acronyms['TLAC'], [not_extraneous])

	def test_catch_divided_expansions(self):
			correct_expansion = 'The Leading Article and Preposition Company, Inc'
			acronym = 'TLAPCI'
			divided_expansion = 'Preposition Company, Inc'
			text = "When I worked for {0} ({1})".format(correct_expansion, acronym) + \
				", we made sure that prepositions were never something we ended sentences with."

			match = re.search(expanded_regex, text)
			revised_expansion = fix_divided_expansion(divided_expansion, acronym, match)

			self.assertEqual(correct_expansion, revised_expansion)


			acronyms = find_expanded_acronyms(text)
			self.assertEqual(len(acronyms), 1)
			self.assertTrue(acronym in acronyms)
			self.assertEqual(correct_expansion, acronyms[acronym][0])


	def test_should_not_span_expansions_across_any_line_breaks(self):
			acronyms = find_expanded_acronyms('Section 1.3.2 Alpha Beta Company\nThe Alpha Beta Company (ABC)')
			self.assertEqual(len(acronyms), 1)
			self.assertTrue('ABC' in acronyms)
			self.assertEqual(acronyms['ABC'], ['Alpha Beta Company'])


			acronyms = find_expanded_acronyms('Section 1.3.2 Alpha Beta Company\rThe Alpha Beta Company (ABC)')
			self.assertEqual(len(acronyms), 1)
			self.assertTrue('ABC' in acronyms)
			self.assertEqual(acronyms['ABC'], ['Alpha Beta Company'])

			# This one isn't strictly across line breaks, but the most common place for a dash to mess 
			# something up would be in a heading/line break/new paragraph starting with that acronym
			# situation, including a dash or other tricksy punctuation.
			acronyms = find_expanded_acronyms('1.  New Good-Fair Company\rThe New Good-Fair Company (NGFC) always...')
			self.assertEqual(len(acronyms), 1)
			self.assertTrue('NGFC' in acronyms)
			self.assertEqual(acronyms['NGFC'], ['New Good-Fair Company'])

	
	def test_acronyms_with_embedded_acronyms(self):
			text = 'The ALPha Beta Company (ALPBC) is a company.  Yes, ALPBC is for realz.  ' + \
							'More in Appendix Q.6 ALPha Beta Company (ALPBC).'
			acronyms = find_expanded_acronyms(text)
			self.assertEqual(len(acronyms), 1)
			self.assertTrue('ALPBC' in acronyms)
			self.assertEqual(len(acronyms['ALPBC']), 1)
			self.assertEqual(acronyms['ALPBC'], ['ALPha Beta Company'])

			text = 'The ALPha BeTa ComPany (ALPBC) is a company.  Yes, ALPBC is for realz.  ' + \
							'More in Appendix Q.6 ALPha BeTa ComPany (ALPBC).'

			acronyms = find_expanded_acronyms(text)
			self.assertEqual(len(acronyms), 1)
			self.assertTrue('ALPBC' in acronyms)
			self.assertEqual(len(acronyms['ALPBC']), 1)
			self.assertEqual(acronyms['ALPBC'], ['ALPha BeTa ComPany'])

				

	def test_find_all_acronyms(self):
			text = 'My BUS went to Zither Yak Xylophone (ZYX) school.  IDK why.  ' + \
							'I hope you Like My Story (LMS), LOL.  ' + \
							'FYI, I meant Laughing Out Loud (LOL).  LOL.'

			acronyms = find_all_acronyms(text)
			self.assertEqual(len(acronyms), 6)
			self.assertDictEqual(acronyms,
							{ 
									'BUS': [''],
									'ZYX': ['Zither Yak Xylophone'],
									'IDK': [''],
									'LMS': ['Like My Story'],
									'LOL': ['Laughing Out Loud'],
									'FYI': ['']
							})

	def test_combine_acronym_lists(self):
			first_text = 'I bought a TV from QVC Pretty Darn Quick (PDQ).'
			second_text = 'My TV is made by Broken Equipment Corp (BEC).  OMG.'

			combined_text = first_text + ' ' + second_text
			correct_combined = find_all_acronyms(combined_text)

			first_acronyms = find_all_acronyms(first_text)
			second_acronyms = find_all_acronyms(second_text)

			test_combined = combine_acronyms(first_acronyms, second_acronyms)
			self.assertDictEqual(correct_combined, test_combined)

			third_text = 'And this software is Pretty Darn Quality (PDQ).'
			combined_text = first_text + ' ' + third_text
			correct_combined = find_all_acronyms(combined_text)

			first_acronyms = find_all_acronyms(first_text)
			third_acronyms = find_all_acronyms(third_text)
			test_combined = combine_acronyms(first_acronyms, third_acronyms)
			# Order of expansions of PDQ not guaranteed, so can't use assertDictEqual
			for k in correct_combined.keys():
					self.assertTrue(k in test_combined)
					self.assertSetEqual(set(correct_combined[k]), set(test_combined[k]))

			self.assertEqual(len(correct_combined), len(test_combined))

	def test_combine_should_not_retain_empty(self):
			first_text = 'I bought my ABC TV from QVC.'
			second_text = 'My Alpha Beta Company (ABC) TV from QVC is pretty sweet.'

			combined_text = first_text + ' ' + second_text
			correct_combined = find_all_acronyms(combined_text)

			first_acronyms = find_all_acronyms(first_text)
			second_acronyms = find_all_acronyms(second_text)

			test_combined = combine_acronyms(first_acronyms, second_acronyms)
			self.assertDictEqual(correct_combined, test_combined)

	def test_request_for_comment(self):
			text = 'Someone published a new Request for Comment (RFC) today.'

			acronyms = find_all_acronyms(text)
			self.assertEqual(len(acronyms), 1)
			self.assertTrue('RFC' in acronyms)
			self.assertEqual(acronyms['RFC'], ['Request for Comment'])

	def test_add_expansion(self):
			acronyms = {}
			add_expansion(acronyms, 'MFE', 'My Fake Expansion')

			self.assertEqual(len(acronyms), 1)
			self.assertEqual(acronyms['MFE'], ['My Fake Expansion'])

			# Adding the same expansion should not change the expansion list
			add_expansion(acronyms, 'MFE', 'My Fake Expansion')
			self.assertEqual(len(acronyms), 1)
			self.assertEqual(acronyms['MFE'], ['My Fake Expansion'])

			add_expansion(acronyms, 'MFE', 'Mother Failed English')
			self.assertEqual(len(acronyms), 1)
			self.assertListEqual(acronyms['MFE'], ['My Fake Expansion', 'Mother Failed English'])

			add_expansion(acronyms, 'ABC', 'A B C')
			self.assertEqual(len(acronyms), 2)
			self.assertListEqual(acronyms['ABC'], ['A B C'])
			self.assertListEqual(acronyms['MFE'], ['My Fake Expansion', 'Mother Failed English'])

# TODO:  Consider adding support for acronym-expansion, e.g. "ABC (Alpha Beta Corporation)"
