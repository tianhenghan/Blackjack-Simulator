# This program plays blackjack automatically w/ learning or manually. Blackjack pays 6 to 5.
# Surrender, double, insurance and split are only allowed on initial hand.
# Split is allowed as long as the values are equal. Blackjack pays 1 to 1 for split hands.
# Dealer hits on soft 17.
# The learnt strategy can be saved into a file.

# For manual play, line692 set1=0; line722 set3=0; line749 deactivate set4
# For random autoplay only, line692 set1=1, adjust set2; line722 set3=0; line749 deactivate set4
# For a random then a smart autoplay: line692 set1=1, adjust set2; line722 set3=0; line749 activate set 4; line757 adjust set5
# For (random then smart autoplay) repeat n>1 times, line692 set1=1; line722 set3=n; line781&787 adjust set6&7

import random
import time
import decimal
import pprint
import json

# update player's record after each game.
def win(pa5,pa60):

	pa5[0] += pa60
	pa5[2] += 1
	pa5[3] += 1
	
	return pa5
	

def push(pa5):

	pa5[2] += 1
	pa5[4] += 1
	
	return pa5
	
	
def lose(pa5,pa60):

	pa5[0] -= pa60
	pa5[2] += 1
	pa5[5] += 1
	
	return pa5
	

# used when need to reject a non-digit input when a non-negative digit is asked.
# isNum(a negative number) returns False.
def isNum(x):    

	if not x.count('.')>1: 
		return x.strip(' ').replace('.','').isdigit()
	else: 
		return False


# returns the value given a card's face.	
def value(face):

	if face in 'JQK': 	return 10
	
	elif face=='A': 	return 1
	
	else: 				return int(face)
		

# returns shuffled cards for numdecks decks.
def shuffle(numdecks):

	a = range(1, 53)*numdecks
	random.shuffle(a)
	
	d=[0]*52*numdecks
	
	for i in range (1,52*numdecks+1):
	
		if   a[i-1]>48: d[i-1]='K'
		
		elif a[i-1]>44: d[i-1]='Q'
		
		elif a[i-1]>40: d[i-1]='J'
		
		elif a[i-1]<5:	d[i-1]='A'
		
		else:			d[i-1] = str(int((a[i-1]+3.5)/4))
		
	return d
	

# returns an auto-generated or manually typed amount of insurance.
def insurance(asset,wager,ran):

	if ran!=0: ins=random.choice([0, 0.5*min(0.5*wager,asset-wager), min(0.5*wager,asset-wager)])
	
	else:
		ins = '-1'
		
		while (not isNum(ins)) or float(ins)<0 or float(ins)>min(0.5*wager,asset-wager):
		
			print '\nYou are allowed to buy an insurance up to $ ', min(0.5*wager,asset-wager),'.'
			ins=raw_input('Type an amount: $ ')
			
		ins=float(ins)
		
	asset -= ins
	
	return [asset,ins]
	

# check whether a hand is a blackjack.
def blackjack(deck):

	if 'A' in deck and ('10' in deck or 'J' in deck or 'Q' in deck or 'K' in deck) and len(deck)==2: 
		return True
	else: 
		return False
		

# returns the total point of a hand.
def total(deck):

	tot = 0
	
	for i in range(len(deck)):	tot += value(deck[i])
		
	if not 'A' in deck:	return tot
	
	elif 10+tot<22:     return 10+tot
	
	else:				return tot
	

# returns an auto-generated or manually typed action.
def decision(act,ran):

	if ran!=0:	
	
		d=random.choice(list(act))
	
	else:
	
		prompt = '\n'
		
		if 'h' in list(act): 	prompt+='hit-h '
		
		if 's' in list(act): 	prompt+='stand-s '
		
		if 'd' in list(act): 	prompt+='double-d '
		
		if 'e' in list(act):	prompt+='surrender-e '
		
		if 'p' in list(act): 	prompt+='split-p '
		
		prompt+=': '
		
		d = raw_input(prompt)
		
		while not d.strip() in list(act):
		
			d=raw_input('Choose one from the listed actions: ')
			
	return d.strip()
	

