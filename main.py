from form_gen_trie import *
from operation_to_dict import *
from cut import *
from tkinter import *
from tkinter.filedialog import askopenfilename,asksaveasfilename
from tkinter import messagebox
import string
import os
path = os.getcwd()

UI=Tk()
UI.title('Chinese Word Segmentation System')
UI.geometry('800x600')

def seg_by_file():
    global UI1,background1,BG1,button6,button7,button8
    try:
        UI1.destroy()
    except:
        pass
    UI1=Toplevel()
    UI1.title('Segmentation by file')
    UI1.geometry('600x400')
    UI1.attributes('-topmost',2)
    background1=PhotoImage(file=path+'\\picture\\BG2.gif')
    button6=PhotoImage(file=path+'\\picture\\openfile.gif')
    button7=PhotoImage(file=path+'\\picture\\kakutei.gif')
    button8=PhotoImage(file=path+'\\picture\\modoru.gif')
    BG1=Label(UI1,image=background1)
    BG1.place(x=300,y=200,anchor=CENTER)
    Input1=Entry(UI1,width=35)
    Input1.place(x=300,y=75,anchor=CENTER)
    try:
        Input1.insert(0,openpath2)
    except:
        pass
    def callback():
        global filepath
        Input1.delete(0,END)
        UI1.lower()
        filepath=askopenfilename(filetypes=[('TXT files','*.txt')])
        if filepath:
            Input1.insert(0,filepath)
        UI1.attributes('-topmost',2)
    Button6=Button(UI1,image=button6,command=callback)
    Button6.place(x=450,y=75,anchor=CENTER)
    def confirm():
        filepath=Input1.get()
        global subUI1,subBG1,subbackground1
        try:
            subUI.destroy()
        except:
            pass
        subbackground1=PhotoImage(file=path+'\\picture\\sub1.gif')
        subUI1=Toplevel(UI1)
        subUI1.title('Choose save path')
        subUI1.geometry('450x300')
        subUI1.attributes('-topmost',1)
        subBG1=Label(subUI1,image=subbackground1)
        subBG1.place(x=225,y=150,anchor=CENTER)
        Input2=Entry(subUI1,width=35)
        Input2.place(x=225,y=30,anchor=CENTER)
        def savepathchoose():
            Input2.delete(0,END)
            global savepath
            UI1.lower()
            subUI1.lower()
            savepath=asksaveasfilename(filetypes=[('TXT files','*.txt')])
            if savepath:
                Input2.insert(0,savepath)
            UI1.attributes('-topmost',2)
            subUI1.attributes('-topmost',1)
        Asksavepath=Button(subUI1,image=button6,command=savepathchoose)
        Asksavepath.place(x=375,y=30,anchor=CENTER)
        def seg_for_txt(originfile,savepath):
            with open(originfile,'r') as ready:
                originstr = ready.read()
                blocklist = seg(originstr)
                seglist = []
                for sentence in blocklist:
                    DAG = get_DAG(sentence)
                    route = calc(sentence,DAG)
                    for i in cut_at_last(sentence):
                        seglist.append(i)
            with open(savepath,'w',-1,'utf-8') as after_file:
                segstr = ''.join(seglist)
                after_file.write(segstr)
        def save():
            try:
                savepath=Input2.get()
                seg_for_txt(filepath,savepath)
                messagebox.showinfo('Message','The result has been stored in the given path, you can check it now.')
            except:
                messagebox.showerror('Error','Please check if the paths are valid!')
                return
            subUI1.destroy()
        Save=Button(subUI1,image=button7,command=save)
        Save.place(x=120,y=60)
        subUI1.mainloop()
    Button7=Button(UI1,image=button7,command=confirm)
    Button7.place(x=300,y=200,anchor=CENTER)
    def go_back():
        UI1.destroy()
    Button8=Button(UI1,image=button8,command=go_back)
    Button8.place(x=300,y=260,anchor=CENTER)
    UI1.mainloop()

def seg_for_txt_2(originstr,path):
    with open(path,'w',-1,'utf-8') as after_file:
        after_file.write(cut_at_last(originstr))

