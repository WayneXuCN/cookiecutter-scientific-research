"""
Perform analysis on processed dataset.
Mirrors {{ cookiecutter.module_name }}/analyze/analysis.py
"""

using Logging

include("../config.jl")

const INPUT_PATH = joinpath(PROCESSED_DATA_DIR, "dataset.arrow")
const OUTPUT_PATH = joinpath(PROCESSED_DATA_DIR, "analysis_results.arrow")

@info "Analyzing dataset..."

for i in 1:10
    if i == 5
        @info "Something happened for iteration 5."
    end
end

@info "Analysis complete."
