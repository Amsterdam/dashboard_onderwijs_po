var config = onderwijsConfig.generateConfig(brin6);
vegaEmbed('#vis', config.specSchoolAdviezen, config.vegaEmbedOptions);
vegaEmbed('#vis2', config.specLeerlingenNaarGewicht, config.vegaEmbedOptions);


// Subsidies (TODO: make this a proper table)

(function () {
    var subdidieDataUrl = "/onderwijs/toegewezen-subsidie/?vestiging=" + brin6 + "&subsidie__jaar=2017";
    d3.json(subdidieDataUrl, function(error, subsidieData){
        var tmp = d3.select('#vis3')
        tmp.selectAll('div')
            .data(subsidieData).enter()
            .append('div')
            .style('font-size', '12px')
            .text(function(d, i){ return d.subsidie + " " + d.aantal; });
    });      
})();
