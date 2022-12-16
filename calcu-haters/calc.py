from math import sin, cos, tan, log10, sqrt, pi, degrees, factorial

def lenFromItem(lst,char):
    return len(lst)-lst.index(char)
def removeAll(lst, itm):
    tmp=[]
    for item in lst:
        if not(itm==item):
            tmp.append(item)
    return tmp
def strConv(lst):
    tmp=""
    for item in lst:
        tmp+=item
    return tmp
def myReplace(usin,search,instead,index,amnt=0):
    newUsin=usin[index:len(usin)] #splits string at index
    if amnt<1:
        newUsin=newUsin.replace(search,instead) #replace all instances of sub
    else:
        newUsin=newUsin.replace(search,instead,amnt)#replace amnt instances of sub
    return usin[0:index]+newUsin #combine the entire string before index and string just worked on and returns it
def total(lst):
    total=0
    for item in lst:
        total+=item
    return total

##########UNUSED##########
def findall(search, sub):
    if not isinstance(search, str):
        raise TypeError("Argument \"search\" must be str, recieved type "+str(type(search)))
    if not isinstance(sub,str):
        raise TypeError("Argument \"sub\" must be str, recieved type "+str(type(sub)))
    instances=[] #list of all found indexes
    start=0 #stores the index of the last instance of sub, used as starting point for searching
    usin=search #stores what search was before splitting
    #finds all instances of sub in search
    #this is the shittiest possible implementation, but it'll fucking work
    tmp=search.find(sub)
    if tmp==-1:
        return [] #return -1 if there are no instances of sub in search
    
    instances.append(tmp)
    start=tmp+len(sub)
    while True:
        tmp2=(usin[:start],usin[start:])
        off=len(tmp2[0])
        search=tmp2[1]
        tmp=search.find(sub) #avoids multiple uses of find, might save cpu time
        if tmp==-1:
            break
        else:
            instances.append(tmp+off)
        start=tmp+off+len(sub)
        if len(instances)>1000:
            raise RuntimeError("Halted at infinete loop")
    return instances
def factForm(usin):

    facts=len(findall(usin,"!"))
    for i in range(facts):
    
        num=""
        factInd=0
        lenFact=0
        for j in range(0,len(usin)):
            if usin[j]=="!":
                for k in range(j-1,-1,-1):
                    if usin[k].isnumeric() or usin[k]==".":
                        num+=usin[k]
                        
                    else:
                        factInd=k+1
                        break
                    lenFact+=1
                num=str(factorial(float(num)))
                break
        """
        newsin=""
        for j in range(0,factInd):
            newsin+=usin[j]
        newsin+=num
        for j in range(factInd+lenFact+1,len(usin)):
            newsin+=usin[j]
        """
        usin=usin[0:factInd]+num+usin[factInd+lenFact+1:]
    return usin


def myFormat(usin):
    #formats the raw user input into something calc() can understand
    #replaces shorthands (like using 4(5) to represent 4*5)
    #removes spaces
    usin=usin.replace(" ","") #remove spaces
    #remove spaces and replace all multi-char sequences (sin, cos, tan, etc.)
    #with special non-alphanumeric characters.
    
    #in this case "{" represents sin, "}" is cos, "?" is tan, and "@" is log
    usin=usin.replace("sin","{")
    usin=usin.replace("cos","}")
    usin=usin.replace("tan","?")
    usin=usin.replace("log","@")
    usin=usin.replace("sqrt","_")

    usin=factForm(usin)
    #inserts a parenthesis between double signs, like "+-" and "*-"
    badchars="+-*/%"
    nums="0123456789"
    
    for i in range(0,len(nums)):
        if i<len(badchars):
            bad=badchars[i]+"-" #substring we wish to replace, creadted by combining an operator with a subtraction sign, ex "+-" or "*-"
            good=badchars[i]+"(-" #substring we wish to replace with, create by inserting a parenthesis between the the sub sign, ex "+(-" or "*(-"
            indexes=(findall(usin,bad))#get all instances of bad
            if indexes!=[]:
                indexes.reverse() #reverses list so that the last elements in the string are done first, meaning that the index of the next element is never wrong
                for i in range(0,len(indexes)): #for each item:
                    usin=myReplace(usin,bad,good,indexes[i],1)#replace instance at index indexes[i]
                    count=indexes[i]+3 #store value of indexs[i]+3 for starting value
                    added=False
                    while usin[count].isdigit() or usin[count]==".":
                        count+=1
                        if count>=len(usin):
                            usin+=")"
                            added=True
                    if not added:
                        usin=usin[0:count]+")"+usin[count]+usin[count:len(usin)]
        usin=usin.replace(nums[i]+"(",nums[i]+"*(")
    usin=usin.replace(")(",")*(")
    return usin
