"""
Data visualization - mirrors {{ cookiecutter.module_name }}/visualization/plots.py
"""

using Logging

include("../config.jl")

const INPUT_PATH = joinpath(PROCESSED_DATA_DIR, "dataset.arrow")
const OUTPUT_PATH = joinpath(FIGURES_DIR, "plot.png")

@info "Generating plot from data..."

for i in 1:10
    if i == 5
        @info "Something happened for iteration 5."
    end
end

@info "Plot generation complete."
