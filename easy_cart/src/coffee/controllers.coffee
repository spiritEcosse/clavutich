'use strict'

### Controllers ###

app_name = "easy_cart"
app = angular.module "#{app_name}.controllers", []

app.controller 'Products', ['$http', '$scope', '$window', '$document', ($http, $scope, $window, $document) ->
  duration = 800
  offset = 100
  $scope.alerts = []

  $http.post('/cart/').success (data) ->
    $scope.products = data.products
  .error ->
    console.error('An error occurred during submission')

  $scope.update_quantity = (product) ->
    if $scope.quantity < 1
      return false

    $http.post($scope.action_update_quantity_product, {product_pk: product.pk, quantity: product.quantity}).success (data) ->
      $scope.alerts.unshift({msg: data.msg, type: 'success'})
      alerts = angular.element(document.getElementById('alerts'))
      $document.scrollToElement(alerts, offset, duration)
    .error ->
      console.error('An error occurred during submission')

  $scope.remove = (index, product) ->
    $scope.closeAlert = (index_alert) ->
      $scope.alerts.splice(index_alert, 1)

    $scope.disabled = true

    $http.post($scope.action_remove, {product_pk: product.pk}).success (data) ->
      $scope.products.splice(index, 1)
      $scope.alerts.unshift({msg: data.msg, type: 'success'})

      if not $scope.products.length
        $('#cart').remove()
        $('#btn-checkout').remove()
        $scope.alerts.unshift({msg: 'Ваша корзина пустая.', type: 'info'})

      alerts = angular.element(document.getElementById('alerts'))
      $document.scrollToElement(alerts, offset, duration)
    .error ->
      console.error('An error occurred during submission')

    $scope.disabled = false
    return false
]
