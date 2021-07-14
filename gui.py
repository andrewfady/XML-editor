from tkinter import *
from tkinter import filedialog
import heapq
import os
import sys
####################huffman
class HuffmanCoding:
	def __init__(self, path):#require the path of the file
		self.path = path
		self.heap = []
		self.codes = {}
		self.reverse_mapping = {}

	class HeapNode:
		def __init__(self, char, freq):
			self.char = char
			self.freq = freq
			self.left = None
			self.right = None

		# defining comparators less_than and equals
		def __lt__(self, other):
			return self.freq < other.freq

		def __eq__(self, other):
			if(other == None):
				return False
			#if (not isinstance(other, HeapNode)):#if not of heap type but have frequency attribute
				#return False
			return self.freq == other.freq

	# functions for compression:

	def make_frequency_dict(self, text):#calcuate frequency of each character and retuen it
		frequency = {}
		for character in text:
			if not character in frequency:
				frequency[character] = 0
			frequency[character] += 1
		return frequency

	def make_heap(self, frequency):#make priority queue
		for key in frequency:
			node = self.HeapNode(key, frequency[key])#create a node and pass the character and its value
			heapq.heappush(self.heap, node)#push the node into heap

	def merge_nodes(self):#build huffman tree, save the root node in heap
		while(len(self.heap)>1):
			node1 = heapq.heappop(self.heap)
			node2 = heapq.heappop(self.heap)

			merged = self.HeapNode(None, node1.freq + node2.freq)
			merged.left = node1
			merged.right = node2

			heapq.heappush(self.heap, merged)


	def make_codes_helper(self, root, current_code):
		if(root == None):
			return

		if(root.char != None):
			self.codes[root.char] = current_code
			self.reverse_mapping[current_code] = root.char
			return

		self.make_codes_helper(root.left, current_code + "0")
		self.make_codes_helper(root.right, current_code + "1")


	def make_codes(self):#make codes for characters
		root = heapq.heappop(self.heap)
		current_code = ""
		self.make_codes_helper(root, current_code)


	def get_encoded_text(self, text):#replace characters with their codes
		encoded_text = ""
		for character in text:
			encoded_text += self.codes[character]
		return encoded_text


	def pad_encoded_text(self, encoded_text):#add padding to text that is not multiple of 8
		extra_padding = 8 - len(encoded_text) % 8
		for i in range(extra_padding):
			encoded_text += "0"

		padded_info = "{0:08b}".format(extra_padding)
		encoded_text = padded_info + encoded_text
		return encoded_text


	def get_byte_array(self, padded_encoded_text):#convert bits into bytes
		if(len(padded_encoded_text) % 8 != 0):
			print("Encoded text not padded properly")
			exit(0)

		b = bytearray()
		for i in range(0, len(padded_encoded_text), 8):
			byte = padded_encoded_text[i:i+8]
			b.append(int(byte, 2))
		return b


	def compress(self):
		filename, file_extension = os.path.splitext(self.path)#extract the file name and the file extension; to save the output file in the same location
		output_path = filename + ".bin"#create output file
        

		with open(self.path, 'r+') as file, open(output_path, 'wb') as output:#open input file in read mode, open output file in write mode
			text = file.read()#read text in input file
			text = text.rstrip()#trim extra spaces

			frequency = self.make_frequency_dict(text)#calculate freq. from the func. and store in the variable
			self.make_heap(frequency)
			self.merge_nodes()
			self.make_codes()

			encoded_text = self.get_encoded_text(text)
			padded_encoded_text = self.pad_encoded_text(encoded_text)

			b = self.get_byte_array(padded_encoded_text)
			output.write(bytes(b))

		print("Compressed")
		return output_path


	""" functions for decompression: """


	def remove_padding(self, padded_encoded_text):
		padded_info = padded_encoded_text[:8]
		extra_padding = int(padded_info, 2)

		padded_encoded_text = padded_encoded_text[8:] 
		encoded_text = padded_encoded_text[:-1*extra_padding]

		return encoded_text

	def decode_text(self, encoded_text):
		current_code = ""
		decoded_text = ""

		for bit in encoded_text:
			current_code += bit
			if(current_code in self.reverse_mapping):
				character = self.reverse_mapping[current_code]
				decoded_text += character
				current_code = ""

		return decoded_text


	def decompress(self, input_path):
		filename, file_extension = os.path.splitext(self.path)
		output_path = filename + "_decompressed" + ".txt"

		with open(input_path, 'rb') as file, open(output_path, 'w') as output:
			bit_string = ""

			byte = file.read(1)
			while(len(byte) > 0):
				byte = ord(byte)
				bits = bin(byte)[2:].rjust(8, '0')
				bit_string += bits
				byte = file.read(1)

			encoded_text = self.remove_padding(bit_string)

			decompressed_text = self.decode_text(encoded_text)
			
			output.write(decompressed_text)

		print("Decompressed")
		return output_path
####################main_functions
def check_all_spaces(str_input): #'      o '=> false
    for i in str_input:
        if i==' ' or i=='\n':
            pass
        else:
            return False
    return True

def remove_double_qouts(str_input1):
    str_input=str_input1
    i=0
    while True:
        i=i+1
        if str_input[0]=='"':
            pos=0
            str_input = str_input[:pos] + str_input[(pos+1):]
        else:
            break
    i=0
    while True:
        i=i+1
        if str_input[-1]=='"':
            pos=len(str_input)-1
            str_input = str_input[:pos]
        else:
            break
    return str_input
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

