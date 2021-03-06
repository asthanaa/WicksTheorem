#This file is the printing part of the whole program. Everthing is being rinted here
#1st part is where contractions are made
#2nd part is where contractions are printed
#3rd partis where there are no contractions and only cummulants and operators are printed.


from collections import deque
import copy
import parity
import func_ewt
func=func_ewt
def fix_con(op_no, cnt, lim_cnt, t_list, matched, contracted, contracted_l, contracted_r, a, i, u, full, f, full_pos, i_c):
    cnt_tmp=cnt+1 # put condition of limiting cnt
    index = 0
    if cnt<lim_cnt and lim_cnt!=0:
        t_list_tmp = copy.deepcopy(t_list)
        t_list_tmp.popleft()
        op_no=op_no+1 #now the +1th annhilation operator is being seen
        while (t_list_tmp):
	    flag=1
    	    while (flag):
		flag=0
		if not t_list_tmp:
	            flag=1
		    return
		elif not t_list_tmp[0]:
		    t_list_tmp.popleft()
	            op_no=op_no+1
		    flag=1
		elif (t_list_tmp[0][0]):
		    for item in matched:
			if item.pos==t_list_tmp[0][0].pos or item.pos==full[op_no].pos:
			    flag=1
			    t_list_tmp[0].popleft()
			    break
            contracted_l.append(full[op_no])
	    contracted_r.append(t_list_tmp[0][0])
	    matched.append(full[op_no])
	    matched.append(t_list_tmp[0][0])
            fix_con(copy.copy(op_no), cnt+1, lim_cnt, copy.deepcopy(t_list_tmp), matched, contracted, contracted_l, contracted_r, a, i, u, full, f, full_pos, i_c)
	    matched.pop()
	    matched.pop()
	    t_list_tmp[0].popleft()
            if (len(t_list_tmp[0])==0):
                t_list_tmp.popleft()
		op_no=op_no+1
	    contracted_l.pop() #remove the last entered a, remove last contraction made
	    contracted_r.pop()
#-----------------------------------------------------------------------------------------------------------------------------------------
    #case when the number of contractions required are done. This we only have to print them
    elif lim_cnt!=0:
	output = deque([]) #stores the position of the output string
	
	#const_of_expression is the constant in case of a GWT
	const_of_expression = 1.0 

	const_of_cumulant = 1.0	
#lists declaration for loop factor check : spin_list_upper, spin_list_lower

	spin_list_upper=deque([])
	spin_list_lower=deque([])

	output_pos = [] #stores the actual string 
	output_name = deque([]) #stores the actual string 
	output_dag = deque([]) #stores the actual string 
	main_list = [] #stores the main list positions
	#make the main_list positions
	if not i_c :
	    sign = 1
	else :
	    sign = -1
	new_list = []
	full_formed = [] # stores the positions of the string formed after all the contractions
	#make th main_list from full
	for item in full:
	    main_list.append(item.pos)
	#make the output list (the order of operators that are in the output formed)
	for index in range(len(contracted_l)):
	    output.append(contracted_l[index])
	    output.append(contracted_r[index])
	    if (contracted_l[index].spin == contracted_r[index].spin):
		print "\n not multiplied\n"
	    else :
		const_of_expression=const_of_expression*(1.0/2.0)
	    #!!!!!make the spin change of the operators here. Think 
	    print const_of_expression, contracted_l[index].spin, contracted_r[index].spin
	flag=0
	#append all the operators that are not contracted
	func.normal_order_adv(full, output)
	# make the output list in name and pos
	for item in output:
	    output_name.append(item.name)
	    output_pos.append(item.pos)
	    output_dag.append(item.dag)
