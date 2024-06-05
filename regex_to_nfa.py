from os import system
class state:
    def __init__(self,name:str) -> None:
        self.name=name
        self.transision={}
        self.is_final=False
        self.transision['$']=set()
    
    def __repr__(self) -> str:
        return self.name
    
    def __str__(self) -> str:
        return self.name
    
    
    def add_transision(self,letter:str,dest_state):
        if self.transision.get(letter):
            self.transision[letter].add(dest_state)
        else:
            self.transision[letter]=set()
            self.transision[letter].add(dest_state)
        return None



class automata:
    def __init__(self) -> None:
        self.SN=0 #state name
        self.states=[]
        self.alphabet=set()
        self.starting_state=state('temp')
        return None
    
    def add_state(self) ->int:
        state_name=self.SN
        self.SN+=1
        self.states.append(state(str(state_name)))
        return state_name
    
    def add_alphabet(self,alphabet_list:list):
        self.alphabets=set(alphabet_list)
        return None
    
    def set_ending_state(self,ending_state:int):
        self.states[ending_state].is_final=True
        return None
    
    def add_transision(self,source:int,letter:str,destination:int):
        self.states[source].add_transision(letter,self.states[destination])
        return None
    
    def check_string(self,string,current_state):
        if current_state==None:
            current_state=self.starting_state
        if string=='':
            if current_state.is_final:
                return True
            else:
                for s in self._check_lambda(current_state):
                    if s.is_final:
                        return True
            return False
        current_states=self._check_lambda(current_state)
        current_states.add(current_state)
        next_states=set()
        for s in current_states:
            next_states_temp=s.transision.get(string[0])
            if next_states_temp==None:
                continue
            else:
                next_states=next_states.union(next_states_temp)
        if len(next_states)==0:
            return False
        for s in next_states:
            result=self.check_string(string[1:],s)
            if result==True:
                return True
        return False
    

    def regex_to_nfa(self,regex:str):
        string=self._infix_to_postfix(regex)
        stack=[]
        for x in string:
            if x =='*':
                state1=stack[-1]
                self.add_transision(state1[0],'$',state1[1])
                self.add_transision(state1[1],'$',state1[0])
            elif x =='|':
                head=self.add_state()
                tail=self.add_state()
                state2=stack.pop()
                state1=stack.pop()
                self.add_transision(head,'$',state1[0])
                self.add_transision(head,'$',state2[0])
                self.add_transision(state1[1],'$',tail)
                self.add_transision(state2[1],'$',tail)
                stack.append((head,tail))
            elif x ==chr(244):
                state2=stack.pop()
                state1=stack.pop()
                self.add_transision(state1[1],'$',state2[0])
                stack.append((state1[0],state2[1]))
            else:
                a=self.add_state()
                b=self.add_state()
                self.add_transision(a,x,b)
                stack.append((a,b))
        self.starting_state=self.states[stack[0][0]]
        self.states[stack[0][1]].is_final=True
        return None
        
    def _check_lambda(self,current_state:state,caller_state=None)->set:
        if caller_state==None:
            caller_state=current_state
        result=current_state.transision['$']
        for next_state in current_state.transision['$']:
            if next_state==caller_state or next_state==current_state:
                continue
            else:
                result=result.union(self._check_lambda(next_state,current_state))
        return result
    
    @staticmethod       
    def _infix_to_postfix(string:str)->str:
        result=[]
        stack=[]
        for i in range(len(string[:-1])):
            if string[i]=='(':
                stack.append('(')
                
            elif string[i]==')':
                while stack[-1] != '(':
                    result.append(stack.pop())
                stack.pop()
                
            elif string[i]=='*':
                while stack and stack[-1] == '*':
                    result.append(stack.pop())
                stack.append('*')
                
            elif string[i]=='|':
                while stack and stack[-1]!='(':
                    result.append(stack.pop())
                stack.append('|')
            else:
                result.append(string[i])
            if (string[i+1] not in {chr(238),'*','|',')'}) and (string[i] not in {'|','('}):
                while stack and (stack[-1] == '*' or stack[-1]==chr(244)):
                    result.append(stack.pop())
                stack.append(chr(244))
        while stack:
            result.append(stack.pop())
        return ''.join(result)


input()
alphabet=input()

regex=input()
regex=regex.replace('\*',chr(201))
regex=regex.replace('\|',chr(202))
regex=regex.replace('\(',chr(203))
regex=regex.replace('\)',chr(204))
regex=regex+chr(238)

my_automata=automata()
my_automata.regex_to_nfa(regex)

string=input()
string=string.replace('*',chr(201))
string=string.replace('|',chr(202))
string=string.replace('(',chr(203))
string=string.replace(')',chr(204))

if my_automata.check_string(string,None):
    print('Accepted')
else:
    print('Rejected')










#\* is chr(201)
#\| is chr(202)
#\( is chr(203)
#\) is chr(204)
#chr(244) is concat