// Script to convert eua_tagged_files.csv to JSON
const fs = require('fs');

// Function to parse CSV line considering commas within quotes
function parseCSVLine(line) {
    const result = [];
    let current = '';
    let inQuotes = false;
    
    for (let i = 0; i < line.length; i++) {
        const char = line[i];
        
        if (char === '"') {
            inQuotes = !inQuotes;
        } else if (char === ',' && !inQuotes) {
            result.push(current.trim());
            current = '';
        } else {
            current += char;
        }
    }
    
    // Don't forget the last field
    result.push(current.trim());
    
    return result;
}

// Read the CSV file
const csvContent = fs.readFileSync('eua_tagged_files.csv', 'utf8');
const lines = csvContent.trim().split('\n');

// Parse header
const headers = parseCSVLine(lines[0]);

// Parse data rows
const documents = [];

for (let i = 1; i < lines.length; i++) {
    const values = parseCSVLine(lines[i]);
    
    if (values.length === headers.length) {
        const doc = {
            filename: values[0],
            title: values[1],
            date: values[2],
            googleDriveLink: values[3],
            folder: values[4],
            fileType: values[5],
            pageCount: parseInt(values[6]) || 0,
            module: values[7],
            documentType: values[8],
            peopleMentioned: values[9] ? values[9].split(',').map(p => p.trim()).filter(p => p) : [],
            tags: values[10] ? values[10].split(',').map(t => t.trim()).filter(t => t) : [],
            hasExemption: values[11] === 'True',
            hasExclusion: values[12] === 'True',
            passwordProtected: values[13] === 'True',
            processed: values[14] === 'True'
        };
        
        documents.push(doc);
    }
}

// Create output structure
const output = {
    documents: documents,
    metadata: {
        totalDocuments: documents.length,
        lastUpdated: new Date().toISOString().split('T')[0],
        sourceFile: 'eua_tagged_files.csv',
        columns: headers,
        statistics: {
            byModule: {},
            byFileType: {},
            byDocumentType: {},
            withExemptions: documents.filter(d => d.hasExemption).length,
            withExclusions: documents.filter(d => d.hasExclusion).length,
            passwordProtected: documents.filter(d => d.passwordProtected).length,
            processed: documents.filter(d => d.processed).length
        }
    }
};

// Calculate statistics
documents.forEach(doc => {
    // By module
    output.metadata.statistics.byModule[doc.module] = 
        (output.metadata.statistics.byModule[doc.module] || 0) + 1;
    
    // By file type
    output.metadata.statistics.byFileType[doc.fileType] = 
        (output.metadata.statistics.byFileType[doc.fileType] || 0) + 1;
    
    // By document type
    output.metadata.statistics.byDocumentType[doc.documentType] = 
        (output.metadata.statistics.byDocumentType[doc.documentType] || 0) + 1;
});

// Write to JSON file
fs.writeFileSync('eua-tagged-files.json', JSON.stringify(output, null, 2));

console.log('Successfully created eua-tagged-files.json');
console.log(`Total documents: ${output.metadata.totalDocuments}`);
console.log('\nStatistics:');
console.log(`- Documents with exemptions: ${output.metadata.statistics.withExemptions}`);
console.log(`- Documents with exclusions: ${output.metadata.statistics.withExclusions}`);
console.log(`- Password protected: ${output.metadata.statistics.passwordProtected}`);
console.log(`- Processed: ${output.metadata.statistics.processed}`);
console.log('\nBy Module:');
Object.entries(output.metadata.statistics.byModule)
    .sort((a, b) => b[1] - a[1])
    .forEach(([module, count]) => console.log(`  ${module}: ${count}`));