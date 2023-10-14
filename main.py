import random

NUMBER_OF_VARIABLES = 8
POPULATION_SIZE = 8
MUTATION_PROB = 0.3
DOMAIN = [1, 2, 3, 4]

def random_probability_generator():
    # Generate a random floating-point value between 0 and 1
    random_value = random.uniform(0, 1)
    return random_value


def fitness_score(state):
    A, B, C, D, E, F, G, H = state[0], state[1], state[2], state[3], state[4], state[5], state[6], state[7]
    
    constraints_satisfaction = [A > G, 
                                abs(G-C)==1, 
                                D != C, 
                                G != F, 
                                abs(E-F)%2==1, 
                                A <= H, 
                                abs(H-C)%2==0, 
                                E != C, 
                                H != F, 
                                abs(F - B) == 1, 
                                H != D, 
                                E < (D - 1), 
                                C != F, 
                                G < H, 
                                D >= G, 
                                E != (H - 2), 
                                D != (F - 1)
                                ]
    
    score = sum(1 for value in constraints_satisfaction if value)

    return score 

def calculate_probability_for_selection(pop):
    ret = []
    sum_scores = sum(pop)

    for score in pop:
        ret.append(score/sum_scores)

    return ret        

def generate_distribution(parents, probs):
    dist = []
    accumulator = 0
    for i in range(len(parents)):
        # a tuple distrubution cointains:
        # start of the interval, end of the interval, the parent for this interval
        dist.append((accumulator, accumulator + probs[i], parents[i]))
        accumulator += probs[i]

    return dist

def pick_parent(dist):
    rand = random_probability_generator()

    for index, interval in enumerate(dist):
         if index == 0 and interval[0] <= rand <= interval[1]:
             return index, interval[2]
         if interval[0] < rand <= interval[1]:
             return index, interval[2]
        

def generate_parent_pairs(parents, probs, num_pairs):
    distribution = generate_distribution(parents, probs)

    count = 0
    pairings = []

    while count != num_pairs:
        parent_1 = pick_parent(distribution)[1]
        parent_2 = pick_parent(distribution)[1]

        # if parent_2 is the same as parent_1, regenerate parent_2
        while parent_1 == parent_2:
            parent_2 = pick_parent(distribution)[1]

        pairings.append((parent_1, parent_2))

        count+=1

    return pairings


def mutated_point_generator():
    # mutation can occur at any variable
    return random.randint(0, NUMBER_OF_VARIABLES-1)

def crossover_point_generator():
    # exclude index 0 because crossover at index 0 is the same thing as swapping two parents
    # crossover point means everything after this index (excluding this index) in each parent will be swapped
    return random.randint(1, NUMBER_OF_VARIABLES-1)

def mutation_value_generator():
    random_index = random.randint(0, len(DOMAIN) - 1)
    return DOMAIN[random_index]

# child is passed by reference
def mutate_child(child):
    mutation_prob = random_probability_generator()
    mutation_occur = mutation_prob <= MUTATION_PROB

    if mutation_occur:
      mutated_point = mutated_point_generator()
      mutated_value = mutation_value_generator()
      org_value = child[mutated_point]
      child[mutated_point] = mutated_value

    return (org_value, mutated_point, mutated_value) if mutation_occur else (None, None, None)
    

def generate_new_generation(parent_pairings):
      new_generation_population = []
      reproduction_details = []
      
      for pair in parent_pairings:
        parent_1 = pair[0]
        parent_2 = pair[1]

        # perform crossover
        crossover_point = crossover_point_generator()
        child_1 = parent_1[:crossover_point] + parent_2[crossover_point:]
        child_2 = parent_2[:crossover_point] + parent_1[crossover_point:]

        # mutate children
        child_1_org_value, child_1_mutated_point, child_1_mutated_value = mutate_child(child_1)
        child_2_org_value, child_2_mutated_point, child_2_mutated_value = mutate_child(child_2)
        
        reproduction_details.append((parent_1, 
                               parent_2, 
                               crossover_point,
                               child_1,
                               child_1_mutated_point,
                               child_1_org_value, 
                               child_1_mutated_value, 
                               child_2, 
                               child_2_mutated_point, 
                               child_2_org_value,
                               child_2_mutated_value))
        
        new_generation_population.append(child_1)
        new_generation_population.append(child_2)

      return reproduction_details, new_generation_population


      

def genetic_algo(num_gens, initial_population): 
    current_generation = initial_population
    reproduction_details = None
    next_generation = None
    count_gen = 0

    while count_gen != num_gens:
      print("GENERATION " + str(count_gen))

      fitness_scores = []

      for parent in current_generation:
          fitness_scores.append(fitness_score(parent))

      probs = calculate_probability_for_selection(fitness_scores)
      dist = generate_distribution(current_generation, probs)   

      report_fitness_and_probs(current_generation, fitness_scores, probs)

      if count_gen == num_gens - 1:
          return

      num_pairs = POPULATION_SIZE / 2

      pairings = generate_parent_pairs(current_generation, probs, num_pairs)

      report_selected_pairings(pairings)

      reproduction_details, next_generation = generate_new_generation(pairings)

      report_reproduction_details(reproduction_details)

      current_generation = next_generation
      count_gen += 1

# report parent pairings for this generation
def report_selected_pairings(pairings):
      print("SELECTED PAIRINGS: ")
      for pair in pairings:
          print(pair)
      print("\n")

# report fitness_score, likelihood to be selected of the current generation
def report_fitness_and_probs(current_generation, fitness_scores, probs):
      print("FITNESS SCORES, PROBABILITY TO BE SELECTED:")
      for i in range(len(current_generation)):
        print(str(current_generation[i]), end=" ")
        print("fitness score = " + str(fitness_scores[i]), end=", ")
        print("likelihood = " + str(probs[i]))
      print("\n")


# report pairings, crossover, offspring and mutation details
def report_reproduction_details(reproduction_details):  
      for index, detail in enumerate(reproduction_details):
          print("PAIR " + str(index+1))
          parent_1, parent_2, crossover_point, child_1, child_1_mutated_point, child_1_org_value, child_1_mutated_value, child_2, child_2_mutated_point, child_2_org_value, child_2_mutated_value = detail
          print("PARENT 1:", end=" ")
          print(parent_1)          
          print("PARENT 2:", end=" ")
          print(parent_2)
          
          print("CROSSOVER POINT: " + str(crossover_point))

          print("CHILD 1", end=" ")
          print(child_1)
          if child_1_org_value is None and child_1_mutated_value is None and child_1_mutated_point is None:
              print("CHILD 1 WAS NOT MUTATED")          
          else: 
              print(f"CHILD 1 WAS MUTATED FROM VALUE {child_1_org_value} TO VALUE {child_1_mutated_value} AT INDEX {child_1_mutated_point}")

          print("CHILD 2", end=" ")
          print(child_2)
          if child_2_org_value is None and child_2_mutated_value is None and child_2_mutated_point is None:
              print("CHILD 2 WAS NOT MUTATED")          
          else:           
              print(f"CHILD 2 WAS MUTATED FROM VALUE {child_2_org_value} TO VALUE {child_2_mutated_value} AT INDEX {child_2_mutated_point}")
          print("__________________________________________")
      print("\n")
      print("...........................................................................................")
  

genetic_algo(
    6, # number of generations 
    [  # intial population
        [1]*8,
        [2]*8,
        [3]*8,
        [4]*8,
        [1,2,3,4,1,2,3,4],
        [4,3,2,1,4,3,2,1],
        [1,2,1,2,1,2,1,2],
        [3,4,3,4,3,4,3,4]     
    ])
    