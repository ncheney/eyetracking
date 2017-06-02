#! /usr/bin/python
# -*- coding: utf-8 -*-
# tkinterPrompt.py
# Nick Cheney
# 9/11/12

from Tkinter import *
from time import *
from random import *
import os
from subprocess import Popen, PIPE, call

#subjectID = randint(0,1000000) #NOTE: no check for duplicates!
subjectID = int(time())
UserTrialCount = 0


call("mkdir "+str(subjectID), shell=True)
userInputFile = open(str(subjectID) + '/' + str(subjectID)+'_UserInput', 'w')

# can numbers be parameterized for different monitors?
#screenWidth = 1920#/8
#screenHeight = 1080#/17
fontSize=40
pad=100

fullscreen=False ### NOTE: Entry currently not able to be selected in full screen mode!!! ###
usingEyetracking = False  #TODO: make random in trials

done=False

startTime = time()
userInputFile.write("%09.2f  " %  (time()-startTime))

if "-E" in sys.argv[:]:
    usingEyetracking = True
elif "-M" in sys.argv[:]:
    usingEyetracking = False
elif random() > 0.5:
    usingEyetracking = True
else: 
    usingEyetracking = False

if usingEyetracking:
    userInputFile.write("UsingEyetracking\n")
else:
    userInputFile.write("UsingMouseClicks\n")


numPages=2
#global onPage
onPage=0

instructionList=[]
successList=[]

exitFlag=False

class Page:

    def __init__(self, master):

        self.frame = Frame(master, width=master.winfo_screenwidth(), height=master.winfo_screenheight() )#width=screenWidth, height=screenHeight)
        self.frame.pack()

    def addButton(self,_text, _command, _param, _color):
        #self.yesButton = Button(frame, text="NO", command=self.say_no, font=100)
        self.yesButton = Button(self.frame, text=_text, pady=20, fg=_color, command=lambda: _command(_param), font=("Helvetica", fontSize))
        self.yesButton.pack(side=BOTTOM, fill=X)

    def addLabel(self,_text):
        Label(self.frame, text=_text, font=("Helvetica", fontSize), padx=pad, pady=pad).pack(side=TOP, fill=X)#)pady=10)
##        
##            text = Text(self.frame)#, state=DISABLED)#, height=screenHeight, width=screenWidth, font=fontSize)
##            text.insert(INSERT, _text)
##            text.pack(side=TOP)#, fill=X, justify=CENTER)

    def addEntry(self, _width):
        e = Entry(self.frame, width = _width, font=("Helvetica", int(round(fontSize/2))))
        e.pack(side=TOP)
        #print type(e)
        return e

def makePage(_labelText, _buttonType, onPage):
    root = initRoot()

    app = Page(root)
    app.addLabel(_labelText)

    if _buttonType == "yesNo":
        app.addButton("NO",say_no, root, "red")
        app.addButton("YES",say_yes, root, "black")
    elif _buttonType == "Continue":
        #app.addButton("BACK", goBack, [onPage,root], "red")
        app.addButton("CONTINUE", nextScreen, root, "black")
    elif _buttonType == "Wait":
        #app.addButton("BACK", goBack, [onPage,root], "red")
        app.addButton("Please wait for experimenter!", nextScreen, root, "black")
    elif _buttonType == "Quit":
        app.addButton("QUIT EXPERIMENT",exitExperiment, root, "red")
        app.addButton("KEEP GOING!",nextScreen, root, "black")
    elif _buttonType == "Scale":
        app.addButton("STRONGLY DISAGREE",stronglyDisagree, root, "red")
        app.addButton("DISAGREE",disagree, root, "red")
        app.addButton("NEUTRAL",neutral, root, "black")
        app.addButton("AGREE",agree, root, "green")
        app.addButton("STRONGLY AGREE",stronglyAgree, root, "green")
    elif _buttonType == "Entry":
        e = app.addEntry(120)
        app.addButton("SUBMIT",getEntry,[e,root],"black")
        

    #if onPage>0:
    #    app.addButton("BACK", goBack, "black")
        
    root.mainloop()

    return onPage

def makePageButtonText(_labelText, _buttonTextArray, onPage):
    root = initRoot()

    app = Page(root)
    app.addLabel(_labelText)

    for thisButtonText in _buttonTextArray:
        app.addButton(thisButtonText,writeButtonPress,[thisButtonText,root],"black")
        
    #if onPage>0:
    #    app.addButton("BACK", goBack, "black")
        
    root.mainloop()

    return onPage


def writeButtonPress(argIn):
    userInputFile.write(argIn[0].replace(" ","")+"\n") 
    print argIn[0].replace(" ","")
    argIn[1].destroy()

def getEntry(argIn):
    userInputFile.write(argIn[0].get()+"\n") 
    print argIn[0].get()
    argIn[1].destroy()

