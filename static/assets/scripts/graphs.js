
google.charts.load('current', {'packages':['corechart']});
google.charts.load('current', {'packages':['treemap']});
google.charts.setOnLoadCallback(createCharts);

// window.addEventListener("load", createCharts)

function createCharts(){
    distribucionesChart()
    edadesChart()
    teacherChart()
    stemChart()
}

function distribucionesChart() {

    var data = google.visualization.arrayToDataTable([
        ['Género', 'Número de Jugadores'],
        ['Niños',     26490],
        ['Niñas',      34892]
    ]);

    var options = {
        // title: 'Distribución de Jugadores por género',
        backgroundColor: 'transparent',
        colors: ["#3AFFFF", "#FF43C0"],
        legend: {position:'right', aligned:'center', textStyle: {color: 'white'}}
    };

    var chart = new google.visualization.PieChart(document.getElementById('genderDistribution'));

    chart.draw(data, options);
}

function edadesChart(){
    var data = google.visualization.arrayToDataTable([
        ["Edad", "Jugadores", { role: "style" } ],
        ["6", 13844, "#FF43C0"],
        ["7", 18393, "#3AFFFF"],
        ["8", 13939, "#FF43C0"],
        ["9", 12930, "#3AFFFF"],
        ["10", 10930, "#FF43C0"],
        ["11", 9236, "#3AFFFF"],
        ["12", 7256, "#FF43C0"],
        ["13", 2564, "#3AFFFF"]
    ]);

    // var view = new google.visualization.DataView(data);
    // view.setColumns([0, 1,
    //     { calc: "stringify",
    //         sourceColumn: 1,
    //         type: "string",
    //         role: "annotation" },
    //     2]);

    var options = {
        bar: {groupWidth: "95%"},
        legend: "none",
        backgroundColor: 'transparent',
        hAxis: {
            textStyle: {
                color: "#FFFFFF"
            },
            gridlines: {
                color: "#FFFFFF"
            },
            baselineColor: '#FFFFFF'
        },
        vAxis: {
            textStyle: {
                color: "#FFFFFF"
            },
            gridlines: {
                color: "#FFFFFF"
            },
            baselineColor: '#FFFFFF'
        }
    };
    let chart = new google.visualization.ColumnChart(document.getElementById("playersAge"));
    chart.draw(data, options);
}

function teacherChart(){
    // var data = google.visualization.arrayToDataTable([
    //     ["Edad", "Jugadores", { role: "style" } ],
    //     ["25-30" , 13844, "#b87333"],
    //     ["30-35", 18393, "silver"],
    //     ["35-40", 13939, "gold"],
    //     ["40-45", 12930, "color: #e5e4e2"],
    //     ["45-50", 10930, "color: #e5e4e2"],
    //     ["50-55", 9236, "color: #e5e4e2"],
    //     ["55-60", 7256, "color: #e5e4e2"],
    //     ["60-65", 2564, "color: #e5e4e2"]
    // ]);

    let data = google.visualization.arrayToDataTable([
        ["Edad", "Jugadores"],
        ["25-30" , 13844],
        ["30-35", 18393],
        ["35-40", 13939],
        ["40-45", 12930],
        ["45-50", 10930],
        ["50-55", 9236],
        ["55-60", 7256],
        ["60-65", 2564]
    ]);

    // var view = new google.visualization.DataView(data);
    // view.setColumns([0, 1,
    //     { calc: "stringify",
    //         sourceColumn: 1,
    //         type: "string",
    //         role: "annotation" },
    //     2]);

    var options = {
        legend: "none",
        backgroundColor: 'transparent',
        hAxis: {
            textStyle: {
                color: "#FFFFFF"
            },
            gridlines: {
                color: "#FFFFFF"
            },
            baselineColor: '#FFFFFF'
        },
        vAxis: {
            textStyle: {
                color: "#FFFFFF"
            },
            gridlines: {
                color: "#FFFFFF"
            },
            baselineColor: '#FFFFFF'
        },
        colors: ["#FF43C0"]
    };
    var chart = new google.visualization.LineChart(document.getElementById("ageSuccess"));
    chart.draw(data, options);
}

function stemChart(){
    var data = google.visualization.arrayToDataTable([
        ['Area','Parent', 'Número de Jugadores'],
        ['Area',    null,   83983],
        ['Ciencias',    'Area',   26490],
        ['Tecnología',   'Area',    34892],
        ['Ingeniería',   'Area',   34892],
        ['Matemáticas',  'Area',    34892]
    ]);

    var options = {
        // title: 'Distribución de Jugadores por género',
        backgroundColor: 'transparent',
        colors: ["#3AFFFF", "#FF43C0"],
        legend: {position:'right', aligned:'center', textStyle: {color: 'white'}}
    };

    var chart = new google.visualization.TreeMap(document.getElementById('areaPreference'));
    chart.draw(data, options);
}

