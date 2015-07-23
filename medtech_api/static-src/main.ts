declare var Chart;

// Create an array with n shallow copies of the given element
function repeat(elem, n) {
    var ar = new Array(n);
    for (var i = 0; i < n; i++) {
        ar[i] = elem;
    }
    return ar;
}

function prepareData(elems) {
}

interface dataPoint {
    x: number;
    y: number;
}

interface dataSet {
    label: string;
    data: dataPoint[];
    borderColor: string;
    backgroundColor: string;
    pointBorderColor: string;
    pointBackgroundColor: string;
    pointBorderWidth: number;
}

function medtech_main() {
    var canvas = <HTMLCanvasElement>document.getElementById('mychart');
    var ctx = canvas.getContext('2d');

    var scatterChartData = {
        datasets: <dataSet[]>[{
            label: 'O₂',
            backgroundColor: 'rgba(0, 0, 0, 0)',
            borderColor: '#00f',
            pointBorderColor: '#000',
            pointBackgroundColor: 'rgba(0, 100, 0, 0.4)',
            pointBorderWidth: 1,
            data: [
                {x: 0.1, y: 0.1},
                {x: 0.2, y: 0.2},
                {x: 0.3, y: 0.3},
                {x: 0.4, y: 0.4},
                {x: 0.5, y: 0.5}
            ],
        },
        {
            label: 'bpm',
            backgroundColor: 'rgba(0, 0, 0, 0)',
            borderColor: '#000',
            pointBorderColor: '#000',
            pointBackgroundColor: 'rgba(0, 100, 0, 0.4)',
            pointBorderWidth: 1,
            data: [
                {x: 0.1, y: 0.5},
                {x: 0.2, y: 0.4},
                {x: 0.3, y: 0.3},
                {x: 0.4, y: 0.2},
                {x: 0.5, y: 0.1}
            ],
        }],
    };
    var options = {
        bezierCurve: false,
        pointDot: false,
    }
    /*
     * This uses the undocumented upcoming Scatter plot from Chart.js v2. The Chart.js repository has
     * a sample using this chart type under /samples/scatter.html. 
     */
    var chart = Chart.Scatter(ctx, {
        data: scatterChartData,
        options: {
            scales: {
                xAxes: [{
                    position: 'top',
                    gridLines: {
                        zeroLineColor: "#0f0",
                    }
                }],
            }
        }
    });
}
