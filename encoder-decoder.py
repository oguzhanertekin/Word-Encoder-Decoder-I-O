import os.path
import sys

letterValue={"A":1,"B":2,"C":3,"D":4,"E":5,"F":6,"G":7,"H":8,"I":9,"J":10,"K":11,\
                 "L":12,"M":13,"N":14,"O":15,"P":16,"Q":17,"R":18,"S":19,"T":20,"U":21,\
                 "V":22,"W":23,"X":24,"Y":25,"Z":26," ":27}

numValue={1:"A",2:"B",3:"C",4:"D",5:"E",6:"F",7:"G",8:"H",9:"I",10:"J",11:"K",\
              12:"L",13:"M",14:"N",15:"O",16:"P",17:"Q",18:"R",19:"S",20:"T",21:"U",\
              22:"V",23:"W",24:"X",25:"Y",26:"Z",27:" "}
validNumbers=["1","2","3","4","5","6","7","8","9","0",",","-"]
try:
    if len(sys.argv)!=5:
        raise Exception("Parameter number error")
    elif sys.argv[1]!="enc" and sys.argv[1]!="dec":
        raise Exception("Undefined parameter error")
    elif not sys.argv[3].endswith(".txt"):
        raise Exception("The input file could not be read error")
    elif not os.path.exists(sys.argv[3]):
        raise Exception("Input file not found error")
    elif os.path.exists(sys.argv[3]):
        if os.stat(sys.argv[3]).st_size == 0:
            raise Exception("Input file is empty error")
        else:
            if "plain_input.txt" in sys.argv[3]:
                file=open(sys.argv[3],"r")
                line=file.readline().strip("\n ")
                for character in line.upper():
                    if character not in letterValue:
                        raise Exception("Invalid character in input file error")
                file.close()
            elif "ciphertext.txt" in sys.argv[3]:
                file=open(sys.argv[3],"r")
                line=file.readline().strip("\n ")
                for character in line:
                    if character not in validNumbers:
                        raise Exception("Invalid character in input file error")
                file.close()

    if not sys.argv[2].endswith(".txt"):
        raise Exception("Key file could not be read error")
    elif not os.path.exists(sys.argv[2]):
        raise Exception("Key file not found error")
    elif os.path.exists(sys.argv[2]):
        if os.stat(sys.argv[2]).st_size == 0:
            raise Exception("Key file is empty error")
        else:
            file = open(sys.argv[2], "r")
            line = file.readlines()
            for characters in line:
                characters = characters.strip("\n ")
                for character in characters:
                    if character not in validNumbers:
                        raise Exception("Invalid character in key file error")
            file.close()

except Exception as error:
    print(error)

else:
    operation=sys.argv[1]
    key_path=sys.argv[2]
    input_path=sys.argv[3]
    output=sys.argv[4]

    keyFile=open(key_path,"r")
    keyList=keyFile.readlines()  
    size=len(keyList)  # SIZE OF MATRIX
    keyFile.close()

    def convert(x):  # Shows the letter or number corresponding letter or number
        if x in letterValue:
            return letterValue[x]
        elif x in numValue:
            return numValue[x]

    def key(keyList):  # It holds key matrix in it ---> e.g [[1,2][2,3]]
        key_matrix=[]
        for line in keyList:
            line=line.strip("\n").split(",")
            key_matrix.append([int(num) for num in line])
        return key_matrix

    def multiply(list1):  # It multiplies key matrix with main text's number values (encrypted or decrypted)
        global keyList
        key_matrix=key(keyList)
        encoded = [0 for i in range(0, len(key_matrix))]
        sum1 = 0
        for i in range(0, len(key_matrix)):
            for j in range(0, len(key_matrix)):
                sum1 += key_matrix[i][j] * list1[j]
            encoded[i] = sum1
            sum1 = 0
        return encoded

    def inverse(list_2d):  # It takes inverse of key matrix
        if len(list_2d) == 2:
            inverseList = [0, 0]
            inverseList[0] = ",".join([str(list_2d[1][1]), str(-list_2d[0][1])])
            inverseList[1] = ",".join([str(-list_2d[1][0]), str(list_2d[0][0])])
            return inverseList
        if len(list_2d)==3:
            inverseList = [0,0,0]
            a,b,c=int(list_2d[0][0]),int(list_2d[0][1]),int(list_2d[0][2])
            d,e,f=int(list_2d[1][0]),int(list_2d[1][1]),int(list_2d[1][2])
            g,h,i=int(list_2d[2][0]),int(list_2d[2][1]),int(list_2d[2][2])
            determinant=a*((e*i)-(f*h)) -b*((d*i)-(f*g)) +c*((d*h)-(e*g))
            x=determinant
            adjugate_0=[str(x*(e*i-f*h)),str(x*(-b*i+c*h)),str(x*(b*f-c*e))]
            adjugate_1=[str(x*(-d*i+f*g)),str(x*(a*i-c*g)),str(x*(-a*f+c*d))]
            adjugate_2=[str(x*(d*h-e*g)),str(x*(-a*h+b*g)),str(x*(a*e-b*d))]
            inverseList[0]= ",".join(adjugate_0)
            inverseList[1]= ",".join(adjugate_1)
            inverseList[2]= ",".join(adjugate_2)
            return inverseList

    def encode(text,size):  
        text=text.upper()
        if len(text)%size!=0:
            text=text+(" ")*(size-(len(text)%size)) # Adding space if text can't divided by key length without remainder
        dividedList=[text[x:x+size] for x in range(0,len(text),size)] # Divide text into parts with key's length
        valueList=[]
        for divide in dividedList:
            values=list(map(convert,divide))
            valueList.append(values)
        return valueList
        

    def decode(numbers):
        valueList=[]
        for num in numbers:
            values=list(map(convert,num))
            valueList.append(values)
        return valueList

    if operation=="enc":
        inputFile=open(input_path,"r")
        text=inputFile.readline()
        outputFile=open(output,"w")
        message= list(map(multiply,encode(text,size)))
        encryptedText=','.join(str(num) for innerList in message for num in innerList)
        outputFile.write(encryptedText)
        outputFile.close()
        inputFile.close()



    elif operation == "dec":
        list_2d = key(keyList).copy()
        keyList = inverse(list_2d)
        inputFile = open(input_path, "r")
        outputFile = open(output, "w")
        numbers = inputFile.readline().strip("\n ").split(",")
        numbers2 = []
        for num in numbers:
            numbers2.append(int(num))
        dividedList = [numbers2[x:x + size] for x in range(0, len(numbers), size)]
        message = list(map(multiply, dividedList))
        decoded = decode(message)
        decryptedText = ''.join(str(num) for innerList in decoded for num in innerList)
        outputFile.write(decryptedText)
        outputFile.close()
        inputFile.close()



      