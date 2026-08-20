"""
Process raw data into processed Arrow/Parquet.
Mirrors {{ cookiecutter.module_name }}/data/make_dataset.py
"""

using DataFrames, CSV, Arrow
using Logging

include("../config.jl")

function main(
    input_file::String=joinpath(RAW_DATA_DIR, "dataset.csv"),
    output_file::String=joinpath(PROCESSED_DATA_DIR, "dataset.arrow"),
)
    @info "Loading raw data from $input_file"
    df = CSV.read(input_file, DataFrame)
    @info "Loaded $(nrow(df)) rows, columns: $(names(df))"

    # --- Add cleaning / transformation here ---
    # Example: df = dropmissing(df)

    @info "Saving processed data to $output_file"
    mkpath(dirname(output_file))
    Arrow.write(output_file, df)
    @info "Saved $(nrow(df)) rows to $output_file"
end

if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
