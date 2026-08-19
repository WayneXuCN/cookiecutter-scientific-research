"""
Cross-language data exchange example.
Mirrors {{ cookiecutter.module_name }}/data/cross_language.py
Demonstrates using Arrow/Feather for sharing data between Python and Julia.
"""

using DataFrames, Arrow
using Logging

include("../config.jl")

# === Configuration ===
const EXPORT_FILE = joinpath(INTERIM_DATA_DIR, "julia_to_python.arrow")
const IMPORT_FILE = joinpath(INTERIM_DATA_DIR, "python_to_julia.arrow")
const OUTPUT_FILE = joinpath(PROCESSED_DATA_DIR, "final_results.arrow")

# === Export to Python ===
@info "Preparing data for Python..."

df_export = DataFrame(x=0:99, y=[i^2 for i in 0:99], category=repeat(["A","B"], 50))

@info "Exporting to Arrow: $EXPORT_FILE"
Arrow.write(EXPORT_FILE, df_export)

@info "Data exported. Python can read with: pyarrow.feather.read_table('julia_to_python.arrow')"

# === Import from Python ===
if isfile(IMPORT_FILE)
    @info "Importing results from Python: $IMPORT_FILE"
    df_result = DataFrame(Arrow.Table(IMPORT_FILE))
    @info "Saving final results: $OUTPUT_FILE"
    Arrow.write(OUTPUT_FILE, df_result)
    @info "Cross-language workflow complete."
else
    @warn "Python output not found: $IMPORT_FILE"
    @info "Waiting for Python to process the data..."
end
