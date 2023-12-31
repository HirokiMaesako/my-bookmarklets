javascript:(
    function(){
        function getSelectedText() {
            let selectedText = '';
        
            if (window.getSelection) {
              selectedText = window.getSelection().toString();
            }
        
            return selectedText;
        };

        function convertToMarkdownTable(csvData) {
            const lines = csvData.trim().split('\n');
            const rows = lines.map(line => line.split(',').map(cell => cell.trim()));

            const header = rows[0];
            const headerRow = `| ${header.join(' | ')} |\n`;
            const separatorRow = `| ${header.map(() => '---').join(' | ')} |\n`;
            const bodyRows = rows.slice(1).map(row => `| ${row.join(' | ')} |`).join('\n');
        
            return `${headerRow}${separatorRow}${bodyRows}`;
        };

        let inputString = getSelectedText();
        let outputString = convertToMarkdownTable(inputString);
        navigator.clipboard.writeText(outputString);
    }
)();