# when no party has a blackjack, evaluates each game and promotes record updates.
def result(pa):

	player=total(pa[1])
	dealer=total(pa[0])
	
	if 22>player>dealer: 			pa[5]=win(pa[5],pa[6][0])
	
	elif 22>dealer>player: 			pa[5]=lose(pa[5],pa[6][0])
	
	elif dealer>21 and player>21:	pa[5]=push(pa[5])
	
	elif 22>dealer==player: 		pa[5]=push(pa[5])
	
	elif player>21: 				pa[5]=lose(pa[5],pa[6][0])
	
	else: 							pa[5]=win(pa[5],pa[6][0])
	
	return pa[5]
	

# get wager and generate initial hands for both parties.
def part1(pa):

	if pa[3][0]!=0:		
	
		pa[6][0]=pa[3][2]
	
	else: 
	
		pa[6][0] = raw_input('\nYour wager in this round: $ ')
		
		while (not isNum(pa[6][0])) or float(pa[6][0])>pa[5][0] or float(pa[6][0])<=0: 
			pa[6][0]=raw_input('Give a positive amount allowed by your asset : $ ')
			
		pa[6][0]=float(pa[6][0])
		
	if pa[5][1]%pa[3][5]==0: 
	
		pa[2] = shuffle(pa[3][4])
		
		if (not pa[3][0]) or pa[3][3]:	print '\nDeck shuffled.'
			
	pa[0]=[]
	pa[1]=[]
	
	for i in range(2):	pa[0].append(pa[2].pop())
	for i in range(2): 	pa[1].append(pa[2].pop())
	
	if (pa[3][0]==0) or pa[3][3]:	print '\nPlayer:', pa[1], '\n\nDealer:', [pa[0][0],'?']
		
	return pa
	

# get player's actions until player's hand is final.
def part2(pa):

	if total(pa[1])<21:
	
		if not pa[6][3] in 'hsde':
		
			if pa[6][2]!=0 or pa[6][1]>0:	pa[6][3] = decision('hs',pa[3][0])
			
			elif pa[5][0]<2*pa[6][0]:		pa[6][3] = decision('hse',pa[3][0])
			
			else: 							pa[6][3] = decision('hsde',pa[3][0])
				
		if pa[6][2]!=0: 
		
			pa[4].append(pa[6][3])
			pa[7].append(findrow(pa[1],1))
			
		pa[4][0]=pa[6][3]
		
		if pa[6][3] == 'e':
		
			pa[5][2] += 1
			pa[5][0] -= 0.5*pa[6][0]
			pa[5][6] += 1
			
		elif pa[6][3] == 'h':
		
			while pa[6][3] == 'h':
			
				pa[1].append(pa[2].pop())
				
				if total(pa[1])>20:	 pa[6][3] = 's'
					
				else:
					if pa[3][0]==0 or pa[3][3]:
					
						print '\nPlayer:',pa[1], '\n\nDealer:', [pa[0][0],'?'] 
					
					pa[6][3]=decision('hs',pa[3][0])
					pa[4].append(pa[6][3])
					pa[7].append(findrow(pa[1],1))
					
		elif pa[6][3] == 'd':
		
			pa[1].append(pa[2].pop())
			pa[6][0] *= 2
			
	return pa
	

# finish dealer's hand and promote result evaluation.
def part3(pa):

	if not pa[6][3]=='e':
	
		while total(pa[0]) < 17 or (sum(value(pa[0][i]) for i in range(len(pa[0])))==7 and 'A' in pa[0]):	
		
			pa[0].append(pa[2].pop())
			
		if pa[6][2]==0 and (pa[3][0]==0 or pa[3][3]):
		
			print '\nPlayer:',pa[1],' sum:',total(pa[1]), '\n\nDealer:',pa[0],' sum:',total(pa[0])
			
		pa[5]=result(pa)
		
	return pa
	

