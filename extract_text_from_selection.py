#!/usr/bin/env python3
"""
Captures a screen region selected by the user using 'spectacle',
extracts text from it using 'tesseract-ocr', prints the text,
and copies it to the clipboard using 'xclip'.

Dependencies:
- spectacle: For capturing screen regions.
  (Usually pre-installed on KDE. `sudo apt install spectacle`)
- tesseract-ocr: For OCR.
  (`sudo apt install tesseract-ocr`)
- xclip: For copying text to clipboard.
  (`sudo apt install xclip`)
"""
import subprocess
import tempfile
import os
import shutil

def check_dependencies():
    """Checks if required command-line tools are installed."""
    dependencies = ["spectacle", "tesseract", "xclip"]
    missing = []
    for dep in dependencies:
        if shutil.which(dep) is None:
            missing.append(dep)
    if missing:
        print("Error: The following required tools are not installed or not in PATH:")
        for m in missing:
            print(f" - {m}")
        print("\nPlease install them to use this script.")
        if "spectacle" in missing:
            print("  For spectacle: sudo apt install spectacle (usually pre-installed on KDE)")
        if "tesseract" in missing: # tesseract-ocr package provides 'tesseract' command
            print("  For tesseract: sudo apt install tesseract-ocr")
        if "xclip" in missing:
            print("  For xclip: sudo apt install xclip")
        return False
    return True

def capture_and_extract_text():
    """
    Guides user to select a screen region, captures it, extracts text,
    prints it, and copies it to clipboard.
    """
    if not check_dependencies():
        return

    try:
        # Create a temporary file for the screenshot
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_image_file:
            tmp_image_path = tmp_image_file.name
        
        print("Please select the screen region you want to capture (it will be copied to clipboard)...")
        # Command: spectacle -b -r -n -c
        # -b: background mode (no UI shown before selection)
        # -r: region selection mode
        # -n: non-notify (disable notification after capture)
        # -c: copy to clipboard
        spectacle_cmd = ["spectacle", "-b", "-r", "-n", "-c"]
        
        # Run spectacle
        process = subprocess.Popen(spectacle_cmd)
        process.wait() # Wait for spectacle to finish (user selects region and it copies to clipboard)

        if process.returncode != 0:
            print(f"Spectacle command failed to copy to clipboard (return code {process.returncode}).")
            if os.path.exists(tmp_image_path):
                 os.remove(tmp_image_path)
            return
        
        print("Region copied to clipboard by Spectacle. Attempting to save from clipboard to temporary file...")
        
        # Save the image from clipboard to the temporary file using xclip
        try:
            with open(tmp_image_path, "wb") as f_out:
                xclip_save_cmd = ["xclip", "-selection", "clipboard", "-t", "image/png", "-o"]
                save_process = subprocess.run(xclip_save_cmd, stdout=f_out, check=True)
            print(f"Region saved from clipboard to: {tmp_image_path}")
        except FileNotFoundError:
            print("xclip command not found. Cannot save image from clipboard.")
            print("Please install xclip: sudo apt install xclip")
            if os.path.exists(tmp_image_path):
                os.remove(tmp_image_path)
            return
        except subprocess.CalledProcessError as e:
            print(f"Failed to save image from clipboard using xclip: {e}")
            if os.path.exists(tmp_image_path):
                os.remove(tmp_image_path)
            return

        if not os.path.exists(tmp_image_path) or os.path.getsize(tmp_image_path) == 0:
            print("Failed to save image from clipboard or the image is empty.")
            # No need to remove tmp_image_path here as it might not have been created or is empty
            return

        # Extract text using tesseract
        # Command: tesseract <image_path> stdout
        tesseract_cmd = ["tesseract", tmp_image_path, "stdout"]
        try:
            result = subprocess.run(tesseract_cmd, capture_output=True, text=True, check=True)
            extracted_text = result.stdout.strip()
            
            if extracted_text:
                print("\nExtracted Text:\n-------------------")
                print(extracted_text)
                print("-------------------\n")

                # Copy to clipboard using xclip
                try:
                    subprocess.run(["xclip", "-selection", "clipboard"], input=extracted_text, text=True, check=True)
                    print("Text copied to clipboard.")
                except FileNotFoundError:
                    print("xclip command not found. Text not copied to clipboard.")
                    print("Please install xclip: sudo apt install xclip")
                except subprocess.CalledProcessError as e:
                    print(f"Failed to copy to clipboard with xclip: {e}")
            else:
                print("No text could be extracted from the selected region.")

        except FileNotFoundError:
            print("tesseract command not found. Is tesseract-ocr installed?")
            print("Please install tesseract-ocr: sudo apt install tesseract-ocr")
        except subprocess.CalledProcessError as e:
            print(f"Tesseract failed to process the image: {e}")
            if e.stderr:
                print(f"Tesseract error output: {e.stderr}")
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # Clean up the temporary image file
        if 'tmp_image_path' in locals() and os.path.exists(tmp_image_path):
            try:
                os.remove(tmp_image_path)
                # print(f"Temporary file {tmp_image_path} removed.")
            except OSError as e:
                print(f"Error removing temporary file {tmp_image_path}: {e}")

if __name__ == "__main__":
    capture_and_extract_text()