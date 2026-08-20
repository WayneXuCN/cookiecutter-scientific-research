"""02 - Exploratory analysis (linear Julia script)."""

using DataFrames, Arrow
using Logging

include("../src/config.jl")

const INPUT_PATH = joinpath(PROCESSED_DATA_DIR, "dataset.arrow")

@info "Loading processed data from $INPUT_PATH"
df = DataFrame(Arrow.Table(INPUT_PATH))
@info "Shape: $(size(df))"
@info "Columns: $(names(df))"
@info "$(describe(df))"

# --- Quick analysis ---
numeric_cols = [n for n in names(df) if eltype(df[!, n]) <: Number]
@info "Numeric columns: $numeric_cols"
if !isempty(numeric_cols)
    col = numeric_cols[1]
    @info "Mean $col: $(mean(df[!, col]))  std: $(std(df[!, col]))"
end

# --- Quick plot placeholder ---
# Replace with Plots.jl: histogram(df[!, col])
const OUT = joinpath(FIGURES_DIR, "02_analyze_hist.png")
mkpath(dirname(OUT))
open(OUT, "w") do io
    write(io, "# placeholder — add Plots.savefig\n")
end
@info "Figure placeholder saved to $OUT"
