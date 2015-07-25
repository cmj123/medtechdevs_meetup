declare var Chart;

interface CanvasJSDataPoint {
    x: number;
    y: number;
}

interface CanvasJSDataSet {
    label: string;
    data: CanvasJSDataPoint[];
    borderColor: string;
    backgroundColor: string;
    pointBorderColor: string;
    pointBackgroundColor: string;
    pointBorderWidth: number;
}

interface CanvasJSScatterData {
    datasets: CanvasJSDataSet[];
}

interface APISensorResponseElem {
    value: string;
    created_at: string;
    modified_at: string;
    timestamp_start: string;
    timestamp_end: string;
    parameter: number;
    sequence: number;
}

interface DataPoint {
    value: number;
    /** Time in milliseconds */
    time: number;
}

function scatterData(o2data: DataPoint[], heartbpm: DataPoint[]): CanvasJSScatterData {
    function convert(val: DataPoint): CanvasJSDataPoint {
        return {x: val.time, y: val.value};
    }

    return {
        datasets: <CanvasJSDataSet[]>[{
            label: 'O₂',
            backgroundColor: 'rgba(0, 0, 0, 0)',
            borderColor: '#00f',
            pointBorderColor: '#000',
            pointBackgroundColor: 'rgba(0, 100, 0, 0.4)',
            pointBorderWidth: 1,
            data: o2data.map(convert),
        },
        {
            label: 'bpm',
            backgroundColor: 'rgba(0, 0, 0, 0)',
            borderColor: '#000',
            pointBorderColor: '#000',
            pointBackgroundColor: 'rgba(0, 100, 0, 0.4)',
            pointBorderWidth: 1,
            data: heartbpm.map(convert),
        }],
    };
}

function plotData(o2data: DataPoint[], heartbpm: DataPoint[]): void {
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

const API_HOST = 'https://copd.herokuapp.com';
const API_BASE = `${API_HOST}/sensors/api/v1.0`;

function parseDataPoints(elem: APISensorResponseElem): DataPoint[] {
    const frequency = 1; // hard-coded 1 Hz
    const start = Date.parse(elem.timestamp_start);
    const end = Date.parse(elem.timestamp_end);
    const npoints = frequency * ((end - start) / 1000) + 1; // + 1 because range is inclusive
    var result = new Array(npoints)
    for (let i = 0; i < npoints; i++) {
        result[i] = {
            value: +elem.value,
            time: start + (i * 1000 / frequency),
        };
    }
    return result;
}

function getSensorData(sensorname: string): Promise<APISensorResponseElem[]> {
    switch (sensorname) {
    case "HR":
    case "O2":
        break;
    default:
        throw new Error(`Unknown sensorname: ${sensorname}`);
    }
    const url = `${API_BASE}/measurement_by_time/?patient_id=1;sensor_name=${sensorname};start_time=201506220000;end_time=20150622220010`;
    return new Promise<APISensorResponseElem[]>(function (good, bad) {
        const xhr = new XMLHttpRequest();
        xhr.responseType = "json";
        xhr.onload = function () {
            const xhr: XMLHttpRequest = this;
            if (xhr.status !== 200) {
                bad(new Error(`Unexpected status code in XHR request: ${xhr.status}`));
                return;
            }
            good(xhr.response);
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

function flatten<T>(ar: T[][]): T[] {
    return [].concat.apply([], ar);
}

function flatMap<T, U>(ar: T[], f: {(T): U[]}): U[] {
    return flatten(ar.map(f));
}

function handleAPIResponse(O2Resp: APISensorResponseElem[], HRResp: APISensorResponseElem[]): void {
    const o2 = flatMap(O2Resp, parseDataPoints);
    const hr = flatMap(HRResp, parseDataPoints);
    plotData(o2, hr);
}

function medtech_main() {
    Promise.all(["O2", "HR"].map(getSensorData)).then(function ([o2, hr]) {
        handleAPIResponse(o2, hr);
    }, function (err) {
        reportError(err);
    });
}