# take in both parties' initial hands. Promote result evaluation if any blackjack exits.
# Otherwise, continue to collect player's actions.
def hand(pa):

	if blackjack(pa[0]) and not blackjack(pa[1]):
	
		if pa[6][2]==0 and (pa[3][0]==0 or pa[3][3]):
		
			print '\n\nPlayer:', pa[1], '\n\nDealer:',pa[0],'blackjack!'
			
		pa[5][0] += 3*pa[6][1]
		pa[5]=lose(pa[5],pa[6][0])
		
	elif blackjack(pa[0]) and blackjack(pa[1]):
	
		if pa[6][2]==0 and (pa[3][0]==0 or pa[3][3]): 
		
			print '\n\nPlayer:', pa[1], 'blackjack!','\n\nDealer:',pa[0],'blackjack!'
			
		pa[5][0] += 3*pa[6][1]
		pa[5]=push(pa[5])
		
	elif blackjack(pa[1]):
	
		if pa[6][2]==0 and (pa[3][0]==0 or pa[3][3]): 
		
			print '\n\nPlayer:', pa[1], 'blackjack!','\n\nDealer:', pa[0]
			
		if pa[6][2]==0:
		
			pa[5][0] += 0.2*pa[6][0]
			
		pa[5]=win(pa[5],pa[6][0])
		
	else:
	
		if pa[3][0]==2:	 pa=readpart2(pa)      #for autoplay using learnt strategy
		
		else: 	pa=part2(pa)
			
		pa=part3(pa)
		
	return pa
	

# return the row number in table 1 & 2--which keep info for strategy learning--for each game.
def findrow(player,v):  

	if v==0:
	
		if value(player[0])==value(player[1]): 	xx=value(player[0])+22
		
		elif 'A' in player: 					xx=value(player[0])+value(player[1])+12
		
		else: 									xx=value(player[0])+value(player[1])-5
		
	else:
	
		if 'A' in player: 						xx=total(player)+35
		
		else: 									xx=total(player)+28
		
	return xx


# update table 1 & 2 after each game.
def strategy(dealeri,playeri,asseti,assetf,act,table1,table2):

	xx=playeri[0]
	yy=value(dealeri)-1
	zz='hsdep'.find(act[0])
	
	table1[xx][yy][zz] = (table1[xx][yy][zz]*table2[xx][yy][zz]+assetf-asseti)/(table2[xx][yy][zz]+1)
	table2[xx][yy][zz] += 1
	
	if len(act)>1:
	
		for k in range(1,len(act)):
		
			xx=playeri[k]
			zz='hs'.find(act[k])
			
			table1[xx][yy][zz] = (table1[xx][yy][zz]*table2[xx][yy][zz]+assetf-asseti)/(table2[xx][yy][zz]+1)
			table2[xx][yy][zz] += 1	
			
	return [table1,table2]
	

# convert table 1 & 2 into a strategy table after finishing designated number of games.
def conversion(table1,table2):

	form = [[' ' for y in range(12)] for x in range(57)]
	
	for i in range(2,12):	form[0][i]=str(i)
	
	for i in range(1,16):	form[i][0]=i+4
	
	for i in range(16,24):	form[i][0]=i+497
	
	for i in range(24,34):	form[i][0]=101*(i-23)
		
	for i in range(34,49):	form[i][0]=i-29
	
	for i in range(49,57):	form[i][0]=i+464
	
			
	for xx in range(1,24):      ### 'p' is not allowed
	
		for yy in range(1,11):
		
			if sum(table2[xx-1][yy-1])>8:
			
				table1[xx-1][yy-1].pop()
				form[xx][yy]='hsde'[table1[xx-1][yy-1].index(max(table1[xx-1][yy-1]))]

	for xx in range(24,34):     ### 'p' is allowed
	
		for yy in range(1,11):
		
			if sum(table2[xx-1][yy-1])>10: 
			
				form[xx][yy]='hsdep'[table1[xx-1][yy-1].index(max(table1[xx-1][yy-1]))]
			
	for xx in range(34,57):
	
		for yy in range(1,11):
		
			if sum(table2[xx-1][yy-1])>4:
			
				table1[xx-1][yy-1].pop()
				table1[xx-1][yy-1].pop()
				table1[xx-1][yy-1].pop()
				form[xx][yy]='hs'[table1[xx-1][yy-1].index(max(table1[xx-1][yy-1]))]
			
	for xx in range(1,57):
	
		form[xx][11]=form[xx][1]
		form[xx][1]=' '
		
	form[0][0]=''
	form[0][1]=''
	
	return form
	

