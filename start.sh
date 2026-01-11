#!/bin/bash
# Script de démarrage pour Render
uvicorn main:app --host 0.0.0.0 --port $PORT