def stronglyDisagree(root):
    userInputFile.write("stronglyDisagree\n")
    root.destroy()

def disagree(root):
    userInputFile.write("disagree\n")
    root.destroy()

def neutral(root):
    userInputFile.write("neutral\n")
    root.destroy()

def agree(root):
    userInputFile.write("agree\n")
    root.destroy()

def stronglyAgree(root):
    userInputFile.write("stronglyAgree\n")
    root.destroy()

def exitExperiment(root):
    global exitFlag
    exitFlag = True
    root.destroy()

def say_yes(root):
    global userInputFile
    global successList
    successList.append("yes")
    userInputFile.write("yes\n")
    print successList
    root.destroy()

def say_no(root):
    global userInputFile
    global successList
    successList.append("no")
    userInputFile.write("no\n")
    print successList
    root.destroy()

def nextScreen(root):
    #global root
    root.destroy()

def goBack(argIn):
    global onPage
    onPage=argIn[0]-2
    argIn[1].destroy

def initRoot():
    root = Tk()
    if fullscreen:
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
       # root.overrideredirect(1) 
      # root.geometry("%dx%d+%d+%d" % (w, h, -w , 0))
        root.geometry("%dx%d+%d+%d" % (1920, 1080, 900 , 0))
    else:
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()        
       # root.overrideredirect(1)
        w=w-300
        h=h-0
       # root.geometry("%dx%d+%d+%d" % (w, h, -w, 0))
        root.geometry("%dx%d+%d+%d" % (1920, 1030, 900 , 0))
    return root

# TEST PAGE

if usingEyetracking:
    clickOn = "look at (without clicking on)"
    ClickOn = "Look at (without clicking on)"
else:
    clickOn = "click on (with the mouse)"
    ClickOn = "Click on (with the mouse)"

textList=["Thanks for taking part in our study.",

          'There are two parts to this study.\n\
In Part I, a set of 15 objects will appear on-screen.\n\
\n\
We will give you a goal shape (e.g. a small red cone).\n\
Your challenge is to produce a shape like the goal.',

	  'You can do that by guiding the set of\n\
shapes to see on screen to look like a goal shape.\n\
The next set of shapes on screen will more closely \n\
resemble the ones you\'ve shown a prefernce for.\n'\
+'\n\
Simply ' +clickOn+' shapes\n\
that will move you toward the goal shape.',

          'Please continue this process until you feel that\n\
at least one of the shapes matches the goal description\n\
(e.g. that you have produced a small red cone).\n\n\
When that happens, press "Q" on the keyboard to quit.',

          'If you believe that you cannot reach the target shape\n\
and wish to give up before the goal is completed,\n\
you may also quit at any time by pressing the "Q" key.',

          "At any point, \
if you find an interesting shape on the screen,\n\
please save that object (you won't lose your progress).\n\
\n\
To do this, pause the screen at the rotation\n\
you desire by pressing the spacebar on the keyboard,\n\
then take a screenshot by pressing the \"S\" key.\n"\
#+"The computer will tell you (out loud) if the save was successful.\n"\
+"\n\
Unpause with the speacebar to continue designing. ",

          'You will be given 3 separate goals.\n\
After each, a questionnaire will pop up. After the third\n\
questionnaire, we will describe Part II of the experiment.\n\
\n\
Please take as long as you want for Part I.\n\
(Though each section will time out after 10 minutes)',

          "Again, the important keys are:\n\
          [Spacebar] - Pause or Unpause the shape design\n\
          [S] - Save a screenshot of found shapes\n\
          [Q] - Quit the trial once shapes are found\n\
          (Please remember to save before you quit!)\n\n\
(If you forget any of the instructions, or your target shape,\n\
please pause with the spacebar before find the information\n\
in the title bar at the top of the screen)\n\n\
Ready to begin?"]

if not usingEyetracking:
    textList.insert(3,'If you wish to click on more than one shape,\n\
right-click on each on you like and then \n\
click on one of them with the left mouse button\n\
to advance to the next generation.')
else:
    textList.insert(6,"If at any time the program pauses (the shapes stop spinning) \n\
and you did not press the spacebar to pause,\n\
it means that your eyes are not within\n\
the capturing range of the eyetracker.\n\
\n\
Please adjust your posture or position until the\n\
program captures your eye movements and unpauses itself.")

