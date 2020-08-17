$(function() {

    $('#search_city').keyup(function() {

        $.ajax({
            url: "/saloons/search-city/",
            method: "GET",
            data: {
                'search_text' : $('#search_city').val(),
                'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
            },
            success: searchSuccess,
            dataType: 'html'
        });
    });
});

function searchSuccess(data, textStatus, jqXHR)
{
    console.log($('#search_city').val())
}