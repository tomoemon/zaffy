"use strict";
$(function () {

    $('#tagPrefix').keyup(_.throttle(function (e) {
        updateTagSearch();
    }, 500));

    if ($.getQuery('prefix')) {
        $('#tagPrefix input').val($.getQuery('prefix'));
        updateTagSearch();
    }

    printAllTags();

    function printAllTags() {
        $.getJSON('/api/tag.json', function (data) {
            var list = _.sortBy(data.list, function (val) {
                return val.tag;
            })
            _.forEach(list, function (val) {
                $('#allTags').append('<span class="badge badge-info"><a href="scenario.html?tag=' + encodeURI(val.tag) + '">' + _.escape(val.tag) + '</a></span>');
            });
        })
    }

    function updateTagSearch() {
        var prefix = $('#tagPrefix input').val();
        $('#tagPrefix a').attr('href', '?prefix=' + encodeURI(prefix));
        $.getJSON('/api/tag.json?prefix=' + encodeURI(prefix), function (data) {
            console.log(data);
            $('#tags tbody tr').remove();
            var list = _.sortBy(data.list, function (val) {
                return val.tag;
            })
            _.forEach(list, function (value) {
                $('#tags tbody').append($('<tr><td>' + _.escape(value.tag) + '</td><td>' + value.count + '</td></tr>'));
            });
            if (!list.length) {
                $('#tags tbody').append($('<tr><td colspan="2">no tags matched</td></tr>'));
            }
        });
    }
});
