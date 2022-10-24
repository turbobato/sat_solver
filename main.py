import copy

# Utility functions :
def litteral_to_variable_number(litteral):
    return abs(int(litteral))


# check if all variables have been assigned a value, returns a tuple (bool, variable)
def variable_not_assigned(variables_values):
    for var, value in variables_values.items():
        if value == -1:
            return (True, var)
    return (False, None)


# Class CNF
class CNF:
    # initialize reading a file
    def __init__(self, file):
        self.variables_values = {}
        self.variables_polarities = {}
        self.clauses = []
        with open(file) as f:
            line = f.readline()
            while line:
                line = line.split()
                # we are going to add a clause as a list of pairs (variable, polarity)
                clause = []
                for litteral in line:
                    if (
                        not litteral_to_variable_number(litteral)
                        in self.variables_values
                    ):
                        # set the value  to -1 for initialization
                        self.variables_values[
                            litteral_to_variable_number(litteral)
                        ] = -1
                    if (
                        not litteral_to_variable_number(litteral)
                        in self.variables_polarities
                    ):
                        self.variables_polarities[
                            litteral_to_variable_number(litteral)
                        ] = set()
                    if int(litteral) < 0:
                        clause.append((litteral_to_variable_number(litteral), -1))
                        self.variables_polarities[
                            litteral_to_variable_number(litteral)
                        ].add(-1)
                    else:
                        clause.append((litteral_to_variable_number(litteral), +1))
                        self.variables_polarities[
                            litteral_to_variable_number(litteral)
                        ].add(1)
                self.clauses.append(clause)
                line = f.readline()

    # returns true if there is an empty clause, in which case the formula is not satisfiable
    def exists_empty_clause(self):
        for clause in self.clauses : 
            if not(clause) : 
                return True
        return False

    # returns true if it's satisfiable, false if it's not, and a list of values that satisfies it if yes
    def naive_solving(self):
        # base case  1 : CNF is empty
        if not (self.clauses):
            return (True, self.variables_values)
        # base case 2 : all variables are assigned but CNF is not empty
        elif self.exists_empty_clause():
            return (False, None)
        # else start backtracking :
        else:
            var = variable_not_assigned(self.variables_values)[
                1
            ]  # get a variable not yet assigned
            clauses_copy = self.clauses # get a copy of the clauses before starting to simplify
            variables_values_copy = self.variables_values.copy()
            # first assign the variable to true
            self.clauses = self.assign_and_simplify(var, 1)
            if self.naive_solving()[0]:
                return self.naive_solving()
            # if it failed, assign the variable to false
            else:
                self.clauses = clauses_copy
                self.variables_values = variables_values_copy
                self.clauses = self.assign_and_simplify(var, 0)  # assign to false
                return self.naive_solving()  # try to solve
            return
    # if a clause is a unit clause, it forces the value of one variable
    # returns a tuple (bool, var, value) where bool is true if unit clause exists,
    # var is the variable in that unit clause and value the value it is forced to take
    def unit_propagation(self) :
        unit_clause = False
        for clause in self.clauses :
            if len(clause) == 1 :
                var = clause[0][0]
                polarity = clause[0][1]
                if polarity > 0 :
                    return (True, var, 1)
                else :
                    return (True, var, 0)
        return (False, None, None)

    # 
    def pure_litteral_elimination(self):
        pass

    # use unit propagation and pure litteral elimination
    def improved_solving(self) :
        pass 

    # assign var to value and  return the simplified CNF
    def assign_and_simplify(self, var, value):
        self.variables_values[var] = value
        new_clauses = []
        if value > 0:
            for clause in self.clauses: # go trough all closes
                new_clause = []
                no_new_clause = False
                for (var1, polarity) in clause: # go through all litterals
                    if var1 == var:  # if we find occurence of the variable we're setting to value
                        if polarity > 0:  # polarity = 1 so we can suppress the clause since we're setting var to True
                            no_new_clause = True
                    else :
                        new_clause.append((var1,polarity))
                if not(no_new_clause) :
                    new_clauses.append(new_clause)
        else:
            for clause in self.clauses:  # go trough all closes
                new_clause = []
                no_new_clause = False
                for (var1, polarity) in clause:  # go through all litterals
                    if var1 == var:  # if we find occurence of the variable we're setting to value
                        if polarity  < 0:  # polarity = -1 so we can suppress the clause since we're setting var to False
                            no_new_clause = True
                    else :
                        new_clause.append((var1,polarity))
                if not(no_new_clause) :
                    new_clauses.append(new_clause)
        return new_clauses


# Run tests
CNF1 = CNF("./cnf1")
CNF2 = CNF("./cnf2")
CNF4 = CNF("./cnf4")
CNF5 = CNF("./cnf5")
CNF6 = CNF("./cnf6")
CNF7 = CNF("./cnf7")
CNF8 = CNF("./cnf8")
CNF9 = CNF("./cnf9")


print(CNF1.naive_solving())
print(CNF2.naive_solving())
print(CNF4.naive_solving())
print(CNF4.naive_solving())
print(CNF6.naive_solving())
print(CNF7.naive_solving())
print(CNF8.naive_solving())
print(CNF9.naive_solving())
