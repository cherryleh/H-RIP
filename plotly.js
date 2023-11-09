
var url1 = `./RID/${RID}/${RID}_rf_month.csv`;
var url2 = `./RID/${RID}/${RID}_rf_12m.csv`;
var url3 = `./RID/${RID}/${RID}_ndvi_month.csv`;
var url4 = `./RID/${RID}/${RID}_ndvi_12m.csv`;
var url5 = `./RID/${RID}/${RID}_et.csv`;
var url6 = `./RID/${RID}/${RID}_ndvi.csv`;
var url7 = `./RID/${RID}/${RID}_et_month.csv`;
var url8 = `./RID/${RID}/${RID}_et_12m.csv`;
var url9 = `./RID/${RID}/${RID}_rf.csv`;
var url11 = `./RID/${RID}/${RID}_t_month.csv`;
var url12 = `./RID/${RID}/${RID}_t_12m.csv`;
var url13 = `./RID/${RID}/${RID}_spi.csv`;

var selectorOptions = {
  buttons: [{
    step: 'month',
    stepmode: 'backward',
    count: 1,
    label: '1m',
    active: true
  }, {
    step: 'month',
    stepmode: 'backward',
    count: 6,
    label: '6m'
  }, {
    step: 'year',
    stepmode: 'todate',
    count: 1,
    label: 'YTD'

  }, {
    step: 'year',
    stepmode: 'backward',
    count: 1,
    label: '1y'
  }, {
    step: 'all',
  }],
};





//Multi = stacked bar+line graph, Single = historical, one-line time series
function makeplot() {
  Plotly.d3.csv(url1, function (data) { processData(data, 'trace1', 'Month', 'RF', 'RF-div', 'multi') });
  Plotly.d3.csv(url2, function (data) { processData(data, 'trace2', 'Month', 'RF', 'RF-div', 'multi') });
  Plotly.d3.csv(url3, function (data) { processData(data, 'trace3', 'Month', 'NDVI', 'NDVI-div', 'multi') });
  Plotly.d3.csv(url4, function (data) { processData(data, 'trace4', 'Month', 'NDVI', 'NDVI-div', 'multi') });
  Plotly.d3.csv(url7, function (data) { processData(data, 'trace5', 'Month', 'ET', 'ET-div', 'multi') });
  Plotly.d3.csv(url8, function (data) { processData(data, 'trace6', 'Month', 'ET', 'ET-div', 'multi') });
  Plotly.d3.csv(url5, function (data) { processData(data, 'trace7', 'datetime', 'ET', 'ET-hist', 'single') });
  Plotly.d3.csv(url6, function (data) { processData(data, 'trace8', 'datetime', 'NDVI', 'NDVI-hist', 'single') });
  Plotly.d3.csv(url9, function (data) { processData(data, 'trace9', 'datetime', 'RF_in', 'RF-hist', 'single') });
  Plotly.d3.csv(url11, function (data) { processData(data, 'trace11', 'Month', 'Temp', 'temp-div', 'multi') });
  Plotly.d3.csv(url12, function (data) { processData(data, 'trace12', 'Month', 'Temp', 'temp-div', 'multi') });
  Plotly.d3.csv(url13, function (data) { processData(data, 'trace13', 'datetime', 'SPI-3', 'SPI-12m', 'etc') });
  Plotly.d3.csv(url13, function (data) { processData(data, 'trace10', 'datetime', 'SPI-3', 'SPI-div', 'single') });
};
//Process CSV
function processData(allRows, traceName, xFieldName, yFieldName, divName, mode) {
  let x = [];
  let y = [];

  if (divName=='SPI-12m'){
    for (var i = allRows.length-12; i < allRows.length; i++) {
      row = allRows[i];
      x.push(row[xFieldName]);
      y.push(row[yFieldName]);
      
  }
  } 
  else{
    for (var i = 0; i < allRows.length; i++) {
      row = allRows[i];

      x.push(row[xFieldName]);
      y.push(row[yFieldName]);

    }
  }



  if (mode == 'single') {
    makeSinglePlot(x, y, traceName, divName)

  } else if (mode == 'multi' && yFieldName == 'RF') {
    traces_RF[traceName].x = x;
    traces_RF[traceName].y = y;

    makeRFPlotly(traces_RF[traceName], divName);
  }

  else if (mode == 'multi' && yFieldName == 'NDVI') {
    traces_NDVI[traceName].x = x;
    traces_NDVI[traceName].y = y;
    makeNDVIPlotly(traces_NDVI[traceName], divName);

  }
  else if (mode == 'multi' && yFieldName == 'ET') {
    traces_ET[traceName].x = x;
    traces_ET[traceName].y = y;
    makeETPlotly(traces_ET[traceName], divName);

  }
  else if (mode == 'multi' && divName == 'temp-div') {
    traces_temp[traceName].x = x;
    traces_temp[traceName].y = y;
    makeTempPlotly(traces_temp[traceName], divName);

  }
  else if (divName == 'SPI-div') {
    traces_SPI[traceName].x = x;
    traces_SPI[traceName].y = y;

    makeSPIPlotly(traces_SPI[traceName], divName);
  }
  else if (divName == 'SPI-12m'){
    SPI_12m[traceName].x = x;
    SPI_12m[traceName].y = y;
    const spiVal = (SPI_12m[traceName].y.map(Math.abs));
    const max = Math.max(...spiVal);
    const axis = ((Math.ceil(max*2)/2).toFixed(2));

    makeSPI_12m(SPI_12m[traceName], divName,axis);
  }


}

