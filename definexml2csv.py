from lxml import etree
import csv
import os
import glob
from collections import OrderedDict
from datetime import datetime

def process_define_xml_files(xml_input_directory, output_directory, csv_filename, report_filename):
    """
    Parses all Define-XML files in a directory, extracts variable and codelist metadata,
    and consolidates it into a single CSV file and a summary report.

    Args:
        xml_input_directory (str): Path to the directory containing Define-XML files.
        output_directory (str): Path to the directory where output CSV and report will be saved.
        csv_filename (str): Name of the output CSV file.
        report_filename (str): Name of the output summary report file.
    """
    print("Beginning processing of Define-XML files.")

    # Ensure output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Define the CDISC namespaces. CRITICAL: Match these exactly to your XML file headers!
    ns = {
        'odm': 'http://www.cdisc.org/ns/odm/v1.3',
        'xlink': 'http://www.w3.org/1999/xlink',
        'def': 'http://www.cdisc.org/ns/def/v2.0',
        'arm': 'http://www.cdisc.org/ns/arm/v1.0'
    }

    # Data structures for consolidation
    all_variable_rows = [] # This will hold all the OrderedDicts for CSV rows
    master_codelists = {}  # OID -> {Name, DataType, CodedValues: [...]} for quick lookup
    
    # For summary reporting
    unique_study_oids = set()
    unique_dataset_oids = set()
    unique_variable_oids = set()
    unique_codelist_oids_for_report = set() # To count unique codelists for the report
    standards_summary = {}

    # Define CSV column headers (order matters for DictWriter)
    # THIS IS THE csv_fieldnames VARIABLE DEFINITION
    csv_fieldnames = [
        "Source_File",
        "Study_OID",
        "Study_Name",
        "Study_Description",
        "Protocol_Name",
        "Define_MetadataVersion_OID",
        "Define_MetadataVersion_Name",
        "Define_Version",
        "Standard_Name",
        "Standard_Version",
        "Dataset_OID",
        "Dataset_Name",
        "Dataset_SAS_Name",
        "Dataset_Description",
        "Dataset_Purpose",
        "Dataset_Structure",
        "Dataset_Class",
        "Dataset_Source",
        "Variable_OID",
        "Variable_Name",
        "Variable_Label",
        "Variable_Data_Type",
        "Variable_Length",
        "Variable_SAS_Field_Name",
        "Variable_Origin",
        "Variable_Roles",
        "Variable_Mandatory",
        "Variable_Key_Sequence",
        "Variable_Method_OID",
        "Variable_WhereClause_OID",
        "CodeList_OID",
        "CodeList_Name",
        "CodeList_Data_Type",
        "CodeList_Coded_Values" # This will contain the semicolon-newline delimited values
    ]
    # END OF csv_fieldnames DEFINITION

    # Get a list of all XML files in the input directory
    xml_files = glob.glob(os.path.join(xml_input_directory, "*.xml"))

    # --- DEBUGGING LINES START ---
    print("\n--- Python's View of Files in Input Directory ---")
    print(f"Listing all items in '{xml_input_directory}':")
    try:
        for item in os.listdir(xml_input_directory):
            print(f"  - '{item}'") # Print with quotes to reveal leading/trailing spaces
    except FileNotFoundError:
        print(f"  Error: Directory '{xml_input_directory}' not found.")
    except Exception as e:
        print(f"  An error occurred while listing directory contents: {e}")

    print(f"Files matched by glob.glob('{os.path.join(xml_input_directory, '*.xml')}'):")
    if not xml_files:
        print("  No XML files found by glob.glob in the specified directory using the pattern.")
    else:
        for f in xml_files:
            print(f"  - '{os.path.basename(f)}'") # Print with quotes for clarity
    print("--- End Python's View ---")
    # --- DEBUGGING LINES END ---

    if not xml_files:
        print(f"No XML files found by the script in '{xml_input_directory}'. Please place your Define-XML files there or check the file pattern.")
        return

    print(f"Found {len(xml_files)} XML files in '{xml_input_directory}'. Starting metadata extraction...")

    # --- Process each XML file ---
    for xml_file_path in xml_files:
        current_file_name = os.path.basename(xml_file_path)
        print(f"\n--- Extracting metadata from: {current_file_name} ---")

        try:
            tree = etree.parse(xml_file_path)
            root = tree.getroot()
        except etree.XMLSyntaxError as e:
            print(f"Error parsing XML file '{xml_file_path}': {e}")
            continue # Skip to next file
        except Exception as e:
            print(f"An unexpected error occurred while reading '{xml_file_path}': {e}")
            continue # Skip to next file

        # Extract Study GlobalVariables
        study_oid = "N/A"
        study_name = "N/A"
        study_description = "N/A"
        protocol_name = "N/A"

        study_elem = root.find('odm:Study', namespaces=ns)
        if study_elem is not None:
            study_oid = study_elem.get("OID")
            gv_elem = study_elem.find('odm:GlobalVariables', namespaces=ns)
            if gv_elem is not None:
                study_name = gv_elem.findtext('odm:StudyName', namespaces=ns)
                study_description = gv_elem.findtext('odm:StudyDescription', namespaces=ns)
                protocol_name = gv_elem.findtext('odm:ProtocolName', namespaces=ns)
        
        if study_oid != "N/A":
            unique_study_oids.add(study_oid)

        # Process MetaDataVersion(s) (typically one in Define-XML)
        for mdv_elem in root.xpath('odm:Study/odm:MetaDataVersion', namespaces=ns):
            mdv_oid = mdv_elem.get('OID')
            mdv_name = mdv_elem.get('Name')
            define_version = mdv_elem.get('{http://www.cdisc.org/ns/def/v2.0}DefineVersion')
            standard_name = mdv_elem.get('{http://www.cdisc.org/ns/def/v2.0}StandardName')
            standard_version = mdv_elem.get('{http://www.cdisc.org/ns/def/v2.0}StandardVersion')

            # Update standards summary
            if standard_name:
                if standard_name not in standards_summary:
                    standards_summary[standard_name] = {}
                standards_summary[standard_name][standard_version] = \
                    standards_summary[standard_name].get(standard_version, 0) + 1

            # --- COLLECT ITEMDEFS (VARIABLES) FIRST for easy lookup ---
            current_file_variables = {} # OID -> {Name, DataType, Description, CodeListOID, etc.}
            for item_def_elem in mdv_elem.xpath('odm:ItemDef', namespaces=ns):
                oid = item_def_elem.get('OID')
                # Extract CodeListOID from CodeListRef child element
                codelist_ref_elem = item_def_elem.find('odm:CodeListRef', namespaces=ns)
                codelist_oid_from_ref = codelist_ref_elem.get('CodeListOID') if codelist_ref_elem is not None else None

                item_def = {
                    "OID": oid,
                    "Name": item_def_elem.get('Name'),
                    "DataType": item_def_elem.get('DataType'),
                    "Length": int(item_def_elem.get('Length')) if item_def_elem.get('Length') else None,
                    "SASFieldName": item_def_elem.get('SASFieldName'),
                    "Origin": item_def_elem.get('Origin'),
                    "CommentOID": item_def_elem.get('CommentOID'),
                    "CodeListOID": codelist_oid_from_ref, # Use the extracted codelist_oid
                    "Description": item_def_elem.findtext('odm:Description/odm:TranslatedText', namespaces=ns),
                    "Roles": [role_elem.text for role_elem in item_def_elem.xpath('def:Role', namespaces=ns)]
                }
                current_file_variables[oid] = item_def

            # --- COLLECT CODELISTS AND ADD TO MASTER LIST ---
            codelist_elements_found_by_xpath = mdv_elem.xpath('odm:CodeList', namespaces=ns)
            print(f"  DEBUG: In file '{current_file_name}', MetaDataVersion '{mdv_oid}'")
            print(f"  DEBUG:   XPath 'odm:CodeList' found {len(codelist_elements_found_by_xpath)} CodeList elements.")

            for code_list_elem in codelist_elements_found_by_xpath:
                cl_oid = code_list_elem.get('OID')
                code_list_data = {
                    "OID": cl_oid,
                    "Name": code_list_elem.get('Name'),
                    "DataType": code_list_elem.get('DataType'),
                    "CodedValues": []
                }
                for item in code_list_elem.xpath('odm:CodeListItem', namespaces=ns):
                    coded_value = item.get('CodedValue')
                    decode_elem = item.find('odm:Decode/odm:TranslatedText', namespaces=ns)
                    decode = decode_elem.text if decode_elem is not None else None
                    code_list_data["CodedValues"].append({'CodedValue': coded_value, 'Decode': decode})
                
                # Add/Update in master_codelists (deduplicates by OID)
                master_codelists[cl_oid] = code_list_data
                unique_codelist_oids_for_report.add(cl_oid) # For final report count

            # --- PROCESS ITEMGROUPDEFS (DATASETS) AND THEIR VARIABLES ---
            for item_group_def_elem in mdv_elem.xpath('odm:ItemGroupDef', namespaces=ns):
                dataset_oid = item_group_def_elem.get('OID')
                dataset_name = item_group_def_elem.get('Name')
                dataset_sas_name = item_group_def_elem.get('SASDatasetName')
                dataset_description = item_group_def_elem.findtext('odm:Description/odm:TranslatedText', namespaces=ns)
                dataset_purpose = item_group_def_elem.findtext('def:Purpose/def:TranslatedText', namespaces=ns)
                dataset_structure = item_group_def_elem.findtext('def:Structure', namespaces=ns)
                dataset_class = item_group_def_elem.findtext('def:Class', namespaces=ns)
                dataset_source = item_group_def_elem.findtext('def:Source', namespaces=ns)
                
                unique_dataset_oids.add(dataset_oid)

                item_refs = []
                for item_ref_elem in item_group_def_elem.xpath('odm:ItemRef', namespaces=ns):
                    item_refs.append({
                        "ItemOID": item_ref_elem.get('ItemOID'),
                        "OrderNumber": int(item_ref_elem.get('OrderNumber')) if item_ref_elem.get('OrderNumber') else None,
                        "Mandatory": item_ref_elem.get('Mandatory') == 'Yes',
                        "KeySequence": int(item_ref_elem.get('KeySequence')) if item_ref_elem.get('KeySequence') else None,
                        "MethodOID": item_ref_elem.get('MethodOID'),
                        "WhereClauseOID": item_ref_elem.get('WhereClauseOID')
                    })
                item_refs.sort(key=lambda x: x['OrderNumber'] if x['OrderNumber'] is not None else float('inf'))

                # Create a CSV row for each variable in this dataset
                for var_item_ref in item_refs:
                    variable_oid = var_item_ref.get("ItemOID")
                    var_details = current_file_variables.get(variable_oid, {}) # Get full details from collected variables
                    
                    if not var_details:
                        print(f"Warning: ItemRef '{variable_oid}' in dataset '{dataset_name}' has no matching ItemDef in this file. Skipping variable row.")
                        continue

                    unique_variable_oids.add(variable_oid)

                    # Populate codelist fields for this variable's row
                    codelist_oid = var_details.get("CodeListOID", None)
                    codelist_name = ""
                    codelist_data_type = ""
                    codelist_coded_values_str = ""

                    if codelist_oid and codelist_oid in master_codelists:
                        codelist_info = master_codelists[codelist_oid] # Get from the master list
                        codelist_name = codelist_info.get("Name", "")
                        codelist_data_type = codelist_info.get("DataType", "")
                        
                        coded_value_pairs = []
                        for cv in codelist_info.get("CodedValues", []):
                            coded_value_pairs.append(f"{cv.get('CodedValue', '')}: {cv.get('Decode', '')}")
                        codelist_coded_values_str = ";\n".join(coded_value_pairs) # Semicolon + newline delimiter


                    row = OrderedDict([
                        ("Source_File", current_file_name),
                        ("Study_OID", study_oid),
                        ("Study_Name", study_name),
                        ("Study_Description", study_description),
                        ("Protocol_Name", protocol_name),
                        ("Define_MetadataVersion_OID", mdv_oid),
                        ("Define_MetadataVersion_Name", mdv_name),
                        ("Define_Version", define_version),
                        ("Standard_Name", standard_name),
                        ("Standard_Version", standard_version),
                        ("Dataset_OID", dataset_oid),
                        ("Dataset_Name", dataset_name),
                        ("Dataset_SAS_Name", dataset_sas_name),
                        ("Dataset_Description", dataset_description),
                        ("Dataset_Purpose", dataset_purpose),
                        ("Dataset_Structure", dataset_structure),
                        ("Dataset_Class", dataset_class),
                        ("Dataset_Source", dataset_source),
                        ("Variable_OID", variable_oid),
                        ("Variable_Name", var_details.get("Name", "N/A")),
                        ("Variable_Label", var_details.get("Description", "")),
                        ("Variable_Data_Type", var_details.get("DataType", "N/A")),
                        ("Variable_Length", var_details.get("Length", None)),
                        ("Variable_SAS_Field_Name", var_details.get("SASFieldName", "")),
                        ("Variable_Origin", var_details.get("Origin", "")),
                        ("Variable_Roles", ", ".join(var_details.get("Roles", []))),
                        ("Variable_Mandatory", var_item_ref.get("Mandatory", False)),
                        ("Variable_Key_Sequence", var_item_ref.get("KeySequence", None)),
                        ("Variable_Method_OID", var_item_ref.get("MethodOID", None)),
                        ("Variable_WhereClause_OID", var_item_ref.get("WhereClauseOID", None)),
                        ("CodeList_OID", codelist_oid),
                        ("CodeList_Name", codelist_name),
                        ("CodeList_Data_Type", codelist_data_type),
                        ("CodeList_Coded_Values", codelist_coded_values_str)
                    ])
                    all_variable_rows.append(row)

    # --- Write the single CSV File ---
    output_csv_path = os.path.join(output_directory, csv_filename)
    try:
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_fieldnames, quoting=csv.QUOTE_MINIMAL)
            writer.writeheader()
            writer.writerows(all_variable_rows)
        print(f"\nSuccessfully wrote consolidated variables CSV to: {output_csv_path}")
    except IOError as e:
        print(f"Error writing CSV file {output_csv_path}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during CSV write: {e}")

    # --- Generate Summary Report ---
    output_report_path = os.path.join(output_directory, report_filename)
    report_content = [
        f"--- Metadata Consolidation Report ---",
        f"Generated On: {datetime.now().isoformat(timespec='seconds')}",
        f"Source XML Directory: {xml_input_directory}",
        f"Total Define-XML Files Processed: {len(xml_files)}",
        f"Total Unique Studies Found: {len(unique_study_oids)}",
        f"Total Unique Datasets Found: {len(unique_dataset_oids)}",
        f"Total Unique Variables Found: {len(unique_variable_oids)}",
        f"Total Unique Codelists Found: {len(unique_codelist_oids_for_report)}",
        f"\nStandards Summary (Standard Name: Version: Count):"
    ]
    for std_name, versions in standards_summary.items():
        for version, count in versions.items():
            report_content.append(f"  - {std_name}: {version} ({count} occurrences)")
    
    try:
        with open(output_report_path, 'w', encoding='utf-8') as f:
            for line in report_content:
                f.write(line + '\n')
        print(f"Successfully wrote summary report to: {output_report_path}")
    except IOError as e:
        print(f"Error writing report file {output_report_path}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during report write: {e}")


# --- Main execution ---
if __name__ == "__main__":
    # --- CONFIGURATION ---
    # !!! IMPORTANT: SET THESE PATHS TO YOUR ACTUAL DIRECTORIES !!!
    # This script will look for XML files directly in the folder where you run it from.
    xml_input_directory = "."
    
    # The folder where the output CSV and report will be saved.
    # This will NOT overwrite previous 'output_metadata_json' contents.
    output_directory = "define_output_csv" # Updated directory name
    
    # Name of the output CSV file
    csv_output_filename = "all_variables_report.csv"
    # Name of the output summary report file
    text_report_filename = "summary_report.txt"
    # --- END CONFIGURATION ---

    # Run the main processing function
    process_define_xml_files(xml_input_directory, output_directory, csv_output_filename, text_report_filename)