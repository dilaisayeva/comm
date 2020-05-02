$('.detail_btn').each(function () {
    // console.log($(this).parent().prev().children().first().next().val())
    // console.log($(this).parent().prev().children().first().next().data('quantity'))
    if ($(this).data('value').trim() == 'True'){
        $(this).text('Added to chart')
    }
    var count = $('#lblCartCount').text()

    $(this).click(function (e) {
        
        e.preventDefault()
        var user  = $(this).data('user')
        var product = $(this).data('product')
        var value = $(this).data('value')
        var quantity = $(this).parent().prev().children().first().next().next().data('quantity')
        if (user.trim() !== 'AnonymousUser'.trim()){
            console.log($(this).parent().prev().children().first().next().val())
        

        if ($(this).text() == 'Added to chart'){
            $('#lblCartCount').text(parseInt($('#lblCartCount').text())-1)
            $(this).text('Add to chart')
        }else if ($(this).text() == 'Add to chart') {
            $(this).text('Added to chart')
            $('#lblCartCount').text(parseInt($('#lblCartCount').text())+1)
        }
        // if ($(this).children().hasClass("ti-heart")) {
        //     $(this).children().removeClass("ti-heart")
        //     $(this).children().addClass("ti-heart-broken")


        //     console.log('salam')
        // } else if ($(this).children().hasClass("ti-heart-broken")) {
        //     $(this).children().removeClass("ti-heart-broken")
        //     $(this).children().addClass("ti-heart")

        //     console.log('salam1')


        // }
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        // console.log(csrftoken)
        $.ajax({
            url: "/ajaxify_detail_form/",
            method: 'POST',
            data: {
                "csrfmiddlewaretoken": csrftoken,
                "user": user,
                'product': product,
                'value': value,
                'quantity': quantity



            },
            success: function (data) {
                // $(".count-join").html(count);
                console.log(data)
            },
            error: function (err) {
                console.log(err)
            }
        }).then(function (resp) {
            console.log(resp)
        })
    }else{
        window.location.href="/signup/";
     
    }

    })

})



$('.increase').each(function () {
    if( $(this).prev().data('quantity') == 1){
        

        $(this).attr("disabled", true);
        
    }else{
        $(this).removeAttr("disabled");

    }
    $(this).click(function (e) {
        price = $(this).prev().data('price')
    
        quantity = $(this).prev().data('quantity')
        var total = 0
        count = $(this).prev().val()
         

        if($(this).prev().val() > 1){

            $(this).next().removeAttr("disabled");
            
        } 
       
        if (parseInt(quantity) == parseInt(count)) {
            $(this).attr("disabled", true);
        } else {
            $(this).removeAttr("disabled");

        }
     
        

    })

})

$('.reduced').each(function () {
    if( $(this).prev().prev().val() == 1){
        

        $(this).attr("disabled", true);
        
    }else{
        $(this).removeAttr("disabled");

    }
    // console.log( $(this).prev())
    $(this).click(function (e) {
        price = $(this).prev().prev().data('price')
        count = $(this).prev().prev().val()
        
     
        if( $(this).prev().prev().val() == 1){

            $(this).attr("disabled", true);
            
        }else{
            $(this).removeAttr("disabled");

        }
        if (parseInt(quantity) > parseInt(count)) {

            $(this).prev().removeAttr("disabled");
        }
        



    })
})