function makeSinglePlot(x, y, yTraceName, divName) {
  var traces = [{
    x: x,
    y: y,
    name: yTraceName,
    marker: {
      color: '#007ea7'
    },

  }];
  var layout = {
    xaxis: {
      rangeselector: selectorOptions,
      rangeslider: {}
    },
    yaxis: {
      fixedrange: true,
      side: 'right'
    },
    margin: {
      l: 30,
      r: 30,
      b: 50,
      t: 50,
      pad: 4
    },
    yaxis: {
      fixedrange: true,
      side: 'left'
    },
    showlegend: false,


  };
  var config = { responsive: true };

  Plotly.newPlot(divName, traces, layout, config);
};

function makeNDVIPlotly(trace, divName) {
  var data = [trace];

  var layout = {
    yaxis: {
      range: [0, 0.95]
    },
    margin: {
      l: 30,
      r: 30,
      b: 50,
      t: 50,
      pad: 4
    },
    showlegend: true,
    legend: {
      "orientation": "h", yanchor: "bottom",
      y: 1.02,
      xanchor: "right",
      x: 1
    }
  };

  var config = { responsive: true };


  Plotly.plot(divName, data, layout, config);
}

function makeRFPlotly(trace, divName) {
  var data = [trace];

  var layout = {

    margin: {
      l: 30,
      r: 30,
      b: 50,
      t: 50,
      pad: 4
    },
    showlegend: true,
    legend: {
      "orientation": "h", yanchor: "bottom",
      y: 1.02,
      xanchor: "right",
      x: 1
    }
  };

  var config = { responsive: true };


  Plotly.plot(divName, data, layout, config);
}

function makeETPlotly(trace, divName) {
  var data = [trace];

  var layout = {

    margin: {
      l: 30,
      r: 30,
      b: 50,
      t: 30,
      pad: 4
    },
    showlegend: true,
    legend: {
      "orientation": "h", yanchor: "bottom",
      y: 1.02,
      xanchor: "right",
      x: 1
    }
  };

  var config = { responsive: true };


  Plotly.plot(divName, data, layout, config);
}

function makeTempPlotly(trace, divName) {
  var data = [trace];

  var layout = {
    yaxis: {
      range: [50, 85]
    },

    margin: {
      l: 30,
      r: 30,
      b: 50,
      t: 30,
      pad: 4
    },
    showlegend: true,
    legend: {
      "orientation": "h", yanchor: "bottom",
      y: 1.02,
      xanchor: "right",
      x: 1
    }
  };

  var config = { responsive: true };


  Plotly.plot(divName, data, layout, config);
}
function makeSPIPlotly(trace, divName) {
  var data = [trace];

  var layout = {
    xaxis: {
      rangeselector: selectorOptions,
      rangeslider: {}
    },
    yaxis: {
      fixedrange: true,
      side: 'right'
    },
    margin: {
      l: 30,
      r: 30,
      b: 50,
      t: 30,
      pad: 4
    },
    shapes: [
      // 1st highlight during Feb 4 - Feb 6
      {
        type: 'line',
        x0: '1920-03-01',
        y0: 1,
        x1: '2022-08-01',
        y1: 1,
        line: {
          width: 0.5,
          dash: 'dashdot',
          opacity: 0.5
        }
      },
      {
        type: 'line',
        x0: '1920-03-01',
        y0: 2,
        x1: '2022-08-01',
        y1: 2,
        line: {
          width: 0.5,
          dash: 'dashdot'
        }
      },

    ],
  };

  var config = { responsive: true };

  Plotly.plot(divName, data, layout, config);
}

function makeSPI_12m(trace, divName,axis) {
    var data = [trace];
    console.log(trace);
    var layout = {
        xaxis: {
            dtick:'M1',
            tickangle: 30,
        },
        yaxis: {
            title: 'Drought         No Drought',
            range: [-axis, axis]
        },
        margin: {
            l: 60,
            r: 15,
            b: 45,
            t: 20,
            pad: 4
        },

    };

    var config = { responsive: true };

    Plotly.plot(divName, data, layout, config);
}