# Read a decisive decision from prior learnt strategy table for autoplay.
def readdecision(pa,act):
 
	if act=='hsde':
	
		if 'A' in pa[1]: 	xx=total(pa[1])+3
		
		else:				xx=total(pa[1])-4
		
	elif act=='hsdep':		xx=value(pa[1][0])+23
	
	elif 'A' in pa[1]: 		xx=total(pa[1])+36
	
	else: 					xx=total(pa[1])+29
		
	if pa[0][0]=='A': 		yy=11
	
	else: 					yy=value(pa[0][0])
	
	if pa[8][xx][yy]==' ': 	return 'h'
	
	else: 					return pa[8][xx][yy]
	

# Direct the readdecision function based on allowed actions.
def readpart2(pa):     

	if total(pa[1])<21:
	
		if not pa[6][3] in 'hsde':
		
			if pa[6][2]==0: pa[6][3]=readdecision(pa,'hsde')
			else: 			pa[6][3]=readdecision(pa,'hs')
			
		if pa[6][3] == 'e':
		
			pa[5][2] += 1
			pa[5][0] -= 0.5*pa[6][0]
			pa[5][6] += 1
			
		elif pa[6][3] == 'h':
		
			while pa[6][3] == 'h':
			
				pa[1].append(pa[2].pop())
				
				if total(pa[1])>20: pa[6][3] = 's'
				else: 				pa[6][3]=readdecision(pa,'hs')
				
		elif pa[6][3] == 'd':
		
			pa[1].append(pa[2].pop())
			pa[6][0] *= 2
			
	return pa
	

# Main code for autoplay utilizing prior learnt strategy table.
def readmain(pa):

	con='y'
	
	while con=='y':
	
		pa[6]=[0,0,0,' ']  # wager,ins,split,sometimes prior decision used to relay info between defs
		
		pa = part1(pa)
		
#		if value(pa[0][0])==1: [pa[5][0],pa[6][1]]=insurance(pa[5][0],pa[6][0],pa[3][0])

		if blackjack(pa[0]) or blackjack(pa[1]): 	pa=hand(pa)
		
		elif pa[6][1]==0 and value(pa[1][0])==value(pa[1][1]) and pa[5][0] >= 2*pa[6][0] and pa[1][0]!='A': 
		
			pa[6][3]=readdecision(pa,'hsdep')
			
			if pa[6][3]=='p':
			
				pa[6][2]=1
				pa11=pa[1][1]
				pa[1]=[pa[1][0], pa[2].pop()]
						
				pa=hand(pa)
				
				hand1=pa[1]
				pa[6][3]=' '
				pa[1]=[pa11, pa[2].pop()]
				
				pa=hand(pa)
				
			else: pa=hand(pa)
			
		elif pa[6][1]==0 and pa[5][0] >= 2*pa[6][0] and pa[1][0]==pa[1][1]=='A':
		
			pa[6][3]=readdecision(pa,'hsdep')
			
			if pa[6][3]=='p':
			
				pa[6][2]=1
				pa[1]=['A', pa[2].pop()]
				
				pa=part3(pa)
				
				hand1=pa[1]
				pa[1]=['A', pa[2].pop()]
				
				pa=part3(pa)
				
			else: pa=hand(pa)
			
		else: pa=hand(pa)
		
		pa[5][1] += 1
		
		if pa[5][1]>pa[3][1]-1: 	break
		
	return pa


