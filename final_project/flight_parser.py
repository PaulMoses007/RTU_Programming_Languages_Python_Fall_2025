#!/usr/bin/env python3
"""
Flight Schedule Parser and Query Tool - Complete Solution (Grade 10)
Student: Thomas Aaran
Student ID: 231ADB187
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
import glob


class FlightParser:
    """Main class for flight schedule parsing and querying"""

    def __init__(self):
        self.valid_flights = []
        self.invalid_lines = []

    def validate_flight_id(self, flight_id):
        """Validate flight ID: 2-8 alphanumeric characters"""
        if not flight_id:
            return False, "missing flight ID"
        if not (2 <= len(flight_id) <= 8):
            return False, "flight ID length must be between 2 and 8 characters"
        if not flight_id.isalnum():
            return False, "flight ID must be alphanumeric"
        return True, ""

    def validate_airport_code(self, code, field_name):
        """Validate airport code: 3 uppercase letters"""
        if not code:
            return False, f"missing {field_name}"
        if len(code) != 3:
            return False, f"{field_name} must be exactly 3 characters"
        if not code.isalpha() or not code.isupper():
            return False, f"{field_name} must be 3 uppercase letters"
        return True, ""

    def validate_datetime(self, datetime_str, field_name):
        """Validate datetime format: YYYY-MM-DD HH:MM"""
        if not datetime_str:
            return False, f"missing {field_name}"
        try:
            datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
            return True, ""
        except ValueError:
            return False, f"invalid {field_name} format"

    def validate_price(self, price_str):
        """Validate price: positive float number"""
        if not price_str:
            return False, "missing price"
        try:
            price = float(price_str)
            if price <= 0:
                return False, "price must be positive"
            return True, ""
        except ValueError:
            return False, "invalid price format"

    def validate_times(self, dep_time_str, arr_time_str):
        """Validate that arrival is after departure"""
        try:
            dep_time = datetime.strptime(dep_time_str, "%Y-%m-%d %H:%M")
            arr_time = datetime.strptime(arr_time_str, "%Y-%m-%d %H:%M")
            if arr_time <= dep_time:
                return False, "arrival must be after departure"
            return True, ""
        except ValueError:
            return False, "cannot compare times due to invalid datetime"

    def parse_line(self, line, line_num):
        """Parse a single line from CSV file"""
        original_line = line.strip()

        # Skip empty lines
        if not original_line:
            return None, None

        # Handle comment lines
        if original_line.startswith("#"):
            return (
                None,
                f"Line {line_num}: {original_line} → comment line, ignored for data parsing",
            )

        # Split the line into fields
        fields = original_line.split(",")

        # Check if we have exactly 6 fields
        if len(fields) != 6:
            return None, f"Line {line_num}: {original_line} → missing required fields"

        flight_id, origin, destination, dep_time, arr_time, price = fields

        # Perform all validations
        errors = []

        # Validate flight ID
        is_valid, error_msg = self.validate_flight_id(flight_id)
        if not is_valid:
            errors.append(error_msg)

        # Validate origin
        is_valid, error_msg = self.validate_airport_code(origin, "origin code")
        if not is_valid:
            errors.append(error_msg)

        # Validate destination
        is_valid, error_msg = self.validate_airport_code(
            destination, "destination code"
        )
        if not is_valid:
            errors.append(error_msg)

        # Validate departure datetime
        is_valid, error_msg = self.validate_datetime(dep_time, "departure datetime")
        if not is_valid:
            errors.append(error_msg)

        # Validate arrival datetime
        is_valid, error_msg = self.validate_datetime(arr_time, "arrival datetime")
        if not is_valid:
            errors.append(error_msg)

        # Validate times comparison (only if both datetimes are valid)
        if (
            self.validate_datetime(dep_time, "departure datetime")[0]
            and self.validate_datetime(arr_time, "arrival datetime")[0]
        ):
            is_valid, error_msg = self.validate_times(dep_time, arr_time)
            if not is_valid:
                errors.append(error_msg)

        # Validate price
        is_valid, error_msg = self.validate_price(price)
        if not is_valid:
            errors.append(error_msg)

        if errors:
            return None, f"Line {line_num}: {original_line} → {', '.join(errors)}"
        else:
            # Create flight dictionary
            flight = {
                "flight_id": flight_id,
                "origin": origin,
                "destination": destination,
                "departure_datetime": dep_time,
                "arrival_datetime": arr_time,
                "price": float(price),
            }
            return flight, None

    def parse_csv_file(self, file_path):
        """Parse a single CSV file"""
        print(f"Parsing CSV file: {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()

            valid_count = 0
            invalid_count = 0

            for line_num, line in enumerate(lines, 1):
                flight, error = self.parse_line(line, line_num)

                if flight:
                    self.valid_flights.append(flight)
                    valid_count += 1
                elif error:
                    self.invalid_lines.append(error)
                    invalid_count += 1

            print(f"  Valid flights: {valid_count}")
            print(f"  Invalid lines: {invalid_count}")

        except Exception as e:
            print(f"Error reading file {file_path}: {e}")

    def parse_csv_folder(self, folder_path):
        """Parse all CSV files in a folder"""
        print(f"Parsing CSV files in folder: {folder_path}")

        # Find all CSV files in the folder
        csv_pattern = os.path.join(folder_path, "*.csv")
        csv_files = glob.glob(csv_pattern)

        if not csv_files:
            print("No CSV files found in the specified folder")
            return

        for csv_file in csv_files:
            self.parse_csv_file(csv_file)

        print(f"Total valid flights from all files: {len(self.valid_flights)}")
        print(f"Total invalid lines from all files: {len(self.invalid_lines)}")

    def load_json_database(self, json_path):
        """Load existing JSON database"""
        print(f"Loading JSON database: {json_path}")

        try:
            with open(json_path, "r", encoding="utf-8") as file:
                self.valid_flights = json.load(file)
            print(f"Loaded {len(self.valid_flights)} flights from JSON database")
        except Exception as e:
            print(f"Error loading JSON database: {e}")
            sys.exit(1)

    def write_output_files(self, output_json="db.json", errors_txt="errors.txt"):
        """Write valid flights to JSON and errors to text file"""

        # Write valid flights to JSON
        try:
            with open(output_json, "w", encoding="utf-8") as json_file:
                json.dump(self.valid_flights, json_file, indent=2, ensure_ascii=False)
            print(f"Valid flights written to: {output_json}")
        except Exception as e:
            print(f"Error writing JSON file: {e}")

        # Write errors to text file
        if self.invalid_lines:
            try:
                with open(errors_txt, "w", encoding="utf-8") as error_file:
                    for error_line in self.invalid_lines:
                        error_file.write(error_line + "\n")
                print(f"Errors written to: {errors_txt}")
            except Exception as e:
                print(f"Error writing errors file: {e}")

    def execute_query(self, query):
        """Execute a single query on the flight database"""
        matches = []

        for flight in self.valid_flights:
            match = True

            # Check each field in the query
            for field, value in query.items():
                if field == "flight_id":
                    if flight["flight_id"] != value:
                        match = False
                        break

                elif field in ["origin", "destination"]:
                    if flight[field] != value:
                        match = False
                        break

                elif field == "departure_datetime":
                    # Include flights with departure >= given value
                    flight_dep = datetime.strptime(
                        flight["departure_datetime"], "%Y-%m-%d %H:%M"
                    )
                    query_dep = datetime.strptime(value, "%Y-%m-%d %H:%M")
                    if flight_dep < query_dep:
                        match = False
                        break

                elif field == "arrival_datetime":
                    # Include flights with arrival <= given value
                    flight_arr = datetime.strptime(
                        flight["arrival_datetime"], "%Y-%m-%d %H:%M"
                    )
                    query_arr = datetime.strptime(value, "%Y-%m-%d %H:%M")
                    if flight_arr > query_arr:
                        match = False
                        break

                elif field == "price":
                    # Include flights with price <= given value
                    if flight["price"] > float(value):
                        match = False
                        break

            if match:
                matches.append(flight.copy())  # Copy to avoid reference issues

        return matches

    def execute_queries_from_file(self, query_file_path):
        """Execute queries from a JSON file"""
        print(f"Executing queries from: {query_file_path}")

        try:
            with open(query_file_path, "r", encoding="utf-8") as file:
                queries_data = json.load(file)

            # Handle both single query and array of queries
            if isinstance(queries_data, dict):
                queries = [queries_data]
            else:
                queries = queries_data

            results = []

            for i, query in enumerate(queries):
                print(f"  Query {i+1}: {query}")
                matches = self.execute_query(query)
                results.append({"query": query, "matches": matches})
                print(f"    Found {len(matches)} matches")

            return results

        except Exception as e:
            print(f"Error executing queries: {e}")
            return []

    def save_query_results(self, results):
        """Save query results to timestamped JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"response_231ADB187_Thomas_Aaran_Paul_Moses_{timestamp}.json"

        try:
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(results, file, indent=2, ensure_ascii=False)
            print(f"Query results saved to: {filename}")
        except Exception as e:
            print(f"Error saving query results: {e}")


