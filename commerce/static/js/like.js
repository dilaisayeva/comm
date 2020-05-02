$('.btn-heart').each(function () {
    // ti-heart-broken
    let value = $(this).data("value")
    if (value.trim() == 'True') {
        $(this).children().removeClass("ti-heart")
        $(this).children().addClass("ti-heart-broken")


    }
    $(this).click(function (e) {
        
        e.preventDefault()
        var user  = $(this).data('user')
        var product = $(this).data('product')
        var value = $(this).data('value')
        if (user.trim() !== 'AnonymousUser'.trim()){


        if ($(this).children().hasClass("ti-heart")) {
            $(this).children().removeClass("ti-heart")
            $(this).children().addClass("ti-heart-broken")


            console.log('salam')
        } else if ($(this).children().hasClass("ti-heart-broken")) {
            $(this).children().removeClass("ti-heart-broken")
            $(this).children().addClass("ti-heart")

            console.log('salam1')


        }
        console.log($(this).children())
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        // console.log(csrftoken)
        $.ajax({
            url: "/ajaxify_like_form/",
            method: 'POST',
            data: {
                "csrfmiddlewaretoken": csrftoken,
                "user": user,
                'product': product,
                'value': value,



            },
            success: function (data) {
                // $(".count-join").html(count);
                // console.log(data)
            },
            error: function (err) {
                // console.log(err)
            }
        }).then(function (resp) {
            console.log(resp)
        })
    }else{
        window.location.href="/signup/";
     
    }

    })

})
