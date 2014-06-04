import tkinter as tk
import word
import acronym_finding

class AcronymUi(tk.Frame):

    def __init__(self, parent=None):
        self.step_frame = []
        
        tk.Frame.__init__(self, parent)
        self.parent = parent
        
        self.initUI()

        self.clear_acronyms()

    def initUI(self):
        self.parent.title("Acronym Extractor")

        self.step_frame.append(tk.LabelFrame(self, text="Step 1:  Set Document"))
        self.step_frame[0].place(x=12, y=12) # geometry="492x76+12+12"))
        
        self.set_button = tk.Button(self.step_frame[0], text="Set Working Document",
                                    command=self.set_working_document)
        self.document_label = tk.Entry(self.step_frame[0])


        self.step_frame.append(tk.LabelFrame(self, text="Step 2:  Scan for Acronyms"))
        self.scan_selection_button = tk.Button(self.step_frame[1], text="Scan Selection for Acronyms",
                                    command=self.scan_selection_for_acronyms)

        self.scan_whole_document_button = tk.Button(self.step_frame[1], text="Scan Whole Document",
                                    command=self.scan_whole_document)

        self.acronyms_found_label = tk.Entry(self.step_frame[1])
        self.acronyms_found_label_label = tk.Label(self.step_frame[1], text="Acronyms Found")
        self.clear_acronyms_button = tk.Button(self.step_frame[1], text="Clear Acronyms",
                                    command=self.clear_acronyms)
        
        self.step_frame.append(tk.LabelFrame(self, text="Step 3:  Output"))
        self.generate_acronym_table_button = tk.Button(self.step_frame[2], text="Generate Acronym Table",
                                    command=self.generate_acronym_table)

        self.grid(column=0, row=0)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.step_frame[0].grid(column=0, row=0, sticky='ew', padx=3, pady=3, ipadx=3, ipady=3)
        self.set_button.grid(column=0, row=0, sticky='w')
        self.document_label.grid(column=0, row=1, columnspan=2, sticky='ew')

        self.step_frame[1].grid(column=0, row=1, sticky='ew', padx=3, pady=3, ipadx=10, ipady=3)
        self.scan_selection_button.grid(row=0, column=0, columnspan=2, sticky='w')
        self.scan_whole_document_button.grid(row=0, column=2, columnspan=1, sticky='w')
        self.acronyms_found_label.grid(row=1, column=0, sticky='w')
        self.acronyms_found_label_label.grid(row=1, column=1, sticky='w')
        self.clear_acronyms_button.grid(row=1, column=2, sticky='ew')

        self.step_frame[2].grid(column=0, row=2, sticky='ew', padx=3, pady=3, ipadx=3, ipady=3)
        self.generate_acronym_table_button.grid(row=0, column=0, sticky='we')


        self.step_frame[0].columnconfigure(1, weight=1, minsize=100)
        for fn in range(0, 3):
            self.rowconfigure(fn, weight=1)
            self.step_frame[fn].columnconfigure(0, weight=1)
            self.step_frame[fn].rowconfigure(0, weight=1)


    def set_working_document(self):
        word.select_active_document()
        if word.target_document is not None:
            self.document_label.delete(0, tk.END)
            self.document_label.insert(0, word.target_document.Name)
        
    def scan_selection_for_acronyms(self):
        if word is None:
            return

        text = word.get_text_in_range(word.get_selected_range())
        acronyms = acronym_finding.find_all_acronyms(text)

        self.working_acronyms = acronym_finding.combine_acronyms(self.working_acronyms, acronyms)
        self.update_acronym_count()
    
    def scan_whole_document(self):
        if word is None:
            return

        text = word.get_text_in_range(word.get_all_document_range())
        acronyms = acronym_finding.find_all_acronyms(text)

        self.working_acronyms = acronym_finding.combine_acronyms(self.working_acronyms, acronyms)
        self.update_acronym_count()

    def clear_acronyms(self):
        self.working_acronyms = {}
        self.update_acronym_count()
    
    def generate_acronym_table(self):
        word.create_acronym_document(self.working_acronyms)

    def update_acronym_count(self):
        self.acronyms_found_label.delete(0, tk.END)
        self.acronyms_found_label.insert(0, len(self.working_acronyms))


if __name__ == '__main__':
    root = tk.Tk()
    app = AcronymUi(root)
    app.mainloop()
