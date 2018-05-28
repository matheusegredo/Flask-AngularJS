app.factory('Users', ['$resource', function($resource) {
  			return $resource('/users/:public_id', null, 
  				{
  					'update': { method: 'PUT'}
  				});
		}]);