def calc(usin,mode="d"):
    #raise TypeError if usin is not a string
    #further try-excepts will be used for alpha characters and division by zero

    if not isinstance(usin, str):
        raise TypeError("\"usin\" must be a str")
    usin=myFormat(usin)
    if mode=="d":
        d=1*pi/180
    else:
        d=1
    tmp=0 #temporary value, used across entire function
    tmp2="" #temporary str value, used across entire function
    tmp3=[] #temporary array value, used across entire function
    banned="+-/*%^" #all chars which will cause usual exit of search routine
    trigs="{}?@_" #all chars which will cause "trig" exit of search routine
    numberchars="0123456789."
    numeric=[] #stores numbers that are "in progress"
    numbers=[] #stores all found numbers
    

    #finds all parenthesis and recurses to find a solution

    start=usin.find("(")#find first paren
    if start!=-1:
        position=start+1
        recurse=""
        parens=1
        closeParens=0
        while parens!=closeParens:
            if usin[position]==")":
                closeParens+=1
            elif usin[position]=="(":
                parens+=1
            else:
                recurse+=usin[position]
            position+=1
        usin=usin.replace(usin[start:position],str(calc(usin[start+1:position-1])))  
    #takes in all instances of "^" and adds a parenthesis in front as expected
    #this allows for only one implementation of "^" handling
    off=0        
        
    #extract numbers from string    
    decimal=0 #variable that stores which index contains the decimal point
    neg=False #boolean indicating if number being extracted is negative
    for char in usin: #for each char in string
        if not char.isnumeric() and char !=".": #if char is a function char
            if numbers==[] and numeric==[]: #if numbers is empty
                if char=="-":
                    neg=True
                elif trigs.find(char)==-1:
                    raise ValueError("Operator character \""+char+"\" found before number")
            else:
                number=0
                try:
                    place=numeric.index(".") #if a decimal place exists, subtract its index from places
                except ValueError: #if a decimal doesn't exist
                    place=len(numeric)-1 #subtract 1 from places
                except Exception as error:
                    raise error #otherwise raise an error
                for digit in numeric:
                    if digit==".":
                        number/=10
                    elif digit!=".":
                        number+=int(digit)*(10**place)
                    place-=1
                if neg: #if the number is negetive
                    number*=-1 #multiply it by -1
                    neg=False #disable neg boolean
                numbers.append(number)
                numeric=[]
        else:
            numeric.append(char)
    if numeric!=[]:
        number=0
        try:
            place=numeric.index(".")
        except ValueError:
            place=len(numeric)-1
        for digit in numeric:
            if digit!=".":
                number+=int(digit)*(10**place)
            place-=1
        numbers.append(number)
    del numeric
    del off
    del number
    del start
    del trigs
    del place
    
    for char in numberchars:
        usin=usin.replace(char,"")
    for number in numbers:
        if number<0:
            usin=usin.replace("-","",1)
    count=0
    newNumber=""
    #actually calculate the thing
    #start with trig functions
    while count<len(usin):
        char=usin[count]
        if char=="_": #square root
            newNumber=sqrt(numbers[count])
        elif char=="{": #sin
            newNumber=sin(numbers[count]*d)
        elif char=="}": #cos
            newNumber=cos(numbers[count]*d)
        elif char=="?": #tan
            newNumber=tan(numbers[count]*d)
        elif char=="@": #log10
            newNumber=log10(numbers[count])
        elif banned.find(char)==-1:
            raise ValueError("String contained nonusable character \""+usin[count]+"\"")
        if newNumber!="":
            numbers[count]=newNumber
            print(numbers)
            newNumber=""
        count+=1
        
    count=0
    usin=usin.replace("_","")
    usin=usin.replace("}","")
    usin=usin.replace("}","")
    usin=usin.replace("?","")
    usin=usin.replace("@","")
    #next with exponents
    usin=usin[::-1]
    numbers.reverse()
    while count<len(usin) and not len(numbers)==1:
        newNumber=""
        char=usin[count]
        if char=="^":
            tmp=count
            tmp2=count+1
            while numbers[tmp2]=="":
                tmp2+=1
            while numbers[tmp]=="":
                tmp-=1
            newNumber=(numbers[tmp2]**numbers[tmp])
        elif banned.find(char)==-1:
            raise ValueError("String contained nonusable character \""+usin[count]+"\"")
        if newNumber!="":
            tmp3=[]#list to do work on
            for i in range(0,tmp):
                tmp3.append(numbers[i]) #append all previous items of "numbers"
            tmp3.append(newNumber) #append the actual number
            tmp3.append("") #append a null value (later removed) to keep length of list consistant and avoid incorrect index references
            for i in range(count+2,len(numbers)):
                tmp3.append(numbers[i])#append the rest of the list
            numbers=tmp3.copy()
        count+=1
    count=0
    usin=usin.replace("^","")
    numbers.reverse()
    usin=usin[::-1]
    #now multipllication and division
    
    while count<len(usin):
        newNumber=""
        if len(numbers)==1:
            break
        char=usin[count]
        if char=="*":
            #introducing the "null string" approach for calculation creates a situation where math could be attempted on null string, crashing the program
            #therefore, we have to make sure we're not doing math on null strings
            tmp=count
            tmp2=count+1
            while numbers[tmp2]=="":
                tmp2+=1
            while numbers[tmp]=="":
                tmp-=1
            newNumber=(numbers[tmp]*numbers[tmp2])
            
        elif char=="/":
            tmp=count
            tmp2=count+1
            while numbers[tmp2]=="":
                tmp2+=1
            while numbers[tmp]=="":
                tmp-=1
            newNumber=(numbers[tmp]/numbers[tmp2])
        elif char=="%":
            tmp=count
            tmp2=count+1
            while numbers[tmp2]=="":
                tmp2+=1
            while numbers[tmp]=="":
                tmp-=1
            newNumber=(numbers[tmp]%numbers[tmp2])
        #calculations done

        #replacing old numbers with new ones.
        if newNumber!="":
            tmp3=[]#list to do work on
            for i in range(0,tmp):
                tmp3.append(numbers[i]) #append all previous items of "numbers"
            tmp3.append(newNumber) #append the actual number
            tmp3.append("") #append a null value (later removed) to keep length of list consistant and avoid incorrect index references
            for i in range(count+2,len(numbers)):
                tmp3.append(numbers[i])#append the rest of the list
            numbers=tmp3.copy()
        count+=1
    count=0
