class state:
    def __init__(self,name:str) -> None:
        self.name=name
        self.transision={}
        self.is_final=False
    
    def __repr__(self) -> str:
        return self.name
    
    def __str__(self) -> str:
        return self.name
    
    
    def add_transision(self,letter:str,dest_state):
        self.transision[letter]=dest_state
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
    
    
    def minimize_dfa(self,state_count):
        inaccessible_count=self._check_accessible()
        marked_pairs={}
        for i in self.states:
            for j in self.states:
                if marked_pairs.get((i,j))==None and marked_pairs.get((j,i))==None and i!=j:
                    if self.states[i].is_final != self.states[j].is_final:
                        marked_pairs[(i,j)]=True
                    else:
                        marked_pairs[(i,j)]=False
        change=True
        while change:
            change=False
            for pair in marked_pairs.copy():
                for x in self.alphabet:
                    transision1=self.states[pair[0]].transision[x].name
                    transision2=self.states[pair[1]].transision[x].name
                    if (marked_pairs.get((transision1,transision2)) or marked_pairs.get((transision2,transision1))) and not marked_pairs[pair]:
                        marked_pairs[pair]=True
                        change=True
        unmarked_states=[]
        for pair in marked_pairs.copy():
            if not marked_pairs[pair]:
                unmarked_states.append(set(pair))
        change=True
        temp=[]
        while change:
            temp=[]
            change=False
            for x in unmarked_states:
                current_set=x
                for y in unmarked_states:
                    if x==y:
                        continue
                    elif current_set.intersection(y):
                        change=True
                        current_set.update(y)
                if current_set not in temp:
                    temp.append(current_set)
            unmarked_states=temp
        new_state_count=state_count+len(unmarked_states)-inaccessible_count
        for x in unmarked_states:
            new_state_count-=len(x)
        return new_state_count
                
            
    
    
    def _check_accessible(self):
        visited={}
        inaccessible_count=0
        for x in self.states:
            visited[x]=False
            
        stack=[]
        stack.append(self.starting_state)
        while stack:
            current_state=stack.pop()
            visited[current_state.name]=True
            for next_state in current_state.transision.values():
                if not visited[next_state.name]:
                    stack.append(next_state)
        for x in visited:
            if not visited[x]:
                inaccessible_count+=1
                self.states.pop(x)
        return inaccessible_count
    
    
state_count=int(input())
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
    
print(my_automata.minimize_dfa(state_count))