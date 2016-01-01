To run the program:

	1. Open the terminal and traverse to the directory containing the program modules and TSV files 

	2. Type the following command:
	
		python runHere.py \
			[population_size] \
			[crossover_rate] \
			[mutation_rate] \
			[number_of_iterations] \
			[number_of_inputs] \
			[lower_weight_boundary] \
			[upper_weight_boundary]
			
	3. The program will prompt you for the name of the function you wish to see approximated
	
	   If 'number_of_inputs' is specified as 2 select one from [xor, complex] 
	   
	   If 'number_of_inputs' is specified as 1 select one from [linear, sine, cubic, tanh]
	   
	4. The program will give you the options to evolve weights or functions.
	
	   Type 'Y' (meaning Yes) or 'N' (meaning No) in response. Note that rejecting the first option will automatically
	   
	   lead the program to run the second.
	   
					
					