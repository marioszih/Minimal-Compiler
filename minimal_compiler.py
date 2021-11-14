#THOMAS PATSANIS A.M:3318 Username: cse63318
#MARIOS ZICHNALIS A.M:3226 Username: cse63226
#
#
#In order to run the program just type 'python final.py *.min'



import os
import sys
import locale
from os import path






###########################################################################				 
#FILE MANAGER	 
#File manager checks file's existance and extension(has to be '.min').
#Otherwise it prints error and terminates the program	 
###########################################################################
def File_Manager(filename):
	extension = filename.split(".")			
	if len(extension)==2:										#check if the user gave something like XXXXX.XXX
		if extension[1] == 'min':								#check the file extension
			if path.isfile(filename):							#if the file exists open it
				file = open(filename, 'r')
				return file
			else:
				print("\tSystem Error: Undeclared file\n\tNo such file: "+filename)
				exit()
		else:
			print("\tSystem Error: Given file isnt minimal++\n\tPlease enter a file with '.min' extension")
			exit()
	else: 
		print("\tSystem Error: Given file isnt minimal++\n\tPlease enter a file with '.min' extension")
		exit()






###########################################################################				 
#ERROR MANAGER	 
#Error manager manages errors of Lexical and Syntact Analyzer.
#Prints the error,the analysis where the error occured,the line
#and a short message for the user.After that, terminates the program
###########################################################################
def Error_Manager(analyzer,char,line,message):
	if(line != -1):
		print("\t Error in "+analyzer+", Line -> "+str(line))
		print("\t "+message+":\t '"+char+"'")
		print("\t Program Exit...")
		exit()
	else:
		print("\t Error in "+analyzer)
		print("\t "+message+":\t '"+char+"'")
		print("\t Program Exit...")
		exit()
 
 
 
 
###########################################################################
#LEX ANALYZER	
#Lex Analyzer does the lexical analysis of a minimal++ code. 
#If everything is correct it returns 1 word, otherwise calls Error_Manager
###########################################################################
def Lex():
	word = ""
	global line_counter
	global char_counter
	global max_letter_counter
	global int_size_checker
	state = 0
	END = -1
	while state != END:
		char = file.read(1)										#Read character from the file
		char_counter += 1										#There is a bug in tell() method so we used a simple counter to move around the file
		#print(str(char_counter)+char)
		if state == 0:											
			if char == " " or char == '\t':  					#Ignore white characters
				state = 0
			elif char == '\n':									#in case of '\n' increase lines value by 1
				state = 0
				line_counter += 1
				#char_counter -= 1
			elif char.isalpha():
				state = 1
				word += char
				max_letter_counter +=1
			elif char.isdigit():
				state = 2
				word += char
			elif char == '<':
				state = 3
				word += char
			elif char == '>':
				state = 4
				word += char
			elif char == ':':
				state = 5
				word += char
			elif char == '/':
				state = 6
			elif char in ('=','+','-','*',';',',','(',')','[',']','{','}'):
				state = END
				word += char
			elif char == '':
				state = END
			elif char == "'":
				state = 0
			else:
				Error_Manager("Lexical Analysis",char,line_counter,"Can't recognise character")
		elif state == 1:
			if char.isalpha() or char.isdigit():						#after reading a letter keep reading for every letter or number
				word += char
				max_letter_counter+=1
				if max_letter_counter > 30:
					Error_Manager("Lexical Analysis",word,line_counter,"Maximum amount of letters is 30")
			elif char == None:
				state = END
			else:
				state = END
				file.seek(char_counter-1+line_counter)								#go back 1 character in the file
				char_counter -= 1
		elif state == 2:
			if char.isdigit():											#after reading keep reading for every number
				word += char
			elif char.isalpha():										#error for letter after num
				word += char
				Error_Manager("Lexical Analysis",word,line_counter,"Letter usage after a number")
			elif char == '':
				state = END
			else:
				int_size_checker = True
				state = END
				file.seek(char_counter - 1+line_counter)
				char_counter -= 1
		elif state == 3:											#in case we have '<=' or '<>'
			if char == '>' or char == '=':
				word += char
				state = END
			elif char == '':
				state = END
			else:
				state = END
				file.seek(char_counter - 1+line_counter)
				char_counter -= 1
		elif state == 4:											#in case we have '>='
			if char == '=':
				word += char
				state = END
			elif char == '':
				state = END
			else:
				state = END
				file.seek(char_counter - 1+line_counter)
				char_counter -= 1
		elif state == 5:											#in case we have ':='
			if char == '=':
				word += char
				state = END
			elif char == '':
				state = END
			else:
				state = END
				file.seek(char_counter - 1+line_counter)
				char_counter -= 1
		elif state == 6:							
			if char == '/':											#no1 case for comments
				state = 7
			elif char == '*':										#no2 case for comments
				state = 8
			elif char == '':
				state = END
				word += '/'
			else:													#case we have '/' for division and not for comments
				file.seek(char_counter - 1+line_counter)
				char_counter -= 1
				word += '/'
				state = END
		elif state == 7:											#in case of '//' ignore every character until '/n' then go back to state 0
			if char == '\n':
				state = 0
				line_counter += 1
			elif char == '':
				state = END
		elif state == 8:											#in  case of '/*' keep searching for '*' and ignore everything else
			if char == '*':
				state = 9
			elif char == '\n':										#keep searching for '*', but if you find '\n' increase lines value by 1
				line_counter += 1
			elif char == '':										#commets dont close error no1
				Error_Manager("Lexical Analysis",'/*',line_counter,"Error: comments were not closed")
		elif state == 9 :
			if char == '/':											#in case we found '*/' comments are closed so we can go back to state 0 and read again
				state = 0
			elif char == '':										#comments dont close error no2
				Error_Manager("Lexical Analysis",'/*',line_counter,"Error: comments were not closed")
				exit()
			elif char == '\n':										#keep searching for '*/', but if you find '\n' increase lines value by 1
				state = 8
				line_counter += 1
			else:													#keep searching for '*/'
				state = 8
	print(word)
	if int_size_checker == True:
		if int(word) < -32767 or int(word) > 32767: 			
			Error_Manager("Lexical Analysis",word,line_counter,"Invalid Integer Error: Integers must be bigger than -32767 and smaller than 32767")
	max_letter_counter = 0
	int_size_checker = False
	return word



