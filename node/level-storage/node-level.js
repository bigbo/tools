var level = require('levelup');
var db    = level('/tmp/mylevel.db');

var call_back_function = function(err){
	if(err){
		console.log('[Error] : '+err);
	}else{
		console.log('Put Key OK');
	}
};

var print_function = function(err , value){
	if(err){
		console.log('{Error} : '+err);
	}

	console.log('[Value] : '+value);
};

db.put('key' , 'value' , call_back_function);
db.get('key' , print_function);