def seg_by_sentence():
    global UI2,background2,BG2,button9,button10,button11,button12
    try:
        UI2.destroy()
    except:
        pass
    UI2=Toplevel()
    UI2.title('Segmentation by sentences')
    UI2.geometry('600x400')
    UI2.attributes('-topmost',2)
    background2=PhotoImage(file=path+'\\picture\\BG3.gif')
    button9=PhotoImage(file=path+'\\picture\\kakutei.gif')
    button10=PhotoImage(file=path+'\\picture\\modoru.gif')
    button11=PhotoImage(file=path+'\\picture\\part_seg.gif')
    button12=PhotoImage(file=path+'\\picture\\zenbu_seg.gif')
    BG2=Label(UI2,image=background2)
    BG2.place(x=300,y=200,anchor=CENTER)
    textbox=Text(UI2,height=10,width=200)
    try:
        textbox.insert(1.0,text2)
    except:
        pass
    textbox.pack()
    def click_Button9():
        global choices,options
        try:
            options.destroy()
        except:
            pass
        def seg(paragraph):
            text=textbox.get('1.0',END)
            result_list=[]
            punctuation=[b'\xef\xbc\x8c'.decode('utf-8'),b'\xe3\x80\x82'.decode('utf-8'),b'\xef\xbc\x9f'.decode('utf-8'),b'\xef\xbc\x81'.decode('utf-8'),'-',b'\xe2\x80\xa6\xe2\x80\xa6'.decode('utf-8'),b'\xef\xbc\x9b'.decode('utf-8'),b'\xe2\x80\xa6'.decode('utf-8'),'\n','\t']
            t=0
            for i in range(len(text)):
                for j in punctuation:
                    if text[i]==j:
                        if j=='\n' or j=='\t':
                            result_list+=[text[t:i]]
                            t=i+1
                        else:
                            result_list+=[text[t:i+1]]
                            t=i+1
            result_list+=[text[t:-1]]
            return(result_list)
        global result_list
        result_list=seg(textbox)
        if result_list!=['','']:
            result_list.remove('')
            choices=StringVar()
            choices.set('Please choose a sentence')
            options=OptionMenu(UI2,choices,*result_list)
            options.place(x=225,y=225)
            def part_seg():
                text=choices.get()
                text0=choices.get()
                for p in string.punctuation:
                    text=text.replace(p,'')
                possible_list=possi(text)
                if Chinese(text0):
                    try:
                        subUI0.destroy()
                    except:
                        pass
                    subUI0=Toplevel(UI2)
                    subUI0.geometry('600x400')
                    subUI0.title('Result')
                    subUI0.attributes('-topmost',1)
                    subBG0=Label(subUI0,image=background2)
                    subBG0.place(x=300,y=200,anchor=CENTER)
                    textbox2=Text(subUI0,height=3,width=200)
                    textbox2.pack()
                    text0=cut_at_last(text0)
                    textbox2.insert(1.0,'The result is:'+text0)
                    modoru=Button(subUI0,image=button10,command=subUI0.destroy)
                    modoru.place(x=300,y=80,anchor=CENTER)
                    List=Listbox(subUI0)
                    List['selectmode']=MULTIPLE
                    for i in range(len(possible_list)):
                        List.insert(i+1,possible_list[i])
                    List.place(x=0,y=50)
                    def all_add():
                        chosen_tuple=List.curselection()
                        for number in chosen_tuple:
                            number=int(number)
                            add_to_dict(possible_list[number],3)
                        messagebox.showinfo('Message','The words chosen have been added to the lexicon.')
                    addword=Button(subUI0,image=button3,command=all_add)
                    addword.place(x=360,y=180,anchor=CENTER)
                    info=Label(subUI0)
                    info['text']='The words in the left list might be new words to the lexicon.\n If you would like to add some of them to the lexicon,\n please click them and then click the add new words button.\nThis will have effect the next time this program operates.'
                    info.place(x=300,y=300,anchor=CENTER)
                else:
                    messagebox.showerror('Error','Please choose a sentence including Chinese characters!')
                subUI0.mainloop()
            Button11=Button(UI2,image=button11,command=part_seg)
            Button11.place(x=300,y=275,anchor=CENTER)
            def all_seg():
                global subbackground1,button6,button7,subBG2
                subbackground1=PhotoImage(file=path+'\\picture\\sub1.gif')
                button6=PhotoImage(file=path+'\\picture\\openfile.gif')
                button7=PhotoImage(file=path+'\\picture\\kakutei.gif')
                text=textbox.get('1.0',END)
                subUI2=Toplevel(UI2)
                subUI2.title('Choose save path')
                subUI2.geometry('450x300')
                subUI2.attributes('-topmost',1)
                subBG2=Label(subUI2,image=subbackground1)
                subBG2.place(x=225,y=150,anchor=CENTER)
                Input3=Entry(subUI2,width=35)
                Input3.place(x=225,y=30,anchor=CENTER)
                def savepathchoose():
                    Input3.delete(0,END)
                    global savepath2
                    UI2.lower()
                    subUI2.lower()
                    savepath2=asksaveasfilename(filetypes=[('TXT files','*.txt')])
                    if savepath2:
                        Input3.insert(0,savepath2)
                    UI2.attributes('-topmost',2)
                    subUI2.attributes('-topmost',1)
                Asksavepath2=Button(subUI2,image=button6,command=savepathchoose)
                Asksavepath2.place(x=375,y=30,anchor=CENTER)
                def save2():
                    savepath2=Input3.get()
                    try:
                        seg_for_txt_2(text,savepath2)
                        messagebox.showinfo('Message','The result has been stored in the given path, you can check it now.')
                    except:
                        messagebox.showerror('Error','Please check if the path is valid!')
                        return
                    subUI2.destroy()
                Save2=Button(subUI2,image=button7,command=save2)
                Save2.place(x=120,y=60)
            Button12=Button(UI2,image=button12,command=all_seg)
            Button12.place(x=300,y=375,anchor=CENTER)
    Button9=Button(UI2,image=button9,command=click_Button9)
    Button9.place(x=175,y=175,anchor=CENTER)
    def go_back():
        UI2.destroy()
    Button10=Button(UI2,image=button10,command=go_back)
    Button10.place(x=425,y=175,anchor=CENTER)
    UI2.mainloop()

