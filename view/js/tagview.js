"use strict";
$(function () {

    $('#tagPrefix').keyup(_.throttle(function (e) {
        updateTagSearch();
    }, 500));

    $('#tagPrefix input').val($.getQuery('prefix'));
    updateTagSearch();

    printAllTags();

    function printAllTags() {
        $.getJSON('/api/tag.json', function (data) {
            var list = _.sortBy(data.list, function (val) {
                return val.tag;
            })
            _.forEach(list, function (val) {
                $('#allTags').append('<span class="badge badge-info"><a href="scenario_list.html?tag=' + encodeURIComponent(val.tag) + '">' + _.escape(val.tag) + '</a></span>');
            });
        })
    }

    function updateTagSearch() {
        var prefix = $('#tagPrefix input').val();
        $('#tagPrefix a').attr('href', '?prefix=' + encodeURIComponent(prefix));
        $.getJSON('/api/tag.json?prefix=' + encodeURIComponent(prefix), function (data) {
            $('#tags tbody tr').remove();
            var list = _.sortBy(data.list, function (val) {
                return val.tag;
            })
            _.forEach(list, function (value) {
                var className = "";
                if (value.notyet > 0) {
                    className = "warning";
                }
                $('#tags tbody').append(
                    $('<tr class="' + className + '">'
                    + '<td><a href="scenario_list.html?tag=' + encodeURIComponent(value.tag) + '">' + _.escape(value.tag) + '</a></td>'
                    + '<td>' + value.total + '</td>'
                    + '<td><strong>' + value.notyet + '</strong></td></tr>'));
            });
            if (!list.length) {
                $('#tags tbody').append($('<tr><td colspan="2">no tags matched</td></tr>'));
            }
        });
    }
});
