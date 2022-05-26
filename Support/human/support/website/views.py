from django.shortcuts import render
from django.shortcuts import render


from .models import Custom, Category


def get_flow(post_data):
    data = {}
    for key, value in post_data.items():
        if 'flow' in key:
            custom = key.replace('-flow', '')
            if value:
                data[custom] = value
    
    return data

def get_textarea(post_data):
    data = {}
    for key, value in post_data.items():
        if 'textarea' in key:
            customm = key.replace('-textarea', '')
            if value:
                data[customm] = value
    return data
    




def index(request):
    return render(request, 'website/index.html')


def customs(request):
    customs = Custom.objects.all()
    
    FLOW_CHOICES = ['Slow','Medium','Fast', '----']
    context = {
        'customs': customs,
        'FLOW_CHOICES': FLOW_CHOICES,
    }
    
    
    if request.method == 'POST':
        if  'Close' in request.POST.values():
            for key, value in request.POST.items():
                if 'Close' == value:
                    custom = customs.filter(md_name=key).get()
                    custom.opened = False
                    custom.save()
                    
        elif 'Open' in request.POST.values():
            for key, value in request.POST.items():
                if 'Open' == value:
                    custom = customs.filter(md_name=key).get()
                    custom.opened = True
                    custom.save()
        
        else:
            flow_data = get_flow(request.POST)
            if flow_data:
                for key, value in flow_data.items():
                    custom = customs.filter(md_name=key).get()
                    custom.flow = value
                    custom.save()

            textArea_data = get_textarea(request.POST)
            
            if textArea_data:
                for key, value in textArea_data.items():
                    custom = customs.filter(md_name=key).get()
                    custom.complementary_text = value
                    custom.save()
    return render(request, 'website/customs.html', context)



def categories(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    
    
    if request.method == 'POST':
        if  'Allow' in request.POST.values():
            for key, value in request.POST.items():
                if 'Allow' == value:
                    category = categories.filter(name=key).get()
                    category.allow_complete = True
                    category.save()

        elif  'Not allow' in request.POST.values():
            for key, value in request.POST.items():
                if 'Not allow' == value:
                    category = categories.filter(name=key).get()
                    category.allow_complete = False
                    category.save()
                    
                    
                    
        elif  'Activate' in request.POST.values():
            for key, value in request.POST.items():
                if 'Activate' == value:
                    category = categories.filter(name=key).get()
                    category.active = True
                    category.save()
                    
        elif  'Deactivate' in request.POST.values():
            for key, value in request.POST.items():
                if 'Deactivate' == value:
                    category = categories.filter(name=key).get()
                    category.active = False
                    category.save()
                    
        else:
            textArea_data = get_textarea(request.POST)
            
            if textArea_data:
                for key, value in textArea_data.items():
                    category = categories.filter(name=key).get()
                    category.default_text = value
                    category.save()
                    
                    
        
    
    
    
    
    
    return render(request, 'website/categories.html', context)