from typing import override

from win32more.Microsoft.UI.Xaml import FrameworkElement, Window
from win32more.Microsoft.UI.Xaml.Controls import Frame, NavigationView, NavigationViewItem, Page
from win32more.Microsoft.UI.Xaml.Markup import XamlReader
from win32more.Windows.UI.Xaml.Interop import TypeKind

from win32more.winui3 import XamlApplication, XamlType, xaml_typename

from pathlib import Path
from win32more.Microsoft.UI.Xaml import Application, Window
from win32more.Microsoft.UI.Xaml.Controls import Button,TextBlock,ComboBox,TextBox,CheckBox,PasswordBox,RadioButton,Slider
from win32more.Microsoft.UI.Xaml.Markup import IComponentConnector
from win32more.Windows.Foundation import Uri,Rect

from win32more import ComClass

from win32more.winui3 import XamlApplication

import tkinter.messagebox as messagebox


import configparser
CONFIG_FILE = "config.ini"

with open('1.xaml',encoding='utf8') as f:
    page=f.read()

class MainWindow(ComClass, Window, IComponentConnector):
    def __init__(self):
        super().__init__(own=True)
        self.InitializeComponent()


    def InitializeComponent(self):
        # ms-appx:///foo.xaml is relative to python.exe.
        # Use absolute path.
        # mx-appx:///C:/Full/Path/To/My.xaml
        # NOTE: According to documentation, LoadComponent() takes relative location.
        self.ExtendsContentIntoTitleBar=True

        
        xaml_path = Path("main.xaml").absolute().as_posix()


        resource_locator = Uri(f"ms-appx:///{xaml_path}")
        Application.LoadComponent(self, resource_locator)
def isnumeric(text:str) -> bool:
    try:
        float(text)
        return True
    except:
        return False
def mustBeANumber(sender,number:int=0):
    if not isnumeric(sender.as_(TextBox).Text):
        sender.as_(TextBox).Text=str(number)
