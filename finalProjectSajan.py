# Name: Sajan Paventhan, ID: 734579



# ---------- DESCRIPTION ----------
'''
This is a math flashcard game that generates 2 numbers and a random operator
(+, -, x, /, %), and the user must input an answer until they either run out of
time or finish the number of questions they inputted. The user may select the
level of difficulty they would like (1, 2, 3, 4), each varying in the number of
question options. The user may enter the amount of time they would like, or they
can select no timer. The user can also enter the number of questions they would
like to answer. Both the timer and number of questions input are validated to
make sure there is no bad input. As well as this, the user also has the choice
to choose which operators they would like to be tested on. In addition, the user
can also choose if they would like negative numbers included. Finally, there is
a theme selector, that is inspired by Pokemon and each lead to a theme dedicated
to its own Pokemon. 

Once the start button is pressed, the tab switches to the game tab where the
game will automatically begin. If the timer is selected, the timer will begin
counting down from the time inputted. There is a live score counter, updating
after each submit. As mentioned earlier, 2 numbers and an operator will be shown
on the screen, with an entry box to the right. Once the answer is inputted and
submit is pressed, all the widgets will update. There is a progress bar that
tracks how many questions you have completed and have left. There is a section
that tells the user how many questions they've completed and have left. After
each question, either wrong or correct images will appear, and will also say the
answer inputted and the correct answer. Once there are no more questions or if
the timer expires, a message box appears with your score. At any point, the
reset button can be clicked to reset the game, and the back button brings the
user back to the menu tab to adjust settings. 
'''

# ---------- ENHANCEMENTS ----------
'''
- No Timer and Timer option (in Seconds)
    - Try and Except to check valid input
- Input number of questions 
    - Try and Except to check valid input
- Select operators to use
- Negative numbers
- Modulus / Division operators
- Theme selector (Orange, Blue, Yellow, Green)
- Question Log (ScrolledText)
- Questions Completed / Questions Remaining
- You answered... / Correct answer is...
- Progress Bar
- Multiple tabs
'''

# Import library
from tkinter import ttk
from tkinter.ttk import Progressbar
from tkinter import scrolledtext
from tkinter import messagebox
import random
from tkinter import *

# Create window
window = Tk()
window.geometry('1024x768')
window.title("Pokemon Math Flashcards")

# Create notebook and set up tabs
tab_control = ttk.Notebook(window)
tab1 = Frame(tab_control)
tab_control.add(tab1, text='MENU')
tab2 = Frame(tab_control)
tab_control.add(tab2, text='GAME')
tab_control.pack(expand=1, fill='both')

# Configure number of columns
tab1.grid_columnconfigure(0, weight=1)

tab2.grid_columnconfigure(0, weight=1)
tab2.grid_columnconfigure(1, weight=1)
tab2.grid_columnconfigure(2, weight=1)


# ---------- FUNCTIONS ----------

# Function to get level from tab1
def getLevel():
    global randomIntegerMax
    global level 
    level = 1
    
    if levelNum.get() == 1:
        level = 1
        randomIntegerMax = 3
    elif levelNum.get() == 2:
        level = 2
        randomIntegerMax = 6
    elif levelNum.get() == 3:
        level = 3
        randomIntegerMax = 9
    elif levelNum.get() == 4:
        level = 4
        randomIntegerMax = 12

# Function to get timer inputted from tab1
# Output: integer (timer)
def getTimer():
    global timer
    global resetBoolean
    timer = 1
    if timerBoolean.get() == 0: # No timer Radiobutton
        timer = "no timer selected"
        resetBoolean = 0 # Reset boolean to make sure countdownn() does not run twice
    elif timerBoolean.get() == 1: # Timer Radiobutton
        # Try and Except to validate timer input
        try: 
            if int(timerInput.get()) >= 1:
                timer = timerInput.get()
                countdownLabel.configure(text = timer)
                
            else:
                # Error message for invalid input
                res = messagebox.showerror("Error", "Please enter a valid time.")
                window.mainloop() # Rerunning program
        except:
            # Error message for invalid input
            res = messagebox.showerror("Error", "Please enter a valid time.")
            window.mainloop() # Rerunning program
            
    return timer

