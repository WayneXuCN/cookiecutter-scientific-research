"""
Build features from processed dataset.
Mirrors {{ cookiecutter.module_name }}/features/build_features.py
"""

using DataFrames, Arrow
using Logging

include("../config.jl")

function main(
    input_path::String=joinpath(PROCESSED_DATA_DIR, "dataset.arrow"),
    output_path::String=joinpath(PROCESSED_DATA_DIR, "features.arrow"),
)
    @info "Loading processed data from $input_path"
    df = DataFrame(Arrow.Table(input_path))
    @info "Input size: $(size(df))"

    # --- Feature engineering ---
    @info "Building features..."
    # Example: df.feat_mean = mean.(eachrow(df[:, numeric_cols]))

    @info "Saving features to $output_path (size=$(size(df)))"
    mkpath(dirname(output_path))
    Arrow.write(output_path, df)
    @info "Feature building complete."
end

if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
