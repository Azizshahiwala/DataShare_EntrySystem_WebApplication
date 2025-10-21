
function calcTotal(){
   var qtd = document.getElementById("prod_qtd").value;
   var price = document.getElementById("prod_price").value;
   
   if(qtd == null && price == null){
    document.getElementById("prod_total").value = "Total";
   }
   else{
   var total = qtd * price;
   document.getElementById("prod_total").value = total;
   }
}


function checkMissingField(){

    var qtd = document.getElementById("prod_qtd").value;
    var price = document.getElementById("prod_price").value;
    var OrderT = document.getElementById("ordertype").value;
    var PaymentT = document.getElementById("paymenttype").value;
    var Item = document.getElementById("item").value;

    if(qtd < 0 || price < 0 || Item == "ITEM" || OrderT == "Order Type" || PaymentT == "Payment type"){
        alert("Missing fields");
        return;
    }


}

function showCredits(){
    
}

