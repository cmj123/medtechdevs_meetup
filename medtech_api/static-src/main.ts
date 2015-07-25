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

interface CanvasJSScatterData {
    datasets: dataSet[];
}

function scatterData(o2data: number[], heartbpm: number[]): CanvasJSScatterData {
    if (o2data.length !== heartbpm.length) {
        throw new Error("Length of two sensor data must be equal");
    }
    return {
        datasets: <dataSet[]>[{
            label: 'O₂',
            backgroundColor: 'rgba(0, 0, 0, 0)',
            borderColor: '#00f',
            pointBorderColor: '#000',
            pointBackgroundColor: 'rgba(0, 100, 0, 0.4)',
            pointBorderWidth: 1,
            data: o2data.map((val, i) => ({x: i, y: val})),
        },
        {
            label: 'bpm',
            backgroundColor: 'rgba(0, 0, 0, 0)',
            borderColor: '#000',
            pointBorderColor: '#000',
            pointBackgroundColor: 'rgba(0, 100, 0, 0.4)',
            pointBorderWidth: 1,
            data: heartbpm.map((val, i) => ({x: i, y: val})),
        }],
    };
}

function plotData(o2data: number[], heartbpm: number[]): void {
    const canvas = <HTMLCanvasElement>document.getElementById('mychart');
    const ctx = canvas.getContext('2d');

    const scatterChartData = scatterData(o2data, heartbpm);
    const options = {
        bezierCurve: false,
        pointDot: false,
    }
    /*
     * This uses the undocumented upcoming Scatter plot from Chart.js v2. The Chart.js repository has
     * a sample using this chart type under /samples/scatter.html. 
     */
    let chart = Chart.Scatter(ctx, {
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

interface APISensorResponseElem {
    value: string;
};

const API_HOST = 'https://copd.herokuapp.com';
const API_BASE = `${API_HOST}/sensors/api/v1.0`;

function getSensorData(sensorname: string): Promise<number[]> {
    switch (sensorname) {
    case "HR":
    case "O2":
        break;
    default:
        throw new Error(`Unknown sensorname: ${sensorname}`);
    }
    const url = `${API_BASE}/measurement_by_time/?patient_id=1;sensor_name=${sensorname};start_time=201506220000;end_time=20150622220010`;
    return new Promise<number[]>(function (good, bad) {
        const xhr = new XMLHttpRequest();
        xhr.responseType = "json";
        xhr.onload = function () {
            const xhr: XMLHttpRequest = this;
            if (xhr.status !== 200) {
                bad(new Error(`Unexpected status code in XHR request: ${xhr.status}`));
                return;
            }
            const responseobj = <APISensorResponseElem[]>xhr.response;
            good(responseobj.map(x => JSON.parse(x.value)));
        };
        xhr.onerror = function (e) {
            const xhr: XMLHttpRequest = this;
            bad(new Error("An error occurred during the XHR request"));
        };
        xhr.open("GET", url);
        xhr.send();
    });
}

function reportError(err) {
    console.error(err);
    const errnode = document.getElementById('error');
    errnode.textContent = ''+err;
    errnode.classList.remove('hidden');
}

function medtech_main() {
    Promise.all(["O2", "HR"].map(getSensorData)).then(function ([o2, hr]) {
        plotData(o2, hr);
    }, function (err) {
        reportError(err);
    });
}
