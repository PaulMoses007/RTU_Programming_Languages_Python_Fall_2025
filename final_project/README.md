# Flight Schedule Parser - Final Assignment

**Student**: Thomas Aaran Paul Moses
**Student ID**: 231ADB187
**Course**: Programming Languages - Python, RTU Fall 2025

## Project Overview
A comprehensive Python application that parses flight schedule CSV files, validates data, exports results, and executes queries on flight databases.

## Project Structure
final_project/
├── flight_parser.py
├── README.md
└── data/
├── db.csv
├── query.json
└── sample_flights/
├── flights1.csv
└── flights2.csv

## Features Implemented
- CSV parsing with validation
- Error reporting to errors.txt
- JSON database export
- Command-line interface
- Folder parsing
- JSON database loading
- Query execution
- DateTime filtering
- Response files with timestamp

## Usage Examples
```bash
python flight_parser.py -i data/db.csv
python flight_parser.py -d data/sample_flights/
python flight_parser.py -i data/db.csv -q data/query.json
python flight_parser.py -j db.json -q data/query.json


python flight_parser.py -i data/db.csv
python flight_parser.py -d data/sample_flights/
python flight_parser.py -i data/db.csv -q data/query.json