import flet as ft
from flet import View
import sqlite3
import datetime
import os
import base64
import translate
from translate import Translator
import time
#Database Connection

db = sqlite3.connect('Apkupcase.db',check_same_thread=False)
cursor = db.cursor()

#Test connection
try:
    if sqlite3.Connection:
        print("Connected")
        print("*"*10)
        cursor.execute("SELECT * FROM item")
        print("Release list of table")
        for obj in cursor.fetchall():
            print(obj[0])
        print("Command in process")
        print("*"*10)
        db.commit()
    else:
        print("Not connected yet")
except sqlite3.Error as error:
    print(error)

class Task(ft.Column):
    
    def __init__(self, name_task, delete_task):
        super().__init__()
        self.name_task = name_task
        self.delete_task = delete_task
        self.Task_value =ft.Text(value=self.name_task,color="white")
        self.edit_task = ft.TextField(width=150,height=40,border_color="white")
        self.display_task =  ft.Container(
                ft.Row(
                    controls=[
                            ft.Checkbox(check_color="white"),
                            ft.Container(
                                self.Task_value,
                                width=150,
                                height=20
                            ),
                            ft.IconButton(ft.icons.DELETE,icon_color="red",on_click=self.Deletete_clicked),
                            ft.IconButton(ft.icons.EDIT,icon_color="blue", on_click=self.Edit_task)
                        ]
                    ),
                padding=ft.padding.only(left=10),
                width=400,
                height=50,
                border=ft.border.all(1,"orange"),
                bgcolor="orange"
            )
        self.EditView = ft.Container(
            ft.Row(
                controls=[
                    self.edit_task,
                    ft.IconButton(ft.icons.DONE, on_click=self.Save_changed)
                ]
            ),
            padding=ft.padding.only(left=10),
            width=400,
            height=50,
            border=ft.border.all(1,"orange"),
            bgcolor="orange",
            visible=False
            
        )
        self.controls = [self.display_task, self.EditView]
    
    def Deletete_clicked(self, e):
        Del_tsk = f'''DELETE FROM item WHERE name = '{self.Task_value.value}' '''
        try:
            cursor.execute(Del_tsk)
            print("item deleted")
            db.commit()
        except sqlite3.Error as error:
            print(error)
        self.delete_task(self)

    def Edit_task(self,e):
        self.display_task.visible = False
        self.EditView.visible = True
        self.update()


    def Save_changed(self, e):
        Save_tsk = f'''UPDATE item SET name = '{self.edit_task.value}' WHERE name = '{self.Task_value.value}' '''
        self.Task_value.value = self.edit_task.value
        try:
            cursor.execute(Save_tsk)
            print("Task updated ")
            db.commit()
        except sqlite3.Error as error:
            print(error)
        self.display_task.visible = True
        self.EditView.visible = False
        self.update()

