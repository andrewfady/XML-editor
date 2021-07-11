def handling(path):
    trial=open(path,'r').read()
    split1 = trial.split("<")
    split2 = trial.split("<")
    open_stack =[]
    close_stack = []
    error_location = []
    split1.remove(split1[0])
    split2.remove(split2[0])
    for i in range(len(split1)):
        split1[i] = split1[i].replace(" ","")
    length=len(split1)
    i=0
    old_count = 0
    while(i<length):
        n=split1[i].find('>')
        value = split1[i][n+1:len(split1[i])]
        if(value == '\n' or value=="\n\n"):
            if(split1[i][0] != '/'):
                open_stack.append(split1[i][0:n])
            else:
                close_stack.append(split1[i][1:n])
                if(open_stack[-1]==close_stack[-1]):
                    open_stack.pop()
                    close_stack.pop()
                else:
                    opening = open_stack[-1]
                    opening = "/" + opening + ">"
                    split1.insert(i,opening)
                    old_count+=1
                    error_location.append(i-old_count)
                    open_stack.pop()
                    length+=1
                    i+=1
        else:
            if(split1[i][0] !='/'):
                opening= split1[i][0:n]
                x=split1[i+1].find('>')
                if(split1[i+1][0] !='/'):
                    closing = split1[i+1][0:x]
                    if(opening != closing):
                        opening = "/" + opening + ">"
                        error_location.append(i)
                        split1.insert(i+1,opening)
                        old_count+=1
                        i+=1
                        length+=1
                    else:
                        i+=1
                else:
                    closing = split1[i+1][1:x]
                    if(opening != closing):
                        opening = "/" + opening + ">"
                        split1[i+1] = opening
                        error_location.append(i)
                        i+=1
                    else:
                        i+=1
        i+=1

    close_stack.append(split1[i-1][1:len(split1[i-1])-1])
    if(open_stack[-1]==close_stack[-1]):
        open_stack.pop()
        close_stack.pop()
    for i in error_location:
        split2[i] = split2[i].replace("\n","")
        split2[i] = split2[i].replace(" ","")
        split2[i] = split2[i] + " ------------> Error\n"
    final = '<'
    final = '<' + final.join(split1)

    visual= '<'
    visual = '<' + visual.join(split2)

    file=open('trial1.xml','w')
    file.writelines(final)

    file=open('trial2.xml','w')
    file.writelines(visual)


handling('trial.xml')