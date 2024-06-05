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
    def __init__(self,states_list:list) -> None:
        self.states={}
        self.alphabet=set()
        for x in states_list:
            self.states[x]=state(x)
        self.starting_state=self.states[states_list[0]]
        return None
    
    def add_alphabet(self,alphabet_list:list):
        self.alphabets=set(alphabet_list)
        return None
    
    def set_ending_states(self,ending_state_list:list):
        for x in ending_state_list:
            self.states[x].is_final=True
        return None
    
    def add_transision(self,source:str,letter:str,destination:str):
        self.states[source].add_transision(letter,self.states[destination])
        return None
    
    def check_string(self,string,current_state):
        if current_state==None:
            current_state=self.starting_state
        if string=='':
            for s in self._check_lambda(current_state):
                if s.is_final:
                    return True
            return False
        
        current_states=self._check_lambda(current_state)
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
    
    
    def _check_lambda(self,current_state:state,caller_state=None)->set:
        if caller_state==None:
            caller_state=current_state
        result=current_state.transision['$']
        for next_state in current_state.transision['$']:
            if next_state==caller_state or next_state==current_state:
                continue
            else:
                result=result.union(self._check_lambda(next_state,current_state))
        result.add(current_state)
        return result
            
        



#strategy:when we get to a transision that has more than one state that is going to,we make searching call for each state saperately,and OR all of thair results,probably need a recursive function for search
 
input()
states=input().split()
my_automata=automata(states)
input()
alphabet=input().split()
my_automata.add_alphabet(alphabet)
input()
ending_states=input().split()
my_automata.set_ending_states(ending_states)


#automata format:
#automata is a dictionary of state,in each state it will hold informations like if it is the final state or not

for _ in range(int(input())):
    temp=input().split(',')
    my_automata.add_transision(temp[0],temp[1],temp[2])

if my_automata.check_string(input(),None):
    print('Accepted')
else:
    print('Rejected')
    