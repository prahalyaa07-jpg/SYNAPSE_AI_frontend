import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import os
import random

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

APP_BG = "#0B1020"
PANEL = "#121A2B"
CARD = "#172338"
ACCENT = "#21C7D9"
TEXT = "#EAF2FF"
MUTED = "#9AAAC2"

class SynapseAI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SYNAPSE AI | Intelligent Document Knowledge Assistant")
        self.geometry("1200x760")
        self.minsize(1000, 650)
        self.configure(fg_color=APP_BG)

        self.documents = []
        self.active_document = None
        self.flashcards = [
            ("What is Artificial Intelligence?", "AI is the ability of machines to perform tasks that typically require human intelligence."),
            ("What is Machine Learning?", "A branch of AI where systems learn patterns from data to make predictions or decisions."),
            ("What is NLP?", "Natural Language Processing enables computers to understand and work with human language.")
        ]
        self.card_index = 0
        self.card_flipped = False
        self.quiz_questions = [
            ("Which technique helps a computer understand human language?", ["NLP", "HTML", "CSS", "SQL"], 0),
            ("Which is a branch of Artificial Intelligence?", ["Networking", "Machine Learning", "Operating Systems", "DBMS"], 1),
            ("What does PDF stand for?", ["Portable Document Format", "Program Data File", "Personal Document Form", "Printed Data Format"], 0)
        ]
        self.quiz_index = 0
        self.quiz_score = 0
        self.quiz_answered = False

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.build_sidebar()
        self.content = ctk.CTkFrame(self, fg_color=APP_BG, corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nsew", padx=22, pady=20)
        self.show_page("Dashboard")

    def build_sidebar(self):
        side = ctk.CTkFrame(self, width=235, corner_radius=0, fg_color=PANEL)
        side.grid(row=0, column=0, sticky="nsw")
        side.grid_propagate(False)
        ctk.CTkLabel(side, text="✦ SYNAPSE", font=ctk.CTkFont(size=27, weight="bold"),
                     text_color=ACCENT).pack(anchor="w", padx=22, pady=(28, 2))
        ctk.CTkLabel(side, text="AI DOCUMENT ASSISTANT", font=ctk.CTkFont(size=10, weight="bold"),
                     text_color=MUTED).pack(anchor="w", padx=23, pady=(0, 25))
        items = [
            ("⌂", "Dashboard"), ("＋", "Upload PDF"), ("✧", "AI Summary"),
            ("◉", "Chat with PDF"), ("⌕", "Semantic Search"), ("▤", "Source References"),
            ("▣", "Document History"), ("◇", "Flashcards"), ("✓", "Quiz"),
            ("◎", "Knowledge Graph"), ("⇄", "PDF Comparison")
        ]
        for icon, name in items:
            ctk.CTkButton(side, text=f"{icon}   {name}", anchor="w", height=39,
                          fg_color="transparent", hover_color="#23334D",
                          text_color=TEXT, font=ctk.CTkFont(size=13),
                          command=lambda n=name: self.show_page(n)).pack(fill="x", padx=12, pady=3)
        ctk.CTkLabel(side, text="FRONTEND DEMO • OFFLINE", text_color=MUTED,
                     font=ctk.CTkFont(size=10)).pack(side="bottom", pady=20)

    def clear(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def heading(self, title, subtitle):
        ctk.CTkLabel(self.content, text=title, font=ctk.CTkFont(size=28, weight="bold"),
                     text_color=TEXT).pack(anchor="w", pady=(8, 3))
        ctk.CTkLabel(self.content, text=subtitle, font=ctk.CTkFont(size=13),
                     text_color=MUTED).pack(anchor="w", pady=(0, 20))

    def card(self, parent, title, body, color=CARD):
        box = ctk.CTkFrame(parent, fg_color=color, corner_radius=14)
        ctk.CTkLabel(box, text=title, font=ctk.CTkFont(size=16, weight="bold"),
                     text_color=ACCENT).pack(anchor="w", padx=17, pady=(15, 7))
        ctk.CTkLabel(box, text=body, font=ctk.CTkFont(size=13), text_color=TEXT,
                     justify="left", wraplength=300).pack(anchor="w", padx=17, pady=(0, 16))
        return box

    def show_page(self, page):
        self.clear()
        if page == "Dashboard": self.dashboard()
        elif page == "Upload PDF": self.upload_page()
        elif page == "AI Summary": self.summary_page()
        elif page == "Chat with PDF": self.chat_page()
        elif page == "Semantic Search": self.search_page()
        elif page == "Source References": self.sources_page()
        elif page == "Document History": self.history_page()
        elif page == "Flashcards": self.flashcards_page()
        elif page == "Quiz": self.quiz_page()
        elif page == "Knowledge Graph": self.graph_page()
        elif page == "PDF Comparison": self.compare_page()

    def dashboard(self):
        self.heading("Welcome to SYNAPSE AI", "Your intelligent document workspace")
        stats = ctk.CTkFrame(self.content, fg_color="transparent")
        stats.pack(fill="x", pady=5)
        for title, value in [("DOCUMENTS", str(len(self.documents))), ("AI TOOLS", "10"), ("WORKSPACE", "READY")]:
            b = ctk.CTkFrame(stats, fg_color=CARD, corner_radius=13)
            b.pack(side="left", fill="x", expand=True, padx=(0, 12))
            ctk.CTkLabel(b, text=title, text_color=MUTED, font=ctk.CTkFont(size=11, weight="bold")).pack(anchor="w", padx=16, pady=(15, 2))
            ctk.CTkLabel(b, text=value, text_color=ACCENT, font=ctk.CTkFont(size=25, weight="bold")).pack(anchor="w", padx=16, pady=(0, 14))
        ctk.CTkLabel(self.content, text="QUICK ACCESS", text_color=MUTED,
                     font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", pady=(25, 10))
        grid = ctk.CTkFrame(self.content, fg_color="transparent")
        grid.pack(fill="both", expand=True)
        options = [
            ("Upload a document", "Add a PDF to your workspace", "Upload PDF"),
            ("Ask your document", "Explore the chat interface", "Chat with PDF"),
            ("Generate a summary", "View a sample AI summary", "AI Summary"),
            ("Study mode", "Practice with interactive flashcards", "Flashcards"),
            ("Test your knowledge", "Take a short sample quiz", "Quiz"),
            ("Compare documents", "Open the comparison workspace", "PDF Comparison")
        ]
        for i, (t, d, p) in enumerate(options):
            r, col = divmod(i, 2)
            f = self.card(grid, t, d)
            f.grid(row=r, column=col, sticky="nsew", padx=6, pady=6)
            ctk.CTkButton(f, text="Open →", width=100, command=lambda x=p: self.show_page(x)).pack(anchor="w", padx=17, pady=(0, 14))
            grid.grid_columnconfigure(col, weight=1)
            grid.grid_rowconfigure(r, weight=1)
        ctk.CTkLabel(self.content, text="Demo note: AI-generated content is represented by sample outputs in this frontend prototype.",
                     text_color=MUTED, font=ctk.CTkFont(size=11)).pack(anchor="w", pady=(10, 0))

    def upload_page(self):
        self.heading("Upload PDF", "Select a document to add it to your demonstration workspace")
        panel = ctk.CTkFrame(self.content, fg_color=CARD, corner_radius=16)
        panel.pack(fill="x", pady=10)
        ctk.CTkLabel(panel, text="⇧", font=ctk.CTkFont(size=48), text_color=ACCENT).pack(pady=(25, 5))
        ctk.CTkLabel(panel, text="Choose a PDF document", font=ctk.CTkFont(size=19, weight="bold")).pack()
        ctk.CTkLabel(panel, text="PDF files • Select a file from your computer", text_color=MUTED).pack(pady=7)
        ctk.CTkButton(panel, text="Browse PDF", command=self.choose_pdf, height=40).pack(pady=(10, 25))
        self.upload_status = ctk.CTkLabel(self.content, text="No document selected yet.", text_color=MUTED)
        self.upload_status.pack(anchor="w", pady=12)
        ctk.CTkLabel(self.content, text="Selected documents", font=ctk.CTkFont(size=17, weight="bold")).pack(anchor="w", pady=(20, 8))
        self.upload_list = ctk.CTkTextbox(self.content, height=180, fg_color=PANEL)
        self.upload_list.pack(fill="both", expand=True)
        self.refresh_upload_list()

    def choose_pdf(self):
        path = filedialog.askopenfilename(title="Choose PDF", filetypes=[("PDF files", "*.pdf")])
        if not path: return
        name = os.path.basename(path)
        if path not in [d["path"] for d in self.documents]:
            self.documents.append({"name": name, "path": path})
        self.active_document = name
        self.upload_status.configure(text=f"✓ Added: {name}", text_color="#63DDAA")
        self.refresh_upload_list()

    def refresh_upload_list(self):
        if hasattr(self, "upload_list") and self.upload_list.winfo_exists():
            self.upload_list.delete("1.0", "end")
            if not self.documents: self.upload_list.insert("end", "No PDFs added in this session.")
            for i, doc in enumerate(self.documents, 1):
                self.upload_list.insert("end", f"{i}.  {doc['name']}\n")

    def summary_page(self):
        self.heading("AI Summary", "Choose a summary length and preview a sample result")
        if self.active_document:
            ctk.CTkLabel(self.content, text=f"Document: {self.active_document}", text_color=ACCENT).pack(anchor="w", pady=(0, 12))
        choice = ctk.StringVar(value="Medium")
        row = ctk.CTkFrame(self.content, fg_color="transparent")
        row.pack(anchor="w", pady=5)
        ctk.CTkLabel(row, text="Summary length:").pack(side="left", padx=(0, 10))
        ctk.CTkOptionMenu(row, values=["Short", "Medium", "Detailed"], variable=choice).pack(side="left")
        output = ctk.CTkTextbox(self.content, height=300, fg_color=PANEL, font=ctk.CTkFont(size=14))
        output.pack(fill="both", expand=True, pady=15)
        samples = {
            "Short": "This document introduces key concepts, explains their importance, and highlights the main takeaways.",
            "Medium": "Overview: The document presents its central topic and supporting ideas.\\n\\nKey points:\\n• Defines the core concepts.\\n• Explains important processes and applications.\\n• Summarizes practical implications.\\n\\nConclusion: The main ideas provide a foundation for further learning.",
            "Detailed": "EXECUTIVE SUMMARY\\n\\n1. Introduction\\nThe document establishes the subject, background and purpose.\\n\\n2. Main concepts\\nIt describes the key terms and explains how the concepts relate to one another.\\n\\n3. Important observations\\nExamples and supporting explanations illustrate the central ideas.\\n\\n4. Conclusion\\nThe document's major themes can be reviewed and used as a basis for further study.\\n\\nNote: This is demonstration text, not a summary extracted from your PDF."
        }
        def generate():
            output.delete("1.0", "end")
            output.insert("end", samples[choice.get()])
        ctk.CTkButton(self.content, text="Generate sample summary", command=generate).pack(anchor="e")
        generate()

    def chat_page(self):
        self.heading("Chat with PDF", "Ask questions in a simulated document conversation")
        if not self.active_document:
            ctk.CTkLabel(self.content, text="Tip: upload a PDF first. You can still try the sample chat.", text_color=MUTED).pack(anchor="w")
        chat = ctk.CTkTextbox(self.content, fg_color=PANEL, font=ctk.CTkFont(size=14))
        chat.pack(fill="both", expand=True, pady=(0, 12))
        chat.insert("end", "SYNAPSE AI  •  Hello! Ask a question about your document.\\n\\n")
        bottom = ctk.CTkFrame(self.content, fg_color="transparent")
        bottom.pack(fill="x")
        entry = ctk.CTkEntry(bottom, placeholder_text="Type your question here...", height=42)
        entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        def send():
            q = entry.get().strip()
            if not q: return
            chat.insert("end", f"\\nYOU  •  {q}\\n")
            chat.insert("end", "SYNAPSE AI  •  This is a sample response. In a connected AI version, the answer would be generated from relevant document passages and include page citations.\\n")
            chat.see("end")
            entry.delete(0, "end")
        ctk.CTkButton(bottom, text="Send", command=send, width=100, height=42).pack(side="right")
        entry.bind("<Return>", lambda event: send())

    def search_page(self):
        self.heading("Semantic Search", "Explore sample meaning-based search results")
        entry = ctk.CTkEntry(self.content, placeholder_text="Enter a concept or question...", height=42)
        entry.pack(fill="x", pady=(0, 10))
        results = ctk.CTkTextbox(self.content, fg_color=PANEL, font=ctk.CTkFont(size=14))
        results.pack(fill="both", expand=True)
        def search():
            q = entry.get().strip()
            if not q: return
            results.delete("1.0", "end")
            results.insert("end", f'Sample results for: "{q}"\\n\\n')
            results.insert("end", "1. Introduction — Page 1\\nRelevant passage: The introduction defines the topic and establishes the context.\\n\\n")
            results.insert("end", "2. Core concepts — Page 3\\nRelevant passage: This section explains the central concepts and their relationships.\\n\\n")
            results.insert("end", "3. Applications — Page 6\\nRelevant passage: Examples show how the concepts can be applied in practice.\\n")
        ctk.CTkButton(self.content, text="Search", command=search).pack(anchor="e", pady=10)

    def sources_page(self):
        self.heading("Source References", "Example citations showing where an answer may be supported")
        for title, desc in [
            ("Source 01  •  Page 2", "Supporting passage: The document introduces the problem statement and its background."),
            ("Source 02  •  Page 5", "Supporting passage: This section explains the key method and its important steps."),
            ("Source 03  •  Page 8", "Supporting passage: The conclusion summarizes the major findings.")
        ]:
            self.card(self.content, title, desc).pack(fill="x", pady=7)

    def history_page(self):
        self.heading("Document History", "PDFs selected during this application session")
        panel = ctk.CTkFrame(self.content, fg_color=PANEL, corner_radius=14)
        panel.pack(fill="both", expand=True)
        if not self.documents:
            ctk.CTkLabel(panel, text="No documents uploaded yet. Visit Upload PDF to add one.", text_color=MUTED).pack(pady=35)
        for i, doc in enumerate(self.documents, 1):
            ctk.CTkLabel(panel, text=f"▤  {i}.  {doc['name']}", text_color=TEXT,
                         font=ctk.CTkFont(size=15)).pack(anchor="w", padx=20, pady=13)

    def flashcards_page(self):
        self.heading("Flashcards", "Click the card to reveal the answer")
        card = ctk.CTkFrame(self.content, fg_color=CARD, corner_radius=18, height=280)
        card.pack(fill="x", pady=20)
        card.pack_propagate(False)
        label = ctk.CTkLabel(card, text="", font=ctk.CTkFont(size=22, weight="bold"),
                             text_color=TEXT, wraplength=650, justify="center")
        label.pack(expand=True, padx=25)
        count = ctk.CTkLabel(self.content, text="", text_color=MUTED)
        count.pack(pady=5)
        def refresh():
            q, a = self.flashcards[self.card_index]
            label.configure(text=a if self.card_flipped else q)
            count.configure(text=f"Card {self.card_index + 1} of {len(self.flashcards)}  •  " + ("Answer" if self.card_flipped else "Question"))
        def flip():
            self.card_flipped = not self.card_flipped
            refresh()
        def next_card():
            self.card_index = (self.card_index + 1) % len(self.flashcards)
            self.card_flipped = False
            refresh()
        row = ctk.CTkFrame(self.content, fg_color="transparent")
        row.pack(pady=15)
        ctk.CTkButton(row, text="Flip card", command=flip).pack(side="left", padx=7)
        ctk.CTkButton(row, text="Next card →", command=next_card).pack(side="left", padx=7)
        refresh()

    def quiz_page(self):
        self.heading("Knowledge Quiz", "Answer the sample multiple-choice questions")
        self.quiz_index, self.quiz_score, self.quiz_answered = 0, 0, False
        question = ctk.CTkLabel(self.content, text="", font=ctk.CTkFont(size=19, weight="bold"),
                                wraplength=750, justify="left")
        question.pack(anchor="w", pady=(15, 20))
        selected = ctk.StringVar(value="")
        options_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        options_frame.pack(fill="x")
        feedback = ctk.CTkLabel(self.content, text="", text_color=ACCENT, font=ctk.CTkFont(size=14))
        feedback.pack(anchor="w", pady=15)
        progress = ctk.CTkLabel(self.content, text="", text_color=MUTED)
        progress.pack(anchor="w")
        next_btn = ctk.CTkButton(self.content, text="Check answer")
        next_btn.pack(anchor="e", pady=15)
        def render():
            self.quiz_answered = False
            selected.set("")
            feedback.configure(text="")
            q, opts, correct = self.quiz_questions[self.quiz_index]
            question.configure(text=f"Question {self.quiz_index + 1}: {q}")
            for w in options_frame.winfo_children(): w.destroy()
            for i, opt in enumerate(opts):
                ctk.CTkRadioButton(options_frame, text=opt, variable=selected, value=str(i),
                                   font=ctk.CTkFont(size=15)).pack(anchor="w", pady=9)
            progress.configure(text=f"Question {self.quiz_index + 1} of {len(self.quiz_questions)}  •  Score: {self.quiz_score}")
            next_btn.configure(text="Check answer", command=check)
        def check():
            if not self.quiz_answered:
                if selected.get() == "":
                    feedback.configure(text="Please select an answer.", text_color="#FFB86B")
                    return
                correct = self.quiz_questions[self.quiz_index][2]
                if int(selected.get()) == correct:
                    self.quiz_score += 1
                    feedback.configure(text="Correct! Well done.", text_color="#63DDAA")
                else:
                    feedback.configure(text=f"Not quite. Correct answer: {self.quiz_questions[self.quiz_index][1][correct]}", text_color="#FF9B9B")
                self.quiz_answered = True
                next_btn.configure(text="Next question" if self.quiz_index < len(self.quiz_questions)-1 else "Show result")
            else:
                if self.quiz_index < len(self.quiz_questions)-1:
                    self.quiz_index += 1
                    render()
                else:
                    question.configure(text=f"Quiz completed! Your score: {self.quiz_score}/{len(self.quiz_questions)}")
                    for w in options_frame.winfo_children(): w.destroy()
                    feedback.configure(text="You can restart the quiz by opening Quiz from the sidebar.")
                    progress.configure(text="Completed")
                    next_btn.configure(text="Finish", state="disabled")
        render()

    def graph_page(self):
        self.heading("Knowledge Graph", "Illustrative concept relationships (sample visualization)")
        canvas = tk.Canvas(self.content, bg=PANEL, highlightthickness=0, height=430)
        canvas.pack(fill="both", expand=True, pady=5)
        canvas.update_idletasks()
        nodes = {
            "Artificial\nIntelligence": (0.5, 0.18),
            "Machine\nLearning": (0.27, 0.48),
            "Natural Language\nProcessing": (0.73, 0.48),
            "Deep\nLearning": (0.27, 0.78),
            "Text\nUnderstanding": (0.73, 0.78)
        }
        w, h = 850, 430
        pts = {k: (x*w, y*h) for k, (x, y) in nodes.items()}
        links = [("Artificial\nIntelligence", "Machine\nLearning"), ("Artificial\nIntelligence", "Natural Language\nProcessing"), ("Machine\nLearning", "Deep\nLearning"), ("Natural Language\nProcessing", "Text\nUnderstanding")]
        for a, b in links:
            canvas.create_line(*pts[a], *pts[b], fill=ACCENT, width=2)
        for name, (x, y) in pts.items():
            canvas.create_oval(x-76, y-34, x+76, y+34, fill="#1E4560", outline=ACCENT, width=2)
            canvas.create_text(x, y, text=name, fill=TEXT, font=("Segoe UI", 10, "bold"), justify="center")
        ctk.CTkLabel(self.content, text="Illustrative graph only — relationships are predefined sample data.",
                     text_color=MUTED).pack(anchor="w", pady=8)

    def compare_page(self):
        self.heading("PDF Comparison", "Select two PDFs and view a sample side-by-side comparison")
        names = [d["name"] for d in self.documents]
        if not names: names = ["Sample_Document_A.pdf", "Sample_Document_B.pdf"]
        left = ctk.StringVar(value=names[0])
        right = ctk.StringVar(value=names[1] if len(names) > 1 else names[0])
        selectors = ctk.CTkFrame(self.content, fg_color="transparent")
        selectors.pack(fill="x", pady=10)
        ctk.CTkLabel(selectors, text="Document A").pack(side="left", padx=5)
        ctk.CTkOptionMenu(selectors, variable=left, values=names).pack(side="left", padx=5)
        ctk.CTkLabel(selectors, text="Document B").pack(side="left", padx=(20, 5))
        ctk.CTkOptionMenu(selectors, variable=right, values=names).pack(side="left", padx=5)
        output = ctk.CTkTextbox(self.content, fg_color=PANEL, font=ctk.CTkFont(size=14))
        output.pack(fill="both", expand=True, pady=15)
        def compare():
            output.delete("1.0", "end")
            output.insert("end", f"COMPARISON: {left.get()}  vs  {right.get()}\\n\\n")
            output.insert("end", "Document A — Main themes\\n• Introduces the topic and its background.\\n• Explains key concepts and applications.\\n\\n")
            output.insert("end", "Document B — Main themes\\n• Presents related concepts and examples.\\n• Highlights practical implications.\\n\\n")
            output.insert("end", "Common ground: Both documents discuss related subject matter.\\nDifferences: Their emphasis and examples may differ.\\n\\n")
            output.insert("end", "Demo note: This is sample comparison content, not an analysis of the selected PDF files.")
        ctk.CTkButton(self.content, text="Compare documents", command=compare).pack(anchor="e")
        compare()

if __name__ == "__main__":
    app = SynapseAI()
    app.mainloop()