#	full_formed.extend(output_pos)
	#append the contraction in the list to be printed in the tec.txt
	for item in output:
	    print "spinn output", item.spin
	try:
	    for index in range(lim_cnt):
	        #When you pop an element from output, make sure is position is stored in full_formed
		tmp_1 = output.popleft()
		full_formed.append(tmp_1.pos)
		tmp_2 = output.popleft()
		full_formed.append(tmp_2.pos)

		#store spin in the list for checking the loop factor

		if tmp_1.dag=='1':

		    print "In the spin formation dag if case: spin :", tmp_1.dag, tmp_1.spin, tmp_2.dag, tmp_2.spin
    		    spin_list_upper.append(tmp_1.spin)
		    spin_list_lower.append(tmp_2.spin)
		else:
    		   
		    print "In the spin formation dag else case : spin :", tmp_1.dag, tmp_1.spin, tmp_2.dag, tmp_2.spin
		    spin_list_upper.append(tmp_2.spin)
		    spin_list_lower.append(tmp_1.spin)
		print "spin list u check : it should have all contracted ", spin_list_upper, lim_cnt 
		print "spin list l check : it should have all contracted ", spin_list_lower 
		    
		if tmp_1.kind != 'ac':
		    tmp_3 = '\delta_{'+tmp_1.name+tmp_2.name+'}'
		elif tmp_1.dag=='1':
		    tmp_3 = '\Gamma^'+tmp_1.name+'_{'+tmp_2.name+'}'
		elif tmp_1.dag=='0':
		    tmp_3 = '\eta^'+tmp_2.name+'_{'+tmp_1.name+'}'
		else :
		    print "!!!!not printing anywhere, if this occurs:there may be a problem"
		new_list.append(tmp_3)
	    #cumulant_present=0
	    
	    #formed cumulants being appended in new_list------------------------
	    const_of_cumulant=func.cummulant(contracted, full_formed, new_list)

	    if const_of_cumulant:
		const_of_expression = const_of_expression * const_of_cumulant
	    #const_of_expression=const_of_expression*const_from_cumulant
	    print "const of expression and cumulant", const_of_expression, const_of_cumulant
	# the summition thingy
	    if func.loop_present(spin_list_upper, spin_list_lower, -1, 0) :
	    #if not output and const_of_expression!=1.0 and not cumulant_present :
	        print "loop function executed"
                const_of_expression=const_of_expression*2.0
	    
	    #append all the normal ordered operators not contracted	
	    for item in output:
		full_formed.append(item.pos)
	    #print all the normal ordered operators not contracted
	    print full_formed, contracted, output
	    if output:
		func.write_normal_order(new_list, output)
	except:
	    print "The try statement in fix_uv did not work. Something wrong in the peice of code tin 'try'"
	#parity function at work ! Woaaa
	if (parity.parity(full_formed, full_pos)):
		sign=sign*(-1)
	if sign == (-1):
	    tmp_5 = '$$'+"-"+str(const_of_expression)+''.join(new_list)+"\\\\"+'$$'+'\n'
	    f.write(tmp_5)
	else :
	    tmp_5 = '$$'+"+"+str(const_of_expression)+''.join(new_list)+'\\\\'+'$$'+'\n'
	    f.write(tmp_5)
#--------------------------------------------------------------------------------------------------------------------
    #The case when no contractions are made, but cummulants are there/not there
    elif lim_cnt==0:
	#In case then no further contractions are made (lim_cnt = 0) this only print operators 	
	#initialise output and others used
	output = []
	output_name = []
	const_of_expression = 1.0	
	main_list = []#used for the original string
	output_pos = []
	full_formed = [] #this stores the 
	contracted_l = []#used to store the left part of a contracted string 
	contracted_r = []
	new_list = []
	if not i_c: #when the string is 1st part of a commutator
	    sign = 1
	else :
	    sign = -1
	#This is where the cumulants are made through 'cumulant' function and the Latex expression is stored in new_list to be printed later
	#cumulant_present=0
	const_of_cumulant=func.cummulant(contracted, full_formed, new_list)

	if const_of_cumulant:
	    const_of_expression = const_of_expression * const_of_cumulant
	#const_of_expression=const_of_expression*const_of_cumulant
	#const_of_expression=const_of_expression*const_from_cumulant
	#make the full position list - main_list
	for item in full:
	    main_list.append(item.pos)
	#make the normal ordered operators list in output
	func.normal_order(full, output, output_pos, full_formed)
	if output and not new_list and i_c:
	    pass
	elif output :
	    func.write_normal_order(new_list, output)#as the name suggest - writes the normal order in output file list
	    #parity function at work ! Woaaa
 	if (parity.parity(full_formed, full_pos)):
	    sign=sign*(-1)
	
	if sign == (-1):
	    tmp_5 = '$$'+"-"+str(const_of_expression)+''.join(new_list)+"\\\\"+'$$'+'\n'
	    f.write(tmp_5)
	else :
	    tmp_5 = '$$'+"+"+str(const_of_expression)+''.join(new_list)+'\\\\'+'$$'+'\n'
	    f.write(tmp_5)