textList2 = [
    "This is the end of Part I.\n\n\
Feel free to take a short break to stretch\n\
or walk around before we start Part II\n\n\
Click \"CONTINUE\" below when you are ready to start.",

    "Part II of the Experiment allows you to freely\n\
design objects that you find interesting.",

"For the next 20 minutes,\n\
simply "+clickOn+" the shapes that\n\
you find most interesting, or that might lead to interesting shapes.",

"At any point, \
if you find an interesting shape on the screen,\n\
please save that object (you won't lose your progress).\n\
\n\
To do this, pause the screen at the rotation\n\
you desire by pressing the spacebar on the keyboard,\n\
then take a screenshot by pressing the \"S\" key.\n"\
#+"The computer will tell you (out loud) if the save was successful.\n"\
+"\n\
Unpause with the speacebar to continue designing. ",

"At any point in time you can restart\n\
the process from scratch by pressing \"Q\".",
    
"You will have 20 minutes for this section.\n\
The computer will automatically stop you when time is up.",
    
          "Again, the important keys are:\n\
          [Spacebar] - Pause or Unpause the shape design\n\
          [S] - Save a screenshot of found shapes\n\
          [Q] - Quit the trial once shapes are found\n\
          (Please remember to save before you quit!)\n\n\
(If you forget any of the instructions, or your target shape,\n\
please pause with the spacebar before find the information\n\
in the title bar at the top of the screen)\n\n\
Ready to begin?"]


#buttonTitleList=["buttonTitle1","buttonTitle2"]
#buttonCommandList=[say_no,say_yes]
buttonTypeList=["Continue"]*len(textList)
buttonTypeList2=["Continue"]*len(textList2)

# RANDOMLY CHOOSE TARGETS:
shapes = ["OVAL", "CUBE", "CONE"]
colors = ["RED", "BLUE", "YELLOW"]
sizes = ["SMALL", "LARGE"]
#noveltyProbability = 0.1

#while onPage < numPages:

if not usingEyetracking:
    makePage(str(subjectID)+'A',"Wait",1)
else:
    makePage(str(subjectID)+'B',"Wait",1)

for onPage in range(len(textList)):
    onPage = makePage(textList[onPage],buttonTypeList[onPage],onPage)


randsUsed = ["999"]
randInts = "999"

userInputFile.write("%09.2f  " %  (time()-startTime))
userInputFile.write("DIRECTED-EVOLUTION:\n")
for trial in range(3):

    while randInts in randsUsed:
        sizeInt = randint(0,len(sizes)-1)
        colorInt = randint(0,len(colors)-1)
        shapeInt = randint(0,len(shapes)-1)
        randInts = str(sizeInt)+str(colorInt)+str(shapeInt)
    randsUsed.append(randInts)

    thisSize = sizes[sizeInt]
    thisColor = colors[colorInt]
    thisShape = shapes[shapeInt]
    
    instructions = 'Please try and find:\n\n' + thisSize + " " + thisColor + " " + thisShape + "S"

    successInstruction ="Please rate your feelings towards the following statement\n\n" + \
                        "I was successful in creating:\n" + \
                        thisSize + " " + \
                        thisColor + " " + \
                        thisShape + "S"  

    instructionList.append(thisSize+thisColor+thisShape)

    userInputFile.write("%09.2f  " %  (time()-startTime))
    userInputFile.write("---\n")
    userInputFile.write("%09.2f  " %  (time()-startTime))
    userInputFile.write(str(subjectID)+str(UserTrialCount)+":\n")
    userInputFile.write("%09.2f  " %  (time()-startTime))
    userInputFile.write(thisSize+"-"+thisColor+"-"+thisShape+"\n")
                           
    instructions2 = 'Please try and find the most interesting shapes you can.'

    instructions3 = "We'll restart in a moment,\nfirst please tell us why you ended the previous session:" #[open entry]

    onPage = makePage(instructions,"Continue",onPage)

    eyeArg = " "
    if usingEyetracking:
        eyeArg = " -E "

    #os.popen("./Hypercube_NEAT -O Subject -R "+ str(subjectID)+str(UserTrialCount) +" -I ShapesExperiment.dat")  # for nick's laptop
    #Popen("./awesomeClient.py "+ eyeArg + " " + str(subjectID)+str(UserTrialCount), shell=True) # for jeff's old macbook
    #os.popen("awesomeClient.py "+ eyeArg + " " + str(subjectID)) # for jeff's old macbook
    call("./awesomeClient.py -O "+str(subjectID)+str(UserTrialCount) + eyeArg + " -R " + str(subjectID)+str(UserTrialCount) + " -I ShapesExperiment.dat -K 10 -SN "+thisSize+"_"+thisColor+"_"+thisShape+"S", shell=True)

    #onPage = makePage("PLESE WAIT...","None",onPage)

    #sleep(4)

    userInputFile.write("%09.2f  " %  (time()-startTime))
    userInputFile.write("success? ")
    onPage = makePage(successInstruction,"Scale",onPage)

    userInputFile.write("%09.2f  " %  (time()-startTime))
    userInputFile.write("reason?  ")
    onPage = makePage(instructions3,"Entry",onPage)

    #onPage = makePage(quitInstructions,"Quit",onPage)
    
    #if trial>10:
    #    exitFlag=True

    #trial +=1 #does (this number + 2) trials

    UserTrialCount+=1

