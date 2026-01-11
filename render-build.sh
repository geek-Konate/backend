#!/bin/bash
# Script de build pour Render avec Poetry
pip install poetry
poetry config virtualenvs.create false
poetry install --no-interaction --no-ansi