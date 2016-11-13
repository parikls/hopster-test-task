angular.module("movieCatalogue")
    .controller("LoginController", LoginController);

LoginController.$inject = ["authService", "messageService"];

function LoginController(authService, messageService) {

    var vm = this;

    activate();

    function activate() {
        vm.submitForm = submitForm;
        vm.messages = messageService.messages;
    }

    function submitForm() {

        if (vm.credentials) {
            authService.login(vm.credentials);
        } else {
            messageService.errorAuth("Credentials cannot be blank");

        }
    }
}