def add_word():
    global UI3,background3,BG3,button13,button14,Button13,Button14
    try:
        UI3.destroy()
    except:
        pass
    UI3=Toplevel()
    UI3.title('Add new words to the lexicon')
    UI3.geometry('600x400')
    UI3.attributes('-topmost',2)
    background3=PhotoImage(file=path+'\\picture\\BG4.gif')
    button13=PhotoImage(file=path+'\\picture\\modoru1.gif')
    button14=PhotoImage(file=path+'\\picture\\kakutei1.gif')
    BG3=Label(UI3,image=background3)
    BG3.place(x=300,y=200,anchor=CENTER)
    def go_back():
        UI3.destroy()
    Button13=Button(UI3,image=button13,command=go_back)
    Button13.place(x=425,y=300,anchor=CENTER)
    Input=Entry(UI3,width=35)
    Input.place(x=200,y=75,anchor=CENTER)
    def click_button14():
        global subUI3,subbackground3,word,low_level,medium_level,high_level
        word=Input.get()
        if not Chinese(word):
            messagebox.showerror('Error','Please enter a word including at least one Chinese character!')
            return
        if search_abs(word):
            messagebox.showwarning('Warning','This word is already in the lexicon.\n If you would like to set this a general service word,\n please use Add general service word.')
            return
        try:
            subUI3.destroy()
        except:
            pass
        subUI3=Toplevel(UI3)
        subUI3.geometry('450x300')
        subUI3.title('Choose frequency')
        subUI3.attributes('-topmost',1)
        subbackground3=PhotoImage(file=path+'\\picture\\sub3.gif')
        subBG3=Label(subUI3,image=subbackground3)
        subBG3.place(x=225,y=150,anchor=CENTER)
        low_level=PhotoImage(file=path+'\\picture\\level_1.gif')
        medium_level=PhotoImage(file=path+'\\picture\\level_2.gif')
        high_level=PhotoImage(file=path+'\\picture\\level_3.gif')
        def click_level_1():
            add_to_dict(word,1)
            messagebox.showinfo('Message','The word has been successfully added to the lexicon.')
            subUI3.destroy()
        Low_level=Button(subUI3,image=low_level,command=click_level_1)
        Low_level.place(x=225,y=30,anchor=CENTER)
        def click_level_2():
            add_to_dict(word,3)
            messagebox.showinfo('Message','The word has been successfully added to the lexicon.')
            subUI3.destroy()
        Medium_level=Button(subUI3,image=medium_level,command=click_level_2)
        Medium_level.place(x=225,y=80,anchor=CENTER)
        def click_level_3():
            add_to_dict(word,5)
            messagebox.showinfo('Message','The word has been successfully added to the lexicon.')
            subUI3.destroy()
        High_level=Button(subUI3,image=high_level,command=click_level_3)
        High_level.place(x=225,y=130,anchor=CENTER)
        subUI3.mainloop()
    Button14=Button(UI3,image=button14,command=click_button14)
    Button14.place(x=425,y=75,anchor=CENTER)
    UI3.mainloop()

