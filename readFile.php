<?php

$pdfText = '';

	//Get database

	$dbConn = new PDO('mysql:dbname=employeeData;host=127.0.0.1;charset=utf8', 'username', 'mypassword',array(PDO::ATTR_PERSISTENT => true));
	$dbConn->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
	$dbConn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

	function getEmployee($employee) {

		global $dbConn;

		$stmt1 = $dbConn->prepare("SELECT employeeName FROM employee WHERE  MATCH (employeeName,surname, otherNames) AGAINST(:employee IN BOOLEAN MODE) LIMIT 1");
		$stmt1->bindValue(':employee', $employee, PDO::PARAM_STR);
		$stmt1->execute();
		while($row1 = $stmt1->fetch()){
			$employeeName = $row1['employeeName'];
		}

		return $employeeName;
	}

	if(isset($_POST['readpdf'])) {
		$extracted_info_list = array();
	
		// Loop through each uploaded file
		foreach ($_FILES['pdf_files']['tmp_name'] as $index => $tmpFile) {
			$fileName = $_FILES['pdf_files']['name'][$index];
			$fileType = pathinfo($fileName, PATHINFO_EXTENSION);
			
			if ($fileType === 'pdf') {
				// Extract information from PDF and add it to the list
				// ...
	
				$extracted_info_list[] = $extracted_info;
			}
		}
	
		// Return extracted information as JSON response
		header('Content-Type: application/json');
		echo json_encode($extracted_info_list);
	}
	

// Display text content
	//Get Client
	if(strpos($pdfText, "\n") !== FALSE) {
		$clientEnd  = strpos($pdfText, "\n");
	}else {
		$clientEnd = 100;
	}
	echo $client = substr($pdfText,0, $clientEnd);

	echo "<p> -----------Report Date-----------<p>";
	//Get report Date
	$dateStart = stripos($pdfText,"JAM Daily Report");
	$dateText = substr($pdfText,$dateStart);

	//Get length of first line for deletion
	if(strpos($dateText, "\n") !== FALSE) {
		$dateLine1End  = strpos($dateText, "\n");
	}else {
		$dateLine1End = $dateStart + 100;
	}

	$dateText = substr($dateText,$dateLine1End+1);

	//Get length of next line
	if(strpos($dateText, "\n") !== FALSE) {
		$dateEnd  = strpos($dateText, "\n");
	}else {
		$dateEnd = 100;
	}

	echo $dateText = substr($dateText,0,$dateEnd);

	//Start work on splitting to obtain data
	$dateData= explode(" ",$dateText);
	$date = $dateData[2].$dateData[3].$dateData[4];

	echo "<p> ---------Contractors-------------<p>";

	$peopleStart = strpos($pdfText,"NOTES");
	$peopleText = substr($pdfText,$peopleStart);
	$peopleEnd = strpos($peopleText,"PHOTO");

	if($peopleEnd == 0){
		$peopleEnd = 1000;
	}

	$peopleText = substr($pdfText,$peopleStart,$peopleEnd);

	if(strpos($peopleText, "\n") !== FALSE) {
		$peopleLine1End  = strpos($peopleText, "\n");
	}else {
		$peopleLine1End = $dateStart + 100;
	}

	$peopleText = substr($peopleText,$peopleLine1End+1);
	$peopleLength = strlen($peopleText);

	$i = $error = 0;
	$peopleLineText = $peopleText;

	while($i<$peopleLength){

		if(strpos($peopleLineText, "\n") !== FALSE) {
			$peopleLine1End  = strpos($peopleLineText, "\n");
		}else {
			$peopleLine1End = $dateStart + 100;
		}

		echo $peopleData = substr($peopleLineText,0,$peopleLine1End);

		$data = explode(" ",$peopleData);
		$dataLength = count($data);
		$name = $remarks = "";
		$hours = 0;
		// loop through the array

		for($i = 0; $i < $dataLength; $i++) {
			//Look for a number
			$numbers = $data[$i];

			try{
				if(is_numeric($numbers)){
					$hours = $data[$i];
					$nameID = $i;
					$error = 0;
				}
			}catch(exception $e){
				error_log("Numeric error" .$e);
				$error = 1;
			}
		}

		//Get name
		for($i = 0; $i < $nameID; $i++) {
			$name .= $data[$i]. " ";
		}

			//Get remarks
			for($i = $nameID+1; $i < $dataLength; $i++) {
				$remarks .= $data[$i]. " ";
			}

		$employee = getEmployee($name);

		$nameCompare = similar_text($name, $employee, $perc);


		echo "Name: " .$name."<br>";
		echo "DB Name: " .$employee."<br>";
		echo "similarity: $nameCompare ($perc %) <br>";
		echo "Hours: " .$hours."<br>";
		echo "Remarks: " .$remarks."<br>";



		echo "----------------------<p>";

		$peopleLineText = substr($peopleLineText,$peopleLine1End+1);
		$i += $peopleLine1End+1;

	}

?>
