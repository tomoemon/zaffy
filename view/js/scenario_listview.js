$(function () {
    var tag = decodeURIComponent($.getQuery('tag'));

    $('#tag').text('tag: ' + tag);

    if (tag) {
        $.getJSON('/api/tag/' + encodeURIComponent(tag) + '.json?co=1', function (data) {
            $('#cooccurrence').empty();
            $('#cooccurrence').append(addTags(_.map(data.list, function (v) { return v.tag; })));
        });
    }

    $.getJSON('/api/scenario.json?tag=' + encodeURIComponent(tag), function (data) {
        $('#scenario_list tbody tr').remove();
        var list = _.sortBy(data.list, function (val) {
            return val.path;
        });
        _.forEach(list, function (value) {
            var className = "";
            if (value.action_count == 0) {
                className = "warning";
            }
            var tr =  $('<tr class="' + className + '">'
                + '<td><a href="/scenario.html?id=' + value.id + '">' +_.escape(value.doc) + '</a></td>'
                + '<td><div>' + _.escape(value.path) + '</div></td>'
                + '<td><strong>' + value.action_count + '</strong></td>'
                + '</tr>'
            );
            tr.children('td:eq(1)').append(addTags(value.tags.split("\t")));

            $('#scenario_list tbody').append(tr);
        });
        if (!list.length) {
            $('#scenario_list tbody').append($('<tr><td colspan="2">no tags matched</td></tr>'));
        }
    });
});
