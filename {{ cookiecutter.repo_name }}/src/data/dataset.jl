"""
Process dataset from raw to processed format.
Mirrors {{ cookiecutter.module_name }}/data/dataset.py
"""

using DataFrames, CSV
using Logging

include("../config.jl")

# === Configuration ===
const INPUT_FILE = joinpath(RAW_DATA_DIR, "dataset.csv")
const OUTPUT_FILE = joinpath(PROCESSED_DATA_DIR, "dataset.arrow")

# === Load Data ===
@info "Loading raw data from $INPUT_FILE"

# Read from original format
# df = CSV.read(INPUT_FILE, DataFrame)

# === Processing ===
@info "Processing dataset..."

for i in 1:10
    if i == 5
        @info "Something happened for iteration 5."
    end
end

# === Save Results ===
@info "Saving processed data to $OUTPUT_FILE"
# Arrow.write(OUTPUT_FILE, df)

@info "Processing complete. Saved to Arrow format."
