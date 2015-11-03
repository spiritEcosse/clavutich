'use strict'

### Controllers ###

app_name = "clavutich"
app = angular.module "#{app_name}.controllers", []

app.controller 'MyFormCtrl', ['$http', '$scope', '$window', 'djangoForm', '$document', ($http, $scope, $window, djangoForm, $document) ->
  $scope.alerts = []
  duration = 800
  offset = 100
  alerts = angular.element(document.getElementById('alerts'));
  $scope.disabled_form = false

  $scope.closeAlert = (index) ->
    $scope.alerts.splice(index, 1)

  $scope.submit = ->
    $scope.disabled_form = true

    if $scope.feedback
      $http.post(".", $scope.feedback).success (data) ->
        if not djangoForm.setErrors($scope.form_comment, data.errors)
          $scope.alerts.unshift({msg: data.msg, type: 'success'})
          $document.scrollToElement(alerts, offset, duration)
        $scope.disabled_form = false
      .error ->
        console.error('An error occurred during submission')

    return false
]
app.directive 'alertSuccess', ['$scope', ($scope) ->

]