"""01 - Process raw data into Arrow (exploratory, linear Julia script)."""

using DataFrames, CSV, Arrow
using Logging

include("../src/config.jl")

const INPUT_PATH = joinpath(RAW_DATA_DIR, "dataset.csv")
const OUTPUT_PATH = joinpath(PROCESSED_DATA_DIR, "dataset.arrow")

@info "Loading raw data from $INPUT_PATH"

if !isfile(INPUT_PATH)
    @warn "$INPUT_PATH not found, creating dummy data"
    mkpath(dirname(INPUT_PATH))
    df_dummy = DataFrame(x=0:99, y=[i^2 for i in 0:99])
    CSV.write(INPUT_PATH, df_dummy)
end

df = CSV.read(INPUT_PATH, DataFrame)
@info "Loaded $(nrow(df)) rows"

# --- Edit here: cleaning / filtering ---
# df = dropmissing(df)

@info "Saving to $OUTPUT_PATH"
mkpath(dirname(OUTPUT_PATH))
Arrow.write(OUTPUT_PATH, df)
@info "Done. Saved $(nrow(df)) rows to $OUTPUT_PATH"
