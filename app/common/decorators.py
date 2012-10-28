from common import debugconstants, egg_errors

def authenticated(fn):
    def new_f(*args, **kwargs):
        instance = args[0]

        if debugconstants.eggAuthenticate==True and not instance.current_user :
            instance.write( egg_errors.UnauthenticatedException().get_json() )
            return

        fn(instance, *args[1:], **kwargs)

    return new_f