# Main code for ramdom autoplay of the learning process or manual play.
def main(pa,table1,table2):

	con='y'
	
	while con=='y':
	
		pa[6]=[0,0,0,' ']   # wager,ins,split,sometimes prior decision used to relay info between defs
		pa[4]=[' ']
		pa[7]=[' ']
		
		pa = part1(pa)
		
		asseti=pa[5][0]
		pa[7][0]=findrow(pa[1],0)
		pa70=pa[7][0]
		dealeri=pa[0][0]
		BJ=False
		
#		if value(pa[0][0])==1: [pa[5][0],pa[6][1]]=insurance(pa[5][0],pa[6][0],pa[3][0])

		if blackjack(pa[0]) or blackjack(pa[1]):
		
			pa=hand(pa)
			BJ=True
			
		elif pa[6][1]==0 and value(pa[1][0])==value(pa[1][1]) and pa[5][0] >= 2*pa[6][0] and pa[1][0]!='A': 
		
			pa[6][3]=decision('hsdep',pa[3][0])
			
			if pa[6][3]=='p':
			
				pa[6][2]=1
				pa11=pa[1][1]
				pa[1]=[pa[1][0], pa[2].pop()]
				
				if pa[3][0]==0 or pa[3][3]:	 print '\nPlayer Hand 1 : ',pa[1]
				
				pa=hand(pa)
				
				if pa[3][0]==0 or pa[3][3]:	 print '\nPlayer Hand 1 : ',pa[1], 'Finished.\n'
				
				hand1=pa[1]
				
				pa[4][0]='p'
				[table1,table2]=strategy(dealeri,pa[7],asseti,pa[5][0],pa[4],table1,table2)
				
				pa[6][3]=' '
				pa[1]=[pa11, pa[2].pop()]
				
				if pa[3][0]==0 or pa[3][3]:	 print '\nPlayer Hand 2 : ',pa[1]
				
				pa=hand(pa)
				
				pa[4][0]='p'
				pa[7][0]=pa70
				[table1,table2]=strategy(dealeri,pa[7],asseti,pa[5][0],pa[4],table1,table2)
				
				if pa[3][0]==0 or pa[3][3]: 
				
					print '\nPlayer Hand 2 : ',pa[1], 'Finished.\n'
					
				if pa[3][0]==0 or pa[3][3]: 
				
					print '\nPlayer Hand 1 : ',hand1,'Sum : ',total(hand1),'\nPlayer Hand 2 : ',pa[1],'Sum : ',total(pa[1]),'\n\nDealer : ',pa[0],'Sum : ',total(pa[0])
				
				pa[4][0]='p'
				
			else: pa=hand(pa)
			
		elif pa[6][1]==0 and pa[5][0] >= 2*pa[6][0] and pa[1][0]==pa[1][1]=='A': 
		
			pa[6][3]=decision('hsdep',pa[3][0])
			
			if pa[6][3]=='p':
			
				pa[6][2]=1
				pa[1]=['A', pa[2].pop()]
				
				pa=part3(pa)
				
				hand1=pa[1]
				pa[1]=['A', pa[2].pop()]
				
				pa=part3(pa)
				
				if pa[3][0]==0 or pa[3][3]: 
				
					print '\nPlayer Hand 1 : ',hand1,'Sum : ',total(hand1),'\nPlayer Hand 2 : ',pa[1],'Sum : ',total(pa[1]),'\n\nDealer : ',pa[0],'Sum : ',total(pa[0])
				
				pa[4][0]='p'
				
			else: pa=hand(pa)
			
		else: pa=hand(pa)
		
		pa[5][1] += 1
		
		if pa[4][0]!='p' and not BJ: 
		
			[table1,table2]=strategy(dealeri,pa[7],asseti,pa[5][0],pa[4],table1,table2)
			
		if pa[3][0]==0 or pa[3][3]: 
		
			print '\nAfter',pa[5][1],'games, your asset is $ ',pa[5][0],'.\nYou have',pa[5][3],'wins,',pa[5][4], 'pushes,',pa[5][5],'losses and',pa[5][6],'surrenders out of',pa[5][2],'hands.'
	
		if pa[3][0]==1 and pa[5][1]>pa[3][1]-1:	 break
			
		elif pa[3][0]==0 and pa[5][0]<=0:
		
			print '\nYou are broke! Find a rehab center IMMEDIATELY!\n'
			break
			
		elif pa[3][0]==0:
		
			con='k'
			
			while con!='y' and con!='n':  
				con = raw_input('\nKeep betting, press "y"; if quitting, press "n".')
			
	if pa[5][0]> 0 and (pa[3][0]==0 or pa[3][3]): 
	
		print '\nYou are very wise and not addicted to gambling.\n'
		
	if pa[3][0]==1:
	
		form=conversion(table1,table2)
