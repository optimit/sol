<?php

function tiene_etiqueta($producto,$conexion ) {
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

//Conexion a BD
require_once('parametros.php');
//Es el ID de la tabla stock_move.
if (isset ($_GET['documentos'])){
	$documentos = $_GET['documentos'];
	$documentos = str_replace('[','',$documentos);
	$documentos = str_replace(']','',$documentos);
$conexion= pg_connect("host=$host port=$port dbname=$dbname user=$user password=$password") 
	   or die ("Nao consegui conectar ao PostGres --> " . pg_last_error($conn)); 
		$query = "SELECT stock_move.id,stock_move.origin,stock_move.cantidad_tambor,
		product_product.name_template, stock_move.partner_id, stock_move.product_id  FROM product_product,stock_move
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
		form input[type=submit] {
			background : url(\"etiqueta.png\") no-repeat center center;
			border : none;
			color : transparent;
			font-size : 0
		}
		</style>
		<body><table border=\"0\" id=\"newspaper-b\">
		
		<thead><tr><th scope=\"col\">Pedido | Producto</th><th scope=\"col\">Lote</th><th scope=\"col\">Cantidad</th><th scope=\"col\">Generar PDF</th></tr></thead>
		";
		
		while ($row = pg_fetch_assoc($result)) {
		$etiqueta = tiene_etiqueta($row['product_id'],$conexion );
		$html .= "<form action=\"etiqueta.php\" target=\"_blank\"><tr><td>"  .$row['origin'] ." | " .$row['name_template'] ."</td>
		<td><input type=\"hidden\" name=\"stock_move_id\" value=\"" .$row['id'] ."\"/>
		<input type=\"text\" name=\"lote\" value=\"" .$row['origin'] ."\"/></td>
		<td><input type=\"text\" name=\"cantidad\" value=\"" .$row['cantidad_tambor'] ."\"/></td>
		<td align=\"center\">";
		if (!$etiqueta) { 
		$html .= "<img src=\"nohay.png\" alt=\"Producto sin datos para etiqueta\"  height=\"32\" width=\"32\" />";
		} else {
		$html .= "<input type=\"image\" src=\"etiqueta.png\" alt=\"Obtener etiquetas\" height=\"32\" width=\"32\"  name=\"submit\" />";}
		$html .=" </td>
		<td align=\"center\">";
		$html .= "</td>
		</tr></form>";
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