def xml_json(path):
    js_dict="{"
    tags=[""]
    tag_type=[""]
    comma=False
    opned_curly=False
    file_data=Minifying(path)
    split1=file_data.split('<')
   
    print(split1)

    count=0
    for i in range(len(split1)) :
        tag_name_complete=split1[i].split('>')
        
        
        if (len(tag_name_complete[0].split(' '))!=1):
            new_temp=tag_name_complete[0].split(' ')
            #print("------------------")
            #print(new_temp)
            tag_name_complete[0]=new_temp[0]
            new_temp2=new_temp[1].split('=')
            #print(new_temp2)
            split1.insert(i+1,f'@{new_temp2[0]}>{remove_double_qouts(new_temp2[1])}')
            split1.insert(i+2,f'/{new_temp2[0]}>\n')
        
        #print(tag_name_complete)

        
          
        
        
        end_tag="/"+tags[-1]
        end_tag2="/"+tags[-1][1:len(tags[-1])]
        if end_tag==tag_name_complete[0] or end_tag2==tag_name_complete[0] :
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
    check=False
    tab_counter=1
    for i in range(len(js_dict)):
        if js_dict[i]=='@':
            check=True
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
    if check:
        temp+="\n}"
    output_file = open("json_format.xml","w")
    output_file.write(temp) 


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


    output_file = open("Minifying.xml","w")
    output_file.write(text_final)
    return text_final
##########################################


# functions 

def operations(selection):
    operation_type=selection
    input_pass=pathh.get()
     # دة بس اللي محتاج يتعدل و ان نعمل كال للفنكشن. هنا الباس اللي معروف هيطلع علية الاوتبوت
    if (operation_type=='Minifying'):
        pass
        
    elif (operation_type=='prettifying'):
        pass
    elif (operation_type=='xml to json'):
        pass

    elif (operation_type=='visualize errors'):
        pass
    elif (operation_type=='correct errors'):
        pass
    elif (operation_type=='decompress'):
        #input_pass ===.bin
        pass
 
    elif (operation_type=='compress'):
        pass
        




def openFile():
    tf = filedialog.askopenfilename(
        initialdir="C:/Users/MainFrame/Desktop/", 
        title="Open Text file", 
        filetypes=(("Text Files", ".xml .bin"),)
        )
    if tf !="":
        pathh.delete(0, END)
        pathh.insert(0, tf)
        if tf.split(".")[1]=='bin':
            tf = open(tf,"rb")
            file_cont = tf.read()

            txtarea.delete('1.0',"end")
            txtarea.insert('1.0', file_cont)
        
            tf.close()
        else:
            tf = open(tf)
            file_cont = tf.read()

            txtarea.delete('1.0',"end")
            txtarea.insert('1.0', file_cont)
        
            tf.close()



def saveFile():
    tf = filedialog.asksaveasfile(
        mode='w',
        title ="Save file",
        defaultextension=".xml"
        )
    pathh.delete(0,END)
    pathh.insert(0, tf.name)
    data = str(txtarea.get(1.0, END))
    tf.write(data)
   
    tf.close()

ws = Tk()
ws.title("PythonGuides")
ws.geometry("720x500")
ws.resizable(False, False)
ws['bg']='#424242'


# add drop down menu
OPTIONS = [
"Minifying",
"prettifying",
"xml to json",
"visualize errors",
"correct errors",
"compress",
"decompress"
]
variable = StringVar(ws)
variable.set(OPTIONS[0]) # default value
w = OptionMenu(ws, variable, *OPTIONS,command=operations)
w["highlightthickness"]=0
w.pack(pady=5)



# adding frame
frame = Frame(ws)
frame.pack(pady=5)

# adding scrollbars 
ver_sb = Scrollbar(frame, orient=VERTICAL )
ver_sb.pack(side=RIGHT, fill=BOTH)

hor_sb = Scrollbar(frame, orient=HORIZONTAL)
hor_sb.pack(side=BOTTOM, fill=BOTH)

# adding writing space
txtarea = Text(frame,wrap=NONE, width=80, height=20,xscrollcommand=hor_sb.set)
txtarea.pack(side=LEFT)


# binding scrollbar with text area
txtarea.config(yscrollcommand=ver_sb.set)
ver_sb.config(command=txtarea.yview)

txtarea.config(xscrollcommand=hor_sb.set)
hor_sb.config(command=txtarea.xview)


# adding buttons 
openphoto=PhotoImage(file="open.png")
Button(
    ws,activebackground="#424242",bg="#424242",
    image=openphoto,  highlightthickness = 0, bd = 0,
    command=openFile
    ).pack(side=LEFT, padx=5,pady=5)
savephoto=PhotoImage(file="save.png")
Button(
    ws,activebackground="#424242",bg="#424242",
    image=savephoto, highlightthickness = 0, bd = 0,
    command=saveFile
    ).pack(side=LEFT,padx=5,pady=5)
exitphoto=PhotoImage(file="done.png")
Button(
    ws, activebackground="#424242",bg="#424242",
    image=exitphoto, highlightthickness = 0, bd = 0,
    command=lambda:ws.destroy()
    ).pack(side=LEFT, padx=5,pady=5)
"""
Button(
    ws, activebackground="#424242",bg="#424242",
    image=exitphoto, highlightthickness = 0, bd = 0,
    command=lambda:ws.destroy()
    ).pack(side=LEFT, padx=5,pady=5)
"""



pathh = Entry(ws)
pathh.pack(expand=True, fill=X, padx=5)
ws.mainloop()