class Page1(Page):
    def __init__(self):
        # Application.LoadComponent() should probably be used.
        super().__init__(move=XamlReader.Load(page))
        self.config = configparser.ConfigParser()
        self.config.read(CONFIG_FILE, encoding='utf-8')
        self.changeTextBlockText('TitleLabel',self.config.get('general','version'))
        self.changeTextBoxText('WidthTextBox',self.config.get('general','width'))
        self.changeTextBoxText('HeightTextBox',self.config.get('general','height'))
        self.changeTextBoxText('MaxImageCountTextBox',self.config.get('general','maximagecount'))
        self.changeTextBoxText('ModelNameTextBox',self.config.get('general','modelname'))
        self.changeCheckBoxChecked("IsVisionModelCheckBox",self.config.getboolean('general','isvisionmodel'))
        
        self.FindName('ApiKeyPasswordBox').as_(PasswordBox).Password=self.config.get('general','api_key')

        server=self.config.get('general','server_url')
        self.changeTextBoxText('CustomServerTextBox',server)

        self.FindName('OllamaRadioButton').as_(RadioButton).IsChecked=server.lower()=='ollama'

        self.FindName('BuiltinRadioButton').as_(RadioButton).IsChecked=server.lower()=='builtin'


        self.FindName('OllamaRadioButton').as_(RadioButton).Tapped+=self.changeToOllama
        self.FindName('BuiltinRadioButton').as_(RadioButton).Tapped+=self.changeToBuiltin
        self.FindName('CustomRadioButton').as_(RadioButton).Tapped+=self.changeToCustom


        self.FindName('WithImageCheckBox').as_(CheckBox).IsChecked=self.config.getboolean('general','withimage')
        self.FindName('AutoLoginCheckBox').as_(CheckBox).IsChecked=self.config.getboolean('general','autologin')
        self.FindName('AutoFocusingCheckBox').as_(CheckBox).IsChecked=self.config.getboolean('general','autofocusing')


        self.FindName('SendImagePossibilitySlider').as_(Slider).Value=(self.config.getint('general','sendimagepossibility'))

        
        
        self.FindName('ATDetectCheckBox').as_(CheckBox).IsChecked=self.config.getboolean('general','atdetect')


        self.changeTextBoxText('SystemTextBox',self.config.get('general','system'))






        def ok(sender,e):
            self.apply(sender,e)
            exit(0)
        def quit(sender,e):
            exit(0)

            


        self.FindName('WidthTextBox').as_(TextBox).TextChanged+=self.WidthTextBox_Changed
        self.FindName('HeightTextBox').as_(TextBox).TextChanged+=self.HeightTextBox_Changed
        self.textBoxConnect("MaxImageCountTextBox",self.MaxImageCountTextBox_Changed)
        self.textBoxConnect('ScrollTextBox',self.ScrollTextBox_Changed)
        self.FindName('ApplyButton').as_(Button).Click+=self.apply
        # self.FindName('OkButton').as_(Button).Click+=ok
        # self.FindName('CancelButton').as_(Button).Click+=quit
        
        

        # self.Button1=self.FindName("Button1").as_(Button)
        # self.Button1.Click+=self.Button1_Click

    def changeToOllama(self,sender,e):
        if self.FindName('OllamaRadioButton').as_(RadioButton).IsChecked:
                self.changeTextBoxText('CustomServerTextBox','ollama')
        self.FindName('CustomServerTextBox').as_(TextBox).IsEnabled=self.FindName('CustomRadioButton').as_(RadioButton).IsChecked
    def changeToBuiltin(self,sender,e):
        if self.FindName('BuiltinRadioButton').as_(RadioButton).IsChecked:
                self.changeTextBoxText('CustomServerTextBox','builtin')
        self.FindName('CustomServerTextBox').as_(TextBox).IsEnabled=self.FindName('CustomRadioButton').as_(RadioButton).IsChecked
    def changeToCustom(self,sender,e):
        self.FindName('CustomServerTextBox').as_(TextBox).IsEnabled=self.FindName('CustomRadioButton').as_(RadioButton).IsChecked
    def changeCheckBoxChecked(self,name,checked=True,toggle=False):
        if not toggle:
            self.FindName(name).as_(CheckBox).IsChecked=checked
        else:
            self.FindName(name).as_(CheckBox).IsChecked=not self.FindName(name).as_(CheckBox).IsChecked

    def changeTextBlockText(self,name:str,text:str):
        self.FindName(name).as_(TextBlock).Text=text
    def changeTextBoxText(self,name:str,text:str):
        self.FindName(name).as_(TextBox).Text=text
    def textBoxConnect(self,name:str,function):
        self.FindName(name).as_(TextBox).TextChanged+=function
    def WidthTextBox_Changed(self,sender,e):
        mustBeANumber(sender,1280)
    def HeightTextBox_Changed(self,sender,e):
        mustBeANumber(sender,720)   
    def ScrollTextBox_Changed(self,sender,e):
        mustBeANumber(sender,4)
    def MaxImageCountTextBox_Changed(self,sender,e):
        mustBeANumber(sender,1) 
    def apply(self,sender,e):
        self.config['general']['width']=self.FindName('WidthTextBox').as_(TextBox).Text
        self.config['general']['height']=self.FindName('HeightTextBox').as_(TextBox).Text
        self.config['general']['maximagecount']=self.FindName('MaxImageCountTextBox').as_(TextBox).Text
        self.config['general']['modelname']=self.FindName('ModelNameTextBox').as_(TextBox).Text
        self.config['general']['isvisionmodel']=getStrBool(self.FindName('IsVisionModelCheckBox').as_(CheckBox).IsChecked)
        self.config['general']['api_key']=self.FindName('ApiKeyPasswordBox').as_(PasswordBox).Password
        self.config['general']['server_url']=self.FindName('CustomServerTextBox').as_(TextBox).Text
        self.config['general']['withimage']=getStrBool(self.FindName('WithImageCheckBox').as_(CheckBox).IsChecked)
        self.config['general']['autologin']=getStrBool(self.FindName('AutoLoginCheckBox').as_(CheckBox).IsChecked)
        self.config['general']['autofocusing']=getStrBool(self.FindName('AutoFocusingCheckBox').as_(CheckBox).IsChecked)
        self.config['general']['sendimagepossibility']=str(int(self.FindName('SendImagePossibilitySlider').as_(Slider).Value))
        self.config['general']['atdetect']=getStrBool(self.FindName('ATDetectCheckBox').as_(CheckBox).IsChecked)
        self.config['general']['system']=self.FindName('SystemTextBox').as_(TextBox).Text
        
        with open(CONFIG_FILE, 'w', encoding='utf-8') as configfile:
            self.config.write(configfile)

def getStrBool(b:bool)->str:
    return "True" if b else "False"

class App(XamlApplication):
    @override
    def OnLaunched(self, args):
        global ContentFrame
        win = MainWindow()
        ContentFrame = win.Content.as_(FrameworkElement).FindName("RootFrame").as_(Frame)
        ContentFrame.Content=Page1()
        win.Activate()

XamlApplication.Start(App)