# DISPLAY PROMPT 2
userInputFile.write("%09.2f  " %  (time()-startTime))
userInputFile.write("***\n")
userInputFile.write("%09.2f  " %  (time()-startTime))
userInputFile.write("OPEN-EVOLUTION:\n")

for onPage in range(len(textList2)):
    onPage = makePage(textList2[onPage],buttonTypeList2[onPage],onPage)

startTimeFreeForm = time()

while time() - startTimeFreeForm < 60*20:
    userInputFile.write("%09.2f  " %  (time()-startTime))
    userInputFile.write("---\n")
    userInputFile.write("%09.2f  " %  (time()-startTime))
    userInputFile.write(str(subjectID)+str(UserTrialCount)+":\n")
    
    #os.popen("./Hypercube_NEAT -O Subject -R "+ str(subjectID) +" -I ShapesExperiment.dat")  # for nick's laptop
    #Popen("awesomeClient.py "+ eyeArg + " " + str(subjectID)+str(UserTrialCount), shell=True) # for jeff's old macbook
    #call("awesomeClient.py "+ eyeArg + " " + str(subjectID)+str(UserTrialCount), shell=True) # for jeff's old macbook
    call("./awesomeClient.py -O "+str(subjectID)+str(UserTrialCount) + eyeArg + " -R " + str(subjectID)+str(UserTrialCount) + " -I ShapesExperiment.dat -K 20 -SN INTERESTING_SHAPES", shell=True)

    #sleep(4)

    userInputFile.write("%09.2f  " %  (time()-startTime))
    userInputFile.write("reason?  ")
    onPage = makePage(instructions3,"Entry",onPage)

    UserTrialCount+=1
userInputFile.write("%09.2f  " %  (time()-startTime))
userInputFile.write("###\n")
userInputFile.write("%09.2f  " %  (time()-startTime))
userInputFile.write("FINAL-QUESTIONS:\n")

makePage("You have completed parts I and II of the experiment.\nPlease answer a few questions about your experience today.","Continue",1) 

userInputFile.write("%09.2f  " %  (time()-startTime))
userInputFile.write("interestingShapes? ")
makePage("The system helped me design interesting shapes:","Scale",1)

userInputFile.write("%09.2f  " %  (time()-startTime))
userInputFile.write("goalsReached?      ")
makePage("The system helped me reach my design goals:","Scale",1)

userInputFile.write("%09.2f  " %  (time()-startTime))
userInputFile.write("novelSuggestions?  ")
makePage("The system suggested shapes I would not have thought of:","Scale",1)

userInputFile.write("%09.2f  " %  (time()-startTime))
userInputFile.write("aidedCreativity?   ")
makePage("The system aided my creative design process:","Scale",1)

userInputFile.write("%09.2f  " %  (time()-startTime))
userInputFile.write("enjoyable?         ")
makePage("The system was enjoyable to use:","Scale",1)

userInputFile.write("%09.2f  " %  (time()-startTime))
userInputFile.write("overallReactions?  ")
makePage("Overall, what did you think about this technology?\nAlso, did you like using it?","Entry",1)

makePage("Before you leave, please answer some quick questions about yourself.","Continue",1)

userInputFile.write("%09.2f  " %  (time()-startTime))
userInputFile.write("Gender?      ")
makePageButtonText("Please choose the option that best describes you:",["I Choose Not To Respond", "Other", "Female","Male"],1)

userInputFile.write("%09.2f  " %  (time()-startTime))
userInputFile.write("Handedness?  ")
makePageButtonText("Please choose the option that best describes you:",["I Choose Not To Respond","Other","Left Handed","Right Handed"],1)

userInputFile.write("%09.2f  " %  (time()-startTime))
userInputFile.write("age?         ")
makePage("How old are you?","Entry",1)

userInputFile.write("%09.2f  " %  (time()-startTime))
userInputFile.write("major?       ")
makePage("What is your area of study (and/or occupation)?","Entry",1)

userInputFile.write("%09.2f  " %  (time()-startTime))
userInputFile.write("feel?        ")
makePage("How do you feel today (happy, tired, stressed, energized, hung-over, etc.)?","Entry",1)

makePage("You're done!\n\nThanks for taking part in our study.\nPlease stay on this page so the experimenter\ncan use the information for your compensation.\n\n"+"%.2f  " %  ((time()-startTime)/60)+"\n"+"$%.2f  " %  ((time()-startTime)/60/60*15),"Wait",1)

userInputFile.close()

#Popen("mkdir run"+str(subjectID), shell=True)
Popen("mv "+str(subjectID)+"* "+str(subjectID), shell=True)