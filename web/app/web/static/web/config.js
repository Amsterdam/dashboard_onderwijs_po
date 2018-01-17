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
        "height": 60,
        "description": "Bar chart van schooladviezen",
        "data": {
            //"url": "/onderwijs/schooladvies/?vestiging=04LA00"
            "url": null // TBD
        },
        "title": "School adviezen",
        "mark": "bar",
        "encoding": {
            "column": {
                "field": "advies",
                "type": "ordinal"
            },
            "y": {
                "field": "totaal",
                "type": "quantitative"
            },
            "x": {
                "field": "jaar",
                "type": "nominal",
                "axis": {
                    "title": "",
                    "labelAngle": -45
                }
            },
            "color": {
                "field": "jaar",
                "type": "nominal",
                "legend": null,
                "scale":{
                    "range": ["#3182bd", "#9ecae1", "#deebf7"]
                }
            }
        },
        "config": {
            "view": {"stroke": "transparent"},
            "axis": {
            "domainWidth": 1
            }
        
        }
    }

    var specLeerlingenNaarGewicht = {
        "$schema": "https://vega.github.io/schema/vega-lite/v2.json",
        "height": 80,
        "description": "A simple bar chart with embedded data.",
        "data": {"url": null}, // To be determined! "/onderwijs/leerling-naar-gewicht/?vestiging=04LA00"
        "title": "Leerlingen naar gewicht",
        "mark": "bar",
        "encoding": {
            "column": {
                "field": "gewicht",
                "type": "ordinal"
            },
            "y": {
                "field": "totaal",
                "type": "quantitative"
            },
            "x": {
                "field": "jaar",
                "type": "nominal",
                "axis": {
                    "labelAngle": -45,
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
        "config": {
            "view": {"stroke": "transparent"},
            "axis": {"domainWidth": 1}
        }
    };

    // Endpoint URLs for these plots:
    var dataUrlSchooladviezen = document.location.origin + '/onderwijs/aggregated-advies/?vestiging=';
    var dataUrlLeerlingenNaarGewicht = document.location.origin + '/onderwijs/leerling-naar-gewicht/?vestiging=';

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