"""
Generate visualization from processed data.
Mirrors {{ cookiecutter.module_name }}/visualization/visualize.py
"""

using DataFrames, Arrow
using Logging

include("../config.jl")

function main(
    input_path::String=joinpath(PROCESSED_DATA_DIR, "dataset.arrow"),
    output_path::String=joinpath(FIGURES_DIR, "plot.png"),
)
    @info "Loading data from $input_path"
    df = DataFrame(Arrow.Table(input_path))
    @info "Data size: $(size(df))"

    # --- Plotting ---
    # Replace with publication-ready plotting (e.g., Plots.jl / CairoMakie).
    # Minimal placeholder: log summary and ensure output dir exists.
    @info "Columns: $(names(df))"
    for col in names(df)
        @info "  $col: $(eltype(df[!, col]))"
    end

    @info "Saving figure placeholder to $output_path"
    mkpath(dirname(output_path))
    open(output_path, "w") do io
        write(io, "# placeholder — replace with Plots.savefig\n")
    end
    @info "Figure saved to $output_path"
end

if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
