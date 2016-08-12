$(function() {
    $('#viz').parent()
        .css('overflow', 'hidden')
        .css('padding', '0');

    $.ajax({
        url: 'graph',
        type: 'GET',
        data: { 'id':window.location.pathname.split('/').pop() },
        success: function(data) {
            create_graph(data);
        },
        error: function() {
            $('#viz').parent().parent().hide();
        }
    });
});

function create_graph(data) {
    var visualization = d3plus.viz()
        .container("#viz")
        .data(data)
        .type("bar")
        .id("name")
        .x("campus")
        .y("participantes")
        .height(300)
        .draw()
}