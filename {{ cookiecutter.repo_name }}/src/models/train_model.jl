"""
Train and persist a model from feature table.
Mirrors {{ cookiecutter.module_name }}/models/train_model.py
"""

using DataFrames, Arrow
using Logging
using Serialization

include("../config.jl")

function main(
    features_path::String=joinpath(PROCESSED_DATA_DIR, "features.arrow"),
    model_path::String=joinpath(MODELS_DIR, "model.jls"),
)
    @info "Loading features from $features_path"
    df = DataFrame(Arrow.Table(features_path))
    @info "Features size: $(size(df))"

    # --- Training ---
    # Replace with MLJ.jl / Flux.jl training logic.
    @info "Training model (placeholder)..."
    model = Dict("n_features" => ncol(df), "n_rows" => nrow(df))

    @info "Saving model to $model_path"
    mkpath(dirname(model_path))
    open(model_path, "w") do io
        serialize(io, model)
    end
    @info "Model saved to $model_path"
end

if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
