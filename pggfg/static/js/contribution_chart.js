$('#highcharts-container').highcharts({
    title: {
        text: chart_title
    },
    credits: {
        enabled: false
    },
    chart: {
        type: 'scatter',
        zoomType: 'xy'
    },
    xAxis: {

        title: {text: 'Период'},
        allowDecimals: false,
        categories: categories,
    },
    yAxis: {
        title: {
            text: 'ECU'
        },

    },
    tooltip: {
        crosshairs: true,
        headerFormat: '<b>{point.series.name}</b><br />',
        pointFormat: 'Contribution: <b>{point.y}</b> '
    },
    legend: {
        layout: 'horizontal',
        align: 'center',
        verticalAlign: 'bottom',
        borderWidth: 0
    },
    series: [
        {
            'name': 'Средний вклад по вашей группе',
            'type': 'line',
            'data': group_average,
            'marker': {
                'radius': 10,
            }
        },
        {
            'name': 'Ваши вложения в общий счет',
            'type': 'line',
            'data': individual_contributions,
            'marker': {
                'radius': 10,
            }
        }]
});
