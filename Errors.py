from prettifying_Minifying import *


def correcting(path):
    trial=open(path,'r').read()
    split1 = trial.split("<")
    split2 = trial.split("<")
    open_stack =[]
    close_stack = []
    close_location = []
    error_location = []
    errors = []
    split1.remove(split1[0])
    split2.remove(split2[0])
    length=len(split1)
    for k in range(length):
        extra_space=split1[k].find('\n')
        if(extra_space== -1):
            continue
        first = split1[k][0:extra_space+1]
        second = split1[k][extra_space:len(split1[k])].replace("\n","")
        split1[k] = first + second
    for k in range(length):
        extra_space=split2[k].find('\n')
        if(extra_space== -1):
            continue
        first = split2[k][0:extra_space+1]
        second = split2[k][extra_space:len(split1[k])].replace("\n","")
        split2[k] = first + second
    i=0
    old_count = 0
    while(i<length):
        n=split1[i].find('>')
        value = split1[i][n+1:len(split1[i])]
        value = value.replace(" ","")
        if(value == '\n'):
            if(split1[i][0] != '/'):
                open_stack.append(split1[i][0:n])
                if('frame' in split1[i][0:n]):
                    open_stack.pop()
            else:
                close_stack.append(split1[i][1:n])
                close_location.append(i)
                space=close_stack[-1].find(" ")
                if(open_stack[-1]==close_stack[-1]):
                    open_stack.pop()
                    close_stack.pop()
                    close_location.pop()
        else:
            if(split1[i][0] !='/'):
                space = split1[i][0:n].find(" ")
                if(space==-1):
                    opening= split1[i][0:n]
                else:
                    opening= split1[i][0:space]
                x=split1[i+1].find('>')
                if(split1[i+1][1:x] in open_stack):
                    errors.append(opening)
                    l = opening.find(" ")
                    if(l != -1):
                        opening = "/" + opening[0:l]+ ">"
                    else:
                        opening = "/" + opening+ ">"
                    error_location.append(i-old_count)
                    split1.insert(i+1,opening)
                    old_count+=1
                    i+=1
                    length+=1
                elif(split1[i+1][0] !='/'):
                    closing = split1[i+1][0:x]
                    if(opening != closing ):
                        errors.append(opening)
                        l = opening.find(" ")
                        if(l != -1):
                            opening = "/" + opening[0:l]+ ">"
                        else:
                            opening = "/" + opening+ ">"
                        error_location.append(i-old_count)
                        split1.insert(i+1,opening)
                        old_count+=1
                        i+=1
                        length+=1
                    elif(opening==closing):
                        errors.append(opening)
                        l = opening.find(" ")
                        if(l != -1):
                            opening = "/" + opening[0:l]+ ">"
                        else:
                            opening = "/" + opening+ ">"
                        error_location.append(i-old_count)
                        split1[i+1] = opening
                        i+=1
                    else:
                        i+=1
                else:
                    closing = split1[i+1][1:x]
                    if(opening != closing):
                        errors.append(opening)
                        l = opening.find(" ")
                        if(l != -1):
                            opening = "/" + opening[0:l]+ ">"
                        else:
                            opening = "/" + opening+ ">"
                        split1[i+1] = opening
                        error_location.append(i-old_count)
                        i+=1
                    else:
                        i+=1
        i+=1
    if(len(close_stack)==0 and len(open_stack) ==1):
        n=split1[i-1].find('>')
        close_stack.append(split1[i-1][1:n])
        close_location.append(i-1)
    k=0
    for i in range(len(close_stack)):
        if(close_stack[i-k] not in open_stack):
            split1.remove(split1[close_location[i]])
            close_stack.remove(close_stack[i-k])
            k+=1
            for i in range(len(close_location)):
                error_location.append(i-old_count)
                close_location[i]-=1
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
    m=0
    for k in range(len(locations_rev)):
        closing = "/" + errors_rev[k] + ">"
        loc = len(split1) - len(open_stack)
        split1.insert(loc,closing)
        i+=2
    n = len(open_stack)
    flag = 0
    count = 0 
    overlapped = []
    while(len(open_stack)==len(close_stack) and len(open_stack) != 0):
        if(open_stack[-1]==close_stack[-1]):
            if(flag == 1):
                overlapped.append(close_stack[-1])
            open_stack.pop()
            close_stack.pop()
        if(len(open_stack)==0):
            break
        if(count>n):
            count =0
            close_stack.reverse()
            flag +=1
        count+=1
        if(flag==2):
            break
    length = len(overlapped)
    if (flag == 1):
        for i in range(length):
            split1.remove(split1[-1])
        for i in range(length):
            closing = "/" + overlapped[i] + ">"
            split1.append(closing)
    print(split1)
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
    close_location = []
    error_location = []
    errors = []
    split1.remove(split1[0])
    split2.remove(split2[0])
    length=len(split1)
    for k in range(length):
        extra_space=split1[k].find('\n')
        if(extra_space== -1):
            continue
        first = split1[k][0:extra_space+1]
        second = split1[k][extra_space:len(split1[k])].replace("\n","")
        split1[k] = first + second
    for k in range(length):
        extra_space=split2[k].find('\n')
        if(extra_space== -1):
            continue
        first = split2[k][0:extra_space+1]
        second = split2[k][extra_space:len(split1[k])].replace("\n","")
        split2[k] = first + second
    i=0
    old_count = 0
    while(i<length):
        n=split1[i].find('>')
        value = split1[i][n+1:len(split1[i])]
        value = value.replace(" ","")
        if(value == '\n'):
            if(split1[i][0] != '/'):
                open_stack.append(split1[i][0:n])
                if('frame'in split1[i][0:n]):
                    open_stack.pop()
            else:
                close_stack.append(split1[i][1:n])
                close_location.append(i)
                space=close_stack[-1].find(" ")
                if(open_stack[-1]==close_stack[-1]):
                    open_stack.pop()
                    close_stack.pop()
                    close_location.pop()
                elif(open_stack[-1]==close_stack[-1][0:space-1]):
                    open_stack.pop()
                    close_stack.pop()
                    close_location.pop()
        else:
            if(split1[i][0] !='/'):
                space = split1[i][0:n].find(" ")
                if(space==-1):
                    opening= split1[i][0:n]
                else:
                    opening= split1[i][0:space]
                x=split1[i+1].find('>')
                if(split1[i+1][1:x] in open_stack):
                    errors.append(opening)
                    l = opening.find(" ")
                    if(l != -1):
                        opening = "/" + opening[0:l]+ ">"
                    else:
                        opening = "/" + opening+ ">"
                    error_location.append(i-old_count)
                    split1.insert(i+1,opening)
                    old_count+=1
                    i+=1
                    length+=1
                elif(split1[i+1][0] !='/'):
                    closing = split1[i+1][0:x]
                    if(opening != closing or opening == closing):
                        errors.append(opening)
                        l = opening.find(" ")
                        if(l != -1):
                            opening = "/" + opening[0:l]+ ">"
                        else:
                            opening = "/" + opening+ ">"
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
                        l = opening.find(" ")
                        if(l != -1):
                            opening = "/" + opening[0:l]+ ">"
                        else:
                            opening = "/" + opening+ ">"
                        split1[i+1] = opening
                        error_location.append(i-old_count)
                        i+=1
                    else:
                        i+=1
        i+=1
    if(len(close_stack)==0 and len(open_stack) ==1):
        n=split1[i-1].find('>')
        close_stack.append(split1[i-1][1:n])
        close_location.append(i-1)

    k=0
    for i in range(len(close_location)):
        error_location.append(close_location[i]-old_count)
    for i in range(len(close_stack)):
        if(close_stack[i-k] not in open_stack):
            p = split1[close_location[i]].find(">")
            errors.append(split1[close_location[i]][1:p])
            split1.remove(split1[close_location[i]])
            close_stack.remove(close_stack[i-k])
            k+=1
            for j in range(len(close_location)):
                close_location[j]-=1
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
        loc = i-diff-1
        split1.insert(loc,closing)
        i+=2
    n = len(open_stack)
    flag = 0
    count = 0 
    overlapped = []
    while(len(open_stack)==len(close_stack) and len(open_stack) != 0):
        if(open_stack[-1]==close_stack[-1]):
            if(flag == 1):
                overlapped.append(close_stack[-1])
            open_stack.pop()
            close_stack.pop()
        if(len(open_stack)==0):
            break
        if(count>n):
            count =0
            close_stack.reverse()
            flag +=1
        count+=1
        if(flag==2):
            break
    length = len(overlapped)
    if (flag == 1):
        for i in range(length):
            split1.remove(split1[-1])
        for i in range(length):
            closing = "/" + overlapped[i] + ">"
            split1.append(closing)
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
        if(j>len(errors)-1):
            break

    visual= '<'
    visual = '<' + visual.join(split2)
    file=open('visualized_errors.xml','w')
    file.writelines(visual)
    file.close()

correcting('trial.xml')
visualizing('trial.xml')