# Function to create the countdown
def countdownn(): # *Keyword countdown() didn't work so I made it countdownn()*
    global timer
    global resetBoolean
    global totalScore
    global numOfQ
    
    if timerBoolean.get() == 1: # Timer Radiobutton
        # Using .after() to use recursion and call the function every 1000ms.
        if int(timer) > 0 and resetBoolean == 1:
            timer = int(timer) - 1
            window.after(1000, countdownn) 
            countdownLabel.configure(text=timer)
            
            # Making sure timer does not end
            if int(timer) > 1000000000000000: 
                countdownLabel.configure(text="You are done!")
        # Timer is done
        else:
            timeDone()
            resetSettings()
            reset()
            getTimer()
            resetBoolean = 0
    elif timerBoolean.get() == 0: # No timer Radiobutton
        countdownLabel.configure(text="no timer selected")

# Function to display ending message for timer end
def timeDone():
    finishedMessage = "Timer is DONE! You got " + str(correctScore) + " out of " + str(totalScore) + " correct."
    res = messagebox.showerror("Timer is done!", finishedMessage)
    countdownLabel.configure(text=getTimer())
    resetBoolean = 0
    timer = 100000

# Function to get the number of questions inputted from tab1
def getNumOfQuestions():
    global numOfQ
    numOfQ = 0
    # Try and Except to validate num of question input
    try:
        if int(numOfQuestionsInput.get()) >= 1:
            numOfQ = numOfQuestionsInput.get()
        else: # Invalid input error message
            res = messagebox.showerror("Error", "Please enter a valid number of questions.")
            window.mainloop()
    except: # Invalid input error message
        res = messagebox.showerror("Error", "Please enter a valid number of questions.")
        window.mainloop()
                
# Function to get operators selected from tab1
def getOperatorOptions():
    global operatorOptions
    global negativeBoolean
    
    negativeBoolean = False
    operatorOptions = []
    
    if negatives_state.get(): 
        negativeBoolean = True
        
    # Appending all used operators to operatorOptions
    if addition_state.get():
        operatorOptions.append("+")
    if subtraction_state.get():
        operatorOptions.append("-")
    if multiplication_state.get():
        operatorOptions.append("x")
    if modulus_state.get():
        operatorOptions.append("%")
    if division_state.get():
        operatorOptions.append("/")

# Function to get theme from tab1
def getTheme():
    global theme
    global theme2
    
    if themeNum.get() == 1: # ORANGE
        theme = "#fcb264"
        theme2 = "orange"
        pokemonFrameImage.configure(file = "charmander.png")
        
    elif themeNum.get() == 2: # BLUE
        theme = "#b4eaff"
        theme2 = "blue"
        pokemonFrameImage.configure(file = "squirtle.png")
    elif themeNum.get() == 3: # YELLOW
        theme = "#fff3a7"
        theme2 = "yellow"
        pokemonFrameImage.configure(file = "pikachu.png")
        
    elif themeNum.get() == 4: # GREEN
        theme = "#cbfa8f"
        theme2 = "green"
        pokemonFrameImage.configure(file = "bulbasaur.png")

# Function to generate and display 2 random integers in the range
def generateRandomNum():
    global negativeBoolean
    global randomIntegerMax
    global randomInt1
    global randomInt2
    
    # Making sure modulus numbers are positive
    if randomSign == '%':
        randomInt1 = random.randrange(1, randomIntegerMax + 1)
        randomInt2 = random.randrange(1, randomIntegerMax + 1)
    
    # Generating negative numbers
    elif negativeBoolean:
        randomInt1 = random.randrange(randomIntegerMax * -1, randomIntegerMax + 1)
        randomInt2 = random.randrange(1, randomIntegerMax + 1)
    
    # Generating positive numbers
    else:
        randomInt1 = random.randrange(1, randomIntegerMax + 1)
        randomInt2 = random.randrange(1, randomIntegerMax + 1)
    
    # Changing numbers for division
    if randomSign == '/':
        randomInt1 *= randomInt2
    
    # Changing numbers for modulus
    elif randomSign == '%':
        if randomInt1 < randomInt2:
            randomInt1, randomInt2 = randomInt2, randomInt1
    
    # Displaying integers 
    integerDisplay1.configure(text=randomInt1)
    integerDisplay2.configure(text=randomInt2)