class Note(ft.Column):
    def __init__(self,Title,Text,Delete):
        super().__init__()
        self.title = Title
        self.Text = Text
        self.Delete = Delete
        self.Language = ft.TextField(width=100,border_color="white",color="white",text_size=15,height=50,border_radius=20)
        self.Translator = ft.TextField(width=100,border_color="white",color="white",text_size=15,height=50,border_radius=20)
        self.Progress = ft.Column(
            [
                ft.Text("Translating...",size=10,color="white"),
                ft.ProgressBar(width=200),
            ],
            visible=False
        )

        self.Translated = ft.Column(
            width=500,
            scroll=ft.ScrollMode.HIDDEN,
            visible=False
        )


        self.Display_title = ft.Text(value=self.title, color="white", size=20,weight="bold")
        self.Display_text = ft.Text(value=self.Text,color="white",size=15)
        self.Edit_text = ft.TextField(value=self.Display_text.value,border_color="grey",
                                      color="white",text_size=15,multiline=True)
        self.Searchitem = ft.TextField(width=300,height=50,border_radius=30,prefix_icon=ft.icons.SEARCH,
                                        text_size=15,border_color="white",on_change=self.Result_search)
        self.Textline = ft.Container(
            ft.Column(
                [
                    self.Display_text,
                
                ],
                height=400,
                scroll=ft.ScrollMode.HIDDEN,
            ),
            
            height=300,
            width=400,
            bgcolor="Grey",
            padding=20,
            
            
        )
        self.Edit_Textline = ft.Container(
            ft.Column(
                [
                    self.Edit_text
                ],
                width=400,
                height=300,
                scroll=ft.ScrollMode.HIDDEN,
            ),
            
            height=300,
            width=400,
            bgcolor="Grey",
            padding=15,
            border = ft.border.BorderSide(1,"grey"),
            border_radius=15
            
        )





        self.Display_Note = ft.Container(
            ft.Column(
                [
                    self.Display_title,
                    self.Textline,
                    ft.Row(
                        [
                            ft.ElevatedButton("Delete",bgcolor="red",color="white",on_click=self.Delete_note),
                            ft.ElevatedButton("Edit",bgcolor="Blue",color="white",on_click=self.Edit_Note),
                            ft.ElevatedButton("Keyword",bgcolor="lightblue",color="white",on_click=self.keyword_Note)
                        ]
                    )
                ]
            ),
            
            width=350,
            bgcolor="orange",
            padding=20,
            height=450,
            border = ft.border.BorderSide(1,"grey"),
            border_radius=15
            
        )

        self.Edit_Note_text = ft.Container(
            ft.Column(
                [
                    self.Display_title,
                    self.Edit_Textline,
                    ft.Row(
                        [
                            ft.ElevatedButton("Delete",bgcolor="red",color="white",on_click=self.Delete_note),
                            ft.ElevatedButton("Save",bgcolor="Green",color="white",on_click=self.Save_Note)
                        ]
                    )
                ]
            ),
            
            width=350,
            bgcolor="orange",
            padding=20,
            height=450,
            visible=False,
            border = ft.border.BorderSide(1,"grey"),
            border_radius=15
        )
        self.Keyword_Search = ft.Container(
            ft.Column(
                [
                    self.Display_title,
                    self.Edit_Textline,
                    ft.Column(
                        [
                            self.Searchitem,
                            ft.ElevatedButton("Trans",color="white",bgcolor="grey",on_click=self.Keyword_trans,
                                                      icon=ft.icons.TRANSLATE,icon_color="white"),
                            ft.Row(
                                [   ft.Text("From: ",size=15,color="white"),       
                                    self.Language,
                                    ft.Text("To: ",size=15,color="white"),
                                    self.Translator
                                ]
                            ),
                            self.Progress,
                            self.Translated,
                            ft.Container(
                                ft.Row(
                                    [
                                        ft.ElevatedButton('Back',color="white",bgcolor="black",on_click=self.Back_event_keyword),
                                    ],
                                    alignment=ft.MainAxisAlignment.END
                                ),
                                margin=ft.margin.only(top=20)
                            )

                        ],
                        width=500,
                        scroll=ft.ScrollMode.HIDDEN
                        
                    )
                    
                ],
                scroll=ft.ScrollMode.HIDDEN
                
               
            ),
            
            width=450,
            bgcolor="orange",
            padding=20,
            height=600,
            visible=False,
            border = ft.border.BorderSide(1,"grey"),
            border_radius=15,
        )
        

        self.controls = [self.Display_Note, self.Edit_Note_text, self.Keyword_Search]

    def Delete_note(self, e):
        
        Remove_Note = f''' DELETE FROM note WHERE title = '{self.Display_title.value}' '''
        try:
            cursor.execute(Remove_Note)
            print("Note Removed")
            db.commit()
        except sqlite3.Error as error:
            print(error)
        self.Delete(self)

    def Edit_Note(self, e):
        self.Display_Note.visible = False
        self.Edit_Note_text.visible = True
        self.update()

    def Save_Note(self,e):
        self.Display_text.value = self.Edit_text.value
        self.Display_Note.visible = True
        self.Edit_Note_text.visible = False
        self.update()

    def keyword_Note(self,e):
        self.Display_Note.visible = False
        self.Keyword_Search.visible = True
        self.update()

    def Result_search(self,e):
        
        self.check = ft.Text(ft.TextSpan(ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE)))
        if self.Searchitem.value in self.Display_text.value.lower():
            self.Display_text.color = "red"
            print("Item in Note")
        else:
            print("item does not exist")
        self.update()

    def Keyword_trans(self, e):
        self.loading(e)
        self.Progress.visible=False
        trans = Translator(from_lang=f"{self.Language.value}",to_lang=f"{self.Translator.value}")
        text = trans.translate(str(self.Searchitem.value.strip()))
        self.translated_text = ft.Text(value=text,size=15,color="white") 
        self.Keyword_Search.height=600
        self.Translated.visible = True
        self.Translated.controls.append(
            ft.Column(
                [
                    ft.Text(value=self.Searchitem.value,size=15,color="white",weight="bold"),
                    self.translated_text
                ]
            )
        )
        self.update()

    def loading(self,e):
        self.Progress.visible=True
        self.Keyword_Search.height=600
        time.sleep(3)
        self.update()

    def Back_event_keyword(self, e):
        self.Keyword_Search.visible = False
        self.Display_Note.visible = True
        self.Display_text.color = "white"
        self.update()

    def Back_event_Edit(self, e):
        self.Edit_Note_text.visible = False
        self.Display_Note.visible = True
        self.Display_text.color = "white"
        self.update()
        
        

