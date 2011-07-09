from forms import WebToPayResponseForm

def callback(request):
    data = request.GET.copy()
    form = WebToPayResponseForm(data)

    if form.is_valid():
        # Get a model instance out of form
        resp_obj = form.save(commit=False)