###########################################################################
#INTERMEDIATE CODE PRODUCTION
#General functions that syntact analyzer uses for  
#intermediate code production.
###########################################################################
def Nextquad():
	return tag_number



def Genquad(op,x,y,z):
	global quads_list,tag_number
	tag = Nextquad()
	sublist = [tag,op,x,y,z]
	tag_number = tag_number + 1
	quads_list.append(sublist)
	
	

def NewTemp():
	global temp_number
	temp_number += 1
	temp_var = 'T_' + str(temp_number)
	c_all_ids.append(temp_var)
	Record_Entity_Var(temp_var,'temp',Count_Offset())
	return temp_var
	


def Emptylist():
	lst = []
	return lst



def Makelist(x):
	lst = []
	lst.append(x)
	return lst



def Merge(list1,list2):
	return list1 + list2
	
	

def Backpatch(list,z):
	global quads_list
	#print(list)
	#print(z)
	for i in range(len(list)):
		for j in range(len(quads_list)):
			if(list[i] == quads_list[j][0]):
				quads_list[j][4] = z






###########################################################################
#FILE CREATOR	
#File creator generates .int & .c files.
#For each file we have different methods
###########################################################################


def Create_Int_File():
	filename = "int_code.int"
	file = open(filename, 'w')
	for i in range (len(quads_list)):
		line = ""
		for j in range(5):
			if j==0:
				line += str(quads_list[i][j])+': '
			elif 0<j<4:
				line += str(quads_list[i][j])+' '
			else:
				line += str(quads_list[i][j])+'\n'
		file.write(line)







def Create_C_File():
	global c_all_ids
	filename = "equivalent.c"
	file = open(filename, 'w')
	file.write("#include <stdio.h>\n\n\n")
	main = "int main()"+'\n'+'{'+'\n'+'\t'+"int " 
	sep = "\\" + 'n'
	file.write(main)
	for i in range (len(c_all_ids)):
		if(i == len(c_all_ids)-1):
			file.write(c_all_ids[i]+';')
		else:
			file.write(c_all_ids[i]+',')
	line_num = 1
	line_tab = '\n'+'\t'+'L_'+str(line_num)+': '
	file.write(line_tab)
	flag = False
	for k in range(len(quads_list)):
		text = ''
		tag = str(quads_list[k][0])
		op = str(quads_list[k][1])
		x = str(quads_list[k][2])
		y = str(quads_list[k][3])
		z = str(quads_list[k][4])
		if(op == ':='):
			text = z + ' = ' + x
		elif(op in ('+','-','*','/')):
			text = z + ' = ' + x+ ' ' + op + ' ' + y
		elif(op in ('=','>=','<=','<>','<','>')):
			if(op == '='):
				op = '=='
			elif(op == '<>'):
				op = '!='
			text = 'if('+ x + ' ' + op + ' ' + y + ') ' + 'goto L_' + z
		elif(op == 'jump'):
			text = 'goto L_' + z
		elif(op == 'out'):
			text = 'printf("%d'  + sep + '"' + ',' + x + ')'
		elif(op == 'inp'):
			text = 'scanf("%d", &'+x+')'
		elif(op == 'halt'):
			text = '{}'
			file.write(text)
			line_num = line_num + 1
			file.write(Create_Quad_Comment(quads_list[k]))
			flag = True
		elif(op == 'end_block'):
			flag = True
		elif(op == 'begin_block'):
			text = ''
			file.write(text)
			line_num = line_num + 1
			file.write(Create_Quad_Comment(quads_list[k]))
			line_tab = '\n'+'\t'+'L_'+str(line_num)+': '
			file.write(line_tab)
			flag = True
		
		if(flag == False):
			file.write(text)
			line_num = line_num + 1
			file.write(';')
			file.write(Create_Quad_Comment(quads_list[k]))
			line_tab = '\n'+'\t'+'L_'+str(line_num)+': '
			file.write(line_tab)
		else:
			flag = False
	file.write('\n}')








def Create_Quad_Comment(quad):
	strr = '\t'+'\t'+'//('+str(quad[1])+','+str(quad[2])+','+str(quad[3])+','+str(quad[4])+')'
	return strr



###########################################################################
#SYMBOLS TABLE
###########################################################################

def Record_Entity_Var(name,type,offset):
	global symbols_array
	entity = [name,type,offset]
	if(type == 'temp'):
		entity = [name,offset]
	symbols_array[len(symbols_array)-1][0].append(entity)



def Record_Entity_Func(name,type,start_quad,argument_list,framelength):
	global symbols_array
	global current_func
	entity = [name,type,start_quad,argument_list,framelength]
	symbols_array[len(symbols_array)-1][0].append(entity)
	current_func.append(symbols_array[len(symbols_array)-1][0][-1])





def Record_Entity_Par(name,par_mod,offset):
	global symbols_array
	global current_func
	entity = [name,par_mod,offset]
	symbols_array[len(symbols_array)-1][0].append(entity)
	current_func[-1][3].append(entity)




def Record_Scope(lst):
	global symbols_array
	global nesting_level
	scope = [lst,nesting_level]
	nesting_level = nesting_level + 1
	symbols_array.append(scope)



def Search_Entity(name):
	global symbols_array
	for j in reversed(symbols_array):
		for i in reversed(j[0]):
			#if(j[1] != nesting_level-1):
			if(i[0] == name):
				#print(name+str(j[1])+'MASSSSSSSSSSSSSSSS')
				return i,j[1]
	Error_Manager('Symbols Array',name,-1,"Undeclared variable")
				



def Delete_Scope():
	global symbols_array
	global permanent_scopes_array
	global nesting_level
	global current_func
	permanent_scopes_array.append(symbols_array[-1])
	nesting_level = nesting_level - 1
	framelength = Count_Offset()
	if(len(current_func) != 0):
		current_func[-1][4] = framelength
		del current_func[-1]
	del symbols_array[-1]



def Print_Array():
	global total_size
	s = ''
	for i in range(len(permanent_scopes_array)):
		s+='('+str(permanent_scopes_array[i][1])+')'
		for j in range(len(permanent_scopes_array[i][0])):
			s+='<-'+str(permanent_scopes_array[i][0][j])
		print(s+'\n')
		s = ''
	print('Framelength of program '+program_name+': '+str(total_size))


