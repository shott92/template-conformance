import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import logging
import os
import csv

# Import logic
from template_conformance_core import check_ears_template_compliance, check_rupp_template_compliance, check_agile_story_template_conformance
from file_handlers.docx_handler import read_docx
from file_handlers.excel_handler import read_excel
from file_handlers.reqif_handler import read_reqif
from file_handlers.text_handler import read_text

logging.basicConfig(level=logging.INFO)

class TemplateConformanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Template Conformance Checker")
        self.root.geometry("600x450")
        
        self.setup_ui()
        
    def setup_ui(self):
        # File Selection Frame
        self.file_frame = ttk.LabelFrame(self.root, text="Input File")
        self.file_frame.pack(fill="x", padx=10, pady=5)
        
        self.file_path_var = tk.StringVar()
        self.file_entry = ttk.Entry(self.file_frame, textvariable=self.file_path_var, width=50)
        self.file_entry.pack(side="left", padx=5, pady=5)
        
        self.browse_btn = ttk.Button(self.file_frame, text="Browse", command=self.browse_file)
        self.browse_btn.pack(side="left", padx=5, pady=5)
        
        # Template Selection Frame
        self.template_frame = ttk.LabelFrame(self.root, text="Template Type")
        self.template_frame.pack(fill="x", padx=10, pady=5)
        
        self.template_var = tk.StringVar(value="ears")
        ttk.Radiobutton(self.template_frame, text="EARS", variable=self.template_var, value="ears").pack(side="left", padx=10, pady=5)
        ttk.Radiobutton(self.template_frame, text="Rupp", variable=self.template_var, value="rupp").pack(side="left", padx=10, pady=5)
        ttk.Radiobutton(self.template_frame, text="Agile User Story", variable=self.template_var, value="agile").pack(side="left", padx=10, pady=5)
        
        # Output Frame
        self.output_frame = ttk.LabelFrame(self.root, text="Output Directory")
        self.output_frame.pack(fill="x", padx=10, pady=5)
        
        self.output_path_var = tk.StringVar(value=os.getcwd())
        self.output_entry = ttk.Entry(self.output_frame, textvariable=self.output_path_var, width=50)
        self.output_entry.pack(side="left", padx=5, pady=5)
        
        self.output_browse_btn = ttk.Button(self.output_frame, text="Select Folder", command=self.browse_output)
        self.output_browse_btn.pack(side="left", padx=5, pady=5)
        
        # Action Frame
        self.action_frame = ttk.Frame(self.root)
        self.action_frame.pack(fill="x", padx=10, pady=20)
        
        self.run_btn = ttk.Button(self.action_frame, text="Run Conformance Check", command=self.run_check)
        self.run_btn.pack(fill="x", padx=50)
        
        # Status
        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief="sunken", anchor="w")
        self.status_bar.pack(side="bottom", fill="x")

    def browse_file(self):
        filetypes = (
            ("Word Documents", "*.docx"),
            ("Excel Files", "*.xlsx"),
            ("ReqIF Files", "*.reqif *.reqifz"),
            ("Text Files", "*.txt"),
            ("All Files", "*.*")
        )
        filename = filedialog.askopenfilename(title="Select Requirement File", filetypes=filetypes)
        if filename:
            self.file_path_var.set(filename)

    def browse_output(self):
        directory = filedialog.askdirectory(title="Select Output Folder")
        if directory:
            self.output_path_var.set(directory)

    def run_check(self):
        file_path = self.file_path_var.get()
        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("Error", "Please select a valid input file.")
            return

        template = self.template_var.get()
        output_dir = self.output_path_var.get()
        
        self.status_var.set("Processing...")
        self.root.update_idletasks()
        
        try:
            # 1. Read File
            requirements = []
            if file_path.endswith('.docx'):
                requirements = read_docx(file_path)
            elif file_path.endswith('.xlsx'):
                requirements = read_excel(file_path)
            elif file_path.endswith('.reqif') or file_path.endswith('.reqifz'):
                requirements = read_reqif(file_path)
            elif file_path.endswith('.txt'):
                requirements = read_text(file_path)
            else:
                 messagebox.showerror("Error", "Unsupported file format.")
                 self.status_var.set("Error")
                 return
            
            if not requirements:
                 messagebox.showwarning("Warning", "No requirements found in the file.")
                 self.status_var.set("Ready")
                 return

            # 2. Check Conformance
            if template == 'ears':
                results = check_ears_template_compliance(requirements) # This returns formatted strings currently, might need raw data for better report
            elif template == 'rupp':
                results = check_rupp_template_compliance(requirements)
            elif template == 'agile':
                results = check_agile_story_template_conformance(requirements)
            
            # 3. Save Output
            output_file = os.path.join(output_dir, f"conformance_report_{template}.csv")
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Original Requirement", "Conforming?", "Type", "Quality Score", "Quality Issues", "Tagged Output"])
                
                for res in results:
                    # res is now a dict
                    writer.writerow([
                        res['requirement'], 
                        res['conformance'], 
                        res['type'],
                        res['quality_score'],
                        res['quality_issues'],
                        res['tagged_requirement']
                    ])
            
            self.status_var.set(f"Completed! Report saved: {output_file}")
            messagebox.showinfo("Success", f"Processing complete.\nSaved to {output_file}")
            
        except Exception as e:
            logging.error(e)
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_var.set("Error")


if __name__ == "__main__":
    root = tk.Tk()
    # Apply theme if possible
    try:
        style = ttk.Style()
        style.theme_use('clam')
    except:
        pass
        
    app = TemplateConformanceApp(root)
    root.mainloop()
