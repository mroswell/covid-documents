// Script to convert sectioned field definitions to flat structure
const fs = require('fs');

// Read the existing JSON file
const data = JSON.parse(fs.readFileSync('field-definitions.json', 'utf8'));

// Create flat structure
const flatDefinitions = {};

// Process each section
data.sections.forEach(section => {
    Object.entries(section.fields).forEach(([fieldName, fieldData]) => {
        flatDefinitions[fieldName] = {
            definition: fieldData.definition,
            comment: fieldData.comment || null,
            section: section.name,
            // Placeholders for future metadata
            mandatory: null,
            codeList: null,
            dataType: null,
            domain: null,
            origin: null
        };
    });
});

// Create output structure with metadata
const output = {
    fields: flatDefinitions,
    metadata: {
        totalFields: Object.keys(flatDefinitions).length,
        lastUpdated: new Date().toISOString().split('T')[0],
        version: "1.0",
        sections: [...new Set(data.sections.map(s => s.name))]
    }
};

// Write to new file
fs.writeFileSync('field-definitions-flat.json', JSON.stringify(output, null, 2));

console.log('Successfully created field-definitions-flat.json');
console.log(`Total fields: ${output.metadata.totalFields}`);
console.log(`Total sections: ${output.metadata.sections.length}`);