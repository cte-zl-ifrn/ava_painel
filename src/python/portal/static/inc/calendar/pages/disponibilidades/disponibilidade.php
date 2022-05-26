
<!DOCTYPE html>
<html lang="en">
    <head>
    <meta charset="utf-8" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
        <meta name="description" content="" />
        <meta name="author" content="" />
        <link href="../../dist/css/styles.css" rel="stylesheet" />
		<link href="../../dist/dependencias/dataTables.bootstrap4.min.css" rel="stylesheet" crossorigin="anonymous" />
        <script src="../../dist/dependencias/all.min.js" crossorigin="anonymous"></script>
        
        <link href='../customDist/lib/main.css' rel='stylesheet' />
        <script src='../customDist/lib/main.js'></script>
        <script src='../customDist/lib/locales-all.js'></script>  

        <?php include '../customDist/lib/calendar.php'?>  
    
    </head>
                <main>
                  <div class="container-fluid">
                    <br>
                         <div class="row">
                            <!-- INFROMAÇÕES PARA AGENDAMENTO -->			
                            <div class="col-xl-6">
                                <form role="form" action="" method='post' id="formAgendamento" enctype="multipart/form-data">  
                                      
                                        <div id='calendar'>
                                        </div>

                                </form>
                                 <!-- FIM INFORMAÇÕES PARA AGENDAMENTO -->        
                                </div>
                            </div>

                        </div>
                        

						
                    </main>
					
                <footer class="py-4 bg-light mt-auto">
                    <div class="container-fluid">
                        <div class="d-flex align-items-center justify-content-between small">
                            <div class="text-muted">Desenvolvido por DANILO 2059</div>
                            <div>
                                <a href="#">Poltícia de Privacidade</a>
                                &middot;
                                <a href="#">Termos &amp; Condições</a>
                            </div>
                        </div>
                    </div>
                </footer>
				
            </div>
        </div>

			
       
<script src="../../dist/dependencias/jquery-3.5.1.min.js" crossorigin="anonymous"></script>
        

<script src="../../dist/dependencias/jquery.min.js"></script>
<link rel="stylesheet" href="../../dist/dependencias/jquery-ui.css">
<script src="../../dist/dependencias/jquery-ui.min.js"></script>

<script src="../../dist/dependencias/bootstrap.bundle.min.js" crossorigin="anonymous"></script>
<script src="../../dist/js/scripts.js"></script>

<link href="//cdnjs.cloudflare.com/ajax/libs/select2/4.0.0/css/select2.min.css" rel="stylesheet" />
<script src="//cdnjs.cloudflare.com/ajax/libs/select2/4.0.0/js/select2.min.js"></script> 


<script>
// function dataDinamica(arg){

//             $(document).ready(function() {
// 			table = $('#listar-disponibilidade').DataTable({	
//                 "language": {
//                    "url": "../../dist/locale/datatable-pt-br.json"
//                 },		
//                 "destroy": true, // Para destruir(resetar) o dataTable sempre que fechado. 
// 				"processing": true,
// 				"serverSide": true,
//                 "lengthMenu": [ [25, 50, 100], [25, 50, 100] ],
// 				"ajax": {
// 					"url": "procDisponibilidade.php",
//                     "data": {
//              			   data : arg
//     	          },
// 					"type": "POST"
// 				}
// 			});
// 		});

//     }   
        
</script>

<script>
// function dataDinamica2(arg){

//         $(document).ready(function() {
//             //e.preventDefault();
//             //var id = $(this).data('id');
//             //confirm("Editar Serviço ? " +id);
            
//             var xmlhttp = new XMLHttpRequest();
//             xmlhttp.onreadystatechange = function() {
//             if (this.readyState == 4 && this.status == 200) {
//             var result = JSON.parse(this.responseText);
            
//             document.getElementById("disponivel").innerHTML = result[0][1];
//             document.getElementById("agendado").innerHTML = result[0][0];

//             }
//             };
//             xmlhttp.open("GET","operacoesQtd.php?id="+arg, true);
//             xmlhttp.send();
// 		});
//     }   
        //table.destroy(); -> Possibilidade de destruir o dataTABLE quando fechar o modal(Ideia)
</script>



    <script>
    // var mask = "HH:MM",
    // pattern = {
    //     'translation': {
    //         'H': {
    //             pattern: /[0-99]/
    //         },
    //         'M': {
    //             pattern: /[0-99]/
    //         }
    //     }
    // };

    // $("#horarioInicial").mask(mask, pattern);
    // $("#horarioFinal").mask(mask, pattern);
    </script>

    </body>
</html>