def main():
    """Main function with command-line argument parsing"""
    parser = argparse.ArgumentParser(
        description="Flight Schedule Parser and Query Tool"
    )

    # Input arguments
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("-i", "--input", help="Parse a single CSV file")
    input_group.add_argument(
        "-d", "--directory", help="Parse all CSV files in a folder"
    )
    input_group.add_argument("-j", "--json", help="Load existing JSON database")

    # Output arguments
    parser.add_argument(
        "-o",
        "--output",
        help="Custom output path for valid flights JSON",
        default="db.json",
    )
    parser.add_argument("-q", "--query", help="Execute queries defined in a JSON file")

    args = parser.parse_args()

    # Create parser instance
    flight_parser = FlightParser()

    # Process input based on arguments
    if args.input:
        # Parse single CSV file
        flight_parser.parse_csv_file(args.input)
        flight_parser.write_output_files(args.output)

    elif args.directory:
        # Parse all CSV files in folder
        flight_parser.parse_csv_folder(args.directory)
        flight_parser.write_output_files(args.output)

    elif args.json:
        # Load existing JSON database
        flight_parser.load_json_database(args.json)

    # Execute queries if specified
    if args.query:
        results = flight_parser.execute_queries_from_file(args.query)
        if results:
            flight_parser.save_query_results(results)


if __name__ == "__main__":
    main()
