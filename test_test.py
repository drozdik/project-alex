import tkinter as tk
from tkinter.scrolledtext import ScrolledText


root = tk.Tk()
root.title("ScrolledText Widget")

test = """
asdfasdfasdf
asdf
asdfasdf
asdfasdf
asdfadf
asdfasfd

asdfasdf

asdfasdf

asdfasdf
adfa
sdfasd
fadf
asdf
"""
st = ScrolledText(root, width=50,  height=10)
st.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
st.insert(tk.INSERT, test)
st.configure(state ='disabled')
st.see("end")

root.mainloop()