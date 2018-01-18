var onderwijsConfig = (function () {
    // General Vega embed options:
    var vegaEmbedOptions = {
        // "actions": {"export": true, "source": true, "editor": true}, // for debugging vega-lite specs
        "actions": {"export": false, "source": false, "editor": false},
        "renderer": "svg"
    };

    // Vega-lite Configuration objects for the various plots:
    var specSchoolAdviezen = {
        "$schema": "https://vega.github.io/schema/vega-lite/v2.json",
        "description": "Bar chart van schooladviezen",
        "data": {
          "url": null
        },
        "title": {
          "text": "School adviezen",
          "offset": 12
        },
        "facet": {
          "column": {
            "field": "advies",
            "type": "ordinal"
          }
        },
        "spec": {
          "height": 60,
          "width": 100,
          "layer": [
            {
              "mark": "bar", 
              "encoding": {
                "y": {
                  "field": "totaal",
                  "type": "quantitative"
                },
                "x": {
                  "field": "jaar",
                  "type": "nominal",
                  "axis": {
                    "title": "",
                    "labelAngle": 1e-10
                  }
                },
                "color": {
                  "field": "jaar",
                  "type": "nominal",
                  "legend": null,
                  "scale": {
                    "range": [
                      "#3182bd",
                      "#9ecae1",
                      "#deebf7"
                    ]
                  }
                }
              }
            },
            {
              "mark": {
                "type": "text",
                "baseline": "bottom",
                "dy": -2
              },
              "encoding": {
                "x": {
                  "field": "jaar",
                  "type": "nominal"
                },
                "y": {
                  "field": "totaal",
                  "type": "quantitative"
                },
                "text": {
                  "field": "totaal",
                  "type": "quantitative"
                }     
              }
            }
          ]
        },
        "config": {
          "view": {
            "stroke": "transparent"
          },
          "axis": {
            "domainWidth": 1
          }
        }
      }


    var specLeerlingenNaarGewicht = {
        "$schema": "https://vega.github.io/schema/vega-lite/v2.json",

        "description": "A simple bar chart with embedded data.",
        "data": {"url": null}, // TBD, see below
        "title": {
            "text": "Leerlingen naar gewicht",
            "anchor": "start",
            "offset": 12
        },
        "facet": {
            "column": {
              "field": "gewicht",
              "type": "ordinal"
            }
        },
        "spec": {
            "height": 80,
            "width": 100,
            "layer": [{
                "mark": "bar",
                "encoding": {
                    "y": {
                        "field": "totaal",
                        "type": "quantitative"
                    },
                    "x": {
                        "field": "jaar",
                        "type": "nominal",
                        "axis": {
                            "labelAngle": 1e-10, // 0 or 360 are not accepted here, bug in vega lite?
                            "title": ""
                        }
                    },
                    "color": {
                        "field": "jaar",
                        "type": "nominal",
                        "legend": null,
                        "scale": {
                            "range": ["#3182bd", "#9ecae1", "#deebf7"]
                        }
                    }
                },
            },
            {
                "mark": {
                    "type": "text",
                    "baseline": "bottom",
                    "dy": -1
                },
                "encoding": {
                    "y": {
                        "field": "totaal",
                        "type": "quantitative"
                    },
                    "x": {
                        "field": "jaar",
                        "type": "nominal"                        
                    },
                    "text": {
                        "field": "totaal",
                        "type": "quantitative"
                    }
                }
            }
            
        ]
        },
        "config": {
            "view": {"stroke": "transparent"},
            "axis": {"domainWidth": 1}
        }
    };

    // Endpoint URLs for these plots:
    var dataUrlSchooladviezen = document.location.origin + '/onderwijs/api/aggregated-advies/?vestiging=';
    var dataUrlLeerlingenNaarGewicht = document.location.origin + '/onderwijs/api/leerling-naar-gewicht/?vestiging=';

    function generateConfig(brin6){
        specSchoolAdviezen.data.url = dataUrlSchooladviezen + brin6;
        specLeerlingenNaarGewicht.data.url = dataUrlLeerlingenNaarGewicht + brin6;

        var config = {
            vegaEmbedOptions: vegaEmbedOptions,
            specSchoolAdviezen: specSchoolAdviezen,
            specLeerlingenNaarGewicht: specLeerlingenNaarGewicht
        }

        return config;
    }

    return {
        generateConfig: generateConfig
    };
})();