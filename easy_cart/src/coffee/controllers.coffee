'use strict'

### Controllers ###

app_name = "easy_cart"
app = angular.module "#{app_name}.controllers", []

app.controller 'Products', ['$http', '$scope', '$window', 'djangoForm', '$document', ($http, $scope, $window, djangoForm, $document) ->
  duration = 800
  offset = 100
  $scope.alerts = []
  alerts = angular.element(document.getElementById('alerts'))
  $scope.disabled_form = false

  $http.post('/cart/').success (data) ->
    $scope.products = data.products
  .error ->
    console.error('An error occurred during submission')

  $scope.update_quantity = (product) ->
    if product.quantity < 1
      return false

    $http.post('/cart/update_quantity_product/' + product.pk + '/', {quantity: product.quantity}).success (data) ->
      $scope.alerts.unshift({msg: data.msg, type: 'success'})
      $document.scrollToElement(alerts, offset, duration)
    .error ->
      console.error('An error occurred during submission')

  $scope.closeAlert = (index_alert) ->
    $scope.alerts.splice(index_alert, 1)

  $scope.submit = ->
    $scope.disabled_form = true

    if $scope.user_data
      $http.post("/cart/order/", $scope.user_data).success (data) ->
        if not djangoForm.setErrors($scope.form_user_data, data.errors)
          $scope.alerts.unshift({msg: data.msg, type: 'success'})
          $document.scrollToElement(alerts, offset, duration)
          $scope.products = []
        $scope.disabled_form = false
      .error ->
        console.error('An error occurred during submission')

    return false

  $scope.remove = (index, product) ->
    $http.post('/cart/remove/' + product.pk + '/').success (data) ->
      $scope.alerts.unshift({msg: data.msg, type: 'success'})
      $document.scrollToElement(alerts, offset, duration)
      $scope.products.splice(index, 1)
    .error ->
      console.error('An error occurred during submission')

    return false
]
