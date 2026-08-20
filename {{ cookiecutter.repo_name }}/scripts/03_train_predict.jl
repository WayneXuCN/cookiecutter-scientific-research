"""03 - Train a quick model (exploratory, linear Julia script)."""

using DataFrames, Arrow
using Logging
using Serialization

include("../src/config.jl")

const FEATURES_PATH = joinpath(PROCESSED_DATA_DIR, "dataset.arrow")
const MODEL_PATH = joinpath(MODELS_DIR, "model.jls")

@info "Loading features from $FEATURES_PATH"
df = DataFrame(Arrow.Table(FEATURES_PATH))
@info "Shape: $(size(df))"

# Demo: last column as label
X = select(df, Not(names(df)[end]))
y = df[!, names(df)[end]]
@info "Training on X=$(size(X)), y=$(length(y))"

# Placeholder model (replace with MLJ.jl)
model = Dict("n_features" => ncol(X), "n_rows" => nrow(X), "trained" => true)

@info "Saving model to $MODEL_PATH"
mkpath(dirname(MODEL_PATH))
open(MODEL_PATH, "w") do io
    serialize(io, model)
end
@info "Model saved to $MODEL_PATH"
