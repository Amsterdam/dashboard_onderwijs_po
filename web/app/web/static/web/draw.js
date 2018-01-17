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

function drawSubsidieTable(id){
    // TODO: make year filter configurable
    var subdidieDataUrl = document.location.origin + "/onderwijs/api/toegewezen-subsidie/?vestiging=" + brin6 + "&subsidie__jaar=2017";
    paginatedJson(subdidieDataUrl, function(error, subsidieData){
        var target = d3.select(id);
        target.append('div')
            .style('font-weight', 'bold')
            .text('Subsidies')
        target.selectAll('div')
            .data(subsidieData).enter()
            .append('div')
            .style('font-size', '12px')
            .text(function(d, i){ return d.subsidie + " " + d.aantal; });
    });
}

function drawCitoScore(id){
    var citoScoresDataUrl = document.location.origin + '/onderwijs/api/cito-score/?vestiging=' + brin6 + '&jaar=2016';

    paginatedJson(citoScoresDataUrl, function(error, data){
        console.log(data);
        var target = d3.select(id);
        target.append('div')
            .style('font-weight', 'bold')
            .text('Cito score');
        target.append('div').append('h1')
            .style('text-align', 'center')
            .text(data[0].cet_gem);
        target.append('div')
            .style('text-align', 'right')
            .text('A\'dams gem = ' + Math.round(data[0].cet_gem_avg));
    });
}

function drawAggStatsTable(id){
    var schoolWisselaarsDataUrl = document.location.origin + '/onderwijs/api/',
        vveIndicatiesDataUrl = '',
        leerlingLeraarRatioDataUrl = '';
}


var config = onderwijsConfig.generateConfig(brin6);
vegaEmbed('#vis2', config.specSchoolAdviezen, config.vegaEmbedOptions);
paginatedVegaEmbed('#vis', config.specLeerlingenNaarGewicht, config.vegaEmbedOptions);
drawSubsidieTable('#vis3');
drawCitoScore('#vis6');