def Count_Offset():
	global symbols_array
	func_counter = 0
	counter = 8
	entities = len(symbols_array[-1][0])
	for i in range(len(symbols_array[-1][0])):
		if(len(symbols_array[-1][0][i]) == 5):
			func_counter += 1
	counter = counter + (entities*4) + 4 -(func_counter*4)
	return counter



	




###########################################################################
#FINAL CODE
#All final's code creation related functions	
###########################################################################




###########################################################################
#GNVLCODE
###########################################################################	
def gnvlcode(v):
	global final_code_list
	try:
		(entity,nest) = Search_Entity(v)
	except:
		Error_Manager('Symbols Array',v,-1,"Undeclared variable")	
	counter = 1
	n = nesting_level-1-nest-1
	while(n>0):
		counter += 1
		n -= 1
	string_command = '	lw $t0,-'+str(counter*4)+'($sp)'
	final_code_list.append(string_command)
	string_command = '	addi $t0,$t0,-'+str(entity[2])
	final_code_list.append(string_command)





###########################################################################
#LOADVR
###########################################################################	
def loadvr(v,r):
	if str(v).isdigit():
		string_command = '	li $'+str(r)+','+str(v)
		final_code_list.append(string_command)
	else:
		try:
			(entity,nest) = Search_Entity(v)
		except:
			Error_Manager('Symbols Array',v,-1,"Undeclared variable")
		if(entity[1] == 'int' and nest == 0 and nest != nesting_level-1):
			string_command = '	lw $'+str(r)+',-'+str(entity[2])+'($s0)'
			final_code_list.append(string_command)
		elif(nest == nesting_level-1):
			if(entity[1] == 'int' or entity[1] == 'cv'):
				string_command = '	lw $'+str(r)+',-'+str(entity[2])+'($sp)'
				final_code_list.append(string_command)
			elif(len(entity)==2):
				string_command = '	lw $'+str(r)+',-'+str(entity[1])+'($sp)'
				final_code_list.append(string_command)
			elif(entity[1] == 'ref'):
				string_command = '	lw $t0,-'+str(entity[2])+'($sp)'
				final_code_list.append(string_command)
				string_command = '	lw $'+str(r)+',($t0)' 
				final_code_list.append(string_command)
		elif(nest < nesting_level-1):
			if(entity[1] == 'int' or entity[1] == 'cv'):
				gnvlcode(entity[0])
				string_command = '	lw $'+str(r)+',($t0)' 
				final_code_list.append(string_command)
			elif(entity[1] == 'ref'):
				gnvlcode(entity[0])
				string_command = '	lw $t0,($t0)' 
				final_code_list.append(string_command)
				string_command = '	lw $'+str(r)+',($t0)' 
				final_code_list.append(string_command)



###########################################################################
#STORERV
###########################################################################	
def storerv(r,v):
	
	try:
		(entity,nest) = Search_Entity(v)
	except:
		Error_Manager('Symbols Array',v,-1,"Undeclared variable")
	if(entity[1] == 'int' and nest == 0 and nest != nesting_level-1):
		string_command = '	sw $'+str(r)+',-'+str(entity[2])+'($s0)'
		final_code_list.append(string_command)
	elif(nest == nesting_level-1):
		if(entity[1] == 'int' or entity[1] == 'cv'):
			string_command = '	sw $'+str(r)+',-'+str(entity[2])+'($sp)'
			final_code_list.append(string_command)
		elif(len(entity)==2):
			string_command = '	sw $'+str(r)+',-'+str(entity[1])+'($sp)'
			final_code_list.append(string_command)
		elif(entity[1] == 'ref'):
			string_command = '	lw $t0,-'+str(entity[2])+'($sp)'
			final_code_list.append(string_command)
			string_command = '	sw $'+str(r)+',($t0)' 
			final_code_list.append(string_command)
	elif(nest < nesting_level-1):
		if(entity[1] == 'int' or entity[1] == 'cv'):
			gnvlcode(entity[0])
			string_command = '	sw $'+str(r)+',($t0)' 
			final_code_list.append(string_command)
		elif(entity[1] == 'ref'):
			gnvlcode(entity[0])
			string_command = '	lw $t0,($t0)' 
			final_code_list.append(string_command)
			string_command = '	sw $'+str(r)+',($t0)' 
			final_code_list.append(string_command)
	
	
	
	
	
	
	

