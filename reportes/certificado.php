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

if (isset ($_GET['envio_mail'])){
	if ($_GET['envio_mail'] == 'si'){
		if (isset ($_GET['mails'])){
		$envio_mail = True;
		$mails_envio = $_GET['mails'];
		} else {
		$envio_mail = False;
		}
	} else  {
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
		$query = "SELECT stock_move.name, product_laboratorio.lote,stock_move.origin, aprobado_por, notas, analisis,observaciones,stock_move.partner_id,
		stock_move.id,
		product_laboratorio.metodo_1, product_laboratorio.analisis_1, product_laboratorio.resultado_1, product_laboratorio.especificacion_1,
		product_laboratorio.metodo_2,product_laboratorio.analisis_2,product_laboratorio.resultado_2,product_laboratorio.especificacion_2,
		product_laboratorio.metodo_3,product_laboratorio.analisis_3,product_laboratorio.resultado_3,product_laboratorio.especificacion_3,
		product_laboratorio.metodo_4,product_laboratorio.analisis_4,product_laboratorio.resultado_4,product_laboratorio.especificacion_4,
		product_laboratorio.metodo_5,product_laboratorio.analisis_5,product_laboratorio.resultado_5,product_laboratorio.especificacion_5,
		product_laboratorio.metodo_6,product_laboratorio.analisis_6,product_laboratorio.resultado_6,product_laboratorio.especificacion_6,
		product_laboratorio.metodo_7,product_laboratorio.analisis_7,product_laboratorio.resultado_7,product_laboratorio.especificacion_7,
		product_laboratorio.metodo_8,product_laboratorio.analisis_8,product_laboratorio.resultado_8,product_laboratorio.especificacion_8,
		product_laboratorio.metodo_9,product_laboratorio.analisis_9,product_laboratorio.resultado_9,product_laboratorio.especificacion_9,
		product_laboratorio.metodo_10,product_laboratorio.analisis_10,product_laboratorio.resultado_10,product_laboratorio.especificacion_10,
		product_laboratorio.metodo_11,product_laboratorio.analisis_11,product_laboratorio.resultado_11,product_laboratorio.especificacion_11,
		product_laboratorio.metodo_12,product_laboratorio.analisis_12,product_laboratorio.resultado_12,product_laboratorio.especificacion_12,
		product_laboratorio.metodo_13,product_laboratorio.analisis_13,product_laboratorio.resultado_13,product_laboratorio.especificacion_13,
		product_laboratorio.metodo_14,product_laboratorio.analisis_14,product_laboratorio.resultado_14,product_laboratorio.especificacion_14,
		product_laboratorio.metodo_15,product_laboratorio.analisis_15,product_laboratorio.resultado_15,product_laboratorio.especificacion_15,
		product_laboratorio.metodo_16,product_laboratorio.analisis_16,product_laboratorio.resultado_16,product_laboratorio.especificacion_16,
		product_laboratorio.metodo_17,product_laboratorio.analisis_17,product_laboratorio.resultado_17,product_laboratorio.especificacion_17
		FROM product_laboratorio,product_product,stock_move 
		WHERE product_laboratorio.name = product_product.id AND product_product.id = stock_move.product_id AND stock_move.id IN 
		($stock_move_id);";
		$result = pg_query($conexion, $query);

		while ($row = pg_fetch_assoc($result)) {

// Extend the TCPDF class to create custom Header and Footer
			class MYPDF extends TCPDF {


				// Page footer
				public function Footer() {
					// Position at 15 mm from bottom
					$this->SetY(-15);
					// Set font
					$this->SetFont('helvetica', 'I', 8);
					// Page number
					$this->Cell(0, 10, 'Este Certificado de Analisis es emitido electronicamente y es valido sin ninguna firma', 0, false, 'C', 0, '', 0, false, 'T', 'M');
				}
			}
				// create new PDF document
				$pdf = new MYPDF(PDF_PAGE_ORIENTATION, PDF_UNIT, PDF_PAGE_FORMAT, true, 'UTF-8', false);
				// set document information
				$pdf->SetCreator(PDF_CREATOR);
				$pdf->SetAuthor('Solvmex S.A.');
				$pdf->SetTitle('Certificado de analisis quimico');
				$pdf->SetSubject('Solvmex certificado de analisis');
				$dias = array("Domingo","Lunes","Martes","Miercoles","Jueves","Viernes","Sábado");
				$meses = array("Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre");

				$fecha = $dias[date('w')]." ".date('d')." de ".$meses[date('n')-1]. " del ".date('Y');
				// set default header data
				$pdf->SetHeaderData('logo_solvmex.jpg', PDF_HEADER_LOGO_WIDTH, 'Certificado de Analisis Quimico', 'Solvmex S.A. | laboratorio@solvmex.com.mx | Impresion: ' .$fecha, array(0,64,255), array(0,64,128));
				$pdf->setFooterData($tc=array(0,64,0), $lc=array(0,64,128));
				// set header and footer fonts
				$pdf->setHeaderFont(Array(PDF_FONT_NAME_MAIN, '', PDF_FONT_SIZE_MAIN));
				$pdf->setFooterFont(Array(PDF_FONT_NAME_DATA, '', PDF_FONT_SIZE_DATA));

				// set default monospaced font
				$pdf->SetDefaultMonospacedFont(PDF_FONT_MONOSPACED);

				//set margins
				$pdf->SetMargins(PDF_MARGIN_LEFT, PDF_MARGIN_TOP, PDF_MARGIN_RIGHT);
				$pdf->SetHeaderMargin(PDF_MARGIN_HEADER);
				$pdf->SetFooterMargin(PDF_MARGIN_FOOTER);

				//set auto page breaks
				$pdf->SetAutoPageBreak(TRUE, PDF_MARGIN_BOTTOM);

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
			$pdf->AddPage();
			



			// Set some content to print
			$stock_move_id = $row['id'];
			$partner_id = $row['partner_id'];
			$Nombre_producto = $row['name'];
			$Lote_producto = $row['lote'];
			$Fac_producto = $row['origin'];
			$des = "585 mmHg.";

			$html = "
			<style>
				table.first {
					color: #003300;
					font-family: helvetica;
					font-size: 12pt;
					border: 1x ;
					background-color: #D8D8D8;
				}
				table.sec {
					padding-top:5px;
					padding-bottom:5px;
					font-family: helvetica;
					font-size: 10pt;
				}
				table.detalles {
					font-family: helvetica;
					font-size: 8pt;
					border: 0x ;
				}
				table.encabezado {
					font-family: helvetica;
					font-size: 10pt;
				}
				td.second {
					font-size: 7pt;
				}
			</style>
			<table width=\"100%\" cellpadding=\"1\"  class = \"encabezado\">
			<tr><td>Producto:</td><td>$Nombre_producto</td> 
			<td>Lote:</td><td><hd>$Lote_producto</td></tr>
			<tr><td>Pedido no.</td><td>$Fac_producto</td><td>Aprobado por</td><td>".$row['aprobado_por']."</td></tr>
			</table>
			<br />
			<table class = \"sec\" border=\"0\" width=\"100%\"  >
			<tr>
			<td colspan=\"4\" >" .$row['analisis'] ." </td>
			</tr>
			</table>
			</br>
			<table class = \"first\"  border=\"1\" width=\"100%\" cellpadding=\"1\" >
			<tr>
			<th width=\"40%\">An&aacute;lisis</th>
			<th width=\"20%\">M&eacute;todo</th>
			<th width=\"20%\">Resultado</th>
			<th width=\"20%\">Especificaci&oacute;n</th>
			</tr>
			</table>
			<table class=\"detalles\" border=\"0\" width=\"100%\" cellpadding=\"1\" >
			<tr><td class=\"second\" colspan=\"4\" ></td></tr>
			<tr>
			<td width=\"40%\">" .$row['analisis_1'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['metodo_1'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['resultado_1'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['especificacion_1'] ."</td>
			</tr>
			<tr><td class=\"second\" colspan=\"4\" ></td></tr>
			<tr>
			<td width=\"40%\">" .$row['analisis_2'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['metodo_2'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['resultado_2'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['especificacion_2'] ."</td>
			</tr>
			<tr><td class=\"second\" colspan=\"4\" ></td></tr>
			<tr>
			<td width=\"40%\">" .$row['analisis_3'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['metodo_3'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['resultado_3'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['especificacion_3'] ."</td>
			</tr>
			<tr><td class=\"second\" colspan=\"4\" ></td></tr>
			<tr>
			<td width=\"40%\">" .$row['analisis_4'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['metodo_4'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['resultado_4'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['especificacion_4'] ."</td>
			</tr>
			<tr><td class=\"second\" colspan=\"4\" ></td></tr>
			<tr>
			<td width=\"40%\">" .$row['analisis_5'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['metodo_5'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['resultado_5'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['especificacion_5'] ."</td>
			</tr>
			<tr><td class=\"second\" colspan=\"4\" ></td></tr>
			<tr>
			<td width=\"40%\">" .$row['analisis_6'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['metodo_6'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['resultado_6'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['especificacion_6'] ."</td>
			</tr>
			<tr><td class=\"second\" colspan=\"4\" ></td></tr>
			<tr>
			<td width=\"40%\">" .$row['analisis_7'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['metodo_7'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['resultado_7'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['especificacion_7'] ."</td>
			</tr>
			<tr><td class=\"second\" colspan=\"4\" ></td></tr>
			<tr>
			<td width=\"40%\">" .$row['analisis_8'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['metodo_8'] ."</td>
			<td width=\"20%\"  align=\"center\">" .$row['resultado_8'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['especificacion_8'] ."</td>
			</tr>
			<tr><td class=\"second\" colspan=\"4\" ></td></tr>
			<tr>
			<td width=\"40%\">" .$row['analisis_9'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['metodo_9'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['resultado_9'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['especificacion_9'] ."</td>
			</tr>
			<tr><td class=\"second\" colspan=\"4\" ></td></tr>
			<tr>
			<td width=\"40%\">" .$row['analisis_10'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['metodo_10'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['resultado_10'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['especificacion_10'] ."</td>
			</tr>
			<tr><td class=\"second\" colspan=\"4\" ></td></tr>
			<tr>
			<td width=\"40%\">" .$row['analisis_11'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['metodo_11'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['resultado_11'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['especificacion_11'] ."</td>
			</tr>
			<tr><td class=\"second\" colspan=\"4\" ></td></tr>
			<tr>
			<td width=\"40%\">" .$row['analisis_12'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['metodo_12'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['resultado_12'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['especificacion_12'] ."</td>
			</tr>
			<tr><td class=\"second\" colspan=\"4\" ></td></tr>
			<tr>
			<td width=\"40%\">" .$row['analisis_13'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['metodo_13'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['resultado_13'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['especificacion_13'] ."</td>
			</tr>
			<tr><td class=\"second\" colspan=\"4\" ></td></tr>
			<tr>
			<td width=\"40%\">" .$row['analisis_14'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['metodo_14'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['resultado_14'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['especificacion_14'] ."</td>
			</tr>
			<tr><td class=\"second\" colspan=\"4\" ></td></tr>
			<tr>
			<td width=\"40%\">" .$row['analisis_15'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['metodo_15'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['resultado_15'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['especificacion_15'] ."</td>
			</tr>
			<tr><td class=\"second\" colspan=\"4\" ></td></tr>
			<tr>
			<td width=\"40%\">" .$row['analisis_16'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['metodo_16'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['resultado_16'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['especificacion_16'] ."</td>
			</tr>
			<tr><td class=\"second\" colspan=\"4\" ></td></tr>
			<tr>
			<td width=\"40%\">" .$row['analisis_17'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['metodo_17'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['resultado_17'] ."</td>
			<td width=\"20%\" align=\"center\">" .$row['especificacion_17'] ."</td>
			</tr>
			<tr><td class=\"second\" colspan=\"4\" ></td></tr>
			</table>
			<br />
			<table border=\"0\" width=\"100%\" >
			<tr>
			<td width=\"20%\"><h6>Observaciones:</h6></td>
			<td width=\"80%\"><h6>".$row['observaciones']."</h6></td>
			</tr>
			<br />
			<tr>
			<td width=\"5%\"></td>
			<td width=\"20%\"><h6>Nota:</h6></td>
			<td width=\"25%\"><h6>".$row['notas']."</h6></td>
			</tr>
			</table>
			";

			// Print text using writeHTMLCell()
			#$pdf->writeHTMLCell($w=0, $h=0, $x='', $y='', $html, $border=0, $ln=1, $fill=0, $reseth=true, $align='', $autopadding=true);
			$pdf->writeHTML($html, true, false,false,false,'left');

			// ---------------------------------------------------------

			// Close and output PDF document
			// This method has several options, check the source code documentation for more information.
			$nombre_archivo = $Fac_producto ."-" .$Nombre_producto;
			if ($envio_mail) {

			$fileatt = $pdf->Output("$nombre_archivo.pdf", 'F');
			$data = chunk_split($fileatt);
			$from = "Solvmex S.A.<administrador@solvmex.com.mx>";
			$responder_a = "Solvmex S.A. Laboratorio<laboratorio@solvmex.com.mx>";
			$to = $mails_envio;
			#$to = "ricardo@optimit.com.mx, ricardo_avila@prodigy.net.mx";
			$subject = $Fac_producto ." | Certificado de analisis para " .$Nombre_producto ." Solvmex S.A.";
			$host = "ssl://smtp.gmail.com";
			$port = "465";
			$username = "administrador@solvmex.com.mx";
			$password = "sol12257";
			$message = new Mail_mime();
			$message->setTXTBody("Certificado de analisis \n $Fac_producto  - $Nombre_producto;");
			$message->addAttachment("$nombre_archivo.pdf");
			$body = $message->get();
			$extraheaders = array("From" => $from, "To" => $to, "Subject"=>$subject,"Reply-To"=>$responder_a);
			$headers = $message->headers($extraheaders);
			$mail = Mail::factory('smtp',
			  array ('host' => $host,
				'port' => $port,
				'auth' => true,
				'username' => $username,
				'password' => $password));
			$mail->send($to, $headers, $body);
			@unlink("$nombre_archivo.pdf"); 
			unset($pdf); 
			echo "Email enviado correctamente " ." | " .$to ;
			$query = "INSERT INTO mail_message( create_uid, create_date, auto_delete,  email_to, email_from, date, partner_id, subject,  
            subtype, state, reply_to, model, res_id)
            VALUES (1,now(),FALSE,'$to','$from',now(),'$partner_id','$subject ','html','sent','$responder_a','stock.move',$stock_move_id);";
			$envio_email = pg_query($conexion, $query);
			} else {
			$pdf->Output('CAQ.pdf', 'I');
			}


} // Cierra while que obtiene los registros de la BD

} else {
echo "No especifico un certificado";
}
//============================================================+
// END OF FILE
//============================================================+
