import PySimpleGUI as sg
import os
font = ("Arial", 30)
def choose_language_view():
    layout=[[sg.Text("Choose your language")],
            [sg.Text("          ")],
            [sg.Text("          "),sg.Button("Hindi"),
             sg.Text("          "),sg.Button("Bangla"),
             sg.Text("          "),sg.Button("Kannada"),sg.Text("          ")],
            [sg.Button("Exit")]]
    return sg.Window(title="Language",layout=layout,font=font,element_justification='center')

def choose_task_view():
    layout=[[sg.Text("Choose your task")],
            [sg.Text("          ")],
            [sg.Text("          "),sg.Button("Search",),sg.Text("          "),sg.Button("Annotate"),sg.Text("          ")],
            [sg.Text("          ")],
            [sg.Button("Back"),sg.Text("     "),sg.Button("Exit")],
            [sg.Text("          ")]]
    return sg.Window(title="Task",layout=layout,font=font,element_justification='center')

def choose_file_for_annotation_view():
    layout=[[sg.Text("          ")],
            [sg.Text("Choose a file: "), sg.Input(), sg.FileBrowse(key="-IN-")],[sg.Button("Submit")],
            [sg.Button("Back"),sg.Text("     "),sg.Button("Exit")]]
    return sg.Window(title="Annotate",layout=layout,font=font,element_justification='center')

# [sg.Column(all_listbox, size=(440, 200), pad=(0, 0),scrollable=True,
#          vertical_scroll_only=True,key='test')]
def choose_search_term_view(lines,key=None):
    if key is not None:
        lines = [line for line in lines if key in line]
        layout = [[sg.Text("          ")],
                  [sg.Text("What do you want to search: "), sg.Input(key="-SEARCH-"), sg.Button("Submit")]]+\
                 [[sg.Column([[sg.Text(line)] for line in lines],scrollable=True,vertical_scroll_only=True,size=(700,200))]]+\
                 [[sg.Text("          ")]]
    else:
        layout=[[sg.Text("          ")],
                [sg.Text("What do you want to search: "), sg.Input(key="-SEARCH-"), sg.Button("Submit")]]+\
               [[sg.Text("          ")]]
    return sg.Window(title="Search", layout=layout,font=font,element_justification='center')

def annotation_view(filename,terms_list):
    lines=[line for line in open(filename).readlines()]
    for i,line in enumerate(lines):
        for term in terms_list:
            lines[i]=lines[i].replace(term,"_".join(term.split()))
    for i,term in enumerate(terms):
        terms[i]="_".join(terms[i].split())
    lines=[line.split() for line in lines]
    lines=[[(word.split("/")[0],word.split("/")[1] if "/" in word else None) for word in line] for line in lines]
    layout = [[[sg.Text(word[0])] if word[0] not in terms_list else [sg.Text(word[0]+" / "),sg.DropDown(["Nominal","Relational","Modifier"],default_value=word[1],key=str(i)+"-"+str(j)+"/"+word[0])] for j,word in enumerate(line)] for i,line in enumerate(lines)]
    layout = [[sg.Column([[value for values in line for value in values] for line in layout],scrollable=True,vertical_scroll_only=True,size=(800,300))]]
    layout = layout+[[sg.Button("Save File")],[sg.Text("Add a new term:"),sg.In(key="new_term")]]+[[sg.Button("Add Term")]]
    return sg.Window(title="Annotate",layout=layout,size=(900,500),font=font)

def create_output_file(filename,values):
    lines = [line.split() for line in open(filename).readlines()]
    lines = [[(word.split("/")[0], word.split("/")[1] if "/" in word else None) for word in line] for line in lines]
    output_filename=filename.replace("_annotated.txt","")+"_annotated.txt"

    fp=open(output_filename,"w")
    for i,line in enumerate(lines):
        s=[]
        for j,word in enumerate(line):
            word,tag=word
            key=str(i)+"-"+str(j)+"/"+word
            if key in values and values[key]!="":
                s.append(word+"/"+values[key])
            else:
                s.append(word)
        fp.write(" ".join(s)+"\n")
    fp.close()
    return





language,terms,filename=None,None,None
view="Home"
while True:
    if view=="Home":
        window=choose_language_view()
        event,values=window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif event!="":
            terms=list(map(lambda x:x.strip(),open(event+"_terms.txt").readlines()))
            language=event
            view="Task"
            window.close()
    elif view=="Task":
        window=choose_task_view()
        event,values=window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif event == "Back":
            view="Home"
            window.close()
        elif event!="":
            view=event
            window.close()
    elif view=="Search":
        filenames=[file for file in os.listdir("corpus/"+language+"/") if file.endswith(".txt")]
        lines=[line.strip() for file in filenames for line in open("corpus/"+language+"/"+file).readlines()]
        search=None
        while True:
            window=choose_search_term_view(lines,key=search)
            event,values=window.read()
            if event == sg.WIN_CLOSED or event=="Exit":
                view="Task"
                window.close()
                break
            elif event == "Back":
                view = "Home"
                window.close()
            elif event=="Submit":
                search=values["-SEARCH-"]
                window.close()
    elif view=="Annotate":
        window=choose_file_for_annotation_view()
        event,values=window.read()
        if event == sg.WIN_CLOSED:
            view="Task"
            window.close()
        elif event=="Submit":
            filename=values["-IN-"]
            view="Annotate2"
            window.close()
    elif view=="Annotate2":
        window=annotation_view(filename,terms)
        event,values=window.read()
        if event == sg.WIN_CLOSED:
            view="Annotate"
            window.close()
        elif event=="Add Term" and values["new_term"]!="":
            terms.append(values["new_term"])
            window.close()
        elif event=="Save File":
            create_output_file(filename,values)
            window.close()
            view="Task"
window.close()




