$(function () {
    var id = decodeURIComponent($.getQuery('id'));
    if (!id) {
        return;
    }

    $.getJSON('/api/scenario/' + encodeURIComponent(id) + '.json', function (data) {
        if (data.list.length === 0) {
            return;
        }
        $('#scenarioDoc').text(data.list[0].doc);
        $('#scenarioPath').text(data.list[0].path);
        $('#scenarioBody').text(data.list[0].body);
        prettyPrint();
    });

    $.getJSON('/api/scenario/' + encodeURIComponent(id) + '/tag.json', function (data) {
        var list = _.sortBy(data.list, function (val) {
            return val.tag;
        })
        _.forEach(list, function (val) {
            $('#scenarioTags').append('<span class="badge badge-info"><a href="scenario_list.html?tag=' + encodeURIComponent(val.tag) + '">' + _.escape(val.tag) + '</a></span>');
        });
    })
});