# Function to generate a random operator
def generateRandomSign():
    global randomSign
    # Random.choice from the list with all the chosen operators
    randomSign = random.choice(operatorOptions)
    
    # Display random operator
    signDisplay.configure(text=randomSign)

# Function to calculate answer
def calculateAns():
    global correctAns
    global randomSign
    global randomInt1
    global randomInt2
    
    if randomSign == '+':
        correctAns = randomInt1 + randomInt2
    elif randomSign == '-':
        correctAns = randomInt1 - randomInt2
    elif randomSign == 'x':
        correctAns = randomInt1 * randomInt2
    elif randomSign == '%':
        # Making sure the first number is greater than the second for modulus and positive
        if abs(randomInt1) < abs(randomInt2):
            randomInt1, randomInt2 = abs(randomInt2), abs(randomInt1)
        correctAns = randomInt1 % randomInt2
    elif randomSign == '/':
        correctAns = randomInt1 // randomInt2

# Function to check answer inputted 
def checkAns():
    global ansInputted
    global correctAns
    global correctScore
    global wrongScore
    global totalScore
    
    ansInputted = answerInput.get()
    
    # Answer is correct
    if ansInputted == str(correctAns):
        correctScore += 1
        totalScore += 1
        correctIndicatorLabel.configure(text="CORRECT", fg="green")
        correctIndicatorImage.configure(file="correct.png")
    
    # Answer is wrong
    else:
        wrongScore += 1
        totalScore += 1
        correctIndicatorLabel.configure(text="WRONG", fg="red")
        correctIndicatorImage.configure(file="wrong.png")
    
    # Displaying score
    correctScoreHeading.configure(text=correctScore)
    wrongScoreHeading.configure(text=wrongScore)
    totalScoreHeading.configure(text=totalScore)

# Function to update scrolledText question log
def updateQuestionLog():
    correctEquation = str(randomInt1) + ' ' + str(randomSign) + ' ' + str(randomInt2) + ' ' + '=' + ' ' + str(correctAns)
    questionLog.insert(INSERT, correctEquation + "\n")

# Function to update correct answer and inputted answer display
def updateAnswerCheck():
    youAnswered.configure(text=ansInputted)
    correctAnswerIs.configure(text=correctAns)

# Function to update number of questions log
def updateNumOfQLog():
    global left
    left = int(numOfQ) - int(totalScore)
    numOfQuestionsCompleted.configure(text=totalScore)
    numOfQuestionsLeft.configure(text=left)

# Function to update progress bar
def updateProgressBar():
    global totalScore
    global numOfQ
    global bar
    bar['value'] = 0
    bar['value'] = int(bar['value']) + (int(totalScore) / int(numOfQ) *100)

# Function for back button
def back():
    global timer
    global resetBoolean
    
    # Reset tab1 settings
    tab_control.select(tab1)
    negatives_state.set(True)
    addition_state.set(True)
    subtraction_state.set(True)
    multiplication_state.set(True)
    modulus_state.set(True)
    division_state.set(True)
    themeNum.set(1)
    
    # Prepare for next start button click
    resetBoolean = 1
    getTimer()
    countdownLabel.configure(text=getTimer())
    timer = 10000000
    resetSettings()

# Function for reset button
def reset():
    global timer
    global resetBoolean
    
    # Similar to start button function, reset tab2
    getTimer()
    getLevel()
    getNumOfQuestions()
    getOperatorOptions()
    getTheme()
    setTheme()
    
    levelTitle.configure(text=level)

    resetSettings()

    tab_control.select(tab2)
    getTimer()
    if resetBoolean == 0:
        resetBoolean = 1
        countdownn()

