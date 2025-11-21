const margin = ({top: 30, right: 50, bottom: 30, left: 50})
const width = document.querySelector('#my_dataviz').offsetWidth - margin.left - margin.right;
const height = window.innerHeight - margin.top - margin.bottom;

const svg = d3.select("#my_dataviz")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
        `translate(${margin.left},${margin.top})`);

const brushHeight = 50;
const label = d => d.name
const colors = d3.interpolateCool
const deselectedColor = "#ddd"

// D3 code
function parallelCoordinatesChart(data) {
    const keys = Object.keys(data.slice(1, 2)[0])
    keys.pop() // Drop the last column which is the name
    const keyz = keys[1]

    const x = new Map(Array.from(keys, key => [key, d3.scaleLinear(d3.extent(data, d => d[key]), [margin.left, width - margin.right])]))
    const y = d3.scalePoint(keys, [margin.top, height - margin.bottom])
    const z = d3.scaleSequential(x.get(keyz).domain().reverse(), colors)

    const line = d3.line()
        .defined(([, value]) => value != null)
        .x(([key, value]) => x.get(key)(value))
        .y(([key]) => y(key))

    const brush = d3.brushX()
        .extent([
            [margin.left, -(brushHeight / 2)],
            [width - margin.right, brushHeight / 2]
        ])
        .on("start brush end", brushed);

    const path = svg.append("g")
        .attr("fill", "none")
        .attr("stroke-width", 1.5)
        .attr("stroke-opacity", 0.4)
        .selectAll("path")
        .data(data.slice().sort((a, b) => d3.ascending(a[keyz], b[keyz])))
        .join("path")
        .attr("stroke", d => z(d[keyz]))
        .attr("d", d => line(d3.cross(keys, [d], (key, d) => [key, d[key]])));

    path.append("title")
        .text(label);

    svg.append("g")
        .selectAll("g")
        .data(keys)
        .join("g")
        .attr("transform", d => `translate(0,${y(d)})`)
        .each(function (d) {
            d3.select(this).call(d3.axisBottom(x.get(d)));
        })
        .call(g => g.append("text")
            .attr("x", margin.left)
            .attr("y", -6)
            .attr("text-anchor", "start")
            .attr("fill", "currentColor")
            .text(d => d))
        .call(g => g.selectAll("text")
            .clone(true).lower()
            .attr("fill", "none")
            .attr("stroke-width", 5)
            .attr("stroke-linejoin", "round")
            .attr("stroke", "white"))
        .call(brush);

    const selections = new Map();

    function brushed({selection}, key) {
        if (selection === null) selections.delete(key);
        else selections.set(key, selection.map(x.get(key).invert));
        const selected = [];
        path.each(function (d) {
            const active = Array.from(selections).every(([key, [min, max]]) => d[key] >= min && d[key] <= max);
            d3.select(this).style("stroke", active ? z(d[keyz]) : deselectedColor);
            if (active) {
                d3.select(this).raise();
                selected.push(d);
            }
        });
        svg.property("value", selected).dispatch("input");
    }

    return svg.property("value", data).node();
}

// D3 code

dataiku.fetch('cars', function (dataFrame) {
    var columnNames = dataFrame.getColumnNames();

    function formatData(row) {
        var out = {};
        columnNames.forEach(function (col) {
            out[col] = col === 'name' ? row[col] : +row[col];
        });
        return out;
    }

    var cars = dataFrame.mapRecords(formatData);
    parallelCoordinatesChart(cars);
});