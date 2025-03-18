/**
 * Share command metadata from a common spot to be used for both runtime
 * and registration.
 */
//CONTAINS REGISTER, LOGIN, LOGOUT, DELETE, NOTIFY, FORCEORDER, ORDER, CANCELORDER, GETORDERS

export const REGISTER = {
    name: 'register',
    description: 'will get email and password from user and create a tokens for user',
}
export const LOGIN = {
    name: 'login',
    description: 'will allow user to login to an account based on discord uid',
}
export const LOGOUT = {
    name: 'logout',
    description: 'will logout user from account',
}
export const DELETE = {
    name: 'delete',
    description: 'Deletes tokens for user',
}
export const NOTIFY = {
    name: 'notify',
    description: 'Will notify user about the status of too good to go stores',
}
export const FORCEORDER = {
    name: 'forceorder',
    description: 'Will force order for user',
}
export const ORDER = {
    name: 'order',
    description: 'Will order for user',
}
export const CANCELORDER = {
    name  : 'cancelorder',
    description: 'Will cancel order for user',
}
export const GETORDERS = {
    name: 'getorders',
    description: 'Will get all orders for user',
}



