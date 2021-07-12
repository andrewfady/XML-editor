#1--try detect error
"""
file_data=open('data-sample - Copy.xml','r').read()
split1=file_data.split('<')
out_name=[]
counter_line=0
for single_split1 in split1 :
    tag_name=single_split1.split('>')[0].split(' ')[0]
    if tag_name !='' and tag_name[0] !='!' and tag_name !='frame':
        if tag_name[0]=='/':
            flag_in=True
            counter_line=counter_line+1
            while flag_in :
                if out_name[-1] == tag_name.split('/')[1] :
                    flag_in=False
                    out_name.pop()
                else:                
                    print(out_name,tag_name)
                    flag_in=True
                    swap_element=out_name[-1]
                    out_name[-1]=out_name[-2]
                    out_name[-2]=swap_element
                    #print(out_name.pop())
                    print('error')
        else:
            out_name.append(tag_name)
"""

#2--try Prettifying
#notes:
##b7ot el value w el tag fy satr 7ta lw konna 7tyno fy tlt stor 
##(m3rf4 hal kda 3mlt el no2ta ally abl el a5yra kman wlla eh)
##lw fyh satr fady by4elo
##lw fyth msyln<select>   data </select>  ==> <select>data</select>
#####lw 7abb tkon bta3t el space w el msafat function lw7dha hna5od nafs el code bs hn4yl el spaces
def check_all_spaces(str_input): #'      o '=> false
    for i in str_input:
        if i==' ' or i=='\n':
            pass
        else:
            return False
    return True

def number_to_space(number):# 1 ->' '
    str_out=''
    for i in range(number):
        str_out=str_out+"   "
    return str_out
def remove_new_line(str_input):
    final_str=''
    for i in str_input:
        if i !='\n':
            final_str=final_str+i
    return final_str
def remove_spaces(str_input1):
    str_input=str_input1
    i=0
    while True:
        i=i+1
        if str_input[0]==' ':
            pos=0
            str_input = str_input[:pos] + str_input[(pos+1):]
        else:
            break
    i=0
    while True:
        i=i+1
        if str_input[-1]==' ':
            pos=len(str_input)-1
            str_input = str_input[:pos]
            print(str_input)
        else:
            break
    return str_input
#dy 3l4an nt2kd an kolo 3ala el 4mal mn8yr ay spaces
def all_left(path_file):
    file_data=open(path_file,'r').readlines()
    final_string=''
    for single_line in file_data:
        final_string=final_string+remove_spaces(single_line)+'\n'
    return final_string

def prettifying(path_in):
    file_data=all_left(path_in)
    split1=file_data.split('<') # tony:hsbdhjbdsj split(':')  [tony,hsbdhjbdsj]
    out_name=[]
    counter_line=0
    text_final=''
    with_new_line=True
    space_count=0
    for single_split1 in split1 :
        tag_name_complete=single_split1.split('>')
        print(tag_name_complete)
        print('====')
        tag_name=tag_name_complete[0]   

        if tag_name !='':
            tag_name=remove_spaces(tag_name_complete[0]).split(' ')[0]   
            if (tag_name[0]=='/'):
                space_count=space_count-1
            if not(check_all_spaces(tag_name_complete[1])):
                #هنا دة اخر المينت و بيطبع في نفس السطر
                value_tag=remove_spaces(remove_new_line(tag_name_complete[1]))
                text_final=text_final+number_to_space(space_count)+'<'+remove_spaces(tag_name_complete[0])+'>'+value_tag
                with_new_line=False
            elif not(with_new_line) :
                #هنا دة مش اخر اليمينت و عبارة عن هيكون في سطر لوحدة
                text_final=text_final+'<'+remove_spaces(tag_name_complete[0])+'>'+'\n'
                with_new_line=True
            else :
                #هنا دة مش اخر اليمينت و عبارة عن هيكون في سطر لوحدة
                text_final=text_final+number_to_space(space_count)+'<'+remove_spaces(tag_name_complete[0])+'>'+'\n'
                with_new_line=True
            if not(tag_name[0]=='/'):
                space_count=space_count+1

    output_file = open("prettifying.xml","w")
    output_file.write(text_final)

     
#3--try Minifying the XML file
def Minifying(path_in):
    file_data=all_left(path_in)
    split1=file_data.split('<') # tony:hsbdhjbdsj split(':')  [tony,hsbdhjbdsj]
    out_name=[]
    counter_line=0
    text_final=''
    with_new_line=True
    space_count=0
    for single_split1 in split1 :
        tag_name_complete=single_split1.split('>')
        print(tag_name_complete)
        print('====')
        tag_name=tag_name_complete[0]   
        if tag_name !='':
            tag_name=remove_spaces(tag_name_complete[0]).split(' ')[0]   

            if not(check_all_spaces(tag_name_complete[1])):
                #هنا دة اخر المينت و بيطبع في نفس السطر
                value_tag=remove_spaces(remove_new_line(tag_name_complete[1]))
                text_final=text_final+'<'+remove_spaces(tag_name_complete[0])+'>'+value_tag
                with_new_line=False
            elif not(with_new_line) :
                #هنا دة مش اخر اليمينت و عبارة عن هيكون في سطر لوحدة
                text_final=text_final+'<'+remove_spaces(tag_name_complete[0])+'>'+'\n'
                with_new_line=True
            else :
                #هنا دة مش اخر اليمينت و عبارة عن هيكون في سطر لوحدة
                text_final=text_final+'<'+remove_spaces(tag_name_complete[0])+'>'+'\n'
                with_new_line=True


    output_file = open("prettifying.xml","w")
    output_file.write(text_final)


#Minifying('try.txt')   
Minifying('try.xml')