###########################################################################
#CREATE_ASM_FILE
#Fill the final_code_list array with assembly commands
###########################################################################		
def Create_Asm_File():	
	global quads_list
	global pointer
	global final_code_list
	global func_labels
	global current_func
	global arg_list
	global call_framelengths
	global flag
	filename = "final_code.asm"
	file = open(filename, 'w')
	i = 0
	while(pointer < len(quads_list)):
		string_command = ''
		line_number = quads_list[pointer][0]
		line = 'L'+str(line_number)
		linee = line+':'
		final_code_list.append(linee)
		element = quads_list[pointer][1]
		x = quads_list[pointer][2]
		y = quads_list[pointer][3]
		label = quads_list[pointer][4]
		
		if(element == 'jump'):
			string_command = '	j L'+str(label)
			final_code_list.append(string_command)
		elif(element == 'begin_block'):
			if(x!=program_name):
				string_command = '	sw $ra,($sp)'
				final_code_list.append(string_command)
				func_labels.append([x,line])
			else:
				del final_code_list[-1]
				string_command = 'Lmain:'
				final_code_list.append(string_command)
				final_code_list.append(linee)
				string_command = '	addi $sp,$sp,'+str(total_size)
				final_code_list.append(string_command)
				string_command = '	move $s0,$sp'
				final_code_list.append(string_command)
		elif(element == 'end_block'):
			if(x!=program_name):
				string_command = '	lw $ra,($sp)'
				final_code_list.append(string_command)
				string_command = '	jr $ra'
				final_code_list.append(string_command)
		elif(element in ('=','>=','<=','<>','<','>') ):
			loadvr(x,'t1')
			loadvr(y,'t2')
			if(element == '='):
				string_command = '	beq $t1,$t2,L'+str(label)
				final_code_list.append(string_command)
			elif(element == '>='):
				string_command = '	bge $t1,$t2,L'+str(label)
				final_code_list.append(string_command)
			elif(element == '<='):
				string_command = '	ble $t1,$t2,L'+str(label)
				final_code_list.append(string_command)
			elif(element == '<>'):
				string_command = '	bne $t1,$t2,L'+str(label)
				final_code_list.append(string_command)
			elif(element == '<'):
				string_command = '	blt $t1,$t2,L'+str(label)
				final_code_list.append(string_command)
			elif(element == '>'):
				string_command = '	bgt $t1,$t2,L'+str(label)
				final_code_list.append(string_command)
		elif(element == ':='):
			loadvr(x,'t1')
			storerv('t1',label)
		elif(element in ('+','-','/','*')):
			loadvr(x,'t1')
			loadvr(y,'t2') 
			if(element == '+'):
				string_command = '	add $t1,$t1,$t2'
				final_code_list.append(string_command)
			elif(element == '-'):
				string_command = '	sub $t1,$t1,$t2'
				final_code_list.append(string_command)
			elif(element == '/'):
				string_command = '	div $t1,$t1,$t2'
				final_code_list.append(string_command)
			elif(element == '*'):
				string_command = '	mul $t1,$t1,$t2'
				final_code_list.append(string_command)
			storerv('t1',label)
		elif(element == 'out'):
			string_command = '	li $v0,1'
			final_code_list.append(string_command)
			loadvr(x,'a0')
			string_command = '	syscall'
			final_code_list.append(string_command)
		elif(element == 'inp'):
			string_command = '	li $v0,5'
			final_code_list.append(string_command)
			string_command = '	syscall'
			final_code_list.append(string_command)
			storerv('v0',x) 
		elif(element == 'retv'):
			loadvr(x,'t1')
			string_command = '	lw $t0,-8($sp)'
			final_code_list.append(string_command)
			string_command = '	sw $t1,($t0)' 
			final_code_list.append(string_command)
		elif(element == 'par'):
			(entity,nest) = Search_Entity(x)
			arg_list.append(y)
			if(quads_list[pointer-1][1] != 'par'):
				string_command = 'flag'+str(flag)####str(Count_Offset()-4)#######################################
				final_code_list.append(string_command)
				i = 0
			if(y == 'CV'):
				loadvr(x,'t0')
				string_command = '	sw $t0, -'+str(12+(4*i))+'($fp)'
				final_code_list.append(string_command)
			elif(y == 'RET'):
				del arg_list[-1]
				if(len(entity)==3):
					string_command = '	addi $t0,$sp,-'+str(entity[2])
					final_code_list.append(string_command)
					string_command = '	sw $t0,-8($fp)'
					final_code_list.append(string_command)
				else:
					string_command = '	addi $t0,$sp,-'+str(entity[1])
					final_code_list.append(string_command)
					string_command = '	sw $t0,-8($fp)'
					final_code_list.append(string_command)
			elif(y == 'REF'):
				#
				if(nest==nesting_level-1):
					if(entity[1] == 'int' or entity[1] == 'cv'):
						string_command = '	addi $t0,$sp,-'+str(entity[2])
						final_code_list.append(string_command)
						string_command = '	sw $t0, -'+str(12+(4*i))+'($fp)'
						final_code_list.append(string_command)
					elif(entity[1] == 'ref'):
						string_command = '	lw $t0,-'+str(entity[2])
						final_code_list.append(string_command)
						string_command = '	sw $t0, -'+str(12+(4*i))+'($fp)'
						final_code_list.append(string_command)
				elif(nest<nesting_level-1):
					if(entity[1] == 'int' or entity[1] == 'cv'):
						gnvlcode(entity[0])
						string_command = '	sw $t0, -' + str(12+(4*i))+'($fp)'
						final_code_list.append(string_command)
					elif(entity[1] == 'ref'):
						gnvlcode(entity[0])
						string_command = '	lw $t0,($t0)'
						final_code_list.append(string_command)
						string_command = '	sw $t0, -'+str(12+(4*i))+'($fp)'
						final_code_list.append(string_command)
						
			###
			i += 1
		elif(element == 'call'):
			(entity,nest) = Search_Entity(x)
			if(len(entity[3])!=0):
				stttt = 'flag'+str(flag)
				call_framelengths.append([stttt,entity[4]])
				flag+=1
			if(Check_Arguments(entity[3]) == False):
				Error_Manager('Symbols Array',x,-1,"Wrong Arguments in function")
			if(len(arg_list)==0):
				string_command = '	addi $fp, $sp,'+str(entity[4])###########rrrrrrr
				final_code_list.append(string_command)
			if(nest==nesting_level-2):
				string_command = '	lw $t0,-4($sp)'
				final_code_list.append(string_command)
				string_command = '	sw $t0,-4($fp)'
				final_code_list.append(string_command)
			else:	
				string_command = '	sw $sp,-4($fp)'
				final_code_list.append(string_command)
			string_command = '	addi $sp,$sp,'+str(entity[4])#######rrrrr
			final_code_list.append(string_command)
			string_command = '	jal '+str(Find_Func_Label(x))########
			final_code_list.append(string_command)
			string_command = '	addi $sp,$sp,-'+str(entity[4])#############rrrrr
			final_code_list.append(string_command)
			arg_list = []
		###
		pointer += 1





###########################################################################
#FIND_FUNC_LABEL
#Finds the label of each function/procedure
###########################################################################	
def Find_Func_Label(name):
	global func_labels
	for i in func_labels:
		#print(i[0])
		if(i[0] == name):
			return i[1]





###########################################################################
#WRITE_ASM
#Writes the .asm file with contents of final_code_list array
###########################################################################	
def Write_Asm():
	global asm_string
	global call_framelengths
	filename = "final_code.asm"
	file = open(filename, 'w')
	bool = False
	fixed_framelength = -1
	for string in final_code_list :
		for flag in call_framelengths:
			if(string == flag[0]):
				fixed_framelength = flag[1]
				bool = True
				break
		if(bool):
			string = '    addi $fp,$sp,'+str(fixed_framelength)
			file.write(string+'\n')
			bool = False
		else:
			file.write(string+'\n')
	
	
	
###########################################################################
#CHECK_ARGUMENT
#Checks if the funtion has called with right arguments.
#Otherwise returns False.
###########################################################################	
def Check_Arguments(func_args):
	global arg_list
	if(len(arg_list) == len(func_args)):
		for i in range(len(arg_list)):
			if(arg_list[i] == func_args[i][1].upper()):
				continue
			else:
				return False
		#arg_list = []
		return True
	else:
		#arg_list = []
		return False
	









