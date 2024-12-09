import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import font
import os
import RetrievalModel as RM
listlen = 0

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    root = tk.Tk()

    root.title("Search Engine")
    root.geometry("1024x480")
    root.configure(bg='#000000')

    back_frame = tk.Frame(root,bg='#2c2e30')
    back_frame.pack(fill="both", expand=True)
    back_frame.grid_rowconfigure(1)  # Allow row 1 to expand
    back_frame.grid_rowconfigure(2)  # Allow row 2 to expand
    back_frame.grid_columnconfigure(0, weight=1)
    
    img = Image.open(os.getcwd() + "\\web-search-engine_8346083.png")
    img = img.resize((100, 100))
    img_tk = ImageTk.PhotoImage(img)
    label = tk.Label(back_frame,bg="#2c2e30", text="Loading image...")
    label.grid(row=0,column=0,sticky="nsew",pady=(10,0))
    # Display the image in a Label
    label.config(image=img_tk)
    label.image = img_tk

    time_frame = tk.Frame(back_frame,bg='#2c2e30',width=5, height=5,)
    time_frame.grid(row=1,column=0,sticky="nsew",pady=(0,3),padx=80)
    
    timeCounter = ""
    timeTakenText = tk.Label(time_frame,text=timeCounter,bg="#2c2e30",fg="white")
    timeTakenText.pack(fill="both", expand=True)

    bottom_frame = tk.Frame(back_frame,bg='#2c2e30')
    bottom_frame.grid(row=2,column=0,sticky="nsew",pady=(0,10),padx=80)

    customFont = font.Font(family="Arial", size=20, weight="bold")
    search_frame = tk.Frame(bottom_frame)
    search_box = tk.Text(search_frame,width=50,font=customFont,height=1,wrap='none')
    search_box.grid(row=0,column=0,sticky="nsew")
    search_btn = tk.Button(search_frame,width=5,text='⌕',font=('Bold'), bg='#76808a',bd=0,activebackground='#2c2e30', command=lambda :(startSearch(bottom_frame)))
    search_btn.grid(row=0,column=1,sticky="nsew")
    search_frame.pack()

    resultFrame = tk.Frame(bottom_frame)
    resultFrame.pack(fill="both", expand=True,pady=10)
    resultList = tk.Listbox(resultFrame, justify="center")
    resultList.pack(fill="both", expand=True)

    def startSearch(bottom_frame):
        global listlen
        timeCounter = 0
        try:
            itemList, timeCounter = RM.process_query(str(search_box.get("1.0",tk.END)))
            for i in range(listlen):
                resultList.delete(0)
            
            listlen = len(itemList)
            timeTakenText.config(text = f"{listlen} results in {timeCounter} seconds")

            for i in range(len(itemList)):
                resultList.insert(tk.END,itemList[i])

            resultList.config(height=50)
        except:
            for i in range(listlen):
                resultList.delete(0)
            listlen = 0
            timeTakenText.config(text = "No results found.")

    root.mainloop()
