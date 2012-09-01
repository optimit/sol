<?php
//============================================================+
// File name   : example_001.php
// Begin       : 2008-03-04
// Last Update : 2010-08-14
//
// Description : Example 001 for TCPDF class
//               Default Header and Footer
//
// Author: Nicola Asuni
//
// (c) Copyright:
//               Nicola Asuni
//               Tecnick.com LTD
//               Manor Coach House, Church Hill
//               Aldershot, Hants, GU12 4RQ
//               UK
//               www.tecnick.com
//               info@tecnick.com
//============================================================+

require_once('tcpdf/config/lang/eng.php');
require_once('tcpdf/tcpdf.php');
//Conexion a BD
require_once('parametros.php');
require_once "Mail.php";
require_once "Mail/mime.php";
if (isset ($_GET['cantidad'])){
$cantidad = $_GET['cantidad'];
} else {
$cantidad = 1;
}
if (isset ($_GET['envio_mail'])){
	if ($_GET['envio_mail'] == 'si'){
		$envio_mail = True;
	} else {
		$envio_mail = False;
	}
} else {
	$envio_mail = False;
}
//Es el ID de la tabla stock_move.
if (isset ($_GET['stock_move_id'])){
	$stock_move_id = $_GET['stock_move_id'];
$conexion= pg_connect("host=$host port=$port dbname=$dbname user=$user password=$password") 
	   or die ("Nao consegui conectar ao PostGres --> " . pg_last_error($conn)); 
		$query = "SELECT stock_move.name, product_laboratorio.lote,stock_move.origin, toxicidad, incendio, reactividad,epp, 
		product_product.capacidad_kg,product_product.capacidad_lt,product_product.default_code
		FROM product_laboratorio,product_product,stock_move 
		WHERE product_laboratorio.name = product_product.id AND product_product.id = stock_move.product_id AND stock_move.id IN 
		($stock_move_id);";
		$result = pg_query($conexion, $query);

		while ($row = pg_fetch_assoc($result)) {
				// create new PDF document
				$pdf = new TCPDF(PDF_PAGE_ORIENTATION, PDF_UNIT, array(120,100), true, 'UTF-8', false);
				
				// set document information
				$pdf->SetCreator(PDF_CREATOR);
				//$pdf->SetAuthor('Solvmex S.A.');
				//$pdf->SetTitle('Etiqueta');
				//$pdf->SetSubject('Etiqueta');
				//$dias = array("Domingo","Lunes","Martes","Miercoles","Jueves","Viernes","Sábado");
				//$meses = array("Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre");

				//$fecha = $dias[date('w')]." ".date('d')." de ".$meses[date('n')-1]. " del ".date('Y');
				// set default header data
				//$pdf->SetHeaderData('', PDF_HEADER_LOGO_WIDTH, '', '' , array(0,64,255), array(0,64,128));
				// set header and footer fonts
				//$pdf->setHeaderFont(Array(PDF_FONT_NAME_MAIN, '', 7));
				

				// set default monospaced font
				$pdf->SetDefaultMonospacedFont(PDF_FONT_MONOSPACED);

				//set margins
				$pdf->SetMargins(0,15,0);
				$pdf->SetHeaderMargin(2);
				
			
				//set auto page breaks
				$pdf->SetAutoPageBreak(TRUE, 5);

				//set image scale factor
				$pdf->setImageScale(PDF_IMAGE_SCALE_RATIO);

				//set some language-dependent strings
				$pdf->setLanguageArray($l);

				// ---------------------------------------------------------

				// set default font subsetting mode
				$pdf->setFontSubsetting(true);

				// Set font
				// dejavusans is a UTF-8 Unicode font, if you only need to
				// print standard ASCII chars, you can use core fonts like
				// helvetica or times to reduce file size.
				$pdf->SetFont('dejavusans', '', 12, '', true);
			// Add a page
			// This method has several options, check the source code documentation for more information.
			for($i = 0; $i < $cantidad; ++$i) {
			$pdf->AddPage();
			// Set some content to print
			$Name =  $row['name'];
			$toxicidad = $row['toxicidad'];
			$incendio =  $row['incendio'];
			$reactividad =  $row['reactividad'];
			$epp =  $row['epp'];
			$cod = "UN 1993";
			$cant = $row['capacidad_lt'];
			$peson = $row['capacidad_kg'];
			$clave = $row['default_code'];
			$lote = $row['lote'];
			

			$html = "
			<style>
				td.title {
					font-size: 22pt;
					text-align: center;
				}
				td.tox {
					font-size: 18pt;
					text-align: center;
				}
				td.inc {
					font-size: 18pt;
					text-align: center;
				}
				td.rea {
					font-size: 18pt;
					text-align: center;
				}
				td.epp {
					font-size: 18pt;					
					text-align: center;
				}
				table.cent {										
					text-align: center;
					font-size: 18pt;
				}
				table.centi {										
					text-align: center;
					font-size: 8pt;
				}
				td.left {
					font-size: 10pt;					
					text-align: left;
				}
			</style>
			<table class=\"cent\" width='100%' border=\"0\" cellpadding='1'>
			<tr><td class=\"title\" colspan=\"3\" >$Name</td></tr>
			<tr><td  class=\"left\" colspan=\"3\" ></td></tr>
			<tr><td class=\"tox\" colspan=\"2\" ></td><td >$toxicidad</td></tr>
			<tr><td class=\"inc\" colspan=\"2\" ></td><td>$incendio</td></tr>
			<tr><td  class=\"left\" colspan=\"3\" ></td></tr>
			<tr><td class=\"rea\" colspan=\"2\" ></td><td>$reactividad</td></tr>
			<tr><td class=\"epp\" colspan=\"2\" ></td><td class=\"cent\">$epp</td></tr>
			<tr><td class=\"left\"></td><td class=\"left\"></td><td class=\"left\"></td></tr>
			<tr><td>$cod</td><td>$cant</td><td>$peson</td></tr>
			<tr><td class=\"left\"></td><td class=\"left\"></td><td class=\"left\"></td></tr>
			<tr><td>$clave</td><td></td><td></td></tr>
			<tr><td class=\"left\" colspan=\"3\"></td></tr>
			<tr><td class=\"left\" colspan=\"3\"></td></tr>
			<tr><td colspan=\"3\">$lote</td></tr>			
			</table>
";
			
			

			// Print text using writeHTMLCell()
			$pdf->writeHTMLCell($w=0, $h=0, $x='', $y='', $html, $border=0, $ln=0, $fill=0, $reseth=true, $align='', $autopadding=true);
			//$pdf->writeHTML($html, true, false,false,false,'left');
			} // Cierra for para muchas etiquetas
			$pdf->Output("Etiqueta-$Name.pdf", "I");
			// ---------------------------------------------------------


} // cierra while para cada producto dentro del corte

} else {
echo "No hay documentos";
}
//============================================================+
// END OF FILE
//============================================================+
