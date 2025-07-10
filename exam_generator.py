import json
import os
import subprocess

JSON_INPUT_FILE = "deck_fronts.json"

IMAGE_MEDIA_PATH = "C:/Users/adamw/AppData/Roaming/Anki2/User 1/collection.media"

AUFGABEN_TITLES = [
    "Aufgabe 1: Leistung, Compiler und CPI",
    "Aufgabe 2: MIPS",
    "Aufgabe 3: Arithmetik",
    "Aufgabe 4: Pipelining",
    "Aufgabe 5: Caching"
]

TEX_FOLDER = "Tex"
PDF_FOLDER = "Exams"
BIN_FOLDER = "bin"

os.makedirs(TEX_FOLDER, exist_ok=True)
os.makedirs(PDF_FOLDER, exist_ok=True)
os.makedirs(BIN_FOLDER, exist_ok=True)


def distribute_questions(data):
    try:
        num_exams = min(len(questions) for questions in data.values())
        if num_exams == 0:
            print("Error: At least one deck is empty. Cannot generate exams.")
            return None
    except (ValueError, AttributeError):
        print("Error: Invalid data format. Could not determine deck sizes.")
        return None

    deck_names = list(data.keys())
    exams = [{deck: [] for deck in deck_names} for _ in range(num_exams)]

    for deck_name, questions in data.items():
        for i, question_text in enumerate(questions):
            exam_index = i % num_exams
            exams[exam_index][deck_name].append(question_text.strip())
            
    return exams

def generate_single_exam_latex(exam_data, exam_number, header_map, image_path):
    safe_image_path = image_path.replace('\\', '/')
    
    latex_preamble = r"""
\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage{graphicx}
\usepackage[a4paper, margin=1in]{geometry}
\usepackage{fancyhdr}
\usepackage{tabularx}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{titling}

% --- Customization ---
\renewcommand{\familydefault}{\sfdefault}

% Setup for headers and footers
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{Fakultät Informatik}
\fancyhead[R]{Klausur: Rechnerarchitekturen}
\fancyfoot[C]{\thepage}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0.4pt}

% Set the path where LaTeX will look for the images
\graphicspath{{""" + safe_image_path + r"""/}}

% Customize section titles
\titleformat{\section}{\normalfont\Large\bfseries}{\thesection}{1em}{}
\titleformat{\subsection}{\normalfont\large\bfseries}{}{0em}{}

% --- Title Page Definition ---
\pretitle{\begin{center}\Huge\bfseries}
\posttitle{\end{center}}
\preauthor{}
\postauthor{}
\predate{}
\postdate{}

\title{Übungsklausur Rechnerarchitekturen \\ \large Klausurvariante """ + str(exam_number) + r"""}
\author{}
\date{\today}
"""
    
    latex_body = r"""
\begin{document}

% --- Title Page ---
\begin{titlepage}
    \maketitle
    \vspace{0.5cm}
    \centering
    \begin{tabularx}{0.9\textwidth}{lX}
        \hline\hline \\
        \textbf{Prüfungsfach:} & Rechnerarchitekturen \\
        \textbf{Semester:} & Platzhalter-Semester \\
        \textbf{Prüfungsdauer:} & 90 Minuten \\
        \textbf{Maximale Punktzahl:} & 90 Punkte \\
        \textbf{Erlaubte Hilfsmittel:} & Taschenrechner \\
        \hline\hline
    \end{tabularx}
    \vspace{2.5cm}
    \begin{tabularx}{0.9\textwidth}{lX}
        \textbf{Name:} & \dotfill \\
        \\
        \textbf{Matrikelnummer:} & \dotfill \\
        \\
        \textbf{Unterschrift:} & \dotfill \\
    \end{tabularx}
    \vfill
    {\Large Viel Erfolg!}
\end{titlepage}
\clearpage
"""

    for deck_name in sorted(exam_data.keys()):
        questions = exam_data[deck_name]
        aufgabe_title = header_map.get(deck_name, deck_name)
        latex_body += f"\\subsection*{{{aufgabe_title}}}\n\n"
        
        if not questions:
            latex_body += "Keine Aufgaben in diesem Abschnitt.\\\\\n"
            continue

        latex_body += "\\begin{enumerate}[label=\\alph*), topsep=5pt, itemsep=10pt]\n"
        for question_text in questions:
            parts = question_text.split()
            text_part = ' '.join([p for p in parts if not p.lower().endswith(('.jpg', '.png', '.jpeg'))])
            image_files = [p for p in parts if p.lower().endswith(('.jpg', '.png', '.jpeg'))]

            # Use \mbox{}\\ to put label on its own line:
            latex_body += "\\item \\mbox{}"

            if image_files:
                latex_body += "\\begin{center}"
                for img in image_files:
                    latex_body += f"\\includegraphics[width=0.9\\linewidth, height=0.6\\textheight, keepaspectratio]{{{img}}}\n"
                latex_body += "\\end{center}\n"

        latex_body += "\\end{enumerate}\n\\clearpage\n"

    latex_body += "\n\\end{document}\n"

    return latex_preamble + latex_body




