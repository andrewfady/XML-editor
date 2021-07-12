from prettifying_Minifying import *

def correcting(path):
    trial=open(path,'r').read()
    split1 = trial.split("<")
    split2 = trial.split("<")
    open_stack =[]
    close_stack = []
    error_location = []
    errors = []
    split1.remove(split1[0])
    split2.remove(split2[0])
    length=len(split1)
    i=0
    old_count = 0
    while(i<length):
        n=split1[i].find('>')
        value = split1[i][n+1:len(split1[i])]
        value = value.replace(" ","")
        y = split1[i].find(">")
        if(value == '\n' or value=="\n\n"):
            if(split1[i][0] != '/'):
                open_stack.append(split1[i][0:n])
            else:
                close_stack.append(split1[i][1:n])
                if(open_stack[-1]==close_stack[-1]):
                    open_stack.pop()
                    close_stack.pop()     
        else:
            if(split1[i][0] !='/'):
                opening= split1[i][0:n]
                x=split1[i+1].find('>')
                if(split1[i+1][1:x] in open_stack):
                    errors.append(opening)
                    opening = "/" + opening + ">"
                    error_location.append(i-old_count)
                    split1.insert(i+1,opening)
                    old_count+=1
                    i+=1
                    length+=1
                elif(split1[i+1][0] !='/'):
                    closing = split1[i+1][0:x]
                    if(opening != closing or opening == closing):
                        errors.append(opening)
                        opening = "/" + opening + ">"
                        error_location.append(i-old_count)
                        split1.insert(i+1,opening)
                        old_count+=1
                        i+=1
                        length+=1
                    else:
                        i+=1
                else:
                    closing = split1[i+1][1:x]
                    if(opening != closing):
                        errors.append(opening)
                        opening = "/" + opening + ">"
                        split1[i+1] = opening
                        error_location.append(i-old_count)
                        i+=1
                    else:
                        i+=1
        i+=1
    close_stack.append(split1[i-1][1:len(split1[i-1])-1])
    close_stack.reverse()
    diff= len(open_stack) -len(close_stack)
    count = diff
    errors_rev =[]
    locations_rev = []
    if(len(close_stack)<=len(open_stack)):
        while(len(close_stack)!=len(open_stack)):
            closing = "/" + open_stack[-1] + ">"
            loc = i-diff-old_count
            locations_rev.append(loc)
            errors_rev.append(open_stack[-1])
            count+=1
            open_stack.pop()
    for k in range(len(locations_rev)):
        locations_rev.reverse()
        errors_rev.reverse()
    for k in range(len(locations_rev)):
        error_location.append(locations_rev[k])
        errors.append(errors_rev[k])
    for k in range(len(locations_rev)):
        closing = "/" + errors_rev[k] + ">"
        loc = i-diff - 1
        split1.insert(loc,closing)
        i+=2
 
    while(len(open_stack)==len(open_stack)):
        if(open_stack[-1]==close_stack[-1]):
            open_stack.pop()
            close_stack.pop()
        if(len(open_stack)==0):
            break
  

    j = 0
    x= -1
    

    final = '<'
    final = '<' + final.join(split1)
    file=open('corrected_errors.xml','w')
    file.writelines(final)
    file.close()
    prettifying('corrected_errors.xml')

def visualizing(path):
    trial=open(path,'r').read()
    split1 = trial.split("<")
    split2 = trial.split("<")
    open_stack =[]
    close_stack = []
    error_location = []
    errors = []
    split1.remove(split1[0])
    split2.remove(split2[0])
    length=len(split1)
    i=0
    old_count = 0
    while(i<length):
        n=split1[i].find('>')
        value = split1[i][n+1:len(split1[i])]
        value = value.replace(" ","")
        y = split1[i].find(">")
        if(value == '\n' or value=="\n\n"):
            if(split1[i][0] != '/'):
                open_stack.append(split1[i][0:n])
            else:
                close_stack.append(split1[i][1:n])
                if(open_stack[-1]==close_stack[-1]):
                    open_stack.pop()
                    close_stack.pop()     
        else:
            if(split1[i][0] !='/'):
                opening= split1[i][0:n]
                x=split1[i+1].find('>')
                if(split1[i+1][1:x] in open_stack):
                    errors.append(opening)
                    opening = "/" + opening + ">"
                    error_location.append(i-old_count)
                    split1.insert(i+1,opening)
                    old_count+=1
                    i+=1
                    length+=1
                elif(split1[i+1][0] !='/'):
                    closing = split1[i+1][0:x]
                    if(opening != closing or opening == closing):
                        errors.append(opening)
                        opening = "/" + opening + ">"
                        error_location.append(i-old_count)
                        split1.insert(i+1,opening)
                        old_count+=1
                        i+=1
                        length+=1
                    else:
                        i+=1
                else:
                    closing = split1[i+1][1:x]
                    if(opening != closing):
                        errors.append(opening)
                        opening = "/" + opening + ">"
                        split1[i+1] = opening
                        error_location.append(i-old_count)
                        i+=1
                    else:
                        i+=1
        i+=1
    close_stack.append(split1[i-1][1:len(split1[i-1])-1])
    close_stack.reverse()
    diff= len(open_stack) -len(close_stack)
    count = diff
    errors_rev =[]
    locations_rev = []
    if(len(close_stack)<=len(open_stack)):
        while(len(close_stack)!=len(open_stack)):
            closing = "/" + open_stack[-1] + ">"
            loc = i-diff-old_count
            locations_rev.append(loc)
            errors_rev.append(open_stack[-1])
            count+=1
            open_stack.pop()
    for k in range(len(locations_rev)):
        locations_rev.reverse()
        errors_rev.reverse()
    for k in range(len(locations_rev)):
        error_location.append(locations_rev[k])
        errors.append(errors_rev[k])
    for k in range(len(locations_rev)):
        closing = "/" + errors_rev[k] + ">"
        loc = i-diff - 1
        split1.insert(loc,closing)
        i+=2
    if(open_stack[-1]==close_stack[-1]):
        open_stack.pop()
        close_stack.pop()
    j = 0
    x= -1
    for i in error_location:
        if(i != x):
            l=split2[i].find(">")
            split2[i] = split2[i].replace("\n","")
            split2[i] = split2[i][0:l]+split2[i][l:len(split2[i])].replace(" ","")
        split2[i] = split2[i] + f'------------> Error at tag "{errors[j]}"\n'
        x = i
        j+=1
    
    visual= '<'
    visual = '<' + visual.join(split2)
    file=open('visualized_errors.xml','w')
    file.writelines(visual)
    file.close()

correcting('trial.xml')
visualizing('trial.xml')

