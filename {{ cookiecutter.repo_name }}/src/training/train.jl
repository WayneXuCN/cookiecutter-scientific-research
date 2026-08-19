"""
Model training - mirrors {{ cookiecutter.module_name }}/training/train.py
"""

using Logging

include("../config.jl")

@info "Training model..."

for i in 1:10
    if i == 5
        @info "Something happened for iteration 5."
    end
end

@info "Training complete."
