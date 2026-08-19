var ajax_request = function(xmlhttp, callback, params) {
	xmlhttp.onreadystatechange = function() {
		if( this.readyState == 4 && this.status == 200 ) {
			callback();
		}
	}
	xmlhttp.open('GET','./ajax.php?'+params,true);
	xmlhttp.send(null);
}

if (typeof XMLHttpRequest == "undefined") {
  XMLHttpRequest = function () {
    try { return new ActiveXObject("Msxml2.XMLHTTP.6.0"); }
      catch (e) {}
    try { return new ActiveXObject("Msxml2.XMLHTTP.3.0"); }
      catch (e) {}
    try { return new ActiveXObject("Microsoft.XMLHTTP"); }
      catch (e) {}
    //Microsoft.XMLHTTP points to Msxml2.XMLHTTP and is redundant
    throw new Error("This browser does not support XMLHttpRequest.");
  };
}

var xmlhttp = new Array();
try {
	var xml = new XMLHttpRequest();
} catch (e) {
	var xml = new ActiveXObject('Microsoft.XMLHTTP');
}

var ajax_buscaDeptos = function(i) {
	try {
		xmlhttp[i] = new XMLHttpRequest();
	} catch (e) {
		xmlhttp[i] = new ActiveXObject('Microsoft.XMLHTTP');
	}
	ajax_request(xmlhttp[i],function() {
		document.getElementById('p_deptos'+i).innerHTML = xmlhttp[i].responseText;
	}, "arg2="+i+"&func=buscaDeptos")
}

var ajax_buscaProjetos = function(depto, i) {
	ajax_request(xml,function() {
		document.getElementById('p_projetos'+i).innerHTML = xml.responseText;
		var span = document.createElement('span');
		span.id = 'p_despesas'+i;
		document.getElementById('p_projetos'+i).parentNode.appendChild(span);
	}, "arg1="+depto+"&arg2="+i+"&func=buscaProjetos")
}

var ajax_buscaDespesas = function(projeto, i) {
	ajax_request(xml,function() {
		document.getElementById('p_despesas'+i).innerHTML = xml.responseText;
	}, 'arg1='+projeto+'&arg2='+i+'&func=buscaDespesas')
}

var ajax_buscaProdutos = function(acao) {
	ajax_request(xml,function() {
		document.getElementById('produtos').innerHTML = xml.responseText;
	}, 'arg1='+acao+'&func=buscaProdutos');
}

var ajax_buscaPeriodos = function(tipo_periodo, tipo) {
	ajax_request(xml,function() {
		document.getElementById('lstPeriodo').innerHTML = "";
		document.getElementById('lstPeriodo').innerHTML = xml.responseText;
	}, 'arg1='+tipo_periodo+'&func=buscaPeriodos');
}

var ajax_buscaAcoes = function(programa) {
	ajax_request(xml,function() {
		document.getElementById('acao').innerHTML = "";
		document.getElementById('acao').innerHTML = xml.responseText;
	}, 'arg1='+programa+'&func=buscaAcoes');
}

var ajax_buscaObjetivos = function(acao) {
	ajax_request(xml,function() {
		document.getElementById('objetivo').innerHTML = "";
		document.getElementById('objetivo').innerHTML = xml.responseText;
	}, 'arg1='+acao+'&func=buscaObjetivos');
}

var ajax_salvarComentario = function(acao,elemento,conta,valor,comentario) {
	xml.open('POST','',true);
	xml.send("acao="+acao+"&elemento="+elemento+"&conta="+conta+"&valor="+valor+"&comentario="+comentario);
}