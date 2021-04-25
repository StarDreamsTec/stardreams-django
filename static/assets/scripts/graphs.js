



// window.addEventListener("load", createCharts)



function distribucionesChart() {

    var data = google.visualization.arrayToDataTable([
        ['Género', 'Número de Jugadores'],
        ['Niño',     gender[1]],
        ['Niña',     gender[0]],
        ['Otro',     gender[2]]
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

function teacherChart(){

    let data = google.visualization.arrayToDataTable([
        ["Edad", "Jugadores"],
        ["20-30" , prof[0]],
        ["30-40", prof[1]],
        ["40-50", prof[2]],
        ["50-60", prof[3]],
        ["60+", prof[4]],
    ]);

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
        colors: ["#FF43C0"],
        lineWidth: 5,
    };
    var chart = new google.visualization.LineChart(document.getElementById("ageSuccess"));
    chart.draw(data, options);
}

function stemChart(){
    var data = google.visualization.arrayToDataTable([
        ['Area','Número de Jugadores'],
        ['Ciencias',  area[0]],
        ['Tecnología',    area[1]],
        ['Ingeniería',  area[2]],
        ['Matemáticas', area[3]]
    ]);

    var options = {
        // title: 'Distribución de Jugadores por género',
        backgroundColor: 'transparent',
        colors: ["#3AFFFF", "#FF43C0"],
        legend: {position:'right', aligned:'center', textStyle: {color: 'white'}}
    };

    var chart = new google.visualization.PieChart(document.getElementById('areaPreference'));
    chart.draw(data, options);
}

