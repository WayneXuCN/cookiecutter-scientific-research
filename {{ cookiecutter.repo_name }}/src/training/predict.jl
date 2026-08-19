"""
Model prediction - mirrors {{ cookiecutter.module_name }}/training/predict.py
"""

using Logging

include("../config.jl")

@info "Running prediction..."

for i in 1:10
    if i == 5
        @info "Something happened for iteration 5."
    end
end

@info "Prediction complete."