def main():
    print(f"Starting exam generation process...")
    
    try:
        print(f"Attempting to read data from '{JSON_INPUT_FILE}'...")
        with open(JSON_INPUT_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("Successfully loaded JSON data.")
    except FileNotFoundError:
        print(f"FATAL ERROR: The file '{JSON_INPUT_FILE}' was not found.")
        print("Please make sure the JSON file is in the same directory as the script.")
        return
    except json.JSONDecodeError:
        print(f"FATAL ERROR: The file '{JSON_INPUT_FILE}' is not a valid JSON file.")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return

    sorted_deck_names = sorted(data.keys())
    header_map = {deck_name: title for deck_name, title in zip(sorted_deck_names, AUFGABEN_TITLES)}

    print("\nSection Title Mapping:")
    for original, new in header_map.items():
        print(f"  '{original}'  ->  '{new}'")

    print("\nDistributing questions...")
    distributed_exams = distribute_questions(data)
    
    if not distributed_exams:
        print("Halting process due to errors in question distribution.")
        return
        
    num_exams = len(distributed_exams)
    print(f"Successfully planned {num_exams} exam variants.")

    print("\nGenerating individual LaTeX files...")
    for i, exam_content in enumerate(distributed_exams):
        exam_num = i + 1
        base_name = f"klausur_variante_{exam_num}"
        tex_filename = os.path.join(TEX_FOLDER, base_name + ".tex")
        pdf_filename = os.path.join(PDF_FOLDER, base_name + ".pdf")

        latex_output = generate_single_exam_latex(exam_content, exam_num, header_map, IMAGE_MEDIA_PATH)

        try:
            with open(tex_filename, "w", encoding="utf-8") as f:
                f.write(latex_output)
            print(f"  - Successfully created LaTeX: '{tex_filename}'")
        except IOError as e:
            print(f"  - Error writing to file '{tex_filename}': {e}")
            continue

        # Compile LaTeX to PDF using pdflatex in the bin folder
        try:
            print(f"  - Compiling LaTeX to PDF...")
            subprocess.run(
                ["pdflatex", "-output-directory", BIN_FOLDER, tex_filename],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            # Move PDF to Exams folder
            generated_pdf = os.path.join(BIN_FOLDER, base_name + ".pdf")
            if os.path.exists(generated_pdf):
                os.replace(generated_pdf, pdf_filename)
                print(f"    -> PDF moved to: {pdf_filename}")
            else:
                print(f"    -> PDF not found in '{BIN_FOLDER}' after compilation.")
        except subprocess.CalledProcessError:
            print(f"    -> pdflatex compilation failed for '{tex_filename}'")

    print("\n--- Process Complete ---")
    print("Please re-compile the new .tex files to see the layout changes.")

if __name__ == "__main__":
    main()
