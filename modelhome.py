'''
Agent model GUI front-end.

Filename: modelhome.py 

Contains: 
- Classes: FrontEnd
- Methods: run, helper, about, finish, sel_no, sel_yes and unchecked.
'''
import tkinter as tk
import subprocess


class FrontEnd():
    '''
    Setup of Agents Model GUI home page
    
    Calls modelmain.py with any parameters entered.
    
    Data entry fields:
        - Number of Agents
            (optional, integer, > 0)
        - Use default start locations (up to first 100 Agents)
            (optional, check button, translated to single byte text,
             default=off)
        - Number of moves for each Agent (applied to every Agent )
            (optional, integer, > 0)
        - Neighbourhood Distance (euclidean)
            (optional, integer, > 0)
        - Plot starting location
            (optional, radio button translated to single byte text)
        - Display summary data
            (optional, 3 x check buttons, each translated to single byte text,
             each default=off)
            
        All parameters, if entered are passed as arguments into modelmain.py
        and validated there.
        
    Buttons:
        - Run 
            (Transfers control to modelmain.py with data entry fiels as
             arguments, if entered or selected)
        - Reset
            (Reset input fields)
        - Exit
            (Terminate application)
            
    Display field
        - Run information
            (Displays any information (help, validation errosr etc) returned
             from modelmain.py or the command prompt)

    Menu bar 
        - File > Run 
            (Transfers control to modelmain.py with data entry fiels as
             arguments, if entered)
        - File > Reset
            (Reset fields)
        - File > Exit
            (Terminate application)
        - Defaults > Create (Not active in v1.0)
            (Creates a random start locations for the first 100 Agents)
        - Defaults > View (Not active in v1.0)
            (Displays the start locations for the first 100 Agents)
        - Help > Input
            (Displays information generated from modelmain.py -h)
        - Help > About
            (Displays generation information of the Agents model)
    '''
    def __init__(self, home):
        '''
        Initialisation of the application GUI front end with:
            - Variable
            - 3 x Entry field
            - 1 x Set Radio buttons (contains 2)
            - 4 x Check buttons
            - 3 x Buttons
            - 1 x Text field (read only)
            - Menu bar (with cascading items)
        '''
        #-------------------------------------------------
        # Create GUI page
        #-------------------------------------------------
        self.home = home
        
        # Fields for Radio and Check buttons
        self.plot_start = tk.StringVar()
        self.agent_defaults = tk.StringVar()
        self.disp_agent_summary = tk.StringVar()
        self.disp_wolf_summary = tk.StringVar()
        self.disp_params = tk.StringVar()
        
        # Other general field before we start contructing the layout
        menu_bar = tk.Menu(self.home)
        self.home.config(menu=menu_bar)
        self.home.geometry('950x700')
        self.home.wm_title('Agents - Student 201388212')
        
        #-------------------------------------------------
        # Setup Keyboard shortcuts that can be used
        # irrespective  of where the cursor is located
        #-------------------------------------------------
        home.bind('<Alt-r>', self.run)
        home.bind('<Alt-x>', self.finish)
        home.bind('<Alt-s>', self.clear)
        
        #-------------------------------------------------
        # Set up Menu Bar and cascading options.
        #-------------------------------------------------
        menu_item_1 = tk.Menu(menu_bar, tearoff=0)
        menu_item_2 = tk.Menu(menu_bar, tearoff=1)
        menu_item_3 = tk.Menu(menu_bar, tearoff=2)

        menu_bar.add_cascade(label='File', menu=menu_item_1)
        menu_bar.add_cascade(label='Defaults', menu=menu_item_2)
        menu_bar.add_cascade(label='Help', menu=menu_item_3)
       
        menu_item_1.add_command(label='Run...', command=self.run, underline=0)
        menu_item_1.add_command(label='Reset', command=self.clear, underline=2)
        menu_item_1.add_command(label='Exit', command=self.finish, underline=1)
        menu_item_2.add_command(label='Create...', state=tk.DISABLED)
        menu_item_2.add_command(label='View...', state=tk.DISABLED)
        menu_item_3.add_command(label='Inputs...', command=self.helper)
        menu_item_3.add_command(label='About...', command=self.about)
        
        #-------------------------------------------------
        # Set up frames for individual screen fields
        #-------------------------------------------------
        frame1 = tk.Frame(self.home)
        frame1.pack(fill=tk.X, expand=False, padx=30, pady=20)
        
        frame2 = tk.Frame(self.home)
        frame2.pack(fill=tk.X, expand=False, padx=30, pady=20)
        
        frame3 = tk.Frame(self.home)
        frame3.pack(fill=tk.X, expand=False, padx=30, pady=20)
        
        frame4 = tk.Frame(self.home)
        frame4.pack(fill=tk.X, expand=False, padx=30, pady=20)
        
        frame5 = tk.Frame(self.home)
        frame5.pack(fill=tk.X, expand=False, padx=30, pady=20)
        
        frame6 = tk.Frame(self.home)
        frame6.pack(fill=tk.X, expand=False, padx=30, pady=20)
        
        frame7 = tk.Frame(self.home)
        frame7.pack(fill=tk.X, expand=False, padx=30, pady=20)
        
        frame8 = tk.Frame(self.home)
        frame8.pack(fill=tk.X, expand=False, padx=30, pady=20)
        
        #-------------------------------------------------
        # Set up screen fields.  There are:
        # 3 x Entry fieds
        # 1 x Radio button set (2)
        # 4 x Check buttons
        # 2 x Buttons
        # 1 x Scrollable text box (This will be protected) 
        #-------------------------------------------------
        
        # Frame 1
        l1 = tk.Label(frame1, width=25, anchor=tk.W, text='No. of Agents')
        l1.pack(side=tk.LEFT, expand=False)
        
        self.e1 = tk.Entry(frame1, width=10) 
        self.e1.focus_set()
        self.e1.pack(side=tk.LEFT, expand=False)

        self.cb1 = tk.Checkbutton(frame1, padx=30, offvalue=tk.N, onvalue=tk.Y, 
                                  variable=self.agent_defaults,
                                  text='Use default start locations ' + 
                                       '(up to first 100 Agents)')
        self.cb1.pack(side=tk.LEFT, expand=False)

        # Frame 2
        l2 = tk.Label(frame2, width=25, anchor=tk.W, 
                      text='No. of moves for each Agent')
        l2.pack(side=tk.LEFT, expand=False)
        
        self.e2 = tk.Entry(frame2, width=10) 
        self.e2.pack(side=tk.LEFT, expand=False)
        
        # Frame 3
        l3 = tk.Label(frame3, width=25, anchor=tk.W, 
                      text='Neighbourhood Distance')
        l3.pack(side=tk.LEFT, expand=False) 
        
        self.e3 = tk.Entry(frame3, width=10) 
        self.e3.pack(side=tk.LEFT, expand=False)
        
        # Frame 4
        l4 = tk.Label(frame4, width=25, anchor=tk.W, text='No. of Wolves')
        l4.pack(side=tk.LEFT, expand=False) 
        
        self.e4 = tk.Entry(frame4, width=10) 
        self.e4.pack(side=tk.LEFT, expand=False)
        
        # Frame 5
        l5 = tk.Label(frame5, width=25, anchor=tk.W, 
                      text='Plot starting location')
        l5.pack(side=tk.LEFT, expand=False)
        
        self.rb1 = tk.Radiobutton(frame5, variable=self.plot_start, 
                                  text='No', value=tk.N, command=self.sel_no) 
        self.rb1.pack(side=tk.LEFT, expand=False)
        
        self.rb2 = tk.Radiobutton(frame5, variable=self.plot_start, 
                                  text='Yes', value=tk.Y, command=self.sel_yes) 
        self.rb2.pack(side=tk.LEFT, expand=False, padx=10)
        
        # Frame 6
        l6 = tk.Label(frame6, width=25, anchor=tk.W, 
                      text='Display summary data')
        l6.pack(side=tk.LEFT, expand=False)
        
        self.cb2 = tk.Checkbutton(frame6, offvalue=tk.N, onvalue=tk.Y, 
                                  variable=self.disp_agent_summary,
                                  text='Agents')
        self.cb2.pack(side=tk.LEFT, expand=False)

        self.cb3 = tk.Checkbutton(frame6, offvalue=tk.N, onvalue=tk.Y, 
                                  variable=self.disp_wolf_summary,
                                  text='Wolves')
        self.cb3.pack(side=tk.LEFT, expand=False)

        self.cb4 = tk.Checkbutton(frame6, offvalue=tk.N, onvalue=tk.Y, 
                                  variable=self.disp_params,
                                  text='Parameters')
        self.cb4.pack(side=tk.LEFT, expand=False)

        # Frame 7
        l7 = tk.Label(frame7, width=25, anchor=tk.W, text=None)
        l7.pack(side=tk.LEFT, expand=False)

        self.b1 = tk.Button(frame7, text='Run', underline=0, width=6,
                            command=self.run)
        self.b1.bind('<Return>', self.run)
        self.b1.pack(side=tk.LEFT, expand=False)
        
        self.b2 = tk.Button(frame7, text='Reset', underline=2, width=6,
                            command=self.clear)
        self.b2.bind('<Return>', self.clear)
        self.b2.pack(side=tk.LEFT, expand=False, padx=20)
        
        self.b3 = tk.Button(frame7, text='Exit', underline=1, width=6,
                            command=self.finish)
        self.b3.bind('<Return>', self.finish)
        self.b3.pack(side=tk.LEFT, expand=False)
        
        # Frame 8
        l8 = tk.Label(frame8, width=25, anchor=tk.W, text='Run information')
        l8.pack(side=tk.LEFT, expand = False)
        
        self.sb1 = tk.Scrollbar(frame8, orient=tk.VERTICAL)
        self.sb1.pack(side=tk.RIGHT, expand=False, padx=10, fill=tk.BOTH)

        self.t1 = tk.Text(frame8, width=600, fg='red', state=tk.DISABLED,
                     yscrollcommand=self.sb1.set)
        self.t1.pack(side = tk.LEFT, expand=False)
        
        #-------------------------------------------------
        # Initialise all input fields.
        #-------------------------------------------------
        self.clear()


    def run(self, event=None):
        '''
        Link to the main Agents model module with any parameters entered.
        
        Display any returned information, errors, help etc.
        
        Note 1: Only parameters that have been entered via the GUI front-end 
        will be passed as arguments to modelhome.py.  
        
        Note 2: Radio and Check button will always have a value.
        '''
        call_string = ''.join(
            ['python modelmain.py',
             ' --agents ' +  self.e1.get() if self.e1.get() != '' else '',
             ' --defaults ' +  self.agent_defaults.get(),        # check button
             ' --moves ' + self.e2.get() if self.e2.get() != '' else '',
             ' --distance ' + self.e3.get() if self.e3.get() != ''  else '',
             ' --wolves ' + self.e4.get() if self.e4.get() != ''  else '',
             ' --plotstart ' + self.plot_start.get(),            # radio button
             ' --dispagents ' +  self.disp_agent_summary.get(),  # check button
             ' --dispwolves ' +  self.disp_wolf_summary.get(),   # check button
             ' --dispparams ' +  self.disp_params.get()          # check button
            ])

        self.b1.focus_set()
        self.t1.configure(state=tk.NORMAL)  
        self.t1.delete(1.0, tk.END)
        self.t1.configure(state=tk.DISABLED)
        
        ret_code, ret_output = subprocess.getstatusoutput(call_string)
        
        self.t1.configure(state=tk.NORMAL)  
        self.t1.insert(tk.END, ret_output)
        self.sb1.config(command=self.t1.yview)
        self.t1.configure(state=tk.DISABLED)

    
    def clear(self, event=None):
        '''
        Set / Reset input fields to their initial values.
        '''
        self.e1.focus_set()
        self.e1.delete(0, tk.END)
        self.e2.delete(0, tk.END)
        self.e3.delete(0, tk.END)
        self.e4.delete(0, tk.END)
        self.rb1.select()
        self.rb2.deselect()
        self.sel_no()
        self.t1.configure(state=tk.NORMAL)  
        self.t1.delete(1.0, tk.END)
        self.t1.configure(state=tk.DISABLED)
        self.unchecked()
    
    
    def helper(self):
        '''
        Get the main Agents model help information.
        
        Display information is a popup window.
        '''
        help_return = subprocess.getoutput('python modelmain.py -h') 
        
        help_info = tk.Tk()
        help_info.geometry('900x500')
        help_info.wm_title('Help - Agents - Student 201388212')
        help_text = tk.Text(help_info)
        help_text.pack(padx=30, pady=30)
        help_text.insert(tk.END, help_return)
        
        b1 = tk.Button(help_info, text='OK', command=help_info.destroy)
        b1.pack()


    def about(self):
        '''
        Display general information about the Agents model in a popup window.
        '''
        about_return = 'Agents Model v1.0\n\n' + \
                       'Author: 201388212\n\n' + \
                       'Course: Master of Science - GIS\n\n' + \
                       'Unit: GEOG5003\n\n' + \
                       'Assignment: 1\n\n' + \
                       'Date: 17 April 2020'
        
        about_info = tk.Tk()
        about_info.geometry('600x450')
        about_info.wm_title('About - Agents - Student 201388212')
        about_text = tk.Text(about_info)
        about_text.pack()
        about_text.insert(tk.END, about_return)
        
        b1 = tk.Button(about_info, text='OK', command=about_info.destroy)
        b1.pack()
        
    
    def finish(self, event=None):
        '''
        Exit the program.
        '''
        exit()
        
        
    def sel_no(self):
        '''
        Set the Plot Starting Location radio button to No.
        '''
        self.plot_start.set(tk.N)
            
            
    def sel_yes(self):
        '''
        Set the Plot Starting Location radio button to Yes.
        '''
        self.plot_start.set(tk.Y)

            
    def unchecked(self):
        '''
        Set all of the Check Buttons off.
        '''
        self.agent_defaults.set(tk.N)
        self.disp_agent_summary.set(tk.N)
        self.disp_wolf_summary.set(tk.N)
        self.disp_params.set(tk.N)
            
            
#-------------------------------------------------
# Main program
#-------------------------------------------------
root = tk.Tk()
window = FrontEnd(root)      
        
#-------------------------------------------------
# Wait for interactions.
#-------------------------------------------------
tk.mainloop() 
        
