


def xml_json(path):
    js_dict="{"
    tags=[""]
    tag_type=[""]
    comma=False
    opned_curly=False
    file_data=open(path,'r').read()
    split1=file_data.split('<')
   
    #print(split1)

    count=0
    for i in range(len(split1)) :
        tag_name_complete=split1[i].split('>')
        print(tag_name_complete)
        end_tag="/"+tags[-1]
        if end_tag==tag_name_complete[0]:
            if tag_type[-1]=="child_array_element": #id,name
                if comma:
                    if split1[i].split('>')[1]=='':
                        js_dict+="}"
                    js_dict+=","
                    
                tag_type.pop(-1)
                tags.pop(-1)
            elif tag_type[-1]=="array_element":#user
                if(js_dict[-1]==','):
                    temp=js_dict[0:len(js_dict)-1]
                    js_dict=temp
                if split1[i].split('>')[0]!=split1[i-2].split('>')[0] and split1[i-1].split('>')[0]+'s'!=split1[i-2].split('>')[0] and js_dict[-1]!='}':
                    js_dict+='}'
                tag_type.pop(-1)
                tags.pop(-1)
            elif tag_type[-1]=="parent_array":#users
                js_dict+="]"
                if i!=len(split1)-1:
                    js_dict+=","
            
            
                tag_type.pop(-1)
                tags.pop(-1)
            elif tag_type[-1]=="child":
                tag_type.pop(-1)
                tags.pop(-1)
            elif tag_type[-1]=="parent":
                js_dict+="}"
                tag_type.pop(-1)
                tags.pop(-1)
            if len(tags)==2 and  js_dict[-1]!='}' and tag_type[-1]!="parent":
                js_dict+="}"


            
        elif tag_name_complete[0]!='' and tag_name_complete[0]+'s'==tags[-1] and tag_name_complete[0][0]!='/':
            tags.append(tag_name_complete[0])
            tag_type.append("array_element")
            #tag_type[-1]="parent_array"
            comma=True
            if js_dict[-1]!='[' and js_dict[-1]!=':':
                js_dict+=','
            if tag_name_complete[1]=="\n":
                js_dict+=f'"{tag_name_complete[0]}":'+"{" #user,post
            if tag_name_complete[1]!="\n" and tag_name_complete[1]!='' :
                tag_val=tag_name_complete[1].replace("\n","")
                js_dict+=f'"{tag_val}"'

        elif tag_name_complete[0]!='' and tag_name_complete[0][0]!='/':
            tags.append(tag_name_complete[0])
            if split1[i+1].split('>')[0]+'s'==tags[-1] or tag_name_complete[0][-1]=='s' : #or split1[i+1].split('>')[0]+'s'==tags[-2] 
                tag_type.append("parent_array")
                
                #count+=1
                #print(tag_name_complete[0])
            elif tag_type[-1]=="array_element":
                tag_type.append("child_array_element")
            elif tag_name_complete[1]=='\n':  #tag_type[-1]=="parent" or tag_type[-1]=="child" :
                tag_type.append("parent")
            else:
                tag_type.append("child")
            if tag_type[-1]=="parent_array":
                js_dict+=f'"{tag_name_complete[0]}":' #users id name
                js_dict+=f'['
            #elif tag_name_complete[0][-1]=='s' and js_dict[-1]!=',' and js_dict[-1]!='{' and js_dict[-1]!=':' :
            #   js_dict+=',***'
            elif tag_type[-1]=="child_array_element" and split1[i+1].split('>')[1]=='' :
                js_dict+="{"
                js_dict+=f'"{tag_name_complete[0]}":'
            elif tag_type[-1]=="parent":
                if js_dict[-1]=='}':
                    js_dict+=","
                js_dict+=f'"{tag_name_complete[0]}":'+'{'
            elif tag_type[-1]=="child":
                if js_dict[-1]!='{': #and js_dict[-1]!=':':
                    js_dict+=","
                js_dict+=f'"{tag_name_complete[0]}":'


            else:
                js_dict+=f'"{tag_name_complete[0]}":' #users id name
            if tag_name_complete[1]!="\n":
                tag_val=tag_name_complete[1].replace("\n","")
                js_dict+=f'"{tag_val}"'#print value
    js_dict+='}'
    #print(js_dict)
    return(js_dict)  

def json_format(js_dict):
    temp=""
    tab_counter=1
    for i in range(len(js_dict)):
        if(i==0):
            temp+=js_dict[i]
            temp+="\n"+"     "
            
            #tab_counter+=1
        elif js_dict[i]=='{' or js_dict[i]=='[' :
            tab_counter+=1
            temp+=js_dict[i]+"\n"+"     "*tab_counter
        
            
           
                
        elif js_dict[i]=='}' or js_dict[i]==']':
            tab_counter-=1
            temp+="\n"+"     "*tab_counter+js_dict[i]
           
            
        elif  js_dict[i]==',':
            temp+=js_dict[i]+"\n"+"     "*tab_counter

        else:
           temp+=js_dict[i] 
    print(temp)
    #write temp in a file 
      





js_on=xml_json('check.txt')
print(js_on)
print("/////////////////////////////////////")
json_format(xml_json('tryyyyy.xml')) #zawed da bas f el gewy XDDDDDDDDDDD bas yeb2a all left el awel 


       

    

 