def Copyright():
    global UI4,background4,BG4,button12
    try:
        UI4.destroy()
    except:
        pass
    UI4=Toplevel()
    UI4.title('Copyright Information')
    UI4.geometry('600x400')
    UI4.attributes('-topmost',2)
    background4=PhotoImage(file=path+'\\picture\\BG5.gif')
    button12=PhotoImage(file=path+'\\picture\\modoru1.gif')
    BG4=Label(UI4,image=background4)
    BG4.place(x=300,y=200,anchor=CENTER)
    def go_back():
        UI4.destroy()
    Button12=Button(UI4,image=button12,command=go_back)
    Button12.place(x=415,y=350)
    UI4.mainloop()

def Open():
    openpath=askopenfilename(filetypes=[('TXT files','*.txt')])
    global text2
    try:
        opened_file=open(openpath,'r',-1,'utf-8')
        text2=opened_file.read()
    except UnicodeDecodeError:
        opened_file=open(openpath,'r',-1,'gbk')
        text2=opened_file.read()
    opened_file.close()
    seg_by_sentence()

def Get_path():
    global openpath2
    openpath2=askopenfilename(filetypes=[('TXT files','*.txt')])
    seg_by_file()

def add_general_service_word():
    global UI5,background5,BG5,button15,button16,Button15,Button16
    try:
        UI5.destroy()
    except:
        pass
    UI5=Toplevel()
    UI5.title('Add general service words to the lexicon')
    UI5.geometry('600x400')
    UI5.attributes('-topmost',2)
    background5=PhotoImage(file=path+'\\picture\\BG3.gif')
    button15=PhotoImage(file=path+'\\picture\\modoru1.gif')
    button16=PhotoImage(file=path+'\\picture\\kakutei1.gif')
    BG5=Label(UI5,image=background5)
    BG5.place(x=300,y=200,anchor=CENTER)
    def go_back():
        UI5.destroy()
    Button15=Button(UI5,image=button15,command=go_back)
    Button15.place(x=425,y=300,anchor=CENTER)
    Input4=Entry(UI5,width=35)
    Input4.place(x=200,y=75,anchor=CENTER)
    def click_button16():
        global gen_ser_word
        gen_ser_word=Input4.get()
        if not Chinese(gen_ser_word):
            messagebox.showerror('Error','Please enter a word including at least one Chinese character!')
            return
        else:
            if search_abs(gen_ser_word):
                general_service_word(gen_ser_word)
                messagebox.showinfo('Message','This gereral service word has been successfully added to the lexicon.')
            else:
                judge=messagebox.askyesno('Question','This word is not in the lexicon, would you like to add this word to the lexicon and use it as a general service word?')
                if judge:
                    add_to_dict(gen_ser_word,5)
                    messagebox.showinfo('Message','This gereral service word has been successfully added to the lexicon.')
                else:
                    return
    Button16=Button(UI5,image=button16,command=click_button16)
    Button16.place(x=425,y=75,anchor=CENTER)
    UI5.mainloop()

