using Logging

# Paths - mirrors {{ cookiecutter.module_name }}/config.py
const PROJ_ROOT = abspath(joinpath(@__DIR__, ".."))

const DATA_DIR = joinpath(PROJ_ROOT, "data")
const RAW_DATA_DIR = joinpath(DATA_DIR, "raw")
const INTERIM_DATA_DIR = joinpath(DATA_DIR, "interim")
const PROCESSED_DATA_DIR = joinpath(DATA_DIR, "processed")
const EXTERNAL_DATA_DIR = joinpath(DATA_DIR, "external")

const MODELS_DIR = joinpath(PROJ_ROOT, "models")

const REPORTS_DIR = joinpath(PROJ_ROOT, "reports")
const LOGS_DIR = joinpath(REPORTS_DIR, "logs")
const FIGURES_DIR = joinpath(REPORTS_DIR, "figures")

# Ensure directories exist
for dir in [DATA_DIR, RAW_DATA_DIR, INTERIM_DATA_DIR, PROCESSED_DATA_DIR, EXTERNAL_DATA_DIR, MODELS_DIR, REPORTS_DIR, LOGS_DIR, FIGURES_DIR]
    mkpath(dir)
end
