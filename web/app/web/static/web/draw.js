function paginatedJson(url, callback, ar){
    // assumes .next property for next page
    // assumes .next is null when no more pages available
    // modifies ar in place

    // make sure we have an array for our results:
    if (ar === undefined){
        var ar = [];
    }

    // download a page, check for following pages, download (recursively)
    d3.json(url, function(error, data){
        if (error) throw error;

        ar = ar.concat(data.results);
        if (data.next !== null) {
            paginatedJson(data.next, callback, ar);
        } else {
            callback(null, ar);
        };
    });
}

function paginatedVegaEmbed(id, vegaSpec, vegaEmbedOptions){
    // this modifies the provided vegaEmbedOptions !
    var dataUrl = vegaSpec.data.url;

    paginatedJson(dataUrl, function(error, data){
        delete vegaSpec.data;
        vegaSpec.data = {
            'values': data
        };
        vegaEmbed(id, vegaSpec, vegaEmbedOptions);
    });
}

function drawSubsidieTable(){
    // TODO: make year filter configurable
    var subdidieDataUrl = "/onderwijs/api/toegewezen-subsidie/?vestiging=" + brin6 + "&subsidie__jaar=2017";
    paginatedJson(subdidieDataUrl, function(error, subsidieData){
        var tmp = d3.select('#vis3')
        tmp.selectAll('div')
            .data(subsidieData).enter()
            .append('div')
            .style('font-size', '12px')
            .text(function(d, i){ return d.subsidie + " " + d.aantal; });
    });
}

var config = onderwijsConfig.generateConfig(brin6);
vegaEmbed('#vis', config.specSchoolAdviezen, config.vegaEmbedOptions);
paginatedVegaEmbed('#vis2', config.specLeerlingenNaarGewicht, config.vegaEmbedOptions);
drawSubsidieTable();
