"""Utility functions - mirrors {{ cookiecutter.module_name }}/utils/tools.py"""

module Utils

export ensure_dir

using Logging

"""
    ensure_dir(path)

Ensure directory exists, create if needed.
"""
function ensure_dir(path::String)
    mkpath(path)
    return path
end

end # module
