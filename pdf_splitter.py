#!/usr/bin/env python3
"""
PDF Splitter - Split a PDF into multiple smaller PDFs based on page ranges

Usage: python pdf_splitter.py <pdf_file> <page_numbers>
Example: python pdf_splitter.py document.pdf 1,7,20,32,45

This will create PDFs with the following page ranges:
- output_1.pdf: pages 2-7
- output_2.pdf: pages 8-20
- output_3.pdf: pages 21-32
- output_4.pdf: pages 33-45
"""

import sys
import os
import argparse
from pathlib import Path
try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    print("Error: pypdf library not found. Please install it with: pip install pypdf")
    sys.exit(1)


def parse_page_numbers(page_string):
    """Parse comma-separated page numbers into a list of integers."""
    try:
        pages = [int(p.strip()) for p in page_string.split(',')]
        return sorted(pages)
    except ValueError as e:
        raise ValueError(f"Invalid page numbers format: {e}")


def calculate_page_ranges(page_numbers):
    """Calculate page ranges based on the input page numbers."""
    ranges = []
    for i in range(len(page_numbers)):
        start_page = page_numbers[i] + 1  # Start after the current page
        if i + 1 < len(page_numbers):
            end_page = page_numbers[i + 1]  # End at the next page number (inclusive)
        else:
            # For the last range, we'll determine the end page from the PDF
            end_page = None
        ranges.append((start_page, end_page))
    return ranges


def split_pdf(input_pdf_path, page_numbers, output_dir=None):
    """Split PDF into multiple files based on page ranges."""
    # Validate input file
    if not os.path.exists(input_pdf_path):
        raise FileNotFoundError(f"PDF file not found: {input_pdf_path}")
    
    # Parse page numbers
    page_list = parse_page_numbers(page_numbers)
    if not page_list:
        raise ValueError("No valid page numbers provided")
    
    # Set output directory
    if output_dir is None:
        output_dir = os.path.dirname(input_pdf_path) or '.'
    
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Read the input PDF
    try:
        reader = PdfReader(input_pdf_path)
        total_pages = len(reader.pages)
        print(f"Input PDF has {total_pages} pages")
    except Exception as e:
        raise Exception(f"Error reading PDF: {e}")
    
    # Calculate page ranges
    ranges = calculate_page_ranges(page_list)
    
    # Generate base filename for output
    input_filename = Path(input_pdf_path).stem
    
    created_files = []
    
    # Create each split PDF
    for i, (start_page, end_page) in enumerate(ranges, 1):
        # Determine actual end page
        if end_page is None:
            actual_end_page = total_pages
        else:
            actual_end_page = min(end_page, total_pages)
        
        # Skip if start page is beyond total pages
        if start_page > total_pages:
            print(f"Warning: Start page {start_page} is beyond total pages ({total_pages}). Skipping range {i}.")
            continue
        
        # Skip if start page is greater than end page
        if start_page > actual_end_page:
            print(f"Warning: Invalid range {start_page}-{actual_end_page}. Skipping range {i}.")
            continue
        
        # Create new PDF writer
        writer = PdfWriter()
        
        # Add pages to the writer (convert to 0-based indexing)
        pages_added = 0
        for page_num in range(start_page - 1, actual_end_page):
            if page_num < total_pages:
                writer.add_page(reader.pages[page_num])
                pages_added += 1
        
        if pages_added == 0:
            print(f"Warning: No pages to add for range {i}. Skipping.")
            continue
        
        # Generate output filename
        output_filename = f"{input_filename}_part_{i}_pages_{start_page}-{actual_end_page}.pdf"
        output_path = os.path.join(output_dir, output_filename)
        
        # Write the output PDF
        try:
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            print(f"Created: {output_filename} (pages {start_page}-{actual_end_page}, {pages_added} pages)")
            created_files.append(output_path)
        except Exception as e:
            print(f"Error creating {output_filename}: {e}")
    
    return created_files


def main():
    parser = argparse.ArgumentParser(
        description="Split a PDF into multiple smaller PDFs based on page ranges",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pdf_splitter.py document.pdf 1,7,20,32,45
  python pdf_splitter.py /path/to/file.pdf 5,10,15 --output-dir ./splits
  
Page ranges explanation:
  If you provide pages 1,7,20,32,45, the program will create:
  - Part 1: pages 2-7
  - Part 2: pages 8-20
  - Part 3: pages 21-32
  - Part 4: pages 33-45
        """
    )
    
    parser.add_argument('pdf_file', help='Path to the input PDF file')
    parser.add_argument('page_numbers', help='Comma-separated list of page numbers (e.g., 1,7,20,32,45)')
    parser.add_argument('--output-dir', '-o', help='Output directory for split PDFs (default: same as input file)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    
    try:
        created_files = split_pdf(args.pdf_file, args.page_numbers, args.output_dir)
        
        print(f"\nSuccessfully created {len(created_files)} PDF files:")
        for file_path in created_files:
            print(f"  - {os.path.basename(file_path)}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()