'''@loginRequired'''
sessionValidationSchema = {
    'type' : 'object', 
    'properties' : {
        'token' : {
            'type' : 'string'
        }, 
        'username' : {
            'type' : 'string', 
            'minLength' : 1,
            'maxLength' : 40
        }
    }, 
    'required' : ['token', 'username']
}


'''/sign-up'''
signUpSchema = {
    'type' : 'object', 
    'properties' : {
        'username' : {
                        'type' : 'string', 
                        'minLength' : 1, 
                        'maxLength' : 20
                    }, 
        'password' : {
                        'type' : 'string', 
                        'minLength' : 7, 
                        'maxLength' : 40, 
                    }
    }, 
    'required' : ['username', 'password']
}