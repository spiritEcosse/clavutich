'use strict'

### Controllers ###

app_name = "catalog"
app = angular.module "#{app_name}.controllers", []

app.controller 'Product', ['$http', '$scope', '$window', '$document', ($http, $scope, $window, $document) ->
  $scope.alerts = []
  $scope.quantity = 1
  duration = 800
  offset = 100
  alerts = angular.element(document.getElementById('alerts'))

  $scope.closeAlert = (index) ->
    $scope.alerts.splice(index, 1)

  $scope.add_to_cart = ->
    $scope.disabled = true
    if $scope.quantity < 1
      return false

    $http.post('/catalog/product_add_to_cart/' + $scope.product.pk + '/', {quantity: $scope.quantity}).success (data) ->
      $scope.alerts.unshift({msg: data.msg, type: 'success'})
      $document.scrollToElement(alerts, offset, duration)
      $scope.disabled = false
    .error ->
      console.error('An error occurred during submission')

    return false
]
app.directive 'alertSuccess', ['$scope', ($scope) ->

]