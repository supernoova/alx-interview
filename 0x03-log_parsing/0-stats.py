#!/usr/bin/python3

"""Script that reads stdin line by line and computes metrics"""

import sys
from typing import Dict
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class MetricsProcessor:
    """Handles the processing of log lines and computation of metrics."""

    def __init__(self):
        """Initialize metrics tracking dictionaries and counters."""
        self.status_codes = {
            "200": 0, "301": 0, "400": 0, "401": 0,
            "403": 0, "404": 0, "405": 0, "500": 0
        }
        self.total_size = 0
        self.line_count = 0
        self.print_interval = 10

    def print_statistics(self) -> None:
        """Print the current statistics for file size and status codes."""
        print(f"File size: {self.total_size}")
        for code in sorted(self.status_codes.keys()):
            if self.status_codes[code] > 0:
                print(f"{code}: {self.status_codes[code]}")

    def process_line(self, line: str) -> None:
        """
        Process a single line of log input.

        Args:
            line: A string containing the log line to process
        """
        try:
            parts = line.split()
            if len(parts) < 2:
                return

            # Update file size
            try:
                self.total_size += int(parts[-1])
            except (ValueError, IndexError):
                logging.warning(f"Invalid file size in line: {line.strip()}")

            # Update status code count
            try:
                status_code = parts[-2]
                if status_code in self.status_codes:
                    self.status_codes[status_code] += 1
            except IndexError:
                logging.warning(f"Invalid status code in line: {line.strip()}")

        except Exception as e:
            logging.error(f"Error processing line: {e}")

    def process_input(self) -> None:
        """Process input from stdin and print statistics"""
        try:
            for line in sys.stdin:
                self.line_count += 1
                self.process_line(line)

                # Print statistics every 10 lines
                if self.line_count % self.print_interval == 0:
                    self.print_statistics()

            # Print final statistics
            self.print_statistics()

        except KeyboardInterrupt:
            logging.info("Processing interrupted by user")
            self.print_statistics()
            raise


def main():
    """Main entry point for the script."""
    try:
        processor = MetricsProcessor()
        processor.process_input()
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