###########################################################################
#SYNTAX ANALYZER	
#Syntax Analyzer does the syntactical analysis of a minimal++ code. 
#If everything is correct the program is ready for semantic analysis.
#Otherwise calls Error_Manager.
###########################################################################
def Syntax():													
	global token
	token = Lex()											#creates the first token and calls the program function
	Program()




###########################################################################
#IS_CONSTANT
#Checks if a variable is an integer and returns True.
#Otherwise returns False.
###########################################################################	
def is_Constant(x):
	try:
		val = int(x)
		return True
	except ValueError:
		return False
		
		
		
		
###########################################################################
#IS_STATEMENT (not used)
#Checks if a token belongs to statements list.
###########################################################################
def is_Statement(token):
	if token in statement_list:
		return True
	else:
		return False		
	



	
###########################################################################
#IS_ID
#Checks if a token is acceptable ID. 
###########################################################################		
def is_ID(token):
	if(token == ''):
			Error_Manager("Syntactical Analysis",token,line_counter,"ID or } was expected but found this")
	if(token[0].isalpha()):
		if token not in commands_list:
			return True
		else:return False
	else:
		return False
		





	
###########################################################################
#<PROGRAM>
#Checks if the file starts with keyword 'program'.Then checks if the code
#is in '{'  '}'.If everything is correct prints success else calls 
#Error Manager.
###########################################################################
def Program():
	global token,program_name
	#print(token)
	if token == 'program':
	
		token = Lex()
		
		#print(token)
		program_name = token
		if is_ID(token):
			token = Lex()
			#print(token)
			if token == '{':
				token = Lex()
				if token == '}':
					print("\n\t ***Syntactical Analysis was successful***")
				else:
					Record_Scope([])
					#Record_Entity_Func(program_name,'main',[],Nextquad(),0)
					Block(program_name)
					
					if token == '}':
						print("\n\t ***Syntactical Analysis was successful***")
					else:
						Error_Manager("Syntactical Analysis",token,line_counter," '}' was expected at the end of file but found this")
			else:
				Error_Manager("Syntactical Analysis",token,line_counter," '{' was expected after program's id but found this")
		else:
			Error_Manager("Syntactical Analysis",token,line_counter,"Name of program was expected but found this")
	else:
		Error_Manager("Syntactical Analysis",token,line_counter,"Keyword program was expected but found this")






###########################################################################
#<BLOCK>
###########################################################################
def Block(name):
	global total_size
	global final_code_list
	Declarations()
	Subprograms()
	Genquad('begin_block',name,'_','_')
	Statements()
	if(name != program_name):
		#gnvlcode('a')
		#print(final_code_list)
		Genquad('end_block',name,'_','_')
	else:
		total_size = Count_Offset()
		#current_func[0][4] = total_size
		Genquad('halt','_','_','_')
		Genquad('end_block',name,'_','_')
		
	Create_Asm_File()
	Delete_Scope()




###########################################################################
#<DECLARATIONS>
#Checks if the program has declarations
#Declare has to close with ';'
###########################################################################
def Declarations():
	global token,all_ids,c_all_ids
	while token == 'declare':
		token = Lex()
		Varlist()
		if token != ';':
			Error_Manager("Syntactical Analysis",token,line_counter,"';' was expected after declarations but found this")
		else:
			token = Lex()
	c_all_ids = all_ids
	all_ids = []
			
			
	
	
###########################################################################
#<VARLIST>
#Checks if tokens are acceptable IDs and they are separated by commas
###########################################################################
def Varlist():
	global token,all_ids
	if is_ID(token):
		if(token in all_ids or token in all_functions):
			Error_Manager("Syntactical Analysis",token,line_counter,"Name already taken")
		all_ids.append(token)
		Record_Entity_Var(token,'int',Count_Offset())
		token = Lex()
		while token == ',':
			token = Lex()
			if is_ID(token) == False:
				Error_Manager("Syntactical Analysis",token,line_counter,"Id was expected for declaration but found this")
			if(token in all_ids or token in all_functions):
				Error_Manager("Syntactical Analysis",token,line_counter,"Name already taken")
			all_ids.append(token)
			Record_Entity_Var(token,'int',Count_Offset())
			token = Lex()




			
###########################################################################
#<SUBPROGRAMS>
#Checks if we have functions or procedures
###########################################################################			
def Subprograms():
	global token,name
	global func_ret
	#token = Lex()
	
	while token == 'function' or token == 'procedure':
		type = token
		token = Lex()
		if(type == 'function'):
			func_ret.append(token)
		Subprogram(type)
		token = Lex()
	



###########################################################################
#<SUBPROGRAM>
###########################################################################
def Subprogram(type):
	global all_functions
	global all_ids
	global token
	if is_ID(token):
		function_name = token
		if(function_name in all_functions or function_name in all_ids):
			Error_Manager("Syntactical Analysis",token,line_counter,"Name already taken")
		all_functions.append(function_name)	
		Record_Entity_Func(function_name,type,Nextquad()+1,[],0)
		token = Lex()
		Funcbody(function_name)




		
###########################################################################
#<FUNCBODY>
#Calls <BLOCK> inside function/procedure
###########################################################################		
def Funcbody(function_name):
	global token,func_ret
	Record_Scope([])
	Formalpars()
	if token == '{':
		token = Lex()
		Block(function_name)
		
		if(function_name in func_ret):
			Error_Manager("Syntactical Analysis",function_name,line_counter,"This function does not return")
		if token != '}':
			Error_Manager("Syntactical Analysis",token,line_counter,"This '}' character was expected to close function/procedure but found this")
	else:
		Error_Manager("Syntactical Analysis",token,line_counter,"This '{' character was expected to open function/procedure but found this")





###########################################################################
#<FORMALPARS>
#Checks if the arguments are inside of '()'
###########################################################################
def Formalpars():
	global token
	if token == '(':
		token = Lex()
		Formalparlist()
		if token == ')':
			token = Lex()
		else:
			Error_Manager("Syntactical Analysis",token,line_counter,"This ')' character was expected to close function's/procedure's arguments but found this")
	else:
		Error_Manager("Syntactical Analysis",token,line_counter,"This '(' character was expected after function/procedure id but found this")