class SelectionTabs(ft.Column):
    def __init__(self):
        
        super().__init__()
        
        self.Todonoticetext = ft.Text("You have 0 Task to finish",color="white",weight="bold")
        #Todo item count
        cursor.execute("SELECT COUNT(*) FROM item")
        for obj in cursor.fetchall():
            self.Todonoticetext.value = f"You have {obj[0]} Tasks to finish"
        self.TodoNotice = ft.Container(
            ft.Row(
                [
                    ft.Icon(name=ft.icons.BOOK,color="white"),
                    self.Todonoticetext
                ]
            ),
            padding=20,
            width=400,
            height=70,
            bgcolor="black",
            border_radius=20
        )

        #Schedule Notice
        self.ScheduleNotice = ft.Container(
            ft.Row(
                [
                    ft.Icon(name=ft.icons.CALENDAR_MONTH,color="white"),
                    ft.Text(f"On Schedule today {datetime.date.today()}",weight="bold",color="white")
                ]
            ),
            padding=20,
            width=400,
            height=70,
            bgcolor="black",
            border_radius=20
        )
        
        #Chat AI Notice
        self.ChatAINotice = ft.Container(
            ft.Row(
                [
                    ft.Icon(name=ft.icons.CHAT,color="white"),
                    ft.Text(f"Coming soon ...",color="white",weight="bold")
                ]
            ),
            padding=20,
            width=400,
            height=70,
            bgcolor="black",
            border_radius=20
        )





        self.item = ft.Column(
            [
               
            ],
            scroll=ft.ScrollMode.HIDDEN,
            width=300,
            height=300,
        )
        cursor.execute("SELECT * FROM item")
        for obj in cursor.fetchall():
            self.item.controls.append(
                ft.Container(
                    ft.Row(
                        [
                            ft.Icon(name=ft.icons.BOOK,color="white"),
                            ft.Text(value=obj[0],color="white",weight="bold")
                        ]
                    ),
                    padding=20,
                    width=400,
                    height=70,
                    bgcolor="black",
                    border_radius=20
                )
            )
        
        self.tabs_1 = ft.Container(
            ft.Column(
                [
                    ft.Text("Home",size=30,color="white"),
                    self.TodoNotice,
                    self.ScheduleNotice,
                    self.ChatAINotice,
                ],
                scroll=ft.ScrollMode.HIDDEN
            ),
            visible=True
        )
        
        self.tabs_2 = ft.Container(
            ft.Column(
                [
                    ft.Text("List of items",color="white"),
                    self.item
                ]
            ),
            
        )
        self.tabs_3 = ft.Container(
            ft.Column(
                [
                    ft.Text("Schedule",size=30,color="white"),
                    ft.Text(value = f"today {datetime.date.today()}",color="white",italic=True)
                ],
                scroll=ft.ScrollMode.HIDDEN
            ),
            visible=True
        )
        self.tabs_4 = ft.Container(
            ft.Column(
                [
                    ft.Text("Chat AI",size=30,color="white"),
                    ft.Text("Coming Soon",color="white",italic=True)
                ],
                scroll=ft.ScrollMode.HIDDEN
            ),
            visible=True
        
        )

        self.Tabselection = ft.Tabs(
            selected_index=0,
            animation_duration=500,
            tabs=[
                ft.Tab(
                    text="Home",
                    icon="Home",
                    content=self.tabs_1
                ),
                ft.Tab(
                    text="to do",
                    icon="Book",
                    content=self.tabs_2
                ),
                ft.Tab(
                    text="Schedule",
                    icon="Schedule",
                    content=self.tabs_3
                ),
                ft.Tab(
                    text="ChatAI",
                    icon=ft.icons.CHAT,
                    content=self.tabs_4
                ),
                
            ],
            expand=1,
            label_color=ft.colors.WHITE,
            divider_color="orange",
            scrollable=True,
            indicator_color="white",
            unselected_label_color=ft.colors.WHITE 
        )
        self.controls = [self.Tabselection]
   
