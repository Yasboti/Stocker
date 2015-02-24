var app = angular.module('app', ['angular-carousel']);

// app.controller('Charts', ['$scope', function($scope) {
app.controller('Charts', ['$scope', Charts]);

function Charts($scope) {
  $scope.symbolString = 'MSFT AAPL TSLA';
  $scope.stub = 'http://chart.finance.yahoo.com/z?z=s&t=6m&s=';

  this.urls = [];
  var symbols = $scope.symbolString.split(' ');

  for(i in symbols)
    this.urls.push(symbols[i]);
};

// so this is kind of functional: take a value, do something to it, return result
// app.factory('urls', ['symbols', function chartUrlFactory(symbols) {
//       urls = [];
//   s = symbols.split(' ')
//   for(i in s)
//     urls.push(stub + s[i]);
//   return urls;
// }]);

// app.controller('ImageList', ['urls', function(urls) {
//   console.log('in controller')
//   this.images = [];
//   for(i in urls)
//     this.images.push(urls[i]);
// }]);

// setTimeout(function(){ console.log(); }, 1000);
