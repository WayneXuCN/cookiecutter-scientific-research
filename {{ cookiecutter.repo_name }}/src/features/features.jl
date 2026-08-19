"""
Feature engineering - mirrors {{ cookiecutter.module_name }}/features/features.py
"""

using DataFrames
using Logging

include("../config.jl")

@info "Creating features..."

# Example: add features to DataFrame
# df[!, :new_feature] = df.x .* 2

@info "Feature engineering complete."
