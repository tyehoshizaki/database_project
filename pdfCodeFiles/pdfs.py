from PyPDF2 import PdfReader # type: ignore
import os

def read_pdf(file_path):
    """Read and extract text from a PDF file."""
    try:
        reader = PdfReader(file_path)
        print(f"✅ Successfully opened: {file_path}")
        print(f"📄 Number of pages: {len(reader.pages)}")
        
        # Extract text from all pages
        full_text = ""
        for page_num, page in enumerate(reader.pages):
            page_text = page.extract_text()
            full_text += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
            print(f"📖 Page {page_num + 1}: {len(page_text)} characters")
        
        return full_text
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return None
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        return None

def get_pdf_info(file_path):
    """Get detailed information about a PDF file."""
    try:
        reader = PdfReader(file_path)
        
        print(f"\n📊 PDF Information for: {file_path}")
        print(f"   📄 Pages: {len(reader.pages)}")
        print(f"   🔒 Encrypted: {reader.is_encrypted}")
        
        # Metadata
        if reader.metadata:
            print(f"   📝 Metadata:")
            for key, value in reader.metadata.items():
                if value:
                    print(f"      {key}: {value}")
        
        return True
    except Exception as e:
        print(f"❌ Error getting PDF info: {e}")
        return False

def list_pdf_files():
    """List all PDF files in the current directory."""
    pdf_dir = "./PDFs"
    pdf_files = [f for f in os.listdir(pdf_dir) if f.lower().endswith('.pdf')]

    if pdf_files:
        print(f"🔍 Found {len(pdf_files)} PDF file(s):")
        for i, pdf_file in enumerate(pdf_files, 1):
            file_size = os.path.getsize(os.path.join(pdf_dir, pdf_file)) / 1024  # Size in KB
            print(f"   {i}. {pdf_file} ({file_size:.1f} KB)")
        return [os.path.join(pdf_dir, f) for f in pdf_files]
    else:
        print("📭 No PDF files found in current directory")
        return []

def main():
    print("🔧 PDF Processing Tool")
    print("=" * 40)
    
    # List PDF files in current directory
    pdf_files = list_pdf_files()
    
    if pdf_files:
        print(f"\n🎯 Processing first PDF file: {pdf_files[0]}")
        
        # Get PDF info
        print("pdf_info: " + pdf_files[0])
        get_pdf_info(pdf_files[0])
        
        # Ask user if they want to read the content
        print(f"\n📖 Would you like to extract text from '{pdf_files[0]}'?")
        print("   (This will show the text content)")
        
        # For demo purposes, let's just show the first few characters
        text = read_pdf(pdf_files[0])
        if text:
            print(f"\n📄 Text preview (first 200 characters):")
            print("-" * 50)
            print(text[:200] + "..." if len(text) > 200 else text)
            print("-" * 50)
            
            # Optionally save to file
            output_file = f"{pdf_files[0]}_extracted.txt"
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f"💾 Full text saved to: {output_file}")
            except Exception as e:
                print(f"❌ Error saving text file: {e}")
    else:
        print("\n💡 To test this script:")
        print("   1. Place a PDF file in this directory")
        print("   2. Run the script again")
        print("   3. The script will analyze and extract text from the PDF")

    print(f"\n✅ PDF processing completed!")

if __name__ == "__main__":
    main()