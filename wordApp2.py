from flask import Flask, render_template, url_for, request, redirect, flash, session

import random, linecache, re, time, collections
from threading import Thread
#from natsort import natsorted

app = Flask(__name__)

###############################################################################################
# A1. Display landing Page - gives user a button to start the game

@app.route('/')
def display_home():
    return render_template("wordHome.html",
                            the_title="Word Game",
                            startGame=url_for("getWord"),
                            home_link = url_for("display_home"),
                            justScores = url_for("showScores"),
                            aboutPage = url_for("aboutPage"),)
			                
###############################################################################################	
# A2. Display game start page, display word to user		                
			                
@app.route('/startGame')
def getWord():
    num = 53354 #cWordLists() For speed, I have hard coded the number of words in the 7-letter word file
    #ranLine = linecache.getline('7_over_wordList', random.randint(1, num))
    
    #session['ranLine'] = ranLine[:-1].lower()
    ranLine = random.choice(list(open('7_over_wordList'))).rstrip()
    session['ranLine'] = ranLine
    session['sTime'] = time.time()
    return render_template("wordStart.html",
                            the_title="Enter 7 Words",
                            ranWord = ranLine,
                            subWords=url_for("scanWords"),
                            home_link = url_for("display_home"),
                            justScores = url_for("showScores"),
                            aboutPage = url_for("aboutPage"),)
                            
def cWordLists():                       
    with open('/usr/share/dict/words') as wordListS:                
        with open('3_over_wordList','w') as bList:
            for lineB in wordListS:
                lineB = lineB[:-1]
                if re.match("^[a-zA-Z]*$", lineB): 
                    if len(lineB) >= 3 :
                        print(lineB, file=bList)
                    
    with open('/usr/share/dict/words') as wordListL:
        i = 0
        with open('7_over_wordList','w') as aList:
            for lineA in wordListL:
                lineA = lineA[:-1]
                if re.match("^[a-zA-Z]*$", lineA):
                    if len(lineA) >= 7:
                        i += 1       
                        print(lineA, file=aList)
        return i
        
################################################################################################

@app.route('/submitWords', methods=["POST"])
def scanWords():
    all_ok=True
    session['timeTaken'] = str(round(time.time() - session['sTime'], 2))    
        
    results = ['','','','','','','']
    userWords = []
    userWords.append(request.form['word1'].lower())
    userWords.append(request.form['word2'].lower())
    userWords.append(request.form['word3'].lower())
    userWords.append(request.form['word4'].lower())
    userWords.append(request.form['word5'].lower())
    userWords.append(request.form['word6'].lower())
    userWords.append(request.form['word7'].lower())
    
    duplicates = list(dupCheck(userWords))
    
    with open('3_over_wordList','r') as rWords:
        rWordList = list(rWords)
        for ind, wrd in enumerate(userWords):
            if len(userWords[ind]) <=2:
                results[ind] = 'Word is too short or empty'
                
            elif userWords[ind] in duplicates:
                results[ind] = 'Duplicate Word'
                
            elif userWords[ind] == session['ranLine']:
                results[ind] = 'Same as source word'
            
            else:            
                for line in rWordList:
                    line = line[:-1]
                    if userWords[ind] == line:
                        results[ind] = 'Valid Word'
                     
                    
                
    for ind2, wrd2 in enumerate(userWords):
        if contains(session['ranLine'], userWords[ind2]) == False:
            if not results[ind2]:
                results[ind2] = 'Word not in source word'
            
    for ind3, wrd3 in enumerate(results):
        if results[ind3] != 'Valid Word':
            all_ok = False
            
    if all_ok:
        for ind3, wrd3 in enumerate(results):
            results[ind3] = 'Valid Word'
        return render_template("wordResults.html",
                            the_title="Your Results",
                            word1 = userWords[0],
                            word2 = userWords[1],
                            word3 = userWords[2],
                            word4 = userWords[3],
                            word5 = userWords[4],
                            word6 = userWords[5],
                            word7 = userWords[6],
                            result1 = results[0],
                            result2 = results[1],
                            result3 = results[2],
                            result4 = results[3],
                            result5 = results[4],
                            result6 = results[5],
                            result7 = results[6],
                            timeTaken = session['timeTaken'],
                            outcome = 'Congratulations, you played well. Enter your name to see where you rank.',
                            resFormAction = url_for("updateScore"),                           
                            home_link = url_for("display_home"),
                            justScores = url_for("showScores"),
                            aboutPage = url_for("aboutPage"),)

    elif all_ok==False:
        insults = ["Did you hit your head before that attempt? Failed.", "That really was bad, you failed", "A child could do better. Failed.", "Nope, no good, try again.", "You suck at this game, try again"]
        chInsult = random.choice(insults)
        for ind3, wrd3 in enumerate(results):
            if results[ind3] == '':
                results[ind3] = 'Not a real Word'
        for ind4, wrd4 in enumerate(userWords):
            if userWords[ind4] == '':
                userWords[ind4] = '*** No User Word Entered ***'
        return render_template("wordResults.html",
                            the_title="Your Results",
                            word1 = userWords[0],
                            word2 = userWords[1],
                            word3 = userWords[2],
                            word4 = userWords[3],
                            word5 = userWords[4],
                            word6 = userWords[5],
                            word7 = userWords[6],
                            result1 = results[0],
                            result2 = results[1],
                            result3 = results[2],
                            result4 = results[3],
                            result5 = results[4],
                            result6 = results[5],
                            result7 = results[6],
                            timeTaken = session['timeTaken'],
                            outcome = chInsult,
                            resFormAction = url_for("getWord"),
                            home_link = url_for("display_home"),
                            justScores = url_for("showScores"),
                            aboutPage = url_for("aboutPage"),)            
        