class NotedApp(ft.Column):
    def __init__(self):
        super().__init__()
        
        



        self.Note_title = ft.TextField(width=400,border_color="white",hint_text="Tittle...")
        self.Note_textField = ft.TextField(value="\n\n",width=400,border_color="white",hint_text="TextLine...",
                                           multiline=True,min_lines=1,max_lines=4)
        self.Note_list = ft.Column(
            [],
            height=600,
            scroll=ft.ScrollMode.HIDDEN
        )

        self.OpenNoteBar = ft.Container(width=100,height=10,bgcolor="grey",on_click=self.Note_TopBar_Open,visible=True)
        self.CloseNoteBar = ft.Container(width=100,height=10,bgcolor="grey",on_click=self.Note_TopBar_close,visible=False)



        cursor.execute("SELECT * FROM note")
        for obj in cursor.fetchall():
            title = obj[0]
            Notedtext = obj[1]
            self.Note_list.controls.append(
                Note(title,Notedtext,self.Delete_note)
            )
        self.NoteBar = ft.Container(
                ft.Column(
                    [
                        ft.Row(
                            [
                                ft.IconButton(ft.icons.MENU,icon_color="white",on_click= None),
                                ft.Text("UpCase",color="white",size=25,weight="bold"),
                                ft.IconButton(ft.icons.SEARCH,icon_color="white")
                                
                            ],
                            alignment="spaceBetween",
                        ),
                        self.Note_title,
                        self.Note_textField,
                        ft.Row(
                            [
                                ft.FloatingActionButton(
                                    icon=ft.icons.ADD, on_click=self.Add_note
                                ),
                                ft.FloatingActionButton(
                                    icon=ft.icons.DELETE, on_click=self.Clear_Field
                                ),
                                ft.FloatingActionButton(
                                    icon=ft.icons.LINE_WEIGHT, on_click=None
                                ),
                                ft.FloatingActionButton(
                                    icon=ft.icons.UPLOAD_FILE, on_click=None
                                ),
                                ft.FloatingActionButton(
                                    icon=ft.icons.INSTALL_MOBILE, on_click=None
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        
                    ]
                ),
                border_radius=ft.border_radius.vertical(
                bottom=25
            ),
            bgcolor="Orange",
            width=400,
            height=60,
            padding=10,
            shadow= ft.BoxShadow(
                blur_radius=3,
                color="black",
                blur_style=ft.ShadowBlurStyle.OUTER
            ),
            animate=ft.animation.Animation(1000, ft.AnimationCurve.BOUNCE_OUT),  
        )

        self.controls = [
            self.NoteBar,
            ft.Row(
                [
                    self.OpenNoteBar,
                    self.CloseNoteBar
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            self.Note_list,
            
            
        ]

    def Add_note(self, e):
        note = Note(self.Note_title.value,self.Note_textField.value, self.Delete_note)
        
        index_tub = [self.Note_title.value, self.Note_textField.value]
        Query_index = '''INSERT INTO note (title, textiled) VALUES (?,?)'''
        try:
            cursor.execute(Query_index,index_tub)
            print("New Note Added")
            db.commit()
        except sqlite3.Error as error:
            print(error)
        
        self.Note_list.controls.append(note)
        self.Note_textField.value = "\n\n\n"
        self.update()

    def Delete_note(self, note):
        self.Note_list.controls.remove(note)
        self.update()

    def Clear_Field(self, e):
        self.Note_title.value = ""
        self.Note_textField.value = "\n\n\n"
        self.update()

    def Note_TopBar_Open(self, e):
        self.OpenNoteBar.visible = False
        self.CloseNoteBar.visible = True
        self.NoteBar.height = 350 if self.NoteBar.height == 60 else 60
        self.update()

    def Note_TopBar_close(self, e):
        self.OpenNoteBar.visible = True
        self.CloseNoteBar.visible = False
        self.NoteBar.height = 60 if self.NoteBar.height == 350 else 350
        self.update()
        

class TodoApp(ft.Column):

    def __init__(self):
        super().__init__()
        
        self.List_task = []
        self.item_task = ft.Text(color="white",visible=False)
        
        self.Task_Field = ft.TextField(width=250,border_color="white",hint_text="Task...",
                              hint_style=ft.TextStyle(color="grey"),color="white")
        self.Todo_list = ft.Column(
            [
                
            ],
            scroll=ft.ScrollMode.HIDDEN,
            height=400,
            width=400,
        )
        cursor.execute("SELECT * FROM item")
        for obj in cursor.fetchall():
            tsk = Task(obj[0], self.Delete)
            self.Todo_list.controls.append(tsk)
            self.List_task.append(tsk)



        self.item_list = ft.Column(
            [
                
            ],
            scroll=ft.ScrollMode.HIDDEN,
            height=400,
            width=400,
            # visible=False
        )
        
        
        self.Checked_list = ft.Column(
            [],
            scroll=ft.ScrollMode.HIDDEN,
            height=400,
            width=400,
        )
        self.count = ft.Text(value=f"You have {len(self.List_task)} task",color="white")
        if len(self.List_task) == 1 or len(self.List_task) == 0:
            self.count.value = f"You have {len(self.List_task)} task"
        else:
            self.count.value = f"You have {len(self.List_task)} tasks"
        self.Status = ft.Tabs(
            selected_index=1,
            animation_duration=500,
            tabs=[
                ft.Tab(
                    text="in Active",
                ),
                ft.Tab(
                    text="Done"
                )
            ],
            indicator_color="white",
            unselected_label_color="grey",
            label_color="white",
            divider_color="black"
        )
        self.controls = [

            ft.Row(
                controls=[
                    self.Task_Field,
                    ft.FloatingActionButton(
                        icon=ft.icons.ADD, on_click=self.add
                    ),
                    
                ]
            ),
            
            self.count,
            self.Status,
            self.Todo_list,
            self.item_list            
        ]

    def Status_Stack(self, e):
        self.update()
        

    def add(self, e):
        task = Task(self.Task_Field.value, self.Delete)
        self.item_task.value = self.Task_Field.value
        self.Todo_list.controls.append(task)
        self.List_task.append(task)
        try:
            item_tub = [self.Task_Field.value]
            Insert = '''
                INSERT INTO item (name) VALUES (?)
            '''
            db.execute(Insert,item_tub)
            print("Item append")
            cursor.execute("SELECT * FROM item")
            print("Release list of table")
            for obj in cursor.fetchall():
                print(obj[0])
            print("Command in process")
            db.commit()
        except Exception as error:
            print(error)

        if len(self.List_task) == 1 or len(self.List_task) == 0:
            self.count.value = f"You have {len(self.List_task)} task"
        else:
            self.count.value = f"You have {len(self.List_task)} tasks"
        print(self.Todo_list.controls)
        self.update()

    def Delete(self, task):

        self.List_task.pop()

        

        if len(self.List_task) == 0:
            self.count.value = f"You have {len(self.List_task)} task"
        else:
            self.count.value = f"You have {len(self.List_task)} tasks"
        self.Todo_list.controls.remove(task)
        self.update()




class Greetingbanner(ft.Column):
    def __init__(self):
        super().__init__()
        self.Search = ft.Container(
            ft.TextField(width=300,height=50,border_color="white",hint_text="Search...",
                hint_style=ft.TextStyle(color="white",size=15),
                text_size=15,border_radius=10,color="white"
            ),
        )
        self.tabs = SelectionTabs()
        self.Menu = ft.IconButton(ft.icons.MENU,icon_color="white",on_click=None,visible=True)
        self.SearchIcon = ft.IconButton(icon="search",icon_color="white",on_click=None,visible=True)
        self.OpenBar = ft.Container(width=100,height=10,bgcolor="grey",on_click=self.Tabs_TopBar,visible=True)
        self.CloseBar = ft.Container(width=100,height=10,bgcolor="grey",on_click=self.Tabs_TopBar_close,visible=False)

        self.Bar = ft.Container(
                ft.Column(
                    [
                        ft.Row(
                            [
                                self.Menu,
                                ft.Text("UpCase",color="white",size=25,weight="bold"),
                                self.SearchIcon
                            ],
                            alignment="spaceBetween",
                        ),
                        ft.Row(
                            [
                                self.Search,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        self.tabs.Tabselection
                        
                    ]
                ),
                border_radius=ft.border_radius.vertical(
                bottom=25
            ),
            bgcolor="Orange",
            width=400,
            height=60,
            padding=10,
            shadow= ft.BoxShadow(
                blur_radius=3,
                color="black",
                blur_style=ft.ShadowBlurStyle.OUTER
            ),
            animate=ft.animation.Animation(1000, ft.AnimationCurve.BOUNCE_OUT),  
        )
        self.controls = [
            self.Bar,
            ft.Row(
                [
                    self.OpenBar,
                    self.CloseBar
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        ]
    def Tabs_TopBar(self, e):
        self.OpenBar.visible = False
        self.CloseBar.visible = True
        self.Bar.height = 500 if self.Bar.height == 60 else 60
        self.update()

    def Tabs_TopBar_close(self, e):
        self.OpenBar.visible = True
        self.CloseBar.visible = False
        self.Bar.height = 60 if self.Bar.height == 500 else 500
        self.update()
    
  
    







        





        


    
    
        

def main(page: ft.Page):
    #--------------- BUILD DATABASE ------------------------- 
    def Display_Profile(e):
        Display_DB_Query = '''
            SELECT name,profession,company,status,birth
            FROM Profile
            WHERE id = 1
        '''
        try:
            cursor.execute(Display_DB_Query)
            print("all record Release")
            for obj in cursor.fetchall():
                Name = obj[0]
                Profession = obj[1]
                Company = obj[2]
                Status = obj[3]
                Birthday = obj[4]
                NameDisplay.value = str(Name)
                professionDisplay.value = str(Profession)
                companyDisplay.value = str(Company)
                statusDisplay.value = str(Status)
                birthDisplay.value = f'{Birthday}'
            print(Birthday)
            db.commit()
        except sqlite3.Error as error:
            print(error)
        page.update()

    
    def Update_Profile(e):
            
        Update_DB_query = f'''
            UPDATE Profile 
            SET  name = '{Nameinput.value}', profession = '{Professioninput.value}',
            company = '{Companyinput.value}', status = '{Statusinput.value}', birth = '{Birthday_select_text.value}'
            WHERE id = 1
        '''
        Insert_DB_query = f'''
            INSERT INTO Profile (id,name,profession,company,status,birth)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        ID = 1
        Query_tube = (ID,str(Nameinput.value),str(Professioninput.value),
                      str(Companyinput.value),str(Statusinput.value),birthDisplay.value)
        try:
            cursor.execute(Update_DB_query)
            print("Command in process")
            Display_Profile(e)
            db.commit()
        except sqlite3.Error as error:
            print(error)
        
        page.update()
    def Display_Edit_Profile(e):
        Display_DB_Query = '''
            SELECT name,profession,company,status,birth
            FROM Profile
            WHERE id = 1
        '''
        try:
            cursor.execute(Display_DB_Query)
            print("all record Release")
            for obj in cursor.fetchall():
                Name = obj[0]
                Profession = obj[1]
                Company = obj[2]
                Status = obj[3]
                Birthday = obj[4]
            Nameinput.value = str(Name)
            Professioninput.value = str(Profession)
            Companyinput.value = str(Company)
            Statusinput.value = str(Status)
            Birthday_select_text.value = f'{Birthday}'
            db.commit()
        except sqlite3.Error as error:
            print(error)
        page.update()

    
    
    #--------------- BUILD FUNCTION ------------------------- 
    #To do Feartures 

    



    #Birthday Selection

    
    def Selected_page(e):
        for index, page_nav in enumerate(page_stack):
            page_nav.visible = True if index == AppBar.selected_index else False
        page.update()

   

    def Birthday_selection(e):
        Birthday_select_text.value = e.control.value.strftime('%Y-%m-%d')
        birthDisplay.value = Birthday_select_text.value
        print(birthDisplay.value)
        page.update()

    #---------------------Notification----------------------

    

    #Set up Date picker Variable    
    DatePickUp = ft.DatePicker(
        first_date=datetime.datetime(1950,1,1),
        last_date=datetime.datetime.now(),
        on_change=Birthday_selection,
        
    )

    #Offset animation
    def ActionNexttoEdit(e):
        Profile.offset = ft.transform.Offset(-2,0)
        EditProfile.offset = ft.transform.Offset(-1.03,0)
        NextAction.visible = False
        BackAction.visible = True
        ChangeSwitched.value = "Edit"
        Profile.update()
        EditProfile.update()
        page.update()

    def ActionBacktoProfile(e):
        Profile.offset = ft.transform.Offset(0,0)
        EditProfile.offset = ft.transform.Offset(2,0)
        NextAction.visible = True
        BackAction.visible = False
        ChangeSwitched.value = "Profile"
        Profile.update()
        EditProfile.update()
        page.update()
    
   
    #--------------- CUSTOMIZE DESIGN VIEW -----------------

    






    '''
        PROFILE PAGE IS THE LAST SELECTION FROM CUPERTINO BAR BELOW
        PROFILE WITH EDIT AND DISPLAY YOUR PERSONAL INFORMATION 
    '''

    #Text Actor 
    NameDisplay = ft.Text("None",color="grey",weight="bold")
    professionDisplay = ft.Text("None",color="grey",weight="bold")
    companyDisplay = ft.Text("None",color="grey",weight="bold")
    statusDisplay = ft.Text("None",color="grey",weight="bold")
    birthDisplay = ft.Text("DD/MM/YY",color="grey",weight="bold")
    
    ChangeSwitched = ft.Text("Profile",size=30,color="white")
    #Animation
    
    #Action button
    NextAction = ft.ElevatedButton("Edit",
        ft.icons.NAVIGATE_NEXT,icon_color="blue"
        ,on_click=ActionNexttoEdit,visible=True,width=385,color="grey"
    )
    BackAction = ft.ElevatedButton(
        "Back",
        ft.icons.NAVIGATE_BEFORE_SHARP,icon_color="blue"
        ,on_click=ActionBacktoProfile,visible=False,width=385,color="grey"
    )

    #Icon
    User = ft.Icon(ft.icons.ACCOUNT_BOX)
    Profession = ft.Icon(ft.icons.LOCAL_ATTRACTION_SHARP)
    company = ft.Icon(ft.icons.HOME)
    status = ft.Icon(ft.icons.VISIBILITY_OUTLINED)
    birth = ft.Icon(ft.icons.CALENDAR_TODAY)
    SaveProfile = ft.ElevatedButton("Save",color="white",bgcolor=ft.colors.GREY_500,on_click=Update_Profile)
    #TextField
    Nameinput = ft.TextField(width=250,height=50,color="grey",bgcolor=ft.colors.GREY_200,border_color=ft.colors.GREY_200)
    Professioninput = ft.TextField(width=250,height=50,color="grey",bgcolor=ft.colors.GREY_200,border_color=ft.colors.GREY_200)
    Companyinput = ft.TextField(width=250,height=50,color="grey",bgcolor=ft.colors.GREY_200,border_color=ft.colors.GREY_200)
    
    Statusinput = ft.Dropdown(
        width=250,
        height=60,
        hint_style=ft.TextStyle(color="grey"),
        hint_text="Choose",
        options=[
            ft.dropdown.Option("On work"),
            ft.dropdown.Option("Offline"),
            
        ],
        filled=True,
        border_color=ft.colors.GREY_200,
        color="grey",
        bgcolor=ft.colors.GREY_200
        
    )
    TimeSelectionButton = ft.IconButton(
        ft.icons.CALENDAR_MONTH,icon_color="white",
        on_click= lambda _: DatePickUp.pick_date()
    ) 
    Time_selection_layout = ft.Container(
        TimeSelectionButton,
        width=50,
        height=54,
        bgcolor="grey",
        margin=ft.margin.only(right=-10)
    )



    Birthday_select_text = ft.TextField(
        hint_text="0/0/0", hint_style=ft.TextStyle(color="grey"),
        width=200,height=55,color="grey",bgcolor=ft.colors.GREY_200,border_color=ft.colors.GREY_200
    )
    def AVT_upload(e: ft.FilePickerResultEvent):
        if e.files and len(e.files):
            try:
                with open(e.files[0].path, 'rb') as r:
                    Editavt.image_src_base64 = base64.b64encode(r.read()).decode('utf-8')
                    Editavt.image_src = str(e.files[0].path)
                    print(e.files[0].path)
            except FileNotFoundError as error:
                print(error)
        page.update()



    AVT_picked = ft.FilePicker(on_result=AVT_upload)
    page.overlay.append(AVT_picked)
    UploadAVT = ft.ElevatedButton("Upload",
                ft.icons.UPLOAD,color="white",bgcolor="grey",
                on_click=lambda _:AVT_picked.pick_files(allow_multiple=False,
                allowed_extensions=['png','jpg']))

    
    #Build Banner
    avt = ft.Container(
        image_src="C:/pen.png",
        bgcolor="grey",
        border=ft.border.BorderSide(5,"black"),
        border_radius=100,
        height=200,
        width=200,
        image_fit=ft.ImageFit.COVER
    )
    Editavt = ft.Container(
        image_src=None,
        bgcolor="grey",
        border=ft.border.BorderSide(5,"black"),
        border_radius=100,
        height=200,
        width=200,
        image_fit=ft.ImageFit.COVER,

    )

    form = ft.Container(
        ft.Column(
            [
                
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Row(
                                    [
                                        User,
                                        NameDisplay
                                    ]
                                ),
                                ft.Row(
                                    [
                                        company,
                                        companyDisplay
                                    ]
                                ),
                                ft.Row(
                                    [
                                        status,
                                        statusDisplay
                                    ]
                                ),
                                ft.Row(
                                    [
                                        birth,
                                        birthDisplay
                                    ]
                                ),
                                ft.Row(
                                    [
                                        Profession,
                                        professionDisplay
                                    ]
                                ),
                                
                            ]
                        )
                    ],
                    
                )
            ]
        ),
        height=250,
        width=300,
        margin=ft.margin.only(left=20),
        padding=ft.padding.only(top=20,left=70),
       
        
    )
    Editform = ft.Container(
        ft.Column(
            [
                ft.Column(
                    [
                        
                        ft.Row(
                            [
                                ft.Column(
                                    [
                                        ft.Text("Name",color="grey",weight="bold"),
                                        Nameinput,
                                        ft.Text("Profession",color="grey",weight="bold"),
                                        Professioninput,
                                        ft.Text("Company",color="grey",weight="bold"),
                                        Companyinput,
                                        ft.Text("Status",color="grey",weight="bold"),
                                        Statusinput,
                                        ft.Text("Birthday",color="grey",weight="bold"),
                                        ft.Row(
                                            [
                                                Time_selection_layout,
                                                Birthday_select_text
                                            ]
                                        )
                                        
                                        
                                    ],
                                    
                                )
                            ],
                            
                        ),
                        
                    ],
                    height=200,
                    scroll=ft.ScrollMode.HIDDEN
                ),
                SaveProfile
            ],
            
        ),
        height=300,
        width=300,
        margin=ft.margin.only(left=20),
        padding=ft.padding.only(top=5,left=30),
        border_radius=20
        
    )
    Profile = ft.Container(
        ft.Column(
            [
                ft.Row(
                    [
                        avt
                    ],
                    alignment= ft.MainAxisAlignment.CENTER
                ),
                form,
                
            ]
        ),
        width=385,        
        height=600,
        bgcolor=ft.colors.GREY_100,
        border_radius=20,
        margin=ft.margin.only(top=10,left=3),
        padding=ft.padding.only(top=40),
        shadow= ft.BoxShadow(
            blur_radius=5,
            color="black",
            blur_style=ft.ShadowBlurStyle.OUTER
        ),
        offset=ft.transform.Offset(0,0),
        animate_offset=ft.animation.Animation(300)
    )

    

    
    EditProfile = ft.Container(
        ft.Column(
            [
                ft.Row(
                    [
                        Editavt
                    ],
                    alignment= ft.MainAxisAlignment.CENTER
                ),
                ft.Row(
                    [
                        UploadAVT
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
              
                Editform
                
            ]
        ),
        width=385,
        height=600,
        bgcolor=ft.colors.GREY_100,
        border_radius=20,
        margin=ft.margin.only(top=10,left=3),
        padding=ft.padding.only(top=40),
        shadow= ft.BoxShadow(
            blur_radius=5,
            color="black",
            blur_style=ft.ShadowBlurStyle.OUTER
        ),
        offset=ft.transform.Offset(2,0),
        animate_offset=ft.animation.Animation(300)
    )
        
    
    ActionEvent = ft.Container(
        ft.Row(
            [
                
                NextAction,
                BackAction
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        # width=600
    )
    
    #-----------------------------------
    '''
        TO DO FEATURE IN UPCASE WITH HELP BEING SCHEDULED ALL 
        TASKS TO DO AND PLANS
    '''

   
    #-----------------------------------
    '''
        HOMEPAGE IN UPCASE WITH ALL UTITLITIES
        INITIAL VIEW FROM CUPERTINOBAR ROUTE BELOW (HOME)
    '''
    #UTILITIES

    #AI Tools
    AI_image = ft.Container(
        image_src="https://img.freepik.com/premium-photo/digital-world-online-shopping-via-phone-pink-phone-pink-background-ai-generated_744422-7299.jpg",
        height=150,
        width=230,
        border_radius=20,
        bgcolor="white",
        image_fit= ft.ImageFit.FILL
    )
    AI_utility = ft.Container(
        ft.Column(
            [
                AI_image,
                ft.Row(
                    [
                        ft.Text("AI Supporting",color="grey")
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
            ]
        ),
        height=250,
        width=250,
        border_radius=20,
        bgcolor="white",
        padding= ft.padding.only(left=10,top=10),
        margin=ft.margin.only(left=3),
        shadow= ft.BoxShadow(
            blur_radius=3,
            color="black",
            blur_style=ft.ShadowBlurStyle.OUTER
        )
    )
   
    #ToDo Feature
    ToDo_image = ft.Container(
        image_src="https://i.pinimg.com/736x/30/47/d7/3047d747871c7b5421137d644b7dbf04.jpg",
        height=150,
        width=230,
        border_radius=20,
        bgcolor=ft.colors.GREY_100,
        image_fit= ft.ImageFit.COVER
    )
    ToDo_utility = ft.Container(
        ft.Column(
            [
                ToDo_image,
                ft.Row(
                    [
                        ft.Text("ToDo List",color="grey")
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
            ]
        ),
        height=250,
        width=250,
        border_radius=20,
        bgcolor="white",
        padding= ft.padding.only(left=10,top=10),
        shadow= ft.BoxShadow(
            blur_radius=3,
            color="black",
            blur_style=ft.ShadowBlurStyle.OUTER
        ),
        on_click= lambda _:page.go("/Todo")
        
    )
    #Note and Line up
    Note_image = ft.Container(
        image_src="https://c0.wallpaperflare.com/preview/356/153/277/adult-businessman-composition-desk.jpg",
        height=150,
        width=230,
        border_radius=20,
        bgcolor=ft.colors.GREY_100,
        image_fit= ft.ImageFit.COVER
    )

    Note_utility = ft.Container(
        ft.Column(
            [
                Note_image,
                ft.Row(
                    [
                        ft.Text("Note & Line",color="grey")
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
            ]
        ),
        height=250,
        width=250,
        border_radius=20,
        bgcolor="white",
        padding= ft.padding.only(left=10,top=10),
        
        shadow= ft.BoxShadow(
            blur_radius=3,
            color="black",
            blur_style=ft.ShadowBlurStyle.OUTER
        ),
        on_click= lambda _:page.go("/Note")
    )





    Header_main = ft.Container(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Utilities",color=ft.colors.WHITE,weight="bold",size=20)
                    ],
                    alignment=ft.MainAxisAlignment.START
                ),
                ft.Row(
                    [
                        AI_utility,
                        ToDo_utility,
                        Note_utility
                        
                    ],
                    scroll=ft.ScrollMode.ALWAYS,
                    
                    height=300
                )
            ]
        ),
        width=400,
        height=350,
        margin=ft.margin.only(top=10),
        # padding=5
        
       
    )




    #Schedule
    ScheduleTabs = ft.Tabs(
        selected_index=1,
        animation_duration=500,
        tabs=[
            ft.Tab(
                text="Monday",
                
            ),
            ft.Tab(
                text="Tuesday",
                
            ),
            ft.Tab(
                text="Wednesday",
                
            ),
            ft.Tab(
                text="Thursday",
                
            ),
            ft.Tab(
                text="Friday",
                
            ),
            ft.Tab(
                text="Saturday",
                
            ),
            ft.Tab(
                text="Sunday",
                
            )
        ],
        label_color=ft.colors.BLACK,
        divider_color=ft.colors.GREY,
        scrollable=True,
        indicator_color="grey",
        unselected_label_color="grey",
         
    )
    Schedule = ft.Container(
        ft.Column(
            [
                ScheduleTabs,
            ]
        ),
        height=300,
        width=400,
        bgcolor="white",
        shadow= ft.BoxShadow(
            blur_radius=3,
            color="black",
            blur_style=ft.ShadowBlurStyle.OUTER
        ),
        border_radius=20,
        padding=10

    )
    #Body main
    Body_main = ft.Container(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Schedule",color=ft.colors.WHITE,weight="bold",size=20)
                    ],
                    alignment=ft.MainAxisAlignment.START
                ),
                Schedule
            ]
        ),
        width=400,
        height=350,
        padding=5,
        
        
       
    )
    
    
    page_1 = ft.Container(
        ft.Column(
            [
                
                Header_main,
                Body_main
                
            ],
            
            scroll=ft.ScrollMode.HIDDEN
        ),
        visible=True
    )
    
    page_2 = ft.Container(
        ft.Column(
            [                
                TodoApp()
            ],
            height=500
        ),
        visible=False
    )
    
    page_3 = ft.Container(
        ft.Column(
            [
                ft.Text("Help",size=30,color="white")
            ]
        ),
        visible=False
    )
    page_4 = ft.Container(
        ft.Column(
            [
                
                ft.Row(
                    controls=[
                        Profile,
                        EditProfile,
                        
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Row(
                    [
                        ActionEvent,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            
            scroll=None
        ),
        visible=False,
        
       
    )
    #Set up Page List and Loop


    #Set up Todo Notification
    
    
   
    #Build up Page list
   
    page_stack = [
        page_1,
        page_2,
        page_3,
        page_4
    ]
    

    #Custom Tabs
   


    #APP'S NAVIGATION
    #Type CupertinoNavigationBar
    AppBar = ft.CupertinoNavigationBar(
        selected_index=0,
        on_change=Selected_page,
        bgcolor=ft.colors.BLACK,
        inactive_color=ft.colors.GREY,
        active_color=ft.colors.ORANGE,
        destinations=[
            ft.NavigationDestination(icon=ft.icons.HOME, label="Home"),
            ft.NavigationDestination(icon=ft.icons.LIST, label="TODO"),
            ft.NavigationDestination(icon=ft.icons.HELP, label="Help"),
            ft.NavigationDestination(icon=ft.icons.ACCOUNT_BOX, label="Profile"),

        ],
        
        
    )

    
    #-----------------------------------------------------------------------
    page.overlay.append(DatePickUp)
    
    
    def route_change(e):
        page.views.clear
        page.views.append(
            View(
                "/HOME",
                [
                    Greetingbanner(),
                    AppBar,
                    ft.Column(page_stack,scroll=True, expand=True)
                ],
                Display_Profile(e),
                Display_Edit_Profile(e),
                bgcolor="Black"
            )
        )
        if page.route == "/Todo":
            page.views.append(
                View(
                    "/Todo",
                    [
                        ft.Row(
                            [
                                ft.IconButton(ft.icons.ARROW_BACK,on_click= lambda _:page.go("/HOME"))

                            ]
                        ),
                        TodoApp()
                    ],
                    
                    Display_Profile(e),
                    Display_Edit_Profile(e),
                    bgcolor="Black",
                    
                ),
                
            )
        elif page.route == "/Note":
            page.views.append(
                View(
                    "/Note",
                    [
                        NotedApp(),
                        
                    ]
                )
            )

        page.update()
    def view_pop(View):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route, skip_route_change_event=True)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


    page.window_width = 380
    page.window_resizable = False
    page.on_resize = True
    page.update()

if __name__ == "__main__":
    ft.app(target=main,assets_dir='assets')