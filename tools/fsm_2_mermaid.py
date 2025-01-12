
import argparse
import re

class fsm_mermaid:   

    mermaid_head = "```mermaid\n"
    mermaid_format = "stateDiagram-v2\n"
    mermaid_tail = "\n```"
    
    fsm_init_pat = r"FSM_STATES_INIT\((.+?)\)"
    fsm_st_note = "FSM_ST_NONE"
    
    def __init__(self, fname="example"):
        
        # Set up argument parser
        parser = argparse.ArgumentParser(description="Create a mermaid graph from a fsm file.")
        parser.add_argument("file_name", type=str, help="The name of the C file with the fsm.")
        args = parser.parse_args()

        # Define the file name and content
        self.file_name = args.file_name

        #Count number of fsm in file
        if self.fsm_count() == 0:
            return None
        
        # Open the file in read mode 
        with open(self.file_name+".c", "r") as file:
            self.content = file.read()  # Reads all lines into a list
            
        # Iterate the number for number of fsm
        for self.fsm_new in range(0, self.fsm_total):          
            # Read and get the FSM
            self.fsm_parse()
            
            # Opens or creates the file in write mode and add content
            self.mermaid_file_write()
    
    def mermaid_file_write(self):
        with open(self.fsm_name+".md", "w") as file:
            # Head
            file.write(self.mermaid_head)
            file.write(self.mermaid_format)  
            #tail
            file.write(self.mermaid_tail)  
                
    def fsm_count(self):
        """Counts the number of fsm in file
        """
        # Initialize counter
        self.fsm_total = 0

        # Open and read the file
        with open(self.file_name+".c", "r") as file:
            for line in file:
                # Check if the pattern is found in the line
                if re.search(self.fsm_init_pat, line):
                    self.fsm_total += 1
        
        # print(f"n fsm: {self.fsm_total}")
         
        return self.fsm_total
    
    def fsm_name_get(self):
        # Get the fsm name
        match = re.findall(self.fsm_init_pat, self.content)

        if match[self.fsm_new]:
            self.fsm_name = match[self.fsm_new]
            
        # print(f"fsm name: {self.match[self.fsm_new]}")
                        
    def fsm_parse(self):  
        # Get fsm name      
        self.fsm_name_get()
        
        #Get states
        self.fsm_states_get()
        
        # parse states 
        self.fsm_states_parse()
        
        #Get transitions
        self.fsm_transitions_get()
                
    def fsm_states_get(self):
        pattern = rf"FSM_CREATE_STATE\({self.fsm_name},\s*(.+?)\)"
        
        # Get the fsm states
        match = re.findall(pattern, self.content)

        if match:
            idx = 0
            elements = match
            for line in match:
                elements[idx] = [item.strip() for item in line.split(',')]
                idx = idx + 1
            self.fsm_states = elements
            # print(f"fsm state: {elements}")
    
    def fsm_transitions_get(self):
        pattern = rf"FSM_TRANSITION_CREATE\({self.fsm_name},\s*(.+?)\)"
        
        # Get the fsm states
        match = re.findall(pattern, self.content)

        if match:
            idx = 0
            elements = match
            for line in match:
                elements[idx] = [item.strip() for item in line.split(',')]
                idx = idx + 1
            self.fsm_transitions = elements
            # print(f"fsm state: {elements}")
    
    def fsm_states_parse(self):
        self.fsm_st_root_n = []
        self.fsm_st = []
        idx = 0
        
        # Find root state
        for element in self.fsm_states:
            print(f"state: {element}")
                    
            # Find root state
            if element[1] == self.fsm_st_note:
                self.fsm_st.append(element[0])     
                self.fsm_st_root_n.append(idx)
                print(f"arr: {self.fsm_st}, idx: {self.fsm_st_root_n}")
                break
            idx = idx + 1
                
        # Get state sub-states
        self.fsm_sub_get(element[0])
    
    def fsm_sub_get(self, state, idx):
        for element in self.fsm_states:
            if element[1] == state:
                     
#------------------------------------------------------------------------------

if __name__ == "__main__":
    
    mv = fsm_mermaid()

    raise SystemExit