import win32com.client as win32

word = None
target_document = None

def select_active_document():
		global word, target_document
		word = win32.gencache.EnsureDispatch('Word.Application')
		target_document = word.ActiveDocument

def get_selected_range():
		global word
		if word is None: return ''
		return word.Selection.Range

def get_all_document_range():
		global target_document
		if target_document is None: return ''
		return target_document.Range()

def get_text_in_range(word_range):
		return word_range.Text


def create_acronym_document(acronyms):
		global word
		if word is None: return ''
		acronym_doc = word.Documents.Add(Visible=True)
		table_behavior = win32.constants.wdWord8TableBehavior
		autofit_behavior = win32.constants.wdAutoFitContent

		table = acronym_doc.Tables.Add(
						acronym_doc.Paragraphs.First.Range,
						len(acronyms) + 1, 2, 
						table_behavior, autofit_behavior)

		table.Style = 'Table Grid 8'  # Always classy
		table.Cell(1,1).Range.Text = 'Acronym'
		table.Cell(1,2).Range.Text = 'Expansion'

		row = 2
		
		for acronym in sorted(acronyms):
			expansions = acronyms[acronym]
		      
			table.Cell(row, 1).Range.Text = acronym
			table.Cell(row, 2).Range.Text = '\r\n'.join(expansions)
			row += 1


