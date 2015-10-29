(function() {
  'use strict';

  /* Declare app level module which depends on filters, and services */
  var app, app_name;

  app_name = 'clavutich';

  app = angular.module(app_name, [app_name + ".controllers", 'ng.django.forms', 'ui.bootstrap', 'ngAnimate', 'duScroll']);

  app.config([
    '$httpProvider', function($httpProvider) {
      $httpProvider.defaults.xsrfCookieName = 'csrftoken';
      $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
      return $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    }
  ]);

}).call(this);

(function() {
  'use strict';

  /* Controllers */
  var app, app_name;

  app_name = "clavutich";

  app = angular.module(app_name + ".controllers", []);

  app.controller('MyFormCtrl', [
    '$http', '$scope', '$window', 'djangoForm', '$document', function($http, $scope, $window, djangoForm, $document) {
      $scope.alerts = [];
      $scope.closeAlert = function(index) {
        return $scope.alerts.splice(index, 1);
      };
      return $scope.submit = function() {
        $scope.disabled = true;
        if ($scope.feedback) {
          $http.post(".", $scope.feedback).success(function(data) {
            var duration, offset, someElement;
            if (!djangoForm.setErrors($scope.form_comment, data.errors)) {
              duration = 800;
              offset = 100;
              $scope.alerts.unshift({
                msg: data.msg,
                type: 'success'
              });
              someElement = angular.element(document.getElementById('alerts'));
              return $document.scrollToElement(someElement, offset, duration);
            }
          }).error(function() {
            return console.error('An error occurred during submission');
          });
        }
        $scope.disabled = false;
        return false;
      };
    }
  ]);

  app.directive('alertSuccess', ['$scope', function($scope) {}]);

}).call(this);

(function() {
  'use strict';

  /* Declare app level module which depends on filters, and services */
  var app, app_name;

  app_name = 'catalog';

  app = angular.module(app_name, [app_name + ".controllers", 'ui.bootstrap', 'ngAnimate', 'duScroll']);

  app.config([
    '$httpProvider', function($httpProvider) {
      $httpProvider.defaults.xsrfCookieName = 'csrftoken';
      $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
      return $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    }
  ]);

}).call(this);

(function() {
  'use strict';

  /* Controllers */
  var app, app_name;

  app_name = "catalog";

  app = angular.module(app_name + ".controllers", []);

  app.controller('Product', [
    '$http', '$scope', '$window', '$document', function($http, $scope, $window, $document) {
      $scope.alerts = [];
      $scope.quantity = 1;
      $scope.closeAlert = function(index) {
        return $scope.alerts.splice(index, 1);
      };
      return $scope.add_to_cart = function() {
        $scope.disabled = true;
        if ($scope.quantity < 1) {
          return false;
        }
        $http.post($scope.action, {
          quantity: $scope.quantity
        }).success(function(data) {
          var alerts, duration, offset;
          duration = 800;
          offset = 100;
          $scope.alerts.unshift({
            msg: data.msg,
            type: 'success'
          });
          alerts = angular.element(document.getElementById('alerts'));
          return $document.scrollToElement(alerts, offset, duration);
        }).error(function() {
          return console.error('An error occurred during submission');
        });
        $scope.disabled = false;
        return false;
      };
    }
  ]);

  app.directive('alertSuccess', ['$scope', function($scope) {}]);

}).call(this);

(function() {
  'use strict';

  /* Declare app level module which depends on filters, and services */
  var app, app_name;

  app_name = 'easy_cart';

  app = angular.module(app_name, [app_name + ".controllers", 'ng.django.forms', 'ui.bootstrap', 'ngAnimate', 'duScroll']);

  app.config([
    '$httpProvider', function($httpProvider) {
      $httpProvider.defaults.xsrfCookieName = 'csrftoken';
      $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
      return $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    }
  ]);

}).call(this);

(function() {
  'use strict';

  /* Controllers */
  var app, app_name;

  app_name = "easy_cart";

  app = angular.module(app_name + ".controllers", []);

  app.controller('Products', [
    '$http', '$scope', '$window', '$document', function($http, $scope, $window, $document) {
      var duration, offset;
      duration = 800;
      offset = 100;
      $scope.alerts = [];
      $http.post('/cart/').success(function(data) {
        return $scope.products = data.products;
      }).error(function() {
        return console.error('An error occurred during submission');
      });
      $scope.update_quantity = function(product) {
        if ($scope.quantity < 1) {
          return false;
        }
        return $http.post($scope.action_update_quantity_product, {
          product_pk: product.pk,
          quantity: product.quantity
        }).success(function(data) {
          var alerts;
          $scope.alerts.unshift({
            msg: data.msg,
            type: 'success'
          });
          alerts = angular.element(document.getElementById('alerts'));
          return $document.scrollToElement(alerts, offset, duration);
        }).error(function() {
          return console.error('An error occurred during submission');
        });
      };
      return $scope.remove = function(index, product) {
        $scope.closeAlert = function(index_alert) {
          return $scope.alerts.splice(index_alert, 1);
        };
        $scope.disabled = true;
        $http.post($scope.action_remove, {
          product_pk: product.pk
        }).success(function(data) {
          var alerts;
          $scope.products.splice(index, 1);
          $scope.alerts.unshift({
            msg: data.msg,
            type: 'success'
          });
          if (!$scope.products.length) {
            $('#cart').remove();
            $('#btn-checkout').remove();
            $scope.alerts.unshift({
              msg: 'Ваша корзина пустая.',
              type: 'info'
            });
          }
          alerts = angular.element(document.getElementById('alerts'));
          return $document.scrollToElement(alerts, offset, duration);
        }).error(function() {
          return console.error('An error occurred during submission');
        });
        $scope.disabled = false;
        return false;
      };
    }
  ]);

}).call(this);
