'use strict'

### Controllers ###

app_name = "catalog"
app = angular.module "#{app_name}.controllers", []

app.controller 'Product', ['$http', '$scope', '$window', '$document', ($http, $scope, $window, $document) ->
  $scope.alerts = []
  $scope.quantity = 1
  $scope.closeAlert = (index) ->
    $scope.alerts.splice(index, 1)

  $scope.add_to_cart = ->
    $scope.disabled = true
    if $scope.quantity < 1
      return false

    $http.post($scope.action, {quantity: $scope.quantity}).success (data) ->
      duration = 800
      offset = 100
      $scope.alerts.unshift({msg: data.msg, type: 'success'})
      alerts = angular.element(document.getElementById('alerts'))
      $document.scrollToElement(alerts, offset, duration)
    .error ->
      console.error('An error occurred during submission')

    $scope.disabled = false
    return false
]
app.directive 'alertSuccess', ['$scope', ($scope) ->

]