# Function to reset tab2 screen
def resetSettings():
    global timer
    global totalScore
    global wrongScore
    global correctScore
    correctScoreHeading.configure(text=0)
    wrongScoreHeading.configure(text=0)
    totalScoreHeading.configure(text=0)
    
    totalScore = 0
    correctScore = 0
    wrongScore = 0
    getNumOfQuestions()
    updateNumOfQLog()
    updateProgressBar()
    correctIndicatorLabel.configure(text="Enter Answer!", fg="black")
    correctIndicatorImage.configure(file="pokeball.png")
    questionLog.delete(0.0, END)

# Function to set theme
def setTheme():
    # Had to set background of every widget used
    tab2.configure(bg=theme)
    scoreFrame.configure(bg=theme)
    gameTitleFrame.configure(bg=theme)
    questionLogFrame.configure(bg=theme)
    questionFrame.configure(bg=theme)
    timerFrame.configure(bg=theme)
    correctIndicatorFrame.configure(bg=theme)
    answerCheckFrame.configure(bg=theme)
    numOfQuestionLogFrame.configure(bg=theme)
    gameTitleHeading.configure(bg=theme)
    numOfQuestionLogFrame.configure(bg=theme)
    levelTitle.configure(bg=theme)
    numOfQuestionLogFrame.configure(bg=theme)
    backButton.configure(bg=theme)
    scoreHeading.configure(bg=theme)
    correctHeading.configure(bg=theme)
    correctScoreHeading.configure(bg=theme)
    wrongHeading.configure(bg=theme)
    wrongScoreHeading.configure(bg=theme)
    totalHeading.configure(bg=theme)
    totalScoreHeading.configure(bg=theme)
    questionLogHeader.configure(bg=theme)
    questionLog.configure(bg=theme)
    integerDisplay1.configure(bg=theme)
    signDisplay.configure(bg=theme)
    integerDisplay2.configure(bg=theme)
    equalSign.configure(bg=theme)
    answerInput.configure(bg=theme)
    timerHeader.configure(bg=theme)
    countdownLabel.configure(bg=theme)
    resetButton.configure(bg=theme)
    submitButton.configure(bg=theme)
    correctIndicatorLabel.configure(bg=theme)
    correctIndicatorDisplay.configure(bg=theme)
    numOfQuestionsCompletedLabel.configure(bg=theme)
    numOfQuestionsCompleted.configure(bg=theme)
    numOfQuestionsLeftLabel.configure(bg=theme)
    numOfQuestionsLeft.configure(bg=theme)
    youAnswered.configure(bg=theme)
    youAnsweredLabel.configure(bg=theme)
    pokemonFrameDisplay.configure(bg=theme)
    correctAnswerIsLabel.configure(bg=theme)
    correctAnswerIs.configure(bg=theme)
    backButton.configure(highlightbackground=theme2, fg="black")
    resetButton.configure(highlightbackground=theme2, fg="black")
    submitButton.configure(highlightbackground=theme2, fg="black")
    answerInput.configure(highlightbackground=theme2)

# Function for start button
def start():
    global timer
    global resetBoolean
    timer = 100000
    reset()
    submit()
    resetSettings()
    getTimer()
    countdownLabel.configure(text=getTimer())
    
    # resetBoolean was used to make sure countdownn() only runs once, otherwise
    # the timer will overlap and make the timer move faster.
    if resetBoolean == 0:
        resetBoolean = 1
        getTimer()
        countdownn()

    tab_control.select(tab2)

# Function for submit button
def submit():
    global timer
    # Runs until game is over
    if int(totalScore) < int(numOfQ):
        # Updating all values
        calculateAns()
        checkAns()
        updateQuestionLog()
        updateAnswerCheck()
        updateNumOfQLog()
        updateProgressBar()
        generateRandomSign()
        generateRandomNum()
        answerInput.delete(0, END)
        answerInput.focus()

    # Finished questions
    else:
        finishedMessage = "You finished! You got " + str(correctScore) + " out of " + str(totalScore) + " correct. Thanks for playing!"
        res = messagebox.showerror("DONE!", finishedMessage)
        timer = 100000000000000000000000000
        countdownLabel.configure(text="Press Reset!")
        resetBoolean = 0

