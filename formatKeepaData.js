function formatKeepaData(keepa_json_path) {

    const json = require(keepa_json_path); // example: ./data.json
    var amazon_data = json['products'][0]['csv'][0];
    var data_array = [];
 
    var amazon_prices = [];
    for (var i = 0; i < amazon_data.length; i++) {
          if(amazon_data[i]%2==1 && i != 0)
          data_array.push({'date': amazon_data[i-1], 'price': amazon_data[i]});
    };
    var tensor_data = JSON.stringify(data_array);
    return tensor_data;
}

function average(data){
    var sum = data.reduce(function(sum, value){
      return sum + value;
    }, 0);
   
    var avg = sum / data.length;
    return avg;
  }

var formatData =  formatKeepaData('./data.json');
//console.log(formatData);