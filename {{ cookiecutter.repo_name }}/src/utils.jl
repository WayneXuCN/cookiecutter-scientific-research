"""
Utility functions - mirrors {{ cookiecutter.module_name }}/utils/tools.py
"""
module Utils

using Logging

"""
    main(; input_path, output_path)

Perform tool operations on data.
"""
function main(; input_path=nothing, output_path=nothing)
    @info "Performing tool operations..."
    for i in 1:10
        if i == 5
            @info "Something happened for iteration 5."
        end
    end
    @info "Tool operations complete."
end

end # module