# ---------- VARIABLES ----------
# All globalized variables
level = 0
timer = 1
numOfQ = 0
resetBoolean = 0
theme = ""
theme2 = ""
negativeBoolean = False
randomIntegerMax = 0
operatorOptions = []
correctScore = 0
wrongScore = -1
totalScore = -1
randomInt1 = 0
randomInt2 = 0
randomSign = "+"
countdown = 0
correctIndicator = "CORRECT / WRONG"
ansInputted = 0
correctAns = 0
completed = 0
left = 0

# ---------- WIDGETS ----------
# TAB 1
# Game detail frame:
gameDetails = Frame(tab1)
gameTitleImage = PhotoImage(file="pokemon.png")
gameTitleDisplay = Label(gameDetails, image=gameTitleImage)

gameDescription = Label(gameDetails, text="Please select the options that you would like.", font=("Ariel", 25))

# Level frame:
levelFrame = Frame(tab1)
levelNum = IntVar()
levelNum.set(1) # setting default value
level1 = Radiobutton(levelFrame, text='Level 1', value=1, variable=levelNum)
level2 = Radiobutton(levelFrame, text='Level 2', value=2, variable=levelNum)
level3 = Radiobutton(levelFrame, text='Level 3', value=3, variable=levelNum)
level4 = Radiobutton(levelFrame, text='Level 4', value=4, variable=levelNum)

# Timer frame:
timerOptionFrame = Frame(tab1)
timerBoolean = IntVar()
timerNo = Radiobutton(timerOptionFrame, text='No Timer', value=0, variable=timerBoolean)
timerYes = Radiobutton(timerOptionFrame, text='Timer', value=1, variable=timerBoolean)
timerInput = Entry(timerOptionFrame, width=4)

# Number of questions frame:
numOfQuestions = Frame(tab1)
numOfQuestionsLabel = Label(numOfQuestions, text="Number of Questions:")
numOfQuestionsInput = Entry(numOfQuestions, width=3)
numOfQuestionsInput.insert(0, "5")

# Operator restrictions frame:
questionRestrictions = Frame(tab1)
includelbl = Label(questionRestrictions, text="Include:")

negatives_state = BooleanVar()
negatives_state.set(True)
addition_state = BooleanVar()
addition_state.set(True)
subtraction_state = BooleanVar()
subtraction_state.set(True)
multiplication_state = BooleanVar()
multiplication_state.set(True)
modulus_state = BooleanVar()
modulus_state.set(True)
division_state = BooleanVar()
division_state.set(True)

negatives = Checkbutton(questionRestrictions, text="Negatives?", var=negatives_state)
addition = Checkbutton(questionRestrictions, text="Addition?", var=addition_state)
subtraction = Checkbutton(questionRestrictions, text="Subtraction?", var=subtraction_state)
multiplication = Checkbutton(questionRestrictions, text="Multiplication?", var=multiplication_state)
modulus = Checkbutton(questionRestrictions, text="Modulus?", var=modulus_state)
division = Checkbutton(questionRestrictions, text="Division?", var=division_state)

# Theme frame:
themeFrame = Frame(tab1)
themelbl = Label(themeFrame, text="Theme:")

themeNum = IntVar()
themeNum.set(1) # setting default value
orangeTheme = Radiobutton(themeFrame, text='Orange', value=1, variable=themeNum)
blueTheme = Radiobutton(themeFrame, text='Blue', value=2, variable=themeNum)
yellowTheme = Radiobutton(themeFrame, text='Yellow', value=3, variable=themeNum)
greenTheme = Radiobutton(themeFrame, text='Green', value=4, variable=themeNum)

# Start frame:
startFrame = Frame(tab1)
startButton = Button(startFrame, text="START", command = start)

# TAB 2
# Game title frame
gameTitleFrame = Frame(tab2)
gameTitleHeading = Label(gameTitleFrame, text="Level:", font=("Ariel", 35))
levelTitle = Label(gameTitleFrame, text=level, font=("Ariel", 35))

# Back button frame
backButtonFrame = Frame(tab2)
backButton = Button(backButtonFrame, text="BACK", font=("Ariel", 25), command=back)

