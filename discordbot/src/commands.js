/**
 * Share command metadata from a common spot to be used for both runtime
 * and registration.
 */


export const REGISTER = {
    name: 'register',
    description: 'will get email and password from user and create a tokens for user',
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