##    print("##########")
##    print("Old Nums:")
##    print(numbers)
##    print()
    numbers=removeAll(numbers,"")
##    print("New Nums:")
##    print(numbers)
##    print("##########")
    usin=usin.replace("*","")
    usin=usin.replace("/","")
##    print("usin = "+usin)
##    print("Numbers: "+str(numbers))
##    print("Adding/Subbing...")
##    print()
##    print("----------")
##    print()
    
    #finally adding and subbing
    while count<(len(usin)):
        if len(numbers)==1:
            break
        newNumber=""
        char=usin[count]
        if char=="+":
            tmp=count
            tmp2=count+1
            while numbers[tmp2]=="" and tmp2:
                tmp2+=1
            while numbers[tmp]=="":
                tmp-=1
            newNumber=(numbers[tmp]+numbers[tmp2])
        elif char=="-":
            tmp=count
            tmp2=count+1
            while numbers[tmp2]=="":
                tmp2+=1
            while numbers[tmp]=="":
                tmp-=1
            newNumber=(numbers[tmp]-numbers[tmp2])
        if newNumber!="":
            tmp3=[]#list to do work on
            for i in range(0,tmp):
                tmp3.append(numbers[i]) #append all previous items of "numbers"
            tmp3.append(newNumber) #append the actual number
            tmp3.append("") #append a null value (later removed) to keep length of list consistant and avoid incorrect index references
            for i in range(count+2,len(numbers)):
                tmp3.append(numbers[i])#append the rest of the list
            numbers=tmp3.copy()
        count+=1
    #converts unneeded floating points into ints ("5.0" to "5")
    if numbers[0]==int(numbers[0]):
        numbers[0]=int(numbers[0])
    
    return numbers[0]
def readtests(infile):
    
    tests=[]
    for line in infile:
        line=line.strip("\n")
        if line!="" and line[0]!="#":
            tests.append(line.split(","))
    for test in tests:
        test=(test[0],float(test[1]))
    return tests
"""def tests():
    infile=open("F:/calcuhate/tests.txt","r")
    tests=readtests(infile)
    infile.close()
    failures=[]
    fuckedup=False
    errortups=[]
    for i in range(0,len(tests)):
        print("Performing test "+str(i+1))
        try:
            result=calc(tests[i][0])
        except Exception as err:
            raise err
            print("Test "+str(i+1)+" failed!")
            print("Raised Error "+str(err))
            failures.append(((i+1),"exception"))
            if not fuckedup:
                errortups.append((i+1,tests[i][1],err))
            fuckedup=True
        else:
            if result==float(tests[i][1]): #makes test result float to account for decimal tests
                print("Test "+str(i+1)+" is good")
            else:
                print("Test "+str(i+1)+" failed!")
                print("Expected "+str(tests[i][1])+", got "+str(result))
                failures.append((i+1,tests[i][1],result))
    if failures==[]:
        print("All tests sucessfull!!!")
    else:
        print("Some tests failed")
        print("A sit-rep:")
        for fail in failures:
            print("Test "+str(fail[0])+" should have returned "+str(fail[1])+", but instead we got "+str(fail[2]))
        if fuckedup:
            print("Furthermore, there were some exceptions")
            print("A quick rundown:")
            for test in errortups:
                print("Test #"+str(test[0])+" raised \""+str(test[1])+"\"")
        else:
            print("At least there wasn't any exceptions!")"""
def manTests():

    print(calc("0.8+0.7"))
    inpt=" "
    while inpt[0]!="N":
        inpt=input("Enter equation to calculate: ")
        try:
            print("Passed with a value of "+str(calc(inpt)))
        except Exception as e:
            print("Raised exception \""+str(e.__class__.__name__)+"\"")
            inpt=input("Raise?: ").upper()
            if inpt[0]=="Y":
                raise e
        inpt=input("Again?: ").upper()
#manTests()
