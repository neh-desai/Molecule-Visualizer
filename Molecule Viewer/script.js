$(document).ready(
	/* this defines a function that gets called after the document is in memory */
	function() {
		$.get("/information", function(data) {
			var arr = []
			$('#Removing').empty();
			if (data.length > 0) {
				arr = data.split(" ")
				var len = arr.length
				for (let i = 0; i < len; i++) {
					$("#Removing").append("<option>" + arr[i] + "</option>");
				}
			}
		});
		$.get("/atomandbondNum", function(data) {
			var arr = []
			var arr2 = []
			arr = data.split("\n")
			var len = arr.length
			$('#DisplayM').empty();
			for (let i = 0; i < len - 1; i++) {
				arr2 = arr[i].split(" ")
				$("#DisplayM").append("<option>" + arr2[0] + " " + "Atom #: " + arr2[1] + " Bond #: " + arr2[2] + "</option>");
			}
		});
		$("#Add").click(
			/* function that gets called when button 2 is clicked */
			function() {
				var validateEcode = 0;
				var check = true
				var changeEnum = false;
				var changeEcode = false;
				var changeEname = false;
				var changeC1 = false;
				var changeC2 = false;
				var changeC3 = false;
				var changerad = false;
				var Enum = parseInt(document.getElementById('Enum').value)
				var Ecode = document.getElementById('Ecode').value
				var Ename = document.getElementById('Ename').value
				var C1 = document.getElementById('Ec1').value
				var C2 = document.getElementById('Ec2').value
				var C3 = document.getElementById('Ec3').value
				var rad = parseFloat(document.getElementById('Erad').value)
				$.get("/infoEcode", function(data) {
					var codes = []
					if (data.length > 0) {
						codes = data.split(" ")
						if (jQuery.inArray(Ecode, codes) == -1) {
							//No match found so valid
							validateEcode = 0;
						} else {
							validateEcode = 1;
						}
					}
					//Add eror check
					if (validateEcode == 0) {
						if (Enum <= 0 || Enum > 118 || !$.trim($("#Enum").val())) {
							// $('#Enum').val('');
							check = false
							changeEnum = true
						}
						if (!$.trim($("#Ecode").val()) || $("#Ecode").val().length > 3) {
							check = false
							changeEcode = true
						}
						if (!$.trim($("#Ename").val()) || $("#Ename").val().length > 32) {
							check = false
							changeEname = true
						}
						if (!$.trim($("#Ec1").val()) || $("#Ec1").val().length < 6) {
							check = false
							changeC1 = true
						}
						if (!$.trim($("#Ec2").val()) || $("#Ec2").val().length < 6) {
							check = false
							changeC2 = true
						}
						if (!$.trim($("#Ec3").val()) || $("#Ec3").val().length < 6) {
							check = false
							changeC3 = true
						}
						if (rad <= 0 || rad > 999 || !$.trim($("#Erad").val())) {
							check = false
							changerad = true
						}
						if (check) {
							alert("You have entered everthing correctly. Good Job!");
							$("#Enum").css('border-color', 'black');
							$("#Ecode").css('border-color', 'black');
							$("#Ename").css('border-color', 'black');
							$("#Ec1").css('border-color', 'black');
							$("#Ec2").css('border-color', 'black');
							$("#Ec3").css('border-color', 'black');
							$("#Erad").css('border-color', 'black');
							// addOption()
							molObject = {
								"Enum": Enum,
								"Ecode": Ecode,
								"Ename": Ename,
								"C1": C1,
								"C2": C2,
								"C3": C3,
								"rad": rad
							}
							$.ajax({
								type: "POST",
								url: "/add",
								data: JSON.stringify(molObject),
								datatype: "json"
							})
							$.get("/information", function(data) {
								var arr = []
								arr = data.split(" ")
								var len = arr.length
								$('#Removing').empty();
								for (let i = 0; i < len; i++) {
									$("#Removing").append("<option>" + arr[i] + "</option>");
								}

							});
						}
						//If check is false or !check
						else {
							alert("Error! You have made a mistake in one of the fields that have been highlighed. Please reivew them and input again. Thanks!")
							if (changeEnum) {
								$("#Enum").css('border-color', 'red');
							} else {
								$("#Enum").css('border-color', 'black');
							}
							if (changeEcode) {
								$("#Ecode").css('border-color', 'red');
							} else {
								$("#Ecode").css('border-color', 'black');
							}
							if (changeEname) {
								$("#Ename").css('border-color', 'red');
							} else {
								$("#Ename").css('border-color', 'black');
							}
							if (changeC1) {
								$("#Ec1").css('border-color', 'red');
							} else {
								$("#Ec1").css('border-color', 'black');
							}
							if (changeC2) {
								$("#Ec2").css('border-color', 'red');
							} else {
								$("#Ec2").css('border-color', 'black');
							}
							if (changeC3) {
								$("#Ec3").css('border-color', 'red');
							} else {
								$("#Ec3").css('border-color', 'black');
							}
							if (changerad) {
								$("#Erad").css('border-color', 'red');
							} else {
								$("#Erad").css('border-color', 'black');
							}
						}
					} else {
						alert("Your Element Code Already Exists Type another one")
					}
				});
			});

		$("#Remove").click(
			/* function that gets called when button 2 is clicked */
			function() {
				var userEname = document.getElementById('Removing').value
				if (userEname.length === 0) {
					alert("Cannot remove an element as there are none currently available. Please Try Again")
				} else {
					$.ajax({
						type: "POST",
						url: "/delete",
						data: userEname,
						datatype: "text",
						success: function() {
							$.get("/information", function(data) {
								var arr = []
								arr = data.split(" ")
								var len = arr.length
								$('#Removing').empty();
								for (let i = 0; i < len; i++) {
									$("#Removing").append("<option>" + arr[i] + "</option>");
								}
							});

						}
					})
				}
			});

		$("#UploadButton").click(
			/* function that gets called when button 2 is clicked */
			function() {
				var fName = document.getElementById('sdf_file').value
				var moluser = document.getElementById('userName').value
				if (fName.length === 0 && moluser.length === 0) {
					alert("You have not uploaded a file and you have not named your molecule. Please review those fields and try again.")
					$("#userName").css('border-color', 'red');
					$("#fileBorder").css('border-color', 'red');
				} else if (fName.length === 0) {
					alert("You have not added an SDF file to be uploaded. Please add one to upload your molecule.")
					$("#fileBorder").css('border-color', 'red');
					$("#userName").css('border-color', 'black');

				} else if (moluser.length === 0) {
					alert("You have not added a name for your molecule. Please add one so you can upload your molecule. ")
					$("#userName").css('border-color', 'red');
					$("#fileBorder").css('border-color', 'black');
				} else {
					$("#userName").css('border-color', 'black');
					$("#fileBorder").css('border-color', 'black');
					var arr = []
					arr = fName.split("\\")
					extension = arr[2].split(".")
					filename = arr[2]
					if (extension[1] === "sdf") {
						$.get("/MolExistOrNot", function(data) {

							var userVal = document.getElementById('userName').value
							var names = []
							names = data.split(" ")
							if (jQuery.inArray(userVal, names) == -1) {
								//No match found so valid
								validateMName = 0;
							} else {
								validateMName = 1;
							}

							if (validateMName == 0) {
								alert("Your File Has Been Uploaded succesfully with your name. Woho!")
								//do a post req to get append to display list along with atom num and bond num of the molecule
								displayObject = {
									"userVal": userVal,
									"fileName": filename
								}
								$.ajax({
									type: "POST",
									url: "/UploaduserMol",
									data: JSON.stringify(displayObject),
									datatype: "json",
									success: function() {
										$.get("/atomandbondNum", function(data) {
											var arr = []
											var arr2 = []
											arr = data.split("\n")
											var len = arr.length
											$('#DisplayM').empty();
											for (let i = 0; i < len - 1; i++) {
												arr2 = arr[i].split(" ")
												$("#DisplayM").append("<option>" + arr2[0] + " " + "Atom #: " + arr2[1] + " Bond #: " + arr2[2] + "</option>");
											}
										});
									}
								})
							} else if (validateMName == 1) {
								alert("Your Molecule name is not valid as it is empty or already exists. Please input again.")
							}
						});
					} else {
						alert("The file you are uploading is not valid. Please Check Your Extension. Thanks!")
						$("#fileBorder").css('border-color', 'red');
					}
				}
			});

		$("#Display").click(function() {
			var userSelect = document.getElementById('DisplayM').value
			var arr = []
			arr = userSelect.split(" ")
			sessionStorage.setItem("current", arr[0]);
			if (userSelect.length === 0) {
				alert("You have not uploaded a molecule and selected it to be displayed. Please review those fields and add that information. ")
			} else {
				locations()
			}
		});

		$("#X").click(function() {
			var rotateVal = document.getElementById('rotateNum').value
			parsed = parseInt(rotateVal)
			var currentOption = sessionStorage.getItem('current')
			if (rotateVal.length === 0 || (rotateVal.length === 1 && rotateVal === '-')) {
				alert("You have not added a rotation value. Please add one so your molecule can be rotated.")
				$("#rotateNum").css('border-color', 'red');
			}  
			else if (parsed === 0 || parsed === -360 || parsed === 360){
				loadMol()
			}
			else if (parsed < -360 || parsed > 360) {
				alert("The rotation value you has entered is not in the range of a valid value. Please enter again.")
				$("#rotateNum").css('border-color', 'red');
			} else {
				$("#rotateNum").css('border-color', 'black');
				$.post("/Xrotate",
					/* pass a JavaScript dictionary */
					{
						"rotateVal": rotateVal,
						/* retreive value of name field */
						"userMol": currentOption
					},
					function(data) {
						let svg = data
						let blob = new Blob([svg], {
							type: 'image/svg+xml'
						})
						let url = URL.createObjectURL(blob)
						let image = document.getElementById("showImg")
						image.src = url;
						image.addEventListener('load', () => URL.revokeObjectURL(url), {
							once: true
						});
					}
				);
			}
		});

		$("#Y").click(function() {
			var rotateVal = document.getElementById('rotateNum').value
			var currentOption = sessionStorage.getItem('current')
			parsed = parseInt(rotateVal)
			if (rotateVal.length === 0 || (rotateVal.length === 1 && rotateVal === '-')) {
				alert("You have not added a rotation value. Please add one so your molecule can be rotated.")
				$("#rotateNum").css('border-color', 'red');
			} else if (parsed === 0 || parsed === -360 || parsed === 360){
				loadMol()
			} else if (parsed < -360 || parsed > 360) {
				alert("The rotation value you has entered is not in the range of a valid value. Please enter again.")
				$("#rotateNum").css('border-color', 'red');
			} else {
				$("#rotateNum").css('border-color', 'black');
				$.post("/Yrotate",
					/* pass a JavaScript dictionary */
					{
						"rotateVal": rotateVal,
						/* retreive value of name field */
						"userMol": currentOption
					},
					function(data) {
						let svg = data
						let blob = new Blob([svg], {
							type: 'image/svg+xml'
						})
						let url = URL.createObjectURL(blob)
						let image = document.getElementById("showImg")
						image.src = url;
						image.addEventListener('load', () => URL.revokeObjectURL(url), {
							once: true
						});
					}
				);
			}
		});

		$("#Z").click(function() {
			var rotateVal = document.getElementById('rotateNum').value
			var currentOption = sessionStorage.getItem('current')
			parsed = parseInt(rotateVal)
			if (rotateVal.length === 0 || (rotateVal.length === 1 && rotateVal === '-')) {
				alert("You have not added a rotation value. Please add one so your molecule can be rotated.")
				$("#rotateNum").css('border-color', 'red');
			} else if (parsed === 0 || parsed === -360 || parsed === 360){
				loadMol()
			} else if (parsed < -360 || parsed > 360) {
				alert("The rotation value you has entered is not in the range of a valid value. Please enter again.")
				$("#rotateNum").css('border-color', 'red');
			} else {
				$("#rotateNum").css('border-color', 'black');
				$.post("/Zrotate",
					/* pass a JavaScript dictionary */
					{
						"rotateVal": rotateVal,
						/* retreive value of name field */
						"userMol": currentOption
					},
					function(data) {
						let svg = data
						let blob = new Blob([svg], {
							type: 'image/svg+xml'
						})
						let url = URL.createObjectURL(blob)
						let image = document.getElementById("showImg")
						image.src = url;
						image.addEventListener('load', () => URL.revokeObjectURL(url), {
							once: true
						});
					}
				);
			}
		});
	});


function checkInput(text) {
	var regex = /[^a-z]/gi;
	text.value = text.value.replace(regex, "");
}

function checkInput2(text) {
	var regex = /[^a-fA-F0-9]/gi
	text.value = text.value.replace(regex, "");
}

function checkEnum(text) {
	var regex = /[^0-9]\d*$/gi;
	text.value = text.value.replace(regex, "");
}

function locations() {
	//var id=20; get the value of id and save in id(getElementById or jquery) 
	window.location.href = 'next.html';
}

function loadMol() {
	var currentOption = sessionStorage.getItem('current')
	$.post("/mol",
		/* pass a JavaScript dictionary */
		{
			"userMol": currentOption,
			/* retreive value of name field */
		},
		function(data) {
			//ADD error statment of empty and dont do post
			let svg = data
			let blob = new Blob([svg], {
				type: 'image/svg+xml'
			})
			let url = URL.createObjectURL(blob)
			let image = document.getElementById("showImg")
			image.src = url;
			image.addEventListener('load', () => URL.revokeObjectURL(url), {
				once: true
			});
		}
	);
}