###########################################################################
#<FORMALPARLIST>
#Check arguments acceptance
###########################################################################
def Formalparlist():
	global token
	if token != ')':
		if token != 'in' and token != 'inout' and token != '':
			Error_Manager("Syntactical Analysis",token,line_counter," 'in' or 'inout' was expected after '(' for function's/procedure's arguments but found this")
		else:
			while token=='in' or token=='inout':
				par_mod = token
				token = Lex()
				Formalparitem(par_mod)
				token = Lex()
				if token==',':
					token = Lex()
					if token!='in' and token!='inout':
						Error_Manager("Syntactical Analysis",token,line_counter," 'in' or 'inout' was expected after ',' for function's/procedure's arguments but found this")
				else:
					if token == ')':
						continue
					else:
						Error_Manager("Syntactical Analysis",token,line_counter," ',' was expected after parameter but found this")



###########################################################################
#<FORMALPARITEM>
###########################################################################
def Formalparitem(par_mod):
	global token
	if is_ID(token) == False:
		Error_Manager("Syntactical Analysis",token,line_counter,"Id was expected after 'in'/'inout' but found this")
	else:
		if(par_mod == 'in'):
			par_mod = 'cv'
		else:
			par_mod = 'ref'
		Record_Entity_Par(token,par_mod,Count_Offset())
	




###########################################################################
#<STATEMENTS>
#Checks if we enter a statement block
###########################################################################		
def Statements():
	global token
	if token == '{':
		token = Lex()
		Statement()
		while token == ';':
			token = Lex()
			Statement()
			if token != '}' and token != ';':
				Error_Manager("Syntactical Analysis",token,line_counter," '}' was expected after statements but found this")
		token = Lex()
	else:
		Statement()




	
###########################################################################
#<STATEMENT>
#Checks if the statement is valid
###########################################################################
def Statement():
	global token
	if is_ID(token): #Assignment-stat
		assignment_Stat(token)
	elif token == 'if': #If-stat
		if_Stat()
	elif token == 'while': #While-stat
		while_Stat()
	elif token == 'doublewhile': #Doublewhile-stat
		doublewhile_Stat()
	elif token == 'loop': #Loop-stat
		loop_Stat()
	elif token == 'exit': #Exit-stat
		exit_Stat()
	elif token == 'forcase': #Forcase-stat
		forcase_Stat()
	elif token == 'incase': #Incase-stat
		incase_Stat()
	elif token == 'call': #Call-stat
		call_Stat()
	elif token == 'return': #Return-stat
		return_Stat()
	elif token == 'input': #Input-stat
		input_Stat()
	elif token == 'print': #Print-stat
		print_Stat()

			
####################################################################	
#<ASSIGNMENT_STAT>
####################################################################
def assignment_Stat(id):
	global token
	token = Lex()
	if token == ':=':
		token = Lex()
		exp = Expression()
		
		Genquad(':=',exp,'_',id)
	else:
		Error_Manager("Syntactical Analysis",token,line_counter," ':=' was expected to assign value but found this")
		
		
		
		
		

#####################################################################
#<IF_STAT>
#####################################################################
def if_Stat():
	global token
	token = Lex()
	if token == '(':
		token = Lex()
		(b_true,b_false) = Condition()
		if token == ')':
			token = Lex()
			if token == 'then':
				Backpatch(b_true,Nextquad())
				
				token = Lex()
				Statements()
				ifList = Makelist(Nextquad())
				Genquad('jump','_','_','_')
				Backpatch(b_false,Nextquad())
				else_Part()
				Backpatch(ifList,Nextquad())
			else:
				Error_Manager("Syntactical Analysis",token,line_counter," Keyword 'then' was expected after 'if' but found this")
		else:
			Error_Manager("Syntactical Analysis",token,line_counter," ')' was expected after if's arguments but found this")
	else:
		Error_Manager("Syntactical Analysis",token,line_counter," '(' was expected after 'if' but found this")
		
		
		


###########################################################################
#<ELSE_PART>
###########################################################################
def else_Part():
	global token
	if token == 'else':
		token = Lex()
		Statements()
		
		
		
		
		
####################################################################	
#<WHILE_STAT>
####################################################################
def while_Stat():
	global token
	token = Lex()
	if token == '(':
		token = Lex()
		Bquad = Nextquad()
		(b_true,b_false) = Condition()
		Backpatch(b_true,Nextquad())
		if token == ')':
			token = Lex()
			Statements()
			Genquad('jump','_','_',Bquad)
			Backpatch(b_false,Nextquad())
		else:
			Error_Manager("Syntactical Analysis",token,line_counter," ')' was expected to close 'while' but found this")
	else:
		Error_Manager("Syntactical Analysis",token,line_counter," '(' was expected after 'while' but found this")






####################################################################	
#<DOUBLEWHILE_STAT>
####################################################################
def doublewhile_Stat():
	global token
	token = Lex()
	if token == '(':
		token = Lex()
		Condition()
		if token == ')':
			token = Lex()
			Statements()
			if token == 'else':
				token = Lex()
				Statements()
			else:
				Error_Manager("Syntactical Analysis",token,line_counter," Keyword 'else' was expected after 'doublewhile' but found this")
		else:
			Error_Manager("Syntactical Analysis",token,line_counter," ')' was expected to close 'doublewhile' but found this")
	else:
		Error_Manager("Syntactical Analysis",token,line_counter," '(' was expected after 'doublewhile' but found this")








####################################################################	
#<LOOP_STAT>
####################################################################	
def loop_Stat():
	global token
	token = Lex()
	Statements()
	
	
	
	
####################################################################	
#<EXIT_STAT>
####################################################################	
def exit_Stat():
	global token
	token = Lex()
	
	
	
	

####################################################################	
#<FORCASE_STAT>
####################################################################	
def forcase_Stat():
	global token
	token = Lex()
	Bquad = Nextquad()
	while token == 'when':
		token = Lex()
		if token == '(':
			token = Lex()
			(b_true,b_false) = Condition()
			if token == ')':
				token = Lex()
				if token == ':':
					token = Lex()
					Backpatch(b_true,Nextquad())
					Statements()
					Genquad('jump','_','_',Bquad)
					Backpatch(b_false,Nextquad())
				else:
					Error_Manager("Syntactical Analysis",token,line_counter," ':' was expected after when's condition in forcase, but found this")
			else:
				Error_Manager("Syntactical Analysis",token,line_counter," ')' was expected to close condition in forcase, but found this")
		else:
			Error_Manager("Syntactical Analysis",token,line_counter," '(' was expected to give conditions in forcase, but found this ")
	if token == 'default':
		token = Lex()
		if token == ':':
			token = Lex()
			Statements()
		else:
			Error_Manager("Syntactical Analysis",token,line_counter," ':' was expected after 'default' but found this")
	else:
		Error_Manager("Syntactical Analysis",token,line_counter," 'default' was expected but found this")






		
