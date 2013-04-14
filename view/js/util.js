"use strict";
$(function () {
    $.extend({
        getQueries: function () {
            var vars = [], hash;
            var href = window.location.href;
            var url = href.substr(0, href.length - window.location.hash.length).replace(/#$/, '');
            var hashes = url.slice(url.indexOf('?') + 1).split('&');
            console.log(hashes);
            for (var i = 0; i < hashes.length; i++) {
                hash = hashes[i].split('=');
                vars.push(hash[0]);
                vars[hash[0]] = hash[1];
            }
            return vars;
        },
        getQuery: function (name) {
            var value = $.getQueries()[name];
            return value ? value : "";
        }
    });
});

function addTags(tags) {
    var appendTo = $('<div class="tags"></div>');
    _.forEach(tags, function (value) {
        appendTo.append('<span class="badge badge-info"><a href="scenario_list.html?tag=' + encodeURIComponent(value) + '">' + _.escape(value) + '</a></span>');
    });
    return appendTo;
}

