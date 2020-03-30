function genType(d) {
  d.TIMESTAMP  = parseDate(d.as_of_date);
  d.LOW        = +d.low;
  d.HIGH       = +d.high; 
  d.OPEN       = +d.open;
  d.CLOSE      = +d.close;
  d.TURNOVER   = +d.turnover;
  d.VOLATILITY = +d.volatility;
  return d;
}

function timeCompare(date, interval) {
  if (interval == "week")       { var durfn = d3.time.monday(date); }
  else if (interval == "month") { var durfn = d3.time.month(date); }
  else { var durfn = d3.time.day(date); } 
  return durfn;
}

function dataCompress(data, interval) {
  var compressedData  = d3.nest()
                 .key(function(d) { return timeCompare(d.TIMESTAMP, interval); })
                 .rollup(function(v) { return {
                         TIMESTAMP:   timeCompare(d3.values(v).pop().TIMESTAMP, interval),
                         OPEN:        d3.values(v).shift().OPEN,
                         LOW:         d3.min(v, function(d) { return d.LOW;  }),
                         HIGH:        d3.max(v, function(d) { return d.HIGH; }),
                         CLOSE:       d3.values(v).pop().CLOSE,
                         TURNOVER:    d3.mean(v, function(d) { return d.TURNOVER; }),
                         VOLATILITY:  d3.mean(v, function(d) { return d.VOLATILITY; })
                        }; })
                 .entries(data).map(function(d) { return d.values; });

  return compressedData;
}
