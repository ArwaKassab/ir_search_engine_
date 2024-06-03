import tkinter as tk
from tkinter import ttk
from search import get_search_result
from inverted_index import set_inverted_index_store_global_variables


import tkinter as tk
from tkinter import ttk, Canvas
from search import get_search_result
from query_refinement import get_ranked_query_suggestions, _suggest_corrected_query

def update_suggestions(event):
    query = entry.get("1.0", tk.END).strip()
    dataset = dataset_var.get()
    
    if query:
        try:
            last_word = query.split()[-1]
            corrected_word = _suggest_corrected_query(last_word)
            refined_queries = get_ranked_query_suggestions(query, dataset)
            show_suggestions(refined_queries)
            if corrected_word.lower() != last_word.lower():
                show_correction_suggestion(corrected_word, last_word)
            else:
                hide_correction_suggestion()
        except Exception as e:
            show_error_window(f"An error occurred: {e}")
    else:
        suggestion_listbox.place_forget()
        hide_correction_suggestion()

def show_suggestions(suggestions):
    suggestion_listbox.delete(0, tk.END)
    
    for suggestion in suggestions:
        suggestion_listbox.insert(tk.END, suggestion)
    
    suggestion_listbox.place(x=entry.winfo_x(), y=entry.winfo_y() + entry.winfo_height(), width=entry.winfo_width())

def show_correction_suggestion(suggestion, word):
    correction_var.set(f"Did you mean: {suggestion}?")
    correction_label.place(x=entry.winfo_x(), y=entry.winfo_y() - 25)
    correction_label.bind("<Button-1>", lambda e: apply_correction(word, suggestion))

def hide_correction_suggestion():
    correction_label.place_forget()

def apply_correction(word, correction):
    current_text = entry.get("1.0", tk.END).strip()
    new_text = current_text.replace(word, correction, 1)
    entry.delete("1.0", tk.END)
    entry.insert("1.0", new_text)
    hide_correction_suggestion()
    underline_misspelled_words()

def handle_space(event):
    hide_correction_suggestion()
    underline_misspelled_words()

def underline_misspelled_words():
    current_text = entry.get("1.0", tk.END).strip()
    words = current_text.split()
    entry.delete("1.0", tk.END)
    for word in words:
        entry.insert(tk.END, word + " ")
        if _suggest_corrected_query(word).lower() != word.lower():
            start_index = entry.search(word, "1.0", stopindex=tk.END)
            end_index = f"{start_index}+{len(word)}c"
            entry.tag_add("underline", start_index, end_index)
            entry.tag_config("underline", underline=True, foreground="red")

def search():
    try:
        selected_query = suggestion_listbox.get(tk.ACTIVE)
    except tk.TclError:
        show_error_window("No query selected.")
        return

    dataset = dataset_var.get()
    
    try:
        results = get_search_result(selected_query, dataset)
        show_results_window(selected_query, results)
    except Exception as e:
        show_error_window(f"An error occurred: {e}")

def show_results_window(query, results):
    results_window = tk.Toplevel(root)
    results_window.title("Search Results")
    results_window.geometry("800x600")
    
    frame = ttk.Frame(results_window)
    frame.pack(fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    result_text = tk.Text(frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
    result_text.pack(expand=True, fill=tk.BOTH)

    scrollbar.config(command=result_text.yview)
    
    result_content = f"Search result for: {query}\n\n"
    if results and "results" in results:
        for idx, result in enumerate(results["results"], start=1):
            if result['text']:
                result_content += f"{idx}. {result['text']}\n\n"
    else:
        result_content += "No results found."

    result_text.insert(tk.END, result_content)

def show_error_window(message):
    error_window = tk.Toplevel(root)
    error_window.title("Error")
    error_window.geometry("400x200")
    
    label = ttk.Label(error_window, text=message, foreground="red")
    label.pack(expand=True)

def create_gradient(canvas, color1, color2):
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    limit = height
    (r1, g1, b1) = canvas.winfo_rgb(color1)
    (r2, g2, b2) = canvas.winfo_rgb(color2)
    r_ratio = float(r2-r1) / limit
    g_ratio = float(g2-g1) / limit
    b_ratio = float(b2-b1) / limit

    for i in range(limit):
        nr = int(r1 + (r_ratio * i))
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))
        color = "#%4.4x%4.4x%4.4x" % (nr, ng, nb)
        canvas.create_line(0, i, width, i, tags=("gradient",), fill=color)
    canvas.lower("gradient")

# إعداد نافذة التطبيق
root = tk.Tk()
root.title("Search")
root.geometry("800x600")
root.configure(bg="#1e1e1e")

# إعداد الخلفية المدرجة
canvas = Canvas(root, width=800, height=600)
canvas.pack(fill=tk.BOTH, expand=True)
create_gradient(canvas, "#1e1e1e", "#383838")

frame = ttk.Frame(root, padding="20", relief="solid", borderwidth=2, style="Custom.TFrame")
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# إعداد الأنماط
style = ttk.Style()
style.configure("TLabel", font=("Arial", 14), background="#1e1e1e", foreground="#ffffff")
style.configure("TEntry", font=("Arial", 14), padding=5)
style.configure("TButton", font=("Arial", 14), padding=10, background="#000000", foreground="#ffffff")
style.configure("TListbox", font=("Arial", 12), background="#1e1e1e", foreground="#ffffff")
style.configure("Custom.TFrame", background="#1e1e1e")

# إعداد النص التوضيحي
label = ttk.Label(root, text="Enter your query", background="#1e1e1e", foreground="#ffffff")
label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

# إعداد خانة اختيار اسم الداتا سيت
dataset_var = tk.StringVar()
dataset_var.set("antique")  # تعيين القيمة الافتراضية

dataset_label = ttk.Label(root, text="Select Dataset", background="#1e1e1e", foreground="#ffffff")
dataset_label.place(relx=0.3, rely=0.15, anchor=tk.CENTER)

dataset_option = ttk.OptionMenu(root, dataset_var, "antique",  "wiki")
dataset_option.place(relx=0.7, rely=0.15, anchor=tk.CENTER)

# إعداد خانة إدخال النص وجعلها أعرض
entry = tk.Text(root, width=80, height=2, font=("Arial", 14), bg="#333333", fg="#ffffff", insertbackground="#ffffff")
entry.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
entry.bind("<KeyRelease>", update_suggestions)
entry.bind("<space>", handle_space)

# إعداد اقتراح التصحيح
correction_var = tk.StringVar()
correction_label = ttk.Label(root, textvariable=correction_var, font=("Arial", 12), background="#333333", foreground="#ffffff", relief="solid", padding=5)
correction_label.place_forget()

# إعداد قائمة الاقتراحات
suggestion_listbox = tk.Listbox(root, width=80, height=10, font=("Arial", 12), bg="#333333", fg="#ffffff", bd=0, highlightthickness=0)
suggestion_listbox.place_forget()

# إعداد زر البحث وإزالة الحدود والخطوط غير المرغوب فيها
style.configure("Search.TButton", 
                font=("Arial", 14), 
                background="#000000",  # لون خلفية الزر إلى أسود
                foreground="#ffffff",  # لون نص الزر إلى أبيض
                borderwidth=1,  # إضافة حدود لجعل الزر مرئياً بشكل أوضح
                relief="flat")
style.map("Search.TButton", 
          background=[("active", "#000000")],  # لون الخلفية عند التفاعل
          foreground=[("active", "#ffffff")])  # لون النص عند التفاعل

search_button = ttk.Button(root, text="Search", command=search, style="Search.TButton")
search_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

root.mainloop()