# Score display frame
scoreFrame = Frame(tab2)
scoreHeading = Label(scoreFrame, text="SCORE:", font=("Ariel", 25))
correctHeading = Label(scoreFrame, text="Correct: ", font=("Ariel", 20))
correctScoreHeading = Label(scoreFrame, text=correctScore, font=("Ariel", 20))
wrongHeading = Label(scoreFrame, text="Wrong: ", font=("Ariel", 20))
wrongScoreHeading = Label(scoreFrame, text=wrongScore, font=("Ariel", 20))
totalHeading = Label(scoreFrame, text="Total: ", font=("Ariel", 20))
totalScoreHeading = Label(scoreFrame, text=totalScore, font=("Ariel", 20))

# Question frame
questionFrame = Frame(tab2)
integerDisplay1 = Label(questionFrame, text=randomInt1, font=("Ariel", 50))
signDisplay = Label(questionFrame, text=randomSign, font=("Ariel", 50))
integerDisplay2 = Label(questionFrame, text=randomInt2, font=("Ariel", 50))
equalSign = Label(questionFrame, text="=", font=("Ariel", 50))
answerInput = Entry(questionFrame, width=3, font=("Ariel", 50), borderwidth = 3)

# Submit button frame
submitFrame = Frame(tab2)
submitButton = Button(submitFrame, text="SUBMIT", font=("Ariel", 25), bg="red", command=submit)

# Question log frame
questionLogFrame = Frame(tab2)
questionLogHeader = Label(questionLogFrame, text="QUESTION LOG", font=("Ariel", 25))
questionLog = scrolledtext.ScrolledText(questionLogFrame, width=13, height=3, font=("Ariel", 20))

# Answer check frame (you answered:... correct answer is...)
answerCheckFrame = Frame(tab2)
youAnsweredLabel = Label(answerCheckFrame, text="You answered:", font=("Ariel", 20))
youAnswered = Label(answerCheckFrame, text=ansInputted, font=("Ariel", 20), fg="red")
correctAnswerIsLabel = Label(answerCheckFrame, text="Correct answer is:", font=("Ariel", 20))
correctAnswerIs = Label(answerCheckFrame, text=correctAns, font=("Ariel", 20), fg="green")

# Correct / wrong checker frame
correctIndicatorFrame = Frame(tab2)
correctIndicatorLabel = Label(correctIndicatorFrame, text=correctIndicator, font=("Ariel", 25))
correctIndicatorImage = PhotoImage(file='pokeball.png')
correctIndicatorDisplay = Label(correctIndicatorFrame, image = correctIndicatorImage)

# Progress bar frame
progressBarFrame = Frame(tab2)
bar = Progressbar(progressBarFrame, length=200)
bar['value'] = 0

# Number of questions completed and left frame
numOfQuestionLogFrame = Frame(tab2)
numOfQuestionsCompletedLabel = Label(numOfQuestionLogFrame, text="Questions Completed:", font=("Ariel", 25))
numOfQuestionsCompleted = Label(numOfQuestionLogFrame, text=completed, font=("Ariel", 25))
numOfQuestionsLeftLabel = Label(numOfQuestionLogFrame, text="Questions Left:", font=("Ariel", 25))
numOfQuestionsLeft = Label(numOfQuestionLogFrame, text=left, font=("Ariel", 25))

# Reset button frame
resetFrame = Frame(tab2)
resetButton = Button(resetFrame, text="RESET", font=("Ariel", 25), command=reset)

# Timer frame
timerFrame = Frame(tab2)
timerHeader = Label(timerFrame, text="TIMER", font=("Ariel", 25))
countdownLabel = Label(timerFrame, text=countdown, font=("Ariel", 25))

# Pokemon frame
pokemonFrame = Frame(tab2)
pokemonFrameImage = PhotoImage(file="") # **IMPORT FILE**
pokemonFrameDisplay = Label(pokemonFrame, image = pokemonFrameImage)

# ---------------------------------------------------------------------
# ---------- GRID ----------
# --- GRID FRAMES ---
# TAB 1
gameDetails.grid(column=0, row=0)
levelFrame.grid(column=0, row=1)
timerOptionFrame.grid(column=0, row=2)
numOfQuestions.grid(column=0, row=3)
questionRestrictions.grid(column=0, row=4)
themeFrame.grid(column=0, row=5)
startFrame.grid(column=0, row=6)