####################################################################	
#<INCASE_STAT>
####################################################################	
def incase_Stat():
	global token
	token = Lex()
	while token == 'when':
		token = Lex()
		if token == '(':
			token = Lex()
			Condition()
			if token == ')':
				token = Lex()
				if token == ':':
					token = Lex()
					Statements()
				else:
					Error_Manager("Syntactical Analysis",token,line_counter," ':' was expected after when's condition in incase, but found this")
			else:
				Error_Manager("Syntactical Analysis",token,line_counter," ')' was expected after when's condition in incase, but found this")
		else:
			Error_Manager("Syntactical Analysis",token,line_counter," '(' was expected to give conditions in incase, but found this")




####################################################################	
#<CALL_STAT>
####################################################################	
def call_Stat():
	global token
	global fix
	global id_tails
	token = Lex()
	if is_ID(token):
		if(token not in all_functions):
			Error_Manager("Syntactical Analysis",token,line_counter,"Undeclared Function")
		name = token
		token = Lex()
		if(len(fix)!=0):
			for i in range(len(fix)):
				id_tails.append(fix[i])
		fix = []
		Actualpars()
		#w = NewTemp()
		for i in range(len(fix)):
			if(fix[i][0] == 'in'):
				Genquad('par',fix[i][1],'CV','_')
			elif(fix[i][0] == 'inout'):
				Genquad('par',fix[i][1],'REF','_')
		#Genquad('par',w,'RET','_')
		fix = []
		Genquad('call',name,'_','_')
	else:
		Error_Manager("Syntactical Analysis",token,line_counter," 'id' was expected after 'call' but found this")
		
		
		
		
####################################################################	
#<RETURN_STAT>
####################################################################	
def return_Stat():
	global token,func_ret
	token = Lex()
	exp = Expression()
	Genquad('retv',exp,'_','_')
	if(len(current_func)>0 and current_func[-1][1]=='procedure'):
		Error_Manager("Syntactical Analysis",current_func[-1][0],line_counter,"Procedures can't return")
	try:
		del func_ret[-1]
	except:
		Error_Manager("Syntactical Analysis",program_name,line_counter,"Main program can't return")
	
	
	
	

####################################################################	
#<INPUT_STAT>
####################################################################	
def input_Stat():
	global token
	token = Lex()
	if token == '(':
		token = Lex()
		if is_ID(token):
			Genquad('inp',token,'_','_')
			token = Lex()
			if token == ')':
				token = Lex()
			else:
				Error_Manager("Syntactical Analysis",token,line_counter," ')' was expected to close 'call' but found this")
		else:
			Error_Manager("Syntactical Analysis",token,line_counter," 'id' was expected after 'input' but found this")
	else:
		Error_Manager("Syntactical Analysis",token,line_counter," '(' was expected to give conditions to 'call' but found this")





####################################################################	
#<PRINT_STAT>
####################################################################	
def print_Stat():
	global token
	token = Lex()
	if token == '(':
		token = Lex()
		if token == ')':
			Error_Manager("Syntactical Analysis",token,line_counter,"Print needs an expression inside but found this")
		else:
			exp = Expression()
			Genquad('out',exp,'_','_')
			if token == ')':
				token = Lex()
			else:
				Error_Manager("Syntactical Analysis",token,line_counter," ')' was expected to close print but found this")		
	else:
		Error_Manager("Syntactical Analysis",token,line_counter," '(' was expected to give conditions to print but found this")




####################################################################	
#<EXPRESSION>
####################################################################
def Expression():
	global token
	flag = 0
	oop = Optional_sign()
	expression = Term()
	if oop != None:
		tmp = NewTemp()
		Genquad(oop,0,expression,tmp)
		flag = 1
		expression = tmp
	while token == '+' or token == '-':
		op = token
		token = Lex()
		term = Term()
		if flag == 0:
			tmp2 = NewTemp()
			Genquad(op,expression,term,tmp2)
			expression = tmp2
		else:
			tmp2 = NewTemp()
			Genquad(op,tmp,term,tmp2)
			expression = tmp2
	return expression
		
		


	
###########################################################################
#<TERM>
###########################################################################
def Term():
	global token
	term = Factor()
	while token == '*' or token == '/':
		op = token
		token = Lex()
		fact = Factor()
		tmp = NewTemp()
		Genquad(op,term,fact,tmp)
		term = tmp
	return term
		



###########################################################################
#<FACTOR>
#CHECKS WHAT TYPE OF TERM WE HAVE
###########################################################################	
def Factor():
	global token
	if is_Constant(token):
		const = token
		token = Lex()
		return const
	elif token == '(':
		token = Lex()
		exp = Expression()
		if token == ')':
			token = Lex()
			return exp
	elif is_ID(token):
		id = token 
		#Record_Entity_Var(id,'int',Count_Offset())
		token = Lex()
		id2 = Idtail(id)
		if(id2 != None):
			id = id2
		return id
	else:
		Error_Manager("Syntactical Analysis",token,line_counter,"Expression was expected after operator but found this")
		




###########################################################################
#<IDTAIL>
###########################################################################				
def Idtail(id):
	global token
	global id_tail_flag
	global fix
	global id_tails
	if token == '(':
		if(len(fix)!=0):
			for i in range(len(fix)):
				id_tails.append(fix[i])
		fix = []
		if(id not in all_functions):
			Error_Manager("Syntactical Analysis",id,line_counter,"Undeclared Function")
		Actualpars()
		w = NewTemp()
		for i in range(len(fix)):
			if(fix[i][0] == 'in'):
				Genquad('par',fix[i][1],'CV','_')
			elif(fix[i][0] == 'inout'):
				Genquad('par',fix[i][1],'REF','_')
		Genquad('par',w,'RET','_')
		fix = []
		Genquad('call',id,'_','_')
		id_tail_flag = True
		return w



