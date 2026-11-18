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

print(clauses)