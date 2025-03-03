import fitz
import os
import sys
import shutil

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
print(f"Script running in directory: {script_dir}")

# Get PDF paths from command-line arguments
pdf_paths = sys.argv[1:]
print(f"PDF paths received: {pdf_paths}")

try:
    os.makedirs("modified/pdf-to-png", exist_ok=True)
    print("Successfully created or found 'modified/pdf-to-png' directory.")

    for pdf_path in pdf_paths:
        if not os.path.exists(pdf_path):
            print(f"File not found: {pdf_path}")
            continue

        image_name = os.path.splitext(os.path.basename(pdf_path))[0]
        output_folder = os.path.join("modified/pdf-to-png", image_name)

        os.makedirs(output_folder, exist_ok=True)
        print(f"Created folder: {output_folder}")

        doc = fitz.open(pdf_path)

        for i in range(doc.page_count):
            page = doc.load_page(i)
            pix = page.get_pixmap()
            pix.save(os.path.join(output_folder, f"{i + 1}.png"))

        print(f"Images for {pdf_path} saved successfully in '{output_folder}'.")

        # Zip the folder
        zip_path = shutil.make_archive(output_folder, 'zip', output_folder)
        print(f"Folder zipped successfully at '{zip_path}'.")

        # Delete the unzipped folder
        shutil.rmtree(output_folder)
        print(f"Deleted the folder '{output_folder}' after zipping.")

except Exception as e:
    print("Error:", e)