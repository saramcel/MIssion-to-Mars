// import the data from data.js
const tableData = data;
// Reference the HTML table using d3
var tbody = d3.select("tbody");

//function to build the table
function buildTable(data) {
    // first clear the table of any old data
    tbody.html("");
    
    // make table row tags with "tr" for each data row
    data.forEach((dataRow) => {
    let row = tbody.append("tr");
    
    // add a new cell for each value
    Object.values(dataRow).forEach((val) => {
        // add table data tags
        let cell = row.append("td");
        // add table data values (as opposed to keys)
        cell.text(val);
        }
    );

    });

}

function handleClick() {
    
    // get datetime value from filter
    let date = d3.select("#datetime").property("value");
    let filteredData = tableData;
    
    // if the user entered a date before they click, then filter data
    if (date) {

        //only keep the rows where datetime value matches filter value
        filteredData = filteredData.filter(row => row.datetime === date);
    };
    // Rebuild the table using the filtered data
    // NOTE: If no date was entered, then filteredData will
    // just be the original tableData.
    buildTable(filteredData);
}

// This lets us listen for the click
d3.selectAll("#filter-btn").on("click", handleClick);

// Build the table when the page loads
buildTable(tableData);