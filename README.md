# Airbyte certified python source connectors compliance tracking

## Overview
This codebase builds a streamlit application to track the compliance of Airbyte certified Python source connectors. 

## Install
```bash
poetry install
```

## Run
```bash
poetry run streamlit run certified_connectors_standards/streamlit_app.py
```

## Generating requirements.txt for Streamlit
```
poetry export --format=requirements.txt > requirements.txt
```