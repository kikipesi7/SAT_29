

T = 3 # number of teams
R = 4 # number of rounds

match_id = {}
counter = 1
for r in range (1, R + 1):
    for i in range (1, T + 1):
        for j in range (1, T + 1):
                if i != j: # i and j must be diferent teams
                     match_id [(i, j, r)] = counter
                     counter += 1 

clauses = []

# Each team plays at least one match in every round
for r in range (1, R + 1):
    for i in range (1, T + 1):
        clause = []
        for j in range (1, T + 1):
            if i != j:
                clause.append(match_id[(i, j, r)])
        clauses.append(clause)

# Each team plays at most one match in every round
for r in range (1, R + 1):
    for i in range (1, T + 1):
         for j in range (1, T + 1):
            for k in range (1, T + 1):
                if i != j and i != k:
                    clauses.append([-match_id[(i, j, r)], -match_id[(i, k, r)]])

# Matches are symmetric
for r in range (1, R + 1):
    for i in range (1, T + 1):
        for j in range (i + 1, T + 1):
            impl_ij = ([-match_id[(i, j, r)], match_id[(j, i, r)]])
            impl_ji = ([match_id[(i, j, r)], -match_id[(j, i, r)]])

            clauses.append(impl_ij)
            clauses.append(impl_ji)

#  Teams play together at most once per tournament
for i in range (1, T + 1):
    for j in range (1, T + 1):
        if i != j:
            for r1 in range (1, R + 1):
                for r2 in range (r1 + 1, R + 1):
                    round_condition = ([-match_id[(i, j, r1)], -match_id[(i, j, r2)]])
                    clauses.append(round_condition)

# Generate DIMACS file for the solver
num_variables = counter - 1
num_clauses = len(clauses)

print (f"Number of variables: {num_variables} \nNumber of variables: {num_clauses}")

with open("dimacs.cnf", "w") as dimacs_file:
    dimacs_file.write(f"p cnf {num_variables} {num_clauses}\n")
    for c in clauses:
        for d in c:
            dimacs_file.write(f"{d} ")
        dimacs_file.write("0\n")
