from metrics import Results

test = Results('./input/landmarks_2_geodesic-mesa_2025-03-01_01-21-08', './saved_output', './datasets/landmarks_2.jrl')

# Generate results folder
test.compute_all_results()