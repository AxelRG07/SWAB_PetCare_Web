from django.shortcuts import redirect

def grupo_requerido(nombre_grupo):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('signin')
            
            if request.user.groups.filter(name=nombre_grupo).exists():
                return view_func(request, *args, **kwargs)
            else:
                return redirect('index') 
        return wrapper_func
    return decorator