var traces_RF = {
  trace1: {
    meta: {
      columnNames: {
        x: 'Month',
        y: 'RF'
      }
    },
    // mode: 'markers', 
    type: 'bar',
    hoverinfo: 'y',
    name: 'Monthly Average',
    hovertemplate: '%{y:.2f}',
    marker: {
      color: 'rgb(158,202,225)',
      opacity: 0.6,
      line: {
        color: 'rgb(8,48,107)',
        width: 1.5
      }
    }
  },
  trace2: {
    meta: {
      columnNames: {
        x: 'Month',
        y: 'RF'
      }
    },
    type: 'scatter',
    name: 'Observed',
    hovertemplate: '%{y:.2f}',
    hoverinfo: 'y',
    marker: {
      color: '#f29a28',

    }
  },

}

var traces_NDVI = {
  trace3: {
    meta: {
      columnNames: {
        x: 'Month',
        y: 'NDVI'
      }
    },
    // mode: 'markers', 
    type: 'bar',
    hoverinfo: 'y',
    name: 'Monthly Average',
    hovertemplate: '%{y:.2f}',
    marker: {
      color: 'rgb(158,202,225)',
      opacity: 0.6,
      line: {
        color: 'rgb(8,48,107)',
        width: 1.5
      }
    }
  },
  trace4: {
    meta: {
      columnNames: {
        x: 'Month',
        y: 'NDVI'
      }
    },
    type: 'scatter',
    name: 'Observed',
    hovertemplate: '%{y:.2f}',
    hoverinfo: 'y',
    marker: {
      color: '#f29a28',

    }
  },

}

var traces_ET = {
  trace5: {
    meta: {
      columnNames: {
        x: 'Month',
        y: 'ET'
      }
    },
    // mode: 'markers', 
    type: 'bar',
    hoverinfo: 'y',
    name: 'Monthly Average',
    hovertemplate: '%{y:.2f}',
    marker: {
      color: 'rgb(158,202,225)',
      opacity: 0.6,
      line: {
        color: 'rgb(8,48,107)',
        width: 1.5
      }
    }
  },
  trace6: {
    meta: {
      columnNames: {
        x: 'Month',
        y: 'ET'
      }
    },
    type: 'scatter',
    name: 'Observed',
    hovertemplate: '%{y:.2f}',
    hoverinfo: 'y',
    marker: {
      color: '#f29a28',

    }
  },

}

var traces_temp = {
  trace11: {
    meta: {
      columnNames: {
        x: 'Month',
        y: 'Temp'
      }
    },
    // mode: 'markers', 
    type: 'bar',
    hoverinfo: 'y',
    name: 'Monthly Average',
    hovertemplate: '%{y:.2f}',
    marker: {
      color: 'rgb(158,202,225)',
      opacity: 0.6,
      line: {
        color: 'rgb(8,48,107)',
        width: 1.5
      }
    }
  },
  trace12: {
    meta: {
      columnNames: {
        x: 'Month',
        y: 'Temp'
      }
    },
    type: 'scatter',
    name: 'Observed',
    hovertemplate: '%{y:.2f}',
    hoverinfo: 'y',
    marker: {
      color: 'orange',

    }
  }/*,
  trace13: {
    meta: {
      columnNames: {
        x: 'Month',
        y: 'RF'
      }
    },
    type: 'scatter',
    name: 'Max',
    hovertemplate: '%{y:.2f}',
    hoverinfo: 'y',
    marker: {
      color: 'red',

    }
  },
  trace14: {
    meta: {
      columnNames: {
        x: 'Month',
        y: 'RF'
      }
    },
    type: 'scatter',
    name: 'Min',
    hovertemplate: '%{y:.2f}',
    hoverinfo: 'y',
    marker: {
      color: 'green',

    }
  }*/
}


var traces_SPI = {
  trace10: {
    meta: {
      columnNames: {
        x: 'Month',
        y: 'SPI'
      }
    },
    type: 'scatter',
    fill: 'tozeroy',
    fillcolor: 'lightblue',
    name: 'Drought',
    hovertemplate: '%{y:.2f}',
    hoverinfo: 'y',
    marker: {
      color: '',

    },
    line: {
      color: 'black',
      width: 0.5
    }
  }

}

var SPI_12m = {
  trace13: {
      meta: {
          columnNames: {
              x: 'Month',
              y: 'SPI'
          }
      },
      mode: 'lines+markers', 
      type: 'scatter',
      hoverinfo: 'y',
      name: 'SPI',
      hovertemplate: '%{y:.2f}',
  }

}

makeplot();

