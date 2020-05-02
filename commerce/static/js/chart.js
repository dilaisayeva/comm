$('.btn-shopping-cart').each(function () {
    let value = $(this).data("value")
    if (value.trim() == 'True') {
        $(this).children().removeClass("ti-shopping-cart")
        $(this).children().addClass("ti-shopping-cart-full")

        console.log('val=',value)

    }
    $(this).click(function (e) {

        e.preventDefault()
        let user = $(this).data("user")
        let quantity = $(this).data("quantity")
        let product = $(this).data("product")
        let value = $(this).data("value").trim()
        if (user.trim() !== 'AnonymousUser'.trim()){

        if ($(this).children().hasClass("ti-shopping-cart")) {
            $(this).children().removeClass("ti-shopping-cart")
            $(this).children().addClass("ti-shopping-cart-full")
            $('#lblCartCount').text(parseInt($('#lblCartCount').text())+1)



        } else if ($(this).children().hasClass("ti-shopping-cart-full")) {
            $(this).children().removeClass("ti-shopping-cart-full")
            $(this).children().addClass("ti-shopping-cart")
            $('#lblCartCount').text(parseInt($('#lblCartCount').text())-1)

        }

        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        $.ajax({
            url: "/ajaxify_cart_form/",
            method: 'POST',
            data: {
                "csrfmiddlewaretoken": csrftoken,
                "user": user,
                'product': product,
                'quantity': quantity,
                'value': value,



            },
            success: function (data) {
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
    var sub = 0
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
        curreny = $(this).parent().parent().siblings(":last").children().first().data('currency')
        total = parseFloat(price * count).toFixed(2)
        var subtotal1 =parseFloat($(this).parent().parent().parent().parent().children().last().prev().prev().children().last().children().first().text().substring(1).trim()) 
        subtotal1= (parseFloat(subtotal1) + parseFloat(price)).toFixed(2)

        if($(this).prev().val() > 1){

            $(this).next().removeAttr("disabled");
            
        } 
       
        if (parseInt(quantity) == parseInt(count)) {
            $(this).attr("disabled", true);
        } else {
            $(this).removeAttr("disabled");

        }
        $(this).parent().parent().siblings(":last").children().first().val(total.toString())
        $(this).parent().parent().parent().parent().children().last().prev().prev().children().last().children().first().text(curreny + subtotal1)
        

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
        var total = 0
        price = $(this).prev().prev().data('price')
        count = $(this).prev().prev().val()
        curreny = $(this).parent().parent().siblings(":last").children().first().data('currency')
        total = parseFloat(price * count).toFixed(2)
        $(this).parent().parent().siblings(":last").children().first().val(total.toString())
        quantity = $(this).prev().prev().data('quantity')
     
        if( $(this).prev().prev().val() == 1){

            $(this).attr("disabled", true);
            
        }else{
            $(this).removeAttr("disabled");

        }
        if (parseInt(quantity) > parseInt(count)) {

            $(this).prev().removeAttr("disabled");
        }
        //  else {
        //     $(this).removeAttr("disabled");


        // }
        subtotal1 = parseFloat($(this).parent().parent().parent().parent().children().last().prev().prev().children().last().children().first().text().substring(1).trim()) 
        // if (total >= price && subtotal1> price) { 

            subtotal1 = (parseFloat(subtotal1) - parseFloat(price)).toFixed(2)
        // }
        $(this).parent().parent().parent().parent().children().last().prev().prev().children().last().children().first().text(curreny + subtotal1)



    })
})