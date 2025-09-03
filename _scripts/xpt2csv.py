import pandas as pd
import os
from pathlib import Path
from tqdm import tqdm
from datetime import datetime

def convert_xpt_to_csv(source_dir=".", output_dir="xpt_converted"):
    """Convert all XPT files to CSV format from subdirectories"""
    
    # Create output directory with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"{output_dir}_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Define subdirectories to search
    subdirs = ["pd-eua-production-051925", "pd-eua-production-063025"]
    
    # Find all XPT files in specified subdirectories
    xpt_files = []
    for subdir in subdirs:
        subdir_path = Path(source_dir) / subdir
        if subdir_path.exists():
            found_files = list(subdir_path.rglob("*.xpt"))
            xpt_files.extend(found_files)
            print(f"Found {len(found_files)} XPT files in {subdir}")
        else:
            print(f"Warning: Directory {subdir} not found")
    
    print(f"\nTotal XPT files found: {len(xpt_files)}")
    
    if not xpt_files:
        print("No XPT files found. Exiting.")
        return
    
    # Track conversions
    successful = 0
    failed = []
    total_size_mb = 0
    
    # Create summary report
    summary_data = []
    
    for xpt_file in tqdm(xpt_files, desc="Converting XPT files"):
        try:
            # Read XPT
            df = pd.read_sas(str(xpt_file), format='xport', encoding='latin1')
            
            # Create output path preserving folder structure
            relative_path = xpt_file.relative_to(source_dir)
            csv_path = Path(output_dir) / relative_path.with_suffix('.csv')
            csv_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save as CSV
            df.to_csv(csv_path, index=False)
            
            # Calculate sizes
            original_size_mb = xpt_file.stat().st_size / 1024 / 1024
            csv_size_mb = csv_path.stat().st_size / 1024 / 1024
            total_size_mb += original_size_mb
            
            # Create a summary file
            summary_path = csv_path.with_suffix('.summary.txt')
            with open(summary_path, 'w') as f:
                f.write(f"Original XPT file: {xpt_file.name}\n")
                f.write(f"Converted CSV: {csv_path.name}\n")
                f.write(f"Rows: {len(df)}\n")
                f.write(f"Columns: {len(df.columns)}\n")
                f.write(f"Column names: {', '.join(df.columns[:10])}")
                if len(df.columns) > 10:
                    f.write(f"... and {len(df.columns) - 10} more")
                f.write("\n")
                f.write(f"Original size: {original_size_mb:.2f} MB\n")
                f.write(f"CSV size: {csv_size_mb:.2f} MB\n")
                f.write(f"Compression ratio: {csv_size_mb/original_size_mb:.2%}\n")
            
            # Add to summary data
            summary_data.append({
                'filename': xpt_file.name,
                'folder': relative_path.parts[0],
                'rows': len(df),
                'columns': len(df.columns),
                'original_size_mb': round(original_size_mb, 2),
                'csv_size_mb': round(csv_size_mb, 2),
                'path': str(relative_path)
            })
            
            successful += 1
            
        except Exception as e:
            print(f"\nError converting {xpt_file.name}: {str(e)}")
            failed.append({
                'file': str(xpt_file),
                'error': str(e)
            })
    
    # Create master inventory
    print("\nCreating master inventory...")
    inventory_path = Path(output_dir) / "XPT_CONVERSION_INVENTORY.xlsx"
    
    if summary_data:
        summary_df = pd.DataFrame(summary_data)
        summary_df = summary_df.sort_values(['folder', 'filename'])
        
        # Create Excel writer with multiple sheets
        with pd.ExcelWriter(inventory_path, engine='openpyxl') as writer:
            # Overview sheet
            overview_df = pd.DataFrame([
                {'Metric': 'Total XPT files found', 'Value': len(xpt_files)},
                {'Metric': 'Successfully converted', 'Value': successful},
                {'Metric': 'Failed conversions', 'Value': len(failed)},
                {'Metric': 'Total original size (GB)', 'Value': f"{total_size_mb/1024:.2f}"},
                {'Metric': 'Conversion date', 'Value': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            ])
            overview_df.to_excel(writer, sheet_name='Overview', index=False)
            
            # Detailed inventory
            summary_df.to_excel(writer, sheet_name='File Inventory', index=False)
            
            # Failed conversions
            if failed:
                failed_df = pd.DataFrame(failed)
                failed_df.to_excel(writer, sheet_name='Failed Conversions', index=False)
    
    # Create a simple log file
    log_path = Path(output_dir) / "conversion_log.txt"
    with open(log_path, 'w') as f:
        f.write(f"XPT to CSV Conversion Log\n")
        f.write(f"{'='*50}\n")
        f.write(f"Conversion date: {datetime.now()}\n")
        f.write(f"Source directory: {source_dir}\n")
        f.write(f"Output directory: {output_dir}\n\n")
        f.write(f"Subdirectories searched:\n")
        for subdir in subdirs:
            f.write(f"  - {subdir}\n")
        f.write(f"\nResults:\n")
        f.write(f"  Total XPT files: {len(xpt_files)}\n")
        f.write(f"  Successful: {successful}\n")
        f.write(f"  Failed: {len(failed)}\n")
        f.write(f"  Total size: {total_size_mb:.2f} MB ({total_size_mb/1024:.2f} GB)\n")
        
        if failed:
            f.write(f"\nFailed conversions:\n")
            for fail in failed:
                f.write(f"  - {fail['file']}: {fail['error']}\n")
    
    print(f"\n{'='*50}")
    print(f"Conversion complete!")
    print(f"Successful: {successful}/{len(xpt_files)}")
    print(f"Failed: {len(failed)}")
    print(f"Total size processed: {total_size_mb/1024:.2f} GB")
    print(f"\nOutput directory: {output_dir}")
    print(f"Inventory file: {inventory_path}")

def create_xpt_inventory(source_dir="."):
    """Create an inventory of all XPT files before conversion"""
    
    subdirs = ["pd-eua-production-051925", "pd-eua-production-063025"]
    inventory = []
    
    for subdir in subdirs:
        subdir_path = Path(source_dir) / subdir
        if subdir_path.exists():
            for xpt_file in subdir_path.rglob("*.xpt"):
                inventory.append({
                    'filename': xpt_file.name,
                    'folder': subdir,
                    'path': str(xpt_file.relative_to(source_dir)),
                    'size_mb': round(xpt_file.stat().st_size / 1024 / 1024, 2)
                })
    
    if inventory:
        df = pd.DataFrame(inventory)
        df = df.sort_values(['folder', 'filename'])
        output_file = "xpt_files_inventory.xlsx"
        df.to_excel(output_file, index=False)
        print(f"Created inventory: {output_file}")
        print(f"Total files: {len(inventory)}")
        print(f"Total size: {df['size_mb'].sum():.2f} MB ({df['size_mb'].sum()/1024:.2f} GB)")
    else:
        print("No XPT files found")

if __name__ == "__main__":
    print("XPT to CSV Converter")
    print("="*50)
    
    # First, create an inventory of XPT files
    print("\nStep 1: Creating XPT inventory...")
    create_xpt_inventory()
    
    # Ask user to proceed
    response = input("\nProceed with conversion? (y/n): ")
    if response.lower() == 'y':
        convert_xpt_to_csv()
    else:
        print("Conversion cancelled.")
