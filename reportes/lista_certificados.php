<?php
function direcciones_correo($partner_id,$conexion ) {

		if ($partner_id <> "") {
		$query = "SELECT name, email_ventas, email_almacen, email_facturas
		FROM res_partner WHERE id = $partner_id";
		$result = pg_query($conexion, $query);
		while ($row = pg_fetch_assoc($result)) {
		$nombre = $row['name'];
		$emails['email_ventas'] = $row['email_ventas'];
		$emails['email_almacen'] = $row['email_almacen'];
		$emails['email_facturas'] = $row['email_facturas'];
		}
		//Quita los mails en blanco
		$emails = array_filter($emails);
		$emails = array_unique ($emails);
		if (count($emails) <= 0) {
		$emails['error']='Cliente no cuenta con email registrado | ' .$nombre ;
		}
		} else {
		$emails['error'] = 'Cliente no especificado';
		}
return ($emails);
}

function tiene_certificado($producto,$conexion ) {
		$res = False;
		if ($producto <> "") {
		$query = "SELECT id
		FROM product_laboratorio WHERE name = $producto";
		$result = pg_query($conexion, $query);
		$cuenta = pg_num_rows($result);
		if ($cuenta == 0) {
		$res = False;
		} else {
		$res = True;
		}
		}

return ($res);
}
function mail_enviado_anteriormente($stock_move,$conexion ) {
		$res = False;
		if ($stock_move <> "") {
		$query = "SELECT id
		FROM mail_message WHERE model = 'stock.move' AND res_id = $stock_move";
		$result = pg_query($conexion, $query);
		$cuenta = pg_num_rows($result);
		if ($cuenta == 0) {
		$res = False;
		} else {
		$res = True;
		}
		}

return ($res);
}
//Conexion a BD
require_once('parametros.php');
//Es el ID de la tabla stock_move.
if (isset ($_GET['documentos'])){
	$documentos = $_GET['documentos'];
	$documentos = str_replace('[','',$documentos);
	$documentos = str_replace(']','',$documentos);
$conexion= pg_connect("host=$host port=$port dbname=$dbname user=$user password=$password") 
	   or die ("Nao consegui conectar ao PostGres --> " . pg_last_error($conn)); 
		$query = "SELECT stock_move.id,stock_move.origin,product_product.name_template, stock_move.partner_id, stock_move.product_id  FROM product_product,stock_move
		WHERE product_product.id = stock_move.product_id AND stock_move.id IN 
		(SELECT listado_id FROM corte_listado_rel WHERE pedido_id IN ($documentos)) ORDER BY origin;";
		$result = pg_query($conexion, $query);

		$html = "<!DOCTYPE html>
		<html>
		<script type=\"text/javascript\">
		function changeImg(img, newimg) {
		img.src = newimg;
		}
		</script>
		<style type=\"text/css\">
		<!--
		@import url(\"style.css\");
		-->
		</style>
		<body><table border=\"0\" id=\"newspaper-b\">
		
		<thead><tr><th scope=\"col\">Pedido | Producto</th><th scope=\"col\">Certificado en PDF</th><th scope=\"col\">Enviar por email</th><th></th></tr></thead>
		";
		
		while ($row = pg_fetch_assoc($result)) {
		$mails = direcciones_correo($row['partner_id'],$conexion );
		$certificado = tiene_certificado($row['product_id'],$conexion );
		$mail = mail_enviado_anteriormente($row['id'],$conexion );
		$lista = implode(" , ", $mails);
		$html .= "<tr><td>"  .$row['origin'] ." | " .$row['name_template'] ."</td>
		<td align=\"center\">";
		if (!$certificado) { 
		$html .= "<img src=\"nohay.png\" alt=\"Producto sin datos para certificado\"  height=\"32\" width=\"32\" />";
		} else {
		$html .= "<a href ='certificado.php?stock_move_id=". $row['id'] ."' target=\"_blank\">
		<img src=\"certificado.png\" alt=\"Obtener certificado\"  height=\"32\" width=\"32\" /></a> ";}
		$html .=" </td>
		<td align=\"center\">";
		if (isset($mails['error']) or !$certificado or $mail){
			if ($mail) {
				$lista = " Mail enviado anteriormente | <a href ='certificado.php?mails=ricardo@optimit.com.mx,ricardo_av_ga@hotmail.com&envio_mail=si&stock_move_id=". $row['id'] ."' target=\"_blank\">Volver a enviar</a>" ;
			}
		$html .=  "<td>$lista</td>";
		} else {
		$html .= "<a href ='certificado.php?mails=ricardo@optimit.com.mx,ricardo_av_ga@hotmail.com&envio_mail=si&stock_move_id=". $row['id'] ."' target=\"_blank\">
		<img onclick=\"changeImg(this, 'cargando.gif')\" src=\"mail.png\" alt=\"Enviar por email\"  height=\"32\" width=\"32\" /></a><td>$lista</td>"; }
		$html .= "</td>
		</tr>";
		#$html .= "<a href ='etiqueta.php?stock_move_id=". $row['id'] ."' target=\"_blank\">"  .$row['origin'] .$row['name_template'] ."</a></p>";
		}
		$html .=" 
		</table></body>
		</html>";
		echo $html;
		} else
		
		{
		echo "Sin numero de docuemntos";
		}
