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
        self.dfa=[]
        self.alphabet=set()
        for x in states_list:
            self.states[x]=state(x)
        self.starting_state=self.states[states_list[0]]
        return None
    
    def add_alphabet(self,alphabet_list:list):
        for x in alphabet_list:
            self.alphabet.add(x)
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
    
    
    def to_dfa_count(self,lambda_closure):
        if lambda_closure==-1:
            lambda_closure=self._check_lambda(self.starting_state)
        if lambda_closure in self.dfa or not lambda_closure:
            return None
        self.dfa.append(lambda_closure)
        for a in self.alphabet:
            next_states=set()
            temp=set()
            for s in lambda_closure:
                
                temp=temp.union(s.transision.get(a,set()))
            for s in temp:
                next_states=next_states.union(self._check_lambda(s))
            
            self.to_dfa_count(next_states)
    
    def _check_lambda(self,current_state:state,caller_state=None)->set:
        if caller_state==None:
            caller_state=current_state
        result=current_state.transision['$'].copy()
        for next_state in current_state.transision['$'].copy():
            if next_state==caller_state or next_state==current_state:
                continue
            else:
                result=result.union(self._check_lambda(next_state,current_state))
        result.add(current_state)
        return result
            
        


 
input()
states=input().split()
my_automata=automata(states)
input()
alphabet=input().split()
my_automata.add_alphabet(alphabet)
input()
ending_states=input().split()
my_automata.set_ending_states(ending_states)


for _ in range(int(input())):
    temp=input().split(',')
    my_automata.add_transision(temp[0],temp[1],temp[2])

my_automata.to_dfa_count(-1)
print(len(my_automata.dfa)+1)