##SpeedNotes A Distraction-Free Note-Taking App
##V1_1
##github.com/thomasjupe/SpeedNotes
## 
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, filedialog
import os
from datetime import datetime

# Function to save the note
def save_note():
    note = text_area.get("1.0", "end-1c").strip()
    if note:
        # Get current timestamp
        timestamp = datetime.now().strftime("%A, %d %B , %Y %I:%M %p")
        
        # Determine the category based on the selected toggle
        category = category_var.get()
        file_name = "work_notes.txt" if category == "Work" else "personal_notes.txt"
        
        # Save note to the appropriate file
        with open(file_name, "a") as file:
            file.write(f"[{timestamp}]\n{note}\n---\n")
        
        # Clear the text area and refresh the notes display
        text_area.delete("1.0", "end")
        load_notes()

# Bind Enter to save the note
def on_enter(event=None):
    save_note()
    return "break"  # Prevent the default action of adding a new line

# Function to allow Shift+Enter to add a new line without saving
def on_shift_enter(event=None):
    text_area.insert(tk.END, "\n")
    return "break"  # Prevents the default Enter key behavior from triggering

# Function to load and display notes
def load_notes():
    category = category_var.get()
    file_name = "work_notes.txt" if category == "Work" else "personal_notes.txt"
    
    view_box.configure(state="normal")
    view_box.delete("1.0", tk.END)
    
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            notes = file.read()
            view_box.insert(tk.END, notes)
    else:
        view_box.insert(tk.END, f"No {category.lower()} notes found.")
    view_box.configure(state="disabled")

# Function to adjust the view box width
def adjust_view_box_width():
    # Get window width dynamically
    window_width = root.winfo_width()
    
    # Set the width of the view box to match the window size
    view_box.configure(width=window_width)

# Function to search notes
def search_notes():
    keyword = search_entry.get().strip().lower()
    if not keyword:
        messagebox.showwarning("Empty Search", "Enter a keyword to search!")
        return

    category = category_var.get()
    file_name = "work_notes.txt" if category == "Work" else "personal_notes.txt"
    
    view_box.configure(state="normal")
    view_box.delete("1.0", tk.END)
    
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            notes = file.readlines()
            filtered_notes = [note for note in notes if keyword in note.lower()]
            
            if filtered_notes:
                view_box.insert(tk.END, "".join(filtered_notes))
            else:
                view_box.insert(tk.END, "No matching notes found.")
    else:
        view_box.insert(tk.END, f"No {category.lower()} notes found.")
    view_box.configure(state="disabled")

# Function to delete all notes
def delete_notes():
    category = category_var.get()
    file_name = "work_notes.txt" if category == "Work" else "personal_notes.txt"
    
    if os.path.exists(file_name):
        os.remove(file_name)
        load_notes()
        messagebox.showinfo("Notes Deleted", f"All {category.lower()} notes have been deleted.")
    else:
        messagebox.showwarning("No Notes", f"No {category.lower()} notes to delete.")

# Function to export notes
def export_notes():
    category = category_var.get()
    file_name = "work_notes.txt" if category == "Work" else "personal_notes.txt"
    
    if os.path.exists(file_name):
        # Generate the default filename
        timestamp = datetime.now().strftime("%d%m%y_%H%M")
        default_filename = f"Notes_{timestamp}.txt"
        
        # Open file dialog with prefilled filename
        save_path = filedialog.asksaveasfilename(
            initialfile=default_filename,
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            title="Export Notes"
        )
        if save_path:
            with open(file_name, "r") as file:
                notes = file.read()
            with open(save_path, "w") as file:
                file.write(notes)
            messagebox.showinfo("Notes Exported", f"Your {category.lower()} notes have been exported.")
    else:
        messagebox.showwarning("No Notes", f"No {category.lower()} notes to export.")

# Setting up the main window
ctk.set_appearance_mode("Dark")  # "System", "Dark", or "Light"
ctk.set_default_color_theme("dark-blue")  # "blue", "green", "dark-blue", etc.

root = ctk.CTk()  # Use CustomTkinter window
root.title("ADHD Speed Notes - Version 1.1 - by Thomas Jupe")  # Set the window title
root.geometry("450x700")  # You can set your preferred size here

# Create a text area for entering notes
text_area_label = ctk.CTkLabel(root, text="Enter Notes:")
text_area_label.pack(anchor="w", padx=10)
text_area = ctk.CTkTextbox(root, height=50, width=400, state="normal", wrap="word")
text_area.pack(padx=10, pady=10, fill="both", expand=True)
root.after(100, adjust_view_box_width) # Adjust the view box width dynamically wt delay to ensure the window size is known

# Bind Enter key to save the note
text_area.bind("<Return>", on_enter)

# Bind Shift + Enter to add a new line without saving
text_area.bind("<Shift-Return>", on_shift_enter)

# Function to toggle between Work and Personal notes
def toggle_category():
    # Get the current value of the variable and load corresponding notes
    load_notes()

# Define the category variable (StringVar)
category_var = tk.StringVar(value="Work")  # Default to "Work"

# Add a CTkSwitch to toggle categories
category_switch = ctk.CTkSwitch(
    root, 
    text="Personal Notes/Work Notes",
    command=toggle_category,  # Called when the switch is toggled
    variable=category_var,    # Binds the switch to category_var
    onvalue="Work",           # Value when toggle is ON
    offvalue="Personal"       # Value when toggle is OFF
)
category_switch.pack(pady=10)
ctk.set_widget_scaling(1.1)
# Set the default value programmatically (if needed elsewhere in the code)
category_var.set("Work")  # This updates the variable and ensures the switch reflects the change

# Add Save button 
save_button = ctk.CTkButton(root, text="Save Note", command=save_note, height=40, width=200)
save_button.pack(pady=10)

# Add Search bar and button 
search_frame = ctk.CTkFrame(root)
search_frame.pack(padx=10, pady=5, fill="x")

search_label = ctk.CTkLabel(search_frame, text="Search Notes:")
search_label.pack(side="left", padx=5)

search_entry = ctk.CTkEntry(search_frame)
search_entry.pack(side="left", fill="x", expand=True, padx=5)

search_button = ctk.CTkButton(search_frame, text="Search", command=search_notes)
search_button.pack(side="left", padx=5)

# Add a View box to display saved notes
view_box_label = ctk.CTkLabel(root, text="Saved Notes:")
view_box_label.pack(anchor="w", padx=10)

view_box = ctk.CTkTextbox(root, height=50, width=400, wrap="word")
view_box.pack(padx=10, pady=10, fill="both", expand=True)
root.after(100, adjust_view_box_width) # Adjust the view box width dynamically

# Add Delete and Export buttons 
actions_frame = ctk.CTkFrame(root)
actions_frame.pack(padx=10, pady=5, fill="x")

delete_button = ctk.CTkButton(actions_frame, text="Delete All Notes", command=delete_notes, height=40, width=200)
delete_button.pack(side="left", padx=5)

export_button = ctk.CTkButton(actions_frame, text="Export Notes", command=export_notes, height=40, width=200)
export_button.pack(side="right", padx=5)

### # Add Email button 

###email_button = ctk.CTkButton(actions_frame, text="Email Notes", command=send_notes, height=40, width=200)
###mail_button.pack(side="centre", padx=5)

# Initial loading of notes
load_notes()
    
# Run the application
root.mainloop()
