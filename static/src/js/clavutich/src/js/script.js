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
      var alerts, duration, offset;
      $scope.alerts = [];
      duration = 800;
      offset = 100;
      alerts = angular.element(document.getElementById('alerts'));
      $scope.disabled_form = false;
      $scope.closeAlert = function(index) {
        return $scope.alerts.splice(index, 1);
      };
      return $scope.submit = function() {
        $scope.disabled_form = true;
        if ($scope.feedback) {
          $http.post(".", $scope.feedback).success(function(data) {
            if (!djangoForm.setErrors($scope.form_comment, data.errors)) {
              $scope.alerts.unshift({
                msg: data.msg,
                type: 'success'
              });
              $document.scrollToElement(alerts, offset, duration);
            }
            return $scope.disabled_form = false;
          }).error(function() {
            return console.error('An error occurred during submission');
          });
        }
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
    '$http', '$scope', '$window', 'djangoForm', '$document', function($http, $scope, $window, djangoForm, $document) {
      var alerts, duration, offset;
      duration = 800;
      offset = 100;
      $scope.alerts = [];
      alerts = angular.element(document.getElementById('alerts'));
      $scope.disabled_form = false;
      $http.post('/cart/').success(function(data) {
        return $scope.products = data.products;
      }).error(function() {
        return console.error('An error occurred during submission');
      });
      $scope.update_quantity = function(product) {
        if (product.quantity < 1) {
          return false;
        }
        return $http.post('/cart/update_quantity_product/' + product.pk + '/', {
          quantity: product.quantity
        }).success(function(data) {
          $scope.alerts.unshift({
            msg: data.msg,
            type: 'success'
          });
          return $document.scrollToElement(alerts, offset, duration);
        }).error(function() {
          return console.error('An error occurred during submission');
        });
      };
      $scope.closeAlert = function(index_alert) {
        return $scope.alerts.splice(index_alert, 1);
      };
      $scope.submit = function() {
        $scope.disabled_form = true;
        if ($scope.user_data) {
          $http.post("/cart/order/", $scope.user_data).success(function(data) {
            if (!djangoForm.setErrors($scope.form_user_data, data.errors)) {
              $scope.alerts.unshift({
                msg: data.msg,
                type: 'success'
              });
              $document.scrollToElement(alerts, offset, duration);
              $scope.products = [];
            }
            return $scope.disabled_form = false;
          }).error(function() {
            return console.error('An error occurred during submission');
          });
        }
        return false;
      };
      return $scope.remove = function(index, product) {
        $http.post('/cart/remove/' + product.pk + '/').success(function(data) {
          $scope.alerts.unshift({
            msg: data.msg,
            type: 'success'
          });
          $document.scrollToElement(alerts, offset, duration);
          return $scope.products.splice(index, 1);
        }).error(function() {
          return console.error('An error occurred during submission');
        });
        return false;
      };
    }
  ]);

}).call(this);
