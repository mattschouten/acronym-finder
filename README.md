
Acronym Finder
=========

Handy-dandy acronym finder for any text, including a UI designed to work with Microsoft Word.

Summary
----
`find_all_acronyms` finds basic and expanded acronyms

`find_acronyms` finds basic acronyms.  Basic acronyms are any word consisting of two or more capital letters.

`find_expanded_acronyms` finds expanded acronyms.  Expanded acronyms are strings of the form `"My Acronym Company (MAC)"`:  the expansion followed by the (basic) acronym in parentheses.

These functions all return a dict.  Keys are the acronym.  Each value is a list containing all expansions found.

Technical
----
Should run under Python 2 or 3.  Tested on Python 3.

Unit tests:  `python3 -m unittest test/test_acronym_finding.py`

Legal and License
----
Copyright &copy; 2014-2018 Matt Schouten

There is no warranty, express or implied.

Licensed under the [GNU General Public License v3](http://www.gnu.org/licenses/gpl.html)