def freq_count(letters):
    f_count = {}
    for char in letters:
        f_count.setdefault(char, 0)
        f_count[char] += 1
    return f_count

def contains(source_word, what):
    sc = freq_count(source_word)
    wc = freq_count(what)
    for letter, count in wc.items():
        if sc.get(letter, 0) < count:
            return False
    return True
    
def dupCheck(userWords):
    dupSet = collections.Counter(userWords)
    dups = [i for i in dupSet if dupSet[i]>1]    
    return dups   
#####################################################################################################

@app.route('/scoreBoard', methods=["POST"])
def updateScore():
    userName = request.form['nameBox']
    if userName == '':
        userName = 'Anonymous'
    userDetails = session['timeTaken'] + ' seconds by ' + userName    
    #scoreUpdateThread = Thread(target=scoreThread, args=(userDetails))
    #scoreUpdateThread.start()
    with open('scores', 'a') as scores:
        print(userDetails, file=scores)
    boardPos = 0
    with open('scores', 'r') as scores:
        lineList = scores.readlines()
        #lineList = natsorted(lineList)
        lineList = humanSort(lineList)
        for i in [i for i,x in enumerate(lineList) if x == userDetails + '\n']:
            boardPos = i + 1
                        
        shortList=[]
        for i in range(10):
            shortList.append(lineList[i])
        #shortList = natsorted(shortList)
        shortList = humanSort(shortList)
        
    if boardPos <= 10:
        scoreResults = ('Your in the top ten! You ranked number ' + str(boardPos) + ' !')
    elif boardPos > 10:
        scoreResults = ('You didn\'t make the top ten, you ranked number ' + str(boardPos) + '.')

    return render_template("wordScores.html",
                            the_title = 'Scoreboard',
                            shortList = shortList,
                            scoreResults = scoreResults,
                            replay=url_for("getWord"),
                            resFormAction = url_for("getWord"),
                            home_link=url_for("display_home"),                            
                            justScores = url_for("showScores"),
                            aboutPage = url_for("aboutPage"),)
                            
#def scoreThread(userDetails):
#    #time.sleep(10)
#    with open('scores', 'a') as scores:
#        print(userDetails, file=scores)
    
                            
###############################################################################################
                            
@app.route('/justScores')
def showScores():
    with open('scores', 'r') as scores:
        lineList = scores.readlines()
        #lineList = natsorted(lineList)
        lineList = humanSort(lineList)
        
                        
        shortList=[]
        for i in range(10):
            shortList.append(lineList[i])
        #shortList = natsorted(shortList)
        shortList = humanSort(shortList)

    return render_template("wordScores.html",
                            the_title = 'Scoreboard',
                            shortList = shortList,
                            scoreResults = "Are you in the top ten?",
                            replay=url_for("getWord"),
                            resFormAction = url_for("getWord"),
                            home_link=url_for("display_home"),                            
                            justScores = url_for("showScores"),
                            aboutPage = url_for("aboutPage"),)
                            
def humanSort(l):
    
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key = alphanum_key)
    
##############################################################################################

@app.route('/aboutWord')
def aboutPage():
    return render_template("wordAbout.html",
                            resFormAction = url_for("getWord"),
                            home_link=url_for("display_home"),
                            justScores = url_for("showScores"),
                            aboutPage = url_for("aboutPage"),)

if __name__ == "__main__":
    app.config['SECRET_KEY'] = 'thisismysecretkeywhichyouwillneverguesshahahahahahahaha'
    app.run(debug=True)