# TAB 2
scoreFrame.grid(column=0, row=0, padx=10, pady=10)
gameTitleFrame.grid(column=1, row=0, padx=10, pady=10)
backButtonFrame.grid(column=2, row=0, padx=10, pady=10)
questionLogFrame.grid(column=0, row=1, padx=10, pady=10)
questionFrame.grid(column=1, row=1, padx=10, pady=10)
timerFrame.grid(column=2, row=1, padx=10, pady=10)
resetFrame.grid(column=0, row=2, padx=10, pady=10)
submitFrame.grid(column=1, row=2, padx=10, pady=10)
correctIndicatorFrame.grid(column=2, row=2, padx=10, pady=10)
answerCheckFrame.grid(column=2, row=3, padx=10, pady=10)
progressBarFrame.grid(column=1, row=3, padx=10, pady=10)
numOfQuestionLogFrame.grid(column=0, row=3, padx=10, pady=10)
pokemonFrame.grid(column=0, row=4, padx=10, pady=10)

# --- GRID WIDGETS ---
# TAB 1
gameTitleDisplay.grid(column=0, row=0, sticky=N+E+S+W, padx=10, pady=10)
gameDescription.grid(column=0, row=1, sticky=N+E+S+W, padx=10, pady=10)

level1.grid(column=0, row=0)
level2.grid(column=1, row=0)
level3.grid(column=2, row=0)
level4.grid(column=3, row=0)

timerNo.grid(column=0, row=0)
timerYes.grid(column=1, row=0)
timerInput.grid(column=1, row=1)

numOfQuestionsLabel.grid(column=0, row=0)
numOfQuestionsInput.grid(column=1, row=0)

includelbl.grid(column=0, row=0)
negatives.grid(column=1, row=0)
addition.grid(column=2, row=0)
subtraction.grid(column=3, row=0)
multiplication.grid(column=4, row=0)
modulus.grid(column=5, row=0)
division.grid(column=6, row=0)

themelbl.grid(column=0, row=0)
orangeTheme.grid(column=1, row=0)
blueTheme.grid(column=2, row=0)
yellowTheme.grid(column=3, row=0)
greenTheme.grid(column=4, row=0)

startButton.grid(column=0, row=0)

# TAB 2
gameTitleHeading.grid(column=0, row=0)
levelTitle.grid(column=1, row=0)

backButton.grid(column=0, row=0)

scoreHeading.grid(column=0, row=0)
correctHeading.grid(column=0, row=1)
correctScoreHeading.grid(column=1, row=1)
wrongHeading.grid(column=0, row=2)
wrongScoreHeading.grid(column=1, row=2)
totalHeading.grid(column=0, row=3)
totalScoreHeading.grid(column=1, row=3)

questionLogHeader.grid(column=0, row=0)
questionLog.grid(column=0, row=1)

integerDisplay1.grid(column=0, row=0)
signDisplay.grid(column=1, row=0)
integerDisplay2.grid(column=2, row=0)
equalSign.grid(column=3, row=0)
answerInput.grid(column=4, row=0)

timerHeader.grid(column=0, row=0)
countdownLabel.grid(column=0, row=1)

resetButton.grid(column=0, row=0)

submitButton.grid(column=0, row=0)

correctIndicatorLabel.grid(column=0, row=0)
correctIndicatorDisplay.grid(column=0, row=1)

numOfQuestionsCompletedLabel.grid(column=0, row=0)
numOfQuestionsCompleted.grid(column=1, row=0)
numOfQuestionsLeftLabel.grid(column=0, row=1)
numOfQuestionsLeft.grid(column=1, row=1)

bar.grid(column=0, row=0)

youAnsweredLabel.grid(column=0, row=0)
youAnswered.grid(column=1, row=0)
correctAnswerIsLabel.grid(column=0, row=1)
correctAnswerIs.grid(column=1, row=1)

pokemonFrameDisplay.grid(column=0, row=0)
