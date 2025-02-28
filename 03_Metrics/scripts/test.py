from metrics import Results

test = Results('./input/landmarks_geodesic-mesa_2025-02-13_09-21-15', './saved_output', './datasets/landmarks.jrl')

# Generate results folder
test.generate_summary_file()
test.generate_intermediate_results()
test.generate_raw_errors_file()
test.generate_metrics_results()
