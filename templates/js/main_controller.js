    	app.controller('GetCtrl', ['$scope', '$http', 'Users', function($scope, $http, Users)	{
         
		$scope.id = null;
		$scope.button = "Inserir";

		Users.get(function(data) {
   			$scope.list = data.users;
   			console.log(data.users);
 		});

		$scope.insertResults = function() {			
					
				var user = new Users();
				user.name = $scope.name;
 				user.password = $scope.password;
 				user.cpf = $scope.cpf;
 				user.telefone = $scope.telefone;
  				
  				if ($scope.id == null) user.$save();
  				else user.$update( { public_id: $scope.id });  		

			    history.go(0);
			};

		
		$scope.Editar = function (public_id){

			$scope.button = "Alterar";			
			Users.get({ public_id: public_id }, function(data)
			{	
				$scope.id = data.user.public_id;
				$scope.name = data.user.name;
				$scope.password = data.user.password;
				$scope.cpf = data.user.cpf;
				$scope.telefone = data.user.telefone;
				console.log(data.user);
			});
			};
		
		$scope.Delete = function deletar(public_id){
		
			Users.remove({ public_id: public_id });
			console.log("Usuario excluido");
			history.go(0);
		};
		
		
		
		$scope.delete = function(public_id)
		{
			$scope.search_delete = public_id;
		};
		
		$scope.select = function(){
			this.setSelectionRange(0, this.value.length);
		}
		
			
		}])
	
	app.config(function($interpolateProvider) {
		$interpolateProvider.startSymbol("[[");
		$interpolateProvider.endSymbol("]]");
	});
  