#		pprint.pprint(form)
		pa.append(form)                ### add pa[8], a record of learnt strategy
		
	return [pa,table1,table2]
	
	
# For those falling short, fill each innermost list of table to have length 5.
# The shortages are caused by the pop.()s in function conversion.
def tablefix(table):

	for i in range(len(table)):
	
		for j in range(len(table[0])):
		
			while len(table[i][j])<5: 	table[i][j].append(0.0)
			
	return table
	

# add statistics from table1b & table2b into table1a & table2a.
def tablemerge(table1a,table2a,table1b,table2b):

	table1 = [[[0.0 for z in range(5)] for y in range(len(table1a[0]))] for x in range(len(table1a))]
	table2 = [[[  0 for z in range(5)] for y in range(len(table2a[0]))] for x in range(len(table2a))]
	
	for i in range(len(tables)):
	
		for j in range(len(table[0])):
		
			table1[i][j]=[x + y for x, y in zip(table1a[i][j],table1b[i][j])]
			table2[i][j]=[x + y for x, y in zip(table2a[i][j],table2b[i][j])]
			
	return [table1,table2]
		
	
#random.seed(1)    
#print 'random seed is set to 1'		###turn it on when checking modified codes

pa=[ [ ],         [ ],     [ ],  	 [ ],   	  [ ],     [ ],	    [ ],  		[ ] ]
#	  0	  		   1	    2	   	  3		 	   4		5	  	 6			 7
#dealer hand, player hand, deck, autoplay para, actions, status, media para, player hands matching pa[4]

       # set1			 set2
pa[3]=[    1,            100000,        	 2,              False,          	 8,               56]
#random(1)/manual(0), num of games, wager/autobet, print details, num of decks used, shuffle after ... games
#disable/change the insurance calling line for random/manual switch


pa[5]=[0,      			0,   			0,  		 0,		 	 0,   	 0,			0] 
#    asset, num of (games played, hands played, winning hands, pushes, losses, surrenders


table1 = [[[0.0 for z in range(5)] for y in range(10)] for x in range(56)] # income/hand
table2 = [[[0 for z in range(5)] for y in range(10)] for x in range(56)]   # num of hands
#             actions hsdep	       deal's face card	   player's starting 2 cards
#for each table, the top half is for initial actions while the bottom is for further actions involving only 'hs'.
#two-part table has a flaw since split hand does not receive blackjack bonus.
#pa[4][0] is initial action, followed by pa[4][1],pa[4][2]...
#pa[7][0] is the row in table 1 for initial player hand, followed by pa[7][1], pa[7][2]...


