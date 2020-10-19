var nodes = new vis.DataSet(NodeSet);
var edges = new vis.DataSet(EdgeSet);
var container = document.getElementById("mynetwork");
var data = {nodes: nodes, edges: edges};
var options = {};
var network = new vis.Network(container, data, options);
network.on('selectEdge',function(properties){
    idd = properties['nodes'][0];
    var tar = NodeSet[idd-1].label;
    console.log(tar);
    console.log(root_str)
    if(tar == root_str) {
        myChart.data.datasets = [];
    }
    myChart.data.datasets.push({'data':zifDict[tar].data, 'label':tar});
    if(tar == root_str) {
        myChart.data.datasets[0].borderColor = 'rgb(255, 99, 132)';
    }
    myChart.update();
});

var ctx = document.getElementById('myChart').getContext('2d');

var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: zifList['label'],
        datasets: [{
            label: root_str,
            data: zifList['data'],
            borderColor: 'rgb(255, 99, 132)',
            borderWidth: 1
        },
              ]
        },
    options: {

        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }
});
/*
var ctx2 = document.getElementById('myChart2').getContext('2d');
var myChart2 = new Chart(ctx2, {
    type: 'bar',
    data: {
        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
        datasets: [{
            label: '# of Votes',
            data: [12, 19, 3, 5, 2, 3],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
        },
    options: {

        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }
});*/