"""
inspect any python object with a slick web interface.

Usage:
    import webinspect
    webinspect.launch("any object you want") #launches a web browser
"""

__version__ = '0.1.6'

import webbrowser
import tempfile
import time
import datetime

def launch(thing,title=False):
    """analyze a thing, create a nice HTML document, and launch it."""
    html=htmlFromThing(thing,title=title)
    fname="%s/%s.html"%(tempfile.gettempdir(),str(time.time()))
    with open(fname,'w') as f:
        f.write(html)
    webbrowser.open(fname)
   
def analyzeThing(thing):
    """analyze an object and all its attirbutes. Returns a dictionary."""    
    things={}
    for name in sorted(dir(thing)):
        item=getattr(thing,name)
        itemType=type(item).__name__
        itemStr=str(item)
        itemEval=""
        if "method" in itemStr:
            try:
                itemEval=str(getattr(thing,name)())
                if len(itemEval)>1000:
                    itemEval=itemEval[:1000]+" ..."
            except:
                itemEval="FAILED TO EVALUATE"
        #print("[%s] (%s) %s {%s}"%(name,itemType,itemStr,itemEval))
        things[name]=[itemType,itemStr,itemEval]
    return things

def websafe(s):
    """return a string with HTML-safe carrots"""
    return s.replace("<","&lt;").replace(">","&gt;")
    
def htmlFromThing(thing,title):
    """create pretty formatted HTML from a things dictionary."""
    stuff=analyzeThing(thing)
    names2=list(stuff.keys())
    for i,name in enumerate(names2):
        if name.startswith("_"):
            names2[i]="zzzzzzzzzz"+name

    html="""<html><head><style>
    body {font-family: courier, monospace;}
    .name {font-weight: bold;}
    .type {font-style: italic; font-family: serif; color: #AAA;}
    .desc {}
    .itemEval {background-color: #DDFFDD;}
    .itemEvalFail {}
    table {font-size: .8em;
           margin-top: 20px;
           border-collapse: collapse;}
    tr {border: 1px solid #CCC;}
    td {padding: 2px 10px 2px 10px;}
    .credits {text-align: center; 
              opacity: 0.5; 
              margin-top: 50px;
              font-size: .8em;
              font-family: sans-serif;}
    </style></head><body>"""
    
    if title:
        html+='<span style="color: #CCC;">title: </span>%s<br>'%title    
    html+='<span style="color: #CCC;">value: </span>%s<br>'%str(thing)
    html+='<span style="color: #CCC;">&nbsp;type: </span>%s<br>'%type(thing).__name__
    html+='<table cellpadding=3 align="center">'
    html+='<tr style="background-color: #000; color: #FFF; font-weight: bold;">'
    html+='<td>property</td><td>type</td><td>value</td>'
    html+='<td>evaluated (without arguments)</td></tr>'
    for name in sorted(names2):
        if name.startswith("zzzzzzzzzz"):
            name=name[10:]
        itemName=str(name)
        itemType=websafe(stuff[name][0])
        itemStr=websafe(stuff[name][1])
        itemEval=websafe(stuff[name][2])
        color="DDDDFF"
        color2=""
        if "method" in itemType:
            itemName+="()"
            color="FFDDDD"
        if itemName.startswith("_"):
            color="EEEEEE"
        if itemStr.startswith("&lt;"):
            itemStr="""<span style="color: #CCC; font-family: serif; 
                font-style: italic;">%s</span>"""%itemStr
        else:
            color2="DDFFDD"
            if itemEval=="":
                itemEval="FAILED TO EVALUATE"
        html+='<tr>'
        html+='<td class="name" style="background-color: #%s;">%s</td>'%(color,itemName)
        html+='<td class="type">%s</td>'%(itemType)
        html+='<td class="itemStr" style="background-color: #%s;">%s</td>'%(color2,itemStr)
        if itemEval=="FAILED TO EVALUATE":
            html+='<td class="itemEvalFail"></td>'
        else:
            html+='<td class="itemEval">%s</td>'%(itemEval)
        html+='</tr>'
        
    dt=datetime.datetime.now()
    html+="""</table><p class="credits">
    page automatically generated by 
    <a href="">webinspect</a> python module
    %s</p>
    </body></html>"""%(dt.strftime("at %I:%M %p on %B %d, %Y"))
    
    return html
    
class TESTCLASS:
    """test class to demonstrate how inspection works."""
    def __init__(self):
        self.x=123
        self.s="scott"
        self.y=[1,8,3,5,6]

    def func(self):
        self.f='asdf'
        
    def __repr__(self):
        return repr(["array","of","things",1234])
        
if __name__=="__main__":
    print("This isn't intended to be run directly, but what the heck...")
    launch("demo string")
    launch(TESTCLASS(), "here is a demo title")