if pa[3][0]==0:    # Manual mode: ask for wager before each game.

	pa[5][0] = raw_input('\nYour total asset in USD: $ ')
	
	while (not isNum(pa[5][0])) or float(pa[5][0])<=0: 	 pa[5][0] = raw_input('Enter a valid number: $ ')
		
	pa[5][0]=float(pa[5][0])
	
else:  pa[5][0]=pa[3][1]*pa[3][2]


# set3
showlearning=0   # Learning process has ... num of stages. The progress at each stages will be printed.
				 # For manual play or merely random autoplay, showlearning must be 0.

if showlearning == 0:    # Learning has 1 stage and the result will be printed.

	if pa[3][0]!=0:  start=decimal.Decimal(time.time())
	
	[pa,table1,table2]=main(pa,table1,table2)
	
	if pa[3][0]!=0:

		if False:		# whether to write to a file.
		
			f=open('table1.txt','w')
			f.write(json.dumps(table1))
			f.close()
			
			f=open('table2.txt','w')
			f.write(json.dumps(table2))
			f.close()
			
		end=decimal.Decimal(time.time())
		
		print '\n',(end-start),'total time in seconds\n', (end-start)*1000/pa[3][1], 'per time in milliseconds'
		print '\nAfter',pa[5][1],'games, your asset is $ ',pa[5][0],'.\nYou have',pa[5][3],'wins,',pa[5][4], 'pushes,',pa[5][5],'losses and',pa[5][6],'surrenders out of',pa[5][2],'hands.'


# set4
#	pa[3][0]=2		 # for autoplay w/ learning. Deactivate this code otherwise.
	

	if pa[3][0]==2:   # autoplay utilizing learnt strategy.
	
		start=decimal.Decimal(time.time())
		
#                  set5		
		pa[3][1] = 500000                        #number of games
		pa[5]=[pa[3][1]*pa[3][2], 0, 0, 0, 0, 0, 0]  #auto assignment of initial asset and zeros the rest
		
		if False:		# whether to read from a file.
		
			f=open('table1.txt')
			table1=json.load(f)
			f.close()
			
			f=open('table2.txt')
			table2=json.load(f)
			f.close()
			
			table1=tablefix(table1)
			table2=tablefix(table2)
			pa[8] = conversion(table1,table2)
			
		pa=readmain(pa)          #learnt strategy is included in pa[8]
		
		end=decimal.Decimal(time.time())
		
		print '\n',(end-start),'total time in seconds\n', (end-start)*1000/pa[3][1], 'per time in milliseconds'
		
		print '\nAfter',pa[5][1],'games, your asset is $ ',pa[5][0],'.'
		print '\nYou have',pa[5][3],'wins,',pa[5][4], 'pushes,',pa[5][5],'losses and',pa[5][6],'surrenders out of',pa[5][2],'hands.'

else:

	for i in range(showlearning):
# learning from random autoplay
#							  set6
		pa[3]=[    1,         10000,        2,          False,           8,            56]
		pa[5]=[pa[3][1]*pa[3][2],   0,    0,   0,    0,     0,      0] 
		
		[pa,table1,table2]=main(pa,table1,table2)

# autoplay utilizing learnt strategy as a check of progress.
#							  set7
		pa[3]=[    2,         10000,        2,          False,           8,            56]
		pa[5]=[pa[3][1]*pa[3][2], 0, 0, 0, 0, 0, 0]
		
		pa=readmain(pa)
		
		pa.pop()
		table1=tablefix(table1)
		table2=tablefix(table2)
		
		print i+1, pa[5][0]/(pa[3][1]*pa[3][2])   # final asset/initial asset
		
		if False:
		
			f=open('learning.txt','a')
			ww = str(pa[5][0]/(pa[3][1]*pa[3][2]))+'\n'
			f.write(ww)
			f.close()

	if False:		# whether to write to a file.
		
			f=open('table1.txt','w')
			f.write(json.dumps(table1))
			f.close()
			
			f=open('table2.txt','w')
			f.write(json.dumps(table2))
			f.close()