def Search_word():
    global button17,button18,searchUIbackground,searchUIBG
    button17 = PhotoImage(file=path + '\\picture\\kakutei.gif')
    button18 = PhotoImage(file=path + '\\picture\\modoru.gif')
    searchUI=Toplevel(UI)
    searchUI.title('Search')
    searchUI.geometry('450x400')
    searchUI.attributes('-topmost',2)
    searchUIbackground=PhotoImage(file=path + '\\picture\\BG6.gif')
    searchUIBG=Label(searchUI,image=searchUIbackground)
    searchUIBG.place(x=225,y=200,anchor=CENTER)
    entry=Entry(searchUI,width=35)
    entry.place(x=225,y=25,anchor=CENTER)
    def kakutei():
        word=entry.get()
        p = re.compile(r'\s')
        judge = Chinese(word)
        n = False
        i=0
        List = Listbox(searchUI)
        if judge == True:
            wordlist = form_gen_trie(path + '\\dict.txt')
            for wordfreq in wordlist:
                if word in wordfreq:
                    i=i+1
                    List.insert(i, p.split(wordfreq)[0])
                    n = True
            if n == False:
                messagebox.showinfo('Message', 'There is no word including the given string in the lexicon.')
            else:
                info=Label(searchUI)
                info['text']='All words including the given string in the lexicon have been listed.'
                info.place(x=200,y=375,anchor=CENTER)
                List.place(x=0, y=100)
        else:
            messagebox.showerror('Error','Please enter a word including at least one Chinese character!')
    Button17=Button(searchUI,image=button17,command=kakutei)
    Button17.place(x=275,y=125,anchor=CENTER)
    def modoru():
        searchUI.destroy()
    Button18=Button(searchUI,image=button18,command=modoru)
    Button18.place(x=275,y=185,anchor=CENTER)
    searchUI.mainloop()

def manual():
    ManualUI=Toplevel(UI)
    ManualUI.title('Manual')
    ManualUI.geometry('450x650')
    try:
        opened_file=open(path+'\\picture\\Manual.txt','r',-1,'utf-8')
        text3=opened_file.read()
    except UnicodeDecodeError:
        opened_file=open(path+'\\picture\\Manual.txt','r',-1,'gbk')
        text3=opened_file.read()
    opened_file.close()
    Textbox=Text(ManualUI,height=50,width=225)
    Textbox.pack()
    Textbox.insert(1.0,text3)
    ManualUI.mainloop()
mainbackground=PhotoImage(file=path+'\\picture\\BG1.gif')
button0=PhotoImage(file=path+'\\picture\\gen_ser.gif')
button1=PhotoImage(file=path+'\\picture\\wjfc.gif')
button2=PhotoImage(file=path+'\\picture\\yjfc.gif')
button3=PhotoImage(file=path+'\\picture\\Addword.gif')
button4=PhotoImage(file=path+'\\picture\\copyright.gif')
button5=PhotoImage(file=path+'\\picture\\exit.gif')
MBG=Label(UI,image=mainbackground)
MBG.place(x=400,y=300,anchor=CENTER)
Button0=Button(UI,image=button0,command=add_general_service_word)
Button0.place(x=400,y=400,anchor=CENTER)
Button1=Button(UI,image=button1,command=seg_by_file)
Button1.place(x=400,y=160,anchor=CENTER)
Button2=Button(UI,image=button2,command=seg_by_sentence)
Button2.place(x=400,y=240,anchor=CENTER)
Button3=Button(UI,image=button3,command=add_word)
Button3.place(x=400,y=320,anchor=CENTER)
Button4=Button(UI,image=button4,command=Copyright)
Button4.place(x=400,y=480,anchor=CENTER)
Button5=Button(UI,image=button5,command=UI.destroy)
Button5.place(x=400,y=560,anchor=CENTER)
menubar=Menu(UI)
filemenu=Menu(menubar,tearoff=0)
filemenu.add_command(label="Open", command=Open)
filemenu.add_command(label="Get path", command=Get_path)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=UI.destroy)
lexiconmenu=Menu(menubar,tearoff=0)
lexiconmenu.add_command(label="Add new word", command=add_word)
lexiconmenu.add_command(label="Add general service word",command=add_general_service_word)
lexiconmenu.add_command(label="Search",command=Search_word)
segmentationmenu=Menu(menubar,tearoff=0)
segmentationmenu.add_command(label='Segmentation to a file',command=seg_by_file)
segmentationmenu.add_command(label='Segmentation to sentences',command=seg_by_sentence)
helpmenu=Menu(menubar,tearoff=0)
helpmenu.add_command(label='Copyright information',command=Copyright)
helpmenu.add_command(label='Manual',command=manual)
menubar.add_cascade(label='File',menu=filemenu)
menubar.add_cascade(label='Lexicon',menu=lexiconmenu)
menubar.add_cascade(label='Segmentation',menu=segmentationmenu)
menubar.add_cascade(label='Help',menu=helpmenu)
UI['menu']=menubar
UI.mainloop()


