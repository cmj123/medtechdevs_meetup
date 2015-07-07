// Testing the build
function medtech_main() {
    var i: number = 3;
    var p = document.createElement('p');
    p.textContent = 'TypeScript build succeeded: ' + i;
    document.body.appendChild(p);
}

/* WIP

function getdata(data) {
    return Promise
}

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

function medtech_main() {
    var ctx = document.getElementById('mychart').getContext('2d');

    var data = {
        labels: repeat('', 6),
        datasets: [{
            label: "O2",
            data: [1,2,1,1,3,1]
        }],
    };
    var options = {
        bezierCurve: false,
        pointDot: false,
    }
    var chart = new Chart(ctx).Line(data, options);
}
*/
