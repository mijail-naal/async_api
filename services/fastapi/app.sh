#!/bin/bash

uvicorn src.main:app --reload --host 0.0.0.0 --port 3000 --log-level debug