###########################################################################
#<ACTUALPARS>
#CHECKS THE SYNTAX TO MAKE SURE THERE ARE PARENTHESIS BEFORE 
#THE LIST OF ARGUMENTS
###########################################################################			
def Actualpars():
	global token
	global id_tails
	if token == '(':
		token = Lex()
		Actualparlist()
		if token == ')':
			token = Lex()
			if(id_tail_flag == True):
				for i in range(len(id_tails)):
					if(id_tails[i][0] == 'in'):
						Genquad('par',id_tails[i][1],'CV','_')
					elif(id_tails[i][0] == 'inout'):
						Genquad('par',id_tails[i][1],'REF','_')
				id_tails = []
		else:
			Error_Manager("Syntactical Analysis",token,line_counter," ')' was expected after arguments but found this")
	else:
		Error_Manager("Syntactical Analysis",token,line_counter," '(' was expected to give arguments but found this")
		




###########################################################################
#<ACTUALPARLIST>
#CHECKS IF WE HAVE MULTIPLE ARGUMENTS STARTING WITH IN/INOUT
#AND IF THEY ARE SEPERATED BY COMMAS
###########################################################################
def Actualparlist():
	global token
	global id_tail_flag
	id_tail_flag = False
	if token != ')':
		if token != 'in' and token != 'inout':
			Error_Manager("Syntactical Analysis",token,line_counter," 'in' or 'inout' was expected but found this")
		else:
			while token == 'in' or token == 'inout':							#THEMA ME ','
				if token == 'in':
					Actualparitem()
					#token = Lex()
				else:
					Actualparitem()
					token = Lex()
				if token == ',':
					token = Lex()
					if token != 'in' and token != 'inout':
						Error_Manager("Syntactical Analysis",token,line_counter," 'in' or 'inout' was expected but found this")
				else:
					if token == ')':
						continue
					else:
						Error_Manager("Syntactical Analysis",token,line_counter," ',' was expected after parameter but found this")
						




###########################################################################
#<ACTUALPARITEM>
###########################################################################
def Actualparitem():
	global token
	global id_tail_flag
	global id_tails
	if token == 'in':
		token = Lex()
		e = Expression()
		if(id_tail_flag != True):
			fix.append(['in',e])
		else: 
			id_tails.append(['in',e])
	elif token == 'inout':
		token = Lex()
		#Genquad('par',token,'REF','_')
		if is_ID(token)==False:
			Error_Manager("Syntactical Analysis",token,line_counter," 'id' was expected after 'in'/'inout' but found this")
		fix.append(['inout',token])


###########################################################################
#<CONDITION>
###########################################################################
def Condition():
	global token
	(b_true,b_false) = Boolterm()
	while token == 'or':
		Backpatch(b_false,Nextquad())
		token = Lex()
		(q2_true,q2_false)=Boolterm()
		b_true = Merge(b_true,q2_true)
		b_false = q2_false
	return (b_true,b_false)




###########################################################################
#<BOOLTERM>
###########################################################################
def Boolterm():
	global token
	(q_true,q_false) = Boolfactor()
	while token == 'and':
		Backpatch(q_true,Nextquad())
		token = Lex()
		(r2_true,r2_false)=Boolfactor()
		q_false = Merge(q_false,r2_false)
		q_true = r2_true
	return (q_true,q_false)



###########################################################################
#<BOOLFACTOR>
###########################################################################
def Boolfactor():
	global token
	if token == 'not':
		token = Lex()
		if token == '[':
			token = Lex()
			return_lists = Condition()
			true_list = return_lists[0]
			false_list = return_lists[1]
			lists = (false_list,true_list)
			if token == ']':
				token = Lex()
			else:
				Error_Manager("Syntactical Analysis",token,line_counter," ']' was expected to close 'not' conditions but found this")
		else:
			Error_Manager("Syntactical Analysis",token,line_counter," '[' was expected after 'not' but found this")
	elif token == '[':
		token = Lex()
		lists = Condition()
		if token == ']':
			token = Lex()
		else:
			Error_Manager("Syntactical Analysis",token,line_counter," ']' was expected to close conditions but found this")
	else:
		expression1 = Expression()
		op = relational_Oper()
		expression2 = Expression()
		r_true = Makelist(Nextquad())
		Genquad(op,expression1,expression2,'_')
		r_false = Makelist(Nextquad())
		Genquad('jump','_','_','_')
		lists = (r_true,r_false)
	return lists

###########################################################################
#<RELATIONAL_OPER>
###########################################################################
def relational_Oper():
	global token
	if token in ('=','>=','<=','<>','<','>'):
		op = token
		token = Lex()
		return op
	else:
		Error_Manager("Syntactical Analysis",token,line_counter," Relational operator was expected but found this")
		
		


###########################################################################
#<OPTIONAL_SIGN>
###########################################################################
def Optional_sign():
	global token 
	if token == '+' or token == '-':
		op = token
		token = Lex()
		return op






















###########################################################################
#Main 
#Creates important variables and starts the program
###########################################################################





def GetFile():
	try:
		filename = sys.argv[1]
	except:
		print("You did not give a file")
		sys.exit()
	return filename









filename = GetFile()
file = File_Manager(filename)
token = ''	
program_name = ''				
line_counter = 1			#Number of lines in the file
char_counter = 0			#Number of chars in the file
max_letter_counter = 0		#counter for variable's maximum characters
tag_number = 1				#tag number
quads_list = []				#List with quad lists
temp_number = 0				#Num of temp variable
all_ids = []
all_functions = []
arg_list = []
flag = 0
func_ret = []
int_size_checker = False
id_tail_flag = False
id_tails = []
c_all_ids = []
fix = []
nesting_level = 0
symbols_array = []
permanent_scopes_array = []
current_func = []
call_framelengths = []
total_size = 0
final_code_list = ['L0:\n\tb Lmain']
pointer = 0
asm_string = ''
func_labels = []
commands_list = ['program','declare','function','procedure','in','inout','if','then','else','while','doublewhile','loop','exit','forcase','when','default','incase','return','call','print','input','or','and','not']


##################
Syntax()
Create_Int_File()
Create_C_File()
Print_Array()
Write_Asm()
##################

		
	
	
	
	
	
	
	
	
	
	
	
